#!/usr/bin/env python3
"""Audit per-tool firings in the aux max-breadth pass.

For each tool (semgrep, rudra, codeql), report:
  * Total entries that fired ≥1 finding
  * Set of unique rule IDs that fired
  * Per-rule: how many entries it fired on
  * Per-entry that fired: was the firing in-class for the entry's vuln_class?
  * Net delta from headline: how many TPs added, FPs added, NOISE added
"""
import json
import sys
import tomllib
from pathlib import Path
from collections import Counter, defaultdict

WS = Path("/home/bob/src/ward/ws/bn-1h7qp")
AUX = WS / "target/bench/aux-max-breadth"
ARTIFACTS = WS / "notes/benchmarks/artifacts"
MANIFEST = WS / "tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml"


def load_manifest():
    with open(MANIFEST, "rb") as f:
        m = tomllib.load(f)
    return {e["id"]: e for e in m["entries"]}


def audit_tool(tool: str, headline_path: Path, aux_path: Path, manifest_idx):
    with open(headline_path) as f:
        headline = json.load(f)
    with open(aux_path) as f:
        aux = json.load(f)
    h_by = {e["harness_id"]: e for e in headline}
    a_by = {e["harness_id"]: e for e in aux}

    h_tp = sum(1 for r in headline if r.get("classification") == "TP")
    h_fp = sum(1 for r in headline if r.get("classification") == "FP")
    h_tn = sum(1 for r in headline if r.get("classification") == "TN")
    h_fn = sum(1 for r in headline if r.get("classification") == "FN")
    a_tp = sum(1 for r in aux if r.get("classification") == "TP")
    a_fp = sum(1 for r in aux if r.get("classification") == "FP")
    a_tn = sum(1 for r in aux if r.get("classification") == "TN")
    a_fn = sum(1 for r in aux if r.get("classification") == "FN")

    print(f"\n=== {tool.upper()} ===")
    print(f"  Headline (raw, pre-paired): TP={h_tp} FP={h_fp} TN={h_tn} FN={h_fn}")
    print(f"  Aux      (raw, pre-paired): TP={a_tp} FP={a_fp} TN={a_tn} FN={a_fn}")
    delta_tp = a_tp - h_tp
    delta_fp = a_fp - h_fp
    print(f"  Δ:  TP={delta_tp:+d}  FP={delta_fp:+d}")

    # Per-entry detail of changes
    changed = []
    for h in headline:
        eid = h["harness_id"]
        a = a_by.get(eid)
        if a is None:
            continue
        if h.get("classification") != a.get("classification"):
            changed.append((eid, h.get("classification"), a.get("classification")))
    if changed:
        print(f"  Classification changes: {len(changed)}")
        for eid, oc, nc in changed[:20]:
            vc = manifest_idx.get(eid, {}).get("vuln_class", "?")
            print(f"    {eid:50s} {oc:3s} → {nc:3s}  (vuln_class={vc})")

    # Rule-id firing audit for aux
    fire_counter = Counter()
    rule_to_entries = defaultdict(list)
    for r in aux:
        for rid in r.get("rule_ids_fired", []):
            fire_counter[rid] += 1
            rule_to_entries[rid].append(r["harness_id"])
    if fire_counter:
        print(f"  Aux unique rules fired: {len(fire_counter)}")
        print(f"  Top rules by firing count:")
        for rid, n in fire_counter.most_common(15):
            ents = rule_to_entries[rid][:3]
            print(f"    {n:3d} × {rid[:60]:60s}  e.g. {ents}")


def main():
    manifest_idx = load_manifest()
    print("bn-1h7qp — aux max-breadth firing audit")
    print("=" * 70)

    # Semgrep
    sg_headline = ARTIFACTS / "bench-results-semgrep.json"
    sg_aux = AUX / "bench-results-semgrep.json"
    if sg_aux.exists():
        audit_tool("semgrep", sg_headline, sg_aux, manifest_idx)
    else:
        print("\n[semgrep aux] not yet produced — skipping")

    # Rudra
    rd_headline = ARTIFACTS / "bench-results-rudra.json"
    rd_aux = AUX / "bench-results-rudra.json"
    if rd_aux.exists():
        audit_tool("rudra", rd_headline, rd_aux, manifest_idx)
    else:
        print("\n[rudra aux] not yet produced — skipping")

    # CodeQL
    cq_headline = ARTIFACTS / "bench-results-codeql-partial.json"
    cq_aux = AUX / "bench-results-codeql.json"
    if cq_aux.exists():
        audit_tool("codeql", cq_headline, cq_aux, manifest_idx)
    else:
        print("\n[codeql aux] not yet produced — skipping")


if __name__ == "__main__":
    main()
