# rs-bench-rustsec-2024-0354

**Benchmark entry**: `rs-bench-rustsec-2024-0354` (paired with `rs-bench-rustsec-2024-0354-fix`)
**Source**: `rustsec_2024_2026` (novel augmentation per methodology §3)
**Advisory**: `RUSTSEC-2024-0354` — https://rustsec.org/advisories/RUSTSEC-2024-0354.html
**CVE ID**: `CVE-2024-40640`
**Aliases**: `CVE-2024-40640`, `GHSA-j8cm-g7r6-hfpq`
**Package**: `vodozemac` (advisory date: 2024-07-17)
**CWE**: `CWE-200` (memory_safety / safe-encap)
**Severity**: low

## Commit pinning

- Repository: `https://github.com/matrix-org/vodozemac.git`
- Vulnerable commit (parent of fix): `3e9866b81d4454981a609da3e7531ace44da1568`
- Fixing commit: `5e65c1b29eb085b4805fa5fcdd5072052bf16cb6`
- Resolution method: `manual-git-log-v4`
- Affected file: `src/cipher/key.rs`

## Files changed by fix

- `src/cipher/key.rs`
- `src/megolm/group_session.rs`
- `src/megolm/inbound_group_session.rs`
- `src/megolm/mod.rs`
- `src/megolm/ratchet.rs`
- `src/olm/account/mod.rs`
- `src/olm/session/chain_key.rs`
- `src/olm/session/mod.rs`
- `src/olm/session/root_key.rs`
- `src/olm/shared_secret.rs`
- … and 1 more

## Expected finding

> vodozemac AccountPickle/SessionPickle keep private key copies past lifetime — memory exposure (cleartext key in heap after free)

## License verification

- License: **Apache-2.0**
- Permits redistribution: yes (permissive license)
- Source redistribution: corpus stores SHAs and metadata only; source repos fetched at scan time from upstream

## Source provenance

Newly collected from RUSTSEC advisory-db (commit pinned at corpus-collection time).
Advisory categories: ['crypto-failure', 'memory-exposure']
Advisory keywords: []
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
