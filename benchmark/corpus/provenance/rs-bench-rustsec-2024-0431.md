# rs-bench-rustsec-2024-0431

**Benchmark entry**: `rs-bench-rustsec-2024-0431` (paired with `rs-bench-rustsec-2024-0431-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0431` — https://rustsec.org/advisories/RUSTSEC-2024-0431.html
**Aliases**: `GHSA-gv7f-5qqh-vxfx`
**Package**: `xous` (advisory date: 2024-12-23)
**CWE**: `CWE-119` (soundness / safe-encap)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/betrusted-io/xous-core.git`
- Vulnerable commit (parent of fix): `f17ce555f7539b534b910fe832d273afe5ad27fc`
- Fixing commit: `5dfad296ae9bdcaf623aa7997b58bf25f54a622b`
- Resolution method: `manual-git-log-v5`
- Affected file: `apps/transientdisk/src/flash_drive.rs`

## Files changed by fix

- `apps/transientdisk/src/flash_drive.rs`
- `kernel/src/services.rs`
- `services/dns/src/main.rs`
- `services/early_settings/src/main.rs`
- `services/graphics-server/src/backend/betrusted.rs`
- `services/graphics-server/src/main.rs`
- `services/net/src/main.rs`
- `services/net/src/std_glue.rs`
- `services/net/src/std_tcplistener.rs`
- `services/net/src/std_tcpstream.rs`
- … and 14 more

## Expected finding

> xous MemoryRange::as_slice / as_slice_mut were safe but constructed slices from arbitrary pointer/length pairs via core::slice::from_raw_parts — unsound

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: []
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
