# COLAB_MULTI_GEOMETRY_TRACE_DX_SCALING.md

# Multi-Geometry Trace dx-Scaling Campaign

## Purpose

Test whether the global heat-trace dx² law survives beyond the original conformal mode.

Current validated single-family law:

\[
\int R\,dV
\approx
-C_0 dx^2[B(a)-B(0)]
\]

with:

```text
C0 ≈ 14.5
q ≈ 2
```

## This campaign tests

```text
xyz_product
high_x_product
additive_mixed
two_mode_product
anisotropic_packet
```

For each geometry, it fits:

\[
C_\Delta(dx)=\frac{\int R\,dV}{B(a)-B(0)}
\approx
-c\,dx^q.
\]

## Output to send back

```text
MULTI-GEOMETRY TRACE DX SCALING SUMMARY
GEOMETRY_SUMMARY
UNIVERSAL_PRED_ROWS
GPU or CPU used
```

## Interpretation

A strong result would show:

```text
each geometry fit_q near 2
per-geometry max prediction error < 8%
universal q near 2
```

A mixed result would mean the dx² law may be geometry-dependent or requires additional normalization by spectral content / mode energy.

**End of file.**
