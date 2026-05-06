# CONSERVATION_WITH_BOUNDARY_FLUX_VERIFIER_SUMMARY.md

# Verifier Summary
## Conservation residual with boundary flux

## Status
**Executed structural verifier. Not covariant conservation proof.**

Verifier file:

```text
conservation_with_boundary_flux_verifier.py
```

Execution log:

```text
conservation_with_boundary_flux_verifier_run.log
```

## Captured output

```text
Conservation with boundary flux verifier
==================================================
Route:
interaction cancellation + graph divergence + boundary flux -> ADM graph residual
Checks finite residual and weak-memory scaling.

PASS: 89.2
SOFT_FAIL: 10.8
HARD_FAIL: 0.0
interaction_residual_ratio_median: 0.0
boundary_flux_norm_median: 1.0363461993860918e-05
total_residual_norm_median: 9.211580268481072e-05
total_half_ratio_median: 0.49891436334642714
kinetic_half_ratio_median: 0.2499999614841444
finite_fraction_median: 1.0
```

## Interpretation

The verifier combines:
- derived interaction cancellation;
- graph-compatible interior divergence;
- graph-boundary flux.

It confirms:
- exact interaction-channel residual cancellation;
- finite boundary flux;
- finite total residual;
- \(O(\eta)\) and \(O(\eta^2)\) scaling.

This strengthens finite-slice conservation accounting but does not prove covariant conservation.

**End of summary.**
