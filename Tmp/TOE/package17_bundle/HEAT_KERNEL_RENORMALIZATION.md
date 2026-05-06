# HEAT_KERNEL_RENORMALIZATION.md

# Heat Kernel Renormalization
## Flat-reference baseline correction for the graph heat-trace curvature coefficient

## Status
**Renormalization diagnostic. Not curvature closure.**

`BOUNDARY_FREE_HEAT_KERNEL_TESTS.md` showed that boundary-free testing improved plateau stability but did not recover trustworthy curvature coefficients.

The main symptom was:

```text
flat torus and sphere both produced large negative coefficients
```

even though the expected continuum result is:

\[
\int R_{\mathrm{flat\ torus}}\,dV=0,
\]

\[
\int R_{\mathrm{sphere}}\,dV>0.
\]

This suggests the raw graph heat coefficient contains a large discretization baseline.

This file tests a first renormalization rule.

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

# 1. Problem

The raw heat coefficient estimator is:

\[
\widehat{\int R\,dV}_{\mathcal G}=6A_1,
\]

where:

\[
H_{\mathcal G}(t)(4\pi t)^{d/2}\approx A_0+A_1t.
\]

But on finite graphs, this includes:

```text
graph discretization baseline
sampling density effects
Laplacian normalization artifacts
finite-size spectral bias
```

So the raw coefficient should be decomposed as:

\[
C_{\mathcal G}^{\mathrm{raw}}
=
C_{\mathrm{baseline}}(n,k,h,\rho)
+
C_{\mathrm{curv}}
+
\text{error}.
\]

The target is:

\[
C_{\mathrm{curv}}.
\]

---

# 2. First renormalization rule

## Definition 1
Use a boundaryless flat reference as the baseline:

```text
flat torus
```

because:

\[
\int R_{\mathrm{flat\ torus}}\,dV=0.
\]

For a fixed graph rule, fixed \(n\), fixed \(k\), and fixed heat-window rule, define:

\[
C_{\mathrm{baseline}}
=
\mathrm{median}
\left[
C_{\mathrm{flat\ torus}}^{\mathrm{raw}}
\right].
\]

Then define the residual coefficient:

\[
C_{\mathrm{ren}}
=
C_{\mathrm{raw}}-C_{\mathrm{baseline}}.
\]

This is not per-geometry calibration. It is one universal flat-reference baseline for the graph rule.

---

# 3. Expected behavior

For flat torus:

\[
C_{\mathrm{ren}}\approx0.
\]

For sphere:

\[
C_{\mathrm{ren}}>0.
\]

A promising result requires:

```text
sphere residual positive
flat residual near zero
residual separation above noise
```

---

# 4. Verifier implementation

## Status
**Implemented as `heat_kernel_renormalization_verifier.py`. Execution log captured.**

The verifier:

1. computes raw coefficients for flat torus and sphere;
2. uses the flat torus median as the baseline;
3. computes residual coefficients;
4. tests whether sphere residual is positive and separated from flat residual.

## Captured verifier output

```text
Heat kernel renormalization verifier
==================================================
Route:
flat boundaryless baseline subtraction -> residual heat coefficient
No per-geometry calibration; one flat reference baseline.

baseline_flat_torus_coeff: -489.4385419608758
flat_torus_raw_median: -489.4385419608758
sphere_raw_median: -464.85901930181353
flat_torus_residual_median: 0.0
sphere_residual_median: 24.579522659062263
flat_torus_residual_std: 11.001710588927303
sphere_residual_std: 11.773338585805819
flat_torus_window_cv_median: 0.5108684097272471
sphere_window_cv_median: 0.526947040248499
sphere_residual_positive: True
residual_separation_z: 1.0792302782963896
classification: RENORMALIZED_PROMISING
```

---

# 5. Interpretation

If the residual sphere coefficient is positive and separated from zero, this supports the idea that the previous failure was dominated by a graph-discretization baseline.

If not, the estimator remains too unstable or wrongly normalized.

---

# 6. What this file establishes

### Established if promising

1. A flat-reference baseline can remove the dominant graph artifact.
2. Residual heat coefficient can begin to distinguish positive curvature from flat geometry.
3. The heat-kernel route remains viable.

### Still open

1. Derivation of the baseline correction.
2. Refinement convergence of the residual.
3. Correct continuum magnitude.
4. Extension to 3D spatial slices.
5. Negative curvature tests.
6. ADM/EH action convergence.

---

# 7. Next derivation target

If promising:

```text
RENORMALIZED_HEAT_KERNEL_REFINEMENT.md
```

If weak:

```text
GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md
```

---

# Honest status line

> `HEAT_KERNEL_RENORMALIZATION.md` tests whether the raw graph heat coefficient is dominated by a flat discretization baseline. It uses one boundaryless flat reference correction and checks whether the residual separates sphere from flat torus. This is a diagnostic, not a proof of curvature convergence.

**End of file.**
