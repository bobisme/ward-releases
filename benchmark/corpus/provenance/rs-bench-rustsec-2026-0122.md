# rs-bench-rustsec-2026-0122

**Benchmark entry**: `rs-bench-rustsec-2026-0122` (paired with `rs-bench-rustsec-2026-0122-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0122` — https://rustsec.org/advisories/RUSTSEC-2026-0122.html
**Package**: `rkyv` (advisory date: 2026-04-23)
**CWE**: `CWE-908` (soundness / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/rkyv/rkyv.git`
- Vulnerable commit (parent of fix): `7f93b3328ca3b9038f062afd925c6a4aa1e070b1`
- Fixing commit: `5828cf5c27b664eb4432c4a93d4769e12e5e42fb`
- Resolution method: `commit-link`
- Affected file: `rkyv/src/util/inline_vec.rs`

## Files changed by fix

- `rkyv/src/util/inline_vec.rs`
- `rkyv/src/util/ser_vec.rs`

## Expected finding

> rkyv ser_vec inline_vec::reserve_exact set_len before init — uninit read on serialize

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['code-execution', 'memory-corruption']
Advisory keywords: ['panic-safety', 'memory-safety', 'use-after-free', 'double-free']
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
