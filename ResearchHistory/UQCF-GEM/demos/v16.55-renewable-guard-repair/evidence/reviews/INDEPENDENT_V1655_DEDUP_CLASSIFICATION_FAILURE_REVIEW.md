# Independent v16.55 deduplicated publication classification failure review

Reviewer: independent Codex agent `/root/v1655_implementation_review`.
Date: 2026-10-04 UTC.
Scope: read-only inspection of existing component ZIP bytes and source classification semantics; no scientific execution, launch, merge, or certification.

## Finding: CHANGES REQUIRED before another publication launch

Publication run 37207229521 / job 111450846638 failed before committing evidence. Reviewed source 1b4f58ff50ad0f0bca7310285a0b1f9a0db7594e, module blob a4de9c83cdea8b9f5286708c538ad4602df58bb9, globally classifies a nonmetadata member as ARCHIVE_REFERENCE whenever its (length,SHA-256) matches any of the 28 original raw archives. The inventory constants describe structural transport roles instead. These rules disagree on nested cached originals in the preserved timeout archive.

| Classification | Source actual count | Source actual bytes | Intended structural count | Intended structural bytes |
|---|---:|---:|---:|---:|
| ARCHIVE_REFERENCE | 45 | 349,559,543 | 28 | 301,804,233 |
| MEMBER_REFERENCE | 2,200 | 535,305,059 | 2,217 | 583,060,369 |
| RETAINED_METADATA | 22 | 188,702 | 22 | 188,702 |

The difference is exactly 17 cached ZIPs, totaling 47,755,310 bytes, under `partial-original-publication/archives/`: one controls ZIP and eight primary plus eight reproduction ZIPs. Each is both a raw original artifact and an extracted member of original partial artifact 11298392763. Independent reconstruction of the original ZIP member content index confirms all 17 resolve as original partial-archive members. Primary, reproduction and inherited component statistics are unchanged; only the partial component gains 17 archive references and loses 17 member references under the global priority rule.

This is a mechanical inventory semantic failure. It does not show missing evidence, changed scientific bytes, or a failed mathematical certificate. The original run remains INCOMPLETE; successful recovery remains its separate completed audit. This failed publication is not a successful durable publication and must be preserved truthfully.

## Minimal correction

Define an exact component-specific transport-path-to-original-ledger mapping. Only those paths may be ARCHIVE_REFERENCE, and each must match its corresponding ledger identity, length and digest, rather than any global raw archive hash:

- primary and reproduction: `originals/shard-0.zip` through `originals/shard-7.zip`;
- inherited: `originals/full-controls.zip`, `originals/inherited-development.zip`, `originals/inherited-domain-0.zip` through `originals/inherited-domain-7.zip`, and `originals/inherited-foundation.zip`;
- partial: `partial-original-publication.zip`.

Retained exact root JSON remains first. All other members, including the 17 nested cached ZIPs, must resolve through the existing original-member content index. Require complete exact transport-path membership with no missing or duplicate roles and reject an incorrect original identity at a declared transport path. This preserves the intended 28/2,217/22 semantic totals without deleting any evidence. The 28 original raw archives remain stored once.

Add a rejecting control whose nested cached ZIP is byte-identical to an original raw archive and must be classified as MEMBER_REFERENCE, together with controls rejecting missing transport paths and a wrong transport identity. Freeze the corrected source, obtain independent exact source review, then launch a fresh publication request. Do not rerun science or weaken resource/evidence requirements.

## Review correction and remaining gates

My earlier source acceptance checked the structural inventory and hash-reference machinery but missed the collision between nested cached ZIP bytes and global archive-first classification. That acceptance is superseded for further launches by this finding. The independent read-only totals and archive-match rows are recorded in `INDEPENDENT_COMPONENT_CLASSIFICATION_CORRECTION.json`.

After a corrected launch, independently read back the immutable evidence commit, verify all 28 original archives and ordered parts, all 25 retained root JSON documents, both component and package reconstruction maps, original/recovery/failed-publication provenance, and reconstruction completeness. Package mapping must still cover all 2,274 members and reference the four superseded wrapper archives through their exact component maps. Actual merge replay and final certification remain later gates.
