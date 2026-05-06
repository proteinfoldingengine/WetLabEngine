# FULL_DIRECT_HEAT_REFINEMENT_COLAB_RESULT.md

# Full Direct Heat-Diagonal Refinement Colab Result
## Direct local heat-kernel curvature recovery on validated conformal torus reference

## Status
**Major 2D local curvature diagnostic milestone. Not theorem closure.**

This file records the Colab/T4 result for the full direct heat-diagonal refinement campaign.

This is important because the previous extended refinement campaign used the conductance surrogate:

\[
-(d_i-\langle d\rangle)\sim R_i.
\]

The Colab run now confirms that the full direct heat-kernel diagonal itself remains strong at larger grids.

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
N = 24, 32, 40, 48
```

Node counts:

```text
576, 1024, 1600, 2304
```

Estimator:

\[
K_{\mathcal G}(t,i,i)=[e^{-tL}]_{ii}
\]

\[
Y_i(t)=K_{\mathcal G}(t,i,i)(4\pi t)
\]

\[
Y_i(t)\approx A_i+B_it
\]

\[
\widehat R_i=-6B_i.
\]

---

# 2. Campaign result

Classification:

```text
FULL_DIRECT_HEAT_REFINEMENT_PROMISING
```

The campaign passed all predefined checks:

```text
corr_ok_all: true
thresholded_sign_ok_all: true
retained_ok_all: true
final_error_lt_0p45: true
scale_cv_lt_0p25: true
```

Scale stability:

```text
scale_cv_across_grids: 0.0364
```

This is strong.

---

# 3. Key numeric trend

Correlation improved slightly with refinement:

```text
N=24: corr_scaled_R = 0.9232
N=32: corr_scaled_R = 0.9264
N=40: corr_scaled_R = 0.9281
N=48: corr_scaled_R = 0.9291
```

Curvature-density correlation stayed extremely high:

```text
N=24: corr_RdV = 0.9915
N=32: corr_RdV = 0.9926
N=40: corr_RdV = 0.9932
N=48: corr_RdV = 0.9935
```

Relative \(L^2\) error improved:

```text
N=24: 0.3843
N=32: 0.3766
N=40: 0.3724
N=48: 0.3699
```

Thresholded sign recovery stayed strong:

```text
N=24: 1.0000
N=32: 0.9895
N=40: 0.9806
N=48: 0.9910
```

---

# 4. Interpretation

This is the strongest local heat-kernel curvature result so far.

The full direct heat diagonal confirms the earlier conductance mechanism:

```text
conductance surrogate was not merely a shortcut
```

The actual heat-kernel diagonal preserves the local curvature-density signal under larger refinement.

The local result now supports:

```text
shape recovery: strong
curvature-density correlation: very strong
thresholded sign recovery: strong
magnitude up to stable scale: promising
larger-grid direct heat validation: passed through N=48
```

---

# 5. What this does not prove

This still does not prove:

\[
R_{\mathcal G}\rightarrow R
\]

as a theorem.

Still open:

1. derive the sign correction;
2. derive the scale factor;
3. prove heat-window scaling;
4. test more metrics;
5. extend to 3D;
6. connect local \(R\) density to ADM action;
7. prove graph-to-Laplace-Beltrami convergence.

---

# 6. Updated status

Before this run:

```text
direct heat local tests: strong on small grids
conductance mechanism: strong on larger grids
```

After this run:

```text
direct heat local tests: strong through N=48 on T4
conductance mechanism validated as explanatory support
```

This moves the branch from:

```text
conductance-supported surrogate
```

to:

```text
direct heat-kernel local curvature diagnostic milestone
```

---

# 7. Recommended next step

The next best file is:

```text
LOCAL_HEAT_CURVATURE_STATUS_FINAL_2D.md
```

Purpose:

Freeze the 2D local heat-curvature result:

```text
validated reference geometry
direct heat diagonal passed through N=48
sign-corrected field tracks R
thresholded sign recovery passed
magnitude up to stable scale passed
remaining theorem obligations listed
```

After that, choose between:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
```

or:

```text
HEAT_CURVATURE_TO_ADM_ACTION.md
```

My recommendation:

```text
HEAT_KERNEL_3D_SPATIAL_TESTS.md
```

because GR needs:

\[
R^{(3)}.
\]

---

# 8. Raw Colab output

