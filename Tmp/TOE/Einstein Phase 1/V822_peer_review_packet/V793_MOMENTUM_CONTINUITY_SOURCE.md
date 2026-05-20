# V793 Momentum Source from Recoverability Continuity

## Purpose
V792 showed shift terms do not fix momentum constraints. V793 derives momentum-source candidates from recoverability continuity/flux terms.

## Summary

```text
best source set: mixed_flux
best target: Mx
best mean R²: 0.001
best min R²: -0.001

Mx best R²: 0.001
My best R²: -0.000
```

## Scores

| source set | target | mean R² | min R² | mean corr | n features |
|---|---|---:|---:|---:|---:|
| mixed_flux | Mx | 0.001 | -0.001 | 0.038 | 3 |
| continuity_resid | Mx | -0.004 | -0.015 | 0.060 | 5 |
| grad_dt | Mx | -0.006 | -0.013 | 0.012 | 10 |
| div_flux_only | Mx | -0.017 | -0.028 | -0.031 | 5 |
| all_continuity | Mx | -0.088 | -0.175 | 0.131 | 28 |
| flux_only | Mx | -0.181 | -0.346 | 0.176 | 10 |
| mixed_flux | My | -0.000 | -0.002 | 0.004 | 3 |
| grad_dt | My | -0.008 | -0.016 | 0.026 | 10 |
| continuity_resid | My | -0.012 | -0.021 | -0.006 | 5 |
| div_flux_only | My | -0.018 | -0.033 | -0.011 | 5 |
| all_continuity | My | -0.100 | -0.366 | 0.194 | 28 |
| flux_only | My | -0.248 | -0.636 | 0.255 | 10 |

## Interpretation

This tests whether momentum constraints are driven by recoverability flux/continuity rather than static stress.

## Next

```text
V794 — freeze momentum failure or derive shift by solving momentum constraints
```
