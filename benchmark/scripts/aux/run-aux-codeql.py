#!/usr/bin/env python3
"""bn-1h7qp aux harness — CodeQL re-run with broader `rust-security-and-quality.qls`.

Per task spec: only re-run on the 25 entries that previously produced
parseable SARIF. Their DBs are still on disk at:

    /home/bob/src/ward/ws/default/target/bench/unsafe-rust-v2/raw/codeql/<id>/codeql-db

We use `codeql database analyze --rerun --output=... <db-path> ... rust-security-and-quality.qls`
inside the locked container (network=none). DB-rebuild is skipped.
The 25 not-attempted entries that timed out at DB-create remain
timed_out; the 110 not_run entries remain not_run.

Output: target/bench/aux-max-breadth/bench-results-codeql.json
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
CODEQL_RAW_ROOT = DEFAULT_WS / "target/bench/unsafe-rust-v2/raw/codeql"
PARTIAL_RESULTS = WS / "notes/benchmarks/artifacts/bench-results-codeql-partial.json"
AUX_ROOT = WS / "target/bench/aux-max-breadth"
RAW_ROOT = AUX_ROOT / "raw" / "codeql"
TOOLCACHE_ROOT = AUX_ROOT / "tool-cache" / "codeql"
IMAGE = "localhost/ward-bench:locked"
TIME_BUDGET_SECS = 600
MEM_GIB = 16
CPUS = 4
CPUSET = "0-3"
SUITE = "codeql/rust-queries:codeql-suites/rust-security-and-quality.qls"


def load_entries():
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    return m["entries"]


def load_codeql_partial():
    with open(PARTIAL_RESULTS) as f:
        return json.load(f)


def parse_sarif(sarif_path: Path, entry):
    if not sarif_path.exists():
        return []
    try:
        with open(sarif_path) as f:
            sarif = json.load(f)
    except Exception:
        return []
    out = []
    for run in sarif.get("runs", []):
        rule_levels = {}
        for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
            rid = rule.get("id", "")
            lvl = rule.get("defaultConfiguration", {}).get("level", "warning")
            rule_levels[rid] = lvl
        for result in run.get("results", []):
            rid = result.get("ruleId", "")
            lvl = result.get("level", rule_levels.get(rid, "warning"))
            if lvl == "note":
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


def run_codeql_analyze(entry):
    eid = entry["id"]
    db_dir = CODEQL_RAW_ROOT / eid / "codeql-db"
    out_host = RAW_ROOT / eid
    tool_cache = TOOLCACHE_ROOT
    out_host.mkdir(parents=True, exist_ok=True)
    tool_cache.mkdir(parents=True, exist_ok=True)

    if not (db_dir / "db-rust").exists():
        return {
            "tool": "codeql",
            "harness_id": eid,
            "expected": entry["expected_result"],
            "detected": False,
            "classification": "FN" if entry["expected_result"] == "tp" else "TN",
            "duration_secs": 0.0,
            "error": "db_missing",
        }

    podman_cmd = [
        "podman", "run", "--rm",
        "--network=none",
        f"--memory={MEM_GIB}g",
        f"--cpus={CPUS}",
        f"--cpuset-cpus={CPUSET}",
        # DB read-write — codeql writes intermediate cache files under
        # <db>/results and <db>/log even on --rerun, so we cannot bind ro.
        "-v", f"{db_dir}:/work/db",
        "-v", f"{out_host}:/bench-out",
        "-v", f"{tool_cache}:/tool-cache",
        "--stop-signal=SIGKILL",
        f"--stop-timeout={TIME_BUDGET_SECS + 5}",
        IMAGE,
        "codeql", "database", "analyze",
        "/work/db",
        SUITE,
        "--rerun",
        "--format=sarif-latest",
        "--output=/bench-out/codeql-aux.sarif",
        "--threads=0",
        "--quiet",
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
        "tool": "codeql",
        "harness_id": eid,
        "expected": entry["expected_result"],
        "duration_secs": duration,
    }
    if timed_out:
        res["error"] = "timed_out_analyze"
        res["timed_out"] = True
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace")
        last = next(
            (l for l in reversed(stderr.splitlines()) if l.strip()),
            "",
        )[:200]
        res["error"] = f"codeql_analyze_failed: {last}"
        res["detected"] = False
        res["classification"] = "FN" if entry["expected_result"] == "tp" else "TN"
        return res

    sarif_host = out_host / "codeql-aux.sarif"
    findings = parse_sarif(sarif_host, entry)
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
    partial = load_codeql_partial()
    entries_by_id = {e["id"]: e for e in entries}
    # Identify the 25 entries that previously ran successfully.
    rerun_ids = [p["harness_id"] for p in partial if p.get("error") is None]
    print(f"[aux-codeql] re-running {len(rerun_ids)} entries with `{SUITE}`", flush=True)
    rerun_results = []
    for i, eid in enumerate(rerun_ids):
        e = entries_by_id[eid]
        t0 = time.time()
        r = run_codeql_analyze(e)
        elapsed = time.time() - t0
        rerun_results.append(r)
        cls = r.get("classification", "?")
        err = r.get("error", "")
        nrules = len(r.get("rule_ids_fired", []))
        print(
            f"[{i+1:3d}/{len(rerun_ids)}] {eid:55s} cls={cls:3s} "
            f"rules_fired={nrules:2d} dur={elapsed:.1f}s {err}",
            flush=True,
        )
    rerun_by_id = {r["harness_id"]: r for r in rerun_results}
    # Compose the full 160-entry results: re-run results for the 25
    # SARIF entries; unchanged (timeout / not_run) for the other 135.
    full = []
    for p in partial:
        eid = p["harness_id"]
        if eid in rerun_by_id:
            full.append(rerun_by_id[eid])
        else:
            full.append(p)
    out_path = AUX_ROOT / "bench-results-codeql.json"
    out_path.write_text(json.dumps(full, indent=2))
    print(f"\n[aux-codeql] wrote {out_path}")
    # Headline numbers across the rerun subset
    tp = sum(1 for r in rerun_results if r.get("classification") == "TP")
    fp = sum(1 for r in rerun_results if r.get("classification") == "FP")
    tn = sum(1 for r in rerun_results if r.get("classification") == "TN")
    fn = sum(1 for r in rerun_results if r.get("classification") == "FN")
    errd = sum(1 for r in rerun_results if r.get("error"))
    print(f"[aux-codeql] (rerun subset) TP={tp} FP={fp} TN={tn} FN={fn} errd={errd}")


if __name__ == "__main__":
    main()
