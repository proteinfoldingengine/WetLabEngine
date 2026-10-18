# receiver_identification draft 8, sections 14-15 freeze: status receipt

Author: proteinfolding-grokbot. 2026-10-18 America/New_York (~10:00-10:35 ET loop).
Status: **verified (GitHub Actions verify GREEN), not yet argument-reviewed.** No milestone, native-access closure or CLOSED/CERTIFIED status is claimed. Native bridge NOT_DERIVED.

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
- Next: dispatch `gh workflow run uqcf-gem-rid8-review.yml --ref research/uqcf-overlapping-guard-exchange -f review=true` (fresh Gemini review, then publication readback), coordinated with the Gemini-review workstream so the key is not hit concurrently.
