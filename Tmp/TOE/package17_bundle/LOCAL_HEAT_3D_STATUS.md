# LOCAL_HEAT_3D_STATUS.md

# Local Heat 3D Status
## Status audit after dx-normalized direct heat recovery of \(R^{(3)}\)

## Status
**Major 3D local curvature diagnostic milestone. Not theorem closure. Not ADM closure.**

This file freezes the current 3D heat-kernel curvature branch after:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
LOCAL_HEAT_3D_CURVATURE_DENSITY_TEST.md
FULL_DIRECT_3D_HEAT_REFINEMENT_COLAB_RESULT.md
LOCAL_HEAT_3D_SCALE_NORMALIZATION.md
DX_NORMALIZED_3D_HEAT_COLAB_RESULT.md
```

Current classification:

```text
3D direct heat-kernel local curvature recovery is diagnostically strong after dx-normalization
```

---

# 1. 3D reference geometry

The 3D spatial reference is a periodic conformal metric:

\[
h_{ij}=e^{2\phi(x,y,z)}\delta_{ij},
\]

with:

\[
\phi(x,y,z)=a\cos x\cos y\cos z.
\]

For three spatial dimensions:

\[
R^{(3)}
=
e^{-2\phi}
\left[
-4\Delta\phi-2|\nabla\phi|^2
\right].
\]

The volume element is:

\[
dV=\sqrt h\,d^3x=e^{3\phi}dxdydz.
\]

The reference verifier passed:

```text
classification: CONFORMAL_3D_REFERENCE_READY
finite_difference_R_relative_error: 0.00584
positive_R_fraction: 0.395
negative_R_fraction: 0.605
nodes at N=24: 13,824
```

Status:

```text
3D spatial reference geometry is valid
```

---

# 2. 3D conductance mechanism

The 3D conductance precursor tested:

\[
\widehat R^{(3)}_{\mathrm{proxy},i}=-(d_i-\langle d\rangle).
\]

It passed strongly through:

```text
N=32
32,768 nodes
```

At \(N=32\):

```text
corr_scaled_R:          0.9751
corr_proxy_RdV:         0.9997
relative_L2_error:      0.2216
thresholded_sign_match: 1.0000
scale_cv_across_grids:  0.0519
```

Status:

```text
3D conductance mechanism is strong
```

---

# 3. First direct 3D heat result

The first full direct 3D heat Colab/T4 test used:

\[
K_{\mathcal G}(t,i,i)=[e^{-tL}]_{ii}.
\]

The local expansion was:

\[
K_{\mathcal G}(t,i,i)(4\pi t)^{3/2}
\approx
A_i+B_it.
\]

The raw sign-corrected estimator was:

\[
\widehat R_i^{(3)}=-6B_i.
\]

It passed shape and sign:

```text
corr_scaled_R ≈ 0.965
corr_RdV ≈ 0.9996
thresholded_sign_match = 1.0
relative_L2_error ≈ 0.26
```

But scale stability initially failed:

```text
raw_scale_cv_across_grids: 0.2675
threshold: 0.25
```

Status:

```text
3D direct heat shape/sign strong, raw scale unstable
```

---

# 4. Scale-normalization diagnosis

The raw fitted scales were:

```text
N=8:  3.704
N=10: 4.947
N=12: 6.328
N=14: 7.779
```

A power-law diagnostic found:

```text
s_N ~ N^1.327
R² ≈ 0.9999
```

Equivalently:

```text
s_N ~ dx^-1.327
```

The simplest correction tested was:

\[
\widehat R^{(3)}_{\mathrm{norm},i}
=
\frac{-6B_i}{dx}.
\]

This corresponds to absorbing approximately one grid-spacing factor.

---

# 5. dx-normalized direct 3D heat result

The dx-normalized Colab/T4 result produced:

```text
classification: DX_NORMALIZED_3D_HEAT_PROMISING
```

Raw scale CV:

```text
0.2675
```

dx-normalized scale CV:

```text
0.0681
```

Thus dx-normalization improved scale stability by about 4x.

The curvature signal was preserved:

```text
corr_R:      ~0.965
corr_RdV:    ~0.9996
sign_match:  1.0
relative_L2: ~0.26
```

Status:

```text
3D direct heat recovery is strong after dx-normalization
```

---

# 6. Current working 3D estimator

The current best diagnostic estimator is:

\[
\widehat R^{(3)}_{\mathrm{heat},i}
=
\frac{-6B_i}{dx},
\]

where:

\[
K_{\mathcal G}(t,i,i)(4\pi t)^{3/2}
\approx
A_i+B_it.
\]

This estimator is not yet theorem-derived.

It is:

```text
diagnostically validated
```

not:

```text
proved convergent
```

---

# 7. What is genuinely established

Established diagnostically:

1. A valid 3D conformal spatial reference exists.
2. The conductance mechanism extends strongly to 3D.
3. The direct 3D heat diagonal recovers analytic \(R^{(3)}\) shape.
4. It recovers curvature-density structure \(R^{(3)}dV\) extremely strongly.
5. Thresholded sign recovery passed perfectly across tested grids.
6. Raw magnitude scale drift was diagnosed.
7. dx-normalization substantially stabilized scale.
8. The best current local estimator is \((-6B_i)/dx\).

This is the strongest 3D local curvature milestone so far.

---

# 8. What remains unproved

Not established:

1. A theorem that \(R_{\mathcal G}^{(3)}\to R^{(3)}\).
2. A derivation of the sign correction.
3. A derivation of the \(1/dx\) normalization.
4. A heat-window theorem.
5. Robustness across multiple 3D conformal metrics.
6. Larger direct 3D heat refinement beyond \(N=14\).
7. ADM action integration.
8. Einstein-Hilbert limit.

Therefore this remains:

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
On a validated periodic 3D conformal spatial slice with analytic R^(3), the dx-normalized direct local heat diagonal recovers curvature shape, thresholded sign, curvature-density structure, and approximate magnitude up to stable scale across N=8,10,12,14 on T4.
```

