# RENORMALIZED_HEAT_KERNEL_REFINEMENT_VERIFIER_SUMMARY.md

# Verifier Summary
## Refinement test for flat-baseline-renormalized heat coefficient

## Status
**Executed refinement diagnostic. Not curvature proof.**

Verifier file:

```text
renormalized_heat_kernel_refinement_verifier.py
```

Execution log:

```text
renormalized_heat_kernel_refinement_verifier_run.log
```

## Captured output

```text
Renormalized heat-kernel refinement verifier
==================================================
Route:
flat baseline residual heat coefficient under graph refinement

n,h_median,flat_baseline_raw,sphere_raw_median,sphere_residual_median,sphere_residual_std,flat_window_cv,sphere_window_cv,residual_separation_z
80,0.7121622677181286,-323.72341535323994,-312.1004047839276,11.623010569312328,14.632922853122595,0.5151319261290269,0.5213103360558391,0.49695671782283946
120,0.5663357491133442,-482.29696582330666,-471.5576651099101,10.739300713396574,6.792106374263096,0.5139450295570345,0.5202784418254799,0.596975933640105
180,0.4729654014630186,-737.9863546880198,-722.884642613823,15.101712074196826,9.631569367313526,0.510164708352247,0.5194094990315961,0.8306702101058555
positive_residual_all_refinements: True
separation_ratio_last_vs_first: 1.6715141989494353
classification: RENORMALIZED_REFINEMENT_PROMISING
```

## Interpretation

The verifier checks whether the positive sphere residual after flat-baseline subtraction persists under graph refinement.

**End of summary.**
