# FULL_DIRECT_3D_HEAT_REFINEMENT_COLAB_RESULT.md

# Full Direct 3D Heat-Diagonal Refinement Colab Result
## Direct local heat-kernel recovery of analytic \(R^{(3)}\)

## Status
**Strong 3D direct heat diagnostic with unresolved scale stability. Not theorem closure.**

This file records the Colab/T4 result for the first full direct 3D heat-diagonal curvature test.

The automatic classification was:

```text
FULL_DIRECT_3D_HEAT_REFINEMENT_WEAK
```

but only because:

```text
scale_cv_lt_0p25: false
```

All shape/sign/error checks passed.

Therefore the correct human classification is:

```text
3D direct heat shape/sign recovery: strong
3D magnitude scale stability: not yet stable enough
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

Node counts:

```text
512, 1000, 1728, 2744
```

Estimator:

\[
K_{\mathcal G}(t,i,i)=[e^{-tL}]_{ii}
\]

\[
Y_i(t)=K_{\mathcal G}(t,i,i)(4\pi t)^{3/2}
\]

\[
Y_i(t)\approx A_i+B_it
\]

\[
\widehat R_i^{(3)}=-6B_i.
\]

---

# 2. Campaign summary

Passed:

```text
corr_ok_all: true
thresholded_sign_ok_all: true
retained_ok_all: true
final_error_lt_0p70: true
conductance_corr_ok_all: true
```

Failed:

```text
scale_cv_lt_0p25: false
```

Scale coefficient variation:

```text
scale_cv_across_grids: 0.2675
```

This narrowly missed the threshold:

```text
threshold: 0.25
observed:  0.2675
```

---

# 3. Key direct heat results

The direct heat field strongly tracks analytic \(R^{(3)}\):

```text
N=8:  corr_scaled_R = 0.9662
N=10: corr_scaled_R = 0.9649
N=12: corr_scaled_R = 0.9646
N=14: corr_scaled_R = 0.9647
```

Curvature-density correlation is extremely high:

```text
N=8:  corr_RdV = 0.99973
N=10: corr_RdV = 0.99965
N=12: corr_RdV = 0.99963
N=14: corr_RdV = 0.99965
```

Thresholded sign recovery passed perfectly:

```text
N=8:  sign_match = 1.0
N=10: sign_match = 1.0
N=12: sign_match = 1.0
N=14: sign_match = 1.0
```

Relative \(L^2\) error stayed low:

```text
N=8:  0.2579
N=10: 0.2626
N=12: 0.2638
N=14: 0.2634
```

---

# 4. Scale issue

The fitted heat scale increased across the ladder:

```text
N=8:  best_scale_s = 3.704
N=10: best_scale_s = 4.947
N=12: best_scale_s = 6.328
N=14: best_scale_s = 7.779
```

This caused:

```text
scale_cv_across_grids: 0.2675
```

Interpretation:

```text
shape/sign recovery is strong, but local heat magnitude scale is not stabilized yet in 3D.
```

Likely causes:
- heat window needs 3D-specific scaling;
- graph Laplacian normalization differs with N;
- local heat coefficient amplitude shrinks with refinement;
- fitted scale may require explicit \(dx\) renormalization;
- dense small-grid range may be too coarse to reveal asymptotic scale.

---

# 5. Conductance mechanism

The conductance precursor also passed strongly:

```text
conductance_corr_R ≈ 0.976
conductance_corr_RdV ≈ 0.9995
conductance_relative_L2_error ≈ 0.214 to 0.219
```

So both:
- conductance mechanism,
- direct heat diagonal,

are aligned in 3D.

This is important.

---

# 6. Correct status

The 3D branch is now:

```text
3D reference geometry: passed
3D conductance mechanism: strong
3D direct heat shape/sign recovery: strong
3D direct heat magnitude scale: unresolved
```

This is not a failure of 3D local heat curvature.

It is a scale-normalization blocker.

---

# 7. What is genuinely established

Established diagnostically:

1. Direct 3D heat diagonal tracks analytic \(R^{(3)}\) shape.
2. Direct 3D heat diagonal tracks \(R^{(3)}dV\) extremely strongly.
3. Thresholded sign recovery passed perfectly across tested grids.
4. Relative error after fitted scale is low.
5. Conductance mechanism remains strong in 3D.
6. T4 run completed through \(N=14\).

Not established:

1. Stable universal scale.
2. 3D heat-window theorem.
3. 3D scale theorem.
4. larger 3D refinement.
5. ADM action integration.

---

# 8. Next target

The next file should be:

```text
LOCAL_HEAT_3D_SCALE_NORMALIZATION.md
```

Purpose:

Determine whether the fitted scale:

\[
s_N
\]

has a predictable dependence on:

\[
dx,\quad N,\quad h,\quad \lambda_1,\quad \text{or graph degree normalization}.
\]

The observed scale trend:

```text
3.704, 4.947, 6.328, 7.779
```

suggests a missing normalization factor, not random failure.

---

# 9. Report-out language

```text
3D direct heat-kernel curvature test passed shape/sign but exposed a scale-normalization seam.

