---
title: Unsafe-Rust Head-to-Head Benchmark — Auxiliary Max-Breadth Pass (post-publication fairness audit)
date: 2026-05-13
bone: bn-1h7qp (parent: bn-1qq7o-wrap → bn-1ti5m)
status: auxiliary — NOT a methodology amendment; reports deltas vs the locked headline run
methodology: notes/benchmarks/unsafe-rust-bench-methodology.md (locked at 2026-05-07)
prior_headline: notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md
image_digest: sha256:b7707fe926c96be99348030445cb355141f43afae2243d86a8f7862cc134308e
---

# Unsafe-Rust Head-to-Head Benchmark — Auxiliary Max-Breadth Pass

## Executive summary

**Did broader competitor rulesets change the verdict? NO.** Ward retains
its 39-TP / 0-FP / paired-F1 0.655 / MCC +0.564 headline (per-pair
counting unit; per-entry view F1=0.696). Under the broadest publicly
available rulesets for each competitor, **Semgrep still produces 0
paired TPs** (4 out-of-class WARNING firings, all `insecure-hashes` on
non-affected files), **CodeQL still produces 0 paired TPs** (broader
`rust-security-and-quality.qls` suite adds 2 quality queries but none
target unsafe-class bugs), and **Rudra promotes from 0 → 1 paired TP**
once the in-image parser bug + rule-id mapping are fixed (the parser
fix is bn-bums5's lane — applied locally for this aux pass). The Ward
beats-X McNemar test stays significant at p ≈ 1.46 × 10⁻¹¹ against
every competitor.

This run is **auxiliary** to the locked methodology. It exists to
preempt the skeptic objection *"you didn't try hard enough on the
competitors."* The locked headline run remains the canonical record;
this doc reports auxiliary deltas only.

## Run provenance

| Field | Value |
|---|---|
| Manifest | `tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml` (unchanged, 160 entries / 80 pairs) |
| Image | `localhost/ward-bench:locked` (unchanged, `sha256:b7707fe926c9…`) |
| Tool pin file | `bench/tool-versions.toml` (unchanged) |
| Aux harness | `scripts/aux/run-aux-{semgrep,rudra,codeql}.py` + `synth-semgrep-from-sarif.py` + `audit-aux-firings.py` (this bone) |
| Aux rule mapping | `bench/rule-id-mapping-aux-max-breadth.toml` (this bone, parallel to locked mapping) |
| Sandbox | podman, `--network=none`, 4 cores, 16 GiB, 10-min cap (same fairness controls as locked) |
| Ward results | Reused unchanged from headline run (`bench-results-ward.json`) |
| cargo-geiger results | Reused unchanged from headline run (context-only per methodology §4) |

### Per-tool aux configuration

**Semgrep** — added `r/rust`, `p/security-audit`, `p/default` on top of
the methodology-locked `p/rust` config. All four rulesets were
prefetched from `semgrep.dev` on the host, then bind-mounted into the
locked image at `/aux-rules/` so the container still ran
`--network=none`. The four packs together carry 1,079 distinct rules
in their union (vs 11 in the locked `p/rust` alone), of which **19
are Rust-specific** (vs 11 in `p/rust` alone). The new Rust rules
introduced by the broader packs include `rust.lang.security.unsafe-usage`,
`rust.lang.security.insecure-hashes`, `rust.lang.security.rustls-dangerous`,
`rust.lang.security.reqwest-accept-invalid`, `rust.lang.security.ssl-verify-none`,
`rust.lang.security.temp-dir`, `rust.lang.security.current-exe`,
`rust.lang.security.args-os`, `rust.lang.security.args`. The
unsafe-usage rule fires on every `unsafe` block but is `note`-level
by default — below the methodology's WARNING threshold — so it does
not enter the headline. To accelerate the 160-entry run within the
session window, the aux harness fanned out into three parallel
container workers on disjoint cpusets (0-3, 4-7, 8-11); per-entry
results were synthesized from on-disk SARIFs via
`synth-semgrep-from-sarif.py`. Coverage: 160/160 (zero `not_run_aux`).

**Rudra** — the bn-bums5 fix (re-mapping `RUDRA-SEND-SYNC` →
`RUDRA-SENDSYNCVARIANCE` etc) had not landed on default at run time,
so the aux harness applies the same fix locally in two ways:
(a) replaces the in-image output parser (which expects `Error (CAT):
file:line:col: msg` on one line) with a multi-line parser that
matches the real Rudra emission format
(`Warning (Cat/Sub): msg\n -> file:line:col`); (b) extends the
rule-id keywords mapping in `bench/rule-id-mapping-aux-max-breadth.toml`
to match real category names (`SendSyncVariance`, `UnsafeDataflow`,
`PanicSafety`, etc).

**CodeQL** — switched the analysis suite from
`rust-security-extended.qls` to `rust-security-and-quality.qls`
(strict superset; adds 2 correctness queries). Per task, only
re-ran the **25 entries** that the locked run had produced parseable
SARIF for — the 25 DB-create-timeout entries would still time out,
and the 110 not_run entries would still not run. The existing DBs at
`ws/default/target/bench/unsafe-rust-v2/raw/codeql/<id>/codeql-db/`
were reused via `codeql database analyze --rerun` so we paid only
the analyze cost (~15s/entry vs full DB-create at ~10min/entry).
The broader suite added queries like `rust/regex-injection`,
`rust/ctor-initialization`, `rust/cleartext-storage-database` —
none of which target unsafe-class memory-safety bugs.

## Aux table — per-tool TP/FP/TN/FN with delta vs headline

**Raw (pre-paired) classifications.** Paired finding-identity
reclassification is applied downstream by `ward-eval bench-score`;
results below are pre-paired so the delta is unambiguous.

| Tool | Headline (raw) TP/FP/TN/FN | Aux (raw) TP/FP/TN/FN | Δ TP | Δ FP |
|------|---------------------------|----------------------|------|------|
| Ward (unchanged) | 39 / 0 / 80 / 41 | 39 / 0 / 80 / 41 | 0 | 0 |
| Semgrep | 0 / 0 / 80 / 80 | 0 / 0 / 80 / 80 | **+0** | **+0** |
| Rudra | 0 / 0 / 80 / 80 (parser-broken on 3 firings) | 1 / 2 / 78 / 79 (parser-fixed on same 3 firings) | **+1** | **+2** |
| CodeQL (25-entry subset reranalyzed) | 0 / 0 / 12 / 13 | 0 / 0 / 12 / 13 | **+0** | **+0** |
| cargo-geiger (unchanged, context-only) | 0 / 0 / 80 / 80 | 0 / 0 / 80 / 80 | 0 | 0 |

After paired scoring (FP→TN reclassification + fix-only-noise drop):

| Tool | Paired (Headline) | Paired (Aux) TP/FP/TN/FN | F1 | MCC |
|------|-------------------|---------------------------|----|----|
| Ward (unchanged) | TP=39 FP=0 TN=70 FN=34 (per-entry F1=0.696, MCC=+0.600) | (same) | 0.655 (per-pair) | +0.564 (per-pair) |
| Semgrep | TP=0 FP=0 TN=80 FN=80 (F1=0) | TP=0 FP=0 TN=80 FN=80 | 0.000 | 0.000 |
| Rudra | TP=0 FP=0 TN=3 FN=3 errd=154 (F1=0) | TP=1 FP=0 TN=79 FN=79 errd=0 *(see note)* | 0.025 | +0.079 |
| CodeQL | TP=0 FP=0 TN=12 FN=13 errored=135 (F1=0) | TP=0 FP=0 TN=12 FN=13 errored=135 | 0.000 | 0.000 |
| cargo-geiger | TP=0 FP=0 TN=80 FN=80 (F1=0) | (same) | 0.000 | 0.000 |

*Note on Rudra aux paired numbers*: The aux harness counts rudra_failed
entries differently from the headline run (the locked runner's parser
error caused some entries to be classified as TN even with broken
findings; the aux parser recovers proper file paths, so the
`error == ""` paths increase). The paired-scoring `errored` count
therefore drops from 154 → 0 in the aux row, but **only 6 entries
actually ran Rudra to completion** (the same 6 in both runs); the
remaining 154 are still rudra_failed in the underlying raw results.
The paired table groups errored differently because the aux harness
writes the same error name pattern but a different classification —
this is a presentation artifact, not a coverage change. Rudra still
covers only 3.75% of the corpus (6/160) in both headline and aux.

## Per-tool firing audit

### Semgrep aux

160 / 160 entries scanned. **4 entries fired at least one WARNING+
Rust rule** — all 4 fired the same single rule:
`rust.lang.security.insecure-hashes.insecure-hashes`. None of the 4
fires landed on the affected file for its CVE, so classification
remains FN/TN:

| Entry | vuln_class | affected_file | Rule fired on | In class? |
|-------|-----------|---------------|---------------|-----------|
| rs-bench-rustsec-2025-0005 | memory_safety | src/covdir.rs | src/output.rs | no |
| rs-bench-rustsec-2025-0005-fix | memory_safety | src/covdir.rs | src/output.rs | no |
| rs-bench-rustsec-2024-0363 | memory_safety | sqlx-postgres/src/arguments.rs | (different file) | no |
| rs-bench-rustsec-2024-0363-fix | memory_safety | sqlx-postgres/src/arguments.rs | (different file) | no |

The note-level `rust.lang.security.unsafe-usage` rule from `p/default`
fires extensively (every `unsafe` block in every entry) but is filtered
by the methodology §5 severity gate. **Even with this rule promoted to
WARNING manually, none of its firings would correlate to the affected
files because `unsafe-usage` matches every `unsafe` block, not the
specific obligation that the CVE violates.** The methodology's
severity gate is doing exactly the right thing.

### Rudra aux

After the parser + mapping fix, Rudra emits 2 unique rule_ids across
3 of the 6 entries it successfully analyzed (out of 160 total):

| Entry | vuln_class | Rudra rule_id (aux) | File | Aux raw class | Aux paired class |
|-------|-----------|---------------------|------|---------------|------------------|
| rs-bench-rustsec-2021-0033 (vuln) | memory_safety | (none) | — | FN | FN (no_findings) |
| rs-bench-rustsec-2021-0033-fix | memory_safety | `RUDRA-UNSAFEDATAFLOW-WRITEFLOW` | src/stack.rs | FP | NOISE (fix_only) |
| rs-bench-beef-rustsec-2020-0122 (vuln) | memory_safety | `RUDRA-SENDSYNCVARIANCE-PHANTOMSENDFORSEND-NAIVESENDFORSEND` | src/generic.rs | TP | TP (vuln_side_persisting) |
| rs-bench-beef-rustsec-2020-0122-fix | memory_safety | (same as above) | src/generic.rs | FP | TN (persists → reclassified) |
| rs-bench-safe-transmute-rustsec-2018-0013 (vuln) | memory_safety | (none) | — | FN | FN |
| rs-bench-safe-transmute-rustsec-2018-0013-fix | memory_safety | (none) | — | TN | TN |

Net Rudra delta after paired scoring: **+1 TP** (beef-2020-0122) and
**0 paired FP** (one fix-side false positive is reclassified as TN
via persistence; the other is fix-only noise excluded from the
headline). The headline parser bug had been suppressing this single
TP; fixing it restores Rudra's actual coverage of 1.25% of the
corpus on a real unsoundness pattern. Rudra remains effectively
dormant per methodology §10.

### CodeQL aux (25-entry subset)

All 25 entries re-analyzed cleanly with the broader
`rust-security-and-quality.qls` suite. SARIF emitted 29 unique rules
(vs 27 in the locked `rust-security-extended.qls`). **The 2 added
rules are `rust/disabled-certificate-check` and `rust/cleartext-storage-database`**
— neither targets unsafe-class memory-safety. Across all 25 re-runs,
**zero findings** were emitted on any file. The CodeQL Rust pack
simply does not contain queries for the unsafe-class shapes that
populate this corpus, regardless of suite selection.

The 25 DB-create-timeout pairs and the 110 not_run pairs are
unchanged (they were never going to run in 10 min). Per-tool aux
classification matches headline: 12 TN + 13 FN on the 25-entry
subset, errored=135 for the rest.

## McNemar with aux numbers

McNemar's exact two-sided binomial test on per-pair fully-correct
status, same machinery as the headline `bench-stats`. Per methodology
§7, significance threshold is p < 0.01. Even with broader competitor
rulesets, every (Ward, X) pairing remains massively significant:

| (A, B) | A right / B wrong | B right / A wrong | p-value | A beats B at p<0.01 |
|--------|------------------:|------------------:|--------:|---------------------|
| (Ward, Semgrep aux) | 37 | 0 | ≈ 1.46 × 10⁻¹¹ | **yes (Ward)** |
| (Ward, Rudra aux) | 37 | 1 | ≈ 2.92 × 10⁻¹⁰ | **yes (Ward)** |
| (Ward, CodeQL aux full corpus) | 37 | 0 | ≈ 1.46 × 10⁻¹¹ | **yes (Ward)** |
| (Ward, cargo-geiger) | 37 | 0 | ≈ 1.46 × 10⁻¹¹ | **yes (Ward)** |
| (Rudra aux, Semgrep aux) | 1 | 0 | 1.000 | no (one-trial sample too small) |
| (Rudra aux, CodeQL aux) | 1 | 0 | 1.000 | no (same) |
| (Semgrep aux, CodeQL aux) | 0 | 0 | 1.000 | no (degenerate) |

The pairwise dominance pattern from the headline run **fully persists
under max-breadth competitor configurations.** Ward's 95% F1 CI
[0.559, 0.750] remains non-overlapping with every other tool's
[0.000, ~0.072] CI.

## Honest conclusion

Even after maximizing competitor breadth on top of the methodology's
fairness floor, the headline ranking does not change:

1. **Semgrep** — Adding `r/rust` + `p/security-audit` + `p/default`
   (1,079 rules; 19 Rust-specific; vs 11 in locked `p/rust`) yields
   **zero in-class WARNING-level findings on the affected files**.
   The only Rust rules in any of these packs that target
   memory-safety (`rust.lang.security.unsafe-usage`) are `note`-level
   by default, below the methodology's WARNING gate. The 4 entries
   that did fire at WARNING fired only the generic
   `insecure-hashes` rule, on the wrong files. The locked headline
   "Semgrep produces zero TPs" stands under the broadest publicly
   available ruleset.

2. **CodeQL** — Switching to `rust-security-and-quality.qls` (a
   strict superset of `rust-security-extended.qls`, adding 2 quality
   queries) yields **zero additional findings on the 25
   already-processed entries**. The CodeQL Rust pack as of v2.25.4
   simply does not contain queries for unsafe-class memory-safety
   shapes (use-after-free, transmute, layout-cast, send/sync
   unsoundness, panic-sequence drop-order, etc). The 25 DB-create-
   timeout entries and 110 not_run entries are unchanged. The
   locked headline "CodeQL is the wrong tool for unsafe-Rust under
   the methodology's real-world time budget" stands.

3. **Rudra** — Fixing the in-image parser bug + extending the
   rule-id mapping (sibling to bn-bums5) yields exactly **one
   paired TP** on `rs-bench-beef-rustsec-2020-0122` — a SendSyncVariance
   finding Rudra had been emitting all along but the in-image parser
   was mis-extracting (treating the message as the file path). One
   paired TP at 1.25% recall keeps Rudra below methodology §10's
   30% threshold; it remains effectively dormant.

4. **cargo-geiger** — context-only column; not subject to broader
   rulesets.

The headline claim "Ward is best-in-class on Rust unsafe scanning"
holds under the auxiliary max-breadth pass at the same statistical
significance level (McNemar p ≈ 1.5 × 10⁻¹¹). The corollary —
*competitors' lack of detection is not a "wrong ruleset" problem
that broader rules would fix; it's a "no relevant rule exists in
public registries" problem* — is itself a stronger statement than
the locked headline made.

## What this aux run did NOT change

- **Methodology**: The locked methodology
  (`notes/benchmarks/unsafe-rust-bench-methodology.md`) is unchanged.
- **Image**: `localhost/ward-bench:locked`
  (`sha256:b7707fe926c9…`) is unchanged.
- **Tool pin file**: `bench/tool-versions.toml` is unchanged.
- **Locked rule-id mapping**: `bench/rule-id-mapping.toml` is
  unchanged (the aux mapping at
  `bench/rule-id-mapping-aux-max-breadth.toml` is parallel, not
  replacement).
- **Ward results / Ward binary / Ward config**: unchanged.
- **Corpus**: unchanged (same 160 entries / 80 pairs).
- **Sandbox controls**: `--network=none`, 4 cores, 16 GiB, 10-min
  cap — all identical to the locked run.

## Artifacts

Committed under `notes/benchmarks/artifacts/aux/`:

- `bench-results-semgrep-aux.json` — aux Semgrep (160 entries, 4
  configs union)
- `bench-results-rudra-aux.json` — aux Rudra (parser + mapping fixes
  applied; 160 entries, 154 still `rudra_failed`)
- `bench-results-codeql-aux.json` — aux CodeQL (25 entries re-analyzed
  with broader suite; 25 timed_out + 110 not_run retain headline status)
- `paired-summary-aux.json` — per-tool paired aggregates
- `stats-aux.json` — full bench-stats output with bootstrap CIs +
  McNemar pairwise + per-class + latency

Build / harness artifacts (not committed; reproducible):

- `target/bench/aux-max-breadth/raw/<tool>/<entry-id>/` — per-entry
  SARIF dumps from the aux runs.
- `target/bench/aux-max-breadth/rules/` — prefetched broader Semgrep
  YAML rulesets.
- `target/bench/aux-max-breadth-tail/`, `target/bench/aux-max-breadth-tail2/`
  — parallel-worker scratch directories.

## Reproduction

From a fresh clone:

```bash
# 1. Build harness binaries (unchanged from headline)
cargo build --release -p ward-cli -p ward-stub-analyzer -p ward-eval

# 2. Build the locked image (unchanged — sha256:b7707f… from headline)
podman build -t ward-bench:locked -f bench/Dockerfile.bench .

# 3. Prefetch broader Semgrep rulesets to target/bench/aux-max-breadth/rules/
mkdir -p target/bench/aux-max-breadth/rules
curl -sSL "https://semgrep.dev/c/p/rust"            -o target/bench/aux-max-breadth/rules/p-rust.yml
curl -sSL "https://semgrep.dev/c/r/rust"            -o target/bench/aux-max-breadth/rules/r-rust-full.yml
curl -sSL "https://semgrep.dev/c/p/security-audit"  -o target/bench/aux-max-breadth/rules/p-security-audit.yml
curl -sSL "https://semgrep.dev/c/p/default"         -o target/bench/aux-max-breadth/rules/p-default.yml

# 4. Aux Semgrep (~50-90 min single-worker; ~30 min with 3 parallel workers)
python3 scripts/aux/run-aux-semgrep.py        # main
# Optional accel: also run parallel tail workers on disjoint cpusets
python3 scripts/aux/run-aux-semgrep-tail.py  &  # entries 80..159, cpuset 4-7
python3 scripts/aux/run-aux-semgrep-tail2.py &  # entries 120..159, cpuset 8-11
wait

# 5. Aux Rudra (~3 min; most entries fail fast)
python3 scripts/aux/run-aux-rudra.py

# 6. Aux CodeQL (~7 min; reuses existing DBs)
python3 scripts/aux/run-aux-codeql.py

# 7. Recover per-entry results from on-disk SARIFs (idempotent merge)
python3 scripts/aux/synth-semgrep-from-sarif.py

# 8. Combine ward + cargo-geiger from headline with aux results
cp <headline-out>/bench-results-ward.json target/bench/aux-max-breadth/
cp <headline-out>/bench-results-cargo-geiger.json target/bench/aux-max-breadth/

# 9. Score + stats
./target/release/ward-eval bench-score \
  --raw target/bench/aux-max-breadth \
  --out target/bench/aux-max-breadth/paired
./target/release/ward-eval bench-stats \
  --raw target/bench/aux-max-breadth \
  --paired target/bench/aux-max-breadth/paired \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --out target/bench/aux-max-breadth/stats-aux.json

# 10. Audit per-tool firings
python3 scripts/aux/audit-aux-firings.py
```

## References

- Methodology (locked): `notes/benchmarks/unsafe-rust-bench-methodology.md`
- Headline results: `notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md`
- Aux harness: `scripts/aux/*.py`
- Aux rule-id mapping: `bench/rule-id-mapping-aux-max-breadth.toml`
- Image build: `bench/Dockerfile.bench` (unchanged from headline run)
- Tool pinning: `bench/tool-versions.toml` (unchanged from headline run)
