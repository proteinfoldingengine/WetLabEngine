# MEMORY_EXCHANGE_CURRENT_ADM_VERIFIER_SUMMARY.md

# Verifier Summary
## ADM memory exchange current

## Status
**Executed structural verifier. Not covariant conservation closure.**

Verifier file:

```text
memory_exchange_current_adm_verifier.py
```

Execution log:

```text
memory_exchange_current_adm_verifier_run.log
```

## Captured output

```text
Memory exchange current ADM verifier
==================================================
Route:
project ∇^μ T^mem_{μν} = -Q_ν into ADM normal/spatial exchange proxies
Checks finite exchange and weak-memory scaling.

PASS: 94.0
SOFT_FAIL: 6.0
HARD_FAIL: 0.0
q_perp_norm_median_median: 7.75566319733455e-06
q_spatial_norm_median_median: 1.5353386148452698e-05
q_total_half_ratio_median: 0.49871047698313964
q_kinetic_half_ratio_median: 0.24999941209250437
finite_fraction_median: 1.0
weak_suppression_fraction_median: 1.0
```

## Interpretation

The verifier projects the memory exchange current into ADM-style components:

\[
Q_\perp,\qquad Q_a.
\]

It confirms:
- finite normal/spatial exchange;
- weak-memory suppression;
- interaction-dominated \(O(\eta)\) scaling;
- kinetic \(O(\eta^2)\) scaling.

This supports controlled exchange at proxy level, not full covariant conservation.

**End of summary.**