On a periodic conformal 3D spatial slice with analytic R^(3), the direct heat diagonal recovered curvature shape at corr≈0.965 and curvature density at corr≈0.9996, with perfect thresholded sign recovery through N=14 on T4.

The only failed criterion was scale stability: fitted scale CV=0.267 versus 0.25 threshold. Next blocker: derive the 3D scale normalization / heat-window rule.
```

---

# Honest status line

> `FULL_DIRECT_3D_HEAT_REFINEMENT_COLAB_RESULT.md` records a strong 3D direct heat result: shape, sign, and scaled error pass, but the fitted magnitude scale is not yet stable. The next proof seam is 3D scale normalization.

---

# Raw Colab output

```text
Torch available: True
Device: cuda
GPU: Tesla T4

Running 3D full direct heat-diagonal curvature test...
N_LIST: [8, 10, 12, 14]
AMP: 0.15
TIME_MULTIPLIERS: [0.8, 1.2, 1.8]
SIGN_THRESHOLD: 0.1

--- Running N=8 (512 nodes) ---
{
  "N": 8,
  "nodes": 512,
  "dx": 0.7853981633974483,
  "geometry_seconds": 0.001,
  "build_seconds": 0.019,
  "heat_seconds": 1.01,
  "total_seconds": 1.072,
  "int_R_dV": 4.192473806507262,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.2890625,
  "negative_R_fraction": 0.7109375,
  "conductance_corr_R": 0.9767886020215342,
  "conductance_corr_RdV": 0.9994468136334013,
  "conductance_best_scale_s": 6.070880214339025,
  "conductance_relative_L2_error": 0.2142055717313575,
  "best_scale_s": 3.704291394303411,
  "relative_L2_error": 0.25788743428298294,
  "corr_raw_Rhat_R": 0.9661749692674196,
  "corr_scaled_R": 0.9661749692674315,
  "corr_raw_Rhat_RdV": 0.9997256004209331,
  "thresholded_sign_match": 1.0,
  "retained_fraction": 0.421875,
  "std_Rhat": 0.1719706772703863,
  "std_R": 0.6593314049196135
}
--- Running N=10 (1000 nodes) ---
{
  "N": 10,
  "nodes": 1000,
  "dx": 0.6283185307179586,
  "geometry_seconds": 0.001,
  "build_seconds": 0.04,
  "heat_seconds": 0.163,
  "total_seconds": 0.264,
  "int_R_dV": 4.192473805996394,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.5,
  "negative_R_fraction": 0.5,
  "conductance_corr_R": 0.9761843913251366,
  "conductance_corr_RdV": 0.9995443411498801,
  "conductance_best_scale_s": 5.7238841626734045,
  "conductance_relative_L2_error": 0.21694246733441136,
  "best_scale_s": 4.946787298720928,
  "relative_L2_error": 0.2626079671444135,
  "corr_raw_Rhat_R": 0.9649026145638999,
  "corr_scaled_R": 0.9649026145639088,
  "corr_raw_Rhat_RdV": 0.9996540828802489,
  "thresholded_sign_match": 1.0,
  "retained_fraction": 0.696,
  "std_Rhat": 0.1286067848672122,
  "std_R": 0.6593312115731242
}
--- Running N=12 (1728 nodes) ---
{
  "N": 12,
  "nodes": 1728,
  "dx": 0.5235987755982988,
  "geometry_seconds": 0.001,
  "build_seconds": 0.104,
  "heat_seconds": 0.264,
  "total_seconds": 0.459,
  "int_R_dV": 4.192473805996352,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.3263888888888889,
  "negative_R_fraction": 0.6736111111111112,
  "conductance_corr_R": 0.9758422003094591,
  "conductance_corr_RdV": 0.9995944749175587,
  "conductance_best_scale_s": 5.546260438490938,
  "conductance_relative_L2_error": 0.2184765435811729,
  "best_scale_s": 6.3282126875665785,
  "relative_L2_error": 0.2638095057561231,
  "corr_raw_Rhat_R": 0.9645747999365775,
  "corr_scaled_R": 0.9645747999365849,
  "corr_raw_Rhat_RdV": 0.9996346860470678,
  "thresholded_sign_match": 1.0,
  "retained_fraction": 0.5601851851851852,
  "std_Rhat": 0.10049824534983731,
  "std_R": 0.6593312113719603
}
--- Running N=14 (2744 nodes) ---
{
  "N": 14,
  "nodes": 2744,
  "dx": 0.4487989505128276,
  "geometry_seconds": 0.001,
  "build_seconds": 0.274,
  "heat_seconds": 0.705,
  "total_seconds": 1.123,
  "int_R_dV": 4.192473805996354,
  "R_min": -2.4297458536368053,
  "R_max": 1.333472797227092,
  "positive_R_fraction": 0.5,
  "negative_R_fraction": 0.5,
  "conductance_corr_R": 0.9756310243083643,
  "conductance_corr_RdV": 0.9996236415275072,
  "conductance_best_scale_s": 5.442635958891208,
  "conductance_relative_L2_error": 0.21941764834898816,
  "best_scale_s": 7.779463095004033,
  "relative_L2_error": 0.26342365877440543,
  "corr_raw_Rhat_R": 0.9646802454688749,
  "corr_scaled_R": 0.9646802454688806,
  "corr_raw_Rhat_RdV": 0.9996468679993146,
  "thresholded_sign_match": 1.0,
  "retained_fraction": 0.6268221574344023,
  "std_Rhat": 0.08175934342305742,
  "std_R": 0.6593312113718282
}

