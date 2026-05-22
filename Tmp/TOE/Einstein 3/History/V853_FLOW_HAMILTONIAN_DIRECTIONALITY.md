# V853 Flow–Hamiltonian Directionality Audit

## Purpose

V852 showed shared u-mediated coupling: flow predicts H, but access curvature does not predict momentum.

V853 tests directionality across ordered-update lag.

```text
lag > 0: past flow predicts current H
lag = 0: simultaneous flow predicts H
lag < 0: future flow predicts current H
```

## Summary

```text
best flow lag: 0
best flow lag R²: 0.758

lag 0 flow R²: 0.758
past lag +1 flow R²: 0.231
future lag -1 flow R²: 0.226
```

## Results

| lag | model | mean R² | min R² | corr |
|---:|---|---:|---:|---:|
| -2 | access_current | 0.886 | 0.828 | 0.943 |
| -1 | access_current | 0.886 | 0.828 | 0.943 |
| 0 | access_current | 0.886 | 0.828 | 0.943 |
| 1 | access_current | 0.886 | 0.828 | 0.943 |
| 2 | access_current | 0.886 | 0.828 | 0.943 |
| -2 | access_plus_flow_lag | 0.892 | 0.836 | 0.946 |
| -1 | access_plus_flow_lag | 0.889 | 0.834 | 0.945 |
| 0 | access_plus_flow_lag | 0.893 | 0.839 | 0.947 |
| 1 | access_plus_flow_lag | 0.891 | 0.841 | 0.946 |
| 2 | access_plus_flow_lag | 0.891 | 0.835 | 0.946 |
| -2 | flow_lag | 0.006 | -0.078 | 0.135 |
| -1 | flow_lag | 0.226 | 0.141 | 0.483 |
| 0 | flow_lag | 0.758 | 0.618 | 0.878 |
| 1 | flow_lag | 0.231 | 0.118 | 0.489 |
| 2 | flow_lag | 0.014 | -0.104 | 0.176 |

## Verdict

```text
simultaneous_or_past_flow_coupling
```
