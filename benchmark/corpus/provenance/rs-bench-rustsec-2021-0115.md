# rs-bench-rustsec-2021-0115

**Benchmark entry**: `rs-bench-rustsec-2021-0115` (paired with `rs-bench-rustsec-2021-0115-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0115` — https://rustsec.org/advisories/RUSTSEC-2021-0115.html
**CVE ID**: `CVE-2021-45706`
**CWE**: `CWE-459` (memory_safety / unclassified)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/iqlusioninc/crates.git`
- Vulnerable commit: `6d9b2242b31a2756b68d9f7bb17dcfd7ec0edfa2`
- Fixing commit: `9376851591e3701df192f88c277b0998b9a3132f`
- Affected file: `derive/src/lib.rs`

## Expected finding

> zeroize_derive #[zeroize(drop)] proc-macro generated Drop impl for enums failed to actually call drop_in_place on inner fields — secrets persisted in memory after zeroize. Bug is derive-macro logic, outside the 14 unsafe shapes

## Fix kind

`derive_macro_drop`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0115`.
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
