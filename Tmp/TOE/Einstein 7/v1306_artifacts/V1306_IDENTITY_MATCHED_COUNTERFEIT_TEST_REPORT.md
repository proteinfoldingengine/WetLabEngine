# V1306 — Identity-Matched Counterfeit Test

## Status

Completed.

## Purpose

V1305 froze this tentative causal diagram:

```text
retained path identity → B-like closure + ADM_M-like propagation
```

V1306 adversarially tests that by introducing identity-matched counterfeits.

## Candidate Summary

| mode                               |    mean_identity |   mean_closure |   mean_momentum |   mean_source_path |
|:-----------------------------------|-----------------:|---------------:|----------------:|-------------------:|
| identity_matched_current_flip      | 182224           |       2.93622  |        2.53861  |        1.70596e-07 |
| identity_matched_flow_phase_warp   |   3440.8         |       1.11507  |        1.27805  |        1.70596e-07 |
| identity_matched_local_spike       |  42593.3         |       1.04393  |        1.10629  |        1.70375e-07 |
| identity_matched_response_scramble |      9.99999e-07 |       6.51384  |        0.994446 |        1.70596e-07 |
| legitimate_transport               |      9.99999e-07 |       0.999926 |        0.994446 |        1.70596e-07 |
| source_shuffle                     | 485859           |       5.84089  |        3.45601  |        2.58981e-08 |
| time_reverse                       |      1.00036e+06 |       0.999926 |        2.09215  |        1.70596e-07 |

## Regime Summary

| regime                    |   valid_winner_rate |   mean_valid_weight |   mean_identity_counterfeit_weight |   mean_identity_residual |   mean_B_like_residual |   mean_ADM_M_residual |   mean_continuity_residual |   mean_flow_coherence |
|:--------------------------|--------------------:|--------------------:|-----------------------------------:|-------------------------:|-----------------------:|----------------------:|---------------------------:|----------------------:|
| identity_closure_momentum |                   1 |             1       |                        1.68128e-11 |              9.04352e-15 |               0.158384 |           0.000908071 |                   0.404325 |              0.999999 |
| identity_only             |                   1 |             0.50669 |                        0.49331     |              9.06065e-15 |               0.702272 |           0.000908071 |                   0.404325 |              0.999999 |
| identity_plus_closure     |                   1 |             1       |                        1.68128e-11 |              9.04352e-15 |               0.158384 |           0.000908071 |                   0.404325 |              0.999999 |
| identity_plus_momentum    |                   1 |             0.50669 |                        0.49331     |              9.05346e-15 |               0.702272 |           0.000908071 |                   0.404325 |              0.999999 |

## Interpretation

If identity-only admits identity-matched counterfeits, identity is not sufficient.

If identity+closure+momentum rejects them, the correct claim becomes:

```text
retained path identity is a strong common ancestor,
but adversarial sufficiency requires closure and momentum consistency.
```

## Next

V1307 should freeze the refined unification claim.
