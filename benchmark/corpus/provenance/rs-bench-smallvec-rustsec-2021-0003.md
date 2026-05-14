# rs-bench-smallvec-rustsec-2021-0003

**Benchmark entry**: `rs-bench-smallvec-rustsec-2021-0003` (paired with `rs-bench-smallvec-rustsec-2021-0003-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2021-0003` — https://rustsec.org/advisories/RUSTSEC-2021-0003.html
**CVE ID**: `CVE-2021-25900`
**CWE**: `CWE-787` (memory_safety / int-overflow-safety)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/servo/rust-smallvec.git`
- Vulnerable commit: `78522049b3ce129d02eea4e802747ba1090a5586`
- Fixing commit: `5757ac500d4e544485d796b542e4e589749c291b`
- Affected file: ``

## Expected finding

> SmallVec::insert_many trusted Iterator::size_hint() to size the destination buffer; if the iterator yields more elements than the lower bound advertised, the writer steps past the allocation. The unsafe write loop has no bounds check against the reserved capacity.

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-smallvec-rustsec-2021-0003`.
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
