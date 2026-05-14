# rs-bench-rustsec-2026-0008

**Benchmark entry**: `rs-bench-rustsec-2026-0008` (paired with `rs-bench-rustsec-2026-0008-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0008` — https://rustsec.org/advisories/RUSTSEC-2026-0008.html
**Aliases**: `GHSA-j39j-6gw9-jw6h`
**Package**: `git2` (advisory date: 2026-02-02)
**CWE**: `CWE-119` (memory_safety / ffi-boundary-contract)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/rust-lang/git2-rs.git`
- Vulnerable commit (parent of fix): `03ec58122907ba45fc9f9ba7721a7e62be1f719e`
- Fixing commit: `9e160f15bd056f82143109bb330573381e5de719`
- Resolution method: `pr-1213`
- Affected file: `src/buf.rs`

## Files changed by fix

- `src/buf.rs`

## Expected finding

> git2-rs Buf::as_slice trusts upstream libgit2 buffer length without validation — out-of-bounds read on truncated buffer

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: ['undefined-behavior']
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
