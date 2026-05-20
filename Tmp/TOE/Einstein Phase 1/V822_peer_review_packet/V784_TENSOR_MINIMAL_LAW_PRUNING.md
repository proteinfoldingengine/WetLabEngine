# V784 Tensor Stress Minimal-Law Pruning

## Purpose
Find a minimal tensor stress library that predicts the nonzero 2+1 Einstein tensor and validate on held-out geometries.

## Minimal terms

```text
gV_defect, gV_repair, g_C2, g_lapC, g_lapRepair
```

## Summary

```text
train R²: 0.310
mean heldout R²: 0.328
min heldout R²: 0.313
mean heldout corr: 0.634
```

## Heldout scores

| test | R² | corr |
|---|---:|---:|
| seed900 | 0.313 | 0.600 |
| defects8 | 0.354 | 0.667 |
| complex5 | 0.317 | 0.636 |

## Pruning history

| step | n terms | removed | mean heldout R² |
|---:|---:|---|---:|
| 0 | 10 |  | 0.331 |
| 1 | 9 | T_C | 0.331 |
| 2 | 8 | T_repair | 0.331 |
| 3 | 7 | T_phi | 0.331 |
| 4 | 6 | T_log_mu | 0.330 |
| 5 | 5 | gV_surplus | 0.328 |

## Interpretation

This tests whether the tensor branch has a transferable source law, not just an in-sample fit.

## Next

```text
V785 — revise 2+1 metric ansatz or derive missing tensor terms
```
