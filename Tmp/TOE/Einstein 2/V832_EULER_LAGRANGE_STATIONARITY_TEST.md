# V832 Euler-Lagrange Residual Stationarity Test

## Purpose

V831 proposed a variational derivation for the unified accessibility-flow ADM-like system.

V832 tests whether Euler-Lagrange residuals align with the observed ADM-like constraint closure.

## Tested residuals

```text
R_phi = Δφ + αΔu
u = log(A + ε)
J_i = -∇ᵢu
```

Flow residual:

```text
R_J = ∂τ²J_i - fitted[∇ᵢ(∇·J), J_i]
```

## Summary

```text
mean EL total RMS: 0.5082
mean R_phi RMS:    0.0472
mean R_J RMS:      0.5060

mean constraint R²: 0.861
min constraint R²:  0.790

corr(-EL, closure):        -0.376
corr(-R_phi, H):           -0.108
corr(-R_J, momentum avg):  -0.598
```

## Case results

| case | EL RMS | mean constraint R² | H R² | Mx R² | My R² |
|---|---:|---:|---:|---:|---:|
| standard_s832_d6_c4 | 0.4856 | 0.790 | 0.732 | 0.835 | 0.805 |
| standard_s1350_d6_c4 | 0.4942 | 0.835 | 0.824 | 0.840 | 0.842 |
| standard_s1351_d8_c4 | 0.5191 | 0.870 | 0.835 | 0.888 | 0.888 |
| standard_s1352_d5_c3 | 0.4731 | 0.849 | 0.835 | 0.866 | 0.847 |
| radial_s1400_d6_c4 | 0.5041 | 0.940 | 0.903 | 0.956 | 0.961 |
| shear_s1401_d8_c5 | 0.5703 | 0.939 | 0.869 | 0.976 | 0.973 |
| counterrot_s1402_d8_c5 | 0.4640 | 0.848 | 0.875 | 0.833 | 0.837 |
| noisy_s1403_d7_c4 | 0.5553 | 0.815 | 0.733 | 0.856 | 0.856 |

## Verdict

```text
variational_stationarity_partial
```

## Interpretation

This is the first numerical stationarity test of the V831 variational action.
