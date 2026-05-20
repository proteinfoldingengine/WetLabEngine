# V795 Shift Vector Solve from ADM Momentum Constraints

## Purpose
Instead of guessing shift β_i, solve it from the ADM momentum residual.

## Method
Approximate local momentum residual as a Poisson-like shift equation:

```text
Δβ_i ≈ M_i
```

and solve per ordered-update slice by Fourier inversion.

## Summary

```text
mean momentum reduction: -0.021
min momentum reduction:  -0.026

mean before norm: 0.201748
mean after norm:  0.205912

mean beta_x rms: 0.123447
mean beta_y rms: 0.134050
```

## Cases

| seed | defects | complexity | before norm | after norm | reduction | beta_x rms | beta_y rms |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 795 | 6 | 4 | 0.187758 | 0.191909 | -0.022 | 0.101700 | 0.100035 |
| 960 | 6 | 4 | 0.188443 | 0.193261 | -0.026 | 0.137987 | 0.147335 |
| 961 | 8 | 4 | 0.211030 | 0.216394 | -0.025 | 0.138026 | 0.139145 |
| 962 | 7 | 5 | 0.206628 | 0.210849 | -0.020 | 0.114984 | 0.143600 |
| 963 | 9 | 5 | 0.214883 | 0.217145 | -0.011 | 0.124537 | 0.140134 |

## Interpretation

This tests whether momentum failure is a shift-solving problem.

## Next

```text
V796 — validate solved shift in full tensor G_ab closure
```
