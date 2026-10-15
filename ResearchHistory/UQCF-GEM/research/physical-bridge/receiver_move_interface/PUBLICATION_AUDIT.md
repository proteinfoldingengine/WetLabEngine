# Independent source and publication audit

Date: 2026-10-15 UTC. Auditor: separately dispatched `receiver_move_publication_audit` agent, independent of the report author and analytical reviewer.

**Stage 1: PASS. Stage 2: PASS. No blocking publication-consistency finding.**

This audit binds the exact source snapshot and seven-file scientific publication below. It verifies source and publication identity, complete change scope, manifest consistency, append-only history preservation, and the final analytical-review bindings. It does not certify the proof or physical derivation. Native milestone: **NOT ACHIEVED**.

## Immutable bindings

| Object | Identity |
| --- | --- |
| Repository | `proteinfoldingengine/WetLabEngine` |
| Declared branch | `research/uqcf-overlapping-guard-exchange` |
| Source parent / sole scientific-commit parent | `c63bc3ea9b92241fb96d52fe5e47dde16fd97c6b` |
| Source parent tree | `c0199b8527c14c44a8bd4496f705411369355d5b` |
| Scientific commit | `d6d9f758747d50acf718bc32b287939690dd0f25` |
| Scientific tree | `0baa957684acf1cda868d3e73df5b7a3f814c72f` |
| Frozen seven-file publication bundle SHA256 | `f32fb9d4a14e1607b5cd15a54bfbad8fa5785ea207074ab8819091d6905c1f95` |
| Frozen publication bundle bytes | 274632 |
| `PUBLICATION_AUDIT_EVIDENCE.json` SHA256 | `052dc2331e461cfab9ce356dead07466f42b2ff2e4511ddaf434267e0fe077f8` |

The scientific commit was independently fetched by immutable SHA. Its tree and its one-element parent list exactly match this table. The bundle's own `tree` field names the source parent tree; the published scientific tree is recorded separately above. This audit is tied to the immutable scientific commit and makes no claim about a later branch head.

## Stage 1: original sources

I independently retrieved all ten full source originals through GitHub with the immutable source-parent ref. Every original exactly matches the supplied source packet in UTF-8 bytes, and its independently calculated byte length, SHA256, and Git blob SHA1 matches `source_identities.json` and the returned GitHub blob. The ten path sets are exact and unique.

I independently retrieved the source parent commit and nine non-recursive Git trees, reconstructed every canonical tree object's SHA1, and checked every path link from the root tree to the ten source blobs. All tree hashes, source blob identities, sizes and links match. An initial recursive-tree request returned `Transport closed`; it supplied no usable evidence. The successful complete non-recursive chain resolved that transport failure without leaving an evidentiary gap.

This was full-source byte/provenance verification. It was not a semantic audit of every historical continuation entry, an archive-wide recertification, or an independent rederivation of the source theorems.

## Stage 2: exact publication readback

I independently retrieved all seven full published files at scientific commit `d6d9f758747d50acf718bc32b287939690dd0f25`. No line-range truncation was requested. Every retrieved text is byte-for-byte equal to the frozen publication bundle; its byte length, SHA256 and locally reconstructed Git blob identity match the bundle declarations, GitHub return value and scientific tree entry.

I fetched and independently hashed the six changed ancestor/new-directory trees, compared their entries with the independently fetched parent trees, and recursively followed only changed subtrees. This establishes exactly **six file additions and one index modification**, with no other changed path. The independent GitHub parent-to-scientific comparison agrees: one commit ahead, zero behind, the same seven paths, six added and one modified. All published entries are regular `100644` blobs.

Paths below are relative to `ResearchHistory/UQCF-GEM/research/physical-bridge/`.

