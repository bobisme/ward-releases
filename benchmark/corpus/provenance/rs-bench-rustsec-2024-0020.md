# rs-bench-rustsec-2024-0020

**Benchmark entry**: `rs-bench-rustsec-2024-0020` (paired with `rs-bench-rustsec-2024-0020-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0020` — https://rustsec.org/advisories/RUSTSEC-2024-0020.html
**Aliases**: `GHSA-w5w5-8vfh-xcjq`
**Package**: `whoami` (advisory date: 2024-02-28)
**CWE**: `CWE-787` (memory_safety / ffi-boundary-contract)
**Severity**: high

## Commit pinning

- Repository: `https://github.com/ardaku/whoami.git`
- Vulnerable commit (parent of fix): `953e702c0b24789a359a4027818af53bcb979db6`
- Fixing commit: `d6ee13ed9e818aa51b8d86d95e8009a376289a40`
- Resolution method: `manual-git-log-v2`
- Affected file: `src/os/unix.rs`

## Files changed by fix

- `TESTING.md`
- `src/os/unix.rs`

## Expected finding

> whoami username/realname on illumos/Solaris uses fixed-size stack buffer that overflows on long names — stack BOF

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['denial-of-service', 'memory-corruption']
Advisory keywords: ['buffer-overflow', 'stack-buffer-overflow', 'cwe-121']
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
