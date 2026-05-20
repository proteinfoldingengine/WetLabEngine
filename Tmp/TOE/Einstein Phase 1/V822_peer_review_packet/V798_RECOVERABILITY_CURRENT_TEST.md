# V798 Recoverability Current Test Against ADM Momentum Residuals

## Purpose
Implement the V797 current candidate:

```text
J_i = A C v_i - B ∂_i C + D repair ∂_i φ - E φ ∂_i μ
```

and test whether it predicts ADM momentum residuals.

## Summary

```text
best source set: current_plus_lap
best target: Mx
best mean R²: 0.042
best min R²: 0.018
best corr: 0.207

Mx best R²: 0.042
My best R²: 0.026
```

## Scores

| source set | target | mean R² | min R² | mean corr |
|---|---|---:|---:|---:|
| current_plus_lap | Mx | 0.042 | 0.018 | 0.207 |
| all_current | Mx | 0.041 | 0.013 | 0.207 |
| V797_current_core | Mx | 0.019 | 0.001 | 0.144 |
| velocity_current | Mx | 0.011 | 0.005 | 0.104 |
| density_current | Mx | 0.007 | -0.006 | 0.082 |
| current_plus_lap | My | 0.026 | -0.004 | 0.175 |
| all_current | My | 0.024 | -0.013 | 0.182 |
| V797_current_core | My | 0.009 | -0.022 | 0.129 |
| velocity_current | My | 0.008 | 0.003 | 0.092 |
| density_current | My | 0.004 | -0.003 | 0.066 |

## Interpretation

This tests whether the missing ADM momentum source is a recoverability current.

## Next

```text
V799 — freeze current-law result and decide tensor branch path
```
