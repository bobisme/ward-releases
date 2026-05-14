# rs-bench-rustsec-2024-0435

**Benchmark entry**: `rs-bench-rustsec-2024-0435` (paired with `rs-bench-rustsec-2024-0435-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0435` — https://rustsec.org/advisories/RUSTSEC-2024-0435.html
**Aliases**: `GHSA-h7h7-6mx3-r89v`
**Package**: `fyrox-core` (advisory date: 2024-12-19)
**CWE**: `CWE-843` (soundness / layout-cast)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/FyroxEngine/Fyrox.git`
- Vulnerable commit (parent of fix): `31344ef0420a5bc1c31b04e4989f45e1fc061c09`
- Fixing commit: `474e3b01a884366cdb7d704f7456ef692e992232`
- Resolution method: `manual-git-log-v4`
- Affected file: `fyrox-core/src/lib.rs`

## Files changed by fix

- `fyrox-core/Cargo.toml`
- `fyrox-core/src/lib.rs`
- `fyrox-impl/Cargo.toml`
- `fyrox-impl/src/scene/mesh/surface.rs`

## Expected finding

> fyrox-core BytesStorage Deref/DerefMut on VertexBuffer reads VertexBuffer<T> bytes as T (transmute) — type confusion if alignment mismatches

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
Advisory keywords: ['uninitialized']
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
