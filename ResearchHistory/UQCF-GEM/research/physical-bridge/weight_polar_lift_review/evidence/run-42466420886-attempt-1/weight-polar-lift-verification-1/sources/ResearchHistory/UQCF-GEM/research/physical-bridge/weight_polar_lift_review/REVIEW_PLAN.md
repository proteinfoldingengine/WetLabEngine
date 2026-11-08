# Prospective whole-argument review plan

## Status before this freeze

The mathematical polar-lift idea, including a weighted-null-space objection and factor-of-two limitation, was explored and published in PR111 comment 6719605741 before this plan. An internal assistant checked the algebra. This is therefore not a preregistration of an undiscovered result. No numerical scientific campaign is proposed. Comment 6719631614 corrects the initial decision not to obtain Gemini review and announces this isolated review.

This plan prospectively freezes the exact full manuscript and immutable original source evidence before new review execution. The independent reviewer receives DERIVATION.md plus the full original sources, but not the internal review, claimed favorable verdicts, prior CI status, or a condensed answer key.

## Sequence and separation

1. Commit DERIVATION.md, this plan and SOURCE_PACKET.json to gpt/weight-polar-lift-review, descended from research head 8d827f647916c7335272aadc38f7415f11d89c55. Record that immutable commit and byte hashes in FREEZE.json in a subsequent implementation commit. Do not modify inherited regression sources.
2. In a fresh GitHub Actions verification job, check source bytes, Git blobs, frozen ancestry, immutable checkout, exact artifact membership, and negative integrity controls. Run the complete inherited owner-correspondence regression/certificate stack without modifying it. This is infrastructure/regression verification, not new evidence for the theorem or a new numerical research campaign.
3. In a distinct job, discover the previously working Gemini model availability using the existing authorized helper, then request an independent adversarial reconstruction of the entire frozen argument. GEMINI_API_KEY is read only from the existing Actions secret. No local credential handling and no substituted OpenAI-as-Gemini review. Preserve model metadata, full prompt/request, raw response, parsed verdict, source hashes, run ID, attempt and workflow SHA. A reviewer may return ACCEPTED, REVISE or FAIL. CI green only means the record was handled correctly, not that the scientific verdict was ACCEPTED.
4. In a distinct publication-audit job, reproduce the inherited certificates, verify exact model-input and raw-response parsing, compare immutable GitHub source readbacks to the checkout, and validate every artifact digest. Keep the independent review verdict separate from the native status, which this submission does not promote beyond NOT_DERIVED.
5. Archive original artifact ZIPs and available completed job logs, with digests, on the isolated branch. Fetch the archived commit and verify manifest members byte-for-byte from immutable Git objects. Preserve any failed run and its logs; never replace it with a success narrative. Inspect the verdict and every objection manually before posting the report. If material repair is required, append a new version/freeze and obtain a fresh independent review rather than editing away history.
6. Open only a draft PR targeting research/uqcf-overlapping-guard-exchange. No merge, default-branch write, PR130/131 status change, or physical/native claim. Publish the useful result and exact review status in the authorized PR111 bot thread, including immutable evidence links and unresolved obligations.

## Acceptance boundary

No named scientific stage is certified by this checkpoint. Publication requires correct evidence provenance and honest disposition of the independent review. Acceptance of the scoped mathematical theorem is distinct from derivation of native incidence, action-current identification, owner access or physical mechanism. Known source limitations do not become resolved because a reviewer repeats them. Any new review objections, model/tool failures, incomplete logs or stale readback are explicitly reported.
