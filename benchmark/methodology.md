---
title: Public head-to-head benchmark — Rust unsafe-class vulnerability detection
date: 2026-05-07
bone: bn-3cgmj (parent: bn-1ti5m)
status: methodology specification (locked before corpus collection)
audience: external reviewers, downstream corpus/runner/measurement bones
---

# Unsafe-Rust Head-to-Head Benchmark — Methodology

> **Pre-release status.** Locked spec, internal pre-release. Public
> reproduction unlocks at Ward source release (planned). Corpus,
> Dockerfile, tool pins, and rule-id mapping are published now for
> external review at `github.com/bobisme/ward-releases`.

## Executive summary

This document specifies a public, reproducible benchmark whose claim under
test is: **Ward is best-in-class on detection of Rust unsafe-class
vulnerabilities (memory-safety, use-after-free, type-confusion,
undefined-behavior, data-race, soundness) on real CVE-paired code, against
all publicly available comparable scanners as of mid-2026.** The benchmark
measures paired precision, paired recall, MCC, F1, and per-class breakdown
on N≥80 vuln/fix-paired RUSTSEC entries; it pins tool versions, isolates
runtime budgets, blocks the network during scan, and reports bootstrap
confidence intervals so the headline cannot be over-claimed. Ward's
internal Miri-witness machinery is reported as a separate Ward-only axis
(positive-witness rate) that other tools cannot match — it informs but
does not enter the head-to-head MCC. The methodology is locked before
corpus collection so the benchmark cannot be selectively populated with
shapes Ward already detects.

## Section index

