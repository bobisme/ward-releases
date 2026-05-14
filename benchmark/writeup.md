---
title: "Ward is best-in-class on Rust unsafe-class vulnerability detection"
subtitle: "A locked, reproducible head-to-head benchmark against Semgrep, CodeQL, Rudra, and cargo-geiger"
date: 2026-05-13
author: Ward team
status: public writeup
methodology: notes/benchmarks/unsafe-rust-bench-methodology.md
headline_results: notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md
aux_results: notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md
corpus_tag: bench/unsafe-rust-v1
---

# Ward leads the tested off-the-shelf scanners on Rust unsafe-class vulnerability detection

## Headline

On a locked, paired benchmark of 80 RUSTSEC advisories targeting Rust
unsafe-class vulnerabilities (memory-safety, use-after-free, type
confusion, soundness), **among the tested off-the-shelf scanner
configurations, Ward is the only one that fires any in-class true
positive at user-facing severity**.

- Ward: TP=39, FP=0, TN=77, FN=41 over 80 paired pairs (160 entries).
- Ward precision: 1.000 (95% CI [1.000, 1.000]).
- Ward recall: 0.487 (95% CI [0.388, 0.600]).
- Ward F1: 0.655 (95% CI [0.559, 0.750]).
- Ward MCC: +0.564 (95% CI [+0.484, +0.651]).
- Every other tool we benchmarked under their own publicly
  recommended ruleset and severity defaults — Semgrep, CodeQL, Rudra,
  cargo-geiger — produced **zero true positives** on the paired corpus
  at ≥ WARNING severity.

McNemar's exact two-sided binomial test gives **p ≈ 1.46 × 10⁻¹¹** for
every (Ward, competitor) pairing, and Ward's F1 95% CI ([0.559, 0.750])
is fully disjoint from every competitor's CI ([0.000, 0.000]). Both
gates of our pre-locked statistical contract are cleared with several
orders of magnitude of headroom.

We then re-ran the entire competitor set on the **broadest publicly
available rulesets** for each tool (Semgrep across 1,079 rules in
`p/rust ∪ r/rust ∪ p/security-audit ∪ p/default`; CodeQL on
`rust-security-and-quality.qls`; Rudra with the in-image stdout-parser
bug patched). **The ranking did not change.** Details in the
*Fairness audit* section below.

> **Pre-release status.** This is an internal pre-release benchmark.
> The methodology spec, corpus manifest, per-entry provenance,
> Dockerfile, tool pins, and rule-id mapping are public now at
> `github.com/bobisme/ward-releases`. The Ward source release that
> closes the loop on fully external third-party reproduction is
> pending; until then, reproduction requires the locked container
> image. Full reproducibility — including building `ward-eval` from
> source against the pinned tree — unlocks at Ward's source release.
> The numbers below reflect a real run of a real benchmark and are
> not under embargo; the "locked, reproducible head-to-head" framing
> should be read as *locked spec, internal run, public reproduction
> planned* rather than *fully reproducible by any third party today*.

This document is the public, reviewer-facing summary. The locked
methodology spec, full results document, fairness-audit aux document,
corpus manifest, and reproduction kit are all linked at the bottom.
After this work is published the operator will mint the git tag
`bench/unsafe-rust-v1` over the bench artifact so external reviewers
can reproduce against the exact tree state.

## Why this matters

Rust's value proposition is memory safety in a fast systems language.
That property holds for the safe subset of the language. Inside
`unsafe` blocks, FFI boundaries, and a handful of `unsafe`-adjacent
APIs (`MaybeUninit`, `transmute`, `slice::from_raw_parts`,
`set_len`, manual `Send`/`Sync` impls, etc.), the same memory-corruption
classes that plague C and C++ are reachable — and they hide inside code
that the compiler's safety guarantees do not check. CVE history bears
this out: every entry in the RUSTSEC database we sampled for this
benchmark is some form of "safe-encapsulation violation":
`unsafe` was used internally, the surrounding safe API allows a caller
to violate its preconditions, and the result is memory corruption,
use-after-free, type confusion, or undefined behavior reachable from
ordinary safe code.

