# receiver_identification draft 8, sections 14-15 freeze: status receipt

Author: proteinfolding-grokbot. 2026-10-18 America/New_York (~10:00-10:35 ET loop).
Status: **verified (verify GREEN) and Gemini ACCEPTED (run 39134753017); publication readback PASS.** Updated ~10:50 ET. No milestone, native-access closure or CLOSED/CERTIFIED status is claimed. Native bridge NOT_DERIVED.

- Frozen argument: `RESULT.md` = `constructions/receiver_identification/CONSTRUCTION.md` draft 8 at `adcafca7` (sha256 `a7a0caefce8621bde682e238c2ce1b3959ce25f2896f9d0740d5d0d754b7e7f0`, 79265 bytes). Under review: sections 14-15 with notes D6, D7, D8.
- Preregistration: `FREEZE.md` committed at `4c3135c7` (sha256 `b44b3ac6…`) before any code existed. Expected values computed by hand.
- Code: `037647a1` (`.github/scripts/uqcf_rid8_{producer,checker,compare,review,publication}.py`, `.github/workflows/uqcf-gem-rid8-review.yml`).
- Actions run 39134392032 (push, head `037647a1`): verify **success**; argument-review and publication-audit skipped (review is gated to `workflow_dispatch` with `review = true`).
  - Exact instances Y1-Y9: producer = checker = preregistered values.
  - U14 (10 trees n <= 4, every l, w in {1,2}, every history of 2-3 steps, every L3 assignment): 85,410 cases, 124,128 step pairs, 48,942 strict climbs; regimes 96,450 / 2,594 / 25,084; 10,212 strict climbs with a random rest and TV preserved (GPT's case); 4,224 multi-member diluted fibers; digest `d584da88…` equal; 0 violations.
  - U15 (Z, Z_5, Z_7 law level): 5,880 cases, 330 regime-2; digest `e421b0f2…` equal; 0 violations. U15m (two-step sumset): 441 cases, 112 with a per-step regime decrease (D8(ii) non-vacuous); digest `014d9f0c…` equal; 0 violations.
  - B14 (checker only, 1,500 random cases on 5-6 node trees, quarter-denominator laws on {0,1,2}): 0 violations.
  - Controls R1-R8 all REJECTED (including draft 6's two overclaims, draft 7's witness sign, and the correlated-nuisance control). 12 tamper cases DETECTED.
- Disclosure: during local development the checker first reported a violation on every step; the cause was the checker's own unnormalized comparison of integer weight vectors (different totals), not the claim. Fixed before the code commit; the committed code is what ran in Actions.
- Gemini review: Aaron lifted the Gemini hold at 09:34 ET. Dispatched `workflow_dispatch` review=true at head `557ebf93` (same frozen RESULT and code): run 39134753017, verify success, argument-review success, publication-audit success (immutable readback PASS).
  - Model requested and returned `gemini-3.1-pro-preview`. Verdict **ACCEPTED**: 11 of 11 reconstruction items VERIFIED; findings, missing assumptions, counterexamples and limitations empty. Inserted mechanisms listed are exactly the five declared inputs (product nuisance, N_1(l), the hypothesis pair (nu, w), I*-b, occurrence). Novelty assessment: standard mathematics, new only in its application to the inherited P1 climb.
  - Hashes: review.txt `5deea38d…`, response.json `c9201508…`, prompt.txt `9d7cc2cc…`, verify compare.json `056806ae…`, freeze `b44b3ac6…`. Raw response kept in Actions artifacts only.
  - **Not adopted:** Gemini's `native_bridge_status = DERIVED_FROM_SOURCES`. It contradicts its own inserted-mechanism list (I*-b, N_1(l), product nuisance are declared, not derived). The native access bridge stays **NOT_DERIVED**.
- What this acceptance covers: the exact loss law, the both-direction equality and recoverability criteria, the cumulative regime monotonicity and the multi-step persistence of the holder's minimal sufficiency, all conditional on the declared inputs. It does not close access premise A.
