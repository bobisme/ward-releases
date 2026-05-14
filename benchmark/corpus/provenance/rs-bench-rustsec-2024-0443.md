# rs-bench-rustsec-2024-0443

**Benchmark entry**: `rs-bench-rustsec-2024-0443` (paired with `rs-bench-rustsec-2024-0443-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0443` — https://rustsec.org/advisories/RUSTSEC-2024-0443.html
**Aliases**: `GHSA-9q78-27f3-2jmh`
**Package**: `webp` (advisory date: 2024-09-06)
**CWE**: `CWE-125` (memory_safety / slice-from-raw-parts-init-violation)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/jaredforth/webp.git`
- Vulnerable commit (parent of fix): `d5238934376bd104f9f5718f7bb4cc4f151db3db`
- Fixing commit: `62b47060d7fb8cc0e92e522ee54948edf5aab556`
- Resolution method: `pr-44`
- Affected file: `src/encoder.rs`

## Files changed by fix

- `src/encoder.rs`
- `src/shared.rs`

## Expected finding

> libwebp decoder writes past output buffer on crafted WebP file — heap BOF in Rust binding

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
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
