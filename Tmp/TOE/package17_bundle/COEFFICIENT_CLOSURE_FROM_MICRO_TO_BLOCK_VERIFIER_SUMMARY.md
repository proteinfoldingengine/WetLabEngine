# COEFFICIENT_CLOSURE_FROM_MICRO_TO_BLOCK_VERIFIER_SUMMARY.md

# Verifier Summary
## Coefficient closure from slow/fast retained-memory micro-to-block map

## Status
**Executed structural verifier. Micro-to-block constrained, not unique microscopic proof.**

Verifier file:

```text
coefficient_closure_from_micro_to_block_verifier.py
```

Execution log:

```text
coefficient_closure_from_micro_to_block_verifier_run.log
```

## Captured output

```text
Coefficient closure from micro-to-block verifier
==================================================
Route:
slow/fast retained-memory recursion -> loading map -> block constants -> continuum coefficients

PASS: 95.83
SOFT_FAIL: 3.139
HARD_FAIL: 1.031
a_median: 0.10674701349097675
b_median: 0.005524549282684422
Lambda_star_median: 0.005724076204032303
chi_star_median: 0.9941180154858547
K_t_median: 1.496616008842975
K_U_median: 1.2362240659484336
K_x_median: 1.7981908096673307e-05
K_int_median: 0.0004154678168615637
Z_R_median: 1.2218828132443919e-05
m_R2_median: 0.8932529865090233
V_quad_median: 0.44662649325451165
lambda_int_median: 0.00027984441608704206
finite_fraction_median: 1.0
```

## Interpretation

The verifier uses the concrete slow/fast retained-memory recursion:

\[
R_{t+1}^{(s)}
=
\alpha_sR_t^{(s)}+\beta_s|\xi_t|,
\]

\[
R_{t+1}^{(f)}
=
\alpha_fR_t^{(f)}+\beta_f|\xi_t|\Theta(|\xi_t|-\varepsilon^*).
\]

It maps this to:

\[
a,b,\Lambda_*,\chi_*,
K_t,K_U,K_x,K_{\mathrm{int}},
Z_R,m_R^2,\lambda_{\mathrm{int}}.
\]

This reduces coefficient freedom at block-action level but does not prove the candidate block constants are unique.

**End of summary.**
