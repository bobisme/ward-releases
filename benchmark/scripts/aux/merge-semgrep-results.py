#!/usr/bin/env python3
"""Merge head-half + tail-half Semgrep results into the canonical aux JSON.

The head runner writes target/bench/aux-max-breadth/bench-results-semgrep.json.
The tail runner writes target/bench/aux-max-breadth-tail/bench-results-semgrep-tail.json.
This script merges them by harness_id (preferring head if duplicate), pads with
`repo_missing` errors for any manifest entry not covered, and writes a single
160-entry bench-results-semgrep.json in manifest order.
"""
import json
from pathlib import Path

WS = Path("/home/bob/src/ward/ws/bn-1h7qp")
HEAD = WS / "target/bench/aux-max-breadth/bench-results-semgrep.json"
TAIL = WS / "target/bench/aux-max-breadth-tail/bench-results-semgrep-tail.json"
MERGED = WS / "target/bench/aux-max-breadth/bench-results-semgrep.json"
MANIFEST = WS / "tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml"


def main():
    import tomllib
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    manifest_ids = [e["id"] for e in m["entries"]]

    head_results = []
    if HEAD.exists():
        try:
            head_results = json.load(open(HEAD))
        except Exception:
            head_results = []
    tail_results = []
    if TAIL.exists():
        try:
            tail_results = json.load(open(TAIL))
        except Exception:
            tail_results = []

    by_id = {}
    for r in tail_results:
        by_id[r["harness_id"]] = r
    # head wins on conflict (running first, more complete state)
    for r in head_results:
        by_id[r["harness_id"]] = r

    # Build merged in manifest order
    merged = []
    missing = 0
    for eid in manifest_ids:
        if eid in by_id:
            merged.append(by_id[eid])
        else:
            # Pad with a `not_run` marker so the schema is whole.
            expected = next(e["expected_result"] for e in m["entries"] if e["id"] == eid)
            merged.append({
                "tool": "semgrep",
                "harness_id": eid,
                "expected": expected,
                "detected": False,
                "classification": "FN" if expected == "tp" else "TN",
                "duration_secs": 0.0,
                "error": "not_run_aux",
            })
            missing += 1

    MERGED.write_text(json.dumps(merged, indent=2))
    print(f"merged: head={len(head_results)} tail={len(tail_results)} unique={len(by_id)} missing={missing} → {MERGED}")
    tp = sum(1 for r in merged if r.get("classification") == "TP")
    fp = sum(1 for r in merged if r.get("classification") == "FP")
    tn = sum(1 for r in merged if r.get("classification") == "TN")
    fn = sum(1 for r in merged if r.get("classification") == "FN")
    errd = sum(1 for r in merged if r.get("error"))
    print(f"merged classifications: TP={tp} FP={fp} TN={tn} FN={fn} errd={errd}")


if __name__ == "__main__":
    main()
