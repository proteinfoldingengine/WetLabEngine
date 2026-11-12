# Target E frozen-note review implementation plan

> For agentic workers: execute this small plan inline using the existing approved review transport. The standing instruction to complete authorized work governs execution.

**Goal:** obtain one independent Gemini review of the frozen Target E argument, including Dot's fixed-binary-effect control, and preserve the complete verdict and source evidence.
**Architecture:** reuse the existing pinned preparability model-call/parser helpers; add a note-specific input lock and controller; run review and a separate immutable-source/publication audit on GitHub. Preserve adverse verdicts and raw evidence.
**Tech stack:** Python standard library, existing Gemini helper, pinned GitHub Actions.
**Spec:** TARGET_E_CLOSED_PREMISE_CHECK_2026_11_12.md at 6c9be7cc12b8810bdf76ac12d6d8e2cda5a25e18 and the contract below.

## Contract and scope

This is review infrastructure for an already written analytical note, not a preregistered discovery or numbered retained-research stage. No scientific simulation or inherited certification rerun is claimed. The review covers the isometry/marginal calculation, pointwise versus uniform quantifiers, no-maximal-closed-set argument, and the fixed-effect control. Older dependency texts supply the stipulated benchmark; unrelated old results are not being recertified.

One generation only, using gemini-3.1-pro-preview. All source documents and reused helpers are pinned by origin, Git blob when applicable, SHA-256 and byte count. Include exact document bytes in the prompt. A peer agreement is evidence to challenge, never authority. Acceptance requires a complete response, matching model, ACCEPTED verdict, empty defect arrays, and explicit NOT_DERIVED native status. An unearned native claim blocks acceptance.

## Files and checks

- Create target_e_closed_premise_review/SOURCE_PACKET.json under physical-bridge: exact source/peer snapshots and locks.
- Create .github/scripts/uqcf_target_e_closed_review.py: source validation, prompt, one-call review, separate audit.
- Create .github/scripts/uqcf_target_e_closed_tests.py: rejecting controls for altered/missing inputs, duplicate sources, wrong remote bytes, truncated/wrong-model/defective responses, altered verdicts, and repeated generation.
- Create .github/workflows/uqcf-target-e-closed-review.yml last: trigger once on its creation; preserve artifacts even on failure.
- Preserve final raw evidence, original artifact digest receipts, logs and review status under target_e_closed_premise_review/evidence/.

## Execution

- [x] Write the rejecting tests and record the expected failure before implementing the controller.
- [x] Implement the minimal controller using the existing model transport; pass the complete local plumbing suite.
- [x] Publish locked inputs and code, verify immutable readback, then publish the triggering workflow.
- [x] Stay in session through review and publication audit. Inspect actual verdict, findings, model identity and logs.
- [x] Preserve raw evidence and exact readback receipts. Report analytical acceptance separately from the native milestone.

Review focus: source substitutions; review-byte alterations; missing response/finish reason; accidental regeneration; confusion between a binary effect, a multi-outcome measurement and optimized trace distance. Tests address the first four; the exact frozen argument and reviewer prompt address the mathematical scope.

## Completion record

Completed 2026-11-12. Run 43217169237 attempt 1 finished successfully: one Gemini generation ACCEPTED the frozen conditional argument, and the separate publication audit passed. The original ZIPs, completed job logs and readable verdict were preserved and verified by exact immutable readback. See [STATUS.md](STATUS.md) for the exact accepted argument and scope. This completed review does not derive native delivery and must not be rerun for the unchanged argument.
