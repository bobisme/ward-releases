# rs-bench-rustsec-2022-0098

**Benchmark entry**: `rs-bench-rustsec-2022-0098` (paired with `rs-bench-rustsec-2022-0098-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2022-0098` — https://rustsec.org/advisories/RUSTSEC-2022-0098.html
**CVE ID**: `CVE-2022-39393`
**CWE**: `CWE-212` (memory_safety / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/bytecodealliance/wasmtime.git`
- Vulnerable commit: `96ae44ac8f1b4bad04df5c77c4dcb248cfdec670`
- Fixing commit: `2614f2e9d2d36805ead8a8da0fa0c6e0d9e428a0`
- Affected file: `crates/runtime/src/instance.rs`

## Expected finding

> wasmtime cross-Store memory reuse: a memory slot is reused between a module with a memory image and one without — safe API exposes stale image bytes when slot is recycled

## Fix kind

`memory_slot_reuse`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2022-0098`.
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
