# rs-bench-rustsec-2025-0051

**Benchmark entry**: `rs-bench-rustsec-2025-0051` (paired with `rs-bench-rustsec-2025-0051-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0051` — https://rustsec.org/advisories/RUSTSEC-2025-0051.html
**Aliases**: `GHSA-655h-hg88-5qmf`
**Package**: `xcb` (advisory date: 2025-08-05)
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/rust-x-bindings/rust-xcb.git`
- Vulnerable commit (parent of fix): `521241dba9ccd6911e4c9c1b96df2ecb77a835ca`
- Fixing commit: `1bce975980fe396b5faf1d12bee43e69e168b72f`
- Resolution method: `manual-git-log-v2`
- Affected file: `src/base.rs`

## Files changed by fix

- `src/base.rs`

## Expected finding

> xcb::Connection::connect_to_fd* takes RawFd without OwnedFd transfer — drop closes fd that caller may still hold, fd UAF

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
Advisory keywords: ['io-safety']
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
