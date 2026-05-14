# rs-bench-rustsec-2022-0102

**Benchmark entry**: `rs-bench-rustsec-2022-0102` (paired with `rs-bench-rustsec-2022-0102-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2022-0102` — https://rustsec.org/advisories/RUSTSEC-2022-0102.html
**CVE ID**: `CVE-2022-39392`
**CWE**: `CWE-125` (type_confusion / layout-cast)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/bytecodealliance/wasmtime.git`
- Vulnerable commit: `2614f2e9d2d36805ead8a8da0fa0c6e0d9e428a0`
- Fixing commit: `e60c3742904ccbb3e26da201c9221c38a4981d72`
- Affected file: `crates/runtime/src/instance.rs`

## Expected finding

> wasmtime memory image reuse: a memory slot is reused between a module with an image and one without — layout assumption that slot was zero-initialized is violated, OOB-read of stale image bytes

## Fix kind

`memory_image_reuse`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2022-0102`.
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
