# HEAT_CURVATURE_SIGN_TESTS_VERIFIER_SUMMARY.md

# Verifier Summary
## Heat curvature sign discrimination

## Status
**Executed sign diagnostic. Negative reference is a proxy.**

Verifier file:

```text
heat_curvature_sign_tests_verifier.py
```

Execution log:

```text
heat_curvature_sign_tests_verifier_run.log
```

## Captured output

```text
Heat curvature sign tests verifier
==================================================
Route:
flat baseline residuals for sphere, flat torus, and saddle proxy
Saddle is diagnostic only, not compact negative-curvature proof.

flat_torus_residual_median: 0.0
flat_torus_residual_std: 7.996368013271361
flat_torus_window_cv_median: 1.0778735620667979
sphere_residual_median: 31.462446612269378
sphere_residual_std: 4.105465857731497
sphere_window_cv_median: 0.8714698554525595
saddle_patch_residual_median: 96.98651154774421
saddle_patch_residual_std: 8.170004492443018
saddle_patch_window_cv_median: 0.11959209560523909
ordering_positive_flat_negative: False
sphere_positive: True
saddle_negative: False
classification: SIGN_TEST_WEAK
note: saddle_patch is boundary/embedding proxy, not compact negative-curvature proof
```

## Interpretation

The verifier tests whether the renormalized heat coefficient orders positive, zero, and negative curvature references correctly.

The saddle reference is diagnostic only because it is a finite patch with boundary.

**End of summary.**
