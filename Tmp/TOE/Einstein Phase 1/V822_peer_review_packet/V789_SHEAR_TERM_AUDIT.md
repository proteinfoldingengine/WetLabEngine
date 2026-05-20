# V789 Weak Component Shear-Term Audit

## Purpose
V788 showed off-diagonal/shear components are weakest, especially G_12. V789 adds shear-flow source terms.

## Summary

```text
overall best feature set: base_plus_shear
overall best mean R²: 0.258

G_12 best set: shear_only
G_12 best mean R²: 0.044

G_01 best mean R²: -0.000
G_02 best mean R²: -0.000
```

## Scores

| feature set | component | mean R² | min R² | mean corr | n features |
|---|---|---:|---:|---:|---:|
| base_plus_shear | 00 | 0.274 | 0.246 | 0.531 | 20 |
| base | 00 | 0.242 | 0.213 | 0.500 | 8 |
| shear_only | 00 | 0.021 | 0.008 | 0.157 | 12 |
| targeted_shear | 00 | 0.014 | 0.004 | 0.130 | 10 |
| base | 01 | -0.000 | -0.000 | nan | 8 |
| targeted_shear | 01 | -0.012 | -0.032 | 0.045 | 10 |
| shear_only | 01 | -0.013 | -0.032 | 0.045 | 12 |
| base_plus_shear | 01 | -0.013 | -0.032 | 0.045 | 20 |
| base | 02 | -0.000 | -0.000 | nan | 8 |
| shear_only | 02 | -0.004 | -0.030 | 0.089 | 12 |
| base_plus_shear | 02 | -0.004 | -0.030 | 0.089 | 20 |
| targeted_shear | 02 | -0.005 | -0.037 | 0.088 | 10 |
| base | 11 | 0.631 | 0.569 | 0.806 | 8 |
| base_plus_shear | 11 | 0.627 | 0.563 | 0.806 | 20 |
| targeted_shear | 11 | -0.006 | -0.015 | 0.027 | 10 |
| shear_only | 11 | -0.011 | -0.018 | 0.025 | 12 |
| shear_only | 12 | 0.044 | 0.041 | 0.212 | 12 |
| base_plus_shear | 12 | 0.044 | 0.041 | 0.212 | 20 |
| targeted_shear | 12 | 0.044 | 0.041 | 0.210 | 10 |
| base | 12 | -0.000 | -0.000 | nan | 8 |
| base | 22 | 0.626 | 0.564 | 0.805 | 8 |
| base_plus_shear | 22 | 0.622 | 0.558 | 0.804 | 20 |
| targeted_shear | 22 | -0.005 | -0.013 | 0.028 | 10 |
| shear_only | 22 | -0.010 | -0.017 | 0.025 | 12 |

## Interpretation

This tests whether weak tensor closure is caused by missing shear/flow terms.

## Next

```text
V790 — decide tensor branch status and next route
```
