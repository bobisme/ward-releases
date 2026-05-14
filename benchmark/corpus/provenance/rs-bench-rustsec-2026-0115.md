# rs-bench-rustsec-2026-0115

**Benchmark entry**: `rs-bench-rustsec-2026-0115` (paired with `rs-bench-rustsec-2026-0115-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0115` — https://rustsec.org/advisories/RUSTSEC-2026-0115.html
**Aliases**: `GHSA-5qv7-j6w5-fr4m`
**Package**: `imageproc` (advisory date: 2026-05-01)
**CWE**: `CWE-125` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/image-rs/imageproc.git`
- Vulnerable commit (parent of fix): `92111303f1baab8bf4f2e4598e4cd08f54877b80`
- Fixing commit: `a6c2393f0c6aee7e7522970a792ce0ce2730e336`
- Resolution method: `manual-git-log-v7`
- Affected file: `src/binary_descriptors/brief.rs`

## Files changed by fix

- `src/binary_descriptors/brief.rs`

## Expected finding

> imageproc::binary_descriptors::brief samples pixels with coordinate that can overflow (constant + input) — OOB read

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
