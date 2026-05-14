# rs-bench-rustsec-2021-0122

**Benchmark entry**: `rs-bench-rustsec-2021-0122` (paired with `rs-bench-rustsec-2021-0122-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0122` — https://rustsec.org/advisories/RUSTSEC-2021-0122.html
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/google/flatbuffers.git`
- Vulnerable commit: `f124e41ae62ae548e045dadb26b6ad172bf8020b`
- Fixing commit: `f0547f7b73aa240ef84232c177c504928f86daa2`
- Affected file: `rust/flatbuffers/src/follow.rs`

## Expected finding

> flatbuffers verifier accepted offsets pointing into uninitialized buffer regions — SET-LEN-INIT analog where the verifier returned safely on uninit ranges

## Fix kind

`verifier_init`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0122`.
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
