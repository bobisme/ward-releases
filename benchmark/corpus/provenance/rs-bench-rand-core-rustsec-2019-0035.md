# rs-bench-rand-core-rustsec-2019-0035

**Benchmark entry**: `rs-bench-rand-core-rustsec-2019-0035` (paired with `rs-bench-rand-core-rustsec-2019-0035-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2019-0035` — https://rustsec.org/advisories/RUSTSEC-2019-0035.html
**CVE ID**: `CVE-2020-25576`
**CWE**: `CWE-704` (type_confusion / transmute-chained-cast)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/rust-random/rand.git`
- Vulnerable commit: `c9fd8897a364e4a1558d18294e6fac55805ddf9c`
- Fixing commit: `7895ad4f655325141e55a3ec9fae87dab3d9014f`
- Affected file: `rand_core/src/block.rs`

## Expected finding

> BlockRng::next_u64 reads a u64 via `unsafe { *(&results[index] as *const u32 as *const u64) }` — a chained cast from a u32-aligned reference through `*const u32` to `*const u64` followed by dereference. This violates u64 alignment (4-byte vs 8-byte) and uses a u32-bounded provenance to access 8 bytes.

## Fix kind

`unknown`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rand-core-rustsec-2019-0035`.
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
