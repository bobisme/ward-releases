# rs-bench-thin-vec-rustsec-2026-0103

**Benchmark entry**: `rs-bench-thin-vec-rustsec-2026-0103` (paired with `rs-bench-thin-vec-rustsec-2026-0103-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2026-0103` — https://rustsec.org/advisories/RUSTSEC-2026-0103.html
**CWE**: `CWE-416` (memory_safety / panic-sequence)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/Gankra/thin-vec.git`
- Vulnerable commit: `70bcca0960a7e11056fa3281445d08052421dab5`
- Fixing commit: `df64748355222525c344ecd9d2c9f59a662e1678`
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

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-thin-vec-rustsec-2026-0103`.
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
