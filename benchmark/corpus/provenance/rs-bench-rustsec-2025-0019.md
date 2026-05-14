# rs-bench-rustsec-2025-0019

**Benchmark entry**: `rs-bench-rustsec-2025-0019` (paired with `rs-bench-rustsec-2025-0019-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0019` — https://rustsec.org/advisories/RUSTSEC-2025-0019.html
**Aliases**: `GHSA-67r5-rqwv-9p9q`
**Package**: `array-init-cursor` (advisory date: 2025-03-27)
**CWE**: `CWE-415` (memory_safety / panic-sequence)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/planus-org/planus.git`
- Vulnerable commit (parent of fix): `1cf18d16af7cf0b17c8f95f7c0fd362c69c78236`
- Fixing commit: `be6f99afde8760dcf87b5dcdade832400e826791`
- Resolution method: `manual-git-log`
- Affected file: `crates/array-init-cursor/src/lib.rs`

## Files changed by fix

- `Cargo.lock`
- `Cargo.toml`
- `crates/array-init-cursor/Cargo.toml`
- `crates/array-init-cursor/src/lib.rs`
- `crates/planus/src/union_vectors/iterators.rs`

## Expected finding

> array-init-cursor 0.2.0 runs Drop twice on stored value via Cursor — double-drop UB when used with non-Copy types

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: []
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
