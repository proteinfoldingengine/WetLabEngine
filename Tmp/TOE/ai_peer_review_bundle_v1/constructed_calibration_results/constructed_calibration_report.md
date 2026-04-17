# Constructed Calibration Results
## First anchored restricted theorem calibration run

This is the first full anchored calibration pass using the constructed calibration dataset.

## Runner status
Return code: 0

## Anchor constants
      C0       V0  lambda0       a0       b0  sigma_p  sqrt_E_r4
0.007771 0.003018 1.311173 0.459965 0.002386 0.205478   0.004438

## Calibration summary
 n_points  mean_abs_epsilon  mean_bound  mean_margin  min_margin  all_points_within_bound  mean_lambda_drift  mean_eta_nu  mean_M_theta
        7          0.005457    0.007378     0.001921    0.001482                     True           0.095608      0.10881       0.10836

## Screened family table
                         label  alpha  beta   nu  delta_cov  delta_var  lambda_theta  lambda_drift  eta_nu_theta  M_theta  epsilon_observed  epsilon_bound  bound_minus_abs_epsilon
constructed_screened_point_001   1.18  1.08 0.08   0.014838   0.033820      1.269277      0.041896      0.083326 0.095355         -0.003104       0.004587                 0.001482
constructed_screened_point_002   1.20  1.10 0.10   0.015918   0.038708      1.366613      0.055440      0.097388 0.099369         -0.004273       0.005992                 0.001720
constructed_screened_point_003   1.22  1.12 0.10   0.015918   0.039462      1.339551      0.028377      0.101467 0.104097         -0.004619       0.006431                 0.001812
constructed_screened_point_004   1.24  1.14 0.11   0.016211   0.042221      1.363423      0.052249      0.111436 0.108737         -0.005595       0.007578                 0.001982
constructed_screened_point_005   1.26  1.16 0.12   0.016048   0.043763      1.424713      0.113539      0.118912 0.111827         -0.006468       0.008509                 0.002042
constructed_screened_point_006   1.28  1.18 0.12   0.017694   0.048153      1.455227      0.144053      0.123116 0.117581         -0.006841       0.009060                 0.002219
constructed_screened_point_007   1.30  1.20 0.13   0.017675   0.049112      1.544875      0.233701      0.126027 0.121553         -0.007301       0.009491                 0.002190

## Read
- `a0` and `b0` are now numerically anchored on the constructed baseline.
- The empirical cloud was evaluated against the anchored affine line.
- The observed remainder was checked against the theorem-controlled bound.
- In this run, all screened points remained within the predicted bound.

## Important scope note
These are **constructed-data calibration results**, not external or measured data results.
They validate the anchored calibration workflow and provide the first full internal restricted-calibration packet.
