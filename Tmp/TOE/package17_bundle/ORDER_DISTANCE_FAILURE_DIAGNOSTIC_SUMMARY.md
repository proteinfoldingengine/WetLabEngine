# ORDER_DISTANCE_FAILURE_DIAGNOSTIC_SUMMARY.md

# Diagnostic Summary
## Why naive order-distance embedding failed

## Status
**Executed diagnostic. Confirms pivot is needed.**

Diagnostic file:

```text
order_distance_failure_diagnostic.py
```

Execution log:

```text
order_distance_failure_diagnostic_run.log
```

## Captured output

```text
Order-distance failure diagnostic
==================================================
Diagnoses why naive order-distance MDS embedding hard-failed.

comparable_density_median: 0.2148500113606383
D_eff_median: 3.2793851235356826
triangle_violation_rate_median: 0.25
triangle_tested_median: 73.0
local_missingness_median: 0.96875
max_finite_neighbors_median: 147.5
mds_negative_eigen_fraction_median: 0.0
mds_positive_rank_median: 0.0
```

## Interpretation

The failed seam is specific:

\[
d_{\mathrm{ord}}(i,j)=N(i,j)^{1/D_{\mathrm{eff}}}
\Rightarrow
\text{MDS embedding}
\]

is not a valid first reconstruction method.

Causal order produces timelike comparability and interval volumes, not a complete symmetric spatial distance matrix.

The correct pivot is:

```text
CAUSAL_SET_RECONSTRUCTION.md
```

using:
- longest chains,
- antichains,
- interval volumes,
- spatial slice reconstruction,
- causal diamonds.

**End of summary.**
