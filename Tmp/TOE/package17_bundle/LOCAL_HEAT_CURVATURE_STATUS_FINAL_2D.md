# LOCAL_HEAT_CURVATURE_STATUS_FINAL_2D.md

# Local Heat Curvature Status Final 2D
## Final 2D status audit after full direct heat-diagonal Colab refinement

## Status
**Major 2D local curvature diagnostic milestone. Not theorem closure. Not GR derivation.**

This file freezes the 2D local heat-kernel curvature-density branch after the full direct Colab/T4 heat-diagonal refinement campaign.

The central result is:

```text
FULL_DIRECT_HEAT_REFINEMENT_PROMISING
```

This is the strongest local curvature-density result so far.

---

# 1. Validated reference geometry

The reference geometry is a deterministic periodic conformal torus:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2),
\]

with:

\[
\phi(x,y)=a\cos x\cos y.
\]

The analytic scalar curvature is:

\[
R=-2e^{-2\phi}\Delta\phi
=
4ae^{-2\phi}\cos x\cos y.
\]

The volume element is:

\[
dV=e^{2\phi}dxdy.
\]

The reference passed:

```text
Gauss-Bonnet error: ~5e-17
finite-difference R relative error: ~8e-4
positive_R_fraction: 0.5
negative_R_fraction: 0.5
```

Status:

```text
2D intrinsic reference geometry is valid
```

---

# 2. Local heat estimator

The direct local heat diagonal is:

\[
K_{\mathcal G}(t,i,i)=[e^{-tL}]_{ii}.
\]

The fitted local expansion is:

\[
K_{\mathcal G}(t,i,i)(4\pi t)
\approx
A_i+B_it.
\]

The sign-corrected local estimator is:

\[
\widehat R_i=-6B_i.
\]

The sign correction is supported by the conductance mechanism:

\[
d_i\sim -R_i,
\]

\[
B_i\sim d_i,
\]

therefore:

\[
-B_i\sim R_i.
\]

Status:

```text
sign correction has mechanistic support but still needs theorem derivation
```

---

# 3. Small-grid direct local heat results

Earlier direct local tests showed:

```text
corr_R:   ~0.914 to 0.919
corr_RdV: ~0.988 to 0.990
```

Thresholded sign recovery passed after excluding near-zero curvature nodes:

```text
threshold_0p10_sign_ok_all: True
threshold_0p10_corr_ok_all: True
threshold_0p10_order_ok_all: True
threshold_0p10_retained_ok_all: True
```

Magnitude up to a fitted scale was promising:

```text
classification: LOCAL_MAGNITUDE_PROMISING
scale_cv_across_grids: 0.093
final relative L2 error: ~0.394
```

---

# 4. Conductance-supported extended refinement

The conductance surrogate:

\[
-(d_i-\langle d\rangle)
\]

was tested through:

```text
N=64
4096 nodes
```

It produced:

```text
classification: CONDUCTANCE_EXTENDED_REFINEMENT_PROMISING
corr_scaled_R at N=64: 0.9334
relative_L2_error at N=64: 0.3587
thresholded_sign_match at N=64: 0.9874
scale_cv_across_grids: 0.0324
```

This supported the mechanism, but did not replace the full heat-diagonal test.

---

# 5. Full direct Colab/T4 heat-diagonal refinement

The decisive follow-up was run on:

```text
Device: cuda
GPU: Tesla T4
```

Grid ladder:

```text
N = 24, 32, 40, 48
```

Node counts:

```text
576, 1024, 1600, 2304
```

Estimator:

\[
\widehat R_i=-6B_i
\]

from the actual direct heat diagonal:

\[
[e^{-tL}]_{ii}.
\]

Campaign classification:

```text
FULL_DIRECT_HEAT_REFINEMENT_PROMISING
```

Campaign summary:

```text
corr_ok_all: true
thresholded_sign_ok_all: true
retained_ok_all: true
final_error_lt_0p45: true
scale_cv_lt_0p25: true
```

Scale stability:

```text
scale_cv_across_grids: 0.0364
```

---

# 6. Key Colab numeric trend

Correlation with analytic curvature improved with refinement:

```text
N=24: corr_scaled_R = 0.9232
N=32: corr_scaled_R = 0.9264
N=40: corr_scaled_R = 0.9281
N=48: corr_scaled_R = 0.9291
```

Correlation with curvature density was extremely high:

```text
N=24: corr_RdV = 0.9915
N=32: corr_RdV = 0.9926
N=40: corr_RdV = 0.9932
N=48: corr_RdV = 0.9935
```

