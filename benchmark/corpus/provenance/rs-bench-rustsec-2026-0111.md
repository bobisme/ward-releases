# rs-bench-rustsec-2026-0111

**Benchmark entry**: `rs-bench-rustsec-2026-0111` (paired with `rs-bench-rustsec-2026-0111-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0111` — https://rustsec.org/advisories/RUSTSEC-2026-0111.html
**Aliases**: `GHSA-h5x4-m2qf-r4f2`
**Package**: `diesel` (advisory date: 2026-04-24)
**CWE**: `CWE-704` (soundness / transmute-utf8-range-invariant)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/diesel-rs/diesel.git`
- Vulnerable commit (parent of fix): `df1f3ee56d8c8ae17dfab081de36a17668bfb31c`
- Fixing commit: `bb17563ca7dd92ceed92d508e3384972b38490c1`
- Resolution method: `pr-5042`
- Affected file: `diesel/src/deserialize.rs`

## Files changed by fix

- `diesel/src/deserialize.rs`
- `diesel/src/mysql/connection/bind.rs`
- `diesel/src/mysql/types/date_and_time/mod.rs`
- `diesel/src/mysql/types/primitives.rs`
- `diesel/src/mysql/value.rs`
- `diesel/src/pg/connection/mod.rs`
- `diesel/src/pg/connection/raw.rs`
- `diesel/src/pg/connection/result.rs`
- `diesel/src/pg/query_builder/copy/copy_from.rs`
- `diesel/src/pg/query_builder/copy/mod.rs`
- … and 14 more

## Expected finding

> diesel SqliteValue::read_str calls str::from_utf8_unchecked on sqlite3_value_text() output without UTF-8 validation — soundness break

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
Advisory keywords: []
Informational flag: `unsound`

NOT previously used by Ward authors during rule development.
No corresponding entry existed in `tests/cve-registry/manifest.toml` prior to this benchmark.

## Methodology conformance

- [x] Source advisory in RUSTSEC (§3 inclusion 1)
- [x] In-scope vuln class (CWE deciding signal; §3 inclusion 2)
- [x] Public, identifiable fix commit (§3 inclusion 3)
- [x] Vulnerable commit identifiable (parent of fix; §3 inclusion 4)
- [x] Repository public, alive, clonable (§3 inclusion 5)
- [x] License permits redistribution (§3 inclusion 6)
- [x] Date ≥ 2024-01-01 (novel-augment window per methodology §3)
- [x] NOT in Ward's existing manifest (novel constraint per methodology §3)
