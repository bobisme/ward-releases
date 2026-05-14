# rs-bench-rustsec-2023-0044

**Benchmark entry**: `rs-bench-rustsec-2023-0044` (paired with `rs-bench-rustsec-2023-0044-fix`)
**Source**: `rustxec_msr_2026` per methodology §3.
**Advisory**: `RUSTSEC-2023-0044` — https://rustsec.org/advisories/RUSTSEC-2023-0044.html
**CWE**: `CWE-126` (type_confusion / ffi-boundary-contract)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/sfackler/rust-openssl.git`
- Vulnerable commit: `8e16a8b6e28e32cedaa9eed814ba994a8c89b5e4`
- Fixing commit: `155b3dc71700d2ff31651bbc99b991765a718c4e`
- Affected file: `openssl/src/x509/verify.rs`

## Expected finding

> X509VerifyParamRef::set_host accepts host slice without enforcing OpenSSL-required lifetime/null-termination — FFI passes Rust slice ptr/len to OpenSSL which may read past the slice end

## Fix kind

`ffi_contract`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Phase 5 (Miri witness gate) eligibility

`phase5_eligible = true`. This entry has a runnable Miri witness fixture in Ward's 
witness gate (`crates/ward-eval/src/phase5_witness_gate.rs`). Miri witness rate is 
reported as a Ward-only axis (methodology §6); other tools are not scored on this axis.

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-rustxec-rustsec-2023-0044`.
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
