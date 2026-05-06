# HEAT_CURVATURE_SIGN_TESTS.md

# Heat Curvature Sign Tests
## Testing whether the renormalized heat coefficient distinguishes \(R>0\), \(R=0\), and \(R<0\)

## Status
**Sign diagnostic. Negative-curvature reference is only a proxy. Not curvature closure.**

`HEAT_CURVATURE_MAGNITUDE_TEST.md` showed that the renormalized heat-kernel curvature estimator gives a positive sphere residual and approaches the rough magnitude scale of:

\[
\int_{S^2}R\,dV=8\pi.
\]

The next test is sign discrimination.

A curvature estimator should distinguish:

\[
R>0,\qquad R=0,\qquad R<0.
\]

This file tests that requirement using:
- unit sphere as positive curvature;
- flat torus as zero curvature baseline;
- saddle patch as a diagnostic negative-curvature proxy.

The saddle patch is not a compact boundaryless negative-curvature manifold. It is only a first diagnostic.

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

# 1. Sign targets

## Positive reference

For the unit sphere:

\[
R>0.
\]

Expected:

\[
C_{\mathrm{ren}}(S^2)>0.
\]

## Zero reference

For the flat torus:

\[
R=0.
\]

Expected:

\[
C_{\mathrm{ren}}(T^2)\approx0.
\]

## Negative diagnostic proxy

For a saddle-like surface patch:

\[
z=x^2-y^2,
\]

the local Gaussian curvature is negative near the origin.

Expected diagnostic behavior:

\[
C_{\mathrm{ren}}(\mathrm{saddle})<0.
\]

Because this object has boundary and embedding effects, failure here is not final failure of the heat-kernel route.

---

# 2. Fixed estimator

The test uses the current best estimator:

```text
alpha = 1 diffusion-map density normalization
flat-torus lambda1 spectral scale
flat heat-coefficient baseline
fixed heat-window rule
```

Residual:

\[
C_{\mathrm{ren}}(M)
=
C_{\mathrm{raw}}(M)
-
C_{\mathrm{raw}}(T^2_{\mathrm{flat}}).
\]

---

# 3. Verifier implementation

## Status
**Implemented as `heat_curvature_sign_tests_verifier.py`. Execution log captured.**

The verifier reports:
- residual median;
- residual standard deviation;
- heat-window CV;
- whether the order is:

\[
C_{\mathrm{sphere}}>C_{\mathrm{flat}}>C_{\mathrm{saddle}}.
\]

## Captured verifier output

```text
Heat curvature sign tests verifier
==================================================
Route:
flat baseline residuals for sphere, flat torus, and saddle proxy
Saddle is diagnostic only, not compact negative-curvature proof.

flat_torus_residual_median: 0.0
flat_torus_residual_std: 7.996368013271361
flat_torus_window_cv_median: 1.0778735620667979
sphere_residual_median: 31.462446612269378
sphere_residual_std: 4.105465857731497
sphere_window_cv_median: 0.8714698554525595
saddle_patch_residual_median: 96.98651154774421
saddle_patch_residual_std: 8.170004492443018
saddle_patch_window_cv_median: 0.11959209560523909
ordering_positive_flat_negative: False
sphere_positive: True
saddle_negative: False
classification: SIGN_TEST_WEAK
note: saddle_patch is boundary/embedding proxy, not compact negative-curvature proof
```

---

# 4. Interpretation

A promising result requires:

```text
sphere residual > 0
flat residual ≈ 0
saddle residual < 0
```

But because the negative reference is a patch, this remains diagnostic.

The stronger future test should use a compact negative-curvature reference.

---

# 5. What this establishes

### If promising

The estimator is sensitive to curvature sign, not merely positive-vs-flat magnitude.

### If weak

The method may still work for positive curvature but does not yet support sign-complete scalar curvature.

---

# 6. Remaining proof obligations

Even if promising:

1. compact negative-curvature reference;
2. boundary correction;
3. 3D sign tests;
4. magnitude convergence;
5. baseline theorem;
6. ADM action integration.

---

# 7. Next derivation target

If promising:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
```

If weak:

```text
NEGATIVE_CURVATURE_REFERENCE_FAILURE.md
```

---

# Honest status line

> `HEAT_CURVATURE_SIGN_TESTS.md` tests sign discrimination of the renormalized heat-kernel curvature estimator. The negative-curvature case is only a saddle-patch proxy, so this is a diagnostic step, not proof of scalar curvature convergence.

**End of file.**
