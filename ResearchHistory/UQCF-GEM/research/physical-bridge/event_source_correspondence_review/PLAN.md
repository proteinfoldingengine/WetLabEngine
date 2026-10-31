# Event/source correspondence review implementation plan

Goal: independently challenge the existing positive proof and blind-port counterexample, with exact source provenance and a constructive attempt at the missing native association.
Architecture: freeze exact manuscripts and eight complete source files; adapt the established balanced-sibling Gemini integration without changing its model transport; run integrity, whole-argument review, and independent publication audit on an isolated research branch.
Tech stack: Python standard library, GitHub Actions, existing Gemini model transport.
Spec: RESULT.md and the user's standing autonomous research/review authorization.

## Constraints and rulings

- Native bridge remains NOT_DERIVED; a reviewer-proposed derivation triggers separate assessment.
- No scientific numerical campaign or numbered-stage closure; no main or shared research-branch merge.
- One model-availability GET and one generation, with no automatic model fallback or retry.
- Raw request/response, prompt, model metadata and run identities must be preserved.
- Ruling: the workspace has no Git checkout. Use a new GitHub branch at the exact verified base and local staging files; the GitHub branch is the isolated authoritative work area.
- Ruling: reuse the established reviewed transport and audit behavior. Test exact hashes, altered-source rejection, altered-proof rejection and prompt inclusion; do not execute the archived scientific programs.
- Existing authorization covers execution and publication; no renewed permission round is needed.

## Tasks

- [ ] Freeze RESULT.md, SOURCE_PACKET.json and FREEZE.json in a first immutable commit. Verify local hashes and exact remote readback.
- [ ] Adapt integration constants/header/path and branch trigger in a second commit. Use existing call_model/parse_response/accepted code. Run source-integrity rejecting controls, syntax checks and configuration review before push.
- [ ] Inspect each GitHub job and raw Gemini response. Preserve findings even on REVISE/FAIL. Inspect publication evidence before any acceptance claim; publish the verified outcome and next actual obligation.

## Review focus

- A source or proof byte change must fail integrity.
- Omitted counterexample must not pass the review packet check.
- Model/network failure must not be reported as acceptance.
- Native DERIVED_FROM_SOURCES must trigger independent assessment rather than automatic certification.
- Workflow and scientific SHAs must remain distinct and recorded.

## Ledger

Preflight: tasks share frozen document identities; workflow SCIENCE is assigned only after the freeze commit exists.
Test-first evidence: local integrity test failed because the adapted integration was absent; no science execution occurred.
