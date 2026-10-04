# Independent v16.55 corrected deduplicated publisher source review

Reviewer: independent Codex agent `/root/v1655_implementation_review`.
Date: 2026-10-04 UTC.
Decision: ACCEPTED for a fresh packaging-only publication launch. This is not evidence publication acceptance, merge approval, or certification.

Exact candidate head: fcf6c9299ca8502152aa560231dbd41e01310e85.
Corrective implementation commit: 9bbc55bdb9f38bba2d44f8082847106216e570a4.
Module blob: 83bc48eb8117ce956b84f9ff55a6a7676958e02c.
Tests blob: 1cc89ca039027159b758846ed84f112232c74d30.

The correction supplies an exact component transport-member-name to (length,SHA-256) content-key map derived from the digest-frozen original archive ledgers. It rejects absent declared names, duplicate wrapper names, duplicate ledger transport roles and content substitution at declared transport paths. Component preparation additionally requires exact 8/8/11/1 transport path inventories. Only declared transport names can resolve as ARCHIVE_REFERENCE; all other nonmetadata members must resolve through the original-member index. The 17 cached ZIP copies are therefore member references, as independently confirmed from existing archive bytes in the preceding failure review. This restores the intended 28 archive / 2,217 member / 22 metadata counts without changing evidence bytes or weakening reconstruction checks.

The package layer retains its separate superseded-component-wrapper classification and fixed 2,274-member inventory. Original archives remain independently API-bound, downloaded, hash-verified, split into ordered parts and reconstructed. Original/recovery immutable tuple binding, credential-safe redirected download, exact root metadata inventories, temporary transport removal, Git-safe isolated publication and pending-certification classification are unchanged. The GitHub compare from previously reviewed 1b4f58ff to candidate shows only module/tests and request files changed; no workflow or scientific source changes.

I independently fetched the exact module/test blobs and candidate-path readback. GitHub run 37207793220, job 111452530296, completed SUCCESS at candidate fcf6c929; logs show all 20 exact test methods passed, no skips, including nested archive-copy collision, missing declared transport, substituted content and duplicate names. Control artifact 11305896235 is 1,232 bytes with SHA-256 c70d3cf7d7b5e2e9f8d66546a387bb3c38dd56db4e9f43def8530afd650bd1d6. No local controls, scientific producer, verifier or campaign was executed.

The failed publication run 37207229521 remains failed and must remain recorded. A fresh literal publication request must be the sole child of this accepted candidate and change only DURABLE_PUBLICATION_REQUEST.json, binding source_parent to this exact head. After execution, immutable output readback must independently verify the 28 original archives, ordered parts, 25 retained JSON roots, complete component/package maps and provenance. No science rerun is authorized by this acceptance. Actual merge replay and final certification remain separate pending gates.
