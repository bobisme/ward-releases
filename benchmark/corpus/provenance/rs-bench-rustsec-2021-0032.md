# rs-bench-rustsec-2021-0032

**Benchmark entry**: `rs-bench-rustsec-2021-0032` (paired with `rs-bench-rustsec-2021-0032-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0032` — https://rustsec.org/advisories/RUSTSEC-2021-0032.html
**CVE ID**: `CVE-2021-28033`
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/wwylele/byte-struct-rs.git`
- Vulnerable commit: `9c41996e55bc91557edd6fa6f6a1c07a48c55731`
- Fixing commit: `a535678377de12bc6bc22620c5f59bcc1369f76f`
- Affected file: `src/lib.rs`

## Expected finding

> byte_struct read_bytes returns &[u8] over uninitialized bytes when struct definition mismatches actual byte length — uninit memory exposed as initialized

## Fix kind

`init_validation`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0032`.
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
