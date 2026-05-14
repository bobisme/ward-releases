# rs-bench-rustsec-2024-0365

**Benchmark entry**: `rs-bench-rustsec-2024-0365` (paired with `rs-bench-rustsec-2024-0365-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0365` — https://rustsec.org/advisories/RUSTSEC-2024-0365.html
**Aliases**: `GHSA-wq9x-qwcq-mmgf`
**Package**: `diesel` (advisory date: 2024-08-23)
**CWE**: `CWE-190` (memory_safety / int-overflow-safety)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/diesel-rs/diesel.git`
- Vulnerable commit (parent of fix): `ae82c4a5a133db65612b7436356f549bfecda1c7`
- Fixing commit: `9eccd7d6d705ac53618bfd478152e32ec3b4536c`
- Resolution method: `manual-borderline-large-pr-2.2.3`
- Affected file: `diesel/src/pg/connection/stmt/mod.rs`

## Files changed by fix

- `diesel/src/pg/connection/stmt/mod.rs`
- `diesel/src/mysql/connection/bind.rs`

## Expected finding

> diesel binary protocol overflow: truncating casts at sqlite/mysql/pg encode boundary (CVE-2024-43791) — query smuggling past 4 GiB

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
