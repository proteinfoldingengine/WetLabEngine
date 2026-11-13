# Independent pre-execution plumbing review

Reviewer: separate fresh-context Codex agent `quiet_review_plumbing`; no model/API calls or file modifications by the reviewer. Completed before workflow commit `8b258a123276fb286d5d8875b549f9da9c58f8b2` was pushed. This review concerns evidence plumbing, not independent scientific certification.

Verdict: Ready for the single paid analytical review. No Critical or Important execution-blocking defects; no merge approval.

Verified: all 8 controller tests pass; seven source documents and both reused helpers match pinned Git bytes; exact document ordering, packet digest, prompt, request, raw response and parsed verdict are bound together; returned model, complete response, run identity and NOT_DERIVED are checked; pinned Actions, read-only permissions, dedicated branch/path and first-attempt-only generation; publication has no model key or generation call.

Minor findings retained for manual verification:

1. `uqcf_quiet_reference_review.py` delegates schema validation to the unchanged parser, which does not require `proof_checks` or `next_native_obligation`. An automated ACCEPTED alone does not establish substantive analysis. Root will inspect both fields and the claim-specific reasoning before adjudication.
2. The controller validates requested model and raw returned model but does not reconcile redundant `manifest.model_returned` or require manifest status in its reusable audit function (called before status becomes ACCEPTED during the review). Root will check those redundant fields against the raw response and completed run.

Root rulings on considered boundaries: no simulation/algebra receipt is appropriate for this analytical task; first-attempt guard is per run, so a later workflow-changing push would be a separate generation decision requiring an explicit reason; original GitHub artifact digests/run evidence provide provenance beyond self-contained hashes; missing native derivation remains an explicit scientific limitation. No scope is promoted by these rulings.