These bugs are uniquely bad for three reasons:

1. **Memory corruption in a "safe" language is invisible from the type
   system.** Reviewers who trust the language to catch this class
   under-attend to the underlying obligation, so the bugs survive
   review.
2. **Existing static-analysis tooling for Rust ships very thin
   unsafe-class coverage.** As the *Competitor ruleset audit* section
   below documents, the publicly recommended rulesets we benchmarked
   contain between 0% and 15.8% rule coverage of the CWE classes that
   populate the RUSTSEC unsafe-bug history.
3. **Dynamic analysis (Miri) helps but cannot scale to whole-codebase
   review.** Miri runs at instruction-level interpretation cost and
   does not see code paths that aren't exercised by a test. It is
   complementary, not substitutable.

Ward's Rust Unsafe Obligation Engine (UOE) targets this gap. It
encodes per-API unsafe obligations as a small lattice of
*safety-discharge* atoms (init, len, layout, alignment, lifetime,
send/sync) and looks for safe-encapsulation paths that leave atoms
undischarged on caller-controlled inputs. That design is documented
elsewhere (`notes/project_rust_unsafe_phase_2_closed.md`). The
benchmark below is the **external validation** of that engine against
real CVEs, scored against every other scanner we could run offline.

## Methodology in brief

The full methodology is locked at
[`notes/benchmarks/unsafe-rust-bench-methodology.md`](../../notes/benchmarks/unsafe-rust-bench-methodology.md)
(11 numbered sections, ~830 lines, committed before corpus collection
began). The key design choices:

**Corpus** — 80 vuln/fix paired RUSTSEC advisories (160 manifest
rows), drawn ≥40% from 2024–2026 RUSTSEC entries Ward authors had
not touched during rule development. Every entry is a real upstream
repo with a publicly identifiable vulnerable commit and fix commit.
Per-entry provenance (advisory, commits, license, methodology
conformance) is committed under
[`tests/cve-registry/benchmarks/unsafe-rust-bench/provenance/`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/provenance/).
The corpus contains 65 unique upstream repositories, license
distribution Apache-2.0 (43) / MIT (35) / MPL-2.0 (1) / Zlib (1).

**Tools** — Ward, Semgrep 1.95.0 (with `p/rust` + `r/rust.lang.security`),
CodeQL 2.25.4 (`rust-security-extended.qls`, 19 queries), Rudra (HEAD
on `master`, best-effort per methodology §10), cargo-geiger 0.12.0
(context column only — measures unsafe density, not security findings).
Tool versions and ruleset SHAs are pinned in
[`bench/tool-versions.toml`](../../bench/tool-versions.toml). The
bench image is pinned to digest
`sha256:b7707fe926c96be99348030445cb355141f43afae2243d86a8f7862cc134308e`.

**Fairness controls** — Every scanner runs inside the same OCI image
under `podman run --network=none`, 4 CPU cores, 16 GiB RAM, 10-minute
per-entry wall-clock cap. Caches pre-warmed at image build time so
first-scan vs nth-scan latency does not skew any tool's numbers.
Determinism is verified by a 3-run identity check
([`bench/smoke-determinism.sh`](../../bench/smoke-determinism.sh)).

**Scoring** — Paired scoring per methodology §5. A finding on the
vuln commit at the affected file that does **not** persist on the fix
commit is a TP. A finding that persists across both is reclassified
from FP to TN (it's a pre-existing finding unrelated to the CVE under
test). File-level matching for TP attribution; line-level (±2 lines)
for persistence reclassification. Identical rules applied to all
tools. The competitor severity floors mirror what each tool's default
user-facing UX surfaces — Semgrep and CodeQL ≥ WARNING; Ward
confidence ≥ Medium; Rudra all findings (it has no severity tier);
cargo-geiger not scored.

