# V829 Unified ADM-like Constraint Audit

## Purpose

Test whether the Hamiltonian-like and momentum-like wins can be unified into one ADM-like accessibility-flow constraint system.

## Unified accessibility-flow model

```text
Hamiltonian source: accessibility curvature / ΔlogA / A
Momentum source: J, dJ/dτ, divJ
```

## Summary

```text
best feature set: unified_all
best overall mean R²: 0.900
best overall min R²: 0.824
best overall corr: 0.949
```

## Unified accessibility-flow by constraint

```text
H  mean R²: 0.802 | min R²: 0.773 | corr: 0.899
Mx mean R²: 0.853 | min R²: 0.840 | corr: 0.924
My mean R²: 0.848 | min R²: 0.824 | corr: 0.922
```

## Overall feature-set comparison

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| unified_all | 0.900 | 0.824 | 0.949 |
| unified_access_flow | 0.834 | 0.773 | 0.915 |
| flow_only | 0.826 | 0.736 | 0.910 |
| adm_geometric_only | 0.344 | -0.007 | 0.423 |
| accessibility_only | 0.280 | 0.002 | 0.398 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| adm_geometric_only | H | 1.000 | 1.000 | 1.000 |
| unified_all | H | 1.000 | 1.000 | 1.000 |
| unified_access_flow | H | 0.802 | 0.773 | 0.899 |
| accessibility_only | H | 0.797 | 0.773 | 0.896 |
| flow_only | H | 0.774 | 0.736 | 0.881 |
| flow_only | Mx | 0.854 | 0.842 | 0.925 |
| unified_access_flow | Mx | 0.853 | 0.840 | 0.924 |
| unified_all | Mx | 0.853 | 0.838 | 0.924 |
| accessibility_only | Mx | 0.019 | 0.002 | 0.140 |
| adm_geometric_only | Mx | 0.016 | -0.004 | 0.131 |
| flow_only | My | 0.849 | 0.824 | 0.923 |
| unified_access_flow | My | 0.848 | 0.824 | 0.922 |
| unified_all | My | 0.848 | 0.824 | 0.922 |
| accessibility_only | My | 0.024 | 0.003 | 0.158 |
| adm_geometric_only | My | 0.017 | -0.007 | 0.137 |

## Verdict

```text
full_adm_like_constraint_system_supported
```

## Interpretation

A full ADM-like claim requires Hamiltonian-like and both momentum-like constraints to transfer together under the same accessibility-flow ontology.
