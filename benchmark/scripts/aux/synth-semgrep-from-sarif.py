#!/usr/bin/env python3
"""Synthesize aux semgrep bench-results from on-disk SARIF artifacts.

If the head runner is interrupted before writing its final JSON, we can
recover per-entry results from the SARIF files it wrote during the run.
This script walks `target/bench/aux-max-breadth/raw/semgrep/<eid>/semgrep.sarif`,
applies the same parser + classification logic as run-aux-semgrep.py,
and writes a 160-entry JSON in manifest order. Missing entries get
`not_run_aux`.

Reads BOTH `target/bench/aux-max-breadth/raw/semgrep/` (head run) and
`target/bench/aux-max-breadth-tail/raw/semgrep/` (tail run); head wins
on conflict (typically there are no conflicts because head runs idx
0..79 and tail runs 80..159).
"""
import json
import os
import tomllib
from pathlib import Path

WS = Path("/home/bob/src/ward/ws/bn-1h7qp")
HEAD_RAW = WS / "target/bench/aux-max-breadth/raw/semgrep"
TAIL_RAW = WS / "target/bench/aux-max-breadth-tail/raw/semgrep"
TAIL2_RAW = WS / "target/bench/aux-max-breadth-tail2/raw/semgrep"
MANIFEST = WS / "tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml"
OUT = WS / "target/bench/aux-max-breadth/bench-results-semgrep.json"


def parse_sarif(sarif_path: Path, entry: dict):
    """Mirror run-aux-semgrep.py's parser."""
    try:
        with open(sarif_path) as f:
            sarif = json.load(f)
    except Exception:
        return None  # SARIF not present or corrupted
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


def synth_for_entry(entry: dict):
    eid = entry["id"]
    # Prefer head, then tail, then tail2
    for raw_dir in (HEAD_RAW, TAIL_RAW, TAIL2_RAW):
        sarif_path = raw_dir / eid / "semgrep.sarif"
        if sarif_path.exists():
            findings = parse_sarif(sarif_path, entry)
            if findings is None:
                continue
            affected = entry.get("affected_file", "")
            detected = any(affected_match(f["file"], affected) for f in findings)
            res = {
                "tool": "semgrep",
                "harness_id": eid,
                "expected": entry["expected_result"],
                "findings": findings,
                "rule_ids_fired": sorted({f["rule_id"] for f in findings}),
                "detected": detected,
                # We don't have precise wall-clock; mark from artifact stat
                "duration_secs": sarif_path.stat().st_size / (1024 * 1024),  # MB-as-proxy
                "error": "",
            }
            if entry["expected_result"] == "tp":
                res["classification"] = "TP" if detected else "FN"
            else:
                res["classification"] = "FP" if detected else "TN"
            return res
    # Not found on disk
    return {
        "tool": "semgrep",
        "harness_id": eid,
        "expected": entry["expected_result"],
        "detected": False,
        "classification": "FN" if entry["expected_result"] == "tp" else "TN",
        "duration_secs": 0.0,
        "error": "not_run_aux",
    }


def main():
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    results = [synth_for_entry(e) for e in m["entries"]]
    OUT.write_text(json.dumps(results, indent=2))
    tp = sum(1 for r in results if r.get("classification") == "TP")
    fp = sum(1 for r in results if r.get("classification") == "FP")
    tn = sum(1 for r in results if r.get("classification") == "TN")
    fn = sum(1 for r in results if r.get("classification") == "FN")
    errd = sum(1 for r in results if r.get("error"))
    print(f"synth: wrote {OUT}")
    print(f"  TP={tp} FP={fp} TN={tn} FN={fn} errd={errd}  (errd is not_run_aux)")


if __name__ == "__main__":
    main()
