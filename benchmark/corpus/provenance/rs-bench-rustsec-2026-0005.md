# rs-bench-rustsec-2026-0005

**Benchmark entry**: `rs-bench-rustsec-2026-0005` (paired with `rs-bench-rustsec-2026-0005-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0005` — https://rustsec.org/advisories/RUSTSEC-2026-0005.html
**Aliases**: `GHSA-rvr2-r3pv-5m4p`
**Package**: `oneshot` (advisory date: 2026-01-25)
**CWE**: `CWE-362` (soundness / impl-send-sync)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/faern/oneshot.git`
- Vulnerable commit (parent of fix): `ee1d1ac4f4d6b991fde02bd5a60b4a95da090be8`
- Fixing commit: `d1a1506010bc48962634807d0dcca682af4f50ba`
- Resolution method: `pr-74`
- Affected file: `src/lib.rs`

## Files changed by fix

- `CHANGELOG.md`
- `src/lib.rs`

## Expected finding

> oneshot Sender/Receiver Send/Sync bounds incorrect for !Send T — sending non-Send value across thread boundary, soundness break

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
Advisory keywords: ['memory-safety', 'use-after-free']
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
