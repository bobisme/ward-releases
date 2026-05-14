# rs-bench-rustsec-2026-0041

**Benchmark entry**: `rs-bench-rustsec-2026-0041` (paired with `rs-bench-rustsec-2026-0041-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2026-0041` — https://rustsec.org/advisories/RUSTSEC-2026-0041.html
**CVE ID**: `CVE-2026-32829`
**Aliases**: `CVE-2026-32829`, `GHSA-vvp9-7p8x-rfvv`
**Package**: `lz4_flex` (advisory date: 2026-03-17)
**CWE**: `CWE-908` (memory_safety / set-len-init)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/PSeitz/lz4_flex.git`
- Vulnerable commit (parent of fix): `7191df8231f2be4daa70c9171ed1c1521123efe5`
- Fixing commit: `055502ee5d297ecd6bf448ac91c055c7f6df9b6d`
- Resolution method: `manual-git-log-v7`
- Affected file: `fuzz/fuzz_targets/fuzz_decomp_corrupt_block.rs`

## Files changed by fix

- `.github/workflows/rust.yml`
- `README.md`
- `fuzz/Cargo.toml`
- `fuzz/fuzz_targets/fuzz_decomp_corrupt_block.rs`
- `fuzz/fuzz_targets/fuzz_decomp_no_output_leak.rs`
- `src/block/decompress.rs`
- `src/block/decompress_safe.rs`
- `src/block/mod.rs`
- `src/sink.rs`

## Expected finding

> lz4_flex decompress_into / decompress with invalid LZ4 match offsets reads from uninitialized output buffer — info disclosure

## License verification

- License: **MIT**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-exposure']
Advisory keywords: ['lz4', 'decompression', 'information-disclosure', 'uninitialized-memory']
Informational flag: `None`

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
