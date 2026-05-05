# CAUSAL_SET_RECONSTRUCTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Causal-set-style reconstruction after failed MDS route

## Status
**Executed structural verifier. Not a metric proof.**

Verifier file:

```text
causal_set_reconstruction_verifier.py
```

Execution log:

```text
causal_set_reconstruction_verifier_run.log
```

## Captured output

```text
Causal set reconstruction verifier
==================================================
Route:
causal order -> longest-chain depth -> antichain slices -> causal-profile spatial adjacency
Coordinates are used only for synthetic evaluation of spatial-neighbor precision.

PASS: 95.0
SOFT_FAIL: 0.0
HARD_FAIL: 5.0
comparable_density_median: 0.21352458979027422
n_slices_median: 9.0
median_slice_size_median: 30.0
antichain_violation_median: 0.0
depth_time_corr_median: 0.9720695249464243
dim_proxy_median: 2.9930602008438965
spatial_neighbor_precision_median: 0.14204848494949832
```

## Interpretation

The verifier tests the replacement route:

```text
causal order
    -> longest-chain depth
    -> antichain rank slices
    -> causal-profile spatial adjacency
    -> interval-volume dimension proxy
```

This is the correct pivot after `ORDER_DISTANCE_EMBEDDING.md` failed.

It does not prove:
- full spatial metric recovery,
- manifoldlikeness,
- curved causal-set reconstruction,
- or Lorentzian geometry.

**End of summary.**
