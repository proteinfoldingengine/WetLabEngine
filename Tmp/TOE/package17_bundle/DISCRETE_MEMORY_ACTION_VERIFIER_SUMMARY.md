# DISCRETE_MEMORY_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Discrete memory action scale map

## Status
**Executed structural verifier. Not a microscopic derivation.**

Verifier file:

```text
discrete_memory_action_verifier.py
```

Execution log:

```text
discrete_memory_action_verifier_run.log
```

## Captured output

```text
Discrete memory action verifier
==================================================
Continuum scale map:
mu_R^2 = K_U / K_t
Z0     = (K_x / K_t) * (dx / dt)^2
lambda0= K_int / K_t
m_R^2  = mu_R^2 * (1-a)

Sweep results:
PASS: 98.988
SOFT_FAIL: 0.193
HARD_FAIL: 0.819
chi_median: 0.7908626513090353
mu_R2_median: 0.31698772999262315
Z0_median: 0.2995201010519064
lambda0_median: 0.0314293688446046
m_R2_median: 0.12218476761960194
chi_min: 0.0007198712317079496
chi_max: 0.9990001095950791
```

## Interpretation

The verifier tests the first structural map:

\[
\mu_R^2=\frac{K_U}{K_t},
\]

\[
Z_0=\frac{K_x}{K_t}\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_0=\frac{K_{\mathrm{int}}}{K_t},
\]

\[
m_R^2=\mu_R^2(1-a).
\]

For positive action constants and stable seam-2 loading parameters, the continuum scales remain finite and positive.

The hard failures are deliberately injected invalid cases:
- \(a\ge1\),
- \(b<0\),
- \(K_t<0\),
- \(K_U<0\),
- singular scale behavior.

This verifies structural compatibility only. It does not derive the block constants from the microscopic pruning law.

**End of summary.**
