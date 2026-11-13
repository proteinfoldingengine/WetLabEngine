# Quiet-reference proof review implementation plan

> **For agentic workers:** Execute this bounded plan inline, with independent whole-argument and code review. Steps use checkbox tracking.

**Goal:** Publish and challenge one explicitly conditional fixed-receiver proof, preserving exact review evidence.
**Architecture:** Freeze the analytical argument in a PR branch; pin its bytes and a small set of direct antecedents in the established analytical-review transport. Run one Gemini review and a separate publication audit on GitHub, then preserve the original artifacts and read back the final PR head.
**Tech Stack:** Python 3.11 standard library, existing pinned Gemini transport, GitHub Actions and Git object APIs.
**Spec:** `ARGUMENT.md` in this directory.

## Global constraints

- Integrated parent: `2ab565c3f5bf10305a96ddeef30901de49959ba5`.
- Keep the same proper qubit receiver and fixed effect; QR and the invoked rank condition are new assumptions.
- No scientific execution, finite enumeration, inherited-stack recertification, source-history replacement, merge or stage closure.
- All proposed additions go through a PR. Reuse immutable helper blobs; one model generation, no retry generation.
- User delegated the approach and already authorized research publication and Gemini review. Proceed without another planning approval loop.

## Review focus

The existing review transport has controls for document substitution, missing/duplicate documents, altered remote bytes, truncated or wrong-model responses, altered verdicts, wrong run identity and unsupported native promotion. Preserve those behavioral tests in this adaptation. Add no scientific fixtures pretending to prove the universal theorem. Pin the requested argument independently of the response; verify both original downloaded ZIPs and all final committed bytes.

## Task 1: Freeze the analytical claim

- [ ] Complete targeted overlap check against T273-R, fixed P1 receiver pair/effect and prior quiet/reference candidates.
- [ ] Preserve the proof, assumption ledger, sharpness construction, rejecting countermodels and scoped overlap note.
- [ ] Create a draft PR from the exact integrated parent. No workflow or model execution at this freeze.

## Task 2: Bind the established review transport

Files: `.github/scripts/uqcf_quiet_reference_review.py`, `.github/scripts/uqcf_quiet_reference_tests.py`, `.github/workflows/uqcf-quiet-reference-review.yml`, and `review/SOURCE_PACKET.json` under this directory.

Interfaces: `load_packet(raw, expected_sha, remote=None)` validates immutable documents; `prompt_for(packet)` reconstructs exact review input; `audit_review(directory, packet, expected_identity, packet_sha256)` validates the saved raw response and its provenance; `main()` exposes review/publication phases. Reuse the prior Target E controller's validated model transport, removing its unrelated algebra execution/receipt dependency.

- [ ] Adapt behavioral controls first and run them; expected RED: absent new controller.
- [ ] Adapt the existing controller to the frozen quiet-reference documents and adversarial questions; no new scientific checker.
- [ ] Run the complete controller-specific suite; expected GREEN. Preserve RED/GREEN logs.
- [ ] Obtain a fresh whole-change code review before starting the paid model call.
- [ ] Commit the packet/controller/workflow. Workflow triggers only its dedicated branch/path, never the research branch.

## Task 3: Complete independent review and publication

- [ ] Inspect exact run/checkout/workflow identities and all job logs. Preserve failure evidence if present; do not generate another response merely to change a verdict.
- [ ] Download original review/publication ZIPs; verify artifact digests, exact prompt/request/raw-response/parsed-verdict relationship and immutable document identities.
- [ ] If accepted, append an adjudication explicitly preserving NOT_DERIVED and all limitations; if not, preserve and answer the actual findings before any revised review.
- [ ] Commit durable artifacts and checksums, read back every final addition, mark the PR ready only if the declared review/publication contract passes, and post the result to the bot thread.

## Execution notes

This plan concerns an analytical note and its existing review plumbing, not a numbered retained-research campaign. The scientific proof was known before freeze. Local isolated file assembly plus Git object APIs supplies the PR isolation; no shared worktree/index edits are needed. The unchanged foundational simulations are not rerun or represented as recertified. The exact independent review and publication audit are the validation appropriate to this new claim.