Relative \(L^2\) error improved:

```text
N=24: 0.3843
N=32: 0.3766
N=40: 0.3724
N=48: 0.3699
```

Thresholded sign recovery stayed strong:

```text
N=24: 1.0000
N=32: 0.9895
N=40: 0.9806
N=48: 0.9910
```

---

# 7. What is now genuinely established

Established diagnostically:

1. The 2D conformal torus reference is mathematically clean.
2. The local heat diagonal contains a strong scalar-curvature signal.
3. The sign-corrected estimator tracks analytic \(R(x,y)\).
4. It tracks curvature density \(R\,dV\) even more strongly.
5. Thresholded sign recovery passes.
6. Magnitude recovery up to a stable scale is promising.
7. Direct heat-diagonal refinement passes through \(N=48\).
8. The conductance mechanism explains the sign reversal and scales through \(N=64\).

This is the strongest 2D local curvature-density milestone in the program.

---

# 8. What is not yet established

Not established:

1. A theorem that \(R_{\mathcal G}\to R\).
2. A derivation of the sign correction.
3. A derivation of the scale factor.
4. A theorem for the heat-time window.
5. Robustness across multiple conformal metrics.
6. Extension to 3D spatial scalar curvature \(R^{(3)}\).
7. Integration into the ADM action.
8. Recovery of Einstein field equations.

Therefore, this remains:

```text
major diagnostic milestone
```

not:

```text
GR derivation
```

---

# 9. Safe claim

Safe:

```text
On a validated 2D periodic conformal reference with exact analytic curvature, the direct local heat-kernel diagonal recovers curvature shape, thresholded sign, and magnitude up to a stable scale across N=24,32,40,48 on T4.
```

Unsafe:

```text
Graph scalar curvature convergence is proved.
```

Unsafe:

```text
The Einstein-Hilbert action has been recovered.
```

Unsafe:

```text
GR has been derived.
```

---

# 10. Next proof obligations

## Obligation 1: Sign theorem

Derive:

\[
\widehat R_i=-6B_i
\]

from the discrete operator and graph convention.

Current status:

```text
mechanistically supported, not theorem-derived
```

---

## Obligation 2: Scale theorem

Derive the fitted scale:

\[
R_i\approx s\widehat R_i.
\]

Current status:

```text
stable diagnostic scale, not derived
```

---

## Obligation 3: Heat-window theorem

Derive a valid heat-time window:

\[
h^2\ll t\ll L_R^2.
\]

Current status:

```text
fixed empirical window
```

---

## Obligation 4: Other 2D metrics

Test multiple conformal functions:

```text
phi = a cos x cos y
phi = a(cos x + cos y)
phi = a cos 2x cos y
mixed-frequency metrics
```

Current status:

```text
single conformal metric passed
```

---

## Obligation 5: 3D spatial extension

GR needs:

\[
R^{(3)}.
\]

Current status:

```text
2D only
```

---

## Obligation 6: ADM action integration

Need to connect local curvature density to:

\[
\int N\sqrt h\,R^{(3)}\,d^3x.
\]

Current status:

```text
not yet integrated
```

---

# 11. Recommended next step

The next best technical target is:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
```

Reason:

The 2D local result is strong enough to justify moving toward the actual GR spatial curvature object:

\[
R^{(3)}.
\]

A 3D test should start with:

```text
flat 3-torus
3D conformal metric on periodic cube
known scalar curvature formula
local heat diagonal
thresholded sign and magnitude recovery
```

Alternative next target:

```text
HEAT_CURVATURE_TO_ADM_ACTION.md
```

But this should wait until at least one 3D spatial curvature diagnostic exists.

---

# 12. Report-out language

```text
Milestone: full direct heat-kernel local curvature recovery passed in 2D.

On a validated intrinsic conformal torus with exact analytic R(x,y), the direct local heat diagonal [exp(-tL)]_ii recovered curvature shape, thresholded sign, and magnitude up to a stable scale across N=24,32,40,48 on T4.

Best grid: corr(Rhat,R)=0.929, corr(Rhat,R dV)=0.993, thresholded sign match=0.991, relative L2 error=0.370, scale CV=0.036.

Still not theorem closure. Next step: extend to 3D spatial curvature R^(3).
```

---

# Honest final status

> `LOCAL_HEAT_CURVATURE_STATUS_FINAL_2D.md` freezes the strongest 2D result: full direct heat-kernel local curvature-density recovery is diagnostically strong through \(N=48\), with shape, sign, and magnitude up to stable scale. The next frontier is \(R^{(3)}\) in 3D spatial slices.

**End of file.**
