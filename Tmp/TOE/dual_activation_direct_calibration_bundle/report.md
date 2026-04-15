# Direct calibration of dual activations

Goal:
Keep the hybrid structure fixed and tune only the activation maps:

chi_class,t = sigma(alpha_c * z(1 - D_class,t) - theta_c)
chi_band,t  = sigma(alpha_b * z(Z_band,t) - theta_b)

Grid searched:
- alpha_c, theta_c
- alpha_b, theta_b

## Best calibration
alpha_c=3.0
theta_c=-1.0
alpha_b=0.5
theta_b=-0.2

## Top 10
 alpha_c  theta_c  alpha_b  theta_b  mean_auc  mean_gap  mean_chi_c  mean_chi_b    score
     3.0     -1.0      0.5     -0.2  0.574243  0.037500    0.603923    0.546334 0.575360
     3.0     -1.0      1.0     -0.2  0.573840  0.037500    0.603923    0.538127 0.575204
     2.5     -1.0      0.5     -0.2  0.574261  0.037500    0.617152    0.546334 0.574982
     2.5     -1.0      0.5      1.0  0.577996  0.045833    0.617152    0.278972 0.574726
     3.0     -1.0      2.5     -0.2  0.572799  0.037500    0.603923    0.520149 0.574701
     3.0     -1.0      3.0     -1.0  0.574641  0.041667    0.603923    0.608191 0.574528
     3.0     -1.0      3.0     -0.6  0.573868  0.037500    0.603923    0.563515 0.574470
     2.0     -1.0      0.5      1.0  0.578109  0.045833    0.636483    0.278972 0.574259
     2.5     -1.0      2.0     -0.2  0.572225  0.041667    0.617152    0.524183 0.574235
     3.0     -1.0      0.5      0.2  0.573778  0.033333    0.603923    0.452121 0.574224

## Summary
                     model regime  roc_auc  low_q_success32  high_q_success32  success32_gap_high_minus_low  mean_lambda
                 core_only      A 0.410080         0.050000          0.016667                     -0.033333     0.519484
                 core_only      B 0.351673         0.066667          0.000000                     -0.066667     0.502050
                 core_only      C 0.585741         0.033333          0.066667                      0.033333     0.475787
                 core_only      D 0.537632         0.050000          0.083333                      0.033333     0.490444
       full_shared_context      A 0.453608         0.050000          0.016667                     -0.033333     0.284460
       full_shared_context      B 0.583627         0.016667          0.050000                      0.033333     0.578815
       full_shared_context      C 0.662232         0.016667          0.083333                      0.066667     0.573644
       full_shared_context      D 0.503961         0.033333          0.016667                     -0.016667     0.547039
      dual_activation_prev      A 0.465827         0.033333          0.016667                     -0.016667     0.482103
      dual_activation_prev      B 0.517386         0.033333          0.033333                      0.000000     0.577232
      dual_activation_prev      C 0.646851         0.016667          0.083333                      0.066667     0.559715
      dual_activation_prev      D 0.530590         0.050000          0.033333                     -0.016667     0.553489
dual_activation_calibrated      A 0.478427         0.033333          0.016667                     -0.016667     0.387636
dual_activation_calibrated      B 0.593750         0.016667          0.066667                      0.050000     0.565149
dual_activation_calibrated      C 0.694866         0.016667          0.116667                      0.100000     0.556980
dual_activation_calibrated      D 0.529930         0.033333          0.050000                      0.016667     0.533798

## Mean AUC by model
                     model  roc_auc
                 core_only 0.471282
dual_activation_calibrated 0.574243
      dual_activation_prev 0.540164
       full_shared_context 0.550857

Interpretation:
This directly tests whether the locked hybrid dual-activation structure becomes stronger when only the activation maps are calibrated.
