# rs-bench-rustsec-2025-0027

**Benchmark entry**: `rs-bench-rustsec-2025-0027` (paired with `rs-bench-rustsec-2025-0027-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0027` — https://rustsec.org/advisories/RUSTSEC-2025-0027.html
**Aliases**: `GHSA-927q-g9w9-pm54`
**Package**: `mp3-metadata` (advisory date: 2025-04-28)
**CWE**: `CWE-119` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/GuillaumeGomez/mp3-metadata.git`
- Vulnerable commit (parent of fix): `7699ac280e10394bec52c85753bfbc148f298f17`
- Fixing commit: `5a9c891db32a89191d23093366a08a92f903a47d`
- Resolution method: `pr-37`
- Affected file: `src/metadata.rs`

## Files changed by fix

- `src/metadata.rs`

## Expected finding

> mp3-metadata unsafe slice indexing past buffer bounds when parsing malformed MP3 frame — OOB read

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['denial-of-service']
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
