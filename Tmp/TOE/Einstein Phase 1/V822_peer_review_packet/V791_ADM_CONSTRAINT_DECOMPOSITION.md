# V791 ADM-style Constraint Decomposition

## Purpose

V790 recommended splitting the tensor branch into ADM-like pieces:

```text
Hamiltonian/scalar constraint
Momentum/off-diagonal constraints
```

## Summary

```text
Hamiltonian mean R²: 1.000
Momentum_x mean R²:  0.030
Momentum_y mean R²:  0.084

overall mean R²: 0.371
overall min R²:  0.006
```

## By constraint

| constraint | mean R² | min R² | mean corr |
|---|---:|---:|---:|
| Hamiltonian | 1.000 | 1.000 | 1.000 |
| Momentum_x | 0.030 | 0.006 | 0.189 |
| Momentum_y | 0.084 | 0.066 | 0.292 |

## All scores

| test | constraint | R² | corr | n features |
|---|---|---:|---:|---:|
| seed940 | Hamiltonian | 1.000 | 1.000 | 14 |
| seed940 | Momentum_x | 0.035 | 0.199 | 8 |
| seed940 | Momentum_y | 0.107 | 0.337 | 8 |
| defects8 | Hamiltonian | 1.000 | 1.000 | 14 |
| defects8 | Momentum_x | 0.050 | 0.230 | 8 |
| defects8 | Momentum_y | 0.078 | 0.280 | 8 |
| complex5 | Hamiltonian | 1.000 | 1.000 | 14 |
| complex5 | Momentum_x | 0.006 | 0.140 | 8 |
| complex5 | Momentum_y | 0.066 | 0.261 | 8 |

## Interpretation

This identifies whether the tensor branch fails in the scalar/Hamiltonian part or the momentum/off-diagonal part.

## Next

```text
V792 — focus on momentum constraint closure or revise shift/lapse from ADM constraints
```
