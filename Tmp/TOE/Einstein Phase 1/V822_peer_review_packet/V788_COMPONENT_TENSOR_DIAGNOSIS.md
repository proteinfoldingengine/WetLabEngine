# V788 Component-wise Tensor Closure Diagnosis

## Purpose
V787 showed partial transferable tensor closure. V788 breaks closure down by Einstein tensor component.

## Summary

```text
best component: 11  mean R²=0.645
worst component: 12 mean R²=-0.000

overall component mean R²: 0.249
overall min R²: -0.000
```

## Component closure

| component | mean R² | min R² | mean corr |
|---|---:|---:|---:|
| 11 | 0.645 | 0.595 | 0.829 |
| 22 | 0.638 | 0.585 | 0.827 |
| 00 | 0.214 | 0.164 | 0.471 |
| 02 | -0.000 | -0.000 | nan |
| 01 | -0.000 | -0.000 | nan |
| 12 | -0.000 | -0.000 | nan |

## Interpretation

This tells us whether the tensor branch is failing uniformly or in specific components.

## Next

```text
V789 — focus missing tensor terms on weakest components
```
