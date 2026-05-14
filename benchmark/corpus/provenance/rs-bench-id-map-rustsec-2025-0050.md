# rs-bench-id-map-rustsec-2025-0050

**Benchmark entry**: `rs-bench-id-map-rustsec-2025-0050` (paired with `rs-bench-id-map-rustsec-2025-0050-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2025-0050` — https://rustsec.org/advisories/RUSTSEC-2025-0050.html
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/andrewhickman/id-map.git`
- Vulnerable commit: `a2fa8d4a554dea2f9ea2ec6c3d06793576f8e7c0`
- Fixing commit: `fab6922b955b5a2986dfff2ccb341628faec30ed`
- Affected file: ``

## Expected finding

> IdMap::from_iter sets `ids` length based on `values.capacity()` rather than `values.len()`. On drop, the destructor iterates 0..ids.len() and calls drop on each value slot, including uninitialized memory in `[len..capacity)`.

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-id-map-rustsec-2025-0050`.
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
