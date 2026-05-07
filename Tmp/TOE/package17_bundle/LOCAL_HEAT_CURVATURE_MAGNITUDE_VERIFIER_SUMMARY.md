# LOCAL_HEAT_CURVATURE_MAGNITUDE_VERIFIER_SUMMARY.md

# Verifier Summary
## Local heat curvature magnitude

## Status
**Executed local magnitude diagnostic.**

Verifier file:

```text
local_heat_curvature_magnitude_verifier.py
```

Execution log:

```text
local_heat_curvature_magnitude_verifier_run.log
```

## Captured output

```text
Local heat curvature magnitude verifier
==================================================
Route:
fit one scale per grid: analytic R ≈ s*(-6B), evaluate L2 error and scale stability
Diagnostic only; scale not yet theorem-derived.

N,nodes,dx,best_scale_s,relative_L2_error,corr_scaled_R,corr_raw_Rhat_R,std_Rhat,std_R
10,100,0.6283185307179586,2.516945963016627,0.40515661259092794,0.9142472965635317,0.9142472965634826,0.2016256397553771,0.55508049291539
12,144,0.5235987755982988,2.7598561718938446,0.4050904296748544,0.9142766232304923,0.9142766232304524,0.1838853428578755,0.5550804707376547
14,196,0.4487989505128276,2.969405771348945,0.4020098833971588,0.9156353278740019,0.9156353278739694,0.1711626257593192,0.555080470681643
16,256,0.39269908169872414,3.143176926809419,0.3980096158390899,0.9173812433767987,0.9173812433767716,0.16200819241977762,0.555080470681545
18,324,0.3490658503988659,3.285126623594159,0.39399915877954134,0.9191108001111532,0.9191108001111304,0.15530008854756328,0.5550804706815448
scale_cv_across_grids: 0.09300713715359335
corr_ok_all: True
final_error_lt_0p45: True
scale_cv_lt_0p25: True
classification: LOCAL_MAGNITUDE_PROMISING
```

## Interpretation

The verifier tests whether the sign-corrected local heat field recovers analytic curvature magnitude up to a fitted scale.

**End of summary.**
