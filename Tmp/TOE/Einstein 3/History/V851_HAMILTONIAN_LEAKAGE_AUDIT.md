# V851 Hamiltonian Leakage Audit

## Purpose

V850 showed H can be partly predicted by momentum features.

V851 tests whether this is genuine structural correlation or simple role leakage.

## Results

| model | mean R² | min R² | corr |
|---|---:|---:|---:|
| H_correct_plus_momentum | 0.891 | 0.877 | 0.945 |
| H_correct | 0.885 | 0.861 | 0.942 |
| H_momentum_proxy | 0.817 | 0.794 | 0.908 |
| H_momentum_shuffled | -0.014 | -0.023 | -0.605 |

## Verdict

```text
H_momentum_leakage_is_structural_correlation
```

## Interpretation

If shuffled momentum features fail while real momentum features predict H, the leakage is structural correlation:
accessibility flow is coupled to scalar curvature, but it is still not the primary compact H law.
