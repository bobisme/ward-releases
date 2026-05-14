# rs-bench-rustsec-2023-0030

**Benchmark entry**: `rs-bench-rustsec-2023-0030` (paired with `rs-bench-rustsec-2023-0030-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2023-0030` — https://rustsec.org/advisories/RUSTSEC-2023-0030.html
**CVE ID**: `CVE-2023-28448`
**CWE**: `CWE-125` (type_confusion / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/firecracker-microvm/versionize.git`
- Vulnerable commit: `732eb8177925113639af989bac78c2a5395ebacf`
- Fixing commit: `fffee7077153224edeabc0f5eaa347a646b6c1ee`
- Affected file: `src/primitives/string.rs`

## Expected finding

> versionize FamStructWrapper::deserialize reads a length-prefixed flexible-array-member without bounds-checking — backing buffer is reused as if initialized for the attacker-supplied length

## Fix kind

`bounds_check`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2023-0030`.
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
