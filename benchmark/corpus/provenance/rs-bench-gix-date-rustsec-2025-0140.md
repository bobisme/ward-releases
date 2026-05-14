# rs-bench-gix-date-rustsec-2025-0140

**Benchmark entry**: `rs-bench-gix-date-rustsec-2025-0140` (paired with `rs-bench-gix-date-rustsec-2025-0140-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2025-0140` — https://rustsec.org/advisories/RUSTSEC-2025-0140.html
**CVE ID**: `CVE-2026-0810`
**CWE**: `CWE-704` (memory_safety / transmute-utf8-range-invariant)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/GitoxideLabs/gitoxide.git`
- Vulnerable commit: `21fecdf928336ac5fa3dd1402f92e8200d8aff62`
- Fixing commit: `115e208b7bc7a96024e64ea872f2731b5125a6e0`
- Affected file: ``

## Expected finding

> TimeBuf::as_str does `unsafe { std::str::from_utf8_unchecked(self.bytes()) }` without ensuring the buffer is valid UTF-8. Subsequent str ops (char_indices, slice) trigger UB on multi-byte boundaries.

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-gix-date-rustsec-2025-0140`.
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
