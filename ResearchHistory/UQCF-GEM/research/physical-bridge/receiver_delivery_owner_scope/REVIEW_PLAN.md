# Owner-scope review implementation and prospective verification plan

Date: 2026-11-01 America/Phoenix. Requested by Aaron: execute the full stack, call Gemini, wait, address findings and complete publication in this session.

Goal: independently adjudicate the exact DERIVATION.md frozen at d9b0a8e11d1425d11098101b2921289834ba034d. This is a narrow conditional ownership exclusion, not a native mechanism.
Architecture: reuse the established P1 location review integration with new pinned document identities and a new neutral prompt; preserve the old implementation unchanged. Run the complete inherited FCV verification stack before review. Independently audit all source, prompt and raw-response bytes after review, then publish immutable evidence and read it back.
Tech stack: Git, GitHub Actions, Python 3.11, sympy==1.13.3, mpmath==1.3.0, Gemini gemini-3.1-pro-preview through the existing Actions secret only.
Spec: DERIVATION.md and Aaron's full-stack instruction. Implementation method: execute inline to completion; no delegated substitute for the Gemini review.

## Frozen scope and known findings
The theorem, two analytical reconstructions, p/v calibration contradiction and W_R/W_E comparison are already known and published. They are not newly blinded or preregistered discoveries. No new finite mathematical universe, numerical threshold or physical construction is introduced. Existing FCV enumeration domains and rejection controls are rerun unchanged; these checks support inherited infrastructure, not a proof by sampling of the new universal statement. Gemini must reconstruct that statement and challenge all quantifiers, source provenance and physical scope from the full packet.

## Ordered tasks
- [ ] Freeze full sources and this prospective plan before executing new verification.
- [ ] Adapt .github/scripts/uqcf_owner_scope_review.py, uqcf_owner_scope_publication.py and uqcf_owner_scope_tests.py. Inputs: DERIVATION.md, SOURCE_PACKET.json, REVIEW_PLAN.md, FREEZE.json. Require exact bytes from the immutable scientific commit and complete source identities. Reject source/document tampering and malformed/incomplete review responses.
- [ ] Add .github/workflows/uqcf-owner-scope-review.yml on the isolated research/uqcf-owner-scope-review branch. Gate review on inherited FCV tests, v15.56 parent regression, v16.15F reproduction, unchanged FCV producer and algorithmically independent verifier, source integrity, and review rejection controls. Preserve complete logs, certificates, pinned dependency list, source snapshot, execution/workflow SHAs and manifests.
- [ ] Verify adapters locally without accessing secrets, publish the exact workflow head, and wait for Actions. GET the exact Gemini model once to verify availability, then one generateContent call with the complete proof/source packet and no previous acceptance verdict. No hidden model fallback or automatic retry. Preserve raw prompts, model metadata, request and response, including failures.
- [ ] If REVISE/FAIL: preserve the original proof and response; adjudicate each objection, add an explicit correction and new freeze where needed, and perform a fresh exact-source review. Do not relabel the original response.
- [ ] Separate publication job rebuilds prompt/request, re-fetches all immutable sources, checks all digests and identities, and requires ACCEPTED with no unresolved defect arrays. Freshly reproduce inherited deterministic certificate bytes and compare them. Archive raw evidence, source and logs.
- [ ] Download and verify artifact ZIP digests and member bytes; commit raw review, verification and publication evidence plus an acceptance receipt only if all gates pass. Fast-forward research only with an exact-head check, audit the final immutable commit, and post the result in PR111.

## Review focus and stopping boundaries
1. Complete complementary state equality versus one detector's equality; p/v mathematical calibration is not a new physical preparation assertion.
2. Full owner representation versus nonzero contrast on the original pair; do not change R or its access.
3. Retained quantum coherence is SUPPLIED, unlike native classical P1 retention.
4. Publication cannot substitute for mathematics; Gemini acceptance is analytical evidence, not physical validation.
5. Reject changed sources, incomplete model response, wrong model/run/commit, modified request or prompt, and unresolved findings.
Infrastructure failures are recorded with sanitized metadata. A reproducible technical failure may be fixed in a new commit; an unavailable model is not repeatedly retried without new evidence. No default-branch merge, secrets disclosure, new physical axiom or native-closure claim.
