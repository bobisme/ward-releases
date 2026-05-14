# rs-bench-rustsec-2021-0036

**Benchmark entry**: `rs-bench-rustsec-2021-0036` (paired with `rs-bench-rustsec-2021-0036-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0036` — https://rustsec.org/advisories/RUSTSEC-2021-0036.html
**CVE ID**: `CVE-2021-28037`
**CWE**: `CWE-362` (memory_safety / impl-send-sync)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/droundy/internment.git`
- Vulnerable commit: `863dbc0653cb8b265b3b969d94b4bdaa50fd4a03`
- Fixing commit: `2928a87a0c9f86c46ba70f8c8058d9b7b10a241d`
- Affected file: `src/lib.rs`

## Expected finding

> unsafe impl<T> Send/Sync for ArcIntern<T> without T: Send/Sync bound; cross-thread move of ArcIntern<Cell<T>> permits data race

## Fix kind

`send_sync_bound`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0036`.
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
