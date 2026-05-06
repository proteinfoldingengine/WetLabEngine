# GRAPH_COVARIANT_DIVERGENCE_VERIFIER_SUMMARY.md

# Verifier Summary
## Graph-compatible divergence of projected memory stress

## Status
**Executed structural verifier. Not continuum covariant derivative proof.**

Verifier file:

```text
graph_covariant_divergence_verifier.py
```

Execution log:

```text
graph_covariant_divergence_verifier_run.log
```

## Captured output

```text
Graph covariant divergence verifier
==================================================
Route:
antichain graph + projected stress S_ab -> graph-compatible D^a S_ab
Checks finite divergence and weak-memory scaling.

PASS: 91.6
SOFT_FAIL: 8.4
HARD_FAIL: 0.0
graph_div_norm_median_median: 0.00031640429181109715
graph_div_half_ratio_median: 0.4978963633431301
kinetic_half_ratio_median: 0.24999998906354332
finite_fraction_median: 1.0
graph_connectivity_fraction_median: 1.0
```

## Interpretation

The verifier defines a graph-compatible divergence:

\[
(D^aS_{ab})(i)
\approx
\sum_{j\in N(i)}
W_{ij}
u_{ij}^a
\left[
S_{ab}(j)-S_{ab}(i)
\right].
\]

It confirms:
- finite graph divergence;
- graph connectivity;
- interaction-dominated \(O(\eta)\) scaling;
- kinetic-only \(O(\eta^2)\) scaling.

This improves the Bianchi/conservation branch but does not prove continuum covariant divergence.

**End of summary.**