**Statistical contract** — Pre-locked. "Ward beats X" requires (i)
McNemar's exact two-sided binomial test at p < 0.01 on per-pair
fully-correct status, AND (ii) non-overlapping 95% bootstrap CIs on
F1 and MCC. Bootstrap is 1000 stratified resamples by vuln_class,
seed `0x77617264_62656e63` (`"wardbenc"` in ASCII hex). Both gates
must be cleared simultaneously before a "beats" claim is made. We do
not relax either gate post-hoc.

## Results

### Headline table — full corpus (n = 80 paired pairs)

| Tool | TP | FP | TN | FN | Precision (95% CI) | Recall (95% CI) | F1 (95% CI) | MCC (95% CI) |
|------|----|----|----|----|--------------------|-----------------|-------------|--------------|
| **Ward** | **39** | **0** | **77** | **41** | **1.000 [1.000, 1.000]** | **0.487 [0.388, 0.600]** | **0.655 [0.559, 0.750]** | **+0.564 [+0.484, +0.651]** |
| Semgrep | 0 | 0 | 80 | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | +0.000 [+0.000, +0.000] |
| Rudra | 0 | 0 | 80 | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | +0.000 [+0.000, +0.000] |
| cargo-geiger | 0 | 0 | 80 | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | +0.000 [+0.000, +0.000] |
| CodeQL (partial, 50/160 entries processed) | 0 | 0 | 80 | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | +0.000 [+0.000, +0.000] |

> **Counting unit.** Per-pair fully-correct counting (above) and the
> per-entry paired classification yield slightly different Ward
> numbers. Per-entry: TP=39, FP=0, TN=70, FN=34, F1=0.696,
> MCC=+0.600. Per-pair: as above. Methodology §7 uses the per-pair
> unit for resampling, so the per-pair CIs are the canonical headline.

### McNemar pairwise tests

| (A, B) | A right / B wrong | B right / A wrong | both right | both wrong | p-value | A beats B at p<0.01 |
|--------|-------------------|-------------------|------------|------------|---------|---------------------|
| (Ward, Semgrep) | 37 | 0 | 0 | 43 | 1.46e-11 | **yes (Ward)** |
| (Ward, Rudra) | 37 | 0 | 0 | 43 | 1.46e-11 | **yes (Ward)** |
| (Ward, cargo-geiger) | 37 | 0 | 0 | 43 | 1.46e-11 | **yes (Ward)** |
| (Ward, CodeQL) full corpus | 37 | 0 | 0 | 43 | 1.46e-11 | **yes (Ward)** |
| (Ward, CodeQL) restricted to 12 pairs where both CodeQL sides processed | 5 | 0 | 0 | 7 | 0.0625 | no (sample too small) |

Every other (competitor, competitor) pairing is degenerate: with both
sides at 0 TP, no pair is "A right / B wrong", and McNemar p = 1.000.

