# Independent source and publication audit

**PASS for the declared source and scientific-publication scope. No blocking findings.** This is a provenance audit of the conditional analytical record, not scientific execution or physical certification. The native physical milestone remains **NOT ACHIEVED**.

| Required identity or disposition | Value |
| --- | --- |
| `stage1_disposition` | `PASS` |
| `stage2_disposition` | `PASS` |
| `scientific_execution_performed` | `false` |
| `scientific_commit` | `f005bf8ed50565f0c844bec4ec1020a3298b8551` |
| `scientific_tree` | `3460aa50a11ec391878f9b1c121ef1c8dd1b32df` |
| `source_parent` | `c65db96eedbcd354c4b96ad9d617f97c2aeb9283` |
| `sole_parent` | `c65db96eedbcd354c4b96ad9d617f97c2aeb9283` |
| `publication_bundle_sha256` | `625cfc8e2a349e7df2431a712990f864c11bbab140664c4da96972085525d1a3` |
| `blocking_findings` | `[]` |

Repository: `proteinfoldingengine/WetLabEngine`. Source tree: `e249605553eee450c9dcd2144e84635c0f084cad`. The branch `research/uqcf-overlapping-guard-exchange` independently resolved to the scientific commit during Stage 2. This is an observation at audit time, not a claim about a later receipt commit or future branch state.

## Stage 1: immutable source originals

I independently retrieved all thirteen source files through GitHub at the exact source parent. All 191,738 original bytes match the packet, file by file. Byte lengths, SHA-256 digests and recomputed Git blob identities match the supplied identity table and GitHub identities. I retrieved nine complete, untruncated directory trees, recomputed their canonical Git tree hashes, and verified every source path through those trees to the parent commit's root tree.

The resolved 404 in `retrieval_note.json` documents the local draft filename's correction to the canonical remote path. It is routing provenance, not a scientific rejecting control.

## Stage 2: frozen scientific publication

I independently retrieved all eight published files at the scientific commit. Their complete bytes, lengths, SHA-256 digests and Git blob identities match the frozen 320,325-byte publication bundle. The commit has exactly the intended sole parent and scientific tree.

The exact change set is seven additions in `research/physical-bridge/pruning_cover_record/`: `RESULT.md`, `INDEX_APPEND.md`, `source_packet.json`, `source_identities.json`, `retrieval_note.json`, `ANALYTICAL_REVIEW_RAW.md`, and `PUBLICATION_MANIFEST.json`; plus the continuation modification. The published continuation is exactly its 72,728 parent bytes followed by the 1,937 bytes of `INDEX_APPEND.md`, yielding 74,665 bytes.

I independently reconstructed the expected complete root tree by applying only those eight entries to the verified parent directory trees, preserving every sibling name, mode and object identity. The computed root is exactly `3460aa50a11ec391878f9b1c121ef1c8dd1b32df`. Six retrieved publication trees match their reconstructed expected entries and hashes. This excludes unrelated changes without auditing unrelated archive contents. The GitHub comparison separately reports exactly seven additions and one modification.

The manifest binds all seven non-manifest payloads, explicitly excludes itself, and correctly binds the source lineage and exact continuation append. The published source packet and identity table retain the Stage 1 originals. The unmodified raw analytical review binds the exact report and append SHA-256 values and accepts their declared conditional analytical scope. My audit verifies that binding; it does not replace the review's mathematical judgment.

## Scope and evidence

`PUBLICATION_AUDIT_EVIDENCE.json` records the source identities, ancestry trees, published identities, complete-tree reconstruction, manifest and review binding checks, and dispositions. The auditor's raw retrievals and provenance verification scripts are retained under `audit_work/`.

No scientific execution, enumeration, simulation, numerical scientific tests, historical replay or archive audit was performed. The auditor did not edit the report, append, review, manifest, bundle or repository refs. Author readback outputs and receipt context were not read or used as evidence. **Later receipt publication and author terminal readback are explicitly excluded.** This audit establishes neither a main merge, historical recertification, numbered-stage CLOSED/CERTIFIED status nor native initialization, physical interaction, enforcement or receiver access.
