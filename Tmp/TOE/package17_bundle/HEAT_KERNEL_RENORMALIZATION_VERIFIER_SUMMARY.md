# HEAT_KERNEL_RENORMALIZATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Flat-reference heat-kernel renormalization

## Status
**Executed renormalization diagnostic. Not curvature proof.**

Verifier file:

```text
heat_kernel_renormalization_verifier.py
```

Execution log:

```text
heat_kernel_renormalization_verifier_run.log
```

## Captured output

```text
Heat kernel renormalization verifier
==================================================
Route:
flat boundaryless baseline subtraction -> residual heat coefficient
No per-geometry calibration; one flat reference baseline.

baseline_flat_torus_coeff: -489.4385419608758
flat_torus_raw_median: -489.4385419608758
sphere_raw_median: -464.85901930181353
flat_torus_residual_median: 0.0
sphere_residual_median: 24.579522659062263
flat_torus_residual_std: 11.001710588927303
sphere_residual_std: 11.773338585805819
flat_torus_window_cv_median: 0.5108684097272471
sphere_window_cv_median: 0.526947040248499
sphere_residual_positive: True
residual_separation_z: 1.0792302782963896
classification: RENORMALIZED_PROMISING
```

## Interpretation

The verifier subtracts a flat boundaryless graph baseline from raw heat coefficients and checks whether the residual sphere coefficient is positive and separated.

**End of summary.**
