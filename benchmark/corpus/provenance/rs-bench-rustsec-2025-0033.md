# rs-bench-rustsec-2025-0033

**Benchmark entry**: `rs-bench-rustsec-2025-0033` (paired with `rs-bench-rustsec-2025-0033-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0033` — https://rustsec.org/advisories/RUSTSEC-2025-0033.html
**Aliases**: `GHSA-79m9-55jc-p6mw`
**Package**: `scanner` (advisory date: 2025-03-27)
**CWE**: `CWE-704` (soundness / safe-encap)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/pombredanne/scanner-rs.git`
- Vulnerable commit (parent of fix): `2893e45f8d60692a11e8584ba01eb38fe7798fea`
- Fixing commit: `20e260a42a8279aac5bccdcaa56daefc20d852d3`
- Resolution method: `pr-1`
- Affected file: `src/lib.rs`

## Files changed by fix

- `src/lib.rs`

## Expected finding

> scanner unsound API exposes raw pointer cast without lifetime / validity check

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: ['out-of-bounds read']
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
