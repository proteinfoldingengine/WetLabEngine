# CAUSAL_ADM_FIELD_EQUATION_PROXY_VERIFIER_SUMMARY.md

# Verifier Summary
## Discrete field-equation proxy with weak-memory source

## Status
**Executed structural verifier. Not Einstein equations.**

Verifier file:

```text
causal_adm_field_equation_proxy_verifier.py
```

Execution log:

```text
causal_adm_field_equation_proxy_verifier_run.log
```

## Captured output

```text
Causal ADM field equation proxy verifier
==================================================
Route:
finite Euler response E_ab^(k) = weak-memory source S_ab^(mem,k)
This is a discrete proxy, not Einstein's equation.

PASS: 100.0
SOFT_FAIL: 0.0
HARD_FAIL: 0.0
euler_norm_median_median: 0.6800877978990056
source_norm_median_median: 0.0011714507094753575
residual_norm_median_median: 0.6791999554202897
source_to_euler_ratio_median: 0.001612824295743367
weak_scaling_ratio_median: 0.499999999573022
finite_fraction_median: 1.0
```

## Interpretation

The verifier tests:

\[
\mathcal E_{ab}^{(k)}
=
\mathcal S_{ab}^{\mathrm{mem},k}.
\]

It confirms:
- finite Euler response;
- finite weak-memory source;
- finite residual;
- source small relative to Euler response;
- linear weak-memory scaling.

This is a proxy-level field equation, not Einstein's equation.

**End of summary.**
