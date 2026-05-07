# LOCAL_HEAT_CURVATURE_MAGNITUDE.md

# Local Heat Curvature Magnitude
## Testing whether the sign-corrected local heat field recovers curvature magnitude up to scale

## Status
**Local magnitude diagnostic. Not curvature closure.**

`LOCAL_HEAT_SIGN_THEOREM_REVISION.md` established a corrected mechanism:

\[
d_i\sim -R_i,\qquad B_i\sim d_i,\qquad -B_i\sim R_i.
\]

The sign-corrected local estimator is:

\[
\widehat R_i=-6B_i.
\]

Previous tests showed strong shape and sign recovery. This file asks the next question:

> Does \(\widehat R_i\) recover the magnitude of analytic \(R_i\) up to a stable scale factor?

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving graph-to-continuum curvature convergence.

---

# 1. Magnitude target

On the validated conformal grid, analytic curvature is known:

\[
R(x,y)=4ae^{-2\phi}\cos x\cos y.
\]

The local heat estimator gives:

\[
\widehat R_i=-6B_i.
\]

Because the graph operator has not yet been normalized to a theorem-level Laplace-Beltrami limit, we allow one scale factor:

\[
R_i\approx s\widehat R_i.
\]

The test asks whether:
- the scaled field has low relative error;
- the scale \(s\) is stable across grids;
- correlation remains high.

---

# 2. Verifier implementation

## Status
**Implemented as `local_heat_curvature_magnitude_verifier.py`. Execution log captured.**

The verifier tests:

```text
N = 10, 12, 14, 16, 18
```

For each grid:
1. compute sign-corrected \(\widehat R_i=-6B_i\);
2. center both \(\widehat R_i\) and analytic \(R_i\);
3. fit one no-intercept scale:

\[
R\approx s\widehat R;
\]

4. compute relative \(L^2\) error;
5. compute scale stability across grids.

## Captured verifier output

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

---

# 3. Interpretation

A promising result requires:
- high correlation across all grids;
- final relative error below a loose threshold;
- scale coefficient stable across grids.

This remains diagnostic because the scale is fitted, not derived.

---

# 4. What this can establish

### If promising

The local heat estimator recovers not just sign/shape, but approximate magnitude up to a stable universal graph scale.

### If weak

The estimator is useful for local curvature pattern detection but not yet magnitude recovery.

---

# 5. Remaining proof obligations

Even if promising:

1. derive the scale \(s\);
2. prove heat-window scaling;
3. test larger grids;
4. test other conformal metrics;
5. extend to 3D;
6. integrate with ADM action.

---

# 6. Next derivation target

If promising:

```text
LOCAL_HEAT_LARGER_REFINEMENT_CAMPAIGN.md
```

If weak:

```text
LOCAL_HEAT_MAGNITUDE_FAILURE.md
```

---

# Honest status line

> `LOCAL_HEAT_CURVATURE_MAGNITUDE.md` tests whether the sign-corrected local heat curvature field recovers analytic curvature magnitude up to a stable scale. It is a magnitude diagnostic, not a proof of curvature convergence.

**End of file.**
