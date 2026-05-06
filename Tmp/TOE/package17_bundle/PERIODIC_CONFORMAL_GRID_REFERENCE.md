# PERIODIC_CONFORMAL_GRID_REFERENCE.md

# Periodic Conformal Grid Reference
## Deterministic intrinsic conformal-metric grid with exact curvature and volume weights

## Status
**Reference construction passed. Not heat-kernel curvature closure.**

`PERIODIC_METRIC_DISTANCE_FAILURE.md` identified that the previous periodic conformal metric test failed because the reference geometry itself was not implemented cleanly.

This file fixes the reference first.

The goal is to construct a deterministic periodic conformal metric grid with:

```text
exact R(x,y)
exact dV
Gauss-Bonnet sanity check
metric-weighted local graph stencil
local curvature-density target
```

Only after this reference passes should it be used for heat-kernel curvature diagnostics.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving graph curvature convergence.

---

# 1. Metric definition

Use the periodic conformal metric:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2),
\]

with:

\[
(x,y)\in[0,2\pi)^2.
\]

Choose:

\[
\phi(x,y)=a\cos x\cos y.
\]

The scalar curvature is:

\[
R=-2e^{-2\phi}\Delta\phi.
\]

Since:

\[
\Delta\phi=-2a\cos x\cos y,
\]

we get:

\[
R=4ae^{-2\phi}\cos x\cos y.
\]

The volume element is:

\[
dV=e^{2\phi}dxdy.
\]

Therefore:

\[
R\,dV=4a\cos x\cos y\,dxdy.
\]

The integral over the torus is exactly:

\[
\int R\,dV=0.
\]

This is the Gauss-Bonnet sanity check.

---

# 2. Deterministic grid

Use:

\[
x_i=\frac{2\pi i}{N},
\qquad
y_j=\frac{2\pi j}{N}.
\]

This avoids Monte Carlo noise in the first reference test.

Compute:

\[
R_{ij},
\qquad
dV_{ij},
\qquad
\rho_{R,ij}=R_{ij}dV_{ij}.
\]

The reference must pass:

\[
\sum_{ij} R_{ij}dV_{ij}\approx0.
\]

---

# 3. Metric-weighted stencil graph

Instead of approximate pairwise geodesics, build a local periodic graph stencil.

For an edge in the \(x\)-direction:

\[
\ell_x(i,j)=e^{\phi(i+1/2,j)}\Delta x.
\]

For an edge in the \(y\)-direction:

\[
\ell_y(i,j)=e^{\phi(i,j+1/2)}\Delta y.
\]

In the verifier, midpoint values are approximated by endpoint averages.

This graph is local, periodic, and metric-aware.

---

# 4. Verifier implementation

## Status
**Implemented as `periodic_conformal_grid_reference_verifier.py`. Execution log captured.**

The verifier checks:

1. exact Gauss-Bonnet integral;
2. finite-difference curvature against analytic curvature;
3. positive and negative curvature regions;
4. local metric stencil graph construction;
5. graph node/edge sanity;
6. metric edge-length and weight ranges.

## Captured verifier output

```text
Periodic conformal grid reference verifier
==================================================
Route:
deterministic periodic conformal grid -> exact R,dV -> Gauss-Bonnet + metric stencil sanity

N: 64
amp: 0.25
dx: 0.09817477042468103
gauss_bonnet_sum_RdV: -5.0415401020575956e-17
abs_gauss_bonnet_error: 5.0415401020575956e-17
finite_difference_R_relative_error: 0.0008029324607676338
R_min: -1.6487212707001282
R_max: 0.6065306597126334
R_mean: -0.12795523503961082
positive_R_fraction: 0.5
negative_R_fraction: 0.5
rho_positive_integral: 7.9871520503391
rho_negative_integral: -7.9871520503391
rho_total: -5.0415401020575956e-17
graph_nodes: 4096
graph_edges_undirected: 8192
edge_length_min: 0.07650462306263041
edge_length_max: 0.12598304732576038
edge_length_mean: 0.0989421536497607
weight_min: 0.6625333213599657
weight_max: 0.8591469393385237
weight_mean: 0.7742770455598758
classification: CONFORMAL_GRID_REFERENCE_READY
```

---

# 5. Result

The reference passed:

```text
classification: CONFORMAL_GRID_REFERENCE_READY
```

The Gauss-Bonnet check passed at numerical precision:

```text
abs_gauss_bonnet_error: 5.04e-17
```

The finite-difference curvature check passed:

```text
finite_difference_R_relative_error: 0.000803
```

The metric contains equal positive and negative curvature regions:

```text
positive_R_fraction: 0.5
negative_R_fraction: 0.5
```

And the curvature density integrates to zero:

```text
rho_positive_integral: +7.987
rho_negative_integral: -7.987
rho_total: ~0
```

---

# 6. Interpretation

The reference geometry is now clean.

This does not mean the heat-kernel estimator recovers local curvature.

It means the test object is mathematically valid enough for local curvature-density tests.

The next step should not be global heat coefficient recovery, because:

\[
\int R\,dV=0
\]

on the torus.

The next step should be local correlation with:

\[
R(x,y)
\]

or:

\[
R(x,y)dV.
\]

---

# 7. Next derivation target

```text
LOCAL_HEAT_CURVATURE_DENSITY_TEST.md
```

Purpose:

Test whether local graph heat-kernel features correlate with the analytic curvature field:

\[
R(x,y)
\]

or curvature density:

\[
R(x,y)dV.
\]

This moves sign testing from global integrated curvature to local curvature-density recovery.

---

# Honest status line

> `PERIODIC_CONFORMAL_GRID_REFERENCE.md` constructs and validates a clean intrinsic periodic conformal-metric grid with exact curvature, exact volume weights, Gauss-Bonnet validation, and a metric-weighted graph stencil. It is now ready for local heat-curvature density testing.

**End of file.**
