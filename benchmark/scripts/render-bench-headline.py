#!/usr/bin/env python3
"""Render the headline markdown blocks for unsafe-rust-bench-results-2026-05-13.md
from stats.json and paired-summary.json.

Reads:
  target/bench/unsafe-rust-v2/stats.json
  target/bench/unsafe-rust-v2/paired/paired-summary.json
  target/bench/unsafe-rust-v2/paired/paired-results-codeql.json (for restricted view)

Emits stdout: markdown table fragments ready to splice into the doc.
"""

import json
import sys
import math
from pathlib import Path

ROOT = Path("/home/bob/src/ward/ws/bn-1qq7o-wrap")
STATS_PATH = ROOT / "target/bench/unsafe-rust-v2/stats.json"
PAIRED_DIR = ROOT / "target/bench/unsafe-rust-v2/paired"


def fmt_ci(lo, hi, digits=3):
    return f"[{lo:.{digits}f}, {hi:.{digits}f}]"


def fmt_metric(val, lo, hi, digits=3):
    return f"{val:.{digits}f} {fmt_ci(lo, hi, digits)}"


def render_headline(stats):
    lines = []
    lines.append("| Tool | TP | FP | TN | FN | Noise | Errored | Precision (95% CI) | Recall (95% CI) | F1 (95% CI) | MCC (95% CI) |")
    lines.append("|------|----|----|----|----|-------|---------|--------------------|-----------------|-------------|--------------|")
    # Sort: ward first, then others alpha, codeql last
    per_tool = stats.get("per_tool", [])
    order = ["ward", "semgrep", "rudra", "cargo-geiger", "codeql"]
    sorted_tools = sorted(per_tool, key=lambda t: order.index(t["tool"]) if t["tool"] in order else 99)
    for t in sorted_tools:
        name = "**Ward**" if t["tool"] == "ward" else t["tool"]
        if t["tool"] == "codeql":
            name = "CodeQL (partial, 50/160 processed)"
        lines.append(
            f"| {name} | {t['tp']} | {t['fp']} | {t['tn']} | {t['fn_']} | "
            f"{t['noise']} | {t['errored']} | "
            f"{fmt_metric(t['precision'], t['precision_ci_lo'], t['precision_ci_hi'])} | "
            f"{fmt_metric(t['recall'], t['recall_ci_lo'], t['recall_ci_hi'])} | "
            f"{fmt_metric(t['f1'], t['f1_ci_lo'], t['f1_ci_hi'])} | "
            f"{fmt_metric(t['mcc'], t['mcc_ci_lo'], t['mcc_ci_hi'])} |"
        )
    return "\n".join(lines)


def render_mcnemar(stats):
    lines = []
    lines.append("| (A, B) | A right / B wrong | B right / A wrong | both right | both wrong | p-value | A beats B at p<0.01 |")
    lines.append("|--------|-------------------|-------------------|------------|------------|---------|---------------------|")
    for m in stats.get("mcnemar", []):
        star = "yes" if m.get("significant_p_lt_0_01") else "no"
        # report direction by larger count
        a_better = m["a_correct_b_wrong"] > m["b_correct_a_wrong"]
        direction = f"{m['tool_a']} beats {m['tool_b']}" if a_better else f"{m['tool_b']} beats {m['tool_a']}"
        p = m["p_value"]
        p_s = f"{p:.4f}" if p >= 0.0001 else f"{p:.2e}"
        beats = f"{star} ({direction})" if star == "yes" else "no"
        lines.append(
            f"| ({m['tool_a']}, {m['tool_b']}) | {m['a_correct_b_wrong']} | "
            f"{m['b_correct_a_wrong']} | {m['both_correct']} | {m['both_wrong']} | "
            f"{p_s} | {beats} |"
        )
    return "\n".join(lines)


def render_latency(stats):
    lines = []
    lines.append("| Tool | N | p50 | p95 | p99 | mean | max | timeouts | OOMs | errored |")
    lines.append("|------|---|-----|-----|-----|------|-----|----------|------|---------|")
    for l in stats.get("latency", []):
        lines.append(
            f"| {l['tool']} | {l['n']} | {l['p50']:.3f}s | {l['p95']:.3f}s | "
            f"{l['p99']:.3f}s | {l['mean']:.3f}s | {l['max']:.3f}s | "
            f"{l['timeouts']} | {l['ooms']} | {l['errored']} |"
        )
    return "\n".join(lines)


def render_per_subgroup(stats, key):
    out = []
    out.append("| Subgroup | Tool | N | TP | FP | TN | FN | Precision | Recall |")
    out.append("|----------|------|---|----|----|----|----|-----------|--------|")
    rows = stats.get(key, [])
    # group by subgroup
    groups = {}
    for r in rows:
        groups.setdefault(r["subgroup"], []).append(r)
    for sg in sorted(groups.keys()):
        for r in sorted(groups[sg], key=lambda x: x["tool"]):
            out.append(
                f"| {sg} | {r['tool']} | {r['n']} | {r['tp']} | {r['fp']} | "
                f"{r['tn']} | {r['fn_']} | {r['precision']:.3f} | {r['recall']:.3f} |"
            )
    return "\n".join(out)


