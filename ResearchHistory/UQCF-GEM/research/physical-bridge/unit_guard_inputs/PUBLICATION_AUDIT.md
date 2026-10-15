# Independent source and publication audit — unit guard inputs

Audit date: 2026-10-15 UTC. Repository: `proteinfoldingengine/WetLabEngine`.

**Stage 1: PASS. Stage 2: PASS. Blocking findings: none.**

This is an independent source-identity and publication audit for the scoped analytical counterexample and bounded source reconciliation. Mathematical acceptance is recorded separately in `ANALYTICAL_REVIEW_RAW.md`. Text, hash, and Git-tree agreement do not establish physical dynamics. The native dynamics milestone remains **NOT ACHIEVED**.

## Immutable identities

| Item | Verified value |
| --- | --- |
| Source parent / sole scientific parent | `ecfda4c115a0ea367a1f06c41c9e29cabe70b986` |
| Source tree | `60a06b8f251796c21ac021ac92f14897f69d2fc7` |
| Scientific commit | `cc6fb045ab4d405e754e8346d318ea1cded5314a` |
| Scientific tree | `8c1b1699ee08bb18814c4596f2610643608baabc` |
| Frozen seven-file bundle SHA-256 | `fc62a775a0c71c2c80339d6f225b25e907a7b0d1fd946578ce6944b55cfb9b1d` |
| Frozen bundle bytes | 266,457 |
| Branch observed at the scientific commit | `research/uqcf-overlapping-guard-exchange` |

## Stage 1 — original sources

I independently fetched all ten required source files through the connected repository interface at the exact source parent. I compared each complete UTF-8 byte sequence with `source_packet.json`, and each byte length, SHA-256 digest and Git blob identity with `source_identities.json`. All ten matched exactly. Immutable path URLs and blob fields also matched.

I independently fetched the parent commit and the nine nonrecursive Git trees needed to connect those paths to the root tree. Every parent-child tree link and terminal blob entry matched. I recomputed all nine Git tree hashes from their complete immediate entries; none of the tree responses was truncated. The source parent resolves to the expected root tree. No unrelated archive file contents were read.

The full source identities and tree checks are retained in `PUBLICATION_AUDIT_EVIDENCE.json`. Raw independent responses and the provenance-only checker are retained in local `audit_work`.

## Stage 2 — scientific publication

I independently fetched the scientific commit, its parent-to-head comparison, the branch ref, and all seven complete published files at the immutable scientific SHA. All published texts, byte lengths, SHA-256 digests and Git blob IDs matched the frozen bundle. The source packet and source-identity file preserve the exact bytes audited in Stage 1. The author payloads and frozen bundle remained unchanged during the audit.

The commit has exactly one parent: the source parent above. Its diff contains exactly six added files under `ResearchHistory/UQCF-GEM/research/physical-bridge/unit_guard_inputs/`:

- `RESULT.md`
- `INDEX_APPEND.md`
- `source_packet.json`
- `source_identities.json`
- `ANALYTICAL_REVIEW_RAW.md`
- `PUBLICATION_MANIFEST.json`

The only other changed path is `ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md`. Its published 72,728 bytes are exactly the independently fetched 70,679 parent bytes followed by the reviewed 2,049-byte append. No parent bytes were deleted or replaced.

The new publication directory was absent at the parent. I independently reconstructed the complete expected scientific root tree from the audited parent trees using only those six new file entries and the continuation replacement. The resulting root hash is exactly `8c1b1699ee08bb18814c4596f2610643608baabc`. This whole-tree check detects unrelated path, content, or file-mode changes without reading unrelated archive content. It also preserves the other nine original source paths unchanged.

The manifest contains exactly the six nonmanifest payload identities, explicitly excludes itself, pins the correct source parent/tree, and correctly identifies both continuation components. The seven-file bundle separately identifies the manifest. The raw analytical review retains its scoped acceptance and binds these exact reviewed artifacts:

| Artifact | UTF-8 bytes | SHA-256 |
| --- | ---: | --- |
| `RESULT.md` | 16,080 | `9c5c1ea51ad7f56cdc5d2a19de69c9431ef971f537cb343550a5d9ddfefa5233` |
| `INDEX_APPEND.md` | 2,049 | `8c40c5074911bda4314830edaba0dcf2bed2fa0429e6886d8f7859c8321b2368` |
| `ANALYTICAL_REVIEW_RAW.md` | 20,427 | `de18a1738df1539c99c85fece1447f7b03c3cbeb74f4e4ee8393fb6516341f01` |

All 57 Stage 2 checks passed. Machine-readable checks, per-file identities, tree reconstruction, and exact continuation provenance are recorded in `PUBLICATION_AUDIT_EVIDENCE.json`.

## Scope and exclusions

No scientific module, enumeration, simulation, numerical campaign, historical replay, numerical test-count increase, or historical recertification was performed by this auditor. Executed code only parsed text and computed or reconciled file identities and Git trees. No author payload was edited.

This audit does not independently recertify the analytical argument, infer a physical guard from the publication, establish enforcement or access, or certify a new force, main merge, numbered-stage closure, or native-event milestone. The report and manifest preserve those limits.

The branch observation applies to the time of this scientific audit. Subsequent publication of this audit, its evidence, or any receipt is explicitly outside the audited seven-file scientific bundle and outside this audit's certification. Subsequent author terminal readback and later branch movements are also excluded. These exclusions must remain attached when the audit is published.
