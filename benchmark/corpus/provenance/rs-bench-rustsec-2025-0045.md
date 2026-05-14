# rs-bench-rustsec-2025-0045

**Benchmark entry**: `rs-bench-rustsec-2025-0045` (paired with `rs-bench-rustsec-2025-0045-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0045` — https://rustsec.org/advisories/RUSTSEC-2025-0045.html
**Package**: `static_cell` (advisory date: 2025-07-17)
**CWE**: `CWE-362` (soundness / impl-send-sync)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/embassy-rs/static-cell.git`
- Vulnerable commit (parent of fix): `2371f15a3728b85dfdf42d098b26aac13b9e1b96`
- Fixing commit: `a814b4af2347348566c133485022c7199a5b0dd2`
- Resolution method: `manual-git-log`
- Affected file: `src/lib.rs`

## Files changed by fix

- `src/lib.rs`

## Expected finding

> embassy ConstStaticCell<T>: Send was unconditional, allowing non-Send T values to cross threads — Sync soundness violation

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure', 'memory-corruption']
Advisory keywords: ['send', 'thread-safety']
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