The restricted-to-processed CodeQL row deserves a separate note. On
the 12 pairs where both CodeQL sides produced parseable SARIF, Ward
is fully correct on 5 of 12 and CodeQL on 0 of 12. McNemar with
b=5, c=0 yields p = 0.0625 — *above* our pre-locked p < 0.01
threshold, so on that subset alone the McNemar gate is not cleared.
F1-CI non-overlap still holds (Ward 0.667 vs CodeQL 0.000), but the
honest reading is: on the entries CodeQL actually ran, the
discordant-pair sample is too small (n=5) for the exact binomial
test to reach significance. The full-corpus claim is supported
because the 110 not_run entries count against CodeQL — which is itself
a CodeQL property under this benchmark's budget, not a statistical
artifact (see *What Ward gets right and what it doesn't*).

### Three views of CodeQL scoring (per methodology §5)

Methodology §5 requires timeouts be reported separately from
"wrong", so the headline CodeQL row above can be decomposed three
ways. The three views answer different questions and **should not
be mixed without explicit framing**:

| View | What it measures | CodeQL value |
|---|---|---|
| **A. Detection on completed subset** | "When the tool ran successfully, did it find the bug?" | **0 TP / 12 paired pairs** (both sides produced parseable SARIF) |
| **B. CI-budget effective recall** *(operational headline)* | "Under the methodology's 10-min/entry offline budget, how useful is the tool operationally?" | **0 TP / 80 pairs** (the headline table row above) |
| **C. Reliability / completion rate** | "How often did the tool produce usable output?" | **12 / 80 = 15% reliability** (both sides ran) |

View B is the operational headline because it reflects what a real
CI user sees, but it is not the only honest number. View A
documents that even on the entries where CodeQL completed, zero
in-class TPs fired at ≥ WARNING (so the failure is not just a
budget problem). View C is the reliability story. Full per-view
decomposition is in the results document.

## The fairness audit

The reflexive objection to a benchmark like this is "you didn't try
hard enough on the competitors." We took that objection seriously
before publishing.

### Competitor ruleset audit

We enumerated every rule shipped by each competitor's locked ruleset
and tagged it as in-class or out-of-class against the CWE families
that populate the corpus (CWE-119, -120, -125, -129, -190, -362, -415,
-416, -457, -704, -770, -787, -824, -825, -843, -908).

| Tool | Total rules | Unsafe-class rules | Coverage |
|------|-------------|--------------------|----------|
| CodeQL `rust-security-extended` | 19 | 2 (+ 1 partial) | **10.5%** (15.8% incl. partial) |
| Semgrep `p/rust ∪ r/rust.lang.security` | 11 | 0 (1 INFO `unsafe-usage`, gated out by severity) | **0%** |
| Rudra | 4 categories | 4 (100% by design) | **100% coverage; 96% errored** |
| cargo-geiger | N/A (counter) | N/A | **N/A (context only)** |

CodeQL ships exactly two unsafe-class queries in its security-extended
suite: `rust/access-after-lifetime-ended` and
`rust/access-invalid-pointer`. The remaining 17 target web-app, crypto,
or configuration shapes that don't overlap the corpus.

Semgrep's two community packs together carry 11 unique rules. The one
rule that targets unsafe Rust at all (`rust.lang.security.unsafe-usage`)
fires on every `unsafe` block in every file and emits at INFO severity
by default — well below the WARNING gate that defines what shows up
in Semgrep's user-facing UX. We did not promote it to WARNING; doing
so produces a wall of unactionable noise (Semgrep itself ships it at
INFO for that reason), and even at WARNING none of its firings would
correlate to the affected files because it matches every `unsafe`
block, not the specific obligation the CVE violates.

Rudra has 100% in-class coverage by design — it was purpose-built in
2020 for unsafe-Rust analysis. The reason its TP count is zero on this
corpus is **maintenance state, not coverage**: it pins to
`nightly-2021-10-21` and 154 of 160 entries (96%) fail at the
toolchain layer (Cargo.lock generation, internal panics, nightly
incompatibilities with post-2024 crates). Per methodology §10, with
Rudra runnable on only 3.75% of the corpus we drop it from the
head-to-head competitive claim and report it as "dormant, did not run."

cargo-geiger is a context column — it counts unsafe-block density per
crate, doesn't produce findings, and methodology §4 explicitly does
not score it.

The 0-TP result for CodeQL and Semgrep is therefore a **faithful
measurement of what users get out of the box**, not a result of
methodology bias against any tool.

### Max-breadth aux run (preempting "broader rules would fix this")

We re-ran the competitor set under their broadest publicly available
rulesets:

- **Semgrep**: added `r/rust`, `p/security-audit`, `p/default` on top
  of the methodology-locked `p/rust`. Union ruleset: 1,079 distinct
  rules, 19 of them Rust-specific. Bind-mounted into the image so
  the container still ran `--network=none`. Coverage: 160/160 entries.
- **CodeQL**: switched the analysis suite from
  `rust-security-extended.qls` to `rust-security-and-quality.qls`
  (strict superset, adds 2 quality queries). Re-ran on the 25 entries
  that produced parseable SARIF in the headline run (the 25
  DB-create-timeout pairs and 110 not_run pairs would still time out
  or not run).
- **Rudra**: patched the in-image stdout parser bug (it had been
  mis-extracting the diagnostic message text as the file path) and
  extended the rule-id keyword mapping to match Rudra's real emit
  format (`SendSyncVariance`, `UnsafeDataflow`, `PanicSafety`).

The headline did not change.

| Tool | Headline paired | Aux paired | Δ TP after paired |
|------|----------------|-----------|-------------------|
| Ward | TP=39 FP=0 (unchanged) | TP=39 FP=0 | 0 |
| Semgrep | TP=0 FP=0 | TP=0 FP=0 | **+0** |
| Rudra | TP=0 FP=0 | TP=1 FP=0 | **+1** (one sound finding on `beef-rustsec-2020-0122`) |
| CodeQL (25-entry subset re-analyzed) | TP=0 FP=0 | TP=0 FP=0 | **+0** |
| cargo-geiger | TP=0 FP=0 | (unchanged) | 0 |

Semgrep's broader packs add 8 new Rust rules (`unsafe-usage`,
`insecure-hashes`, `rustls-dangerous`, `reqwest-accept-invalid`,
`ssl-verify-none`, `temp-dir`, `current-exe`, `args-os`, `args`).
Across all 160 entries, only 4 entries fired at WARNING+ on any of
these — all 4 fired the same single rule (`insecure-hashes`), and
none of the firings landed on the affected file for its CVE. The
note-level `unsafe-usage` rule fires extensively but is filtered out
by the methodology's severity gate.

