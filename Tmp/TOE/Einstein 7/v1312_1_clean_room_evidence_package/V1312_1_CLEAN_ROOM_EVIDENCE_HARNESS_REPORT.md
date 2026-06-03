# V1312.1 — Clean-Room Evidence Harness Report

## Status

Completed.

## Claim Under Test

```text
identity + closure is a scaled, adversarially tested minimal sufficient stack
inside synthetic transport simulations.
```

## Summary by Regime

| regime                    |   valid_winner_rate |   mean_valid_weight |   mean_identity_counterfeit_weight |   counterfeit_pass_rate |   adm_pass_rate |   closure_pass_rate |   all_pass_rate |   mean_B_like_residual |   mean_ADM_M_residual |   mean_flow_coherence |
|:--------------------------|--------------------:|--------------------:|-----------------------------------:|------------------------:|----------------:|--------------------:|----------------:|-----------------------:|----------------------:|----------------------:|
| closure_only              |            0.791667 |            0.281312 |                          0.437376  |                       0 |               0 |                   1 |               0 |               0.17885  |           0.40809     |              0.916695 |
| closure_plus_momentum     |            1        |            0.838133 |                          0.161766  |                       0 |               0 |                   1 |               0 |               0.158972 |           0.0493636   |              0.99869  |
| identity_closure_momentum |            1        |            0.997852 |                          0.0021482 |                       1 |               1 |                   1 |               1 |               0.158436 |           0.000548754 |              1        |
| identity_only             |            0        |            0.200561 |                          0.799439  |                       0 |               1 |                   0 |               0 |               0.471822 |           0.000548754 |              1        |
| identity_plus_closure     |            1        |            0.997852 |                          0.0021482 |                       1 |               1 |                   1 |               1 |               0.158436 |           0.000548754 |              1        |
| identity_plus_momentum    |            0        |            0.200561 |                          0.799439  |                       0 |               1 |                   0 |               0 |               0.471822 |           0.000548754 |              1        |
| momentum_only             |            0        |            0.190286 |                          0.809692  |                       0 |               0 |                   0 |               0 |               0.44224  |           0.0430796   |              0.998922 |

## Candidate Summary

| mode                                |    mean_identity |   mean_closure |   mean_momentum |
|:------------------------------------|-----------------:|---------------:|----------------:|
| identity_matched_current_flip       | 176408           |       2.97526  |         3.29549 |
| identity_matched_flow_phase_warp    |   2634.75        |       1.11092  |         1.27329 |
| identity_matched_lagged_response    |      9.99999e-07 |       6.4873   |         1.00431 |
| identity_matched_local_spike        |  35779.6         |       1.04565  |         1.27496 |
| identity_matched_nonlinear_response |      9.99999e-07 |       2.55991  |         1.00431 |
| identity_matched_response_scramble  |      9.99999e-07 |       6.51606  |         1.00431 |
| identity_matched_spectral_response  |      9.99999e-07 |       2.49292  |         1.00431 |
| legitimate_transport                |      9.99999e-07 |       0.999838 |         1.00431 |
| source_shuffle                      | 484592           |       5.76691  |         4.63417 |
| time_reverse                        |      1.15125e+06 |       0.999838 |         2.02827 |

## Scale Summary

