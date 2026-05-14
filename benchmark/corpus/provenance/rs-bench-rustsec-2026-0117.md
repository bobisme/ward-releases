# rs-bench-rustsec-2026-0117

**Benchmark entry**: `rs-bench-rustsec-2026-0117` (paired with `rs-bench-rustsec-2026-0117-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0117` — https://rustsec.org/advisories/RUSTSEC-2026-0117.html
**Aliases**: `GHSA-qg8r-f7x3-25f7`
**Package**: `imageproc` (advisory date: 2026-05-01)
**CWE**: `CWE-125` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/image-rs/imageproc.git`
- Vulnerable commit (parent of fix): `ef38866275c697379c483d5a631fd94e7e70ee27`
- Fixing commit: `8a9e5d53984c5b7b43012da90cd9be130d09b536`
- Resolution method: `manual-git-log-v7`
- Affected file: `examples/projection.rs`

## Files changed by fix

- `Cargo.toml`
- `examples/projection.rs`
- `src/definitions.rs`
- `src/geometric_transformations.rs`
- `tests/data/truth/elephant_affine_bicubic.png`
- `tests/data/truth/elephant_affine_bilinear.png`
- `tests/data/truth/elephant_rotate_bicubic.png`
- `tests/data/truth/elephant_rotate_bicubic_rgba.png`
- `tests/data/truth/elephant_rotate_bilinear.png`
- `tests/data/truth/elephant_rotate_bilinear_rgba.png`
- … and 8 more

## Expected finding

> imageproc::warp_into / warp_into_with floating-point bounds check fails on NaN — OOB read on unchecked access

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
