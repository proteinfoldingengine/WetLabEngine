# PERIODIC_CONFORMAL_GRID_REFERENCE_VERIFIER_SUMMARY.md

# Verifier Summary
## Periodic conformal grid reference

## Status
**Executed reference construction verifier. Reference passed.**

Verifier file:

```text
periodic_conformal_grid_reference_verifier.py
```

Execution log:

```text
periodic_conformal_grid_reference_verifier_run.log
```

## Captured output

```text
Periodic conformal grid reference verifier
==================================================
Route:
deterministic periodic conformal grid -> exact R,dV -> Gauss-Bonnet + metric stencil sanity

N: 64
amp: 0.25
dx: 0.09817477042468103
gauss_bonnet_sum_RdV: -5.0415401020575956e-17
abs_gauss_bonnet_error: 5.0415401020575956e-17
finite_difference_R_relative_error: 0.0008029324607676338
R_min: -1.6487212707001282
R_max: 0.6065306597126334
R_mean: -0.12795523503961082
positive_R_fraction: 0.5
negative_R_fraction: 0.5
rho_positive_integral: 7.9871520503391
rho_negative_integral: -7.9871520503391
rho_total: -5.0415401020575956e-17
graph_nodes: 4096
graph_edges_undirected: 8192
edge_length_min: 0.07650462306263041
edge_length_max: 0.12598304732576038
edge_length_mean: 0.0989421536497607
weight_min: 0.6625333213599657
weight_max: 0.8591469393385237
weight_mean: 0.7742770455598758
classification: CONFORMAL_GRID_REFERENCE_READY
```

## Interpretation

The deterministic periodic conformal grid now passes exact curvature, volume, and Gauss-Bonnet sanity checks.

It is ready for local heat-curvature density testing.

**End of summary.**
