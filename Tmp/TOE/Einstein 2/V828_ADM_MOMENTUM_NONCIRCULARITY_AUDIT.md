# V828 ADM Momentum Non-Circularity Audit

## Purpose
Audit whether the V827 ADM-momentum-like signal is genuine accessibility-flow structure or circular leakage from the curvature proxy.

## Summary

```text
flow only R²:              0.844
G only R²:                 0.015
flow + G R²:               0.844

G shuffled only R²:        -0.000
flow + shuffled G R²:      0.844
unrelated Laplacian R²:    -0.000

increment over G only:     0.829
increment over flow only:  0.000
```

## Feature summary

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| flow_plus_G | 0.844 | 0.829 | 0.920 |
| flow_plus_shuffledG | 0.844 | 0.828 | 0.920 |
| flow_only | 0.844 | 0.828 | 0.920 |
| G_only | 0.015 | -0.001 | 0.122 |
| G_shuffled_only | -0.000 | -0.003 | 0.004 |
| unrelated_lap | -0.000 | -0.001 | -0.009 |

## By target

| feature set | target | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| flow_plus_G | Mx | 0.843 | 0.829 | 0.919 |
| flow_plus_shuffledG | Mx | 0.842 | 0.828 | 0.919 |
| flow_only | Mx | 0.842 | 0.828 | 0.919 |
| G_only | Mx | 0.023 | 0.012 | 0.155 |
| unrelated_lap | Mx | -0.000 | -0.001 | -0.008 |
| G_shuffled_only | Mx | -0.001 | -0.003 | -0.013 |
| flow_only | My | 0.845 | 0.835 | 0.921 |
| flow_plus_shuffledG | My | 0.845 | 0.835 | 0.921 |
| flow_plus_G | My | 0.845 | 0.834 | 0.921 |
| G_only | My | 0.007 | -0.001 | 0.089 |
| G_shuffled_only | My | 0.000 | -0.000 | 0.020 |
| unrelated_lap | My | -0.000 | -0.001 | -0.010 |

## Verdict

```text
noncircular_adm_like_signal_supported
```

## Interpretation

A clean ADM-like momentum result requires shuffled/unrelated controls to fail and flow+G to beat G-only.
