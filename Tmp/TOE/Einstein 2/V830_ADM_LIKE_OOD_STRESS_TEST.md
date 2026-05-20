# V830 ADM-like OOD Stress Test

## Purpose

V829 supported a unified ADM-like constraint system in-family.

V830 tests out-of-distribution dynamics:

```text
radial
shear
counter-rotating
noisy repair
```

## Summary

```text
best feature set: unified_all
best mean R²: 0.897
best min R²: 0.828
best corr: 0.967
```

## Unified accessibility-flow OOD results

```text
H  mean R²: 0.807 | min R²: 0.675 | corr: 0.904
Mx mean R²: 0.846 | min R²: 0.830 | corr: 0.950
My mean R²: 0.846 | min R²: 0.831 | corr: 0.951
```

## Overall

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| unified_all | 0.897 | 0.828 | 0.967 |
| unified_access_flow | 0.833 | 0.675 | 0.935 |
| adm_geometric_only | 0.344 | -0.002 | 0.423 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| adm_geometric_only | H | 1.000 | 1.000 | 1.000 |
| unified_all | H | 1.000 | 1.000 | 1.000 |
| unified_access_flow | H | 0.807 | 0.675 | 0.904 |
| unified_access_flow | Mx | 0.846 | 0.830 | 0.950 |
| unified_all | Mx | 0.845 | 0.828 | 0.950 |
| adm_geometric_only | Mx | 0.027 | -0.002 | 0.162 |
| unified_access_flow | My | 0.846 | 0.831 | 0.951 |
| unified_all | My | 0.846 | 0.832 | 0.951 |
| adm_geometric_only | My | 0.006 | -0.002 | 0.106 |

## Verdict

```text
adm_like_system_ood_robust
```
