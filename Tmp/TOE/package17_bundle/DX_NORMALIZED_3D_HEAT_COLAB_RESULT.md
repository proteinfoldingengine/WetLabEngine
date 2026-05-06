# DX_NORMALIZED_3D_HEAT_COLAB_RESULT.md

# dx-Normalized 3D Direct Heat Colab Result
## Stabilizing the 3D local heat curvature scale with \((-6B_i)/dx\)

## Status
**Major 3D direct heat diagnostic milestone. Scale seam substantially resolved diagnostically. Not theorem closure.**

`LOCAL_HEAT_3D_SCALE_NORMALIZATION.md` predicted that the raw 3D heat estimator was missing approximately one power of grid-spacing normalization.

The proposed normalized estimator was:

\[
\widehat R^{(3)}_{\mathrm{norm},i}
=
\frac{-6B_i}{dx}.
\]

This Colab/T4 run confirms that the normalization substantially stabilizes scale while preserving the strong shape/sign result.

Campaign classification:

```text
DX_NORMALIZED_3D_HEAT_PROMISING
```

---

# 1. Device and setup

The run used:

```text
Torch available: True
Device: cuda
GPU: Tesla T4
```

Grid ladder:

```text
N = 8, 10, 12, 14
```

Estimator comparison:

Raw:

\[
\widehat R_i^{(3)}=-6B_i.
\]

dx-normalized:

\[
\widehat R_{i,\mathrm{norm}}^{(3)}
=
\frac{-6B_i}{dx}.
\]

---

# 2. Campaign summary

The dx-normalized campaign passed all checks:

```text
scale_improved_by_dx_normalization: true
corr_ok_all: true
thresholded_sign_ok_all: true
retained_ok_all: true
final_error_lt_0p70: true
dxnorm_scale_cv_lt_0p15: true
conductance_corr_ok_all: true
classification: DX_NORMALIZED_3D_HEAT_PROMISING
```

Most important scale result:

```text
raw_scale_cv_across_grids:    0.2675
dxnorm_scale_cv_across_grids: 0.0681
```

This is a major improvement.

---

# 3. What changed

Raw fitted scale:

```text
N=8:  3.704
N=10: 4.947
N=12: 6.328
N=14: 7.779
```

dx-normalized fitted scale:

```text
N=8:  2.909
N=10: 3.108
N=12: 3.313
N=14: 3.491
```

The scale still drifts upward slightly, but the coefficient of variation dropped from:

```text
0.2675 -> 0.0681
```

So one power of \(dx\) captures most of the missing normalization.

---

# 4. Shape/sign preservation

The dx-normalized estimator preserved the strong direct heat result.

Correlation with analytic \(R^{(3)}\):

```text
N=8:  0.9662
N=10: 0.9649
N=12: 0.9646
N=14: 0.9647
```

Correlation with curvature density \(R^{(3)}dV\):

```text
N=8:  0.99973
N=10: 0.99965
N=12: 0.99963
N=14: 0.99965
```

Thresholded sign recovery:

```text
N=8:  1.0
N=10: 1.0
N=12: 1.0
N=14: 1.0
```

Relative \(L^2\) error:

```text
N=8:  0.2579
N=10: 0.2626
N=12: 0.2638
N=14: 0.2634
```

The dx normalization changes scale stability, not the shape/sign quality.

---

# 5. Interpretation

The previous 3D scale failure was not a curvature-detection failure.

It was primarily a normalization seam.

The current evidence supports:

```text
3D direct heat curvature shape: strong
3D direct heat curvature sign: strong
3D curvature-density correlation: extremely strong
3D magnitude scale after dx normalization: promising
```

This suggests that the graph heat diagonal is recovering a node-density-scaled version of curvature, and one factor of \(dx\) removes most of the grid-spacing dependence.

---

# 6. What remains open

Still not theorem closure.

Remaining obligations:

