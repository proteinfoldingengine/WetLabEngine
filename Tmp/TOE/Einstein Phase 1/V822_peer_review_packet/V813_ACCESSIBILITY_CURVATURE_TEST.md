# V813 Explicit Accessibility Field Curvature Test

## Purpose
Test the V812 law:

```text
G_proxy = 2α Δ log(A + ε)
```

where A is explicit reachable-state accessibility.

## Summary

```text
best candidate: A_exp_density
mean heldout R²: 0.879
min heldout R²: 0.860
mean corr: 0.938
mean α: 0.127
```

## Candidate scores

| candidate | mean R² | min R² | mean corr | mean α |
|---|---:|---:|---:|---:|
| A_exp_density | 0.879 | 0.860 | 0.938 | 0.127 |
| A_sigmoid_density | 0.794 | 0.735 | 0.893 | 0.183 |
| A_defect_repair | 0.782 | 0.766 | 0.885 | 0.149 |
| A_phi_capacity | 0.384 | 0.375 | 0.620 | 0.243 |

## Interpretation

This tests whether curvature is better understood as accessibility-density curvature rather than local momentum transport.

## Verdict

```text
accessibility_curvature_law_supported
```

## Next

```text
V814 — refine accessibility field or freeze accessibility law status
```
