# V1401.0 — Full-Stack Baseline Harness Report

## Status
Completed.

## Purpose
Anti-regression canonical runnable simulation:

```text
Genesis key
→ candidate histories
→ pruning / retained weights
→ retained accessibility network
→ identity + closure
→ Ω / curvature-like geometry proxy
→ local M / continuity diagnostics
→ candidate H diagnostics
→ ADM-like local constraint report
```

## Summary by Regime
| regime                    |   valid_winner_rate |   mean_valid_weight |   mean_H_current |    mean_M |   mean_continuity |   mean_alignment |
|:--------------------------|--------------------:|--------------------:|-----------------:|----------:|------------------:|-----------------:|
| closure_only              |                   0 |           0.0106789 |          1.0246  | 1.36839   |          1.08518  |        0.969968  |
| full_stack                |                   1 |           1         |          1.02976 | 0.0193896 |          0.416027 |       -0.0928208 |
| identity_closure_momentum |                   1 |           0.5       |          1.02976 | 0.0193896 |          0.416027 |       -0.0928208 |
| identity_only             |                   1 |           0.33856   |          1.03146 | 0.0193896 |          0.416027 |       -0.0204575 |
| identity_plus_closure     |                   1 |           0.5       |          1.02976 | 0.0193896 |          0.416027 |       -0.0928208 |
| weak_control              |                   0 |           0.137878  |          1.07196 | 0.85217   |          0.914103 |        0.0190899 |

## Summary by H Definition
| regime                    | H_definition     |   mean_H_residual |   mean_M_residual |   mean_continuity_residual |   mean_source_flow_alignment |
|:--------------------------|:-----------------|------------------:|------------------:|---------------------------:|-----------------------------:|
| closure_only              | H_current        |          1.0246   |         1.36839   |                   1.08518  |                    0.969968  |
| closure_only              | H_response_only  |          1.14176  |         1.36839   |                   1.08518  |                    0.969968  |
| closure_only              | H_rho_omega      |          1.00124  |         1.36839   |                   1.08518  |                    0.969968  |
| closure_only              | H_source_divflow |          1.13505  |         1.36839   |                   1.08518  |                    0.969968  |
| closure_only              | H_source_only    |          0.975822 |         1.36839   |                   1.08518  |                    0.969968  |
| full_stack                | H_current        |          1.02976  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| full_stack                | H_response_only  |          1.15473  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| full_stack                | H_rho_omega      |          0.928621 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| full_stack                | H_source_divflow |          0.90739  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| full_stack                | H_source_only    |          0.977516 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_closure_momentum | H_current        |          1.02976  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_closure_momentum | H_response_only  |          1.15473  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_closure_momentum | H_rho_omega      |          0.928621 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_closure_momentum | H_source_divflow |          0.90739  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_closure_momentum | H_source_only    |          0.977516 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_only             | H_current        |          1.03146  |         0.0193896 |                   0.416027 |                   -0.0204575 |
| identity_only             | H_response_only  |          1.1719   |         0.0193896 |                   0.416027 |                   -0.0204575 |
| identity_only             | H_rho_omega      |          0.928621 |         0.0193896 |                   0.416027 |                   -0.0204575 |
| identity_only             | H_source_divflow |          0.90739  |         0.0193896 |                   0.416027 |                   -0.0204575 |
| identity_only             | H_source_only    |          0.977516 |         0.0193896 |                   0.416027 |                   -0.0204575 |
| identity_plus_closure     | H_current        |          1.02976  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_plus_closure     | H_response_only  |          1.15473  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_plus_closure     | H_rho_omega      |          0.928621 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_plus_closure     | H_source_divflow |          0.90739  |         0.0193896 |                   0.416027 |                   -0.0928208 |
| identity_plus_closure     | H_source_only    |          0.977516 |         0.0193896 |                   0.416027 |                   -0.0928208 |
| weak_control              | H_current        |          1.07196  |         0.85217   |                   0.914103 |                    0.0190899 |
| weak_control              | H_response_only  |          1.20331  |         0.85217   |                   0.914103 |                    0.0190899 |
| weak_control              | H_rho_omega      |          1.06498  |         0.85217   |                   0.914103 |                    0.0190899 |
| weak_control              | H_source_divflow |          0.961714 |         0.85217   |                   0.914103 |                    0.0190899 |
| weak_control              | H_source_only    |          1.00942  |         0.85217   |                   0.914103 |                    0.0190899 |

## Interpretation
Identity + closure preserves valid retained path and strongly supports local M-like / continuity propagation. H-like scalar closure remains unresolved.

## Boundary
Synthetic ADM-like diagnostics only. No physical GR, Einstein equations, full ADM derivation, physical spacetime, or physical curvature is claimed.