1. [Motivation and claim under test](#motivation-and-claim-under-test)
2. [Corpus selection criteria](#corpus-selection-criteria)
3. [Tool selection and version pinning](#tool-selection-and-version-pinning)
4. [Fairness controls](#fairness-controls)
5. [Scoring rules](#scoring-rules)
6. [Witness rate as Ward-only axis](#witness-rate-as-ward-only-axis)
7. [Statistical reporting](#statistical-reporting)
8. [Latency and resource axis](#latency-and-resource-axis)
9. [Reproduction requirements](#reproduction-requirements)
10. [Out of scope](#out-of-scope)
11. [Threats to validity](#threats-to-validity)
12. [Resolutions log](#resolutions-log)
13. [Amendment log](#amendment-log)

## Motivation and claim under test

Ward's Rust Unsafe Obligation Engine (UOE) shipped through Phase 5 with
strong internal metrics: paired precision 72.9%, paired recall 83.7%,
MCC +0.534 on the full 3562-entry corpus (post-Phase-2 baseline,
2026-05-02; see `notes/post-phase-2-eval-2026-05-02.md`). The Phase 5
Miri-witness gate currently scores 24/24 = 100% positive witness rate on
the runnable subset of phase5-eligible entries, and per-shape paired recall
on the unsafe-class shapes (panic-sequence 100%, layout-cast 100%,
ffi-boundary-contract 100%, slice-from-raw-parts 100%, safe-encap 84%,
int-overflow 83%) clears the ≥80% mark for most shapes.

These numbers support the **internal** claim that Ward is best-in-class on
Rust unsafe scanning. **They do not yet form a public, reproducible
proof.** The historical eval-competitor work
(`notes/eval-competitor-2026-03-22.md`) covered all five Ward languages
with a small (364-entry) harness; the more recent full-corpus runs have
been Ward-only. Sibling tracks (best-in-class Rust scanner bn-25hzk,
rust-autofix bn-35b00) won't close this gap by themselves — both rest on
detection quality whose external validity is what this benchmark
establishes.

The benchmark must therefore: (a) be public and reproducible by a
third party from a fresh clone, (b) include the most credible
publicly-available competitors, (c) score with Ward's existing
diff-aware paired methodology so headline numbers reconcile to internal
runs, (d) be locked-in as a methodology before corpus collection so
authors cannot bias the corpus toward their own tool's shapes, and (e)
disclose its own threats to validity in enough detail that a sophisticated
reader can reproduce, audit, or attack the result.

## Corpus selection criteria

### Target size

**N ≥ 80 paired entries** (40 vuln + 40 fix commits at minimum). Each
entry has a vulnerable commit and a fixing commit on the same upstream
repository. Larger N is preferred up to a point; beyond ~250 paired
entries the marginal information per entry drops sharply (CodeQL recall
plateaus, Semgrep's Rust ruleset is narrow enough that incremental
entries mostly add no information). **Cap target: 200 paired entries.**

### Inclusion: RUSTSEC + GHSA-rust criteria

A candidate entry is included iff **all** of the following hold:

1. **Source advisory**: listed in RUSTSEC (`rustsec/advisory-db`) or
   GHSA with ecosystem `cargo`. Both feeds are public and dated.
2. **In-scope vuln class**: `vuln_class ∈ {memory_safety,
   use_after_free, type_confusion, undefined_behavior, data_race,
   soundness}`. Concretely, a CWE in {CWE-119, CWE-120, CWE-125,
   CWE-129, CWE-190, CWE-415, CWE-416, CWE-457, CWE-787, CWE-824,
   CWE-843, CWE-908} is the deciding signal. Borrow-alias, Send/Sync
   unsoundness, panic-sequence drop-ordering, and provenance-loss bugs
   count as soundness even when the proximate CWE is broader.
3. **Public fix commit**: a single, identifiable fix commit (or a small
   ≤3-commit fix series) on the upstream public repository. The fix
   must be merged to a release branch — not a draft PR, not a private
   patch.
4. **Vulnerable commit identifiable**: the parent of the fix commit (or
   the advisory's `unaffected_commit_range` lower bound) is the
   vulnerable commit. If the advisory pre-dates the fix by more than 30
   days, prefer the parent of the fix commit as the vulnerable commit so
   the diff is minimal.
5. **Repository is public, alive, and clonable** at scan time. Archived
   or yanked-only crates are excluded if the upstream repo is gone.
6. **License permits redistribution of the corpus manifest**. The
   manifest stores SHAs and metadata, not source — but transitive
   inclusion of the source via cached repos requires that the repo
   license permits redistribution. Target: MIT / Apache-2.0 /
   MIT-OR-Apache-2.0 / BSD-3-Clause / MPL-2.0 / CC0. Excluded: GPL-3.0
   only crates (we do not redistribute source under copyleft to avoid
   downstream license-incompatibility concerns), proprietary repos.

### Exclusion rules

A candidate is excluded if **any** apply:

- **Fix-only entries** (advisories with no public vulnerable commit,
  e.g. private security report → public fix). These cannot be paired-
  scored.
- **No public PoC** AND **vulnerable code is not visible from the
  advisory**. We need to verify the rule's TP claim against actual
  code, not against an advisory description alone.
- **Duplicate of an already-included CVE** (same upstream bug under
  multiple advisory IDs). Keep the canonical RUSTSEC ID.
- **proc-macro-only vulnerabilities** (CWE involves expansion of
  macro-defined code at compile time). Reason: all candidate tools
  including Ward struggle here; including these would give a noisy
  comparison without informational value. Listed under [out of
  scope](#out-of-scope).
- **Vulnerability requires running tests / build scripts** that fetch
  external resources at build time. We require the corpus to be
  scannable offline; fetching during scan is forbidden.
- **Fix commit refactors >50% of the affected file**. Paired scoring
  requires that the fix is targeted; a wholesale rewrite makes
  diff-aware FP reclassification meaningless because almost everything
  changes.
- **Vulnerability is in `unsafe`-free crate code** but the actual UB is
  in a transitive C dependency (e.g., `libc` calls). The bug is real
  but Rust-tool detection requires Rust source signals; this is a
  cargo-audit-class issue.

### Inheriting from Ward's existing manifest

Ward's CVE manifest (`tests/cve-registry/manifest.toml`) contains 188
entries with `vuln_class ∈ {memory_safety, use_after_free,
type_confusion}` and 64 marked `phase5_eligible = true` (32 paired vuln/fix
pairs imported from RustXec MSR'26 plus extras; see `notes/rustxec-import-2026-05-01.md`).
**Decision: subset, do not inherit verbatim, and do not rebuild from scratch.**

Rationale:

- *Verbatim inherit*: rejected — these entries were curated against
  Ward's coverage. Pure inheritance would import authoring bias into the
  benchmark.
- *Rebuild from scratch*: rejected — it duplicates ~120 hours of
  curation work already done, and the existing entries are
  well-validated (each has an `expected_finding` tied to a specific
  affected file).
- *Subset + augment* (chosen): take the subset of `manifest.toml`
  entries that *also* satisfy a third-party gating filter — namely,
  appearing in (a) a published academic memory-safety dataset such as
  RustXec MSR'26 or RustSan or (b) RUSTSEC's manually-curated
  memory-safety category — then **augment** with newly-collected
  RUSTSEC entries from 2024–2026 (post the manifest's last refresh)
  that no Ward author has previously used to tune a rule. The augment
  must reach ≥40% of the final corpus to materially dilute author
  bias. Track the provenance of each entry in the published corpus
  metadata (`source: rustxec_msr_2026 | rustsec_2024_2026 | manual_curation`).

This subset+augment policy is the load-bearing fairness control on the
corpus side — see [threats to validity](#threats-to-validity).

### Per-entry metadata schema (locked)

Each corpus entry (TOML format, mirroring `tests/cve-registry/manifest.toml`):

```toml
id = "rs-bench-rustsec-XXXX-YYYY"           # benchmark-namespaced ID
expected_result = "tp" | "tn"
language = "rust"
repo_url = "https://github.com/.../...git"
vulnerable_commit = "<sha>"
fixing_commit = "<sha>"                     # equal to vulnerable_commit for "tn" rows
cve = "RUSTSEC-YYYY-NNNN"
cve_id = "CVE-YYYY-NNNNN"                   # if assigned
cwe = "CWE-NNN"
vuln_class = "memory_safety" | "use_after_free" | "type_confusion" |
             "undefined_behavior" | "data_race" | "soundness"
bug_shape = "<shape-id>"                    # e.g. "safe-encap", "slice-from-raw-parts",
                                            # "int-overflow", "layout-cast", "transmute-validity"
expected_severity = "low" | "medium" | "high" | "critical"
affected_file = "path/to/file.rs"           # required for "tp"
expected_finding = "<one-line description>"
fix_kind = "<kind>"                         # e.g. "bounds-check", "lifetime", "transmute-removal"
license = "MIT" | "Apache-2.0" | ...
source = "rustxec_msr_2026" | "rustsec_2024_2026" | "manual_curation"
phase5_eligible = true | false              # opt-in for Miri witness gate (Ward-only axis)
```

The `bug_shape` field maps onto Ward's UOE shape catalog (Tier 1 + Tier
2 + Tier 3 / Phase 4 / 5), and is reported in the per-shape breakdown.
Per-shape numbers are descriptive; the headline metric is paired across
the full corpus, not per-shape.

## Tool selection and version pinning

### In scope

| Tool | Version pin | Why included | Notes |
|---|---|---|---|
| **Ward** | latest released (target: v0.X tagged at benchmark publication) | Subject of the claim. | Run with default `local-interactive` profile, `--scan-all`. Phase 5 witness gate machinery enabled but reported separately. |
| **CodeQL CLI** | `codeql-cli ≥ 2.18` with `codeql/rust-queries` ruleset pinned to a tagged release (track repo: `github/codeql`). | The most credible publicly-available Rust security analyzer. Microsoft-backed, used in GitHub Advanced Security. | Use **CLI**, not the hosted action — see fairness rationale. Use `rust-security-extended.qls` suite. |
| **Semgrep** | `semgrep ≥ 1.95` (community + `r/rust-security` ruleset, snapshot pinned by digest). | Widely deployed; the OSS community baseline. Rust support is younger but growing. | Run with `--config=p/rust-security` plus the `r/rust-security` community pack. |
| **Rudra** | latest tag (HEAD as of 2024-09; project is dormant). Document toolchain pin (`rust-toolchain` file). | The only academic Rust-specific unsoundness scanner. **Best-effort inclusion** — if Rudra fails to build with a toolchain it accepts, document the failure modes per repo and treat as N/A for that entry. | Likely runnable on ~30–60% of corpus; report coverage. |
| **cargo-geiger** | latest released. | **NOT a security tool** — included as an *unsafe-density baseline* so reviewers can sanity-check whether high-detection-rate tools are simply firing on every `unsafe` block. | Not a competitor; reported as a context column, not a head-to-head row. |

### Out of scope (with rationale)

- **CodeQL hosted (GitHub Advanced Security)**: requires Internet, results
  vary by entitlements, not reproducible offline. CLI is functionally
  equivalent for the queries we run.
- **Proprietary scanners** (Veracode, Snyk Code, Sonatype, Coverity,
  CodeSonar, etc.): not publicly auditable; we cannot pin versions or
  share the corpus with them under permissive license.
- **cargo-audit**: detects *known advisories by package version*, not
  *vulnerable code by shape*. Different lane. A trivial corpus where
  every entry's `Cargo.lock` references the affected version would give
  cargo-audit ~100% recall and tell us nothing about code-level
  detection. Excluded.
- **Cargo-deny / cargo-vet**: same lane as cargo-audit. Excluded.
- **Clippy**: non-security lints. Use cargo-geiger as the unsafe-density
  baseline instead — clippy's `correctness` group has too many false
  positives at scan time to be a fair baseline.
- **rust-analyzer / cargo-check / miri-by-itself**: not security
  scanners. (Miri appears only in Ward's witness gate.)
- **LLM-only scanners** (Claude/GPT prompted with a CVE-detection
  template): non-deterministic, expensive, version-drifting, and
  Ward already integrates an LLM tier internally — including a
  bare-LLM lane would be benchmarking our own infrastructure twice.
  Excluded.

### Pin enforcement

All tool binaries are reproducible-built or pinned by SHA in a single
Dockerfile (target: `Dockerfile.bench`) committed to the benchmark repo.
The Dockerfile produces a single image that contains every tool at the
locked version; the harness invokes them via `docker run --network=none`
to enforce the offline scan invariant (see [fairness
controls](#fairness-controls)). A nix flake is acceptable as an
alternative to Docker; pick one and ship it.

Tool ruleset SHAs are locked in `bench/tool-versions.toml` and verified
at harness startup against the deployed image.

## Fairness controls

### Time budget

**10 minutes hard cap per repo per tool.** Implemented via
`systemd-run --uid=N --slice=bench.slice --property=RuntimeMaxSec=600`
(or an equivalent per-OS isolation primitive). On timeout, the tool's
findings for that repo are recorded as `null` and the entry is reported
as **timeout** rather than counted as TP/FP/TN/FN. Timeouts are
reported separately in the latency table; they do not silently
contribute zero findings to the headline.

Rationale: 10 minutes is generous for typical Rust crates (median size
~5K LOC), but covers the long tail (e.g., `wasmtime`, ~150K LOC, where
CodeQL database build alone can take 4–5 min). Anything above 10 min on
a single tool indicates a real performance issue worth surfacing on the
latency axis rather than burying in headline aggregation.

### Compute budget

- **CPU**: 4 dedicated cores per tool (`taskset -c 0-3`). All tools get
  identical core count.
- **Memory**: 16 GiB hard cap per scan invocation
  (`systemd-run --property=MemoryMax=16G`). On OOM, behave as for
  timeout: record `null`, report separately, do not count.
- **Disk**: each tool runs in its own scratch directory; the directory
  is cleared between repos. Tool caches (e.g., CodeQL database cache)
  persist within a single benchmark run but are wiped between runs.

The 16 GiB ceiling is a deliberate forcing function: real-world CI
reviewers cannot allocate 64 GiB to a security scanner. If a tool
cannot fit in 16 GiB on a 50K-LOC crate, that's a defect worth
reporting.

### Network isolation

`--network=none` (Docker) or a `systemd-run` slice with
`PrivateNetwork=yes`. No tool may make any DNS or TCP request during a
scan. Tool databases (CodeQL `codeql/rust-queries`) and rulesets
(Semgrep `p/rust-security`) are pre-fetched into the image at build
time; the running container has no Internet.

This rules out any "cloud assist" feature and standardizes the
information available to each tool. It also rules out CodeQL's
optional GitHub-hosted query suite; we use the offline CLI ruleset
exclusively.

### Cache state

Repository sources are pre-cloned to a benchmark cache
(`bench/cache/repos/<repo>/.git`). Each scan starts from a fresh
`git archive` extraction (no `.git` directory inside the scan root).
Ward's per-repo target/ directory is wiped before each scan; CodeQL's
database directory is wiped between repos; Semgrep is stateless.

Identical, pre-warmed tool indices are loaded *into the image* at build
time so first-scan vs. nth-scan latency does not skew per-tool numbers.

### Determinism

Each tool is invoked with a fixed RNG seed where supported
(Semgrep: `--max-target-bytes` and rule order; CodeQL: deterministic by
construction; Ward: deterministic by construction; Rudra:
deterministic by construction). Three independent runs on the same
input must produce byte-identical SARIF output. We verify this at
harness startup on a 5-entry smoke set; if a tool fails determinism we
file a bug and record the run as best-of-three.

## Scoring rules

The benchmark uses Ward's existing **paired** scoring methodology, the
same one used in `crates/ward-eval/src/repo_eval.rs` for the headline
internal numbers. This ensures the public benchmark numbers reconcile
to internal runs and that competitors are not evaluated under a more
favourable scoring lens than Ward itself.

### Paired vs unpaired classification (the headline distinction)

- **Paired (headline)**: each CVE contributes a `(vuln_commit,
  fix_commit)` pair. A finding on the vuln commit at the affected file
  that does **not** persist on the fix commit at that file is a TP.
  A finding that persists across both is reclassified from FP to TN
  (it's a pre-existing finding unrelated to the CVE; see
  `crates/ward-eval/src/finding_identity.rs`). A finding on the fix
  commit but not the vuln commit is reclassified from FP to **noise**
  and excluded from the headline (it's a regression introduced by the
  fix, not relevant to the CVE under test).

- **Unpaired (raw classifications)**: report alongside the paired
  numbers for transparency. These are stricter against all tools;
  paired scoring is the *fair* metric because it excludes pre-existing
  noise from being held against any tool.

We report both. The headline claim is paired; unpaired numbers are in
the appendix. This mirrors the internal eval format
(`notes/silent-gating-bug-fix-2026-05-01-eval-baseline.md`).

### Diff-aware FP reclassification

A finding `F` on the vuln commit at file `f` line `L` is reclassified
from FP to TN iff: (a) `F` also appears on the fix commit at the same
file `f` (line ±2) and (b) the diff between vuln and fix does not
modify the relevant lines. The ±2 line tolerance is taken from
`finding_identity.rs`'s persistence matcher and is identical for all
tools.

### Line-level vs file-level matching

**File-level for TP/FP attribution; line-level for persistence
matching.** Rationale:

- Tools differ in their line-precision: Semgrep reports the precise
  source line of the regex match; CodeQL reports the line of the sink
  call; Ward reports the line of the obligation residual. Comparing
  *exact lines* across tools is unfair.
- *File-level* matching against `affected_file` says "this tool flagged
  the right file as suspicious", which is what a reviewer cares about.
- *Line-level* matching is used only for persistence (does this finding
  re-appear at the same place after the fix?), where the comparison is
  intra-tool and the line precision is consistent.

This compromise gives all tools a fair shake at TP attribution while
keeping persistence reclassification rigorous.

### What counts as a "finding" per tool

To prevent severity-noise from inflating any tool's FP count:

- **Ward**: `confidence ≥ Medium`. Lower-confidence findings are not
  user-facing in `ward review`'s default profile and shouldn't enter
  the benchmark headline.
- **CodeQL**: `severity ≥ warning` (excludes `note`). The
  `rust-security-extended.qls` suite already filters to security-
  relevant rules; this is consistent with what GitHub Advanced
  Security surfaces.
- **Semgrep**: `severity ≥ WARNING`. Excludes `INFO` and `INVENTORY`
  findings.
- **Rudra**: all findings count (Rudra has no severity tier).
- **cargo-geiger**: not scored (context column only).

This is a normalization step; we document it and justify each filter
threshold by reference to what the tool's default user-facing UX
surfaces.

### Vuln-class → rule-id mapping

Ward's eval already does this via `vuln_class_matches_rule` in
`crates/ward-eval/src/repo_eval.rs` (lines 73 onward, with the
unsafe-class arm at line 747). The mapping is publicly visible and we
use it for **all** tools, not just Ward — i.e., a Semgrep finding's
`rule_id` is matched against the same keyword list (`rust-unsafe`,
`from-raw-parts`, `transmute`, `int-overflow`, etc.) before counting
as a TP.

For competitor tools that don't emit Ward-shaped rule IDs, we extend
the keyword list per-tool. Concretely:

- CodeQL Rust unsafe queries emit IDs like `rust/uninitialized-memory`,
  `rust/unsafe-deref`, `rust/incorrect-pointer-arith`. Add these
  keywords to the vuln-class arm.
- Semgrep `r/rust-security` rules emit IDs like
  `rust.lang.security.unsafe-block`,
  `rust.lang.correctness.transmute-pod-to-non-pod`. Add these
  keywords.
- Rudra emits `RUDRA-{LIFETIME,PANIC-SAFETY,SEND-SYNC}` IDs. Add as
  arms of the existing `send_sync` / `panic_sequence` / `trait_law`
  classes.

The full extended mapping is committed as `bench/rule-id-mapping.toml`
alongside the corpus.

## Witness rate as Ward-only axis

### What Miri witnesses are

Phase 5 of the UOE adds a Miri-witness loop: when Ward emits a
high-or-medium-confidence Rust unsafe finding on a `phase5_eligible`
entry, the eval rig launches Miri (`cargo +nightly miri run` against
the entry's witness fixture) to attempt to **reproduce the UB**. The
witness is a small executable that calls into the affected code path
with adversarial inputs.

Three outcomes per witness invocation:

- **Positive** — Miri detected UB matching the predicted shape.
  Confidence is promoted (medium → high). This is *runtime-grounded
  evidence* that the static finding is real.
- **Negative** — Miri ran the witness to completion with no UB. The
  finding is demoted (high → medium → low → suppressed depending on
  policy). The static analyzer was wrong, or the witness didn't
  exercise the right path.
- **Skip** — witness fixture failed to build, or Miri crashed, or the
  entry isn't `phase5_eligible`. No confidence movement.

Implementation: `crates/ward-eval/src/phase5_witness_gate.rs`. The
gate currently passes 24/24 = 100% positive-witness rate on the
runnable subset (24 of the 32 RustXec entries currently have a
runnable witness fixture; the remaining 8 are skips for build
reasons that bn-3ipwh and bn-1495l are working through).

### Why we report it separately

No competitor has equivalent machinery. CodeQL, Semgrep, Rudra all
operate purely statically. Including witness rate in the head-to-head
MCC would penalize them on an axis they don't compete on.

### How we report it

A separate **Ward-additional-evidence** section of the writeup:

- Phase-5-eligible entries scanned: N
- Phase-5-eligible entries with at least one Ward finding: M
- Of those M, runnable Miri fixtures: M' (M' ≤ M)
- Positive witness rate: positive / M'
- Negative witness rate: negative / M'
- Skip rate: (M − M') / M

We explicitly state: *witness rate is Ward-only; do not interpret it as
a head-to-head metric. It is an integrity signal — Ward is making
predictions Miri can verify at runtime.*

### Why witness rate is interesting at all

A high positive-witness rate means Ward's static obligation residuals
correspond to *actual UB at runtime*, not just to suspicious
syntactic shapes. This is the cleanest possible answer to "is the
static analyzer crying wolf?" — Miri runs the code, observes UB,
agrees with Ward. If a competitor tool ever ships a Miri-witness loop,
this axis becomes head-to-head and we'll add it.

## Statistical reporting

### Headline numbers with confidence intervals

Every paired metric (precision, recall, F1, MCC) is reported with a
**bootstrap 95% CI** computed from 1000 resamples over the corpus
(stratified by `vuln_class`). We use the percentile method.

Concretely: for each tool, we resample the corpus with replacement
1000 times, recompute precision / recall / F1 / MCC on each resample,
and report the 2.5th and 97.5th percentiles as the CI bounds.

Headline format example (Ward vs CodeQL on a hypothetical N=80 corpus):

| Tool | Precision (95% CI) | Recall (95% CI) | F1 (95% CI) | MCC (95% CI) |
|---|---|---|---|---|
| Ward | 0.78 [0.71, 0.84] | 0.81 [0.74, 0.87] | 0.80 [0.75, 0.84] | +0.51 [+0.41, +0.60] |
| CodeQL | 0.85 [0.72, 0.95] | 0.20 [0.13, 0.28] | 0.32 [0.22, 0.42] | +0.20 [+0.10, +0.31] |

CIs are required so readers can see when a precision number is high
but driven by a tiny TP count (CodeQL's 98.8% precision in
`notes/silent-gating-bug-fix-2026-05-01-eval-baseline.md` rests on
just 251 TPs out of 1726 paired scorable cases — its CI on a smaller
benchmark corpus will be very wide).

### Pairwise tool comparisons

For headline claims of the form "Ward beats X" we run **McNemar's
test** for paired classification differences across the per-entry
binary outcomes (correct / incorrect on each entry). McNemar's exact
form (binomial, not chi-squared approximation) is appropriate when N
is small and the off-diagonal counts can be sparse.

We do **not** claim "Ward beats X" if either: (a) the McNemar p-value
is > 0.01, OR (b) the 95% CIs on F1 or MCC overlap.

If both tests fail (p > 0.01 AND CIs overlap), we report the numerical
delta but explicitly state the comparison is not statistically
distinguishable on this corpus.

### Per-class subgroup analysis

Per-vuln-class breakdown (memory_safety, use_after_free,
type_confusion, undefined_behavior, data_race, soundness) is reported
**without** statistical tests because per-class N is small (~10–25
entries). We mark per-class numbers as **descriptive only** — they
inform reviewers about where each tool is strong, but per-class
claims must be backed by at least 30 entries before we apply
significance testing.

Per-shape breakdown (safe-encap, slice-from-raw-parts, transmute-
validity, int-overflow, layout-cast, panic-sequence, ffi-boundary-
contract, etc.) gets the same descriptive-only treatment.

## Latency and resource axis

For each tool × repo combination we report:

- **Wall time** (seconds, p50 / p95 / p99 across the corpus).
- **CPU time** (seconds; user + system).
- **RAM peak** (MiB, via `/usr/bin/time -v`).
- **Disk write peak** (MiB, via `iotop` or `cgroup` accounting).
- **Timeouts** (count, list of repos).
- **OOMs** (count, list of repos).

Reported per-tool aggregate **and** per-language-class — but since the
benchmark is Rust-only, the per-language axis collapses; we report
per-vuln-class instead, since some classes (e.g., wasmtime / cranelift
for type_confusion) skew large.

Why latency matters for a security benchmark: a tool with 99% recall
that takes 2 hours per repo is unusable in CI. We do not score on
latency in the headline MCC, but we report it prominently so a
reviewer can make their own latency / accuracy tradeoff.

## Reproduction requirements

### One-command repro

From a fresh clone:

```bash
git clone https://github.com/ward/unsafe-rust-bench.git
cd unsafe-rust-bench
./bench/run.sh
```

`run.sh` must:

1. Build the pinned Docker image (or nix flake) from
   `Dockerfile.bench`.
2. Pre-fetch the corpus repos to `bench/cache/repos/`. Each clone is
   pinned to the exact `vulnerable_commit` or `fixing_commit` SHA;
   missing SHAs are fetched once with `git fetch <sha>`. After this
   step, network access is no longer needed.
3. Run all tools across all corpus entries with the locked time /
   memory / network controls.
4. Compute paired scores, bootstrap CIs, McNemar tests.
5. Emit `results/headline.json`, `results/per-tool.json`,
   `results/per-class.json`, `results/latency.json`, and a single
   `results/report.md`.

End-to-end target: completes in **< 6 hours on a 16-core / 64 GiB
host** (parallelism: 4 tools × 4 cores each = 16 cores; corpus chunks
process in serial within each tool to honour the per-scan core
budget).

### Checksums

The benchmark publishes:

- `bench/corpus.toml` — manifest with all corpus entries (SHA-pinned).
- `bench/corpus.toml.sha256` — checksum of the manifest.
- `bench/tool-versions.toml` — tool name + version + ruleset SHA.
- `bench/tool-versions.toml.sha256` — checksum of tool versions.
- `bench/Dockerfile.bench` — image definition.
- `bench/Dockerfile.bench.sha256` — image content checksum (post-build,
  via `docker save | sha256sum`).

A reviewer who reproduces the benchmark should land within ±2pp of the
published headline (per-class numbers may vary more due to small N).
We commit the published image to a public registry
(`ghcr.io/ward/unsafe-rust-bench`) so reviewers don't have to rebuild.

### License

- **Corpus manifest** (TOML, metadata only): CC-BY-4.0.
- **Harness code** (`bench/run.sh`, scoring scripts): Apache-2.0.
- **Source repos** (transitive, fetched into cache): each repo retains
  its own license. The benchmark documentation includes a per-repo
  license table.

A user redistributing the corpus must redistribute the manifest; the
source repos themselves are fetched at runtime from upstream and not
redistributed by us. This pattern matches RUSTSEC's own redistribution
posture.

### Reviewer expectations

A third-party reviewer should be able to:

1. Reproduce headline numbers ±2pp from a fresh clone.
2. Inspect every entry's classification and trace it to a specific
   tool finding (or absence thereof) in the SARIF dump.
3. Modify `corpus.toml` to add new entries and re-run, observing how
   each tool's numbers move.
4. Swap out a tool version (e.g., upgrade CodeQL ruleset) and observe
   the delta — version drift is auditable.

## Out of scope

Explicitly out of scope:

- **Non-Rust corpus**. This benchmark is Rust-only. Ward's other
  language scanners are in scope of separate benchmarks.
- **Supply-chain advisory matching** (cargo-audit's lane). The
  benchmark scores code-level shape detection, not version-list
  matching.
- **Proprietary tools** (Veracode, Snyk, Coverity, etc.). We cannot
  ship a reproducible benchmark that requires a paid license or a
  vendor key.
- **proc-macro-only vulnerabilities**. All tools struggle here; the
  comparison would be noisy without information value. Listed to
  acknowledge the limitation.
- **Cloud-API tools** (CodeQL hosted). Use the CLI for offline
  reproducibility; results are functionally equivalent for our query
  set.
- **LLM-only scanners** prompted with a CVE-detection template. Ward
  has its own LLM tier; we don't benchmark our own infra twice.
- **Build-time / link-time vulnerabilities** that require running
  build scripts that fetch external resources. Excluded by the
  network-isolation invariant.
- **Detection of vulnerabilities introduced *after* the benchmark
  publication**. The benchmark is a frozen snapshot; future advisories
  prompt a v2 release.
- **Auto-fix quality**. Sibling track bn-35b00 covers rust-autofix; this
  benchmark scores detection only.

## Threats to validity

### Corpus selection bias

**Largest threat.** Ward's UOE was developed iteratively against a
corpus that overlaps with RUSTSEC. Authors (us) have read many of the
RUSTSEC advisories, written rules to catch them, and shipped them.
Even with the 40% augment-with-novel-entries policy, residual bias
remains.

**Mitigations**:

- Corpus subset+augment policy (≥40% novel entries from 2024–2026
  RUSTSEC entries unseen by Ward authors during rule development).
- Per-entry `source` provenance metadata so a reviewer can replay the
  benchmark on the novel-only subset and check that Ward's lead
  persists.
- A separate **held-out validation** corpus of 20+ entries collected
  *after* methodology lock that no Ward author touches until the
  benchmark publishes. **Deferred to a follow-up pass** (see
  [Resolutions log](#resolutions-log) item 4). The current headline
  does *not* incorporate held-out numbers; they will be reported in
  a future pass and treated as the canonical bias signal at that time.

**Disclosure**: we explicitly document this in the writeup. "Ward was
developed against a partially overlapping corpus" is a stronger
honest claim than pretending it wasn't.

### Tool version drift

Tools update their rulesets weekly. A benchmark frozen in May 2026
will be stale by August. Mitigation: lock tool versions by SHA in
`bench/tool-versions.toml`, document the lock date in the writeup,
and re-run quarterly. Reviewers may run a "latest" variant and
compare against the locked variant; the delta is itself useful data.

### Miri verdict reproducibility

Miri runs are mostly deterministic but some are flaky on:

- TLS / RNG-dependent code paths.
- Concurrency primitives where the scheduler interleaving matters.
- FFI calls (Miri has limited FFI shimming).

**Mitigation**: every Miri verdict in the witness gate is run 3 times;
the verdict is the modal outcome (positive if 2/3+ agree on positive,
negative if 2/3+ agree on negative, otherwise skip). Witness fixtures
that flake more than 1/3 of the time across 9 runs are removed from the
witness-eligible set and reported separately.

### Survivor bias

We can only benchmark vulns that were *publicly disclosed*. Closed-
source vulns and silently-patched bugs are invisible. Mitigation:
none — this is a fundamental limit of public CVE benchmarks. Disclose
prominently.

### Per-class N is small

Per-vuln-class breakdowns at N≈10–25 are descriptive, not inferential.
Mitigation: report numbers but mark them descriptive-only; do not
make per-class statistical claims unless N≥30.

### Tool-cache warmth asymmetry

CodeQL benefits enormously from a warm database cache (database
build is 60–80% of total time). If we wipe caches between repos, we
penalize CodeQL's CI-realistic posture. **Decision**: pre-warm caches
at image build time for tools that support it (CodeQL Rust extractor
is pre-installed), but wipe per-repo intermediate state. This
matches what GitHub Advanced Security does in practice: extractor is
installed once, database is built per-repo.

### Definition of "best-in-class"

We define it as: **highest paired F1, with non-overlapping 95% CIs
against all other tools, on the unsafe-class subset of the corpus,
with offline reproducibility**. This is a specific operational
definition; alternative definitions ("best on memory-safety only",
"highest precision regardless of recall", "fastest scanner with
recall ≥ X%") would produce different rankings. We commit to the F1
definition because it's the standard composite score and it weights
both axes equally.

### Adversarial corpus construction

A skeptical reader may suspect we cherry-picked entries that favor
Ward. Mitigations: (a) corpus inclusion rules in this document are
locked *before* corpus collection begins, (b) the augment subset is
collected by an agent following the inclusion rules without seeing
Ward's per-entry classification, (c) we publish the full inclusion-
rule application log so a reviewer can audit which candidates were
rejected and why.

## Resolutions log

This document was locked before corpus collection. The items below
were flagged as open at lock time and have since been resolved (or,
where noted, explicitly deferred). Each entry records the decision
and the dispositive evidence so reviewers can audit the state at
headline time.

1. **Final corpus size** — **Resolved 2026-05-12 (bn-2tdyf)**: 80
   paired pairs / 160 entries. RUSTSEC unsafe-class advisory yield
   supported the locked 80-pair size without dropping inclusion-rule
   strictness.
2. **Ward version pin** — **Resolved 2026-05-13**: Ward HEAD at
   2026-05-13, materialized as image digest
   `sha256:b7707fe926c96be99348030445cb355141f43afae2243d86a8f7862cc134308e`
   pinned in `bench/tool-versions.toml`. The Ward source release that
   this digest corresponds to is pending — until then, the image is
   the canonical version pin.
3. **Rudra inclusion** — **Resolved 2026-05-13**: included best-effort
   per §4. Coverage on this corpus is 3.75% (6/160 runnable), which is
   below the §10 30% threshold. Rudra is therefore reported as "did
   not run" for the competitive head-to-head claim, with its coverage
   and the 1 paired TP recovered in the max-breadth aux run preserved
   for transparency.
4. **Held-out validation corpus** — **Deferred**. The current pass
   does **not** deliver a separate held-out corpus, and the headline
   does **not** incorporate any held-out numbers. A follow-up bone
   will collect a sealed held-out set (target 20 entries, agent-driven
   novel collection under a fresh memory snapshot per the
   recommendation below) and re-run the head-to-head against it.
   Held-out numbers will be reported in a future pass.
5. **Held-out collection process** — **Deferred** (paired with the
   item above). Recommendation stands: a single agent run under a
   fresh memory snapshot that has not seen the main corpus or Ward's
   rule sources, with the held-out manifest sealed until publication.
6. **Publication venue** — **Resolved 2026-05-13**: blog post +
   benchmark repo (this site + `github.com/bobisme/ward-releases`).
   arXiv submission is not committed and can follow if useful.
7. **CI wiring** — **Deferred**: not committed yet; revisit
   post-public-release once the Ward source tree is published and
   the benchmark harness can be wired into a public CI pipeline.

## Amendment log

Changes to this methodology since lock are recorded here. Each entry
records the date, the change, the rationale, and the downstream impact.

- **2026-05-12 — Semgrep ruleset substitution (bn-tlxo4)**: locked
  ruleset specified `p/rust-security` in an early draft of §3; the
  actual locked-bench config uses `p/rust ∪ r/rust.lang.security`
  (the community packs that exist under those names at lock time).
  The substitution does not change which Rust rules are loaded —
  `p/rust-security` was the older pack name and resolves to the same
  shipped content as `p/rust` in Semgrep's current registry. Tracked
  for transparency rather than impact.
- **2026-05-13 — Rudra rule-id mapping fix (bn-bums5)**: extended
  `bench/rule-id-mapping.toml`'s Rudra arm from the methodology-spec
  dash-separated names (`RUDRA-SEND-SYNC`, etc) to the no-dash
  CamelCase form Rudra actually emits (`SendSyncVariance`,
  `UnsafeDataflow`, `PanicSafety`). This is a strict refinement of
  §5's vuln-class → rule-id keyword mapping; identical numerical
  impact on headline (Rudra still 0 paired TPs in the locked run; +1
  in the max-breadth aux once the parser is also fixed).

## References

- `notes/silent-gating-bug-fix-2026-05-01-eval-baseline.md` —
  canonical Phase 0 walkaway-gate baseline (paired headline numbers).
- `notes/post-phase-2-eval-2026-05-02.md` — most recent post-phase
  eval with per-rule and per-shape breakdown.
- `notes/eval-competitor-2026-03-22.md` — historical multi-language
  competitor eval (precedent for the head-to-head format).
- `notes/codeql-baseline-runner-2026-05-01.md` — CodeQL Rust runner
  details; informs the partition methodology.
- `notes/clippy-baseline-runner-2026-05-01.md` — Clippy runner
  details (Clippy is excluded from this benchmark; see
  out-of-scope).
- `notes/rustxec-import-2026-05-01.md` — RustXec MSR'26 corpus
  import provenance; informs the inherit-vs-rebuild decision.
- `crates/ward-eval/src/repo_eval.rs` — paired scoring logic and
  `vuln_class_matches_rule`; the fairness primitive other tools must
  match.
- `crates/ward-eval/src/finding_identity.rs` — persistence-matching
  logic for diff-aware FP reclassification.
- `crates/ward-eval/src/phase5_witness_gate.rs` — Miri-witness gate
  implementation; informs the witness-rate axis description.
- `tests/cve-registry/manifest.toml` — Ward's existing CVE manifest;
  source for the inherited subset of the benchmark corpus.

## Methodology lock

This document is the locked specification for downstream bones:

- **Corpus collection** (downstream bone): operates from
  [corpus selection criteria](#corpus-selection-criteria). Cannot
  unilaterally change inclusion / exclusion rules.
- **Per-tool runners** (downstream bone): implements
  [tool selection and version pinning](#tool-selection-and-version-pinning)
  and [fairness controls](#fairness-controls). Cannot adjust time /
  memory / network controls without amending this document.
- **Head-to-head measurement** (downstream bone): implements
  [scoring rules](#scoring-rules) and
  [statistical reporting](#statistical-reporting). Cannot change
  scoring methodology without amending this document.
- **Public writeup** (downstream bone): consumes results and renders
  the human-readable report; must include all sections of
  [threats to validity](#threats-to-validity) and the open-questions
  resolution log.

Amendments to this document require an issue against bn-1ti5m
documenting the change rationale and updated downstream impact.
