# DIRECT_HEAT_ADM_ACTION_COLAB_RESULT.md

# Direct Heat ADM Spatial Curvature Action Colab Result
## dx-normalized direct heat \(R^{(3)}\) assembled into the ADM spatial-curvature action term

## Status
**Major ADM spatial-curvature diagnostic milestone. Zero-mode not autonomously recovered. Not full ADM closure.**

This file records the Colab/T4 result for the direct-heat ADM spatial curvature action test.

The test used the dx-normalized direct heat estimator:

\[
\widehat R_{\mathrm{heat}}^{(3)}
=
\frac{-6B_i}{dx}.
\]

It assembled the spatial ADM curvature term:

\[
I_R
=
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x
\]

using:

\[
I_R^{\mathrm{heat}}
=
\sum_i N_i\sqrt{h_i}\widehat R_i^{(3)}dx^3.
\]

Campaign classification:

```text
DIRECT_HEAT_ADM_SPATIAL_ACTION_PROMISING
```

---

# 1. Device and setup

The run used:

```text
Torch available: True
Device: cuda
GPU: Tesla T4
```

Grid ladder:

```text
N = 8, 10, 12, 14
```

Node counts:

```text
512, 1000, 1728, 2744
```

The tested lapse fields were:

```text
unit
smooth_positive
curvature_coupled
mixed_wave
```

---

# 2. Campaign summary

The direct heat ADM spatial action test passed the mean-restored action criterion:

```text
local_corr_ok: true
mean_restored_action_ok_all: true
mean_restored_density_corr_ok_all: true
classification: DIRECT_HEAT_ADM_SPATIAL_ACTION_PROMISING
```

The strongest summary numbers:

```text
mean_restored_action_rel_error_max: 0.0387
mean_restored_density_corr_min: 0.9674
```

This is a strong pass.

---

# 3. Local curvature quality

The local dx-normalized heat estimator remained strong:

```text
local_corr_R:   ~0.965
local_corr_RdV: ~0.9996
local_L2:       ~0.26
```

This confirms that the local curvature signal survives when assembled into an action-density test.

---

# 4. Mean-restored action result

The mean-restored version used:

\[
\widehat R_{\mathrm{action}}
=
s(\widehat R-\langle\widehat R\rangle)+\langle R\rangle.
\]

This tests whether the recovered local curvature shape/density correctly assembles into:

\[
\int N\sqrt hR^{(3)}d^3x
\]

when the curvature zero mode is supplied.

It passed all lapse fields.

Representative results:

## \(N=14\), unit lapse

```text
S_true: 4.19247
S_hat_mean_restored: 4.31590
relative_error: 0.02944
density_corr: 0.96750
```

## \(N=14\), curvature-coupled lapse

```text
S_true: 9.79128
S_hat_mean_restored: 10.12883
relative_error: 0.03447
density_corr: 0.96943
```

Thus the direct heat curvature density integrates correctly at the ADM spatial-curvature level, once the mean curvature mode is supplied.

---

# 5. Zero-mode failure

The no-mean-restoration version failed strongly:

```text
no_mean_action_ok_all: false
no_mean_action_rel_error_max: 5.1261
zero_mode_status: ZERO_MODE_NOT_AUTONOMOUSLY_RECOVERED
```

This is not surprising.

The local heat estimator is currently a centered local curvature-shape estimator. It recovers:

\[
R^{(3)}-\langle R^{(3)}\rangle
\]

well, but does not autonomously recover the mean curvature mode:

\[
\langle R^{(3)}\rangle.
\]

Important nuance:

```text
no_mean density correlation still passed
```

with:

```text
no_mean_density_corr_min: 0.9683
```

So the no-mean version still gets the spatial pattern, but the integral is badly wrong because the zero mode dominates the total action.

---

# 6. What is genuinely established

Established diagnostically:

1. dx-normalized direct heat \(R^{(3)}\) remains locally accurate.
2. The recovered curvature-density pattern assembles into the ADM spatial curvature action.
3. Mean-restored action relative error is below 4%.
4. Density correlation remains above 0.967 across tested lapse fields.
5. The result survives nontrivial lapse weighting.
6. The zero-mode problem is now isolated cleanly.

This is the first direct-heat ADM spatial curvature action milestone.

---

# 7. What is not established

Not established:

1. Autonomous zero-mode recovery.
2. Full ADM action.
3. Extrinsic curvature terms:
   \[
   K_{ij}K^{ij}-K^2.
   \]
4. Lapse/shift derivation from causal slicing.
5. Action variation.
6. Einstein equations.
7. Continuum convergence theorem.

Therefore this remains:

```text
ADM spatial-curvature diagnostic
```

not:

```text
GR derivation
```

---

# 8. Updated seam status

Before this run:

```text
3D local R^(3): strong
ADM spatial action: conductance-proxy promising
```

After this run:

```text
3D local R^(3): strong
ADM spatial action: direct-heat promising
zero mode: open blocker
```

The next blocker is no longer whether local curvature integrates into the ADM spatial term.

It does.

The blocker is:

```text
how to recover the curvature zero mode without analytic mean insertion
```

---

# 9. Next target

The next best file is:

```text
ADM_SPATIAL_ZERO_MODE_RECOVERY.md
```

Purpose:

Determine whether \(\langle R^{(3)}\rangle\) can be recovered from graph observables such as:

```text
heat trace
global heat coefficient
spectral zeta coefficient
volume-normalized trace
integrated conductance deficit
curvature-density integral calibration
```

If the zero mode can be recovered, then:

\[
\int N\sqrt hR^{(3)}d^3x
\]

can become autonomous rather than mean-restored.

---

# 10. Report-out language

```text
Milestone: direct heat ADM spatial curvature action passed.

Using the dx-normalized direct heat estimator Rhat=(-6B)/dx on a 3D conformal spatial slice, the recovered local curvature density assembled into the ADM spatial curvature term ∫N√hR^(3)d^3x with <4% max relative error and density correlation >0.967 across multiple lapse fields.

The no-mean version failed, isolating the next seam: autonomous recovery of the curvature zero mode.
```

---

# Honest status line

> `DIRECT_HEAT_ADM_ACTION_COLAB_RESULT.md` records the first direct-heat ADM spatial-curvature action milestone: the recovered local \(R^{(3)}\) density assembles accurately into \(\int N\sqrt hR^{(3)}d^3x\) when the curvature mean is supplied. The next open seam is autonomous zero-mode recovery.

**End of file.**
