# NEGATIVE_CURVATURE_REFERENCE_FAILURE.md

# Negative Curvature Reference Failure
## Why the saddle-patch sign test failed and how to choose a better negative-curvature reference

## Status
**Failure analysis. Not heat-kernel route rejection.**

`HEAT_CURVATURE_SIGN_TESTS.md` tested the current renormalized heat-kernel curvature estimator on:

```text
sphere       -> positive curvature
flat torus   -> zero curvature
saddle patch -> negative-curvature proxy
```

The result was:

```text
classification: SIGN_TEST_WEAK
```

The estimator correctly separated sphere from flat:

```text
sphere_residual_median: +31.46
flat_torus_residual_median: 0.00
```

But the saddle patch did not come out negative:

```text
saddle_patch_residual_median: +96.99
saddle_negative: False
```

This file explains why that failure is not yet a decisive rejection of the heat-kernel route, and what the next negative-curvature test must require.

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

# 1. What failed

The sign ordering target was:

\[
C_{\mathrm{sphere}}>C_{\mathrm{flat}}>C_{\mathrm{saddle}}.
\]

Observed:

\[
C_{\mathrm{sphere}}>C_{\mathrm{flat}},
\]

but:

\[
C_{\mathrm{saddle}}>C_{\mathrm{flat}}.
\]

So the estimator failed the diagnostic negative-curvature sign test.

---

# 2. Why the saddle patch is a bad reference

The saddle patch was:

\[
z=x^2-y^2.
\]

This is locally negative in Gaussian curvature near the origin, but it is not a clean scalar-curvature reference for the current heat-kernel test.

## 2.1 Boundary contamination

The saddle patch is a finite patch with boundary.

Heat-kernel expansions on manifolds with boundary include boundary terms:

\[
t^{1/2},\quad t^{3/2},\quad \ldots
\]

These can dominate the same small-\(t\) regime used to estimate the curvature coefficient.

So the estimated coefficient is not purely curvature.

## 2.2 Noncompact/patch geometry

The saddle is not a compact reference geometry.

The graph is sampling a finite window, not a closed manifold.

Thus the heat trace sees:

```text
patch size
boundary
sampling support
edge effects
```

not just intrinsic curvature.

## 2.3 Extrinsic distance bias

The saddle was sampled as an embedded surface in \(\mathbb R^3\), and graph distances used ambient Euclidean distances.

But scalar curvature is intrinsic.

For small neighborhoods this may approximate intrinsic distance, but at finite graph spacing it can inject extrinsic geometry.

## 2.4 Mixed curvature over the patch

The hyperbolic paraboloid has varying curvature magnitude.

The sampled patch is not a constant-curvature reference.

So the expected integrated curvature is not a simple clean target.

## 2.5 Baseline mismatch

The baseline was a flat torus:

```text
compact
boundaryless
periodic
uniform reference
```

The saddle patch is:

```text
noncompact patch
boundary-dominated
nonperiodic
embedded
```

The baseline class \(\mathcal R\) is therefore mismatched.

This violates the baseline theorem assumptions.

---

# 3. Correct conclusion

The failed saddle result means:

```text
the current estimator has not demonstrated negative-curvature sign discrimination
```

It does not mean:

```text
the heat-kernel route is false
```

The test reference was not strong enough to support that conclusion.

---

# 4. What a valid negative-curvature test needs

A better test should satisfy as many of these as possible:

1. compact;
2. boundaryless;
3. intrinsic metric known;
4. known negative scalar curvature;
5. same dimension as positive/flat references;
6. compatible sampling rule;
7. compatible graph baseline class;
8. no per-geometry tuning.

---

# 5. Candidate negative-curvature references

## Candidate A: compact hyperbolic surface

A closed genus \(g>1\) hyperbolic surface has constant negative curvature:

\[
K=-1.
\]

For a 2D surface:

\[
R=2K=-2.
\]

By Gauss-Bonnet:

\[
\int R\,dV=4\pi\chi(M)=4\pi(2-2g).
\]

For genus \(g=2\):

\[
\int R\,dV=-8\pi.
\]

This is the cleanest target mathematically.

Problem:

```text
sampling and geodesic distances on compact hyperbolic surfaces are harder to implement
```

## Candidate B: periodic pseudosphere-like proxy

Use a periodic metric with negative curvature regions.

Pros:
- easier than compact hyperbolic surface;
- boundary-free if periodic.

Cons:
- curvature may vary;
- exact target may need numerical integration.

## Candidate C: synthetic metric grid

Instead of embedding a surface, define a 2D metric:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2)
\]

on a periodic domain.

Scalar curvature in 2D is:

\[
R=-2e^{-2\phi}\Delta\phi.
\]

This gives controlled positive/negative curvature with periodic boundaries.

Pros:
- intrinsic;
- periodic;
- exact curvature computable;
- no embedding bias.

Cons:
- requires graph distances/weights from the metric rather than Euclidean coordinates.

This is likely the best next practical route.

---

# 6. Recommended next step

The next file should be:

```text
PERIODIC_METRIC_CURVATURE_REFERENCE.md
```

Purpose:

Define a periodic 2D conformal metric:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2)
\]

with known scalar curvature:

\[
R=-2e^{-2\phi}\Delta\phi.
\]

Then test the heat-kernel estimator on:
- flat torus: \(\phi=0\);
- positive/negative mixed periodic metric;
- optionally sign-separated regions.

This avoids the boundary and embedding failures of the saddle patch.

---

# 7. Stop rules

Do not use a negative-curvature proxy for sign claims if it has:

```text
boundary
ambient-distance bias
unknown integrated curvature
baseline-class mismatch
```

Do not claim sign completeness until a compact/boundaryless intrinsic reference passes.

---

# 8. Updated status

Current heat-kernel branch status:

```text
positive curvature vs flat: promising
magnitude on sphere: promising
negative curvature sign: not yet demonstrated
```

Therefore:

```text
heat-kernel curvature route remains promising but sign-incomplete
```

---

# Honest status line

> `NEGATIVE_CURVATURE_REFERENCE_FAILURE.md` explains that the saddle-patch sign failure is caused by reference-geometry mismatch: boundary, embedding bias, noncompactness, and baseline-class mismatch. The next principled test should use a periodic intrinsic metric or compact hyperbolic reference, not an embedded saddle patch.

**End of file.**
