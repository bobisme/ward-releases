# rs-bench-rustsec-2026-0116

**Benchmark entry**: `rs-bench-rustsec-2026-0116` (paired with `rs-bench-rustsec-2026-0116-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0116` — https://rustsec.org/advisories/RUSTSEC-2026-0116.html
**Aliases**: `GHSA-w5p8-4jcx-2j6r`
**Package**: `imageproc` (advisory date: 2026-05-01)
**CWE**: `CWE-190` (memory_safety / int-overflow-safety)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/image-rs/imageproc.git`
- Vulnerable commit (parent of fix): `1e5197fde065d66eb1ef44863f0e6b77d3ffc754`
- Fixing commit: `17511afd8135e9115700ebc24f6f7670ab8aeb12`
- Resolution method: `manual-git-log-v7`
- Affected file: `src/kernel.rs`

## Files changed by fix

- `src/kernel.rs`

## Expected finding

> imageproc::Kernel::new dimension overflow before bounds compare — bounds check bypass for crafted dimensions

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
Advisory keywords: ['out-of-bounds read', 'memory-safety']
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
