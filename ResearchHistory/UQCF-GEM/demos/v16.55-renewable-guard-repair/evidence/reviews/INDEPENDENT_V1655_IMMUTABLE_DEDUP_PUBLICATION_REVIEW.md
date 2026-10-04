# Independent v16.55 immutable deduplicated publication review

Reviewer: independent Codex agent `/root/v1655_implementation_review`.
Date: 2026-10-04 UTC.
Decision: ACCEPTED for durable publication only. No merge approval or numbered certification.

Immutable evidence commit: bbdbf6138b60e51e0f229951280b01455d2a4c09, isolated branch research/v16.55-evidence-37207960846-1. GitHub Git-commit readback confirms the sole parent abb27dcacfe8721a49a7a9742b37eebc2f3a0efc. Compare confirms exactly 98 added files, all exclusively under evidence/recovery/run-37196753029-attempt-1, with no scientific source change. Publication run 37207960846/job 111453031531 independently observed terminal SUCCESS. Receipt artifact 11305083885 independently API-bound to the request SHA/attempt, length 641,298 bytes and SHA-256 26bd0c1c7d1120ec1dddbbd785e23c46dba90f8f14d028e553a5851400b2378a; this review does not rely on receipt/uploader PASS for content correctness.

## Independent reconstruction method

Fetched the untruncated immutable recursive Git tree and all 61 JSON files. Two duplication maps exceed the contents endpoint threshold and were retrieved by their exact Git blob SHA instead. For every JSON file, derived Git SHA-1 over the exact `blob <length>\0` prefix plus raw bytes and compared immutable tree identity/length; separately checked publication SHA-256 manifest.

For the 37 binary parts, used previously independently downloaded and external-digest-verified raw originals embedded in the four existing recovery wrapper ZIPs. Independently extracted each original, verified its external length/SHA-256, divided exact bytes into the declared ordered 20 MiB chunks, and computed each chunk's Git blob SHA-1, length and SHA-256. Every value matches the immutable Git tree, PARTS.json and PUBLICATION_MANIFEST.json. Thus this is exact Git object identity verification against independently known bytes, not direct redownload of all binary parts and not inference from successful upload. Independently concatenated original byte streams match all 28 original archive digests; ordered parts and manifest membership are exact.

Streamed actual original ZIP member bytes into an independent (artifact ID,member name) content index. Streamed every component wrapper member and checked its full identity and every reference edge. Compared the 22 retained component root JSON bytes directly to their original wrapper bytes. Derived package membership independently from the four actual component ZIP member sets plus four wrapper transports and three retained package roots. Checked every package reference, every row identity, and exact package DURABLE_MANIFEST path/hash membership. No mathematical producer, path verifier, numerical campaign or scientific control was executed locally; this is artifact/identity inspection.

## Exact results

| Published or accounted evidence | Count | Bytes |
|---|---:|---:|
| Published Git files | 98 | — |
| Original archives | 28 | 301,804,233 |
| Original binary parts | 37 | 301,804,233 |
| PARTS manifests | 28 | — |
| Retained component root metadata | 22 | 188,702 |
| Retained package root metadata | 3 | 362,414 |
| Component original archive references | 28 | 301,804,233 |
| Component original-member references | 2,217 | 583,060,369 |
| Package superseded wrapper references | 4 | 603,564,564 |
| Package component-member references | 2,267 | 885,053,304 |

The component/package maps cover all 2,267 component members and all 2,274 package members respectively. Original package DURABLE_MANIFEST contains exactly 2,272 paths: full package membership except STATUS.json and DURABLE_MANIFEST.json, with exact hashes. Structured COMPONENT_ARTIFACTS consists of exactly the four expected component/id/name/length/digest rows and equals DERIVED_WRAPPER_REFERENCES.recovery_components. All package edges resolve down to component maps, then to original archive bytes/original members or retained metadata; no circular resolutions exist. The 17 nested cached ZIPs correctly resolve as original partial-archive members, preserving intended classification totals.

The original 28 raw ZIP encodings are durably preserved byte-exactly once. Derived component/package ZIP encodings are intentionally referenced by immutable original GitHub IDs/lengths/digests; their payload membership/bytes are fully accounted by the maps, rather than promising to reproduce identical derived ZIP container encoding. No recursive wrappers or temporary transport files are committed. This satisfies the revised deduplicated evidence policy.

## Provenance and limitations

Published receipt preserves original run 37180275767/attempt1/SHA60c48b818366354d26366af35726788553865455 as cancelled, and recovery run37196753029/attempt1/SHAa75c82f31c5547bf20feb75960fbedf2f7e5c0a6 as successful. Preserved original partial archive11298392763 reconstructs exactly, including its INCOMPLETE state, as established in the whole-evidence review. Publication event/workflow SHA both equal abb27dcacfe8721a49a7a9742b37eebc2f3a0efc, run37207960846/attempt1. Package/receipt explicitly leave numbered certification pending.

Prior failed publication run37207229521/job111450846638 independently remains FAILURE with commit step skipped; it must remain described in publication history by the failure/correction review and not be presented as a success. No scientific rerun occurred in this publication.

No Critical or Important blocker remains for this immutable publication. The actual-merge source/topology repair, reviewed source contract, fresh actual-merge replay, durable replay evidence and independent whole-argument/actual-merge acceptance remain mandatory before v16.55 certification. This acceptance does not close unrestricted native connectivity or the separate efficiency obligation.

Machine inspection summary: INDEPENDENT_IMMUTABLE_PUBLICATION_INSPECTION.json. Independent inspection source: inspect_immutable_publication.py. Immutable readback and raw JSON evidence retained locally for publication of this attributable review.
