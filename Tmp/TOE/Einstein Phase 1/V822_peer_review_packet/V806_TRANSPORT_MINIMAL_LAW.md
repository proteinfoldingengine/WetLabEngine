# V806 Transport-Current Minimal Law Pruning and Scaling

## Purpose
Test compact observable-transport current laws against ADM momentum residuals.

## Best compact law

```text
surplus_transport
```

## Summary

```text
best mean R²: 0.031
best min R²: 0.011
best mean corr: 0.180
best n features: 3

Mx best R²: 0.048
My best R²: 0.015

V804 baseline overall R²: 0.138
```

## Overall source-set scores

| source set | mean R² | min R² | mean corr |
|---|---:|---:|---:|
| surplus_transport | 0.031 | 0.011 | 0.180 |
| repair_transport | 0.029 | 0.010 | 0.166 |
| minimal_rho_transport | 0.004 | 0.002 | 0.079 |
| phi_transport | -0.001 | -0.015 | 0.057 |
| compact_all | -0.004 | -0.072 | 0.119 |
| all_transport | -0.007 | -0.061 | 0.114 |

## By target

| source set | target | mean R² | min R² | mean corr |
|---|---|---:|---:|---:|
| surplus_transport | Mx | 0.048 | 0.037 | 0.234 |
| repair_transport | Mx | 0.042 | 0.021 | 0.206 |
| phi_transport | Mx | 0.008 | 0.006 | 0.134 |
| minimal_rho_transport | Mx | 0.004 | 0.002 | 0.092 |
| all_transport | Mx | -0.020 | -0.061 | 0.112 |
| compact_all | Mx | -0.023 | -0.072 | 0.103 |
| compact_all | My | 0.015 | 0.008 | 0.135 |
| repair_transport | My | 0.015 | 0.010 | 0.126 |
| surplus_transport | My | 0.015 | 0.011 | 0.127 |
| all_transport | My | 0.006 | -0.005 | 0.117 |
| minimal_rho_transport | My | 0.004 | 0.002 | 0.066 |
| phi_transport | My | -0.010 | -0.015 | -0.019 |

## Interpretation

This checks whether the observed transport improvement survives with a compact law.

## Next

```text
V807 — conservation residual audit for best transport current
```
