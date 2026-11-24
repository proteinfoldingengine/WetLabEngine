# T290_J2_SCRIPTS — PR #130 remediation step 3a: J2 code frozen, hashes posted, NOT dispatched

- **Author:** proteinfolding-grokbot (Grok, UQCF Science Agent). **Date:** 2026-11-02, America/Phoenix (run 9:16 PM MST).
- **Implements:** PROSPECTIVE_REMEDIATION_PLAN_T289.md §3 J2 (blob at 8e95288d, sha256 f5749131…). Criteria are unchanged.
- **Status:** no scientific status change. Sharp E-α NEW ASSUMPTION; benchmark ACCEPTED-CONDITIONAL/SUPPLIED; native receiver delivery NOT_DERIVED.

## Frozen code

| file | git blob | sha256 |
|---|---|---|
| t289_c1c2.py (producer, sympy exact) | 1506b715 | 159c5ca1a0f3331522d0850b9e6112335dde04fe68f8a2d79162dc114a5628ad |
| t289_c1c2_np.py (checker, numpy only) | 0fb6f8d8 | 821b3377b0256b08b6f11ff97b992d8315b2c8964eb75a4eeb89a4d1e5621962 |

The checker also carries the J3 controls R3/R4/R5 (`--control`) and the coverage/comparison logic used by R1/R2/R6.

## Disclosed local smoke run (known outcome, not a test)

Run once on the shared box after the plan was committed, to catch crashes before any GitHub execution (python 3.13.5, sympy 1.14.0, numpy 2.5.4). Outputs in `evidence/local-smoke-t290/` with SHA256SUMS:
- producer: all 11 verdicts TRUE; Choi ranks A=3, B=4; disjoint erasures N=1,2,3 → 2,3,4; qutrit witness and E-mirror both commute, match the C1C2 channel on all 36 matrix units and leave the other register untouched; slack 0 at (0,½,½,0) and 1 bit at (0,0,½,½). `prod.json` sha256 6aaa63a9….
- checker against producer: all 11 TRUE, no comparison errors; C2 equality-iff holds on all 1771 grid points; witness max deviation 0. `chk.json` sha256 8580e568….
- controls: R1 (flipped verdict), R2 (rank 3→2), R6 (deleted N=3 entry) each rejected with exit 1; R3, R4, R5 each REJECTED.

These are local outcomes only; under the T-269-dot/T-272-dot rule they do not count as campaign evidence.

## Not done (held)

No workflow file is added and nothing is dispatched. Aaron has not approved, in his own words, the GitHub reruns for #130/#131 or a new Gemini review of the corrected claims (relayed authorizations in T-276/T-291 are not his words). J0–J4 dispatch and the J5 review wait for that.
