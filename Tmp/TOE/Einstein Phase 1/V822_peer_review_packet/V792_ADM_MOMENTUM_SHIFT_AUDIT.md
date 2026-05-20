# V792 ADM Momentum Constraint Shift Audit

## Purpose
V791 showed Hamiltonian closure is strong but momentum constraints fail. V792 tests whether recoverability-flow shift terms repair momentum closure.

## Summary

```text
best shift mode: repair_flow
best momentum mean R²: 0.043
best momentum min R²: 0.025
best momentum corr: 0.213

no-shift momentum mean R²: -0.003
```

## Momentum shift comparison

| shift mode | momentum mean R² | momentum min R² | momentum corr |
|---|---:|---:|---:|
| repair_flow | 0.043 | 0.025 | 0.213 |
| mixed_flow | 0.041 | 0.025 | 0.209 |
| C_flow | 0.039 | 0.025 | 0.204 |
| none | -0.003 | -0.020 | 0.040 |

## Interpretation

This tests whether the failed off-diagonal/momentum branch is caused by missing shift geometry.

## Next

```text
V793 — freeze ADM result or derive momentum source from continuity equation
```
