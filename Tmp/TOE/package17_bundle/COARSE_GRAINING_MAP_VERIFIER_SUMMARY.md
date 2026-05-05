# COARSE_GRAINING_MAP_VERIFIER_SUMMARY.md

# Verifier Summary
## Coarse-graining map for \(R_{\mathrm{eff}}\sim\Lambda\)

## Status
**Executed structural verifier. Not a metric derivation.**

Verifier file:

```text
coarse_graining_map_verifier.py
```

Execution log:

```text
coarse_graining_map_verifier_run.log
```

## Captured output

```text
Coarse-graining map verifier
==================================================
Map tested:
G_block = <G_e>_B
M_block = <M_e>_B
R_eff   = Lambda_block = M_block / G_block
phi_eff = <phi_e>_B [proxy only]

Sweep results:
PASS: 99.48
SOFT_FAIL: 0.01
HARD_FAIL: 0.51
Lambda_mean_median: 0.5119507072320512
Lambda_cv_median: 0.08170381235391694
R_eff_std_median: 0.040957517533984786
Lambda_mean_min: 0.2740981074470208
Lambda_mean_max: 2.573909536317794
```

## Interpretation

The verifier tests:

\[
G_B=\langle G_e\rangle_B,
\]

\[
M_B=\langle M_e\rangle_B,
\]

\[
R_{\mathrm{eff}}=\Lambda_B=\frac{M_B}{G_B}.
\]

The sweep shows that broad sampled local regimes produce a finite, stable scalar loading field.

This does not prove:
- emergent metric construction,
- Lorentzian covariance,
- Regge/causal-set compatibility,
- or full GR continuum recovery.

It only supports the narrower identification:

\[
R_{\mathrm{eff}}\sim\Lambda.
\]

**End of summary.**
