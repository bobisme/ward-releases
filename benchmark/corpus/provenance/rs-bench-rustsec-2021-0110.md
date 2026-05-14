# rs-bench-rustsec-2021-0110

**Benchmark entry**: `rs-bench-rustsec-2021-0110` (paired with `rs-bench-rustsec-2021-0110-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0110` — https://rustsec.org/advisories/RUSTSEC-2021-0110.html
**CVE ID**: `CVE-2021-39216`
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/bytecodealliance/wasmtime.git`
- Vulnerable commit: `e56312e61a71f90c3d7fe9edbe817ec9a7584f4f`
- Fixing commit: `101998733b74624cbd348a2366d05760b40181f3`
- Affected file: `crates/runtime/src/externref.rs`

## Expected finding

> wasmtime ExternRef GC walks Linker-rooted func references; func_wrap / func_new return externref handles whose lifetime is not tied to the Store — Store::gc may free a reference still held by safe code

## Fix kind

`gc_lifetime`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0110`.
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