Unsafe:

```text
Graph scalar curvature convergence is proved.
```

Unsafe:

```text
The ADM action has been recovered.
```

Unsafe:

```text
Einstein gravity has been derived.
```

---

# 10. Next proof obligations

## Obligation 1: dx-normalization theorem

Derive why the 3D graph heat diagonal requires:

\[
\frac{1}{dx}
\]

relative to the raw coefficient.

Current status:

```text
diagnostically supported, not derived
```

---

## Obligation 2: sign theorem

Derive why the correct sign is:

\[
-6B_i
\]

rather than:

\[
+6B_i.
\]

Current status:

```text
conductance-supported, not theorem-derived
```

---

## Obligation 3: heat-window theorem

Derive the valid time window:

\[
h^2\ll t\ll L_R^2.
\]

Current status:

```text
empirical fixed window
```

---

## Obligation 4: multiple 3D metrics

Test:
- \(\phi=a\cos x\cos y\cos z\)
- \(\phi=a(\cos x+\cos y+\cos z)\)
- \(\phi=a\cos 2x\cos y\cos z\)
- mixed-frequency conformal fields

Current status:

```text
one 3D conformal metric passed
```

---

## Obligation 5: ADM action integration

Connect local curvature density to:

\[
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

Current status:

```text
not yet integrated
```

---

# 11. Recommended next step

The next best file is:

```text
HEAT_CURVATURE_TO_ADM_ACTION.md
```

Reason:

We now have a plausible diagnostic for local \(R^{(3)}\). The next question is whether this can be assembled into an ADM spatial-curvature action term:

\[
S_R
=
\sum_i N_i \sqrt{h_i}\,\widehat R_i^{(3)}\,\Delta^3x
\]

and compared against the analytic reference:

\[
\int N\sqrt h\,R^{(3)}\,d^3x.
\]

This does not yet require extrinsic curvature or full field equations.

It tests the spatial-curvature action component only.

---

# 12. Report-out language

```text
Milestone: dx-normalized 3D direct heat curvature passed.

On a periodic conformal 3D spatial slice with analytic R^(3), the direct local heat diagonal recovered curvature shape at corr≈0.965, curvature density at corr≈0.9996, and thresholded sign at 1.0.

The raw scale instability was largely removed by Rhat=(-6B)/dx, dropping scale CV from 0.2675 to 0.0681.

Still not theorem closure. Next seam: integrate the local R^(3) density into the ADM spatial curvature action ∫N√hR^(3)d^3x.
```

---

# Honest final status

> `LOCAL_HEAT_3D_STATUS.md` freezes the current 3D result: dx-normalized direct heat-kernel local curvature recovery is diagnostically strong, but theorem derivation and ADM action integration remain open. The next frontier is the spatial-curvature action term.

**End of file.**
