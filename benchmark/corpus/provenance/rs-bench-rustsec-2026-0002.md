# rs-bench-rustsec-2026-0002

**Benchmark entry**: `rs-bench-rustsec-2026-0002` (paired with `rs-bench-rustsec-2026-0002-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0002` — https://rustsec.org/advisories/RUSTSEC-2026-0002.html
**Aliases**: `GHSA-rhfx-m35p-ff5j`
**Package**: `lru` (advisory date: 2026-01-07)
**CWE**: `CWE-787` (memory_safety / len-cap-confusion)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/jeromefroe/lru-rs.git`
- Vulnerable commit (parent of fix): `c1f843ded02d718138483df6ed8da4961accc201`
- Fixing commit: `62be24c96137fcf5c6323607ff15ed878b157ee2`
- Resolution method: `pr-224`
- Affected file: `src/lib.rs`

## Files changed by fix

- `src/lib.rs`

## Expected finding

> lru iter / iter_mut hand out &mut on aliased entries via raw-pointer iteration — len-cap confusion / aliasing UAF

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: ['stacked-borrows']
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
