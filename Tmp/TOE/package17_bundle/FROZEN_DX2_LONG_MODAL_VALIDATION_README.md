# Frozen dx2/long Modal Library Validation

## Interpretation of the previous run

The previous calibration found:

- `raw/long` had the lowest combined stability score
- but `raw/long` produced q ≈ 7.63, which is a graph-time scaling artifact
- `dx2/long` produced q ≈ 1.06, no dropped rows, stable sign, and lower mean I error

So we should freeze the physical candidate:

```text
operator = graph_laplacian / dx^2
window = long = [0.25, 0.40, 0.65, 1.00, 1.60]
```

## What this notebook tests

It re-runs the 23-geometry modal library using only `dx2/long` and measures:

1. q stability across geometries
2. C stability within each geometry
3. amplitude power law
4. modal descriptor prediction of C
5. leave-one-geometry-out generalization
6. whether sign flips are gone

## What to send back

```text
FROZEN DX2 LONG SUMMARY
GEOMETRY_FITS
DESCRIPTOR_MODEL_RANKINGS
LEAVE_ONE_GEOMETRY_OUT
```
