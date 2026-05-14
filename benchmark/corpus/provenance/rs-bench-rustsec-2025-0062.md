# rs-bench-rustsec-2025-0062

**Benchmark entry**: `rs-bench-rustsec-2025-0062` (paired with `rs-bench-rustsec-2025-0062-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0062` — https://rustsec.org/advisories/RUSTSEC-2025-0062.html
**Aliases**: `GHSA-pfp7-vxgr-83pw`
**Package**: `toodee` (advisory date: 2025-05-22)
**CWE**: `CWE-787` (memory_safety / panic-sequence)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/antonmarsden/toodee.git`
- Vulnerable commit (parent of fix): `0467f3d66116eebf7d6f3f5f60e28a19702161ea`
- Fixing commit: `e6e16d5a97e6258ffbedbae1bde65b45c60f242f`
- Resolution method: `manual-git-log-v6`
- Affected file: `src/toodee.rs`

## Files changed by fix

- `src/tests.rs`
- `src/toodee.rs`

## Expected finding

> toodee DrainCol::drop ptr::copy invocation has off-by-one length, copying beyond DrainCol vec bounds — heap BOF on drop

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption', 'memory-exposure']
Advisory keywords: ['memory-safety', 'buffer-overflow']
Informational flag: `None`

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
