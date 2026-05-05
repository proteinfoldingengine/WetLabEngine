# ANTICHAIN_SPATIAL_GEOMETRY_VERIFIER_SUMMARY.md

# Verifier Summary
## Spatial adjacency from causal antichains

## Status
**Executed structural verifier. Not a spatial metric proof.**

Verifier file:

```text
antichain_spatial_geometry_verifier.py
```

Execution log:

```text
antichain_spatial_geometry_verifier_run.log
```

## Captured output

```text
Antichain spatial geometry verifier
==================================================
Route:
causal order -> rank antichains -> causal-profile adjacency -> spatial graph diagnostics
Coordinates are used only for hidden spatial-neighbor evaluation.

PASS: 92.0
SOFT_FAIL: 0.0
HARD_FAIL: 8.0
n_slices_median: 9.0
median_slice_size_median: 38.25
antichain_violation_rate_median: 0.0
neighbor_precision_median: 0.6858272508869291
neighbor_recall_proxy_median: 0.7379981884057971
graph_connectivity_fraction_median: 1.0
laplacian_rank_median_median: 37.25
```

## Interpretation

The verifier tests whether rank antichains support spatial adjacency using causal-profile similarity.

It evaluates:
- antichain validity,
- spatial-neighbor precision/recall proxy,
- graph connectivity,
- graph Laplacian rank.

This supports a spatial-slice route but does not yet construct the spatial metric \(h_{ab}\).

**End of summary.**
