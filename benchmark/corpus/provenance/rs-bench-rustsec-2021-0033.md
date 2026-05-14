# rs-bench-rustsec-2021-0033

**Benchmark entry**: `rs-bench-rustsec-2021-0033` (paired with `rs-bench-rustsec-2021-0033-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0033` — https://rustsec.org/advisories/RUSTSEC-2021-0033.html
**CVE ID**: `CVE-2021-28034`
**CWE**: `CWE-415` (memory_safety / panic-sequence)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/thepowersgang/stack_dst-rs.git`
- Vulnerable commit: `807e9d45019c02369e11d40bd181cbf7bb7981fc`
- Fixing commit: `2a4d53809e3000f40085f2b229b6b1a33759881d`
- Affected file: `src/stack.rs`

## Expected finding

> StackA::push_cloned writes T via Clone before bumping len; if Clone panics, partially-written byte range is double-dropped — drop-ordering bug

## Fix kind

`panic_safety`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0033`.
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
