# rs-bench-rustsec-2025-0020

**Benchmark entry**: `rs-bench-rustsec-2025-0020` (paired with `rs-bench-rustsec-2025-0020-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2025-0020` — https://rustsec.org/advisories/RUSTSEC-2025-0020.html
**CWE**: `CWE-119` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/PyO3/pyo3.git`
- Vulnerable commit: `4aca459fd30441fa006c3eb388c812047f5465ce`
- Fixing commit: `5caaa371dce8fe8a93c64d7a465c3c2c80ce6e2f`
- Affected file: `src/types/string.rs`

## Expected finding

> PyString::from_object / from_object_bound returns &PyString backed by a CPython buffer whose lifetime can be invalidated by the Python interpreter — safe API exposes a reference to memory it does not own

## Fix kind

`lifetime_extension`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2025-0020`.
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
