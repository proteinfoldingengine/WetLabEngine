# v15.38 Pre-Time Response Axiom Admissibility — Implementation Plan

**Date:** 2026-09-18
**Base:** `2d7950d7c151a386654e044af6d092bf68317c59`

1. Pin v15.25/v15.26 canary guardrails, v15.37 branch-stop result, and exact v15.28 representation machinery.
2. Confirm RED on absent `response_axiom_admissibility_gate`.
3. Rebuild exact cycle carriers at L=5,7,9; require dimensions 26,50,82.
4. Build canonical adjacency independently at each size and verify exact translation/D4 covariance.
5. Evaluate three predeclared target-blind polynomial controls with one unchanged coefficient vector across all sizes.
6. Verify the three accepted controls are projectively distinct on L=7 and use no eigenspectrum query or spectral-edge parameter.
7. Reject five preregistered contaminated controls for their intended primary reasons.
8. Require structural falsifier, locked future test, projective-scale discipline and full gravity/source-selection firewall.
9. Run inherited v15.36/v15.37 regressions.
10. Freeze ledger only after GREEN, then exact-head byte replay.

RED receipt: run `35409808140`, job `105806990302`, head `9d8432e83d27295028ac2158287709e53aed0e49`, intended missing-module failure.
