# rs-bench-rustsec-2025-0042

**Benchmark entry**: `rs-bench-rustsec-2025-0042` (paired with `rs-bench-rustsec-2025-0042-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0042` — https://rustsec.org/advisories/RUSTSEC-2025-0042.html
**Aliases**: `GHSA-xrrq-rrgq-h89w`
**Package**: `static-alloc` (advisory date: 2025-07-11)
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/197g/static-alloc.git`
- Vulnerable commit (parent of fix): `0732720d47a38f0065d47675003e583be04b3f39`
- Fixing commit: `d8d6a7d096d3aaafd963b356a8f1bbd8d26fd967`
- Resolution method: `manual-git-log`
- Affected file: `static-alloc/src/unsync/bump.rs`

## Files changed by fix

- `static-alloc/src/unsync/bump.rs`

## Expected finding

> static-alloc MemBump::new() allocates uninitialized memory; subsequent alloc calls read+write start of memory as Cell — UB (uninit Cell)

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure', 'memory-corruption']
Advisory keywords: ['initialization']
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
