# rs-bench-beef-rustsec-2020-0122

**Benchmark entry**: `rs-bench-beef-rustsec-2020-0122` (paired with `rs-bench-beef-rustsec-2020-0122-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2020-0122` — https://rustsec.org/advisories/RUSTSEC-2020-0122.html
**CVE ID**: `CVE-2020-36442`
**CWE**: `CWE-362` (memory_safety / impl-send-sync)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/maciejhirsz/beef.git`
- Vulnerable commit: `0b4685143e680749991c295836d8d09565fd6814`
- Fixing commit: `8e970aaa60471a845a309c0fe82ebe59779341ca`
- Affected file: `src/generic.rs`

## Expected finding

> `unsafe impl<T: Beef + Send + ?Sized, U: Capacity> Send for Cow<'_, T, U>` requires only T: Send, but Cow holds a shared reference into T's storage. Without T: Sync, `Send + !Sync` types (e.g. Cell<_>, RefCell<_>) can be sent across threads → data race on interior-mutable cells → memory corruption.

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-beef-rustsec-2020-0122`.
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
