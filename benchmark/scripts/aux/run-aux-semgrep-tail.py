#!/usr/bin/env python3
"""bn-1h7qp aux harness — Semgrep tail-half parallel runner.

Processes entries 80..159 of the manifest. Uses cpuset 4-7 (not 0-3)
so it doesn't fight the main run for cores. Memory cap unchanged
(16 GiB). Writes to a sibling output dir to avoid scratch conflict.
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
AUX_ROOT = WS / "target/bench/aux-max-breadth-tail"
RULES_HOST = WS / "target/bench/aux-max-breadth/rules"
RAW_ROOT = AUX_ROOT / "raw" / "semgrep"
SCRATCH_ROOT = AUX_ROOT / "scratch" / "semgrep"
TOOLCACHE_ROOT = AUX_ROOT / "tool-cache" / "semgrep"
IMAGE = "localhost/ward-bench:locked"
TIME_BUDGET_SECS = 600
MEM_GIB = 16
CPUS = 4
CPUSET = "4-7"  # distinct from main run's 0-3


def load_manifest_entries():
    import tomllib
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


def parse_sarif(sarif: dict, entry):
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
            sev = (result.get("level", "").upper()
                   or rule_sev.get(rid, "WARNING"))
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


def run_one(entry):
    eid = entry["id"]
    scratch = SCRATCH_ROOT / eid
    out_host = RAW_ROOT / eid
    tool_cache = TOOLCACHE_ROOT
    scratch.mkdir(parents=True, exist_ok=True)
    out_host.mkdir(parents=True, exist_ok=True)
    tool_cache.mkdir(parents=True, exist_ok=True)

    if not stage_repo(entry, scratch):
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

    sarif_host = out_host / "semgrep.sarif"
    if sarif_host.exists():
        sarif_host.unlink()

    cmd = [
        "podman", "run", "--rm",
        "--network=none",
        f"--memory={MEM_GIB}g",
        f"--cpus={CPUS}",
        f"--cpuset-cpus={CPUSET}",
        "-v", f"{repo_host}:/repo:ro",
        "-v", f"{scratch}:/scratch",
        "-v", f"{out_host}:/bench-out",
        "-v", f"{tool_cache}:/tool-cache",
        "-v", f"{RULES_HOST}:/aux-rules:ro",
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
        "--output", "/bench-out/semgrep.sarif",
        "/repo",
    ]
    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=TIME_BUDGET_SECS + 30)
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
    if rc is not None and rc >= 2:
        stderr = proc.stderr.decode("utf-8", "replace") if proc else ""
        stdout = proc.stdout.decode("utf-8", "replace") if proc else ""
        detail = stderr if stderr.strip() else stdout
        last = next(
            (l for l in reversed(detail.splitlines()) if l.strip()), ""
        )[:200]
        res["error"] = f"semgrep_failed(exit={rc}): {last}"
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res

    findings = []
    if sarif_host.exists():
        try:
            with open(sarif_host) as f:
                sarif = json.load(f)
            findings = parse_sarif(sarif, entry)
        except Exception as e:
            res["error"] = f"sarif_parse: {e}"

    affected = entry.get("affected_file", "")
    detected = False
    for fdg in findings:
        ff = fdg.get("file", "")
        if affected and (
            ff == affected
            or ff.endswith("/" + affected)
            or os.path.basename(ff) == os.path.basename(affected)
        ):
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


def main():
    entries = load_manifest_entries()
    # Process the LAST HALF (idx 80..159)
    entries = entries[80:160]
    print(f"[aux-semgrep-tail] starting on {len(entries)} entries (manifest idx 80..159, cpuset {CPUSET})", flush=True)
    results = []
    for i, e in enumerate(entries):
        t0 = time.time()
        r = run_one(e)
        elapsed = time.time() - t0
        results.append(r)
        cls = r.get("classification", "?")
        err = r.get("error", "")
        nrules = len(r.get("rule_ids_fired", []))
        print(
            f"[T {i+1:3d}/{len(entries)}] {e['id']:55s} cls={cls:3s} "
            f"rules_fired={nrules:2d} dur={elapsed:.1f}s {err}",
            flush=True,
        )
    AUX_ROOT.mkdir(parents=True, exist_ok=True)
    out_path = AUX_ROOT / "bench-results-semgrep-tail.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n[aux-semgrep-tail] wrote {out_path}")


if __name__ == "__main__":
    main()
