# RENORMALIZED_HEAT_KERNEL_CONVERGENCE_CAMPAIGN.md

# Renormalized Heat Kernel Convergence Campaign
## Refinement campaign for the flat-baseline residual heat coefficient

## Status
**Convergence campaign diagnostic. Not curvature closure.**

`RENORMALIZED_HEAT_KERNEL_REFINEMENT.md` found a promising result:

```text
positive sphere residual across refinements
classification: RENORMALIZED_REFINEMENT_PROMISING
```

This file expands that into a more formal refinement campaign.

The purpose is to test whether the residual coefficient:

\[
C_{\mathrm{ren}}
=
C_{\mathrm{raw}}
-
C_{\mathrm{flat}}
\]

persists across a larger refinement ladder under one fixed graph rule.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Fixed rule

The campaign uses:

```text
boundaryless flat torus baseline
sphere positive-curvature target
intrinsic distances
fixed graph construction
fixed heat-window set
no per-geometry calibration
```

The only refinement parameter is graph density:

\[
n\uparrow,
\qquad
h\downarrow.
\]

---

# 2. Residual coefficient

For each \(n\), define:

\[
C_{\mathrm{flat}}(n)
=
\mathrm{median}
\left[
C_{\mathrm{raw,flat}}(n)
\right].
\]

Then:

\[
C_{\mathrm{ren,sphere}}(n)
=
C_{\mathrm{raw,sphere}}(n)
-
C_{\mathrm{flat}}(n).
\]

The minimal expected behavior is:

\[
C_{\mathrm{ren,sphere}}(n)>0
\]

across refinements.

---

# 3. Verifier implementation

## Status
**Implemented as `renormalized_heat_kernel_convergence_campaign_verifier.py`. Execution log captured.**

The verifier evaluates:

```text
n = 60, 90, 120, 180, 240
```

and reports:
- graph spacing \(h\);
- flat raw baseline;
- sphere raw coefficient;
- sphere residual;
- residual variance;
- window plateau CV;
- residual separation score;
- residual-vs-\(h\) trend.

## Captured verifier output

```text
Renormalized heat-kernel convergence campaign verifier
==================================================
Route:
fixed flat-baseline residual heat coefficient across refinement ladder
No per-geometry calibration.

n,h_median,flat_baseline_raw,sphere_raw_median,sphere_residual_median,sphere_residual_std,flat_residual_std,flat_window_cv,sphere_window_cv,residual_separation_z
60,0.7757960938871017,-243.33284431895373,-225.27935174707983,18.053492571873903,5.183120231753891,5.533720290772406,0.4984634018268752,0.521458870737542,1.6845909514025725
90,0.6538535307637955,-365.04282497083943,-357.00703972883724,8.035785242002191,9.508254767713602,6.33598320051037,0.5147000595095625,0.5092017042995984,0.5071739807315226
120,0.5858965120954753,-497.5474753982587,-463.7057727481736,33.8417026500851,17.95451367826028,3.887813736945229,0.5095980130636666,0.5276242766354742,1.5493633991826663
180,0.4628031803042234,-706.93935293054,-705.5335949906953,1.4057579398447047,27.598253520343775,11.071702769215516,0.5225808511036026,0.5237487393869896,0.03635271602890889
240,0.40787755370122514,-970.6284668685373,-972.4283902276634,-1.799923359126069,14.310269332545287,11.576732892539827,0.5179264651168933,0.5142236191082694,0.06953000364722925
positive_residual_all_refinements: False
window_cv_ok_all: True
separation_ratio_last_vs_first: 0.041274116775528225
residual_vs_h_log_slope: 4.233874194728276
classification: CONVERGENCE_CAMPAIGN_WEAK
```

---

# 4. Interpretation

A promising result requires:

1. positive residual across all refinements;
2. heat-window CV controlled;
3. residual separation not collapsing;
4. trend not obviously vanishing.

This still does not prove:

\[
R_{\mathrm{graph}}\rightarrow R.
\]

It only supports the renormalized heat-kernel route as a viable candidate for an integrated curvature estimator.

---

# 5. What remains open

Even if promising:

1. correct continuum magnitude;
2. theoretical derivation of flat baseline subtraction;
3. volume normalization;
4. three-dimensional spatial slices;
5. negative curvature / hyperbolic compact reference;
6. action-level convergence;
7. proof-level Laplacian convergence.

---

# 6. Next derivation target

If promising:

```text
HEAT_KERNEL_BASELINE_THEOREM.md
```

Purpose:

Derive why the flat baseline subtraction is legitimate:

\[
C_{\mathrm{raw}}
=
C_{\mathrm{graph\ artifact}}
+
C_{\mathrm{curvature}}
+
o(1).
\]

If weak:

```text
GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md
```

---

# Honest status line

> `RENORMALIZED_HEAT_KERNEL_CONVERGENCE_CAMPAIGN.md` tests whether the flat-baseline-renormalized heat coefficient persists across a refinement ladder. It strengthens or falsifies the spectral curvature route, but does not by itself prove graph-to-continuum curvature convergence.

**End of file.**
