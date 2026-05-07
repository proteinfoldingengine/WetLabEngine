# LOCAL_HEAT_SIGN_CONVENTION_ANALYSIS_VERIFIER_SUMMARY.md

# Verifier Summary
## Local heat sign-convention diagnostic

## Status
**Executed sign convention analysis. Sign-flipped field is strongly correlated.**

Verifier file:

```text
local_heat_sign_convention_analysis_verifier.py
```

Execution log:

```text
local_heat_sign_convention_analysis_verifier_run.log
```

## Captured output

```text
Local heat sign convention analysis verifier
==================================================
Route:
original local heat slope vs explicit sign-flipped coefficient

original_corr_R: -0.920030024111805
original_corr_RdV: -0.9903831286957712
original_sign_match: 0.09876543209876543
original_pos_gt_neg: False
original_mean_pos_R: -0.11315492524324891
original_mean_neg_R: 0.11315492524324877
sign_flipped_corr_R: 0.920030024111805
sign_flipped_corr_RdV: 0.9903831286957712
sign_flipped_sign_match: 0.9012345679012346
sign_flipped_pos_gt_neg: True
sign_flipped_mean_pos_R: 0.11315492524324891
sign_flipped_mean_neg_R: -0.11315492524324877
classification: SIGN_CONVENTION_FLIP_PROMISING
```

## Interpretation

The verifier tests whether the previous local heat-curvature anti-correlation is explained by a sign convention in the coefficient extraction.

The result supports a sign-convention correction but does not prove curvature convergence.

**End of summary.**
