# V1400 — Local Constraint Propagation Bridge

## Status
Completed.

## Summary by Regime
| regime                |   valid_winner_rate |   mean_valid_weight |   mean_H |    mean_M |   mean_continuity |   mean_alignment |
|:----------------------|--------------------:|--------------------:|---------:|----------:|------------------:|-----------------:|
| closure_only          |                   0 |           0.0108556 |  1.01732 | 1.34021   |          1.08821  |        0.949908  |
| identity_only         |                   1 |           0.51185   |  1.02301 | 0.0187317 |          0.425716 |        0.0688271 |
| identity_plus_closure |                   1 |           1         |  1.0204  | 0.0187317 |          0.425716 |       -0.0843984 |
| weak_control          |                   0 |           0.1597    |  1.05081 | 0.841241  |          0.89792  |        0.0202093 |

## Deltas vs Identity + Closure
| regime                |   delta_H_vs_identity_closure |   delta_M_vs_identity_closure |   delta_continuity_vs_identity_closure |
|:----------------------|------------------------------:|------------------------------:|---------------------------------------:|
| closure_only          |                   -0.0030824  |                   1.32148     |                               0.66249  |
| identity_only         |                    0.00260237 |                  -1.73472e-17 |                               0        |
| identity_plus_closure |                    0          |                   0           |                               0        |
| weak_control          |                    0.0304072  |                   0.82251     |                               0.472204 |

## Boundary
Synthetic ADM-like diagnostics only. No physical GR or Einstein equation claim.