```text
Torch available: True
Device: cuda
GPU: Tesla T4

Running full direct heat-diagonal refinement...
N_LIST: [24, 32, 40, 48]
AMP: 0.25
TIME_MULTIPLIERS: [0.8, 1.2, 1.8]
SIGN_THRESHOLD: 0.1

--- Running N=24 (576 nodes) ---
{
  "N": 24,
  "nodes": 576,
  "dx": 0.2617993877991494,
  "gauss_bonnet_error": 1.2576745200831851e-16,
  "build_seconds": 0.013,
  "heat_seconds": 0.712,
  "total_seconds": 0.778,
  "best_scale_s": 3.5723078289167907,
  "relative_L2_error": 0.3843214875241444,
  "corr_raw_Rhat_R": 0.9231993252960974,
  "corr_scaled_R": 0.9231993252961119,
  "corr_raw_Rhat_RdV": 0.991533398510887,
  "thresholded_sign_match": 1.0,
  "retained_fraction": 0.7430555555555556,
  "std_Rhat": 0.14345066006632398,
  "std_R": 0.5550804706815449
}
--- Running N=32 (1024 nodes) ---
{
  "N": 32,
  "nodes": 1024,
  "dx": 0.19634954084936207,
  "gauss_bonnet_error": 1.6002824065886043e-16,
  "build_seconds": 0.048,
  "heat_seconds": 0.163,
  "total_seconds": 0.28,
  "best_scale_s": 3.7716590899835447,
  "relative_L2_error": 0.37664963521392164,
  "corr_raw_Rhat_R": 0.9263557914177369,
  "corr_scaled_R": 0.9263557914177457,
  "corr_raw_Rhat_RdV": 0.9926131436258487,
  "thresholded_sign_match": 0.9895287958115183,
  "retained_fraction": 0.74609375,
  "std_Rhat": 0.13633310870653356,
  "std_R": 0.5550804706815449
}
--- Running N=40 (1600 nodes) ---
{
  "N": 40,
  "nodes": 1600,
  "dx": 0.15707963267948966,
  "gauss_bonnet_error": 1.457167719820518e-16,
  "build_seconds": 0.1,
  "heat_seconds": 0.267,
  "total_seconds": 0.47,
  "best_scale_s": 3.87547979691999,
  "relative_L2_error": 0.3724081550099972,
  "corr_raw_Rhat_R": 0.928069052431996,
  "corr_scaled_R": 0.9280690524320018,
  "corr_raw_Rhat_RdV": 0.9931741814387971,
  "thresholded_sign_match": 0.9805825242718447,
  "retained_fraction": 0.7725,
  "std_Rhat": 0.13292625260447183,
  "std_R": 0.5550804706815448
}
--- Running N=48 (2304 nodes) ---
{
  "N": 48,
  "nodes": 2304,
  "dx": 0.1308996938995747,
  "gauss_bonnet_error": 8.543513119185775e-17,
  "build_seconds": 0.185,
  "heat_seconds": 0.453,
  "total_seconds": 0.798,
  "best_scale_s": 3.9353516074615666,
  "relative_L2_error": 0.3698952063982705,
  "corr_raw_Rhat_R": 0.9290734827146668,
  "corr_scaled_R": 0.9290734827146709,
  "corr_raw_Rhat_RdV": 0.9934943648841913,
  "thresholded_sign_match": 0.9909706546275395,
  "retained_fraction": 0.7690972222222222,
  "std_Rhat": 0.13104560850552308,
  "std_R": 0.5550804706815448
}

================ CAMPAIGN SUMMARY ================
{
  "n_completed": 4,
  "N_completed": [
    24,
    32,
    40,
    48
  ],
  "scale_cv_across_grids": 0.03641870166068641,
  "corr_ok_all": true,
  "thresholded_sign_ok_all": true,
  "retained_ok_all": true,
  "final_error_lt_0p45": true,
  "scale_cv_lt_0p25": true,
  "classification": "FULL_DIRECT_HEAT_REFINEMENT_PROMISING"
}

CSV_ROWS:
N,nodes,dx,gauss_bonnet_error,best_scale_s,relative_L2_error,corr_scaled_R,corr_raw_Rhat_R,corr_raw_Rhat_RdV,thresholded_sign_match,retained_fraction,std_Rhat,std_R,build_seconds,heat_seconds,total_seconds
24,576,0.2617993877991494,1.2576745200831851e-16,3.5723078289167907,0.3843214875241444,0.9231993252961119,0.9231993252960974,0.991533398510887,1.0,0.7430555555555556,0.14345066006632398,0.5550804706815449,0.013,0.712,0.778
32,1024,0.19634954084936207,1.6002824065886043e-16,3.7716590899835447,0.37664963521392164,0.9263557914177457,0.9263557914177369,0.9926131436258487,0.9895287958115183,0.74609375,0.13633310870653356,0.5550804706815449,0.048,0.163,0.28
40,1600,0.15707963267948966,1.457167719820518e-16,3.87547979691999,0.3724081550099972,0.9280690524320018,0.928069052431996,0.9931741814387971,0.9805825242718447,0.7725,0.13292625260447183,0.5550804706815448,0.1,0.267,0.47
48,2304,0.1308996938995747,8.543513119185775e-17,3.9353516074615666,0.3698952063982705,0.9290734827146709,0.9290734827146668,0.9934943648841913,0.9909706546275395,0.7690972222222222,0.13104560850552308,0.5550804706815448,0.185,0.453,0.798
```

---

# Honest status line

> `FULL_DIRECT_HEAT_REFINEMENT_COLAB_RESULT.md` records a major direct heat-kernel local curvature milestone: on a validated periodic conformal grid, the sign-corrected local heat diagonal recovers analytic curvature shape, sign, and magnitude up to stable scale across \(N=24,32,40,48\) on T4. This is not theorem closure, but it is the strongest local curvature result so far.

**End of file.**
