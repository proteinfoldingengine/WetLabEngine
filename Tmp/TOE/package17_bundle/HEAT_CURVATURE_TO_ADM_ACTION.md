# HEAT_CURVATURE_TO_ADM_ACTION.md

# Heat Curvature to ADM Action
## First diagnostic assembly of local \(R^{(3)}\) recovery into the ADM spatial-curvature action term

## Status
**ADM spatial-curvature action diagnostic. Not full ADM closure. Not Einstein equation derivation.**

`LOCAL_HEAT_3D_STATUS.md` froze the current 3D local heat-curvature milestone:

\[
\widehat R^{(3)}_{\mathrm{heat},i}
=
\frac{-6B_i}{dx}
\]

with strong diagnostic recovery of analytic \(R^{(3)}\) shape/sign and curvature-density structure.

This file tests the next seam:

\[
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

It does **not** include extrinsic curvature terms yet:

\[
K_{ij}K^{ij}-K^2.
\]

It does **not** vary the action.

It tests only whether the recovered local spatial curvature signal can assemble into the ADM spatial curvature action component.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving the Einstein equations.

---

# 1. ADM target term

The ADM gravitational action contains the spatial curvature term:

\[
S_R
=
\int dt\int_{\Sigma_t} N\sqrt h\,R^{(3)}\,d^3x.
\]

For a single spatial slice, the target is:

\[
I_R
=
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

The discrete approximation is:

\[
I_R^{\mathrm{disc}}
=
\sum_i N_i\sqrt{h_i}\,\widehat R^{(3)}_i\,\Delta x^3.
\]

---

# 2. Reference geometry

The spatial metric is:

\[
h_{ij}=e^{2\phi}\delta_{ij},
\]

with:

\[
\phi=a\cos x\cos y\cos z.
\]

The analytic curvature is:

\[
R^{(3)}
=
e^{-2\phi}
\left[
-4\Delta\phi-2|\nabla\phi|^2
\right].
\]

The volume factor is:

\[
\sqrt h=e^{3\phi}.
\]

---

# 3. Diagnostic estimator

For computational speed at larger grids, this verifier uses the validated conductance mechanism:

\[
\widehat R^{(3)}_{\mathrm{proxy},i}
=
s\left[-(d_i-\langle d\rangle)\right]
+
\langle R\rangle.
\]

Important caveat:

```text
the zero mode / mean curvature is restored using the analytic mean in this diagnostic
```

That means this test evaluates action assembly from the local curvature shape and density, but does not yet prove autonomous recovery of the curvature zero mode.

The direct heat dx-normalized estimator should later replace the conductance proxy in a Colab/T4 action test.

---

# 4. Lapse fields tested

The verifier tests several lapse choices:

```text
unit
smooth_positive
curvature_coupled
```

This checks whether the action-density recovery survives nontrivial weighting by \(N(x)\).

---

# 5. Verifier implementation

## Status
**Implemented as `heat_curvature_to_adm_action_verifier.py`. Execution log captured.**

The verifier reports:
- analytic \(I_R\);
- recovered \(I_R\);
- absolute and relative error;
- density correlation;
- lapse statistics.

## Captured verifier output

```text
Heat curvature to ADM action verifier
==================================================
Route:
3D local curvature proxy -> spatial ADM curvature action integral
Uses conductance proxy for larger grids; direct heat dx-normalization already validated on small grids.

N,nodes,lapse_kind,scale_s,S_true,S_hat,abs_error,relative_error,density_corr,mean_lapse,min_lapse,max_lapse
16,4096,unit,5.376731249793324,4.192473805996354,4.5560516986377575,0.3635778926414037,0.08672156570693508,0.9770650978964057,1.0,1.0,1.0
16,4096,smooth_positive,5.376731249793324,4.192473805996354,4.556051698637761,0.3635778926414073,0.08672156570693593,0.9770729353039183,1.0,0.85,1.1500000000000001
16,4096,curvature_coupled,5.376731249793324,9.791279905380012,10.392732194092757,0.6014522887127445,0.06142734091200919,0.9783977099518424,1.0,0.9,1.1
20,8000,unit,5.3005544881972915,4.192473805996354,4.552935229069452,0.36046142307309825,0.08597821709880607,0.9769182205029601,1.0,1.0,1.0
20,8000,smooth_positive,5.3005544881972915,4.1924738059963556,4.552935229069452,0.3604614230730965,0.08597821709880561,0.9769260235712478,1.0,0.85,1.1500000000000001
20,8000,curvature_coupled,5.3005544881972915,9.791279905380012,10.389441641010812,0.5981617356308,0.061091271152616845,0.9782598145061739,1.0,0.9,1.1
24,13824,unit,5.259764407827845,4.192473805996352,4.551214692294097,0.3587408862977446,0.08556783009223914,0.976837642572343,1.0,1.0,1.0
24,13824,smooth_positive,5.259764407827845,4.192473805996352,4.551214692294097,0.3587408862977446,0.08556783009223914,0.9768454268836401,1.0,0.85,1.1500000000000001
24,13824,curvature_coupled,5.259764407827845,9.791279905380005,10.387622204709652,0.5963422993296472,0.060905449041643134,0.9781841661940328,1.0,0.9,1.1
32,32768,unit,5.21961107062733,4.192473805996353,4.549484403051509,0.35701059705515625,0.08515511690125552,0.9767569649232971,1.0,1.0,1.0
32,32768,smooth_positive,5.21961107062733,4.192473805996354,4.549484403051507,0.3570105970551536,0.08515511690125487,0.9767647305123183,1.0,0.85,1.1500000000000001
32,32768,curvature_coupled,5.21961107062733,9.79127990538001,10.385790501243138,0.5945105958631274,0.0607183740642938,0.9781084257367331,1.0,0.9,1.1
relative_error_all_lt_0p15: True
density_corr_all_gt_0p95: True
classification: ADM_SPATIAL_CURVATURE_ACTION_PROMISING
```

---

# 6. Interpretation

A promising result means:

```text
the recovered local R^(3) density can assemble into the ADM spatial curvature action term under tested lapse fields
```

It does not mean:

```text
full ADM action is recovered
```

because we still need:
- direct heat action test;
- zero-mode recovery;
- extrinsic curvature terms;
- causal slicing;
- action variation.

---

# 7. What remains open

1. Replace conductance proxy with direct dx-normalized heat estimator in Colab.
2. Recover curvature zero mode without analytic mean insertion.
3. Add extrinsic curvature terms:
   \[
   K_{ij}K^{ij}-K^2.
   \]
4. Add lapse/shift from causal slicing.
5. Prove continuum convergence.
6. Vary the action.

---

# 8. Next derivation target

If promising:

```text
ADM_SPATIAL_ACTION_STATUS.md
```

If weak:

```text
ADM_SPATIAL_ACTION_FAILURE.md
```

Then next technical step:

```text
DIRECT_HEAT_ADM_ACTION_COLAB_TEST.md
```

---

# Honest status line

> `HEAT_CURVATURE_TO_ADM_ACTION.md` tests whether the 3D local curvature signal can be assembled into the ADM spatial curvature action term \(\int N\sqrt hR^{(3)}d^3x\). It is a spatial-curvature action diagnostic only, not full ADM or GR closure.

**End of file.**
