# LOCAL_HEAT_3D_CURVATURE_DENSITY_TEST.md

# Local Heat 3D Curvature Density Test
## First 3D conductance precursor for analytic \(R^{(3)}\)

## Status
**3D conductance precursor diagnostic. Not direct heat-diagonal recovery. Not curvature closure.**

`HEAT_KERNEL_3D_SPATIAL_TESTS.md` constructed a validated periodic 3D conformal spatial reference with analytic scalar curvature:

\[
R^{(3)}(x,y,z).
\]

A direct dense 3D heat-diagonal run was too heavy in this environment. This file therefore runs the fast 3D analogue of the conductance mechanism that explained the 2D heat sign correction.

The tested proxy is:

\[
\widehat R^{(3)}_{\mathrm{proxy},i}
=
-(d_i-\langle d\rangle),
\]

where:

\[
d_i=\sum_j w_{ij}.
\]

This is not a replacement for the full heat diagonal. It is a precursor test asking whether the 2D conductance mechanism has a 3D analogue.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving graph-to-continuum curvature convergence.

---

# 1. 3D target

The 3D conformal metric is:

\[
g_{ij}=e^{2\phi}\delta_{ij},
\]

with:

\[
\phi=a\cos x\cos y\cos z.
\]

The analytic scalar curvature is:

\[
R^{(3)}
=
e^{-2\phi}
\left[
-4\Delta\phi-2|\nabla\phi|^2
\right].
\]

The proxy is compared to centered analytic curvature:

\[
R^{(3)}-\langle R^{(3)}\rangle.
\]

---

# 2. Verifier implementation

## Status
**Implemented as `local_heat_3d_curvature_density_verifier.py`. Execution log captured.**

The verifier tests:

```text
N = 8, 10, 12, 16, 20, 24, 32
```

and reports:
- best-fit scale;
- relative \(L^2\) error;
- correlation with analytic \(R^{(3)}\);
- correlation with curvature density;
- thresholded sign match;
- scale stability.

## Captured verifier output

```text
Local heat 3D curvature density verifier
==================================================
Route:
3D conductance precursor: -weighted-degree proxy vs analytic R^(3)
This is not the direct heat diagonal; it tests whether the 2D mechanism extends to 3D.

N,nodes,dx,int_R_dV,best_scale_s,relative_L2_error,corr_scaled_R,corr_proxy_RdV,thresholded_sign_match,retained_fraction,std_proxy,std_R
8,512,0.7853981633974483,4.192473806507262,6.070880214339029,0.2142055717313565,0.976788602021557,0.9994468136334013,1.0,0.421875,0.10608468270533132,0.6593314049196135
10,1000,0.6283185307179586,4.192473805996394,5.723884162673406,0.21694246733441158,0.9761843913251473,0.9995443411498799,1.0,0.696,0.11244616752525587,0.6593312115731242
12,1728,0.5235987755982988,4.192473805996352,5.546260438490938,0.218476543581173,0.975842200309465,0.9995944749175588,1.0,0.5601851851851852,0.11600667281555807,0.6593312113719603
16,4096,0.39269908169872414,4.192473805996354,5.376731249793322,0.22003499756309197,0.9754919783613838,0.9996421202765492,1.0,0.595703125,0.11962143501243895,0.6593312113718282
20,8000,0.3141592653589793,4.192473805996355,5.300554488197288,0.22076762164881228,0.9753264362414897,0.9996633786951825,1.0,0.619,0.1213199792817844,0.659331211371828
24,13824,0.2617993877991494,4.192473805996352,5.259764407827845,0.22116860326882998,0.97523558637291,0.9996747061551623,1.0,0.6174768518518519,0.12224944135885873,0.659331211371828
32,32768,0.19634954084936207,4.192473805996354,5.21961107062733,0.22156941768191768,0.9751446011480016,0.9996858116425003,1.0,0.607666015625,0.12317838674909831,0.659331211371828
scale_cv_across_grids: 0.05186217541587021
corr_ok_all_gt_0p75: True
thresholded_sign_ok_all_gt_0p70: True
final_error_lt_0p70: True
scale_cv_lt_0p25: True
classification: LOCAL_3D_CONDUCTANCE_PROMISING
```

---

# 3. Interpretation

A promising result means:

```text
the conductance mechanism that supports the 2D local heat result has a plausible 3D analogue
```

It does not mean:

```text
the 3D direct local heat diagonal has passed
```

The direct 3D heat run should be performed on Colab/T4 or using sparse heat methods.

---

# 4. Next derivation target

If promising:

```text
LOCAL_HEAT_3D_DIRECT_COLAB_TEST.md
```

If weak:

```text
LOCAL_HEAT_3D_CONDUCTANCE_FAILURE.md
```

---

# Honest status line

> `LOCAL_HEAT_3D_CURVATURE_DENSITY_TEST.md` tests the 3D conductance precursor \(-(d_i-\langle d\rangle)\) against analytic \(R^{(3)}\). It checks whether the 2D heat-curvature mechanism plausibly extends to 3D, but it is not a direct heat-diagonal result.

**End of file.**