================ 3D CAMPAIGN SUMMARY ================
{
  "n_completed": 4,
  "N_completed": [
    8,
    10,
    12,
    14
  ],
  "scale_cv_across_grids": 0.2675395461387084,
  "corr_ok_all": true,
  "thresholded_sign_ok_all": true,
  "retained_ok_all": true,
  "final_error_lt_0p70": true,
  "scale_cv_lt_0p25": false,
  "conductance_corr_ok_all": true,
  "classification": "FULL_DIRECT_3D_HEAT_REFINEMENT_WEAK"
}

CSV_ROWS:
N,nodes,dx,int_R_dV,R_min,R_max,positive_R_fraction,negative_R_fraction,conductance_corr_R,conductance_corr_RdV,conductance_relative_L2_error,best_scale_s,relative_L2_error,corr_scaled_R,corr_raw_Rhat_R,corr_raw_Rhat_RdV,thresholded_sign_match,retained_fraction,std_Rhat,std_R,geometry_seconds,build_seconds,heat_seconds,total_seconds
8,512,0.7853981633974483,4.192473806507262,-2.4297458536368053,1.333472797227092,0.2890625,0.7109375,0.9767886020215342,0.9994468136334013,0.2142055717313575,3.704291394303411,0.25788743428298294,0.9661749692674315,0.9661749692674196,0.9997256004209331,1.0,0.421875,0.1719706772703863,0.6593314049196135,0.001,0.019,1.01,1.072
10,1000,0.6283185307179586,4.192473805996394,-2.4297458536368053,1.333472797227092,0.5,0.5,0.9761843913251366,0.9995443411498801,0.21694246733441136,4.946787298720928,0.2626079671444135,0.9649026145639088,0.9649026145638999,0.9996540828802489,1.0,0.696,0.1286067848672122,0.6593312115731242,0.001,0.04,0.163,0.264
12,1728,0.5235987755982988,4.192473805996352,-2.4297458536368053,1.333472797227092,0.3263888888888889,0.6736111111111112,0.9758422003094591,0.9995944749175587,0.2184765435811729,6.3282126875665785,0.2638095057561231,0.9645747999365849,0.9645747999365775,0.9996346860470678,1.0,0.5601851851851852,0.10049824534983731,0.6593312113719603,0.001,0.104,0.264,0.459
14,2744,0.4487989505128276,4.192473805996354,-2.4297458536368053,1.333472797227092,0.5,0.5,0.9756310243083643,0.9996236415275072,0.21941764834898816,7.779463095004033,0.26342365877440543,0.9646802454688806,0.9646802454688749,0.9996468679993146,1.0,0.6268221574344023,0.08175934342305742,0.6593312113718282,0.001,0.274,0.705,1.123
```

**End of file.**
