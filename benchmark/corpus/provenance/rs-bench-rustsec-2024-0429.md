# rs-bench-rustsec-2024-0429

**Benchmark entry**: `rs-bench-rustsec-2024-0429` (paired with `rs-bench-rustsec-2024-0429-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0429` — https://rustsec.org/advisories/RUSTSEC-2024-0429.html
**Aliases**: `GHSA-wrw7-89jp-8q8g`
**Package**: `glib` (advisory date: 2024-03-30)
**CWE**: `CWE-416` (memory_safety / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/gtk-rs/gtk-rs-core.git`
- Vulnerable commit (parent of fix): `e24f5fcf05b4d78afca97a2b325f3e70cf7cac72`
- Fixing commit: `05dff0ee696f9bcd8617cd48c4b812d046d440cb`
- Resolution method: `pr-1343`
- Affected file: `glib/src/variant_iter.rs`

## Files changed by fix

- `glib/src/variant_iter.rs`

## Expected finding

> glib::VariantIter clone iterates Variant memory after underlying ref is freed — UAF on iter clone

## License verification

- License: **MIT**
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
