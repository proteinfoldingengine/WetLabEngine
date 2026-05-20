# V809 Hidden Reservoir Audit

## Purpose
Test whether the failed conservation current is an open-system current with hidden exchange:

```text
Λ_hidden = ∂τρ + ∇·J
```

Then ask whether Λ_hidden is structured.

## Summary

```text
mean holdout R²: 0.010
min holdout R²: 0.002
mean holdout corr: 0.109

Λ RMS: 1.447
Λ mean abs: 0.872

top feature: repair_phi
top feature corr: 0.057
```

## Holdout scores

| holdout | R² | corr |
|---|---:|---:|
| s809_d6_c4 | 0.002 | 0.081 |
| s1010_d6_c4 | 0.020 | 0.147 |
| s1011_d8_c4 | 0.011 | 0.109 |
| s1012_d5_c3 | 0.005 | 0.090 |
| s1013_d9_c5 | 0.012 | 0.118 |

## Top feature correlations

| feature | corr with Λ_hidden |
|---|---:|
| repair_phi | 0.057 |
| gradC_energy | -0.055 |
| C | 0.026 |
| mu | 0.025 |
| defect_phi | 0.023 |
| defect_grad_energy | 0.014 |
| surplus_phi | 0.012 |
| entropy_like | 0.010 |
| repair_grad_energy | -0.009 |
| coherence_like | -0.008 |

## Interpretation

If Λ_hidden is predictable, momentum failure is missing hidden-state exchange rather than random failure.

## Verdict

```text
hidden_reservoir_not_yet_structured
```

## Next

```text
V810 — derive reservoir-corrected transport current if structured, or freeze if weak
```
