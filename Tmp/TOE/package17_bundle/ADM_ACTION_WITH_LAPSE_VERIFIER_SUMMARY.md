# ADM_ACTION_WITH_LAPSE_VERIFIER_SUMMARY.md

# Verifier Summary
## ADM-like action proxy with measured lapse

## Status
**Executed structural verifier. Not full ADM/EH proof.**

Verifier file:

```text
adm_action_with_lapse_verifier.py
```

Execution log:

```text
adm_action_with_lapse_verifier_run.log
```

## Captured output

```text
ADM action with measured lapse verifier
==================================================
Route:
replace fixed N=1 with measured N_k from causal rank/slice density
main branch keeps N_a=0; aligned shift remains diagnostic-only

PASS: 94.0
SOFT_FAIL: 0.0
HARD_FAIL: 6.0
n_slices_median: 8.0
lapse_median_median: 1.003458747156299
lapse_cv_median: 0.03932362339741718
fixed_action_abs_median: 1761.3451410870189
lapse_action_abs_median: 1784.7064889599249
action_ratio_median: 1.0038791499625725
finite_fraction_median: 1.0
```

## Interpretation

The verifier replaces fixed \(N=1\) with measured \(N_k\) from causal rank / slice density.

The main branch keeps:

\[
N_a=0.
\]

Aligned shift remains diagnostic-only.

This strengthens the ADM action proxy but does not close full ADM, spatial curvature, boundary terms, or Einstein-Hilbert convergence.

**End of summary.**
