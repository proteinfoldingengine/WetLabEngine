# V844 Dimensionless Compact ADM-like Coefficient Audit

## Purpose

V843 showed compact ADM-like coefficients transfer, but coefficient stability was not frozen.

V844 applies per-case dimensionless normalization before coefficient fitting.

## Performance

| constraint | mean R² | min R² | corr |
|---|---:|---:|---:|
| H | 0.886 | 0.865 | 0.942 |
| Mx | 0.869 | 0.837 | 0.938 |
| My | 0.870 | 0.832 | 0.938 |

## Coefficient stability

| constraint | mean CV | max CV |
|---|---:|---:|
| H | 0.431 | 1.671 |
| Mx | 0.689 | 1.970 |
| My | 0.504 | 1.455 |

## Coefficients

| constraint | term | mean coef | std coef | abs CV |
|---|---|---:|---:|---:|
| H | A | -0.20977 | 0.00354 | 0.017 |
| H | K | 0.00048 | 0.00080 | 1.671 |
| H | K2 | 0.01903 | 0.00043 | 0.023 |
| H | access_curv | 0.67567 | 0.00893 | 0.013 |
| Mx | J | 0.00137 | 0.00270 | 1.970 |
| Mx | dJ | 1.20937 | 0.01319 | 0.011 |
| Mx | divJ | 0.05628 | 0.00485 | 0.086 |
| My | J | -0.00162 | 0.00236 | 1.455 |
| My | dJ | 1.18522 | 0.01336 | 0.011 |
| My | divJ | 0.05391 | 0.00243 | 0.045 |

## Summary

```text
H  mean R²: 0.886 | mean CV: 0.431
Mx mean R²: 0.869 | mean CV: 0.689
My mean R²: 0.870 | mean CV: 0.504
```

## Verdict

```text
dimensionless_coefficients_still_unstable
```
