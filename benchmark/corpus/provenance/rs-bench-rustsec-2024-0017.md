# rs-bench-rustsec-2024-0017

**Benchmark entry**: `rs-bench-rustsec-2024-0017` (paired with `rs-bench-rustsec-2024-0017-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0017` — https://rustsec.org/advisories/RUSTSEC-2024-0017.html
**CVE ID**: `CVE-2024-27284`
**Aliases**: `CVE-2024-27284`, `GHSA-x9xc-63hg-vcfq`
**Package**: `cassandra-cpp` (advisory date: 2024-02-28)
**CWE**: `CWE-416` (use_after_free / safe-encap)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/Metaswitch/cassandra-rs.git`
- Vulnerable commit (parent of fix): `9698afb9131cab8be1ef0550ca380008962d308c`
- Fixing commit: `299e6ac50f87eb2823a373baec37b590a74994ee`
- Resolution method: `manual-git-log-v5`
- Affected file: `examples/collections.rs`

## Files changed by fix

- `CHANGELOG.md`
- `Cargo.toml`
- `README.md`
- `examples/collections.rs`
- `examples/simple.rs`
- `examples/ssl.rs`
- `src/cassandra/batch.rs`
- `src/cassandra/cluster.rs`
- `src/cassandra/collection.rs`
- `src/cassandra/consistency.rs`
- … and 36 more

## Expected finding

> cassandra-rs ResultIterator: code using item returned by next() after iterator advances accesses freed C++ memory — UAF

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['memory-corruption', 'memory-exposure']
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
