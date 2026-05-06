# HEAT_CURVATURE_STATUS_AND_NEXT_PROOF_OBLIGATIONS.md

# Heat Curvature Status and Next Proof Obligations
## Status audit for the spectral/heat-kernel curvature route

## Status
**Promising diagnostic route. Not curvature closure. Not GR derivation.**

This file consolidates the current status of the heat-kernel curvature branch after the recent root-cause, renormalization, operator-normalization, and refinement tests.

Current classification:

```text
heat-kernel curvature route is promising but not closed
```

---

# 1. Why this route matters

The continuum heat trace satisfies:

\[
\mathrm{Tr}(e^{-t\Delta})
\sim
(4\pi t)^{-d/2}
\left[
\mathrm{Vol}
+
\frac{t}{6}\int R\,dV
+
O(t^2)
\right].
\]

So the scalar curvature action term appears directly:

\[
\int R\,dV.
\]

This is the correct object for the spatial ADM curvature contribution:

\[
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

---

# 2. What failed

## 2.1 Extrinsic curvature proxy

The covariance/PCA graph curvature proxy could separate curved from flat data, but it was mostly an embedding-dependent signal.

Status:

```text
rejected as GR curvature evidence
```

## 2.2 Generic heat-trace area/slope

The first spectral diagnostic used generic heat-trace area/slope features.

Result:

```text
classification: SPECTRAL_DIAGNOSTIC_WEAK
```

Status:

```text
diagnostic only; not enough
```

## 2.3 Raw heat coefficient

The first coefficient estimator targeted:

\[
H(t)(4\pi t)^{d/2}\approx A_0+A_1t.
\]

But raw coefficients had unstable signs/magnitudes.

Root causes:

```text
boundary contamination
graph discretization baseline
bad measure normalization
heat-window instability
```

Status:

```text
raw coefficient not accepted
```

---

# 3. What improved

## 3.1 Flat baseline renormalization

Using a boundaryless flat-torus baseline:

\[
C_{\mathrm{ren}}
=
C_{\mathrm{raw}}
-
C_{\mathrm{flat}}
\]

revealed a positive sphere residual:

```text
sphere residual: +24.58
classification: RENORMALIZED_PROMISING
```

This supported the hypothesis:

```text
raw graph heat coefficient is dominated by a flat discretization baseline
```

## 3.2 Operator-level correction

Density-normalized graph Laplacian testing found the best tested diffusion-map normalization:

\[
\alpha=1.
\]

Result:

```text
classification: MEASURE_NORMALIZATION_PROMISING
best_alpha: 1.0
```

The spectrum had the right ordering but wrong scale.

## 3.3 Current best method

The best current method is:

```text
alpha = 1 diffusion-map density normalization
universal flat-torus lambda1 spectral scale
flat heat-coefficient baseline subtraction
sphere residual test
refinement ladder
```

The normalized retest produced:

```text
classification: NORMALIZED_HEAT_RETEST_PROMISING
sphere residual: +32.77
residual_separation_z: 3.25
```

The normalized refinement campaign produced:

```text
classification: NORMALIZED_REFINEMENT_PROMISING
```

with residuals:

```text
n=70:   +3.20
n=110: +14.61
n=160: +17.53
```

and:

```text
separation_ratio_last_vs_first: 5.40
```

This is the strongest heat-curvature result so far.

---

# 4. Honest classification

The heat-kernel curvature branch is now:

```text
promising diagnostic route
```

not:

```text
curvature convergence proof
```

The safe claim is:

> A density-normalized, spectrally scaled, flat-baseline-renormalized heat trace produces a persistent positive sphere residual over a small refinement ladder.

The unsafe claim is:

> \(R_{\mathcal G}\to R\) has been shown.

That has not been shown.

---

# 5. Remaining proof obligations

## Obligation 1: baseline theorem

Justify:

\[
C_{\mathrm{raw}}
=
C_{\mathrm{graph\ baseline}}
+
C_{\mathrm{curvature}}
+
o(1).
\]

Next file:

```text
HEAT_KERNEL_BASELINE_THEOREM.md
```

## Obligation 2: Laplacian convergence

Need:

\[
L_{\mathcal G}\rightarrow \Delta_h.
\]

Next file:

```text
DIFFUSION_MAP_LAPLACIAN_DERIVATION.md
```

## Obligation 3: heat-window theorem

Need a principled window:

\[
h^2\ll t\ll L_R^2.
\]

Next file:

```text
HEAT_WINDOW_SCALE_SELECTION.md
```

## Obligation 4: magnitude calibration

Need the sphere residual to converge toward:

\[
\int_{S^2}R\,dV=8\pi.
\]

Next file:

```text
HEAT_CURVATURE_MAGNITUDE_TEST.md
```

## Obligation 5: sign tests

Need:

\[
R>0,\quad R=0,\quad R<0.
\]

Next file:

```text
HEAT_CURVATURE_SIGN_TESTS.md
```

## Obligation 6: 3D spatial extension

Need:

\[
R^{(3)}
\]

tests on 3D references.

Next file:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
```

## Obligation 7: ADM action integration

Need:

\[
\sum_k N_k C_{\mathrm{ren},k}
\rightarrow
\int N\sqrt h R^{(3)}\,d^3x.
\]

Next file:

```text
HEAT_CURVATURE_TO_ADM_ACTION.md
```

---

# 6. Recommended next step

The next highest-value file is:

```text
HEAT_KERNEL_BASELINE_THEOREM.md
```

Reason:

The current method depends on flat baseline subtraction. If this cannot be justified, the curvature signal remains a diagnostic artifact.

The theorem target is:

\[
C_{\mathrm{raw}}
=
C_{\mathrm{flat\ baseline}}
+
C_{\mathrm{curvature}}
+
o(1).
\]

---

# 7. Safe report-out

```text
Milestone: the curvature seam has moved from extrinsic graph proxies to a first-principles heat-kernel route.

The strongest current signal uses alpha=1 diffusion-map normalization, a universal flat-torus spectral scale, and flat-baseline residual subtraction. Sphere residuals stayed positive across a small refinement ladder.

This is not curvature closure, but it is the first credible spectral path toward the integrated ∫R√h term needed for ADM/EH convergence.

Next theorem: justify the flat baseline subtraction.
```

---

# Honest final status

> `HEAT_CURVATURE_STATUS_AND_NEXT_PROOF_OBLIGATIONS.md` classifies the spectral curvature route as promising but not closed. The next decisive theorem is the heat-kernel baseline theorem: whether flat-reference subtraction is a legitimate universal removal of graph discretization bias, leaving a curvature residual.

**End of file.**
