# Modal Library Trace Normalization Campaign

## Current diagnosis

The prior result showed:

```text
q_mean ≈ 2.064
q_std ≈ 0.204
best scalar descriptor = log_k_eff
classification = MIXED
```

Meaning:

```text
dx² scaling survives
universal C0 fails
single spectral moment is insufficient
```

## Next theorem target

Instead of:

```text
int R dV ≈ -C0 dx² ΔTrace
```

test:

```text
int R dV ≈ -C(f) dx^q ΔTrace
```

where `C(f)` is predicted from a modal descriptor vector.

## What to send back

```text
MODAL LIBRARY TRACE NORMALIZATION SUMMARY
GEOMETRY_FITS
TOP_DESCRIPTOR_MODELS
BEST_DESCRIPTOR_BY_GEOMETRY
```