| Published path | Bytes | SHA256 | Git blob SHA1 |
| --- | ---: | --- | --- |
| `COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` | 70679 | `4df672e43c55642b10beb004b436893a046fab50e981bc927b9e5c1e76e0caf2` | `6e12bc0621056d625d67791ac3453b7199db07c2` |
| `receiver_move_interface/ANALYTICAL_REVIEW_RAW.md` | 15998 | `9b97c2ed3e4710f21409759d8cdc02e85f6434e609c23e8d1edbcee56dc36b91` | `d3203da22b9cdc602db3d502f2db8e73773e67f8` |
| `receiver_move_interface/INDEX_APPEND.md` | 2267 | `b32a0acc3dc04566fc6c504501447a7aacbfec0b8da424fbe115c25656e579d2` | `3473c8ad514e7628bc894a06929874b4a13f4332` |
| `receiver_move_interface/PUBLICATION_MANIFEST.json` | 2738 | `95ba8621ea77d0644f8e22bcd7e62273d51bc8fd68ff1d253b6bae61689a9b25` | `25c6bc17f4e61ddeb50a9b9e7ca0f10c1be4368c` |
| `receiver_move_interface/RESULT.md` | 14856 | `91ea3f0e5581cd7e95a05dd1e21afa1d946e4d58e9ca4f74bec8b9e3d089bde2` | `0371d4a8aa66ce02ffbda084ad5dde93f1ec1136` |
| `receiver_move_interface/source_identities.json` | 2935 | `aa38332fadccf04b1cb8f33681836347a30289ec23ded32d59b5b3d7c216465a` | `28f419a40eaf90dab2537eba05a45763d1fff5ab` |
| `receiver_move_interface/source_packet.json` | 159491 | `dccb60daf0b348551fdf3400f0a7c14f001da8b92225a74ff7d0a195a2e8e9f5` | `f2814aa4e62e8c17b176343c50982f56e3f950c5` |

The new directory contains exactly the six added files shown above. The continuation index is the sole modified file.

## Manifest, source packet and continuation

The published `PUBLICATION_MANIFEST.json` exactly matches the frozen manifest. It names exactly the six non-manifest payloads, gives their correct byte lengths, SHA256 values and Git blobs, and expressly excludes itself. Its own identity is independently bound in the seven-file table and audit evidence, so this does not create a self-referential hash claim. Its source parent/tree, no-execution declaration and `NOT_ACHIEVED` physical milestone are correct as declared publication metadata.

The published source packet and source identities remain byte-identical to those audited in Stage 1. All ten embedded source texts still exactly match the independently retrieved originals and their identities; no original source was silently substituted.

The published continuation is exactly the independently retrieved **68412-byte parent continuation plus the 2267-byte `INDEX_APPEND.md`**, producing **70679 bytes**. The comparison checks the entire concatenation, not merely a prefix or a reported line count. Manifest base and append identities match those exact bytes. No earlier continuation byte changed.

## Analytical-review binding and claim boundaries

I read the final report, append and raw independent analytical review. The raw review states **ACCEPT for the explicitly conditional bare-command classification and bounded receiver-candidate assessment**, and records no remaining blocking mathematical/source finding. Its exact four-object SHA256 table binds the published report, append, source packet and source identities. In particular, the report hash is `91ea3f0e5581cd7e95a05dd1e21afa1d946e4d58e9ca4f74bec8b9e3d089bde2` and the append hash is `b32a0acc3dc04566fc6c504501447a7aacbfec0b8da424fbe115c25656e579d2`.

The raw review records the unit-band control across all five internal coordinates (`h_o`, `h_p`, `h_u1`, `h_u2`, `h_v`) and total deficit, and explicitly separates mathematical acceptance from repository publication. This audit verifies that the stated acceptance and coordinate check are preserved in the exact committed review; it does not substitute a new proof review or independently certify those derivations.

The report and append keep bare-relation classification separate from physical enforcement and readable feedback, leave native access open, and preserve the richer guarded-interface qualification. The report retains the explicit not-achieved milestone, Path A active / Path B closed, time as pruning / ordered recoverability update, and open broad C3/C4-C6 and physical origin. It makes no numerical-execution, historical test-count increment, main-merge, or numbered-stage CLOSED/CERTIFIED claim.

## Limits and disposition

Only text/JSON parsing, byte comparisons, cryptographic hashes and Git tree/path comparisons were executed by this auditor. **Scientific execution performed: false.** No scientific modules, enumeration, simulation, numerical campaign, inherited test stack, historical workflow replay or recertification were run. The report and manifest no-execution statements were checked as publication declarations; this is not a forensic assertion about unrelated activity.

The raw retrieval records and reproducible provenance comparisons are retained under `audit_work`; the accompanying evidence JSON records the exact checked predicates, all source and publication identities, tree chain, changed-path set, review bindings and scope exclusions. Its disposition follows 29 passing publication predicates and the passing ten-source Stage 1 checks. No author report, append, source packet, source identities or manifest was edited by this auditor.

**Excluded from this independent audit:** any later receipt commit, the later five-file receipt, terminal author readback, later branch state, main merge and post-merge closure. Publishing this audit alongside a later receipt does not extend the audit to that receipt. This audit is not self-certification of its own later publication.

Final disposition: **PASS for the exact source/publication consistency scope at the scientific commit above; no blocking findings. Physical derivation and native milestone remain unearned.**
