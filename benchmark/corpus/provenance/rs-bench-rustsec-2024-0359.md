# rs-bench-rustsec-2024-0359

**Benchmark entry**: `rs-bench-rustsec-2024-0359` (paired with `rs-bench-rustsec-2024-0359-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0359` — https://rustsec.org/advisories/RUSTSEC-2024-0359.html
**Aliases**: `GHSA-cx7h-h87r-jpgr`
**Package**: `gix-attributes` (advisory date: 2024-07-24)
**CWE**: `CWE-704` (soundness / transmute-utf8-range-invariant)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/GitoxideLabs/gitoxide.git`
- Vulnerable commit (parent of fix): `a807dd1ffb05efd177700d065095249e6c4b3c68`
- Fixing commit: `3cb216edcaab67b5de9ccc97cdcf2468a466f0d7`
- Resolution method: `manual-git-log-v2`
- Affected file: `gix-attributes/src/lib.rs`

## Files changed by fix

- `gix-attributes/src/lib.rs`
- `gix-attributes/src/name.rs`
- `gix-attributes/src/parse.rs`
- `gix-attributes/src/search/mod.rs`
- `gix-attributes/src/state.rs`
- `gix-attributes/tests/parse/mod.rs`
- `gix-attributes/tests/search/mod.rs`

## Expected finding

> gix-attributes ValueRef unsafely creates &str from &[u8] containing non-UTF-8 data via kstring — soundness violation

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
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
