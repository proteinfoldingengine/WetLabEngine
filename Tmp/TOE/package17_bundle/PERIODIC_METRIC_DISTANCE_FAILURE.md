# PERIODIC_METRIC_DISTANCE_FAILURE.md

# Periodic Metric Distance Failure
## Why the intrinsic conformal torus reference failed and what must be fixed before sign testing

## Status
**Reference-construction failure analysis. Not heat-kernel route rejection.**

`PERIODIC_METRIC_CURVATURE_REFERENCE.md` attempted to replace the failed embedded saddle patch with an intrinsic periodic conformal metric:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2).
\]

This was the right first-principles direction, because it avoids:

```text
boundary
noncompact support
ambient saddle embedding
baseline-class mismatch
```

But the verifier returned:

```text
classification: PERIODIC_METRIC_DIAGNOSTIC_WEAK
```

with:

```text
local_metric_response_detected: False
gauss_bonnet_integral_near_zero: False
```

This file diagnoses the failure.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving or disproving graph curvature convergence.

---

# 1. What was attempted

The reference metric was:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2)
\]

on a periodic domain:

\[
(x,y)\in[0,2\pi)^2.
\]

For:

\[
\phi(x,y)=a\cos x\cos y,
\]

the scalar curvature is:

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
R\,dV
=
4a\cos x\cos y\,dxdy.
\]

The integral over the torus is exactly:

\[
\int_0^{2\pi}\int_0^{2\pi}4a\cos x\cos y\,dxdy=0.
\]

So Gauss-Bonnet requires:

\[
\int R\,dV=0.
\]

---

# 2. What failed

The verifier did not recover this clean zero integral.

That means the reference implementation failed before the heat-kernel estimator could be meaningfully judged.

The failure is not:

```text
heat-kernel curvature route rejected
```

The failure is:

```text
periodic conformal metric reference not implemented with sufficient intrinsic accuracy
```

---

# 3. Root causes

## 3.1 Approximate pairwise distance was not geodesic distance

The verifier used:

\[
d_{ij}\approx e^{(\phi_i+\phi_j)/2}d_{0,ij}.
\]

This is only a crude local conformal correction.

It is not the geodesic distance of:

\[
ds^2=e^{2\phi}(dx^2+dy^2).
\]

For finite graph spacing, this approximation can distort the metric.

## 3.2 Sampling was not volume-weighted

Uniform sampling in coordinates:

\[
dxdy
\]

is not uniform sampling in Riemannian volume:

\[
dV=e^{2\phi}dxdy.
\]

If the graph Laplacian assumes sampling from volume measure but the points are sampled uniformly in coordinates, density normalization may not fully correct the bias.

## 3.3 Gauss-Bonnet sanity check was too noisy

The analytic integral is exactly zero:

\[
\int R\,dV=0.
\]

But the Monte Carlo estimate was not near zero.

That suggests the reference sampling/weighting procedure is not accurate enough.

## 3.4 Global heat coefficient is the wrong first observable

For a conformal metric on a torus, total curvature is zero.

So a global heat coefficient cannot distinguish sign-varying local curvature unless we recover local curvature density.

The first test should not be:

```text
global coefficient response
```

It should be:

```text
local curvature-density correlation
```

---

# 4. Correct first-principles correction

Before using periodic metrics for sign tests, we need a clean reference-construction pipeline.

## Step 1: deterministic grid instead of random sampling

Use a uniform periodic grid:

\[
x_i=\frac{2\pi i}{N},
\qquad
y_j=\frac{2\pi j}{N}.
\]

This removes Monte Carlo noise from Gauss-Bonnet checks.

## Step 2: exact analytic curvature field

Compute:

\[
R(x,y)=-2e^{-2\phi(x,y)}\Delta\phi(x,y).
\]

For:

\[
\phi=a\cos x\cos y,
\]

use:

\[
R=4ae^{-2\phi}\cos x\cos y.
\]

## Step 3: exact volume weights

Use:

\[
w_{ij}=e^{2\phi(x_i,y_j)}\Delta x\Delta y.
\]

Then verify:

\[
\sum_{ij}R_{ij}w_{ij}\approx0.
\]

This must pass before heat-kernel tests.

## Step 4: graph metric from weighted local stencil

Instead of pairwise conformal distance approximation, build the graph from a local stencil with edge lengths:

\[
\ell_x(i,j)=e^{\phi(i+1/2,j)}\Delta x,
\]

\[
\ell_y(i,j)=e^{\phi(i,j+1/2)}\Delta y.
\]

This gives a graph-native metric consistent with the conformal metric.

## Step 5: local curvature-density target

Because total curvature is zero, define local target:

\[
\rho_R(x,y)=R(x,y)\sqrt h.
\]

Then compare local graph heat/curvature density to:

\[
R(x,y)
\]

or:

\[
R(x,y)\sqrt h.
\]

---

# 5. New verifier requirements

The next verifier must first pass reference sanity checks:

1. deterministic grid;
2. exact volume weights;
3. Gauss-Bonnet integral near zero;
4. curvature field has both signs;
5. local stencil edge lengths reflect conformal metric;
6. no ambient embedding distances.

Only then should we test heat-kernel curvature.

---

# 6. Revised next target

The next file should be:

```text
PERIODIC_CONFORMAL_GRID_REFERENCE.md
```

Purpose:

Build a deterministic periodic conformal metric grid with:
- exact \(R(x,y)\);
- exact \(dV\);
- Gauss-Bonnet check;
- metric-weighted local graph stencil;
- local curvature-density target.

This is a reference-construction file, not yet a heat-kernel curvature file.

---

# 7. What not to do

Do not continue using:

```text
d_ij ≈ exp((phi_i+phi_j)/2) d0_ij
```

as if it were geodesic distance.

Do not use random sampling for the first Gauss-Bonnet sanity check.

Do not expect a global heat coefficient to detect sign-varying curvature on a torus with total curvature zero.

Do not treat this failure as a failure of the heat-kernel route.

---

# 8. Current status of sign testing

Current status:

```text
positive curvature vs flat: promising
sphere magnitude: promising
negative/local sign testing: blocked by reference construction
```

So the next bottleneck is not the estimator.

It is:

```text
build a clean intrinsic sign-varying reference geometry
```

---

# Honest status line

> `PERIODIC_METRIC_DISTANCE_FAILURE.md` identifies the failure in the periodic conformal metric test: the reference geometry was not implemented with sufficient intrinsic accuracy. The next step is a deterministic periodic conformal grid with exact curvature, exact volume weights, Gauss-Bonnet validation, and metric-weighted graph stencils.

**End of file.**
