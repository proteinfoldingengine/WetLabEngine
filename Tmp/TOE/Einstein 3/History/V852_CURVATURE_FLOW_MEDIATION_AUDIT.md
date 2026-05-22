# V852 Curvature–Flow Mediation Audit

## Purpose

V851 showed momentum features predict H structurally. V852 quantifies coupling asymmetry:

```text
Does flow predict H?
Does access-curvature predict M?
Are both downstream of u = log A?
```

## Summary

```text
H from access R²: 0.886
H from flow R²:   0.771
H from both R²:   0.889

M_parallel from flow R²: 0.873
M_parallel from access R²: 0.008

M_perp from flow R²: 0.873
M_perp from access R²: -0.000

H flow-overlap fraction: 0.871
M_parallel access-overlap fraction: 0.009
M_perp access-overlap fraction: -0.000
```

## Results

| target | model | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| H | H_from_both | 0.889 | 0.859 | 0.944 |
| H | H_from_access | 0.886 | 0.852 | 0.943 |
| H | H_from_flow | 0.771 | 0.587 | 0.885 |
| M_parallel | Mpar_from_flow | 0.873 | 0.825 | 0.938 |
| M_parallel | Mpar_from_access | 0.008 | -0.009 | 0.094 |
| M_perp | Mperp_from_flow | 0.873 | 0.839 | 0.940 |
| M_perp | Mperp_from_access | -0.000 | -0.013 | 0.042 |

## Verdict

```text
shared_u_mediated_coupling_supported
```

## Interpretation

If flow predicts H but access features do not predict M, the coupling is asymmetric:
flow carries downstream information about scalar curvature, but momentum remains role-specific.
