# NORMALIZED_LAPLACIAN_HEAT_CURVATURE_RETEST.md

# Normalized Laplacian Heat Curvature Retest
## Retesting heat curvature with diffusion-map \(\alpha=1\) measure normalization and one universal spectral scale

## Status
**Operator-corrected heat-curvature diagnostic. Not curvature closure.**

`GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md` showed that diffusion-map density normalization improves the graph Laplacian operator test.

The best tested choice was:

\[
\alpha=1.
\]

However, the spectrum was under-scaled relative to continuum references.

This file retests the heat curvature estimator using:

```text
alpha = 1 diffusion normalization
one universal flat-torus eigenvalue scale correction
no per-geometry calibration
```

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

# 1. Operator rule

Use the density-normalized kernel:

\[
K_{ij}^{(\alpha)}
=
\frac{K_{ij}}{q_i^\alpha q_j^\alpha}
\]

with:

\[
\alpha=1.
\]

This is the best candidate from the operator-normalization diagnostic.

---

# 2. Universal spectral scale

The low spectrum was under-scaled.

For the flat torus with side \(2\pi\), the first nonzero continuum eigenvalue is:

\[
\lambda_1=1.
\]

So define one universal scale:

\[
s=\frac{1}{\lambda_{1,\mathrm{flat}}^{\mathrm{median}}}.
\]

Then use:

\[
L_{\mathrm{scaled}}=sL_{\mathcal G}.
\]

This is not per-geometry calibration. The same \(s\) is applied to sphere and flat torus.

---

# 3. Heat coefficient residual

Compute:

\[
C_{\mathrm{raw}}=6A_1
\]

from:

\[
H(t)(4\pi t)^{d/2}\approx A_0+A_1t.
\]

Then subtract the flat baseline:

\[
C_{\mathrm{ren}}=C_{\mathrm{raw}}-C_{\mathrm{flat}}.
\]

Expected:

\[
C_{\mathrm{ren,flat}}\approx0,
\]

\[
C_{\mathrm{ren,sphere}}>0.
\]

---

# 4. Verifier implementation

## Status
**Implemented as `normalized_laplacian_heat_curvature_retest_verifier.py`. Execution log captured.**

The verifier:
1. estimates the flat-torus \(\lambda_1\) scale;
2. applies the same scale to all geometries;
3. computes scaled heat coefficients;
4. subtracts the flat baseline;
5. tests sphere residual sign and separation.

## Captured verifier output

```text
Normalized Laplacian heat curvature retest verifier
==================================================
Route:
alpha=1 diffusion normalization + universal flat-torus lambda1 scale -> heat coefficient residual
No per-geometry calibration.

flat_lambda1_scale_factor: 4.941419254104508
geometry,raw_coeff_median,scaled_coeff_median,scaled_coeff_std,scaled_window_cv,raw_lambda1_median,h_median
flat_torus,-834.0126952117635,-18.371757158652223,6.335146139278723,1.1738219576530793,0.19435153865372568,0.6390814966778808
sphere,-818.1849778024426,14.393523597331072,3.748908910000576,5.411075029976456,0.4334295985218092,0.37236162746258095
flat_scaled_residual_median: 1.7763568394002505e-15
sphere_scaled_residual_median: 32.7652807559833
sphere_residual_positive: True
residual_separation_z: 3.2492167680423125
classification: NORMALIZED_HEAT_RETEST_PROMISING
```

---

# 5. Interpretation

A promising result means the operator-level correction improves the residual curvature signal.

A weak result means the issue is deeper than simple spectral scale correction.

---

# 6. Remaining open items

Even if promising:

1. larger \(n\) refinement;
2. negative curvature compact reference;
3. magnitude calibration from theory;
4. 3D spatial-slice extension;
5. proof of graph Laplacian convergence;
6. ADM action convergence.

---

# 7. Next derivation target

If promising:

```text
NORMALIZED_HEAT_REFINEMENT_CAMPAIGN.md
```

If weak:

```text
DIFFUSION_MAP_LAPLACIAN_DERIVATION.md
```

---

# Honest status line

> `NORMALIZED_LAPLACIAN_HEAT_CURVATURE_RETEST.md` retests the heat-curvature route with the best density-normalized graph operator and a universal flat-torus spectral scale. It remains diagnostic and does not prove curvature convergence.

**End of file.**
