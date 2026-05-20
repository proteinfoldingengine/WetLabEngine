# V836 Irrotational vs Vortical ADM-like Momentum Decomposition

## Purpose

The extended gauge/vorticity video suggested organized momentum flow with possible zero-spin / irrotational structure.

V836 decomposes the ADM-like momentum into:

```text
irrotational / gradient-compatible sector
vortical / curl-compatible sector
```

and tests which carries the ADM-like signal.

## Summary

```text
best feature set: irrot_plus_flow
best mean R²: 0.973
best min R²: 0.957
best corr: 0.987

access-flow R²:        0.856
curl-augmented R²:     0.856
vort+flow R²:          0.856
vortical-only R²:      -0.006

curl gain:             0.000
vortical gain:         0.000
```

## Overall

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| irrot_plus_flow | 0.973 | 0.957 | 0.987 |
| full_decomp | 0.973 | 0.957 | 0.987 |
| M_irrot_only | 0.934 | 0.918 | 0.972 |
| vort_plus_flow | 0.856 | 0.832 | 0.946 |
| curl_augmented | 0.856 | 0.832 | 0.946 |
| access_flow | 0.856 | 0.832 | 0.946 |
| M_vort_only | -0.006 | -0.010 | -0.027 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| irrot_plus_flow | Mx | 0.972 | 0.957 | 0.987 |
| full_decomp | Mx | 0.972 | 0.957 | 0.987 |
| M_irrot_only | Mx | 0.932 | 0.918 | 0.972 |
| vort_plus_flow | Mx | 0.849 | 0.832 | 0.943 |
| access_flow | Mx | 0.849 | 0.832 | 0.943 |
| curl_augmented | Mx | 0.849 | 0.832 | 0.943 |
| M_vort_only | Mx | -0.007 | -0.010 | -0.026 |
| irrot_plus_flow | My | 0.975 | 0.958 | 0.988 |
| full_decomp | My | 0.975 | 0.958 | 0.988 |
| M_irrot_only | My | 0.936 | 0.919 | 0.973 |
| curl_augmented | My | 0.862 | 0.834 | 0.948 |
| vort_plus_flow | My | 0.862 | 0.834 | 0.948 |
| access_flow | My | 0.862 | 0.834 | 0.948 |
| M_vort_only | My | -0.006 | -0.009 | -0.028 |

## Verdict

```text
irrotational_accessibility_flow_dominates
```

## Interpretation

If curl/vortical terms add little, ADM-like momentum is dominantly conservative accessibility-flow compatibility.
If curl/vortical terms add strongly, a topological/vorticity sector is active.
