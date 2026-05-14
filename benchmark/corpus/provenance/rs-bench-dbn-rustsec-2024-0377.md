# rs-bench-dbn-rustsec-2024-0377

**Benchmark entry**: `rs-bench-dbn-rustsec-2024-0377` (paired with `rs-bench-dbn-rustsec-2024-0377-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2024-0377` — https://rustsec.org/advisories/RUSTSEC-2024-0377.html
**CWE**: `CWE-125` (memory_safety / ffi-boundary-contract)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/databento/dbn.git`
- Vulnerable commit: `f90df0a8da947ebd6d670519ba0c9bec1d28cf14`
- Fixing commit: `20379b8dd62b557d13aba2a9166488ca9eabcb86`
- Affected file: ``

## Expected finding

> c_chars_to_str calls `CStr::from_ptr(buf.as_ptr())` on a fixed-length `[c_char; N]` array that may not contain a null terminator. CStr::from_ptr → strlen reads past the array end into adjacent memory.

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-dbn-rustsec-2024-0377`.
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
