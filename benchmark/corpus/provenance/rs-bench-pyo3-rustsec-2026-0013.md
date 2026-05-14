# rs-bench-pyo3-rustsec-2026-0013

**Benchmark entry**: `rs-bench-pyo3-rustsec-2026-0013` (paired with `rs-bench-pyo3-rustsec-2026-0013-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2026-0013` — https://rustsec.org/advisories/RUSTSEC-2026-0013.html
**CWE**: `CWE-843` (type_confusion / layout-cast)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/PyO3/pyo3.git`
- Vulnerable commit: `b62c7a278fc14e9afb0d73ab1ded7ba00cda3be2`
- Fixing commit: `75abd8602896b350fd8c778e52e0a74b4644ccca`
- Affected file: `src/pycell/impl_.rs`

## Expected finding

> 

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-pyo3-rustsec-2026-0013`.
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
