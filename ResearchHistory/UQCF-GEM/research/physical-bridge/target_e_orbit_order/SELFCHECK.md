# Engineering handoff and review plan

Date: 2026-11-12. Request: assess the bounded answer to T-426 section 6, not a new native mechanism or research branch.

## Self-check

- The group/orbit language, fixed factorization, source pair, action, topology and weakness order are explicitly SUPPLIED.
- Equal orbits count as one premise; no inference from orbit inclusion to subgroup inclusion occurs.
- Every witness group is compact and connected. The universal orbit bound is proved analytically, not inferred from samples.
- No greatest orbit is claimed; absence of maximal orbits is expressly NOT claimed.
- Orthogonal markers with equal R marginals provide the adverse endpoint control.
- Proper-R contrast and the retained-source p-effect are separate. The latter stays 1/5, including the blind endpoint.
- The scope concerns optimized distinguishability. It does not derive a common binary effect, exclude an informationally complete measurement, or impose a new detection threshold.
- T-426's orbit-order limitation was already disclosed and is credited.
- PREREG.md and check.py were published and exactly read back before execution at b87165c31e0566b2bc6aa0d57a0d6b3666a7de1c.
- The exact algebra checker completed with 15 checks passing. It checks all 16 matrix units for the displayed family and all 16 at the blind endpoint. No sampling count is presented as a proof of the infinite orbit claim.
- No native premise was earned; NOT_DERIVED / Not claimed / scientific_breakthrough=false.
- This is new content beyond run 43217169237; no acceptance is inherited from that review.

## Review sequence

1. Freeze RESULT.md, exact CHECKS.json, and this self-check; send their identities to Engineering before the formal bot-thread result.
2. Freeze a new review packet with the new argument, checker, preregistration, output, and exact benchmark/directive sources. Reuse the already audited transport/parser; do not rerun the previously accepted note.
3. Run the frozen algebra checker and adversarial review-integrity controls in GitHub Actions, then one independent Gemini generation for this new argument.
4. Audit raw prompt, response, verdict, model and immutable inputs in a separate publication job. Preserve original artifacts and exact readback.
5. Publish the actual outcome and any required repairs. Do not claim mathematical acceptance before inspecting the raw verdict. Do not certify a numbered stage or change a merge hold.
