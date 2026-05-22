# V841 ADM Role-Separation Audit

## Purpose

V840 showed χ is a slice-deformation / extrinsic geometry object.

V841 tests whether the ADM-like branches separate into their expected roles:

```text
Hamiltonian-like H  -> accessibility curvature
Momentum-like M_i   -> accessibility flow / extrinsic slice deformation
```

## Summary

```text
H from accessibility R²: 0.849
H from extrinsic R²:     0.702

Mx from flow R²:         0.865
My from flow R²:         0.863

Mx extrinsic+flow R²:    0.863
My extrinsic+flow R²:    0.862

best overall feature set: unified_all
best overall R²: 0.892
best min R²: 0.845
best corr: 0.962
```

## Overall

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| unified_all | 0.892 | 0.845 | 0.962 |
| extrinsic_plus_flow | 0.869 | 0.845 | 0.951 |
| access_plus_flow | 0.860 | 0.779 | 0.947 |
| flow_only | 0.846 | 0.706 | 0.940 |
| accessibility_only | 0.303 | 0.000 | 0.426 |
| extrinsic_only | 0.246 | -0.005 | 0.369 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| unified_all | H | 0.952 | 0.944 | 0.976 |
| extrinsic_plus_flow | H | 0.882 | 0.871 | 0.940 |
| access_plus_flow | H | 0.857 | 0.779 | 0.932 |
| accessibility_only | H | 0.849 | 0.779 | 0.926 |
| flow_only | H | 0.811 | 0.706 | 0.907 |
| extrinsic_only | H | 0.702 | 0.698 | 0.844 |
| flow_only | Mx | 0.865 | 0.861 | 0.957 |
| extrinsic_plus_flow | Mx | 0.863 | 0.856 | 0.956 |
| unified_all | Mx | 0.862 | 0.853 | 0.956 |
| access_plus_flow | Mx | 0.862 | 0.854 | 0.956 |
| accessibility_only | Mx | 0.043 | 0.000 | 0.210 |
| extrinsic_only | Mx | 0.020 | -0.005 | 0.138 |
| flow_only | My | 0.863 | 0.845 | 0.955 |
| extrinsic_plus_flow | My | 0.862 | 0.845 | 0.955 |
| access_plus_flow | My | 0.861 | 0.844 | 0.955 |
| unified_all | My | 0.861 | 0.845 | 0.955 |
| accessibility_only | My | 0.018 | 0.011 | 0.142 |
| extrinsic_only | My | 0.016 | 0.002 | 0.125 |

## Verdict

```text
adm_role_separation_supported
```

## Interpretation

This tests whether the model has a true ADM-like role split rather than one generic predictor doing everything.
