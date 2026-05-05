# CAUSAL_INTERVAL_GEOMETRY_VERIFIER_SUMMARY.md

# Verifier Summary
## Interval scaling and dimension proxy

## Status
**Executed structural verifier. Not a coordinate-free metric proof.**

Verifier file:

```text
causal_interval_geometry_verifier.py
```

Execution log:

```text
causal_interval_geometry_verifier_run.log
```

## Captured output

```text
Causal interval geometry verifier
==================================================
Test:
Build causal intervals I(i,j), count |I(i,j)|, estimate dimension from log interval-size scaling.

Sweep results:
PASS: 87.5
SOFT_FAIL: 2.5
HARD_FAIL: 10.0
dim_estimate_median: 2.598292971546218
dim_estimate_min: 1.423584566509049
dim_estimate_max: 2.943546323196807
r2_median: 0.8677155751384873
comparable_pairs_median: 17423.0
```

## Interpretation

The verifier tests whether causal interval cardinality scales with proper-time-like separation:

\[
|I(i,j)|\sim\tau_{ij}^{D}.
\]

It estimates \(D\) from a log-log regression.

This supports the causal-geometry seam only structurally. It does not prove:
- coordinate-free metric reconstruction,
- manifoldlikeness,
- light-cone recovery from order alone,
- or curved spacetime interval scaling.

**End of summary.**
