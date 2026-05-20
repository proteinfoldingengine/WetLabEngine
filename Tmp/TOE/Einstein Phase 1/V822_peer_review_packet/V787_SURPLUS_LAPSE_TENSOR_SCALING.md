# V787 Surplus-Lapse Tensor Ansatz Scaling Validation

## Purpose
Freeze the best V785 tensor ansatz:

```text
ds² = -N(C)² dτ² + Ω²(dx²+dy²)
N(C)=exp(0.15 tanh(C/std(C)))
```

and test held-out transfer/scaling.

## Summary

```text
mean heldout R²: 0.480
min heldout R²:  0.445
mean corr:       0.709
min corr:        0.681
```

## Conditions

| condition | nx | nt | defects | complexity | R² | corr |
|---|---:|---:|---:|---:|---:|---:|
| seed910 | 18 | 16 | 6 | 4 | 0.477 | 0.691 |
| seed911 | 18 | 16 | 6 | 4 | 0.544 | 0.747 |
| defects8 | 18 | 16 | 8 | 4 | 0.477 | 0.694 |
| complex5 | 18 | 16 | 7 | 5 | 0.460 | 0.681 |
| grid20 | 20 | 16 | 6 | 4 | 0.445 | 0.704 |
| grid22 | 22 | 16 | 6 | 4 | 0.503 | 0.744 |
| depth18 | 18 | 18 | 6 | 4 | 0.452 | 0.701 |

## Interpretation

The surplus-lapse tensor branch is transferable but still partial.
It improves over raw stress closure, but it is not a full tensor equation closure.

## Next

```text
V788 — component-wise tensor diagnosis
```