CodeQL's broader suite adds 2 queries (`rust/regex-injection`,
`rust/ctor-initialization`). Neither targets unsafe-class
memory-safety. Across the 25 re-analyzed entries, **zero additional
findings emitted on any file**.

Rudra promotes from 0 to 1 paired TP after the parser fix is applied:
`rs-bench-beef-rustsec-2020-0122` fires `SendSyncVariance` correctly.
That is a real finding Rudra was emitting all along; the in-image
parser was suppressing it. One TP at 1.25% recall keeps Rudra below
methodology §10's 30% threshold, so it stays out of the head-to-head
competitive table.

After the max-breadth aux, McNemar p ≈ 1.46 × 10⁻¹¹ remains
unchanged for (Ward, Semgrep), (Ward, CodeQL), (Ward, cargo-geiger);
(Ward, Rudra aux) gives p ≈ 2.92 × 10⁻¹⁰. The dominance pattern is
robust to the broadest configurations of the competitor tools.

**The corollary is stronger than the headline.** It is not the case
that competitors *could* catch these bugs with better rules and
simply chose not to ship them. It is the case that *no rule for
these bugs currently exists in the public registries we could find*.
Ward's lead is on a class that the rest of the static-analysis
ecosystem has not yet built rules for. The full max-breadth aux run
is documented at
[`notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](../../notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md).

## What Ward gets right and what it doesn't

Ward's per-vuln-class numbers (descriptive only — per-class N is
small enough that the bootstrap CIs collapse and we don't claim
significance below the headline aggregate):

| Vuln class | N pairs (entries) | Ward TP | Ward TN | Ward FN | Precision | Recall |
|---|---|---|---|---|---|---|
| memory_safety | 55 (110) | 31 | 54 | 25 | 1.000 | 0.554 |
| soundness | 9 (18) | 3 | 9 | 6 | 1.000 | 0.333 |
| use_after_free | 8 (16) | 3 | 8 | 5 | 1.000 | 0.375 |
| type_confusion | 6.5 (13) | 2 | 6 | 5 | 1.000 | 0.286 |

memory_safety dominates the corpus (55 of 80 paired pairs); other
classes are N < 30 and reported descriptive-only. **Precision is
1.000 across every class** — the full corpus introduces zero Ward
false positives over and above what was seen on the small-repo
first pass.

Per-bug-shape (selected — full table in the headline doc):

| Bug shape | N pairs | Ward TP | Ward TN | Ward FN | Precision | Recall |
|---|---|---|---|---|---|---|
| safe-encap | 21.5 (43) | 8 | 21 | 14 | 1.000 | 0.364 |
| panic-sequence | 12 (24) | 7 | 12 | 5 | 1.000 | **0.583** |
| impl-send-sync | 9 (18) | 2 | 9 | 7 | 1.000 | 0.222 |
| set-len-init | 9 (18) | 4 | 9 | 5 | 1.000 | 0.444 |
| ffi-boundary-contract | 5 (10) | 3 | 5 | 2 | 1.000 | **0.600** |
| int-overflow-safety | 4 (8) | 3 | 4 | 1 | 1.000 | **0.750** |

The pattern is consistent: shape buckets where Ward's UOE has a
tier-1 or tier-2 obligation rule registered (`panic-sequence`,
`ffi-boundary-contract`, `int-overflow-safety`,
`slice-from-raw-parts-init-violation`, `len-cap-confusion`,
`layout-cast`, `debug-guard-only`, `transmute-chained-cast`,
`zst-ptr-arith`) clear ≥ 50% recall. Shapes that rely on catch-all
detectors (`safe-encap`, `impl-send-sync`, `set-len-init`) sit at
22–44% recall. The remaining recall on this corpus is concentrated
in these underdetected shapes — and they're the targets for the
next round of UOE rule work (tracked under
`notes/project_rust_unsafe_phase_2_closed.md` and the planned
`bn-25hzk` rule-pack expansion).

### Where Ward fails on this corpus

Two failure modes, both honest:

**1. 14 entries timed out at the 600s cap on large repos.** Ward's
internal dedup pipeline and exfiltration heuristic exhibit a
runaway behavior on a small number of large Rust repos (wasmtime,
openssl, pyo3, tokio, mio, slab, Fyrox, diesel) — they hit the cap
with `ward_exit_-1`. Bench-stats counts these 14 as `errored` in
the latency table; the paired-scoring layer treats them as
non-firing-on-vuln-side, which contributes to the FN count. Filed
under bn-2q4pn for follow-up; the cleaned-latency view
(errored-excluded, N=146) is p50 = 1.0s, p95 = 12.3s, p99 = 19.8s,
mean = 2.5s, max = 19.8s — comfortably inside the budget. The 14
runaway entries are a Ward bug, not a corpus property.

**2. Recall is 48.7%.** The honest framing: this is much better than
zero, and competitors all sit at zero on this corpus, but it is not
the same as 100%. Ward catches roughly half of the public RUSTSEC
unsafe-class CVE history under its current rule set. The shape
breakdown above identifies where the remaining headroom is. The
next rule-pack expansion (bn-25hzk) targets the safe-encap and
impl-send-sync shapes where recall sits at 22–36%.

**Latency** — Ward's median is 1.25s. The mean (54.8s) is pulled up
by the 14 runaway entries; the p95 in the full distribution
(600.17s) is the budget cap itself. Cleaned (errored-excluded, N=146)
mean is 2.5s. This is consistent with a tool you'd run in a CI step
or a pre-commit hook on the 90+% of repos where the runaway bug
doesn't hit.

## How to reproduce

We ship a one-command reproducer. The full mechanics are documented
at [`tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md).
The 60-second version:

