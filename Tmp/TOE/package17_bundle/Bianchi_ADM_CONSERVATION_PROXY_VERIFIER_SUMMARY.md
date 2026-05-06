# Bianchi_ADM_CONSERVATION_PROXY_VERIFIER_SUMMARY.md

# Verifier Summary
## ADM total-conservation residual

## Status
**Executed structural verifier. Not Bianchi proof.**

Verifier file:

```text
bianchi_adm_conservation_proxy_verifier.py
```

Execution log:

```text
bianchi_adm_conservation_proxy_verifier_run.log
```

## Captured output

```text
Bianchi ADM conservation proxy verifier
==================================================
Route:
Q_mem + Q_mat = 0 at ADM proxy level with controlled closure residual
This is not covariant Bianchi proof.

PASS: 88.33333333333333
SOFT_FAIL: 11.666666666666666
HARD_FAIL: 0.0
mem_exchange_norm_median_median: 2.4059979592917865e-05
total_residual_norm_median_median: 5.259310908417771e-08
residual_to_mem_ratio_median: 0.0017674840020501237
residual_tol_scaling_ratio_median: 0.4999904801521554
finite_fraction_median: 1.0
```

## Interpretation

The verifier tests ADM-level cancellation:

\[
Q_{\mathrm{mem}} + Q_{\mathrm{mat}} = 0
\]

up to a controlled residual.

It confirms:
- finite exchange currents;
- finite residual;
- residual small relative to memory exchange;
- residual scales linearly with conservation tolerance.

This supports total-conservation structure at proxy level, not covariant Bianchi closure.

**End of summary.**
