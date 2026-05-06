# MATTER_EXCHANGE_DERIVATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Matter exchange from scalar memory-matter interaction

## Status
**Executed structural verifier. Not covariant conservation proof.**

Verifier file:

```text
matter_exchange_derivation_verifier.py
```

Execution log:

```text
matter_exchange_derivation_verifier_run.log
```

## Captured output

```text
Matter exchange derivation verifier
==================================================
Route:
L_int = lambda R_eff O_mat -> Q_mat ADM proxy
Checks O(eta) scaling and cancellation with interaction memory exchange.

PASS: 100.0
SOFT_FAIL: 0.0
HARD_FAIL: 0.0
q_mat_norm_median_median: 4.2702961654984524e-05
q_mat_half_ratio_median: 0.4999999882889808
q_mem_int_norm_median_median: 4.2702961654984524e-05
best_residual_ratio_median: 0.0
finite_fraction_median: 1.0
```

## Interpretation

The verifier derives a matter exchange proxy from:

\[
\lambda_{\mathrm{int}}R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}.
\]

It confirms:
- finite matter exchange;
- \(O(\eta)\) scaling;
- cancellation with the interaction part of memory exchange under a consistent sign convention.

This improves the Bianchi/conservation branch but does not prove covariant conservation.

**End of summary.**
