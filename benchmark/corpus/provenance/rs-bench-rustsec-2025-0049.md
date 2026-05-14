# rs-bench-rustsec-2025-0049

**Benchmark entry**: `rs-bench-rustsec-2025-0049` (paired with `rs-bench-rustsec-2025-0049-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0049` — https://rustsec.org/advisories/RUSTSEC-2025-0049.html
**Aliases**: `GHSA-77h3-w9rx-hj3q`
**Package**: `scratchpad` (advisory date: 2025-08-14)
**CWE**: `CWE-415` (memory_safety / panic-sequence)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/okready/scratchpad.git`
- Vulnerable commit (parent of fix): `0cc776fb47e5339259675eca5548dc524aa7c550`
- Fixing commit: `18abedadaa77646cce6f2ca2149c0119a2e4f428`
- Resolution method: `manual-git-log-v3`
- Affected file: `src/array_iter.rs`

## Files changed by fix

- `CHANGELOG.md`
- `src/array_iter.rs`
- `src/lib.rs`
- `src/tests.rs`
- `src/traits.rs`

## Expected finding

> scratchpad Allocation::drop_unchecked panics during drop_in_place run twice on subsequent unwind — double-free

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: ['memory-safety', 'buffer-overflow', 'raw-pointer']
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
