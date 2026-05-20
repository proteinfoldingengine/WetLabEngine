# V807 Transport Current Conservation Residual Audit

## Purpose
V804 showed observable transport improves ADM momentum. V806 showed compact current laws are weak.

V807 asks whether the candidate currents obey a conservation/balance law:

```text
∂τ ρ + ∂x Jx + ∂y Jy = source - sink
```

## Summary

```text
best candidate: phi_weighted_rho_transport
mean balance R²: 0.010
min balance R²: 0.001
mean balance corr: 0.086
mean continuity RMS: 1.3838
```

## Candidate balance scores

| candidate | continuity RMS | balance R² | min R² | corr |
|---|---:|---:|---:|---:|
| phi_weighted_rho_transport | 1.3838 | 0.010 | 0.001 | 0.086 |
| rho_transport | 1.4487 | 0.008 | 0.002 | 0.082 |
| full_mixed_transport | 1.9821 | 0.007 | 0.003 | 0.079 |
| surplus_transport | 0.4799 | 0.005 | 0.001 | 0.065 |
| repair_transport | 1.0571 | 0.004 | 0.001 | 0.058 |

## Interpretation

If the current has a strong balance law, it can become a real momentum primitive.
If not, the transport current is predictive but not yet conserved.

## Verdict

```text
transport_current_conservation_weak
```

## Next

```text
V808 — derive corrected conserved current if balance is weak,
or retest momentum with conserved current if strong.
```
