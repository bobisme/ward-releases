# rs-bench-safe-transmute-rustsec-2018-0013

**Benchmark entry**: `rs-bench-safe-transmute-rustsec-2018-0013` (paired with `rs-bench-safe-transmute-rustsec-2018-0013-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2018-0013` — https://rustsec.org/advisories/RUSTSEC-2018-0013.html
**CVE ID**: `CVE-2018-21000`
**CWE**: `CWE-119` (memory_safety / len-cap-confusion)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/nabijaczleweli/safe-transmute-rs.git`
- Vulnerable commit: `c79ebfdb5858982af59a78df471c7cad7a78fd23`
- Fixing commit: `a134e06d740f9d7c287f74c0af2cd06206774364`
- Affected file: `src/lib.rs`

## Expected finding

> guarded_transmute_vec_permissive and guarded_transmute_to_bytes_vec call `Vec::from_raw_parts(ptr, capacity, len)` — capacity and length arguments are swapped. Vec then thinks len > cap (or vice-versa), violating the Vec invariant. Subsequent push/extend writes past the allocation; on Drop the deallocator is called with the wrong size, causing heap corruption.

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-safe-transmute-rustsec-2018-0013`.
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