def compute_restricted_codeql(paired_dir):
    """Per methodology: McNemar restricted to entries CodeQL actually processed.
    Returns (ward_subset, codeql_subset, mcnemar_b, mcnemar_c) on the 25 pairs
    where CodeQL produced SARIF (error == '')."""
    with open(paired_dir / "paired-results-codeql.json") as f:
        codeql = json.load(f)
    with open(paired_dir / "paired-results-ward.json") as f:
        ward = json.load(f)
    # Identify pair_ids (vuln + fix both) where neither side has error.
    cq_by_id = {r["harness_id"]: r for r in codeql}
    ward_by_id = {r["harness_id"]: r for r in ward}
    processed_pairs = []
    for r in codeql:
        if r.get("error", "") != "":
            continue
        hid = r["harness_id"]
        if hid.endswith("-fix"):
            continue
        sibling = hid + "-fix"
        if sibling in cq_by_id and cq_by_id[sibling].get("error", "") == "":
            processed_pairs.append(hid)
    def tally(by_id, pair_ids):
        tp = fp = tn = fn = 0
        fully_correct = set()
        for pid in pair_ids:
            v = by_id.get(pid)
            fx = by_id.get(pid + "-fix")
            if v is None or fx is None:
                continue
            v_cls = v.get("paired_classification") or v["classification"]
            fx_cls = fx.get("paired_classification") or fx["classification"]
            if v_cls == "TP":
                tp += 1
            elif v_cls == "FN":
                fn += 1
            if fx_cls == "TN":
                tn += 1
            elif fx_cls == "FP":
                fp += 1
            if v_cls == "TP" and fx_cls == "TN":
                fully_correct.add(pid)
        return tp, fp, tn, fn, fully_correct
    w_tp, w_fp, w_tn, w_fn, w_correct = tally(ward_by_id, processed_pairs)
    c_tp, c_fp, c_tn, c_fn, c_correct = tally(cq_by_id, processed_pairs)
    def metrics(tp, fp, tn, fn):
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * p * r / (p + r) if (p + r) else 0.0
        denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        mcc = (tp * tn - fp * fn) / denom if denom > 0 else 0.0
        return p, r, f1, mcc
    return {
        "n_pairs": len(processed_pairs),
        "ward": (w_tp, w_fp, w_tn, w_fn, *metrics(w_tp, w_fp, w_tn, w_fn)),
        "codeql": (c_tp, c_fp, c_tn, c_fn, *metrics(c_tp, c_fp, c_tn, c_fn)),
        "ward_correct": w_correct,
        "codeql_correct": c_correct,
    }


def mcnemar_p_value(b, c):
    """Two-sided exact binomial test (matches stats.rs::mcnemar_p_value)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # P(X <= k | n, 0.5) doubled
    cum = 0.0
    for i in range(k + 1):
        cum += math.comb(n, i) * (0.5 ** n)
    p = 2 * cum
    return min(p, 1.0)


def main():
    with open(STATS_PATH) as f:
        stats = json.load(f)
    print("## Headline\n")
    print(render_headline(stats))
    print("\n## McNemar pairwise\n")
    print(render_mcnemar(stats))
    print("\n## Latency\n")
    print(render_latency(stats))
    print("\n## Per-vuln-class\n")
    print(render_per_subgroup(stats, "per_vuln_class"))
    print("\n## Per-bug-shape\n")
    print(render_per_subgroup(stats, "per_bug_shape"))
    print("\n## CodeQL restricted (only 25 pairs CodeQL processed)\n")
    r = compute_restricted_codeql(PAIRED_DIR)
    print(f"n_pairs = {r['n_pairs']}")
    w = r["ward"]
    c = r["codeql"]
    print(f"| Ward (n={r['n_pairs']} pairs) | TP={w[0]} FP={w[1]} TN={w[2]} FN={w[3]} | P={w[4]:.3f} R={w[5]:.3f} F1={w[6]:.3f} MCC={w[7]:+.3f} |")
    print(f"| CodeQL (n={r['n_pairs']} pairs) | TP={c[0]} FP={c[1]} TN={c[2]} FN={c[3]} | P={c[4]:.3f} R={c[5]:.3f} F1={c[6]:.3f} MCC={c[7]:+.3f} |")
    # McNemar restricted
    w_only = r["ward_correct"] - r["codeql_correct"]
    c_only = r["codeql_correct"] - r["ward_correct"]
    p = mcnemar_p_value(len(w_only), len(c_only))
    print(f"McNemar restricted: ward_right_codeql_wrong={len(w_only)} codeql_right_ward_wrong={len(c_only)} p={p:.6f}")
    print(f"witness_audit: {stats.get('witness_audit')}")
    print(f"paired_pair_count={stats.get('paired_pair_count')} strata={stats.get('strata_count')} bootstrap_reps={stats.get('bootstrap_reps')}")


if __name__ == "__main__":
    main()
