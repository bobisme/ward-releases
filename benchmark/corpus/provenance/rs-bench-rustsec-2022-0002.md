# rs-bench-rustsec-2022-0002

**Benchmark entry**: `rs-bench-rustsec-2022-0002` (paired with `rs-bench-rustsec-2022-0002-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2022-0002` — https://rustsec.org/advisories/RUSTSEC-2022-0002.html
**CWE**: `CWE-416` (memory_safety / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/xacrimon/dashmap.git`
- Vulnerable commit: `f4daed99a1d19e036db06a82aaf222fbd4d64953`
- Fixing commit: `fbb6ffb1d70ae520889062728476d7d607c9309e`
- Affected file: `src/mapref/multiple.rs`

## Expected finding

> RefMulti::key / value / pair hand out &K / &V whose lifetime is tied to the iterator, but the safe API allows iterator advance that releases the underlying shard read-lock — UAF when shard is mutated

## Fix kind

`lifetime_extension`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2022-0002`.
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
