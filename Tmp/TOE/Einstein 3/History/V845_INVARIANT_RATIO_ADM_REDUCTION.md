# V845 Invariant-Ratio ADM-like Reduction

## Purpose

V844 improved performance but coefficients remained unstable.

V845 tests invariant-ratio features to remove remaining scale/orientation dependence.

## Performance

| constraint | mean R² | min R² | corr |
|---|---:|---:|---:|
| H | 0.296 | -0.594 | 0.613 |
| Mx | 0.481 | 0.231 | 0.708 |
| My | 0.483 | 0.404 | 0.700 |

## Coefficient stability

| constraint | mean CV | max CV |
|---|---:|---:|
| H | 0.520 | 1.038 |
| Mx | 0.269 | 0.712 |
| My | 0.298 | 0.719 |

## Coefficients

| constraint | term | mean coef | std coef | abs CV |
|---|---|---:|---:|---:|
| H | QH1 | 0.00051 | 0.00053 | 1.038 |
| H | QH2 | -1.00107 | 0.01899 | 0.019 |
| H | QH3 | -5.90324 | 2.96924 | 0.503 |
| Mx | QJ | -0.00379 | 0.00270 | 0.712 |
| Mx | QdJ | 0.56908 | 0.01886 | 0.033 |
| Mx | Qdiv | -0.01502 | 0.00094 | 0.063 |
| My | QJ | 0.00312 | 0.00224 | 0.719 |
| My | QdJ | 0.55518 | 0.00906 | 0.016 |
| My | Qdiv | -0.00609 | 0.00097 | 0.159 |

## Verdict

```text
invariant_ratio_reduction_partial
```
