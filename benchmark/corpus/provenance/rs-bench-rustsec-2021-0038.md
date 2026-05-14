# rs-bench-rustsec-2021-0038

**Benchmark entry**: `rs-bench-rustsec-2021-0038` (paired with `rs-bench-rustsec-2021-0038-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0038` — https://rustsec.org/advisories/RUSTSEC-2021-0038.html
**CVE ID**: `CVE-2021-28306`
**CWE**: `CWE-476` (memory_safety / ffi-boundary-contract)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/fltk-rs/fltk-rs.git`
- Vulnerable commit: `f067beed0e54888125e0c81bc5de15e4e931dc75`
- Fixing commit: `1b2e6bdbd93df1f673f5c57cf6dda625e36b4810`
- Affected file: `fltk/src/prelude.rs`

## Expected finding

> set_label_type / set_icon / Pixmap::new pass Rust pointers to FLTK C++ without null-check — null-deref and lifetime mismatch at the FFI boundary

## Fix kind

`ffi_null`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0038`.
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
