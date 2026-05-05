# SPATIAL_GRAPH_CURVATURE_VERIFIER_SUMMARY.md

# Verifier Summary
## Spatial graph curvature on antichain slices

## Status
**Executed structural verifier. Not continuum \(R^{(3)}\) proof.**

Verifier file:

```text
spatial_graph_curvature_verifier.py
```

Execution log:

```text
spatial_graph_curvature_verifier_run.log
```

## Captured output

```text
Spatial graph curvature verifier
==================================================
Route:
antichain spatial graph + h_ab proxy -> Forman/Ollivier-like R3 graph curvature proxy
This is not continuum R^(3), but replaces the pure spectral placeholder.

PASS: 90.0
SOFT_FAIL: 1.6666666666666667
HARD_FAIL: 8.333333333333334
n_slices_median: 9.0
median_edges_median: 213.5
forman_median_median: -14.999999999984999
forman_iqr_median: 4.986625436539217
ollivier_proxy_median_median: 0.3157894736842105
scalar_R3_median_median: 0.26992776747543495
finite_fraction_median: 1.0
```

## Interpretation

The verifier replaces a pure spectral placeholder with explicit graph-curvature proxies:
- Forman-style curvature;
- Ollivier-style neighbor-overlap curvature;
- normalized slice scalar \(R^{(3)}_{\mathrm{graph}}\).

This strengthens the spatial curvature ingredient but does not prove continuum spatial curvature convergence.

**End of summary.**
