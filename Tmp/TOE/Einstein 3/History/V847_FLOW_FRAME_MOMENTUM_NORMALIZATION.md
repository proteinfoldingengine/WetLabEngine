# V847 Flow-Frame Momentum Normalization

## Purpose

V846 showed Mx coefficient instability, suggesting an orientation/gauge-normalization issue.

V847 rotates momentum into the local accessibility-flow frame:

```text
M_parallel = M · J / |J|
M_perp     = M × J / |J|
```

Then tests compact flow-frame predictors.

## Performance

| component | mean R² | min R² | corr |
|---|---:|---:|---:|
| parallel | 0.862 | 0.817 | 0.934 |
| perp | 0.875 | 0.850 | 0.942 |

## Coefficient stability

| component | mean CV | max CV |
|---|---:|---:|
| parallel | 0.125 | 0.213 |
| perp | 0.118 | 0.198 |

## Coefficients

| component | term | mean coef | std coef | abs CV |
|---|---|---:|---:|---:|
| parallel | Jmag | -0.00663 | 0.00141 | 0.213 |
| parallel | dJ_frame | 1.16734 | 0.01248 | 0.011 |
| parallel | div | -0.01876 | 0.00285 | 0.152 |
| perp | Jmag | -0.00879 | 0.00128 | 0.146 |
| perp | dJ_frame | 1.20801 | 0.01397 | 0.012 |
| perp | div | -0.00634 | 0.00125 | 0.198 |

## Summary

```text
parallel R²: 0.862 | CV: 0.125
perp R²:     0.875 | CV: 0.118
```

## Verdict

```text
flow_frame_resolves_orientation_instability
```
