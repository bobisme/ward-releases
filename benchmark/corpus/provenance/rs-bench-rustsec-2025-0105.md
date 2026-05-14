# rs-bench-rustsec-2025-0105

**Benchmark entry**: `rs-bench-rustsec-2025-0105` (paired with `rs-bench-rustsec-2025-0105-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0105` — https://rustsec.org/advisories/RUSTSEC-2025-0105.html
**Aliases**: `GHSA-fp5x-7m4q-449f`
**Package**: `direct_ring_buffer` (advisory date: 2025-10-21)
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/ain1084/direct_ring_buffer.git`
- Vulnerable commit (parent of fix): `09022f60ac0970c999bd89d8ec4e697f978f8794`
- Fixing commit: `0b29f73465f81cd9ac9e8c864a66604439159d7e`
- Resolution method: `manual-git-log`
- Affected file: `benches/benchmarks.rs`

## Files changed by fix

- `.github/workflows/rust.yml`
- `CHANGELOG.md`
- `Cargo.toml`
- `README.md`
- `benches/benchmarks.rs`
- `src/lib.rs`
- `tests/tests.rs`

## Expected finding

> direct_ring_buffer uses set_len(capacity) before initialization — uninit read on first read after allocation

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
Advisory keywords: ['uninitialized-memory', 'soundness']
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
