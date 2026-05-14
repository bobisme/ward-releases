# rs-bench-rustsec-2021-0050

**Benchmark entry**: `rs-bench-rustsec-2021-0050` (paired with `rs-bench-rustsec-2021-0050-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0050` — https://rustsec.org/advisories/RUSTSEC-2021-0050.html
**CVE ID**: `CVE-2021-29941`
**CWE**: `CWE-787` (memory_safety / slice-from-raw-parts-init-violation)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/tiby312/reorder.git`
- Vulnerable commit: `5a7aa092eaf9de87300e6c5b25a2df953d60ee90`
- Fixing commit: `8b0eba0b117b82abe4c24c05188b4d30ba4d461e`
- Affected file: `src/lib.rs`

## Expected finding

> reorder swap_unchecked uses ptr::swap_nonoverlapping with hand-rolled length but does not check overlap — OOB-write when indices overlap

## Fix kind

`bounds_validation`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0050`.
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
