# `notes/benchmarks/` — index

This directory holds the design, results, and aux documents for
Ward's public benchmarks. Read in the order below.

## Unsafe-Rust head-to-head benchmark (v1, 2026-05)

1. **Methodology (locked before corpus collection)** —
   [`unsafe-rust-bench-methodology.md`](unsafe-rust-bench-methodology.md)
   — locked 2026-05-07 under bn-3cgmj. 12 numbered sections covering
   claim under test, corpus selection, tool pinning, fairness
   controls, scoring rules, witness-rate axis, statistical reporting,
   latency, reproduction requirements, out-of-scope, threats to
   validity, open questions. Amendments require an issue against
   bn-1ti5m.
2. **Smoke run** —
   [`smoke-run-results-20260511.md`](smoke-run-results-20260511.md)
   — 5-entry determinism + tool-wiring smoke.
3. **Headline (full 80-pair head-to-head)** —
   [`unsafe-rust-bench-results-2026-05-13.md`](unsafe-rust-bench-results-2026-05-13.md)
   — canonical headline numbers (Ward F1=0.655, MCC=+0.564, P=1.000;
   every competitor at 0 TP; McNemar p ≈ 1.46e-11) with bootstrap
   CIs, per-vuln-class / per-bug-shape breakdown, latency table,
   CodeQL restricted view, competitor ruleset audit, witness audit
   sidecar.
4. **Max-breadth aux (post-publication fairness audit)** —
   [`unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](unsafe-rust-bench-aux-max-breadth-2026-05-13.md)
   — re-runs Semgrep / CodeQL / Rudra under their broadest publicly
   available rulesets; documents that the headline ranking does not
   change.
5. **Public-facing writeup** —
   [`../../docs/blog/unsafe-rust-benchmark.md`](../../docs/blog/unsafe-rust-benchmark.md)
   — external-reviewer synthesis covering headline, fairness audit,
   Ward strengths/weaknesses, threats to validity, what's next.
6. **Reproduction kit** —
   [`../../tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md)
   — one-command repro, ±2pp tolerance, expected wall time,
   determinism smoke pointer, troubleshooting checklist.
7. **Prior Ward-only first pass** —
   [`unsafe-rust-bench-results-2026-05-12.md`](unsafe-rust-bench-results-2026-05-12.md)
   — 68-pair small-repo subset, superseded by (3).

Corpus and provenance:
[`tests/cve-registry/benchmarks/unsafe-rust-bench/`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/).
Bench image:
[`bench/Dockerfile.bench`](../../bench/Dockerfile.bench). Tool
pinning: [`bench/tool-versions.toml`](../../bench/tool-versions.toml).
Rule-id mapping:
[`bench/rule-id-mapping.toml`](../../bench/rule-id-mapping.toml).
Committed artifacts under
[`artifacts/`](artifacts/).

Benchmark version tag: `bench/unsafe-rust-v1` (minted by the
operator after the bench artifact lands on `default`).
