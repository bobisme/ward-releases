# rs-bench-rustsec-2025-0005

**Benchmark entry**: `rs-bench-rustsec-2025-0005` (paired with `rs-bench-rustsec-2025-0005-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2025-0005` — https://rustsec.org/advisories/RUSTSEC-2025-0005.html
**CWE**: `CWE-191` (memory_safety / unclassified)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/mozilla/grcov.git`
- Vulnerable commit: `9d7b882be80f666b22da956697a26579dd884b34`
- Fixing commit: `c8219563bc91615dd4a27884a5c63f09db8d03bb`
- Affected file: `src/covdir.rs`

## Expected finding

> grcov get_coverage panics on malformed covdir input due to integer-arithmetic overflow during percentage compute — DoS, not a memory-safety UB residual at any unsafe sink

## Fix kind

`arithmetic_validation`

## License verification

- License: **MPL-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2025-0005`.
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
