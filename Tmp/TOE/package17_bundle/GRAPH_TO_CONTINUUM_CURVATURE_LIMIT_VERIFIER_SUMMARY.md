# GRAPH_TO_CONTINUUM_CURVATURE_LIMIT_VERIFIER_SUMMARY.md

# Verifier Summary
## Graph curvature refinement stability

## Status
**Executed reference-geometry refinement verifier. Current proxy not stable enough.**

Verifier file:

```text
graph_to_continuum_curvature_limit_verifier.py
```

Execution log:

```text
graph_to_continuum_curvature_limit_verifier_run.log
```

## Captured output

```text
Graph-to-continuum curvature limit verifier
==================================================
Route:
unit sphere sampled graph -> curvature proxy -> refinement stability
Diagnostic only; not proof of continuum curvature convergence.

n,h_median,R_est_calibrated,relative_error,coefficient_of_variation
100,0.4582525618,2.06704192,0.03352096014,0.4187500702
200,0.3196813085,2.051256935,0.02562846728,0.4318102635
400,0.2268022303,2.037673402,0.01883670079,0.4158925157
800,0.1607363148,2,0,0.4358697484
stability_class: PROXY_NOT_STABLE
cv_improvement_factor: 0.960723
```

## Interpretation

The verifier tests whether a graph curvature proxy stabilizes under increasing graph density on a known unit-sphere reference geometry.

The calibrated median can be matched to the known sphere curvature, but local variability does not decrease with refinement.

Therefore this is not yet evidence for:

\[
R_{\mathrm{graph}}^{(3)}
\rightarrow
R^{(3)}.
\]

**End of summary.**
