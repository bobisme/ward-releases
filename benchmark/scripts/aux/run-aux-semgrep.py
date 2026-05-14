#!/usr/bin/env python3
"""bn-1h7qp aux harness — max-breadth Semgrep run.

Wraps `podman run` against the methodology-locked `ward-bench:locked`
image, but mounts in additional Semgrep rulesets prefetched on the
host to a sibling rules directory. Image content does NOT change; only
the `--config` args do.

Per-entry output schema matches `crates/ward-eval/src/bench/mod.rs::BenchToolResult`
so downstream `bench-score` / `bench-stats` consume it unchanged.

Configs used (4):
  * /aux-rules/p-rust.yml            (canonical methodology = `p/rust`)
  * /aux-rules/r-rust-full.yml       (`r/rust` community pack)
  * /aux-rules/p-security-audit.yml  (cross-language audit pack; ~225 rules; 0 Rust)
  * /aux-rules/p-default.yml         (Semgrep default; 1058 rules; 4 Rust)

The aux run executes against ALL 160 entries of the unsafe-rust manifest.
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
RULES_HOST = AUX_ROOT / "rules"
RAW_ROOT = AUX_ROOT / "raw" / "semgrep"
SCRATCH_ROOT = AUX_ROOT / "scratch" / "semgrep"
TOOLCACHE_ROOT = AUX_ROOT / "tool-cache" / "semgrep"
IMAGE = "localhost/ward-bench:locked"
TIME_BUDGET_SECS = 600
MEM_GIB = 16
CPUS = 4
CPUSET = "0-3"


def load_manifest_entries():
    """Parse the bench manifest TOML (Python 3.11+ tomllib)."""
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    return m["entries"]


def repo_cache_dir(repo_url: str) -> Path:
    """Match `bench_repo_cache_dir` from mod.rs: blake3(repo_url) → 16-hex."""
    # Mod.rs uses blake3; we'll just enumerate cache dirs and try to match
    # by reading each one's `git config remote.origin.url`.
    return CACHE_ROOT  # caller resolves


_cache_map = None


def find_cache_dir_for_url(repo_url: str) -> Path | None:
    global _cache_map
    if _cache_map is None:
        _cache_map = {}
        for d in CACHE_ROOT.iterdir():
            if not d.is_dir():
                continue
            cfg = d / "config"
            if not cfg.exists():
                continue
            try:
                txt = cfg.read_text()
                m = re.search(r"url\s*=\s*(\S+)", txt)
                if m:
                    _cache_map[m.group(1)] = d
            except Exception:
                pass
    return _cache_map.get(repo_url)


def stage_repo(entry: dict, scratch_dir: Path) -> bool:
    """Materialize the repo at the right commit into scratch_dir.

    Uses `git archive` from the cached bare clone, matching mod.rs's
    stage_real_repo_if_needed semantics. Returns True on success.
    """
    repo_url = entry["repo_url"]
    if repo_url == "fixture://local":
        return False  # aux pass doesn't cover fixtures
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
        subprocess.run(["rm", "-rf", str(repo_dir)], check=False)
    repo_dir.mkdir(parents=True, exist_ok=True)
    # git archive <sha> | tar -x in repo_dir
    proc = subprocess.run(
        f"git -C {cache} archive {sha} | tar -x -C {repo_dir}",
        shell=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return False
    return True


def run_semgrep_on_entry(entry: dict) -> dict:
    """Run one entry through podman-wrapped semgrep with broad configs."""
    eid = entry["id"]
    scratch = SCRATCH_ROOT / eid
    out_host = RAW_ROOT / eid
    tool_cache = TOOLCACHE_ROOT
    scratch.mkdir(parents=True, exist_ok=True)
    out_host.mkdir(parents=True, exist_ok=True)
    tool_cache.mkdir(parents=True, exist_ok=True)

    staged = stage_repo(entry, scratch)
    if not staged:
        return {
            "tool": "semgrep",
            "harness_id": eid,
            "expected": entry["expected_result"],
            "detected": False,
            "classification": "FN" if entry["expected_result"] == "tp" else "TN",
            "duration_secs": 0.0,
            "error": "repo_missing",
        }
    repo_host = scratch / "repo"

    sarif_in_container = "/bench-out/semgrep.sarif"
    sarif_host = out_host / "semgrep.sarif"
    # Remove stale sarif so we don't read the previous run's output
    if sarif_host.exists():
        sarif_host.unlink()

    cmd = [
        "podman",
        "run",
        "--rm",
        "--network=none",
        f"--memory={MEM_GIB}g",
        f"--cpus={CPUS}",
        f"--cpuset-cpus={CPUSET}",
        "-v",
        f"{repo_host}:/repo:ro",
        "-v",
        f"{scratch}:/scratch",
        "-v",
        f"{out_host}:/bench-out",
        "-v",
        f"{tool_cache}:/tool-cache",
        "-v",
        f"{RULES_HOST}:/aux-rules:ro",
        "--stop-signal=SIGKILL",
        f"--stop-timeout={TIME_BUDGET_SECS + 5}",
        IMAGE,
        "semgrep",
        "--config", "/aux-rules/p-rust.yml",
        "--config", "/aux-rules/r-rust-full.yml",
        "--config", "/aux-rules/p-security-audit.yml",
        "--config", "/aux-rules/p-default.yml",
        "--sarif",
        "--metrics=off",
        "--quiet",
        "--no-rewrite-rule-ids",
        "--include", "*.rs",
        "--output", sarif_in_container,
        "/repo",
    ]
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=TIME_BUDGET_SECS + 30,
        )
        timed_out = False
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        proc = None
        timed_out = True
        rc = None
    duration = time.time() - start

    res = {
        "tool": "semgrep",
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
    # exit 1 = findings (success); exit 2+ = launch/config failure
    if rc is not None and rc >= 2:
        stderr = proc.stderr.decode("utf-8", "replace") if proc else ""
        stdout = proc.stdout.decode("utf-8", "replace") if proc else ""
        detail = stderr if stderr.strip() else stdout
        last = next(
            (l for l in reversed(detail.splitlines()) if l.strip()),
            "",
        )[:200]
        res["error"] = f"semgrep_failed(exit={rc}): {last}"
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res

    # Parse SARIF
    findings = []
    if sarif_host.exists():
        try:
            with open(sarif_host) as f:
                sarif = json.load(f)
            findings = parse_sarif(sarif, entry)
        except Exception as e:
            res["error"] = f"sarif_parse: {e}"

    # File-level detection + classification
    affected = entry.get("affected_file", "")
    detected = False
    for fdg in findings:
        # File-level basename match
        ff = fdg.get("file", "")
        if affected and (ff == affected or ff.endswith("/" + affected) or os.path.basename(ff) == os.path.basename(affected)):
            detected = True
            break
    res["findings"] = findings
    res["rule_ids_fired"] = sorted({f["rule_id"] for f in findings})
    res["detected"] = detected
    if entry["expected_result"] == "tp":
        res["classification"] = "TP" if detected else "FN"
    else:
        res["classification"] = "FP" if detected else "TN"
    res["error"] = res.get("error", "")
    return res


def parse_sarif(sarif: dict, entry: dict) -> list:
    """Mirror the semgrep.rs parser: drop INFO/INVENTORY/NOTE severities."""
    out = []
    for run in sarif.get("runs", []):
        rule_sev = {}
        for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
            rid = rule.get("id", "")
            sev = (
                rule.get("properties", {}).get("severity")
                or rule.get("defaultConfiguration", {}).get("level")
                or "WARNING"
            ).upper()
            rule_sev[rid] = sev
        for result in run.get("results", []):
            rid = result.get("ruleId", "")
            sev_r = result.get("level", "").upper()
            sev = sev_r or rule_sev.get(rid, "WARNING")
            if sev in ("INFO", "INVENTORY", "NOTE"):
                continue
            msg = result.get("message", {}).get("text", "")
            for loc in result.get("locations", []):
                ploc = loc.get("physicalLocation", {})
                uri = (
                    ploc.get("artifactLocation", {}).get("uri", "").lstrip("./")
                )
                line = ploc.get("region", {}).get("startLine")
                if not uri:
                    continue
                out.append({
                    "rule_id": rid,
                    "file": uri,
                    "start_line": line,
                    "message": msg,
                    "confidence": 0.0,
                })
    return out


def main():
    entries = load_manifest_entries()
    filter_id = os.environ.get("AUX_FILTER", "")
    if filter_id:
        entries = [e for e in entries if filter_id in e["id"]]
    print(f"[aux-semgrep] starting on {len(entries)} entries", flush=True)
    results = []
    for i, e in enumerate(entries):
        t0 = time.time()
        r = run_semgrep_on_entry(e)
        elapsed = time.time() - t0
        results.append(r)
        cls = r.get("classification", "?")
        err = r.get("error", "")
        nrules = len(r.get("rule_ids_fired", []))
        print(
            f"[{i+1:3d}/{len(entries)}] {e['id']:55s} cls={cls:3s} "
            f"rules_fired={nrules:2d} dur={elapsed:.1f}s {err}",
            flush=True,
        )
    out_path = AUX_ROOT / "bench-results-semgrep.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n[aux-semgrep] wrote {out_path}")
    # Summary
    tp = sum(1 for r in results if r.get("classification") == "TP")
    fp = sum(1 for r in results if r.get("classification") == "FP")
    tn = sum(1 for r in results if r.get("classification") == "TN")
    fn = sum(1 for r in results if r.get("classification") == "FN")
    errd = sum(1 for r in results if r.get("error"))
    print(f"[aux-semgrep] TP={tp} FP={fp} TN={tn} FN={fn} errd={errd}")


if __name__ == "__main__":
    main()
