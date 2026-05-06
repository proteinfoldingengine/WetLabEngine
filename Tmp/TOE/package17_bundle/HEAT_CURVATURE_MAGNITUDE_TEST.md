# HEAT_CURVATURE_MAGNITUDE_TEST.md

# Heat Curvature Magnitude Test
## Testing whether the renormalized sphere coefficient approaches \(\int_{S^2} R\,dV=8\pi\)

## Status
**Magnitude diagnostic. Not curvature closure.**

`HEAT_KERNEL_BASELINE_UNIVERSALITY_TEST.md` supported the flat-baseline theorem candidate at the diagnostic level.

The next question is stronger:

> Does the renormalized heat coefficient approach the known continuum magnitude?

For the unit two-sphere:

\[
R=2,
\qquad
\mathrm{Area}(S^2)=4\pi,
\]

so:

\[
\int_{S^2}R\,dV=8\pi.
\]

This file tests whether the current estimator moves toward that value without per-sphere fitting.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving curvature convergence.

---

# 1. Fixed estimator

The estimator uses the current best rule:

```text
alpha = 1 diffusion-map density normalization
universal flat-torus lambda1 spectral scale
flat heat-coefficient baseline subtraction
fixed heat-window rule
no per-sphere magnitude fit
```

The residual is:

\[
C_{\mathrm{ren}}(S^2)
=
C_{\mathrm{raw}}(S^2)
-
C_{\mathrm{raw}}(T^2_{\mathrm{flat}}).
\]

Target:

\[
C_{\mathrm{ren}}(S^2)\rightarrow 8\pi.
\]

---

# 2. Verifier implementation

## Status
**Implemented as `heat_curvature_magnitude_test_verifier.py`. Execution log captured.**

The verifier tests:

```text
n = 70, 110, 160
```

and reports:
- flat spectral scale;
- flat baseline;
- sphere residual;
- residual standard deviation;
- relative error to \(8\pi\);
- heat-window CV.

## Captured verifier output

```text
Heat curvature magnitude test verifier
==================================================
Route:
renormalized sphere coefficient -> compare to continuum target 8*pi
No per-sphere magnitude fit.

n,flat_lambda1_scale,flat_baseline,sphere_residual_median,sphere_residual_std,relative_error_to_8pi,flat_window_cv,sphere_window_cv
70,6.601524405803193,28.38975392259178,6.495258888046177,2.015589339003611,0.7415618603264709,0.279329131017032,0.11863158904750143
110,5.617020047595984,-4.356881616871824,22.790580185796195,9.931741921225944,0.09319162687458227,2.6355531495271523,0.6453097941177763
160,5.868268245929568,-0.14802651097761288,21.270400740355914,1.9290767138802305,0.1536776451567115,0.7736115121732458,0.3370596192231909
positive_all: True
relative_error_improves: True
final_relative_error_lt_0p75: True
classification: MAGNITUDE_TEST_PROMISING
```

---

# 3. Interpretation rule

A promising result requires:
1. positive residual at all refinements;
2. relative error decreasing with refinement;
3. final relative error less than a loose threshold.

This is still diagnostic. Correct magnitude over three small refinement levels is not a proof.

---

# 4. What this establishes

### If promising

The estimator is not merely sign-sensitive; it may be moving toward the correct integrated curvature scale.

### If weak

The current estimator detects positive curvature but does not yet recover correct magnitude.

---

# 5. Remaining proof obligations

Even if promising:

1. larger refinement ladder;
2. uncertainty scaling;
3. heat-window theorem;
4. baseline theorem;
5. negative curvature;
6. 3D spatial extension;
7. action-level integration.

---

# 6. Next derivation target

If promising:

```text
HEAT_CURVATURE_SIGN_TESTS.md
```

If weak:

```text
HEAT_CURVATURE_MAGNITUDE_FAILURE.md
```

---

# Honest status line

> `HEAT_CURVATURE_MAGNITUDE_TEST.md` tests whether the renormalized heat-kernel curvature estimator approaches the known unit-sphere value \(8\pi\). It is a magnitude diagnostic, not a proof of graph-to-continuum curvature convergence.

**End of file.**
