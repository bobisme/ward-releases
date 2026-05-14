# rs-bench-rustsec-2021-0031

**Benchmark entry**: `rs-bench-rustsec-2021-0031` (paired with `rs-bench-rustsec-2021-0031-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2021-0031` — https://rustsec.org/advisories/RUSTSEC-2021-0031.html
**CVE ID**: `CVE-2021-28032`
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: critical

## Commit pinning

- Repository: `https://github.com/bennetthardwick/nano-arena.git`
- Vulnerable commit: `f5306c73a0f8f260eb49f9f0a8509ef85f038244`
- Fixing commit: `6b83f9d0708337a9f8b709c1624a8587021ceba2`
- Affected file: `src/lib.rs`

## Expected finding

> Arena::split_at / ArenaSplit::split_at hand out two &mut references aliased to the same underlying allocation — safe API permits creating two mutable borrows where the type-level borrow tracking is bypassed

## Fix kind

`aliasing_split`

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2021-0031`.
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
