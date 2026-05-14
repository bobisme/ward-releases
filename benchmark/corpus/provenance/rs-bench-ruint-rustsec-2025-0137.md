# rs-bench-ruint-rustsec-2025-0137

**Benchmark entry**: `rs-bench-ruint-rustsec-2025-0137` (paired with `rs-bench-ruint-rustsec-2025-0137-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2025-0137` — https://rustsec.org/advisories/RUSTSEC-2025-0137.html
**CWE**: `CWE-125` (memory_safety / debug-guard-only)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/recmo/uint.git`
- Vulnerable commit: `7732304cfe489141fdff939121edf35b8bb343d7`
- Fixing commit: `bc3fad727853ce31fa78a053c950748db8571369`
- Affected file: ``

## Expected finding

> ruint::algorithms::div::reciprocal_mg10 has `debug_assert!(d.bit(63))` guarding subsequent unsafe slice indexing. In release builds, the assertion is no-op; out-of-precondition input proceeds to the unsafe block and reads OOB.

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-ruint-rustsec-2025-0137`.
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
