# NORMALIZED_LAPLACIAN_HEAT_CURVATURE_RETEST_VERIFIER_SUMMARY.md

# Verifier Summary
## Normalized Laplacian heat-curvature retest

## Status
**Executed operator-corrected heat curvature diagnostic.**

Verifier file:

```text
normalized_laplacian_heat_curvature_retest_verifier.py
```

Execution log:

```text
normalized_laplacian_heat_curvature_retest_verifier_run.log
```

## Captured output

```text
Normalized Laplacian heat curvature retest verifier
==================================================
Route:
alpha=1 diffusion normalization + universal flat-torus lambda1 scale -> heat coefficient residual
No per-geometry calibration.

flat_lambda1_scale_factor: 4.941419254104508
geometry,raw_coeff_median,scaled_coeff_median,scaled_coeff_std,scaled_window_cv,raw_lambda1_median,h_median
flat_torus,-834.0126952117635,-18.371757158652223,6.335146139278723,1.1738219576530793,0.19435153865372568,0.6390814966778808
sphere,-818.1849778024426,14.393523597331072,3.748908910000576,5.411075029976456,0.4334295985218092,0.37236162746258095
flat_scaled_residual_median: 1.7763568394002505e-15
sphere_scaled_residual_median: 32.7652807559833
sphere_residual_positive: True
residual_separation_z: 3.2492167680423125
classification: NORMALIZED_HEAT_RETEST_PROMISING
```

## Interpretation

The verifier uses \(\alpha=1\) diffusion normalization and one universal flat-torus eigenvalue scale correction, then retests heat coefficient residuals.

**End of summary.**
