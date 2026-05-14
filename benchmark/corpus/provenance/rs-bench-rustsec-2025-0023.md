# rs-bench-rustsec-2025-0023

**Benchmark entry**: `rs-bench-rustsec-2025-0023` (paired with `rs-bench-rustsec-2025-0023-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2025-0023` — https://rustsec.org/advisories/RUSTSEC-2025-0023.html
**Aliases**: `GHSA-rr8g-9fpq-6wmg`
**Package**: `tokio` (advisory date: 2025-04-07)
**CWE**: `CWE-362` (soundness / impl-send-sync)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/tokio-rs/tokio.git`
- Vulnerable commit (parent of fix): `9681ce2b95ae7271c041f69b9fc48912259a7ea8`
- Fixing commit: `4b174ce2c95fe1d1a217917db93fcc935e17e0da`
- Resolution method: `manual-git-log-v8-corrected`
- Affected file: `tokio/src/sync/broadcast.rs`

## Files changed by fix

- `tokio/src/sync/broadcast.rs`

## Expected finding

> tokio::sync::broadcast clone() called on stored value without Sync bound — receivers can clone in parallel, racing on !Sync interior state

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption']
Advisory keywords: []
Informational flag: `unsound`

NOT previously used by Ward authors during rule development.
No corresponding entry existed in `tests/cve-registry/manifest.toml` prior to this benchmark.

## Methodology conformance

- [x] Source advisory in RUSTSEC (§3 inclusion 1)
- [x] In-scope vuln class (CWE deciding signal; §3 inclusion 2)
- [x] Public, identifiable fix commit (§3 inclusion 3)
- [x] Vulnerable commit identifiable (parent of fix; §3 inclusion 4)
- [x] Repository public, alive, clonable (§3 inclusion 5)
- [x] License permits redistribution (§3 inclusion 6)
- [x] Date ≥ 2024-01-01 (novel-augment window per methodology §3)
- [x] NOT in Ward's existing manifest (novel constraint per methodology §3)
