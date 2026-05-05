# COEFFICIENT_DERIVATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Patch CL-2 coefficient bridge

## Status
**Executed structural verifier. Not a microscopic derivation.**

Verifier file:

```text
continuum_limit_verifier_v2.py
```

Execution log:

```text
continuum_limit_verifier_v2_run.log
```

## Captured output

```text
CL-2 symbolic coefficient derivation
==================================================
Lambda_star: -b/(a - 1)
chi: (1 - a)/(-a + b + 1)
Z_R: -Z0*b*(a - 1)/(-a + b + 1)**2
lambda_int: -b*lambda0*(a - 1)/(-a + b + 1)**2
m_R2: muR**2*(1 - a)
V0: 0
Vprime_at_Rstar: 0
Vsecond_at_Rstar: muR**2*(1 - a)
Tmem_expansion: eta*(-Tmat*b*lambda0*r*(a - 1)/(-a + b + 1)**2 - b**2*muR**2*(2*a*r/b - 2*r/b)/(2*(a - 1))) + eta**2*(-Z0*b*dr2*(a - 1)/(2*(-a + b + 1)**2) - b**2*muR**2*(a*r/b - r/b)**2/(2*(a - 1))) + O(eta**3)

CL-2 numerical sweep
==================================================
PASS: 99.191
SOFT_FAIL: 0.0
HARD_FAIL: 0.809
chi_min: 0.0005766938303031946
chi_median: 0.7935310738878313
chi_max: 0.9989839526125909
Lambda_min: 0.0010170807896883022
Lambda_median: 0.260190095771037
Lambda_max: 1733.0223658613684
Z_R_median: 0.05415588182140546
lambda_int_median: 0.005391396262720907
m_R2_median: 0.39301924878618466
```

## Interpretation

The verifier confirms the CL-2 coefficient bridge is structurally admissible for the sampled stable loading regimes.

The key symbolic checks are:

\[
V(0)=0,
\]

\[
V'(R_*)=0,
\]

\[
V''(R_*)=\mu_R^2(1-a).
\]

Thus, under the seam-2 stability condition

\[
0\le a<1,
\]

the potential has positive curvature at the retained-memory loading fixed point.

The sweep result:

```text
PASS: 99.191%
HARD_FAIL: 0.809%
```

The hard failures were deliberately injected invalid/pathological cases:
- unstable \(a\ge1\),
- negative \(b\),
- singular \(Z_0\),
- singular \(\mu_R\).

## Meaning

This verifies structural compatibility only.

It does **not** prove:
- microscopic origin of \(\mu_R,Z_0,\lambda_0\),
- uniqueness of the \(\chi(1-\chi)\) envelope,
- covariant emergence of \(R_{\mathrm{eff}}\),
- or the full continuum GR limit.

**End of summary.**
