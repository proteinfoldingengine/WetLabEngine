# V848 Flow-Frame Compact ADM-like Law Candidate

## Purpose

V847 resolved momentum orientation instability by using the local accessibility-flow frame.

V848 combines:

```text
H ~ ac_n + A_n + K_n + K2_n
M_parallel ~ |J| + dJ_parallel + divJ
M_perp ~ |J| + dJ_perp + divJ
```

into one compact flow-frame ADM-like law candidate.

## Performance

| constraint | mean R² | min R² | corr |
|---|---:|---:|---:|
| H | 0.893 | 0.877 | 0.946 |
| M_parallel | 0.874 | 0.829 | 0.939 |
| M_perp | 0.875 | 0.836 | 0.943 |

## Coefficient stability

| constraint | mean CV | max CV |
|---|---:|---:|
| H | 0.070 | 0.228 |
| M_parallel | 0.089 | 0.147 |
| M_perp | 0.147 | 0.265 |

## Coefficients

| constraint | term | mean coef | std coef | abs CV |
|---|---|---:|---:|---:|
| H | A_n | -0.22955 | 0.00576 | 0.025 |
| H | K2_n | 0.01907 | 0.00030 | 0.016 |
| H | K_n | -0.00269 | 0.00061 | 0.228 |
| H | ac_n | 0.68327 | 0.00697 | 0.010 |
| M_parallel | Jmag | -0.00911 | 0.00101 | 0.110 |
| M_parallel | dJ_frame | 1.19171 | 0.01225 | 0.010 |
| M_parallel | div_n | -0.01914 | 0.00282 | 0.147 |
| M_perp | Jmag | -0.00571 | 0.00151 | 0.265 |
| M_perp | dJ_frame | 1.22006 | 0.01674 | 0.014 |
| M_perp | div_n | -0.01661 | 0.00268 | 0.161 |

## Summary

```text
H R²:          0.893 | CV: 0.070
M_parallel R²:0.874 | CV: 0.089
M_perp R²:    0.875 | CV: 0.147
```

## Verdict

```text
flow_frame_compact_adm_law_candidate_supported
```
