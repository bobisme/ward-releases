# rs-bench-rustsec-2024-0007

**Benchmark entry**: `rs-bench-rustsec-2024-0007` (paired with `rs-bench-rustsec-2024-0007-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0007` — https://rustsec.org/advisories/RUSTSEC-2024-0007.html
**Aliases**: `GHSA-c8v3-jhv9-4ppc`
**Package**: `rust-i18n-support` (advisory date: 2024-01-19)
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/longbridgeapp/rust-i18n.git`
- Vulnerable commit (parent of fix): `37aa93a07c0da2ce8286e337fd137874bdec2e29`
- Fixing commit: `22e0609591a2c08930f52a0e6bc860f02a0e88c0`
- Resolution method: `manual-git-log`
- Affected file: `crates/support/src/atomic_str.rs`

## Files changed by fix

- `README.md`
- `crates/support/Cargo.toml`
- `crates/support/src/atomic_str.rs`
- `src/lib.rs`
- `tests/multi_threading.rs`

## Expected finding

> rust-i18n AtomicStr stores Arc<String> as raw pointer; as_str() returns &str without incrementing arc refcount — UAF after locale change

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
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
