# V833 Action-Term Discovery After V832 Stationarity Failure

## Purpose

V832 showed the unified ADM-like constraints remain strong, but the first V831 action was not the correct variational principle.

V833 tests which action-term family is favored by held-out constraint transfer.

## Candidate families

```text
V831_second_order:       d²J, ∇(∇·J), J
V828_first_order:        J, dJ/dτ, ∇·J
mixed_EL_first_second:   J, dJ, d²J, divJ, graddivJ
weighted_flow_action:    J, dJ, divJ, A·J, A·dJ, u·J
full_discovery:          all candidate terms
ham_access:              lapu, A, grad_energy, divJ
```

## Summary

```text
best candidate: full_discovery
best mean R²: 0.857
best min R²: 0.719
best corr: 0.937

V831 second-order momentum R²: 0.001
V828 first-order momentum R²:  0.864
mixed momentum R²:             0.863
weighted-flow momentum R²:     0.865
```

## Overall

| candidate | mean R² | min R² | corr |
|---|---:|---:|---:|
| full_discovery | 0.857 | 0.719 | 0.937 |
| weighted_flow_action | 0.838 | 0.562 | 0.927 |
| V828_first_order | 0.837 | 0.562 | 0.927 |
| mixed_EL_first_second | 0.837 | 0.562 | 0.926 |
| ham_access | 0.291 | -0.009 | 0.406 |
| V831_second_order | -0.001 | -0.016 | 0.020 |

## By constraint

| candidate | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| full_discovery | H | 0.841 | 0.719 | 0.921 |
| ham_access | H | 0.820 | 0.685 | 0.910 |
| V828_first_order | H | 0.784 | 0.562 | 0.889 |
| mixed_EL_first_second | H | 0.784 | 0.562 | 0.889 |
| weighted_flow_action | H | 0.784 | 0.562 | 0.889 |
| V831_second_order | H | -0.005 | -0.016 | nan |
| full_discovery | Mx | 0.867 | 0.829 | 0.946 |
| weighted_flow_action | Mx | 0.867 | 0.828 | 0.945 |
| V828_first_order | Mx | 0.865 | 0.828 | 0.945 |
| mixed_EL_first_second | Mx | 0.865 | 0.828 | 0.945 |
| ham_access | Mx | 0.039 | 0.013 | 0.191 |
| V831_second_order | Mx | 0.001 | -0.000 | 0.032 |
| weighted_flow_action | My | 0.864 | 0.832 | 0.945 |
| full_discovery | My | 0.863 | 0.832 | 0.945 |
| V828_first_order | My | 0.862 | 0.833 | 0.945 |
| mixed_EL_first_second | My | 0.862 | 0.833 | 0.945 |
| ham_access | My | 0.015 | -0.009 | 0.118 |
| V831_second_order | My | 0.000 | -0.001 | 0.009 |

## Verdict

```text
first_order_dissipative_action_favored
```

## Interpretation

If first-order terms dominate, the correct action is likely dissipative / Onsager-like, not conservative second-order Euler-Lagrange.
