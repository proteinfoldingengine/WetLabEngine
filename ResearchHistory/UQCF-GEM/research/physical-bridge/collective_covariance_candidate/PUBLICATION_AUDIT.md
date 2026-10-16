# Independent publication audit: collective-covariance candidate

**Verdict: PASS — immutable publication integrity only. No publication blocker remains.**

Audit date: 2026-10-16 UTC. The auditor is separate from the candidate author and the independent mathematical reviewer. The audit binds the seven-file scientific commit below. It does not audit a future receipt commit or future branch head.

| Binding | Exact identity |
| --- | --- |
| Repository | `proteinfoldingengine/WetLabEngine` |
| Source parent, and sole parent of scientific commit | `0583236e036fc9bfad2481721be6cfc4dd9a4cf3` |
| Source tree | `2203341fc5437bd400b5289324bfad6115e62029` |
| Scientific commit | `64c2ac3c0957b743201977df0a2a7054cd8bec20` |
| Scientific tree | `91f5bdaa82e42d87fc3d65cfea197156a716458a` |
| Frozen bundle SHA-256 | `ae25f677448aa1fba7df54c5da1d4b460a347dbd5425b5d9d2b88e7c08f4a851` |

The [scientific commit](https://github.com/proteinfoldingengine/WetLabEngine/commit/64c2ac3c0957b743201977df0a2a7054cd8bec20) was retrieved directly through the GitHub connector. Its Git commit metadata gives exactly the stated tree and sole parent. The research branch was observed at the source parent during Stage 1 and at the scientific commit during Stage 2. These are point-in-time observations; the immutable commit is the audit target.

## Original-source authentication

All 11 original files named by the published `source_identities.json` were independently retrieved at the immutable source parent using base64 transport. Decoded originals equal the published packet contents byte for byte. Every byte length, SHA-256, computed Git blob identity, connector blob identity, immutable source URL, and source-parent tree membership agrees. Path sets are exactly equal, with no duplicate or omitted source.

The published `source_packet.json` and `source_identities.json` have exactly the Stage 1 audited identities, binding the independent original-source audit to the final publication. The packet is 186,446 bytes, SHA-256 `c51f7dafd232c38e8426b3abaa472bb7f474d6585cf974b1d069a3ed6774c7dd`; the identity file is 5,399 bytes, SHA-256 `330c4a81b1d6500a27168489cc309120725d37e2b4fa6bcfd16d181f72e4f059`.

Fifteen complete ancestor trees establish all source paths. Root and `ResearchHistory` contain no `AGENTS.md`; no deeper applicable source or publication ancestor introduces one. The sole applicable file is the unchanged `ResearchHistory/UQCF-GEM/AGENTS.md`, blob `e5407215a81b914fc02f5c107333a2f0261634ee`. Its full original was read. Its numbered-stage closure requirements remain in force where applicable and are not satisfied or overridden by this bounded analytical publication audit.

## Published bytes and review bindings

Each of the seven files was independently downloaded at the exact scientific commit and compared in full with the frozen bundle. All lengths, SHA-256 values, independently computed Git blob hashes, connector blob hashes, and scientific-tree entries agree.

Paths in this table are relative to `ResearchHistory/UQCF-GEM/research/physical-bridge/collective_covariance_candidate/`.

| Published file | Bytes | SHA-256 | Git blob |
| --- | ---: | --- | --- |
| `RESULT.md` | 16341 | `5b58822c309013cfb6c07b528a3dafc8360f15d3c587a2fb52143ec04f4b3eb7` | `65bbcbe3fdb88edf390f42bba16ed77dc90debcc` |
| `INDEX_APPEND.md` | 2004 | `ca85e0ea7dc98ba062b9a80a72426ffbcb8ee2909aacd038f608abde6e6a4a06` | `94af75024c16493b379487e6e36ffa4a53bca80d` |
| `source_packet.json` | 186446 | `c51f7dafd232c38e8426b3abaa472bb7f474d6585cf974b1d069a3ed6774c7dd` | `e522bfda7fc6cfe2d67ebb196cd0c9823378926a` |
| `source_identities.json` | 5399 | `330c4a81b1d6500a27168489cc309120725d37e2b4fa6bcfd16d181f72e4f059` | `38a9b29e1d2a55c73e6758aca2c5b04aaff5a942` |
| `ANALYTICAL_REVIEW_RAW.md` | 15548 | `8712d2da5f3456fc044b189619d53708be7b2314fca979375b141b4254aacbe7` | `c6e9c27596297411e83ae41dcf2d9c848c8c0f2d` |
| `../COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` | 80735 | `b84333a11d1a79fddb79b430d6b750a20291ad10b9cb87717a2f211931e75c3a` | `02e20ebfb77bd967721261fec4edcadd8bb11313` |
| `PUBLICATION_MANIFEST.json` | 2180 | `d7e90ed8483d05c256099ad0159c02b4729bff3ac5640bc1fc29b73120902925` | `8654bf8517fb79b6aea8596235c295b8170c091f` |

The frozen bundle is 313,872 bytes. Reconstructing it from the retrieved published bytes with the recorded field order and serialization reproduces its exact bytes and SHA-256.

`PUBLICATION_MANIFEST.json` has exactly the six payload entries: result, append, source packet, source identities, raw analytical review, and updated continuation. All three identity fields for every entry agree. The manifest explicitly excludes itself; this audit independently binds its own bytes and blob identity.

The raw independent analytical review is preserved byte for byte against the reviewer's supplied original: 15,548 bytes, SHA-256 `8712d2da5f3456fc044b189619d53708be7b2314fca979375b141b4254aacbe7`. Its four reviewed input length/hash pairs exactly match the published result, append, source packet, and source identities. Its recorded decision has no blocking mathematical or claim-boundary defect, permits this exact candidate to proceed to publication audit, and retains the native milestone limitation. The publication auditor verifies that binding and preservation; the separate reviewer owns the mathematical judgment.

The continuation is exactly the original 78,731-byte parent content followed by the complete 2,004-byte `INDEX_APPEND.md`: 80,735 bytes total. The old prefix and entire appended suffix match separately. No earlier continuation byte changed.

## Complete change boundary

Complete non-truncated tree entries were compared from both repository roots, descending every differing tree and pruning only entries with equal mode, type, and Git identity. All 21 independently retrieved complete tree objects reproduce their Git tree hashes. Six directory pairs cover the full changed path chain.

The complete leaf change set is exactly six new files in `collective_covariance_candidate/` plus the one continuation modification. All changed files are ordinary `100644` blobs. There are no deletions, mode changes, type changes, or other repository edits. Equal untouched subtree identities carry the boundary through the rest of the repository; the result does not rely on a supplied changed-file list or a possibly truncated diff.

## Preserved failure, evidence, and limits

The initial recursive source-root tree request returned `Transport closed`. The complete error and endpoint are preserved in the evidence. Complete non-recursive ancestor retrieval replaced that request; there is no remaining source or change-boundary gap. No other GitHub retrieval failed in this audit, and there are no unresolved blockers.

[PUBLICATION_AUDIT_EVIDENCE.json](PUBLICATION_AUDIT_EVIDENCE.json) is self-contained for these checks. It embeds all 18 unique original-source and published byte objects, complete required tree entries, commit metadata, source and publication membership chains, full tree comparisons, manifest/review bindings, the continuation comparison, the failed retrieval, and the exact frozen-bundle reconstruction rule. It does not require local-only evidence files. Its identity is:

- Bytes: 942490
- SHA-256: `6f7c1f7af52899f160db2290164abe75acfd18eccf4ba962ea67f4cb0c843c33`
- Git blob: `d87fceb204da9abcd4c01abc3c5223df7b9e2b9c`

All 71 recorded metadata checks pass. No scientific module, simulation, numerical campaign, scientific test, historical stack, or workflow was executed by this auditor. Only connector reads and local decoding, hashing, serialization, and file/tree comparisons were used. The auditor did not publish objects or update refs.

This verdict certifies only the recorded source and publication integrity at the immutable scientific commit. It is not native physical evidence, an independent re-performance of the mathematical review, historical reproduction, numbered-stage closure, PR readiness, approval to merge, or audit of a later receipt. The published candidate and review continue to state that the native informational-difference milestone is NOT ACHIEVED and broad C3/C4-C6 remain OPEN.
