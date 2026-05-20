# V837 Momentum Potential Unification

## Purpose

V836 showed ADM-like momentum is overwhelmingly irrotational.

V837 tests whether the full momentum field can be reconstructed from a scalar potential:

```text
Δχ = ∇·M
M_i ≈ ∇ᵢχ
```

and whether accessibility-flow terms approximate that potential structure.

## Summary

```text
best feature set: chi_plus_flow
best mean R²: 0.974
best min R²: 0.961
best corr: 0.988

grad χ only R²:       0.931
access flow R²:       0.836
potential basis R²:   0.835
```

## Overall

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| chi_plus_flow | 0.974 | 0.961 | 0.988 |
| grad_chi_only | 0.931 | 0.919 | 0.972 |
| access_flow | 0.836 | 0.820 | 0.949 |
| potential_basis | 0.835 | 0.820 | 0.949 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| chi_plus_flow | Mx | 0.974 | 0.961 | 0.987 |
| grad_chi_only | Mx | 0.930 | 0.921 | 0.971 |
| access_flow | Mx | 0.836 | 0.825 | 0.950 |
| potential_basis | Mx | 0.835 | 0.828 | 0.949 |
| chi_plus_flow | My | 0.975 | 0.962 | 0.988 |
| grad_chi_only | My | 0.931 | 0.919 | 0.973 |
| access_flow | My | 0.836 | 0.820 | 0.948 |
| potential_basis | My | 0.836 | 0.820 | 0.948 |

## Verdict

```text
single_momentum_potential_supported
```
