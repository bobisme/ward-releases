# rs-bench-rustsec-2021-0124

**Benchmark entry**: `rs-bench-rustsec-2021-0124` (paired with `rs-bench-rustsec-2021-0124-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0124` — https://rustsec.org/advisories/RUSTSEC-2021-0124.html
**CVE ID**: `CVE-2021-45710`
**CWE**: `CWE-362` (memory_safety / impl-send-sync)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/tokio-rs/tokio.git`
- Vulnerable commit: `ccf855ec24db7e91af7d60d4524dcd44d25d98c2`
- Fixing commit: `844dc9be2f95e2403dc50562333090af7d2d20a5`
- Affected file: `tokio/src/sync/oneshot.rs`

## Expected finding

> oneshot::Receiver::close racy UnsafeCell access against Sender::send via the value slot; race condition on close vs send corrupts the slot — implicit Send/Sync contract violated

## Fix kind

`send_sync_race`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0124`.
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
