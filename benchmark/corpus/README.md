# Unsafe-Rust head-to-head benchmark — corpus

Auditable corpus snapshot for the Rust unsafe-class vulnerability
detection head-to-head between Ward and publicly-available competitor
tools.

**Auditable, not yet fully reproducible.** The manifest, per-entry
provenance log, inclusion criteria, and methodology lock are committed
here for external review. The sourcing pipeline that selected the 80
advisories runs against a private cache under `target/bench-cache/` and
is not itself committed — the committed truth of the corpus is what
appears in `manifest.toml` + `provenance/`, not the generator that
produced them. Independent re-derivation of the same 80 pairs from raw
RUSTSEC + MSR'26 inputs is pending Ward source release and a snapshot
of the bench-cache.

> **Methodology lock**: this corpus conforms to the spec in
> [`notes/benchmarks/unsafe-rust-bench-methodology.md`](../../../../notes/benchmarks/unsafe-rust-bench-methodology.md)
> (committed to main 2026-05-07 under bn-3cgmj). The methodology is locked
> *before* corpus collection so authors cannot bias the corpus toward their
> own tool. Amendments require an issue against bn-1ti5m.

## Corpus statistics

- **Total paired entries**: 80 (vuln + fix = 160 manifest rows)
- **Languages**: Rust only
- **Date range** of advisories: 2018 → 2026
- **Unique upstream repositories**: 65

### Per `source`

| Source | Count | Description |
|---|---|---|
| `rustxec_msr_2026` | 30 | Paired subset from RustXec MSR'26 academic memory-safety dataset |
| `manual_curation` | 18 | Ward's curated subset gated by RUSTSEC manually-curated memory-safety category |
| `rustsec_2024_2026` | 32 | Novel augmentation: 2024-2026 RUSTSEC entries not previously used by Ward authors |

**Novel ratio**: 32 / 80 = **40.0%** 
(methodology §3 requires ≥40% to dilute author bias).

### Per `vuln_class`

| vuln_class | Count |
|---|---|
| `memory_safety` | 56 |
| `soundness` | 9 |
| `use_after_free` | 8 |
| `type_confusion` | 7 |

### Per `bug_shape`

| bug_shape | Count |
|---|---|
| `safe-encap` | 22 |
| `panic-sequence` | 12 |
| `set-len-init` | 9 |
| `impl-send-sync` | 9 |
| `ffi-boundary-contract` | 5 |
| `layout-cast` | 4 |
| `int-overflow-safety` | 4 |
| `unclassified` | 3 |
| `slice-from-raw-parts-init-violation` | 3 |
| `transmute-utf8-range-invariant` | 3 |
| `len-cap-confusion` | 2 |
| `transmute-chained-cast` | 1 |
| `transmute-size-mismatch` | 1 |
| `debug-guard-only` | 1 |
| `zst-ptr-arith` | 1 |

### Per `cwe`

| CWE | Count | Class |
|---|---|---|
| `CWE-416` | 13 | Use After Free |
| `CWE-415` | 9 | Double Free |
| `CWE-908` | 9 | Use of Uninitialized Resource |
| `CWE-362` | 9 | Concurrent Execution using Shared Resource (Race Condition) |
| `CWE-125` | 8 | Out-of-bounds Read |
| `CWE-119` | 6 | Improper Restriction of Operations within Bounds |
| `CWE-787` | 6 | Out-of-bounds Write |
| `CWE-704` | 5 | Incorrect Type Conversion or Cast |
| `CWE-843` | 4 | Type Confusion |
| `CWE-190` | 3 | Integer Overflow or Wraparound |
| `CWE-200` | 2 | Exposure of Sensitive Information |
| `CWE-126` | 1 | Buffer Over-read |
| `CWE-459` | 1 | Incomplete Cleanup |
| `CWE-476` | 1 | NULL Pointer Dereference |
| `CWE-191` | 1 | Integer Underflow |
| `CWE-826` | 1 | Premature Release of Resource |
| `CWE-212` | 1 | Improper Removal of Sensitive Information |

### Per `license` (upstream repo)

| License | Count |
|---|---|
| `Apache-2.0` | 43 |
| `MIT` | 35 |
| `MPL-2.0` | 1 |
| `Zlib` | 1 |

### Phase 5 (Miri witness gate) eligibility

- `phase5_eligible = true`: **30** entries (subset of `rustxec_msr_2026`).
- `phase5_eligible = false`: **50** entries.

Phase 5 is a **Ward-only axis** (see methodology §6). The Miri witness gate runs
Ward's emitted findings against a runnable witness fixture and confirms via Miri
whether the runtime UB matches the static prediction. Competitor tools do not have
equivalent machinery, so positive-witness rate is reported as Ward-only context, not
as a head-to-head metric.

## Per-repo distribution

**65 unique upstream repositories** are referenced. Top 10 by entry count:

| Repository | Entries |
|---|---|
| `bytecodealliance/wasmtime` | 3 |
| `tokio-rs/tokio` | 3 |
| `image-rs/imageproc` | 3 |
| `jeromefroe/lru-rs` | 2 |
| `sfackler/rust-openssl` | 2 |
| `antonmarsden/toodee` | 2 |
| `PyO3/pyo3` | 2 |
| `okready/scratchpad` | 2 |
| `rwf2/Rocket` | 2 |
| `GitoxideLabs/gitoxide` | 2 |

Full repo list: see `provenance/<id>.md` for each entry.

## File structure

```
unsafe-rust-bench/
├── README.md              # this file
├── manifest.toml          # 80 paired entries (160 rows) — locked schema per methodology §3
├── MANIFEST.sha256        # SHA-256 of manifest.toml
├── inclusion-log.md       # candidate-by-candidate decision log (every accept/reject)
└── provenance/
    ├── rs-bench-<id>.md   # per-entry: advisory + commits + license + methodology conformance
    └── ...                # 80 files
```

## How to reproduce the collection

```bash
# 1. Clone the RUSTSEC advisory database (pinned at corpus-collection time)
git clone https://github.com/rustsec/advisory-db.git

# 2. Run the candidate-discovery pipeline (script at target/bench-cache/, not committed)
#    The pipeline:
#    - Parses 1049 RUSTSEC advisories
#    - Filters by date ≥ 2024-01-01 + memory-safety categories/keywords
#    - Cross-references against tests/cve-registry/manifest.toml (drops already-seen)
#    - Verifies upstream repo + fix-commit availability via GitHub API
#    - Verifies license-permissive via GitHub API + manual Cargo.toml inspection
#    - Classifies vuln_class / CWE / bug_shape from advisory body

# 3. Verify each entry by cloning the upstream repo and checking out the commits
for entry in $(cat manifest.toml | grep '^id = ' | cut -d'"' -f2); do
    # See provenance/<entry>.md for the upstream repo URL + commits
    : run your scanner here
done
```

The full collection pipeline is auditable via the inclusion-log.md decision record.

## How to add a new entry

New entries must conform to methodology §3:

1. Source advisory in RUSTSEC or GHSA-cargo
2. In-scope CWE (deciding signal)
3. Public, identifiable fix commit
4. Vulnerable commit identifiable
5. Repository public, alive, clonable
6. License permits redistribution (Apache-2.0 | MIT | BSD-2/3 | MPL-2.0 | CC0 | Zlib | ISC | Unicode-3.0)

Plus add a `provenance/<id>.md` file with the advisory link, commit hashes, license
verification, and methodology conformance checklist.

## License attestation

- **Corpus manifest** (this file + `manifest.toml` + `provenance/*`): CC-BY-4.0
- **Source repos** referenced: each retains its own permissive license. Source is
  fetched at scan time from upstream; we do not redistribute it.

Per-repo license distribution table above. All licenses are confirmed permissive
per methodology §3 inclusion 6.

## Relationship to Ward's existing manifest

This corpus is **derived from** but **distinct from** Ward's primary CVE manifest
at `tests/cve-registry/manifest.toml`. The primary manifest contains 3834 entries
across 5 languages and is used for Ward's ongoing real-repo eval. This corpus is a
frozen subset+augment of that manifest specifically for the head-to-head benchmark.

Entry IDs are prefixed `rs-bench-` to distinguish from the primary manifest. Each
entry has a 1:1 mapping back to its primary-manifest origin (for `rustxec_msr_2026`
and `manual_curation` sources) or to a RUSTSEC advisory (for `rustsec_2024_2026`).
See `provenance/<id>.md` for the per-entry origin.

## Out-of-scope (per methodology §10)

- Non-Rust corpora (separate benchmarks)
- Supply-chain advisory matching (cargo-audit's lane)
- Proprietary tools (Veracode, Snyk, Coverity, etc.)
- proc-macro-only vulnerabilities
- Cloud-API tools (use the CodeQL CLI offline variant)
- LLM-only scanners
- Build-time vulnerabilities requiring network fetch during build

## Held-out validation set

Per methodology §11.1 mitigation, a separate **held-out validation set** of ≥20
entries is collected by a separate sealed-agent run that does not see this main
corpus. **That set is not in this directory**. It is collected and frozen by a
sibling bone (to be filed) and sealed until benchmark publication day to prevent
leakage.

## Citation

When citing this benchmark, reference:

- The methodology document (`notes/benchmarks/unsafe-rust-bench-methodology.md`)
- This corpus manifest (`manifest.toml`) at the SHA pinned by `MANIFEST.sha256`
- The benchmark version tag (`unsafe-rust-bench-v1`)

Generated under bone bn-2tdyf, parent goal bn-1ti5m, in the Ward project.