# ADM_ACTION_WITH_GRAPH_CURVATURE_VERIFIER_SUMMARY.md

# Verifier Summary
## ADM-like action with measured lapse and graph curvature

## Status
**Executed structural verifier. Not full ADM/EH proof.**

Verifier file:

```text
adm_action_with_graph_curvature_verifier.py
```

Execution log:

```text
adm_action_with_graph_curvature_verifier_run.log
```

## Captured output

```text
ADM action with graph curvature verifier
==================================================
Route:
measured lapse + explicit R3_graph -> ADM-like action proxy
main branch keeps N_a=0; not full ADM/EH convergence

PASS: 86.0
SOFT_FAIL: 0.0
HARD_FAIL: 14.0
n_slices_median: 9.0
lapse_median_median: 0.9999999999995073
lapse_cv_median: 0.0367625773546524
R3_graph_median_median: 0.2643796148801645
action_graph_abs_median: 879.9853498689251
action_spectral_abs_median: 1758.4425220873677
action_ratio_median: 0.61009408526721
finite_fraction_median: 1.0
```

## Interpretation

The verifier integrates:
- measured lapse \(N_k\),
- zero main-branch shift,
- antichain spatial metric \(h_{ab}\),
- graph-native \(R^{(3)}_{\mathrm{graph}}\),
- extrinsic-curvature proxy.

It confirms the integrated action remains finite and controlled in sampled regimes.

This is not full ADM, not variational closure, and not Einstein-Hilbert convergence.

**End of summary.**
