# Reproducing the unsafe-Rust head-to-head benchmark

> **Source release pending**: this reproduction kit references `ward-eval`
> and `ward-cli` binaries built from the Ward repo, which is currently
> private as Ward is under heavy development. The bench infrastructure
> (Dockerfile, tool pins, rule mappings, corpus, methodology) is public
> NOW so the methodology can be reviewed. When the Ward source is
> released, this REPRODUCE.md will be runnable end-to-end. Until then,
> the headline numbers stand by their own audit trail (`provenance/`,
> methodology lock, image digest, McNemar + bootstrap CIs).

This document is the mechanics-focused companion to the public
writeup at
[`docs/blog/unsafe-rust-benchmark.md`](../../../../docs/blog/unsafe-rust-benchmark.md).
It tells an external reviewer exactly what to install and what to run
to regenerate the published headline within ±2 percentage points.

The numbers under reproduction:

- Ward: TP=39, FP=0, TN=77, FN=41 over 80 paired pairs.
- Precision = 1.000 [1.000, 1.000].
- Recall = 0.487 [0.388, 0.600].
- F1 = 0.655 [0.559, 0.750].
- MCC = +0.564 [+0.484, +0.651].
- Every other competing tool: 0 TPs at ≥ WARNING severity.
- McNemar p ≈ 1.46 × 10⁻¹¹ for every (Ward, competitor) pairing.

