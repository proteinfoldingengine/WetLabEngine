# CAUSAL_SLICE_CURVATURE_VERIFIER_SUMMARY.md

# Verifier Summary
## Curvature proxies from causal-slice metric sequence

## Status
**Executed structural verifier. Not full curvature proof.**

Verifier file:

```text
causal_slice_curvature_verifier.py
```

Execution log:

```text
causal_slice_curvature_verifier_run.log
```

## Captured output

```text
Causal slice curvature verifier
==================================================
Route:
slice Lorentzian metrics -> finite slice variation -> curvature proxies
This is not full Riemann/Ricci curvature.

PASS: 80.0
SOFT_FAIL: 2.5
HARD_FAIL: 17.5
n_metric_slices_median: 9.0
median_h_condition_median: 1.9882031855720235
median_metric_velocity_median: 57.63886410740121
median_metric_acceleration_median: 91.09527058275171
median_log_volume_curvature_median: 0.879519800945336
finite_fraction_median: 1.0
```

## Interpretation

The verifier tests:
- finite metric slices,
- finite condition numbers,
- metric velocity,
- metric acceleration,
- log-volume second variation.

These are curvature-like diagnostics for the causal-slice route, not full Riemann/Ricci curvature.

**End of summary.**