1. derive why \(1/dx\) appears in 3D;
2. test whether the residual scale drift follows \(dx^{-0.327}\) or finite-grid effects;
3. test larger \(N\), especially \(N=16,18\);
4. test other 3D conformal metrics;
5. compare against mass-matrix/volume-normalized graph heat diagonal;
6. integrate with ADM action density \(N\sqrt h R^{(3)}\);
7. prove graph-to-Laplace-Beltrami convergence.

---

# 7. Next target

The next best file is:

```text
LOCAL_HEAT_3D_STATUS.md
```

Purpose:

Freeze the current 3D branch honestly:

```text
3D reference: passed
3D conductance proxy: strong
3D direct heat shape/sign: strong
dx-normalized scale: promising
theorem closure: open
```

After that, the next technical target should be:

```text
HEAT_CURVATURE_TO_ADM_ACTION.md
```

because we now have a plausible local \(R^{(3)}\) density signal.

---

# 8. Report-out language

```text
Milestone: dx-normalized 3D direct heat curvature passed.

On a periodic conformal 3D spatial slice with analytic R^(3), the direct heat diagonal recovered curvature shape at corr≈0.965, curvature density at corr≈0.9996, and thresholded sign at 1.0 across N=8,10,12,14.

The prior scale instability was largely removed by Rhat=(-6B)/dx: scale CV dropped from 0.2675 to 0.0681.

Still not theorem closure. Next seam: derive the dx/measure normalization and connect local R^(3) density to the ADM action.
```

---

# Raw Colab output

