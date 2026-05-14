# rs-bench-slab-rustsec-2025-0047

**Benchmark entry**: `rs-bench-slab-rustsec-2025-0047` (paired with `rs-bench-slab-rustsec-2025-0047-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2025-0047` — https://rustsec.org/advisories/RUSTSEC-2025-0047.html
**CWE**: `CWE-125` (memory_safety / slice-from-raw-parts-init-violation)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/tokio-rs/slab.git`
- Vulnerable commit: `6a1b675665ee141ab68fd3e4f82b3cb3efc09e01`
- Fixing commit: `2d65c514bc964b192bab212ddf3c1fcea4ae96b8`
- Affected file: `src/lib.rs`

## Expected finding

> 

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-slab-rustsec-2025-0047`.
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
