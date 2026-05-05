# MICRO_TO_BLOCK_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Micro-to-block action map

## Status
**Executed structural verifier. Not a microscopic proof.**

Verifier file:

```text
micro_to_block_action_verifier.py
```

Execution log:

```text
micro_to_block_action_verifier_run.log
```

## Captured output

```text
Micro-to-block action verifier
==================================================
Candidate map:
a     = (w_s alpha_s c_s + w_f alpha_f c_f) / mu_G
b     = (w_s beta_s I_s + w_f beta_f I_f) / (mu_G G_star)
K_t   = 1 + w_s alpha_s + w_f alpha_f
K_U   = K_t * (1-a)
K_x   = K_t * chi*(1-chi) * sigma_neighbor^2
K_int = K_t * chi*(1-chi) * rho_mat

Sweep results:
PASS: 96.479
SOFT_FAIL: 0.197
HARD_FAIL: 3.324
a_median: 0.2094273095088997
b_median: 0.022478946055010322
chi_median: 0.9688470147427344
chi_min: 0.00017794652866240872
chi_max: 0.9999998632711617
K_t_median: 1.4832378459808226
K_U_median: 1.1243411709620674
K_x_median: 7.075977820578564e-05
K_int_median: 0.0004262693777977181
```

## Interpretation

The verifier tests the candidate map:

\[
a
=
\frac{w_s\alpha_s c_s+w_f\alpha_f c_f}{\mu_G},
\]

\[
b
=
\frac{
w_s\beta_sI_s+w_f\beta_fI_f
}
{\mu_G\mathcal G_*},
\]

\[
K_t=1+w_s\alpha_s+w_f\alpha_f,
\]

\[
K_U=K_t(1-a),
\]

\[
K_x=K_t\chi(1-\chi)\sigma_{\nabla\Lambda}^2,
\]

\[
K_{\mathrm{int}}=K_t\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

The sweep shows that broad sampled stable microscopic regimes produce admissible positive block constants.

This does not prove the microscopic law. It only shows the candidate map is structurally viable.

**End of summary.**
