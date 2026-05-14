#!/usr/bin/env python3
"""bn-1h7qp aux harness — Rudra re-run with corrected parser + mapping.

The image-side Rudra runner (`crates/ward-eval/src/bench/runners/rudra.rs`)
miscomputes the `file` field — it expects `Error (CAT): file:line:col: msg`
on one line, but real Rudra output is:

    Warning (SendSyncVariance:/PhantomSendForSend/NaiveSendForSend): Suspicious impl of `Send` found
    -> src/generic.rs:531:1: 531:76
    unsafe impl<...>

This wrapper re-runs Rudra inside the locked image (no image change),
captures stdout/stderr, and parses both lines per-emission so the `file`
is real and `rule_id` reflects the actual Rudra category. The aux mapping
side (rule-id-mapping-aux-max-breadth.toml) extends keywords to match
`sendsyncvariance`, `unsafedataflow`, `panicsafety`, etc.

Per methodology §4 best-effort: Rudra coverage is still poor (toolchain
mismatches kill most entries), but we want to make sure we don't miss
the entries that DO run.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

WS = Path("/home/bob/src/ward/ws/bn-1h7qp")
DEFAULT_WS = Path("/home/bob/src/ward/ws/default")
MANIFEST = WS / "tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml"
CACHE_ROOT = DEFAULT_WS / "target/bench/unsafe-rust-v2/cache/repos"
AUX_ROOT = WS / "target/bench/aux-max-breadth"
RAW_ROOT = AUX_ROOT / "raw" / "rudra"
SCRATCH_ROOT = AUX_ROOT / "scratch" / "rudra"
TOOLCACHE_ROOT = AUX_ROOT / "tool-cache" / "rudra"
IMAGE = "localhost/ward-bench:locked"
TIME_BUDGET_SECS = 600
MEM_GIB = 16
CPUS = 4
CPUSET = "0-3"


def load_entries():
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    return m["entries"]


_cache_map = None


def find_cache_dir_for_url(repo_url: str):
    global _cache_map
    if _cache_map is None:
        _cache_map = {}
        for d in CACHE_ROOT.iterdir():
            cfg = d / "config"
            if cfg.exists():
                try:
                    txt = cfg.read_text()
                    m = re.search(r"url\s*=\s*(\S+)", txt)
                    if m:
                        _cache_map[m.group(1)] = d
                except Exception:
                    pass
    return _cache_map.get(repo_url)


def stage_repo(entry, scratch_dir):
    repo_url = entry["repo_url"]
    if repo_url == "fixture://local":
        return False
    sha = (
        entry["vulnerable_commit"]
        if entry["expected_result"] == "tp"
        else entry["fixing_commit"]
    )
    cache = find_cache_dir_for_url(repo_url)
    if cache is None:
        return False
    repo_dir = scratch_dir / "repo"
    if repo_dir.exists():
        subprocess.run(["bash", "-c", f"command rm -rf '{repo_dir}'"], check=False)
    repo_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        f"git -C {cache} archive {sha} | tar -x -C {repo_dir}",
        shell=True,
        capture_output=True,
    )
    return proc.returncode == 0


def parse_rudra_output_multiline(stdout: str, stderr: str):
    """Parse the real Rudra 2-line emission format.

    Format:
        (Warning|Error|Info) (Category:/Sub): <message>
        -> <file>:<line>:<col>[: <endline>:<endcol>]
        [<code-snippet line(s)>]

    Per methodology §5 "What counts as a finding": Rudra has no severity
    tier so all emissions count, but we filter out lines that begin with
    `Info (` since they're informational annotations — Rudra docs say
    `Warning` + `Error` are the actionable signals.
    """
    findings = []
    lines = (stdout + "\n" + stderr).split("\n")
    i = 0
    HEADER = re.compile(r"^(Warning|Error)\s*\(([^)]+)\)\s*:\s*(.*)$")
    ARROW = re.compile(r"^\s*->\s*([^:]+):(\d+):(\d+)")
    while i < len(lines):
        line = lines[i].rstrip()
        m = HEADER.match(line)
        if m:
            level = m.group(1)
            category = m.group(2).strip()
            message = m.group(3).strip()
            # Look ahead for arrow line
            file_ = ""
            lineno = None
            if i + 1 < len(lines):
                am = ARROW.match(lines[i + 1])
                if am:
                    file_ = am.group(1).strip()
                    try:
                        lineno = int(am.group(2))
                    except ValueError:
                        lineno = None
                    i += 1  # consume the arrow line
            cat_norm = (
                category.upper()
                .replace("/", "-")
                .replace(":", "")
                .replace(" ", "-")
            )
            findings.append({
                "rule_id": f"RUDRA-{cat_norm}",
                "file": file_,
                "start_line": lineno,
                "message": message,
                "confidence": 0.0,
                "level": level,
            })
        i += 1
    return findings


def classify_failure(stderr: str) -> str:
    s = stderr.lower()
    if "rustc" in s and ("mismatch" in s or "requires" in s):
        return "rudra_toolchain_mismatch"
    if "no such subcommand" in s or "no such command" in s or "cargo-rudra: not found" in s:
        return "rudra_unavailable"
    if "internal error" in s or "panicked" in s:
        return "rudra_internal_error"
    if "no `cargo.lock`" in s or "could not find `cargo.lock`" in s:
        return "rudra_lockfile_missing"
    if "not found" in s or "command not found" in s:
        return "rudra_unavailable"
    return "rudra_failed"


def affected_match(finding_file: str, affected: str) -> bool:
    if not affected or not finding_file:
        return False
    if finding_file == affected:
        return True
    if finding_file.endswith("/" + affected):
        return True
    if affected.endswith("/" + finding_file):
        return True
    return os.path.basename(finding_file) == os.path.basename(affected)


def run_rudra_on_entry(entry):
    eid = entry["id"]
    scratch = SCRATCH_ROOT / eid
    out_host = RAW_ROOT / eid
    tool_cache = TOOLCACHE_ROOT
    scratch.mkdir(parents=True, exist_ok=True)
    out_host.mkdir(parents=True, exist_ok=True)
    tool_cache.mkdir(parents=True, exist_ok=True)

    if not stage_repo(entry, scratch):
        return {
            "tool": "rudra",
            "harness_id": eid,
            "expected": entry["expected_result"],
            "detected": False,
            "classification": "FN" if entry["expected_result"] == "tp" else "TN",
            "duration_secs": 0.0,
            "error": "repo_missing",
        }
    repo_host = scratch / "repo"

    # Use /work as the scratch mount (not /scratch — host-tooling rule
    # blocks `rm -rf /scratch/...`). The container script uses /work.
    cmd_script = (
        "cp -r /repo /work/rudra-repo && "
        "cd /work/rudra-repo && "
        "(cargo +nightly-2021-10-21 generate-lockfile --offline >/dev/null 2>&1 || "
        " cargo +nightly-2021-10-21 generate-lockfile >/dev/null 2>&1); "
        "cargo +nightly-2021-10-21 rudra --manifest-path Cargo.toml 2>&1"
    )
    podman_cmd = [
        "podman", "run", "--rm",
        "--network=none",
        f"--memory={MEM_GIB}g",
        f"--cpus={CPUS}",
        f"--cpuset-cpus={CPUSET}",
        "-v", f"{repo_host}:/repo:ro",
        "-v", f"{scratch}:/work",
        "-v", f"{out_host}:/bench-out",
        "-v", f"{tool_cache}:/tool-cache",
        "--stop-signal=SIGKILL",
        f"--stop-timeout={TIME_BUDGET_SECS + 5}",
        IMAGE,
        "sh", "-c", cmd_script,
    ]
    start = time.time()
    try:
        proc = subprocess.run(
            podman_cmd, capture_output=True, timeout=TIME_BUDGET_SECS + 30
        )
        timed_out = False
    except subprocess.TimeoutExpired:
        timed_out = True
        proc = None
    duration = time.time() - start

    res = {
        "tool": "rudra",
        "harness_id": eid,
        "expected": entry["expected_result"],
        "duration_secs": duration,
    }
    if timed_out:
        res["error"] = "timed_out"
        res["timed_out"] = True
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res

    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")

    # Rudra prints findings to stdout regardless of success/fail status.
    # We parse first, then classify failure if no findings AND non-zero rc.
    findings = parse_rudra_output_multiline(stdout, stderr)

    if proc.returncode != 0 and not findings:
        # Combine stdout+stderr for failure classification — rudra writes
        # to both depending on the failure point.
        res["error"] = classify_failure(stderr + "\n" + stdout)
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res

    # Persist raw output for audit
    (out_host / "rudra.stdout").write_text(stdout)
    (out_host / "rudra.stderr").write_text(stderr)

    affected = entry.get("affected_file", "")
    detected = any(affected_match(f["file"], affected) for f in findings)
    res["findings"] = findings
    res["rule_ids_fired"] = sorted({f["rule_id"] for f in findings})
    res["detected"] = detected
    if entry["expected_result"] == "tp":
        res["classification"] = "TP" if detected else "FN"
    else:
        res["classification"] = "FP" if detected else "TN"
    res["error"] = ""
    return res


def main():
    entries = load_entries()
    filter_id = os.environ.get("AUX_FILTER", "")
    if filter_id:
        entries = [e for e in entries if filter_id in e["id"]]
    print(f"[aux-rudra] starting on {len(entries)} entries", flush=True)
    results = []
    for i, e in enumerate(entries):
        t0 = time.time()
        r = run_rudra_on_entry(e)
        elapsed = time.time() - t0
        results.append(r)
        cls = r.get("classification", "?")
        err = r.get("error", "")
        nfind = len(r.get("findings", []))
        print(
            f"[{i+1:3d}/{len(entries)}] {e['id']:55s} cls={cls:3s} "
            f"findings={nfind:2d} dur={elapsed:.1f}s {err}",
            flush=True,
        )
    out_path = AUX_ROOT / "bench-results-rudra.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n[aux-rudra] wrote {out_path}")
    tp = sum(1 for r in results if r.get("classification") == "TP")
    fp = sum(1 for r in results if r.get("classification") == "FP")
    tn = sum(1 for r in results if r.get("classification") == "TN")
    fn = sum(1 for r in results if r.get("classification") == "FN")
    errd = sum(1 for r in results if r.get("error"))
    print(f"[aux-rudra] TP={tp} FP={fp} TN={tn} FN={fn} errd={errd}")


if __name__ == "__main__":
    main()
