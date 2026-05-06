# HEAT_TRACE_COEFFICIENT_ESTIMATOR_VERIFIER_SUMMARY.md

# Verifier Summary
## Heat-trace coefficient extraction

## Status
**Executed coefficient diagnostic. Not curvature proof.**

Verifier file:

```text
heat_trace_coefficient_estimator_verifier.py
```

Execution log:

```text
heat_trace_coefficient_estimator_verifier_run.log
```

## Captured output

```text
Heat trace coefficient estimator verifier
==================================================
Route:
scaled unnormalized graph Laplacian -> fixed h^2 heat window -> coefficient of t
No per-geometry calibration. Diagnostic only.

kind,intR_coeff_median,intR_coeff_std,A0_median,h_median
plane,28.262619527284944,24.654759746054616,3.8643381836962636,0.21656729111416584
sphere,-32.949554905351704,7.3467437467326935,10.576674833059272,0.3649239975171181
saddle,7.132411053602986,9.370161280352955,5.125091235113048,0.2431453612152054
perturbed_sphere,-26.988372415509854,8.114307205327256,10.852814353976832,0.37258820477121013
separation_sphere_plane_coeff: 0.9999999999999837
separation_saddle_plane_coeff: 0.5969823482817084
classification: COEFFICIENT_DIAGNOSTIC_PROMISING
```

## Interpretation

The verifier estimates the coefficient of \(t\) in:

\[
H(t)(4\pi t)^{d/2}
\sim V+\frac{t}{6}\int R\,dV+\cdots.
\]

This is closer to the action target than generic heat-trace area/slope, but remains diagnostic.

**End of summary.**
