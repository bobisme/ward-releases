# rs-bench-self-cell-rustsec-2023-0070

**Benchmark entry**: `rs-bench-self-cell-rustsec-2023-0070` (paired with `rs-bench-self-cell-rustsec-2023-0070-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2023-0070` — https://rustsec.org/advisories/RUSTSEC-2023-0070.html
**CWE**: `CWE-843` (type_confusion / unclassified)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/Voultapher/self_cell.git`
- Vulnerable commit: `e418be1c132a57d3b9ccc56847443b83457cbe83`
- Fixing commit: `2f3448127bb2058acaaaa90886613f2f99581257`
- Affected file: `src/lib.rs`

## Expected finding

> 

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-self-cell-rustsec-2023-0070`.
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