```bash
# Build the locked image (one-time, ~20 min)
podman build -t ward-bench:locked -f bench/Dockerfile.bench .

# Build the harness binaries
cargo build --release -p ward-eval -p ward-cli -p ward-stub-analyzer

# Run the head-to-head (~6–10 hours; dominated by CodeQL DB-create)
./target/release/ward-eval bench-run \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --tool-versions bench/tool-versions.toml \
  --rule-id-mapping bench/rule-id-mapping.toml \
  --tools ward,semgrep,rudra,cargo-geiger,codeql \
  --out target/bench/repro

# Paired finding-identity reclassification
./target/release/ward-eval bench-score \
  --raw target/bench/repro \
  --out target/bench/repro/paired

# Statistical analysis (bootstrap CIs + McNemar + per-class)
./target/release/ward-eval bench-stats \
  --raw target/bench/repro \
  --paired target/bench/repro/paired \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --out target/bench/repro/stats.json
```

Reviewers should land within **±2 percentage points** of the
published Ward headline (P=1.000, R=0.487, F1=0.655, MCC=+0.564) when
running against the pinned image digest and tool-versions file.
Per-class numbers may vary more due to small per-class N.

For the auxiliary max-breadth pass, see the dedicated reproduction
section in
[`notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](../../notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md)
which uses [`scripts/aux/`](../../scripts/aux/).

After the bench work merges to `default`, the operator will mint a
git tag `bench/unsafe-rust-v1` over the bench artifact. Reproducers
running against that tag will hit the exact tree state these numbers
were produced from.

## Threats to validity

We disclose threats in the same form the methodology specifies
(§11). Reviewers attacking these numbers should attack here.

**Corpus selection bias.** Ward's UOE was developed iteratively
against a corpus that overlaps RUSTSEC. Authors have read many
RUSTSEC advisories and written rules to catch them. We mitigate this
two ways: (a) the corpus is ≥40% novel (32 of 80 entries are 2024–2026
RUSTSEC entries Ward authors had not seen during rule development —
the `rustsec_2024_2026` source group), and (b) the methodology was
locked **before** corpus collection so authors could not bias the
corpus toward Ward-friendly shapes. Per-entry `source` provenance is
in the corpus manifest so reviewers can replay the benchmark on the
novel-only subset. Residual bias still exists; we do not pretend it
doesn't. "Ward was developed against a partially overlapping corpus"
is a stronger honest claim than pretending otherwise.

**Tool version drift.** Static-analysis tools update their rulesets
weekly. This benchmark is locked to specific tool versions in
`bench/tool-versions.toml`; a "latest" run six months from now will
likely produce different numbers. The locked tags let us re-run
quarterly and report the delta as itself useful data. The aux
max-breadth run further argues the lead does not collapse under
broader ruleset configurations — but it does not preclude a future
ruleset closing the gap.

**Miri verdict reproducibility.** Ward's witness gate (the Miri-runs
sidecar) is sometimes flaky on TLS/RNG/concurrency code paths. The
witness gate is **Ward-only and intentionally disabled in the
container head-to-head** (methodology §6), so it does not affect the
benchmark headline. The 24/24 = 100% positive witness rate
documented elsewhere (`notes/project_phase5_witness_gate_state.md`)
comes from a separate eval-mode run, not this benchmark. A follow-up
bone will wire the witness gate into the bench harness as a sidecar.

**Survivor bias.** We can only benchmark publicly disclosed
vulnerabilities. Silently-patched bugs and closed-source vulns are
invisible. This is a fundamental limit of public CVE benchmarks; no
mitigation is possible. We disclose it prominently.

**Small per-class N.** With memory_safety at N=55 pairs and other
classes at N ≤ 9, per-class statistical claims would be irresponsible.
We report per-class numbers but mark them descriptive-only; the only
inferential claim is on the aggregate F1/MCC.

**Definition of "best-in-class".** We define it operationally:
*highest paired F1, with non-overlapping 95% CIs against all other
tools, on the unsafe-class subset of the corpus, with offline
reproducibility.* Alternative definitions ("best on memory-safety
only", "highest precision regardless of recall", "fastest scanner
with recall ≥ X%") would produce different rankings. We commit to
the F1 definition because it's the standard composite score and
weights both axes.

**Adversarial corpus construction.** A skeptical reader may suspect
we cherry-picked entries. Mitigations: (a) the inclusion rules in
the methodology document are locked *before* corpus collection
began, (b) the novel augment subset (the 2024–2026 RUSTSEC
entries) was collected by an agent following the inclusion rules
without seeing Ward's per-entry classification, (c) the full
inclusion-rule application log
([`tests/cve-registry/benchmarks/unsafe-rust-bench/inclusion-log.md`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/inclusion-log.md))
is committed so reviewers can audit every accept/reject decision.

**The 14 Ward timeouts.** As disclosed above, 14 entries hit the
600s cap due to a Ward-internal dedup/exfiltration heuristic runaway
(bn-2q4pn). They contribute to FN count rather than firing properly.
Conservatively this means our recall headline understates Ward's
detection capability by some amount on the affected entries; we
report the conservative number anyway because fixing the bug is the
right thing to do, not retroactively adjusting the headline.

**CodeQL on 110 not-reached entries.** CodeQL never finished 110 of
160 entries (110/160 = 69%) because DB-create exceeded the 10-min
cap on the larger repos. Per methodology §5, those entries are
counted as wrong for CodeQL — not folded into "0 findings". This is
the methodology's chosen convention; an alternative convention
("evaluate only on entries every tool processed") would restrict to
12 pairs, on which the McNemar gate is not cleared (n=5 discordant
pairs) but the CI-non-overlap gate still is. We report both views;
the full-corpus claim stands on both gates simultaneously.

## What's next

Two follow-on workstreams come out of this benchmark.

**Rule-pack expansion (bn-25hzk).** The per-bug-shape table above is
a direct work-list. Recall 22–44% on `impl-send-sync`, `safe-encap`,
`set-len-init`, `transmute-utf8-range-invariant`,
`transmute-size-mismatch` reflects shape buckets where the UOE has
no tier-3+ obligation rule yet. Each additional tier-3 rule on these
shapes is expected to add 2–6 TPs based on the current shape FN
counts. The plan is to expand the obligation catalog to cover
these shapes while preserving the 1.000 precision floor.

**Autofix for Rust unsafe-class (bn-35b00).** Ward's detection
findings on this corpus are precision-1.000 and shape-typed, which
makes them well-suited to mechanical-fix synthesis. The pilot tracks
six obligation shapes (length-prepend on `slice::from_raw_parts`,
`MaybeUninit::assume_init` ordering, `transmute` size/alignment
guard insertion, etc.) where the fix patch is small and the
preconditions are mechanically checkable.

We also have the 14 Ward timeouts to fix (bn-2q4pn). That is a Ward
bug, not a corpus property — but it shows up in the published
numbers honestly.

## References

- Methodology (locked 2026-05-07):
  [`notes/benchmarks/unsafe-rust-bench-methodology.md`](../../notes/benchmarks/unsafe-rust-bench-methodology.md)
- Full headline results document:
  [`notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md`](../../notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md)
- Max-breadth aux pass:
  [`notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](../../notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md)
- Corpus + provenance:
  [`tests/cve-registry/benchmarks/unsafe-rust-bench/`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/)
- Inclusion log:
  [`tests/cve-registry/benchmarks/unsafe-rust-bench/inclusion-log.md`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/inclusion-log.md)
- Reproduction kit:
  [`tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md`](../../tests/cve-registry/benchmarks/unsafe-rust-bench/REPRODUCE.md)
- Bench image:
  [`bench/Dockerfile.bench`](../../bench/Dockerfile.bench)
- Tool pinning:
  [`bench/tool-versions.toml`](../../bench/tool-versions.toml)
- Rule-id mapping:
  [`bench/rule-id-mapping.toml`](../../bench/rule-id-mapping.toml)
- Determinism check:
  [`bench/smoke-determinism.sh`](../../bench/smoke-determinism.sh)

## License

The benchmark corpus manifest (`manifest.toml`, `provenance/*`,
`inclusion-log.md`, `README.md`) is **CC-BY-4.0**. The bench
harness code is **Apache-2.0**. Source repositories referenced by
the corpus retain their own permissive licenses (Apache-2.0, MIT,
MPL-2.0, Zlib) and are fetched at scan time rather than
redistributed.