| regime                    |   N |   T |   all_pass_rate |   mean_valid_weight |   mean_identity_counterfeit_weight |   mean_B_like_residual |   mean_ADM_M_residual |
|:--------------------------|----:|----:|----------------:|--------------------:|-----------------------------------:|-----------------------:|----------------------:|
| closure_only              |  96 |   6 |               0 |            0.281661 |                         0.436677   |               0.176866 |           0.407888    |
| closure_only              |  96 |   8 |               0 |            0.280992 |                         0.438016   |               0.179829 |           0.404872    |
| closure_only              |  96 |  10 |               0 |            0.280826 |                         0.438347   |               0.180088 |           0.400304    |
| closure_only              | 128 |   6 |               0 |            0.281529 |                         0.436941   |               0.179868 |           0.409018    |
| closure_only              | 128 |   8 |               0 |            0.281281 |                         0.437438   |               0.178527 |           0.408244    |
| closure_only              | 128 |  10 |               0 |            0.281013 |                         0.437974   |               0.1786   |           0.408859    |
| closure_only              | 160 |   6 |               0 |            0.282016 |                         0.435968   |               0.179005 |           0.412754    |
| closure_only              | 160 |   8 |               0 |            0.281311 |                         0.437377   |               0.179105 |           0.412513    |
| closure_only              | 160 |  10 |               0 |            0.281179 |                         0.437642   |               0.177763 |           0.408356    |
| closure_plus_momentum     |  96 |   6 |               0 |            0.68845  |                         0.311504   |               0.159797 |           0.056866    |
| closure_plus_momentum     |  96 |   8 |               0 |            0.826577 |                         0.17326    |               0.158872 |           0.0573568   |
| closure_plus_momentum     |  96 |  10 |               0 |            0.893735 |                         0.106129   |               0.159595 |           0.0422879   |
| closure_plus_momentum     | 128 |   6 |               0 |            0.750703 |                         0.249252   |               0.159068 |           0.0583631   |
| closure_plus_momentum     | 128 |   8 |               0 |            0.879818 |                         0.120084   |               0.15909  |           0.0465289   |
| closure_plus_momentum     | 128 |  10 |               0 |            0.922867 |                         0.0769921  |               0.158582 |           0.040318    |
| closure_plus_momentum     | 160 |   6 |               0 |            0.778802 |                         0.221162   |               0.159267 |           0.055228    |
| closure_plus_momentum     | 160 |   8 |               0 |            0.872607 |                         0.12727    |               0.1583   |           0.0510495   |
| closure_plus_momentum     | 160 |  10 |               0 |            0.929639 |                         0.070243   |               0.158173 |           0.0362745   |
| identity_closure_momentum |  96 |   6 |               1 |            0.998398 |                         0.00160158 |               0.158617 |           0.0006176   |
| identity_closure_momentum |  96 |   8 |               1 |            0.997904 |                         0.00209575 |               0.158305 |           0.000439142 |
| identity_closure_momentum |  96 |  10 |               1 |            0.997537 |                         0.0024628  |               0.159319 |           0.00061951  |
| identity_closure_momentum | 128 |   6 |               1 |            0.998306 |                         0.00169378 |               0.158147 |           0.000721623 |
| identity_closure_momentum | 128 |   8 |               1 |            0.997768 |                         0.00223201 |               0.158728 |           0.000530583 |
| identity_closure_momentum | 128 |  10 |               1 |            0.997432 |                         0.00256753 |               0.158418 |           0.000602431 |
| identity_closure_momentum | 160 |   6 |               1 |            0.998224 |                         0.0017759  |               0.158458 |           0.000284168 |
| identity_closure_momentum | 160 |   8 |               1 |            0.997735 |                         0.0022646  |               0.157904 |           0.000580035 |
| identity_closure_momentum | 160 |  10 |               1 |            0.99736  |                         0.00263983 |               0.158025 |           0.000543695 |
| identity_only             |  96 |   6 |               0 |            0.200907 |                         0.799093   |               0.45717  |           0.0006176   |
| identity_only             |  96 |   8 |               0 |            0.200662 |                         0.799338   |               0.459304 |           0.000439142 |
| identity_only             |  96 |  10 |               0 |            0.200431 |                         0.799569   |               0.476348 |           0.00061951  |
| identity_only             | 128 |   6 |               0 |            0.2007   |                         0.7993     |               0.479638 |           0.000721623 |
| identity_only             | 128 |   8 |               0 |            0.200549 |                         0.799451   |               0.468443 |           0.000530583 |
| identity_only             | 128 |  10 |               0 |            0.200398 |                         0.799602   |               0.466133 |           0.000602431 |
| identity_only             | 160 |   6 |               0 |            0.200627 |                         0.799373   |               0.477022 |           0.000284168 |
| identity_only             | 160 |   8 |               0 |            0.200436 |                         0.799564   |               0.478356 |           0.000580035 |
| identity_only             | 160 |  10 |               0 |            0.200336 |                         0.799664   |               0.483983 |           0.000543695 |
| identity_plus_closure     |  96 |   6 |               1 |            0.998398 |                         0.00160158 |               0.158617 |           0.0006176   |
| identity_plus_closure     |  96 |   8 |               1 |            0.997904 |                         0.00209575 |               0.158305 |           0.000439142 |
| identity_plus_closure     |  96 |  10 |               1 |            0.997537 |                         0.0024628  |               0.159319 |           0.00061951  |
| identity_plus_closure     | 128 |   6 |               1 |            0.998306 |                         0.00169378 |               0.158147 |           0.000721623 |
| identity_plus_closure     | 128 |   8 |               1 |            0.997768 |                         0.00223201 |               0.158728 |           0.000530583 |
| identity_plus_closure     | 128 |  10 |               1 |            0.997432 |                         0.00256753 |               0.158418 |           0.000602431 |
| identity_plus_closure     | 160 |   6 |               1 |            0.998224 |                         0.0017759  |               0.158458 |           0.000284168 |
| identity_plus_closure     | 160 |   8 |               1 |            0.997735 |                         0.0022646  |               0.157904 |           0.000580035 |
| identity_plus_closure     | 160 |  10 |               1 |            0.99736  |                         0.00263983 |               0.158025 |           0.000543695 |
| identity_plus_momentum    |  96 |   6 |               0 |            0.200907 |                         0.799093   |               0.45717  |           0.0006176   |
| identity_plus_momentum    |  96 |   8 |               0 |            0.200662 |                         0.799338   |               0.459304 |           0.000439142 |
| identity_plus_momentum    |  96 |  10 |               0 |            0.200431 |                         0.799569   |               0.476348 |           0.00061951  |
| identity_plus_momentum    | 128 |   6 |               0 |            0.2007   |                         0.7993     |               0.479638 |           0.000721623 |
| identity_plus_momentum    | 128 |   8 |               0 |            0.200549 |                         0.799451   |               0.468443 |           0.000530583 |
| identity_plus_momentum    | 128 |  10 |               0 |            0.200398 |                         0.799602   |               0.466133 |           0.000602431 |
| identity_plus_momentum    | 160 |   6 |               0 |            0.200627 |                         0.799373   |               0.477022 |           0.000284168 |
| identity_plus_momentum    | 160 |   8 |               0 |            0.200436 |                         0.799564   |               0.478356 |           0.000580035 |
| identity_plus_momentum    | 160 |  10 |               0 |            0.200336 |                         0.799664   |               0.483983 |           0.000543695 |
| momentum_only             |  96 |   6 |               0 |            0.179886 |                         0.820102   |               0.40102  |           0.0542006   |
| momentum_only             |  96 |   8 |               0 |            0.189733 |                         0.81023    |               0.427337 |           0.0505464   |
| momentum_only             |  96 |  10 |               0 |            0.19383  |                         0.80614    |               0.45653  |           0.035371    |
| momentum_only             | 128 |   6 |               0 |            0.184784 |                         0.815204   |               0.432749 |           0.0533508   |
| momentum_only             | 128 |   8 |               0 |            0.193278 |                         0.806701   |               0.447201 |           0.0389742   |
| momentum_only             | 128 |  10 |               0 |            0.195527 |                         0.804443   |               0.452059 |           0.0332784   |
| momentum_only             | 160 |   6 |               0 |            0.186938 |                         0.813054   |               0.437208 |           0.0469226   |
| momentum_only             | 160 |   8 |               0 |            0.192684 |                         0.807289   |               0.455467 |           0.0450394   |
| momentum_only             | 160 |  10 |               0 |            0.195911 |                         0.804065   |               0.470586 |           0.0300332   |

## Auditor Use

Use these outputs to attack:

```text
identity leakage
closure tautology
counterfeit diversity
ADM_M diagnostic dependence
scaling limits
minimality
```

## Boundary

This does not claim physical GR, Einstein equations, full ADM derivation, or physical spacetime curvature.
