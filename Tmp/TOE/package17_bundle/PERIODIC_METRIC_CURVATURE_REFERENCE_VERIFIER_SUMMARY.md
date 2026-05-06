# PERIODIC_METRIC_CURVATURE_REFERENCE_VERIFIER_SUMMARY.md

# Verifier Summary
## Periodic intrinsic conformal-metric reference

## Status
**Executed reference diagnostic. Not curvature proof.**

Verifier file:

```text
periodic_metric_curvature_reference_verifier.py
```

Execution log:

```text
periodic_metric_curvature_reference_verifier_run.log
```

## Captured output

```text
Periodic metric curvature reference verifier
==================================================
Route:
intrinsic periodic conformal metrics with computable scalar curvature
Diagnostic only; distance approximation is local conformal.

flat_lambda1_scale: 6.270016181887365
flat_baseline_coeff: 2.582767337276003
mode,residual_coeff_median,residual_coeff_std,window_cv_median,analytic_intR_approx,analytic_meanR
flat,-0.34168572092160354,6.754878308832649,1.8461208557856414,0.0,0.0
mixed,2.886082407253057,5.375088414294631,1.0152340271110163,-1.5089871649955102,-0.16764533567304246
mostly_negative,0.4735939957973545,3.202860963003784,2.007982056347361,0.552656332057536,-0.2571429850237046
local_metric_response_detected: False
gauss_bonnet_integral_near_zero: False
classification: PERIODIC_METRIC_DIAGNOSTIC_WEAK
```

## Interpretation

The verifier tests intrinsic periodic conformal metrics with computable scalar curvature.

Because total curvature on the torus is zero, this reference is useful for local curvature-response testing, not negative-total-curvature proof.

**End of summary.**