```text
Torch available: True
Device: cuda
GPU: Tesla T4

Running 3D dx-normalized direct heat-diagonal curvature test...
N_LIST: [8, 10, 12, 14]
AMP: 0.15
TIME_MULTIPLIERS: [0.8, 1.2, 1.8]
SIGN_THRESHOLD: 0.1

--- Running N=8 (512 nodes) ---
{
  "N": 8,
  "nodes": 512,
  "dx": 0.7853981633974483,
  "geometry_seconds": 0.003,
  "build_seconds": 0.039,
  "heat_seconds": 1.317,
  "total_seconds": 1.454,
  "int_R_dV": 4.192473806507262,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.2890625,
  "negative_R_fraction": 0.7109375,
  "conductance_corr_R": 0.9767886020215342,
  "conductance_corr_RdV": 0.9994468136334013,
  "conductance_best_scale_s": 6.070880214339025,
  "conductance_relative_L2_error": 0.2142055717313575,
  "raw_best_scale_s": 3.704291394303411,
  "raw_relative_L2_error": 0.25788743428298294,
  "raw_corr_raw_Rhat_R": 0.9661749692674196,
  "raw_corr_scaled_R": 0.9661749692674315,
  "raw_corr_raw_Rhat_RdV": 0.9997256004209331,
  "raw_thresholded_sign_match": 1.0,
  "raw_retained_fraction": 0.421875,
  "raw_std_Rhat": 0.1719706772703863,
  "raw_std_R": 0.6593314049196135,
  "dxnorm_best_scale_s": 2.9093436577749445,
  "dxnorm_relative_L2_error": 0.25788743428298294,
  "dxnorm_corr_raw_Rhat_R": 0.9661749692674233,
  "dxnorm_corr_scaled_R": 0.9661749692674317,
  "dxnorm_corr_raw_Rhat_RdV": 0.9997256004209408,
  "dxnorm_thresholded_sign_match": 1.0,
  "dxnorm_retained_fraction": 0.421875,
  "dxnorm_std_Rhat": 0.21895986683554425,
  "dxnorm_std_R": 0.6593314049196135
}
--- Running N=10 (1000 nodes) ---
{
  "N": 10,
  "nodes": 1000,
  "dx": 0.6283185307179586,
  "geometry_seconds": 0.002,
  "build_seconds": 0.064,
  "heat_seconds": 0.152,
  "total_seconds": 0.318,
  "int_R_dV": 4.192473805996394,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.5,
  "negative_R_fraction": 0.5,
  "conductance_corr_R": 0.9761843913251366,
  "conductance_corr_RdV": 0.9995443411498801,
  "conductance_best_scale_s": 5.7238841626734045,
  "conductance_relative_L2_error": 0.21694246733441136,
  "raw_best_scale_s": 4.946787298720928,
  "raw_relative_L2_error": 0.2626079671444135,
  "raw_corr_raw_Rhat_R": 0.9649026145638999,
  "raw_corr_scaled_R": 0.9649026145639088,
  "raw_corr_raw_Rhat_RdV": 0.9996540828802489,
  "raw_thresholded_sign_match": 1.0,
  "raw_retained_fraction": 0.696,
  "raw_std_Rhat": 0.1286067848672122,
  "raw_std_R": 0.6593312115731242,
  "dxnorm_best_scale_s": 3.1081581273067087,
  "dxnorm_relative_L2_error": 0.2626079671444136,
  "dxnorm_corr_raw_Rhat_R": 0.964902614563904,
  "dxnorm_corr_scaled_R": 0.9649026145639089,
  "dxnorm_corr_raw_Rhat_RdV": 0.9996540828802671,
  "dxnorm_thresholded_sign_match": 1.0,
  "dxnorm_retained_fraction": 0.696,
  "dxnorm_std_Rhat": 0.20468405526772787,
  "dxnorm_std_R": 0.6593312115731242
}
--- Running N=12 (1728 nodes) ---
{
  "N": 12,
  "nodes": 1728,
  "dx": 0.5235987755982988,
  "geometry_seconds": 0.004,
  "build_seconds": 0.238,
  "heat_seconds": 0.306,
  "total_seconds": 0.737,
  "int_R_dV": 4.192473805996352,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.3263888888888889,
  "negative_R_fraction": 0.6736111111111112,
  "conductance_corr_R": 0.9758422003094591,
  "conductance_corr_RdV": 0.9995944749175587,
  "conductance_best_scale_s": 5.546260438490938,
  "conductance_relative_L2_error": 0.2184765435811729,
  "raw_best_scale_s": 6.3282126875665785,
  "raw_relative_L2_error": 0.2638095057561231,
  "raw_corr_raw_Rhat_R": 0.9645747999365775,
  "raw_corr_scaled_R": 0.9645747999365849,
  "raw_corr_raw_Rhat_RdV": 0.9996346860470678,
  "raw_thresholded_sign_match": 1.0,
  "raw_retained_fraction": 0.5601851851851852,
  "raw_std_Rhat": 0.10049824534983731,
  "raw_std_R": 0.6593312113719603,
  "dxnorm_best_scale_s": 3.313444414935617,
  "dxnorm_relative_L2_error": 0.26380950575612316,
  "dxnorm_corr_raw_Rhat_R": 0.9645747999365817,
  "dxnorm_corr_scaled_R": 0.9645747999365848,
  "dxnorm_corr_raw_Rhat_RdV": 0.9996346860470978,
  "dxnorm_thresholded_sign_match": 1.0,
  "dxnorm_retained_fraction": 0.5601851851851852,
  "dxnorm_std_Rhat": 0.19193751023386432,
  "dxnorm_std_R": 0.6593312113719603
}
--- Running N=14 (2744 nodes) ---
{
  "N": 14,
  "nodes": 2744,
  "dx": 0.4487989505128276,
  "geometry_seconds": 0.003,
  "build_seconds": 0.414,
  "heat_seconds": 0.725,
  "total_seconds": 1.446,
  "int_R_dV": 4.192473805996354,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.5,
  "negative_R_fraction": 0.5,
  "conductance_corr_R": 0.9756310243083643,
  "conductance_corr_RdV": 0.9996236415275072,
  "conductance_best_scale_s": 5.442635958891208,
  "conductance_relative_L2_error": 0.21941764834898816,
  "raw_best_scale_s": 7.779463095004033,
  "raw_relative_L2_error": 0.26342365877440543,
  "raw_corr_raw_Rhat_R": 0.9646802454688749,
  "raw_corr_scaled_R": 0.9646802454688806,
  "raw_corr_raw_Rhat_RdV": 0.9996468679993146,
  "raw_thresholded_sign_match": 1.0,
  "raw_retained_fraction": 0.6268221574344023,
  "raw_std_Rhat": 0.08175934342305742,
  "raw_std_R": 0.6593312113718282,
  "dxnorm_best_scale_s": 3.4914148725912333,
  "dxnorm_relative_L2_error": 0.2634236587744054,
  "dxnorm_corr_raw_Rhat_R": 0.9646802454688784,
  "dxnorm_corr_scaled_R": 0.9646802454688809,
  "dxnorm_corr_raw_Rhat_RdV": 0.9996468679993569,
  "dxnorm_thresholded_sign_match": 1.0,
  "dxnorm_retained_fraction": 0.6268221574344023,
  "dxnorm_std_Rhat": 0.18217365109618402,
  "dxnorm_std_R": 0.6593312113718282
}

================ 3D DX-NORMALIZED CAMPAIGN SUMMARY ================
{
  "n_completed": 4,
  "N_completed": [
    8,
    10,
    12,
    14
  ],
  "raw_scale_cv_across_grids": 0.2675395461387084,
  "dxnorm_scale_cv_across_grids": 0.06809330473651544,
  "scale_improved_by_dx_normalization": true,
  "corr_ok_all": true,
  "thresholded_sign_ok_all": true,
  "retained_ok_all": true,
  "final_error_lt_0p70": true,
  "dxnorm_scale_cv_lt_0p15": true,
  "conductance_corr_ok_all": true,
  "classification": "DX_NORMALIZED_3D_HEAT_PROMISING"
}

CSV_ROWS:
N,nodes,dx,int_R_dV,raw_scale,dxnorm_scale,raw_rel_L2,dxnorm_rel_L2,raw_corr_R,dxnorm_corr_R,raw_corr_RdV,dxnorm_corr_RdV,raw_sign_match,dxnorm_sign_match,retained_fraction,conductance_corr_R,conductance_corr_RdV,geometry_seconds,build_seconds,heat_seconds,total_seconds
8,512,0.7853981633974483,4.192473806507262,3.704291394303411,2.9093436577749445,0.25788743428298294,0.25788743428298294,0.9661749692674315,0.9661749692674317,0.9997256004209331,0.9997256004209408,1.0,1.0,0.421875,0.9767886020215342,0.9994468136334013,0.003,0.039,1.317,1.454
10,1000,0.6283185307179586,4.946787298720928,3.1081581273067087,0.2626079671444135,0.2626079671444136,0.9649026145639088,0.9649026145639089,0.9996540828802489,0.9996540828802671,1.0,1.0,0.696,0.9761843913251366,0.9995443411498801,0.002,0.064,0.152,0.318
12,1728,0.5235987755982988,4.192473805996352,6.3282126875665785,3.313444414935617,0.2638095057561231,0.26380950575612316,0.9645747999365849,0.9645747999365848,0.9996346860470678,0.9996346860470978,1.0,1.0,0.5601851851851852,0.9758422003094591,0.9995944749175587,0.004,0.238,0.306,0.737
14,2744,0.4487989505128276,4.192473805996354,7.779463095004033,3.4914148725912333,0.26342365877440543,0.2634236587744054,0.9646802454688806,0.9646802454688809,0.9996468679993146,0.9996468679993569,1.0,1.0,0.6268221574344023,0.9756310243083643,0.9996236415275072,0.003,0.414,0.725,1.446
```

---

# Honest status line

> `DX_NORMALIZED_3D_HEAT_COLAB_RESULT.md` records a major 3D diagnostic milestone: direct heat-kernel local curvature recovery remains strong for shape/sign, and \(dx\)-normalization reduces scale instability by roughly 4x. The result is promising but still requires a normalization theorem and ADM integration.

**End of file.**
