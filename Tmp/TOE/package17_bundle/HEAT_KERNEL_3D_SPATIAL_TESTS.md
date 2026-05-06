# HEAT_KERNEL_3D_SPATIAL_TESTS.md

# Heat Kernel 3D Spatial Tests
## Building the 3D conformal spatial reference for \(R^{(3)}\)

## Status
**3D reference construction. Not heat-kernel curvature closure.**

`LOCAL_HEAT_CURVATURE_STATUS_FINAL_2D.md` froze the strongest 2D local curvature-density result so far.

The next frontier is the actual GR spatial scalar curvature object:

\[
R^{(3)}.
\]

This file begins the 3D branch by constructing a clean periodic 3D conformal reference geometry.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving ADM or Einstein-Hilbert convergence.

---

# 1. 3D conformal metric

Use a periodic 3D conformal metric:

\[
g_{ij}=e^{2\phi(x,y,z)}\delta_{ij}.
\]

Choose:

\[
\phi(x,y,z)=a\cos x\cos y\cos z.
\]

For \(n=3\), under conformal rescaling from flat space:

\[
R_g=e^{-2\phi}\left[-4\Delta\phi-2|\nabla\phi|^2\right].
\]

This gives an analytic spatial scalar curvature field:

\[
R^{(3)}(x,y,z).
\]

The volume element is:

\[
dV=\sqrt g\,d^3x=e^{3\phi}dxdydz.
\]

---

# 2. Why this is the correct next branch

The ADM action contains:

\[
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

The 2D branch tested local scalar curvature recovery on a conformal torus.

The 3D branch must now test whether the same heat-kernel/local-diagonal machinery can recover:

\[
R^{(3)}(x,y,z)
\]

on a known spatial slice.

---

# 3. Reference sanity checks

Before running heat-kernel diagnostics, the reference must pass:

1. analytic \(R^{(3)}\) computation;
2. finite-difference \(R^{(3)}\) consistency;
3. exact volume weights;
4. positive and negative curvature regions;
5. periodic metric-weighted local stencil.

Unlike the 2D torus, there is no Gauss-Bonnet constraint forcing:

\[
\int R\,dV=0.
\]

So \(\int R\,dV\) is recorded, not required to vanish.

---

# 4. Metric-weighted 3D stencil

For each local edge:

\[
\ell=e^{\phi_{\mathrm{mid}}}\Delta x.
\]

Weight:

\[
w=\exp\left(-\frac{\ell^2}{4\Delta x^2}\right).
\]

Use periodic 6-neighbor connectivity.

This is the 3D analogue of the 2D stencil.

---

# 5. Verifier implementation

## Status
**Implemented as `heat_kernel_3d_spatial_reference_verifier.py`. Execution log captured.**

The verifier checks:
- analytic \(R^{(3)}\);
- finite-difference \(R^{(3)}\) relative error;
- sign distribution;
- volume-weighted curvature;
- metric stencil edge/weight ranges.

## Captured verifier output

```text
3D conformal spatial reference verifier
==================================================
Route:
periodic 3D conformal metric -> analytic R^(3), dV, finite-difference sanity, metric stencil

N: 24
amp: 0.15
dx: 0.2617993877991494
int_R_dV: 4.192473805996352
mean_R: -0.08491032800191478
R_min: -2.4297458536368053
R_max: 1.333472797227092
positive_R_fraction: 0.3949652777777778
negative_R_fraction: 0.6050347222222222
rho_positive_integral: 59.16038062402014
rho_negative_integral: -54.96790681802379
finite_difference_R_relative_error: 0.0058354214932062045
nodes: 13824
undirected_edges: 41472
edge_length_min: 0.22590940996964828
edge_length_max: 0.30339116666816957
edge_length_mean: 0.262161552391206
weight_min: 0.7148058742762994
weight_max: 0.8301460895027147
weight_mean: 0.7779947054789503
classification: CONFORMAL_3D_REFERENCE_READY
```

---

# 6. Interpretation

A ready reference means:

```text
3D conformal spatial slice is mathematically clean enough for direct local heat testing
```

It does not mean heat curvature recovery has passed.

---

# 7. Next derivation target

If ready:

```text
LOCAL_HEAT_3D_CURVATURE_DENSITY_TEST.md
```

Purpose:

Compute the direct local heat diagonal:

\[
[e^{-tL}]_{ii}
\]

and test whether a sign/scaled local estimator recovers analytic:

\[
R^{(3)}(x,y,z).
\]

If weak:

```text
CONFORMAL_3D_REFERENCE_FAILURE.md
```

---

# Honest status line

> `HEAT_KERNEL_3D_SPATIAL_TESTS.md` begins the 3D spatial curvature branch by constructing a periodic conformal 3D reference with analytic \(R^{(3)}\), volume weights, and metric-weighted graph stencils. It prepares the path toward the ADM spatial curvature term but does not yet recover it.

**End of file.**
