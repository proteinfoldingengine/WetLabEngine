# RENORMALIZED_HEAT_KERNEL_REFINEMENT.md

# Renormalized Heat Kernel Refinement
## Testing whether the flat-baseline residual curvature coefficient persists under graph refinement

## Status
**Refinement diagnostic. Not curvature closure.**

`HEAT_KERNEL_RENORMALIZATION.md` showed that subtracting a boundaryless flat-torus baseline reveals a positive sphere residual:

\[
C_{\mathrm{ren}}
=
C_{\mathrm{raw}}
-
C_{\mathrm{flat}}.
\]

That was promising, but a single sample size is not enough.

This file tests whether the residual signal persists under graph refinement.

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

# 1. Renormalized coefficient

The raw coefficient is:

\[
C_{\mathrm{raw}}=6A_1,
\]

from:

\[
H_{\mathcal G}(t)(4\pi t)^{d/2}
\approx
A_0+A_1t.
\]

The flat-baseline correction is:

\[
C_{\mathrm{ren}}
=
C_{\mathrm{raw}}
-
C_{\mathrm{flat}}.
\]

For flat torus:

\[
C_{\mathrm{ren}}\approx0.
\]

For sphere:

\[
C_{\mathrm{ren}}>0.
\]

---

# 2. Refinement target

Under graph refinement:

\[
n\to\infty,
\qquad
h\to0,
\]

we want:

\[
C_{\mathrm{ren,sphere}}
\]

to remain positive and stabilize.

The minimal diagnostic criteria are:

1. positive residual across refinements;
2. residual separation does not collapse;
3. heat-window plateau remains controlled.

---

# 3. Verifier implementation

## Status
**Implemented as `renormalized_heat_kernel_refinement_verifier.py`. Execution log captured.**

The verifier tests several graph sizes:

```text
n = 80, 120, 180
```

For each \(n\), it computes:
- raw flat-torus coefficient;
- raw sphere coefficient;
- flat-baseline residual;
- residual separation score;
- heat-window coefficient-of-variation.

## Captured verifier output

```text
Renormalized heat-kernel refinement verifier
==================================================
Route:
flat baseline residual heat coefficient under graph refinement

n,h_median,flat_baseline_raw,sphere_raw_median,sphere_residual_median,sphere_residual_std,flat_window_cv,sphere_window_cv,residual_separation_z
80,0.7121622677181286,-323.72341535323994,-312.1004047839276,11.623010569312328,14.632922853122595,0.5151319261290269,0.5213103360558391,0.49695671782283946
120,0.5663357491133442,-482.29696582330666,-471.5576651099101,10.739300713396574,6.792106374263096,0.5139450295570345,0.5202784418254799,0.596975933640105
180,0.4729654014630186,-737.9863546880198,-722.884642613823,15.101712074196826,9.631569367313526,0.510164708352247,0.5194094990315961,0.8306702101058555
positive_residual_all_refinements: True
separation_ratio_last_vs_first: 1.6715141989494353
classification: RENORMALIZED_REFINEMENT_PROMISING
```

---

# 4. Interpretation

This test asks whether the positive-curvature residual is robust to refinement.

A promising result means:

```text
the renormalized spectral route deserves a stronger convergence campaign
```

not:

```text
curvature convergence is proved
```

---

# 5. What remains open

Even if promising:

1. correct continuum magnitude;
2. larger refinement range;
3. volume normalization;
4. negative-curvature tests;
5. three-dimensional spatial slices;
6. derivation of the flat baseline correction;
7. ADM action convergence.

---

# 6. Next derivation target

If promising:

```text
RENORMALIZED_HEAT_KERNEL_CONVERGENCE_CAMPAIGN.md
```

If weak:

```text
GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md
```

---

# Honest status line

> `RENORMALIZED_HEAT_KERNEL_REFINEMENT.md` tests whether the flat-baseline-renormalized heat coefficient remains positive and stable under graph refinement. It is a diagnostic step toward graph-to-continuum curvature convergence, not a proof.

**End of file.**
