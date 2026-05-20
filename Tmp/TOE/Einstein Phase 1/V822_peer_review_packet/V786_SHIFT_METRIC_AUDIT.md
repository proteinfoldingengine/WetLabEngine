# V786 Non-Diagonal Shift / Cross-Term Metric Audit

## Purpose
V785 showed source-coupled lapse improves tensor closure. V786 tests whether recoverability-flow shift/cross terms improve it further.

## Best result

```text
best shift mode: no_shift
best feature set: lap_flow
mean heldout R²: 0.396
min heldout R²: 0.331
mean corr: 0.669
```

## Scores

| shift mode | feature set | mean R² | min R² | mean corr | n features |
|---|---|---:|---:|---:|---:|
| no_shift | lap_flow | 0.396 | 0.331 | 0.669 | 6 |
| mixed_shift | lap_flow | 0.378 | 0.314 | 0.650 | 6 |
| surplus_shift | lap_flow | 0.369 | 0.308 | 0.642 | 6 |
| repair_shift | lap_flow | 0.368 | 0.305 | 0.641 | 6 |
| repair_shift | all | 0.143 | -0.025 | 0.646 | 12 |
| repair_shift | prior_all | 0.141 | -0.034 | 0.645 | 8 |
| surplus_shift | all | 0.135 | -0.033 | 0.645 | 12 |
| mixed_shift | all | 0.134 | -0.039 | 0.648 | 12 |
| mixed_shift | prior_all | 0.132 | -0.047 | 0.647 | 8 |
| surplus_shift | prior_all | 0.132 | -0.041 | 0.644 | 8 |
| no_shift | prior_all | 0.127 | -0.053 | 0.658 | 8 |
| no_shift | all | 0.125 | -0.050 | 0.658 | 12 |
| repair_shift | flow_only | 0.007 | -0.003 | 0.088 | 4 |
| surplus_shift | flow_only | 0.006 | -0.002 | 0.086 | 4 |
| mixed_shift | flow_only | 0.005 | -0.004 | 0.076 | 4 |
| no_shift | flow_only | -0.001 | -0.003 | -0.018 | 4 |

## Interpretation
Non-diagonal terms test whether recoverability flow belongs in the metric, not just the stress source.

## Next

```text
V787 — freeze best tensor metric ansatz and run scaling validation
```
