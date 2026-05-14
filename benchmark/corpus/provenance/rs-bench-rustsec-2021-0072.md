# rs-bench-rustsec-2021-0072

**Benchmark entry**: `rs-bench-rustsec-2021-0072` (paired with `rs-bench-rustsec-2021-0072-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0072` — https://rustsec.org/advisories/RUSTSEC-2021-0072.html
**CVE ID**: `CVE-2021-38191`
**CWE**: `CWE-362` (memory_safety / impl-send-sync)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/tokio-rs/tokio.git`
- Vulnerable commit: `a5ee2f0d3d78daa01e2c6c12d22b82474dc5c32a`
- Fixing commit: `84394949228d11d1f68925e26f36c435946b9d11`
- Affected file: `tokio/src/runtime/task/mod.rs`

## Expected finding

> JoinHandle::abort racing concurrent abort calls dropped task-output ManuallyDrop twice — race condition on task termination causes double-free

## Fix kind

`abort_race`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0072`.
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
