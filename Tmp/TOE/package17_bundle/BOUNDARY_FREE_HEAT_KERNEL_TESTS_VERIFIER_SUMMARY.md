# BOUNDARY_FREE_HEAT_KERNEL_TESTS_VERIFIER_SUMMARY.md

# Verifier Summary
## Boundary-free heat-kernel curvature diagnostic

## Status
**Executed boundary-free spectral test. Weak result.**

Verifier file:

```text
boundary_free_heat_kernel_tests_verifier.py
```

Execution log:

```text
boundary_free_heat_kernel_tests_verifier_run.log
```

## Captured output

```text
Boundary-free heat-kernel tests verifier
==================================================
Route:
intrinsic distances on flat torus and sphere -> heat coefficient plateau test
No per-geometry calibration.

geometry,intR_coeff_median,intR_coeff_std,window_plateau_cv_median,h_median
flat_torus,-479.08872096067756,7.279410123940157,0.5195571444237038,0.733773190148194
sphere,-462.71443202195746,10.755680347564299,0.521337785407889,0.4086656704737675
sphere_greater_than_flat_torus: True
separation_score: 0.01738610545830482
plateau_stable: True
classification: BOUNDARY_FREE_WEAK
```

## Interpretation

The verifier compares flat torus and sphere using intrinsic distances and fixed heat-window plateau estimates.

The ordering is weakly correct, but separation is too small and coefficient sign/magnitude are wrong.

**End of summary.**
