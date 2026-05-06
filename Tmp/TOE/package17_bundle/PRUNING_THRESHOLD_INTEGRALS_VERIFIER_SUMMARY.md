# PRUNING_THRESHOLD_INTEGRALS_VERIFIER_SUMMARY.md

# Verifier Summary
## Slow/fast pruning-threshold integrals

## Status
**Executed analytic + Monte Carlo verifier. Gaussian assumption.**

Verifier file:

```text
pruning_threshold_integrals_verifier.py
```

Execution log:

```text
pruning_threshold_integrals_verifier_run.log
```

## Captured output

```text
Pruning threshold integrals verifier
==================================================
Route:
Gaussian noise -> I_s and I_f(eps*) closed forms

PASS: 74.0
SOFT_FAIL: 26.0
HARD_FAIL: 0.0
I_s_analytic_median: 1.2601587425606637
I_f_analytic_median: 0.13499393517283803
ratio_analytic_median: 0.15623545037286146
rel_err_s_median: 0.0015088314750812176
rel_err_f_median: 0.007974246953227595
```

## Interpretation

For:

\[
\xi\sim\mathcal N(0,\sigma_\xi^2),
\]

the verifier confirms:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

and:

\[
I_f=
\sqrt{\frac{2}{\pi}}\sigma_\xi
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

Thus:

\[
I_f/I_s=
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

This makes the pruning-threshold dependence explicit.

**End of summary.**
