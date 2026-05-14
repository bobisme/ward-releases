# rs-bench-rustsec-2024-0342

**Benchmark entry**: `rs-bench-rustsec-2024-0342` (paired with `rs-bench-rustsec-2024-0342-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0342` — https://rustsec.org/advisories/RUSTSEC-2024-0342.html
**CVE ID**: `CVE-2024-34063`
**Aliases**: `CVE-2024-34063`, `GHSA-c3hm-hxwf-g5c6`
**Package**: `vodozemac` (advisory date: 2024-05-02)
**CWE**: `CWE-200` (memory_safety / safe-encap)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/matrix-org/vodozemac.git`
- Vulnerable commit (parent of fix): `266a388a41d7d17bf92e8ec051634a20f67151f4`
- Fixing commit: `1f8ee9acbf7ffc32a4c9e71bcc62b5136d24a888`
- Resolution method: `manual-git-log-v4`
- Affected file: `src/olm/account/mod.rs`

## Files changed by fix

- `src/olm/account/mod.rs`
- `src/olm/session/mod.rs`

## Expected finding

> vodozemac libolm-compat Debug impl prints private key material — memory exposure via debug logs

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
Advisory keywords: []
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
