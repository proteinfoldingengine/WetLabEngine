# V860 Scaling Barrier Diagnostic

## Purpose

V859 showed residual improves with resolution but does not extrapolate near zero.

V860 separates three possible causes:

```text
A. fixed_nx32: frozen high-resolution coefficients
B. per_resolution_refit: best achievable fit at each resolution
C. leave_resolution_out: transfer across resolution
```

## Summary

| audit | mean compat | nx=12 RMS | nx=32 RMS | improvement | no-offset p |
|---|---:|---:|---:|---:|---:|
| fixed_nx32 | 0.9724 | 1.0994 | 0.9300 | 0.1693 | 0.183 |
| per_resolution_refit | 0.9674 | 1.0756 | 0.9300 | 0.1456 | 0.165 |
| leave_resolution_out | 0.9717 | 1.0961 | 0.9308 | 0.1653 | 0.180 |

## Compatibility by resolution

| audit | nx | dx | compatibility RMS |
|---|---:|---:|---:|
| fixed_nx32 | 12 | 1.45455 | 1.0994 |
| fixed_nx32 | 16 | 1.06667 | 1.0177 |
| fixed_nx32 | 20 | 0.84211 | 0.9645 |
| fixed_nx32 | 24 | 0.69565 | 0.9238 |
| fixed_nx32 | 28 | 0.59259 | 0.8989 |
| fixed_nx32 | 32 | 0.51613 | 0.9300 |
| leave_resolution_out | 12 | 1.45455 | 1.0961 |
| leave_resolution_out | 16 | 1.06667 | 1.0165 |
| leave_resolution_out | 20 | 0.84211 | 0.9637 |
| leave_resolution_out | 24 | 0.69565 | 0.9237 |
| leave_resolution_out | 28 | 0.59259 | 0.8992 |
| leave_resolution_out | 32 | 0.51613 | 0.9308 |
| per_resolution_refit | 12 | 1.45455 | 1.0756 |
| per_resolution_refit | 16 | 1.06667 | 1.0139 |
| per_resolution_refit | 20 | 0.84211 | 0.9630 |
| per_resolution_refit | 24 | 0.69565 | 0.9232 |
| per_resolution_refit | 28 | 0.59259 | 0.8985 |
| per_resolution_refit | 32 | 0.51613 | 0.9300 |

## Diagnostic gap

```text
fixed nx=32 RMS - per-resolution refit nx=32 RMS = 0.0000
```

## Verdict

```text
operator_discretization_barrier
```

## Interpretation

If per-resolution refit is far lower than fixed coefficients, the current barrier is not the ADM-like law form itself.
It is coefficient/normalization transfer across resolutions.
