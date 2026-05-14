# rs-bench-rustsec-2021-0030

**Benchmark entry**: `rs-bench-rustsec-2021-0030` (paired with `rs-bench-rustsec-2021-0030-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0030` — https://rustsec.org/advisories/RUSTSEC-2021-0030.html
**CVE ID**: `CVE-2021-28031`
**CWE**: `CWE-415` (memory_safety / panic-sequence)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/okready/scratchpad.git`
- Vulnerable commit: `0cc776fb47e5339259675eca5548dc524aa7c550`
- Fixing commit: `18abedadaa77646cce6f2ca2149c0119a2e4f428`
- Affected file: `src/lib.rs`

## Expected finding

> SliceMoveSource trait impls for arrays and boxed slices do not inhibit dropping of source elements; if the consume-closure panics, source elements are double-dropped

## Fix kind

`panic_safety`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0030`.
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
