# rs-bench-rustsec-2025-0106

**Benchmark entry**: `rs-bench-rustsec-2025-0106` (paired with `rs-bench-rustsec-2025-0106-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0106` — https://rustsec.org/advisories/RUSTSEC-2025-0106.html
**Aliases**: `GHSA-h5j3-crg5-8jqm`
**Package**: `orx-pinned-vec` (advisory date: 2025-10-21)
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/orxfun/orx-pinned-vec.git`
- Vulnerable commit (parent of fix): `fa4cf094d09f5f3f3b0bce5a9b71cf40901cff14`
- Fixing commit: `d4fb7b9f958665c04fb9ec6e5454439264a025be`
- Resolution method: `manual-git-log-v4`
- Affected file: `src/concurrent_pinned_vec.rs`

## Files changed by fix

- `src/concurrent_pinned_vec.rs`

## Expected finding

> orx-pinned-vec iter / iter_mut hand out aliased &mut references via raw-pointer iteration without lifetime gate

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: ['undefined-behavior', 'soundness']
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
