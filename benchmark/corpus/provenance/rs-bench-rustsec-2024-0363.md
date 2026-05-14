# rs-bench-rustsec-2024-0363

**Benchmark entry**: `rs-bench-rustsec-2024-0363` (paired with `rs-bench-rustsec-2024-0363-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0363` — https://rustsec.org/advisories/RUSTSEC-2024-0363.html
**Aliases**: `GHSA-xmrp-424f-vfpx`
**Package**: `sqlx` (advisory date: 2024-08-15)
**CWE**: `CWE-190` (memory_safety / int-overflow-safety)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/launchbadge/sqlx.git`
- Vulnerable commit (parent of fix): `9ec09fb78927bf56f99ce72fc3c853ec1d554a31`
- Fixing commit: `16f8b1900d6a41528518e7594d9c13e4bc6c2a55`
- Resolution method: `manual-git-log`
- Affected file: `sqlx-postgres/src/arguments.rs`

## Files changed by fix

- `sqlx-postgres/src/arguments.rs`

## Expected finding

> sqlx-postgres binary protocol overflow: truncating cast on encoded value length lets attacker smuggle queries past 4 GiB boundary

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['format-injection']
Advisory keywords: ['sql', 'injection', 'overflow', 'truncation']
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
