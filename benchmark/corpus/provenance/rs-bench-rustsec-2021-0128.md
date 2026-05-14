# rs-bench-rustsec-2021-0128

**Benchmark entry**: `rs-bench-rustsec-2021-0128` (paired with `rs-bench-rustsec-2021-0128-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0128` — https://rustsec.org/advisories/RUSTSEC-2021-0128.html
**CVE ID**: `CVE-2021-45713`
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/rusqlite/rusqlite.git`
- Vulnerable commit: `d70fbac2314333ecf2e67db43dbb43b0a47a4797`
- Fixing commit: `426056c0924291367c9cee1fd2ecc4554da06e96`
- Affected file: `src/functions.rs`

## Expected finding

> create_scalar_function / create_aggregate_function / create_window_function leak the user-provided closure into SQLite without binding its drop to the Connection — Connection drop double-frees the closure or runs while still in use

## Fix kind

`closure_lifetime`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0128`.
Imported into Ward's manifest via bn-jth16 (2026-05-01); see 
`notes/rustxec-import-2026-05-01.md` for the RustXec MSR'26 mapping methodology.
Selected for this benchmark because it appears in the RustXec MSR'26 published
academic memory-safety dataset (third-party gating filter (a) per methodology §3).

## Methodology conformance

- [x] Source advisory in RUSTSEC or GHSA-cargo (§3 inclusion 1)
- [x] In-scope vuln class (CWE deciding signal; §3 inclusion 2)
- [x] Public, identifiable fix commit (§3 inclusion 3)
- [x] Vulnerable commit identifiable (§3 inclusion 4)
- [x] Repository public, alive, clonable (§3 inclusion 5)
- [x] License permits redistribution (§3 inclusion 6)
