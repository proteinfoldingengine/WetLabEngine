# COEFFICIENT_MICRO_DERIVATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Conditional coefficient extraction from two-mode retained-memory recursion

## Status
**Executed structural verifier. Conditional theorem pass.**

Verifier file:

```text
coefficient_micro_derivation_verifier.py
```

Execution log:

```text
coefficient_micro_derivation_verifier_run.log
```

## Captured output

```text
Coefficient micro-derivation verifier
==================================================
Route:
two-mode retained-memory recursion ansatz -> Z_R, V(R), lambda_int
Conditional theorem pass; exact recursion must replace ansatz for closure.

PASS: 77.44
SOFT_FAIL: 20.95
HARD_FAIL: 1.61
Z_R_median: 4.891534451311188
m_R2_median: 11.153798957780275
lambda_int_median: 0.2520409784486992
V_quad_median: 5.576899478890137
weak_scaling_ratio_median: 0.4824955068069357
finite_fraction_median: 1.0
```

## Interpretation

The verifier tests the conditional coefficient map:

\[
Z_R=\frac{1}{2D_R},
\]

\[
m_R^2=\frac{k_R}{D_R},
\]

\[
V(R)=\frac12m_R^2(R-R_*)^2+\cdots,
\]

\[
\lambda_{\mathrm{int}}=\frac{\lambda_{\mathrm{micro}}}{D_R}.
\]

It confirms finite positive coefficients and correct weak-memory scaling for stable microscopic drift/diffusion regimes.

This does not close coefficient derivation until the exact production recursion is substituted.

**End of summary.**