The locked methodology spec is
[`notes/benchmarks/unsafe-rust-bench-methodology.md`](../../../../notes/benchmarks/unsafe-rust-bench-methodology.md);
the headline results doc is
[`notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md`](../../../../notes/benchmarks/unsafe-rust-bench-results-2026-05-13.md);
the max-breadth aux is
[`notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](../../../../notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md).

## Prerequisites

- **podman ≥ 5.0** (preferred — rootless, no daemon). Docker also
  works: pass `--runtime docker` to `ward-eval bench-run`. The image
  format is OCI-standard, so `podman build` and `docker build`
  produce interchangeable images.
- **~80 GB free disk**. The bench image is ~1.5 GiB; per-entry
  CodeQL DBs can run 500 MB – 4 GB each; clone caches for 65 upstream
  repos total another ~20 GB.
- **Rust stable** for building the harness (`cargo build --release`).
  The image bundles its own Rust toolchain — your host toolchain only
  needs to build `ward-eval` / `ward-cli` / `ward-stub-analyzer`.
- **Network access on first run** to pull the bench image base
  layers and (one-time) the corpus's upstream repositories. The
  scan-time containers themselves all run under `--network=none`.
- **`jq`** on the host (used by `bench/smoke-determinism.sh` and
  some aux scripts).

The bench image build will pull pinned versions of CodeQL bundle
v2.25.4, Semgrep 1.95.0, Rudra (HEAD on `master` at
`nightly-2021-10-21`), cargo-geiger 0.12.0 and bake them in. None of
those are runtime dependencies on the host.

## What you can reproduce now

The public materials in this repository let you independently verify
the **inputs and the materialization of the published outputs**:

```bash
# 1. Build the locked bench image from the public Dockerfile.bench
#    (one-time, ~20 min). The image bundles CodeQL 2.25.4 bundle,
#    Semgrep 1.95.0, Rudra (master @ nightly-2021-10-21), cargo-geiger
#    0.12.0 and the pinned rule snapshots.
podman build -t ward-bench:locked -f bench/Dockerfile.bench .

# 2. Verify the image digest matches the published headline.
#    Expected: sha256:b7707fe926c96be99348030445cb355141f43afae2243d86a8f7862cc134308e
podman image inspect ward-bench:locked --format '{{.Digest}}'

# 3. Verify the materialized CodeQL JSON against the raw artifact tree
#    by re-running the classification script on the committed raw
#    SARIF + DB directories under notes/benchmarks/artifacts/raw/codeql.
python3 scripts/synth-bench-results-codeql.py
diff <regen> notes/benchmarks/artifacts/bench-results-codeql-partial.json
```

You can also inspect every other input the headline depends on:
`manifest.toml`, `provenance/<id>.toml` for each entry,
`bench/tool-versions.toml`, `bench/rule-id-mapping.toml`,
`bench/rule-id-mapping-aux-max-breadth.toml`, the methodology spec, the
results doc, and the raw per-entry SARIF / stdout dumps under
`notes/benchmarks/artifacts/raw/`.

## Future source-release reproduction (pending)

End-to-end re-execution of the head-to-head sweep requires the Ward
harness binaries (`ward-eval`, `ward-cli`, `ward-stub-analyzer`), which
live in the private Ward repository while Ward is under heavy
development. The commands below will run as published once the source
is released; until then this section is the contract for what
reproduction will look like, not a runnable recipe today.

```bash
# Source release pending — these commands will run end-to-end once
# the Ward source tree is published.

# 3. Build the harness binaries.
cargo build --release -p ward-eval -p ward-cli -p ward-stub-analyzer

# 4. Full head-to-head sweep.
#    Wall-clock is dominated by CodeQL DB-create on large repos.
#    Expect ~6–10 hours total (Ward + Semgrep + Rudra + cargo-geiger
#    finish in ~60–90 min; CodeQL alone takes ~14h to complete the
#    full 160 entries, of which 53% time out at the 10-min cap — that
#    rate is itself a documented headline finding).
./target/release/ward-eval bench-run \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --tool-versions bench/tool-versions.toml \
  --rule-id-mapping bench/rule-id-mapping.toml \
  --tools ward,semgrep,rudra,cargo-geiger,codeql \
  --out target/bench/repro

# 5. Paired finding-identity reclassification.
./target/release/ward-eval bench-score \
  --raw target/bench/repro \
  --out target/bench/repro/paired

# 6. Bootstrap CIs + McNemar pairwise + per-class breakdown.
./target/release/ward-eval bench-stats \
  --raw target/bench/repro \
  --paired target/bench/repro/paired \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --out target/bench/repro/stats.json
```

If you want to split CodeQL into a separate (much longer) sweep so
the fast tools' results land first, run step 4 twice:

```bash
# Source release pending — see note above.

# 4a. Fast tools first (~60–90 min).
./target/release/ward-eval bench-run \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --tool-versions bench/tool-versions.toml \
  --rule-id-mapping bench/rule-id-mapping.toml \
  --tools ward,semgrep,rudra,cargo-geiger \
  --out target/bench/repro

# 4b. CodeQL alone (allow ~14h wall-clock).
./target/release/ward-eval bench-run \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --tool-versions bench/tool-versions.toml \
  --rule-id-mapping bench/rule-id-mapping.toml \
  --tools codeql \
  --out target/bench/repro
```

## Tolerance

Reviewers running against the pinned image digest and tool-versions
file should land within **±2 percentage points** of the published
Ward headline (P=1.000, R=0.487, F1=0.655, MCC=+0.564) on the
aggregate numbers.

**Per-class numbers may vary by more than ±2pp** due to small per-class
N (memory_safety N=55; soundness, use_after_free, type_confusion all
N ≤ 9). The methodology (§7) explicitly marks per-class numbers as
descriptive-only — they are not subject to significance testing.

**The competitor 0-TP result should reproduce exactly.** If any
competing tool produces a non-zero TP count on the locked rulesets,
that is a meaningful finding and should be reported. The aux
max-breadth doc covers the case where you try broader rulesets; even
under those, the headline 0-TP result is robust (Rudra promotes to 1
TP after the in-image parser fix; Semgrep and CodeQL stay at 0).

## Expected wall time

| Tool | Wall time (full 160 entries) | Notes |
|------|------------------------------|-------|
| Ward | ~50–80 min | Median 1.25s/entry; 14 entries hit the 600s cap on large repos (known bn-2q4pn dedup/exfiltration runaway). |
| Semgrep | ~10 min | Mean 3.0s/entry; no timeouts. |
| Rudra | ~3 min | 154/160 fail fast at toolchain layer; 6 entries take 0–1s each. |
| cargo-geiger | ~30 min | Mean 9.9s/entry; no timeouts. |
| CodeQL | ~14h (extrapolated) | 53% timeout rate at DB-create on big repos; 110/160 entries unreachable within the wall-clock budget we held to. The published headline ran CodeQL until 6h 36m wall-clock; `bench-results-codeql.json` was materialized from on-disk SARIF + DB artifacts using `scripts/synth-bench-results-codeql.py`. The classification rule is mechanical and pre-locked — see [CodeQL outcome classification rule](#codeql-outcome-classification-rule) below. |

Total end-to-end (combined run with CodeQL) is therefore
approximately **6–10 hours** if you cap CodeQL at the same wall-clock
the headline used, or up to ~16 hours if you let CodeQL run to
completion.

## Determinism

Every tool in this benchmark is supposed to be byte-identical across
runs. We verify this with a 3-run identity check on a 5-entry subset:

```bash
./bench/smoke-determinism.sh \
  --manifest tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml \
  --tools ward,codeql,semgrep,rudra,cargo-geiger
```

Exit 0 means every (entry, tool) pair was deterministic across 3
independent runs. Exit 1 means at least one (entry, tool) pair
produced different output across runs — per methodology §5, affected
tools must be reported best-of-three and the non-determinism
disclosed.

The smoke is parameterized by:

- Pinned image digest in `bench/tool-versions.toml::image_digest`
  (`sha256:b7707fe926c9…`). The harness rejects scans against an image
  whose digest doesn't match.
- Pinned tool versions in `bench/tool-versions.toml::[tools.*]`. The
  harness reads `/BENCH_VERSIONS.json` from the image at startup and
  asserts a match.
- Pinned bootstrap seed (`0x77617264_62656e63` = `"wardbenc"`) so
  per-pair CIs are byte-identical across runs.

## Auxiliary max-breadth reproducer

To regenerate the max-breadth aux pass — broader Semgrep packs,
broader CodeQL suite, Rudra parser fix applied locally — see the
detailed reproduction section in
[`notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md`](../../../../notes/benchmarks/unsafe-rust-bench-aux-max-breadth-2026-05-13.md).
The aux scripts live under
[`scripts/aux/`](../../../../scripts/aux/):

- `run-aux-semgrep.py` — main aux Semgrep runner (160 entries).
- `run-aux-semgrep-tail.py`, `run-aux-semgrep-tail2.py` — parallel
  workers on disjoint cpusets.
- `synth-semgrep-from-sarif.py` — merges per-entry SARIFs into
  `bench-results-semgrep-aux.json`.
- `run-aux-rudra.py` — Rudra with parser bug fixed locally.
- `run-aux-codeql.py` — re-analyzes existing CodeQL DBs against the
  broader `rust-security-and-quality.qls` suite.
- `audit-aux-firings.py` — emits the per-firing audit table in the
  aux doc.
- `merge-semgrep-results.py` — combines parallel-worker outputs.

The aux runner uses `bench/rule-id-mapping-aux-max-breadth.toml` —
parallel to the locked `bench/rule-id-mapping.toml`, not a
replacement.

## Where artifacts live after a run

```
target/bench/<run-name>/
├── bench-results-ward.json           # full Ward results
├── bench-results-semgrep.json
├── bench-results-codeql.json         # (may be materialized from raw/codeql/ when CodeQL is killed before all 160 entries finish — see CodeQL outcome classification rule below)
├── bench-results-rudra.json
├── bench-results-cargo-geiger.json
├── raw/
│   └── <tool>/<entry-id>/            # per-tool per-entry SARIF / stdout
├── paired/
│   ├── paired-summary.json           # per-tool paired aggregates
│   └── paired-detail-<tool>.json     # per-entry paired classification
└── stats.json                        # bootstrap CIs + McNemar + per-class + latency
```

### CodeQL outcome classification rule

CodeQL DB-create exceeds the 10-min per-entry cap on ~half of the
larger repos in this corpus (53% measured rate on the headline run).
Because the budget is part of the locked methodology, we cannot just
let CodeQL run longer; the resulting on-disk state per entry can be
one of three cases. `scripts/synth-bench-results-codeql.py` walks the
raw artifact tree and applies this **pre-locked, mechanical**
classification rule (lifted from the script's module docstring):

| On-disk state for entry `<id>` | Classification |
|---|---|
| `raw/codeql/<id>/results.sarif` present **and** parses cleanly | `success` — TP/FP/TN/FN per `(expected, detected)` from SARIF parse, exactly as for any other tool's SARIF output. |
| `raw/codeql/<id>/codeql-db/` present **but no SARIF** (timeout during the analyze step after DB-create completed) | `timed_out=true`, `detected=false`, `error="codeql_db_create_timed_out"`, `duration_secs=600.0` (the cap). Classification per `expected`: `tp→FN`, `tn→TN`. |
| Neither DB nor SARIF (sweep killed before this entry reached analysis) | `not_run`, `detected=false`, `error="not_run"`, `duration_secs=0.0`. Classification per `expected`: `tp→FN`, `tn→TN`. |

**The rule is not a judgment call.** Missing SARIF after timeout is
recorded as `timed_out` or `not_run`; it is **never** silently
collapsed to FN/TN as if CodeQL had returned a confident negative.
The script's source is the authoritative implementation; the
docstring at the top of `scripts/synth-bench-results-codeql.py`
re-states the rule alongside the SARIF parser logic.

**Audit trail for the headline run:**

- Raw per-entry SARIF and `codeql-db/` directories:
  `notes/benchmarks/artifacts/raw/codeql/<entry-id>/` for each of the
  50/160 entries CodeQL reached. Each directory is the unmodified
  on-disk output `codeql database analyze` left behind.
- Sweep timeout log: `notes/benchmarks/artifacts/codeql-timeout-log.txt`
  (one line per entry recording wall-clock at DB-create + analyze
  steps).
- Aggregator script: `scripts/synth-bench-results-codeql.py` (Python,
  no external state — given the raw tree above, regenerates
  `bench-results-codeql.json` byte-for-byte on the same Python
  version).
- Resulting JSON: `notes/benchmarks/artifacts/bench-results-codeql-partial.json`.

To audit the materialization: run the script on the raw tree, diff
the output against the committed JSON. If they disagree, the script
is wrong, not the headline.



Committed reference artifacts (so you can diff your reproduction
against the canonical run) live under
[`notes/benchmarks/artifacts/`](../../../../notes/benchmarks/artifacts/):

- `bench-results-codeql-partial.json` — partial CodeQL results
  materialized from the on-disk artifact tree per the CodeQL outcome
  classification rule above (50/160 entries: 25 SARIF + 25
  DB-timeout; 110 marked `not_run`).
- `bench-results-semgrep.json` — full Semgrep results.
- `bench-results-rudra.json` — full Rudra results (154 errored, 6
  ran).
- `bench-results-cargo-geiger.json` — full cargo-geiger results
  (context-only).
- `paired-summary-2026-05-13.json` — per-tool paired aggregates.
- `stats-2026-05-13.json` — full bench-stats output.

And under `notes/benchmarks/artifacts/aux/`:

- `bench-results-semgrep-aux.json`, `bench-results-rudra-aux.json`,
  `bench-results-codeql-aux.json`, `paired-summary-aux.json`,
  `stats-aux.json` — aux pass equivalents.

## Reproducing the corpus

The bench corpus (`manifest.toml` + 80 `provenance/<id>.md` files)
is committed to this directory. The collection pipeline is
auditable via [`inclusion-log.md`](./inclusion-log.md), which records
every accept/reject decision against the methodology §3 inclusion
rules.

To verify the manifest hasn't drifted from the published version:

```bash
sha256sum -c tests/cve-registry/benchmarks/unsafe-rust-bench/MANIFEST.sha256
```

To add a new entry, see the *How to add a new entry* section of
[`README.md`](./README.md). New entries require a `provenance/<id>.md`
file with the advisory link, commit hashes, license verification, and
methodology conformance checklist.

## License and redistribution

- **Corpus manifest** (`manifest.toml`, `provenance/*`, `README.md`,
  `inclusion-log.md`, `MANIFEST.sha256`, this file): **CC-BY-4.0**.
- **Bench harness code** (`crates/ward-eval/src/bench/`,
  `bench/Dockerfile.bench`, `bench/smoke-determinism.sh`,
  `scripts/synth-bench-results-codeql.py`, `scripts/aux/*`):
  **Apache-2.0**.
- **Source repositories** referenced by the corpus: each retains its
  own permissive license (Apache-2.0, MIT, MPL-2.0, Zlib per the
  README license-distribution table). We fetch source at scan time
  from the upstream repositories; we do not redistribute upstream
  source.

When citing the benchmark, reference:

- The methodology document at the locked SHA
  (`notes/benchmarks/unsafe-rust-bench-methodology.md`, committed
  2026-05-07 under bn-3cgmj).
- This corpus manifest at the SHA pinned by
  [`MANIFEST.sha256`](./MANIFEST.sha256).
- The benchmark version tag `bench/unsafe-rust-v1` (minted by the
  operator after the bench artifact lands on `default`).

## If your reproduction misses tolerance

If the harness completes but your numbers diverge by more than ±2pp
on aggregate F1 / MCC / precision / recall:

1. **Verify the image digest.** `podman image inspect ward-bench:locked
   --format '{{.Digest}}'` should match
   `sha256:b7707fe926c96be99348030445cb355141f43afae2243d86a8f7862cc134308e`.
   If it doesn't, you're running a different image — the bench harness
   would normally refuse to start; if it didn't, your tool-versions
   pin is out of sync.
2. **Verify the tool versions inside the image.** Inside the container,
   `cat /BENCH_VERSIONS.json` should report CodeQL 2.25.4, Semgrep
   1.95.0, cargo-geiger 0.12.0, Rust stable 1.88.0.
3. **Verify the corpus.** `sha256sum -c MANIFEST.sha256` should pass.
4. **Check the determinism smoke.** Run
   `./bench/smoke-determinism.sh` first to confirm your environment
   is producing byte-identical SARIFs across runs.
5. **Confirm fairness controls.** The harness should be using
   `podman run --network=none --memory=16g --cpus=4 --cpuset-cpus=0-3
   --stop-signal=SIGKILL --stop-timeout=600` for every scan.
6. **Compare your `stats.json` line-by-line** against
   `notes/benchmarks/artifacts/stats-2026-05-13.json`. Differences
   in the `latency` section are expected (wall-clock varies with host
   load); differences in `tp/fp/tn/fn` indicate a methodology
   divergence somewhere.

If steps 1–5 pass and you still see a divergence in the headline
numbers, file an issue against the parent bone `bn-1ti5m` with your
`stats.json` attached.

## Open issues we know about

- **bn-2q4pn**: 14 Ward entries hit the 600s cap on large repos due
  to an internal dedup/exfiltration heuristic runaway. They count as
  errored (and therefore FN on the vuln side) in the published
  numbers. Fixing this is a Ward-side cleanup; it will likely improve
  Ward's recall on next quarterly re-run.
- **bn-1t4si** (filed, not yet landed): the in-image Rudra stdout
  parser misattributes the diagnostic message text to the file field.
  The aux pass shows that fixing this bug adds 1 paired TP for Rudra;
  the locked headline reflects the parser-broken state.
- **Witness gate (Phase 5) wiring into the bench harness**: still a
  Ward-only sidecar, not wired into the head-to-head numbers
  (methodology §6). A follow-up bone will wire it.

These are the known limitations. Anything else surfacing during your
reproduction is a meaningful finding — please report it.
