# rs-bench-ouch-rustsec-2024-0374

**Benchmark entry**: `rs-bench-ouch-rustsec-2024-0374` (paired with `rs-bench-ouch-rustsec-2024-0374-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2024-0374` — https://rustsec.org/advisories/RUSTSEC-2024-0374.html
**CWE**: `CWE-908` (type_confusion / transmute-size-mismatch)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/ouch-org/ouch.git`
- Vulnerable commit: `f474d2455e5cf604219986135d0d70e1528f62bc`
- Fixing commit: `0dbbd3b8825d1bb8f985b3e384cdd987d5f4d40f`
- Affected file: ``

## Expected finding

> convert_zip_date_time reads a u8 month from the zip header and `unsafe { mem::transmute::<u8, time::Month>(month) }` without checking 1..=12. Out-of-range bytes produce an invalid Month enum that downstream uses as an array index, causing OOB reads.

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-ouch-rustsec-2024-0374`.
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
