# rs-bench-openssl-ghsa-4fcv

**Benchmark entry**: `rs-bench-openssl-ghsa-4fcv` (paired with `rs-bench-openssl-ghsa-4fcv-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `GHSA-4fcv-w3qc-ppgg`
**CWE**: `CWE-416` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/sfackler/rust-openssl.git`
- Vulnerable commit: `7c7b2e6c9f95e77e56ab37af70b16de75beff387`
- Fixing commit: `87085bd67896b7f92e6de35d081f607a334beae4`
- Affected file: `openssl/src/md.rs`

## Expected finding

> 

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-openssl-ghsa-4fcv`.
Selected for this benchmark because the source RUSTSEC advisory falls in the
manually-curated memory-safety category (one of `memory-corruption`, `memory-exposure`,
`thread-safety`, `format-injection`, or marked `informational = "unsound"`) —
third-party gating filter (b) per methodology §3.

## Methodology conformance

- [x] Source advisory in RUSTSEC or GHSA-cargo (§3 inclusion 1)
- [x] In-scope vuln class (CWE deciding signal; §3 inclusion 2)
- [x] Public, identifiable fix commit (§3 inclusion 3)
- [x] Vulnerable commit identifiable (§3 inclusion 4)
- [x] Repository public, alive, clonable (§3 inclusion 5)
- [x] License permits redistribution (§3 inclusion 6)
