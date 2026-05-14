# rs-bench-borsh-rustsec-2023-0033

**Benchmark entry**: `rs-bench-borsh-rustsec-2023-0033` (paired with `rs-bench-borsh-rustsec-2023-0033-fix`)
**Source**: `manual_curation` per methodology §3.
**Advisory**: `RUSTSEC-2023-0033` — https://rustsec.org/advisories/RUSTSEC-2023-0033.html
**CWE**: `CWE-908` (memory_safety / zst-ptr-arith)
**Severity**: medium

## Commit pinning

- Repository: `https://github.com/near/borsh-rs.git`
- Vulnerable commit: `e564c4bcff28cefc4bd14a1b14bb911040f92a13`
- Fixing commit: `e880d8786cb16aa9a3f258e7503932445d708df7`
- Affected file: `borsh/src/de/mod.rs`

## Expected finding

> Vec<T>::deserialize_reader for non-Copy ZST T deserializes the element ONCE then calls `Vec::from_raw_parts(p, len, len)` after `forget(result)` — produces a Vec of len elements all at the same ZST address. Drop iterates len times invoking T::drop on the same byte → double-free / segfault on non-trivial Drop impls.

## Fix kind

`unknown`

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Inherited from Ward's `tests/cve-registry/manifest.toml` entry `rs-borsh-rustsec-2023-0033`.
Selected for this benchmark because the source RUSTSEC advisory falls in the
manually-curated memory-safety category (one of `memory-corruption`, `memory-exposure`,
`thread-safety`, `format-injection`, or marked `informational = "unsound"`) —
third-party gating filter (b) per methodology §3.

## Methodology conformance

- [x] Source advisory in RUSTSEC or GHSA-cargo (§3 inclusion 1)
- [x] In-scope vuln class (CWE deciding signal; §3 inclusion 2)
- [x] Public, identifiable fix commit (§3 inclusion 3)
- [x] Vulnerable commit identifiable (§3 inclusion 4)
- [x] Repository public, alive, clonable (§3 inclusion 5)
- [x] License permits redistribution (§3 inclusion 6)
