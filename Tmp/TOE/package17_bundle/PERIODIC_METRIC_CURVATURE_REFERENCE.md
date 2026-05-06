# PERIODIC_METRIC_CURVATURE_REFERENCE.md

# Periodic Metric Curvature Reference
## Intrinsic periodic conformal-metric reference for heat-kernel curvature diagnostics

## Status
**Reference-geometry diagnostic. Not curvature closure.**

`NEGATIVE_CURVATURE_REFERENCE_FAILURE.md` showed that the saddle patch is not a valid negative-curvature reference for the heat-kernel route because it has:

```text
boundary
embedding-distance bias
noncompact support
baseline-class mismatch
```

This file replaces that with an intrinsic periodic metric reference.

The purpose is not yet to prove sign completeness, but to build a cleaner reference class for future curvature tests.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving graph curvature convergence.

---

# 1. Periodic conformal metric

Define a two-dimensional periodic metric on the torus:

\[
ds^2=e^{2\phi(x,y)}(dx^2+dy^2),
\]

where:

\[
(x,y)\in[0,2\pi)^2.
\]

For a 2D conformal metric, scalar curvature is:

\[
R=-2e^{-2\phi}\Delta\phi.
\]

This gives a known intrinsic curvature field without embedding a saddle surface in \(\mathbb R^3\).

---

# 2. Example metric

Use:

\[
\phi(x,y)=a\cos x\cos y.
\]

Then:

\[
\Delta\phi=-2a\cos x\cos y.
\]

So:

\[
R=4ae^{-2\phi}\cos x\cos y.
\]

This metric has positive and negative curvature regions, while remaining periodic and boundaryless.

By Gauss-Bonnet on the torus:

\[
\int R\,dV=0.
\]

Thus this is not a negative-total-curvature reference. It is a sign-varying local curvature reference.

---

# 3. Why this is better than a saddle patch

The periodic metric is:

```text
boundaryless
intrinsic
compact
periodic
has computable scalar curvature
shares baseline class with flat torus
```

It avoids the main saddle-patch failure modes.

---

# 4. Verifier implementation

## Status
**Implemented as `periodic_metric_curvature_reference_verifier.py`. Execution log captured.**

The verifier:
1. samples flat torus and periodic conformal metrics;
2. approximates local conformal distances;
3. applies the current \(\alpha=1\) density-normalized heat-kernel estimator;
4. subtracts flat baseline;
5. compares residual response to analytic integrated curvature.

## Captured verifier output

```text
Periodic metric curvature reference verifier
==================================================
Route:
intrinsic periodic conformal metrics with computable scalar curvature
Diagnostic only; distance approximation is local conformal.

flat_lambda1_scale: 6.270016181887365
flat_baseline_coeff: 2.582767337276003
mode,residual_coeff_median,residual_coeff_std,window_cv_median,analytic_intR_approx,analytic_meanR
flat,-0.34168572092160354,6.754878308832649,1.8461208557856414,0.0,0.0
mixed,2.886082407253057,5.375088414294631,1.0152340271110163,-1.5089871649955102,-0.16764533567304246
mostly_negative,0.4735939957973545,3.202860963003784,2.007982056347361,0.552656332057536,-0.2571429850237046
local_metric_response_detected: False
gauss_bonnet_integral_near_zero: False
classification: PERIODIC_METRIC_DIAGNOSTIC_WEAK
```

---

# 5. Interpretation

Because the conformal metric lives on a torus:

\[
\int R\,dV=0.
\]

So the integrated heat coefficient should remain near zero in the continuum if the graph estimator is measuring total curvature.

However, the local curvature field is nonzero and sign-varying.

Therefore this file primarily tests:

```text
whether the graph heat estimator responds to metric deformation while respecting zero total curvature
```

It is not yet a clean negative total curvature test.

---

# 6. What this establishes

### If promising

The periodic intrinsic metric is a better reference class than embedded saddle patches.

### If weak

The current distance/operator construction is not yet sensitive to intrinsic conformal geometry in the right way.

---

# 7. Next derivation target

If promising:

```text
LOCAL_HEAT_CURVATURE_DENSITY_TEST.md
```

because sign-varying torus metrics require local curvature-density recovery, not just global integrated curvature.

If weak:

```text
PERIODIC_METRIC_DISTANCE_FAILURE.md
```

---

# Honest status line

> `PERIODIC_METRIC_CURVATURE_REFERENCE.md` replaces the failed saddle-patch reference with an intrinsic periodic conformal metric. Because the torus has zero total curvature by Gauss-Bonnet, this is a cleaner reference for local curvature response, not a negative total-curvature proof.

**End of file.**
