# Mixed Hidden-Completion / Source Response Theorem Gate — Preregistration

Empirical parent: 66f1b048ac71e104d53328bf02b69e26634a0f85, verdict ROBUST_LINEAR_HIDDEN_GEOMETRY_RESPONSE.

## Mathematical target
For rho_eta = rho + eta G and ETL source flow E_s(rho_eta)=exp(log rho_eta+sP)/Z, define pair connected correlations C_e(eta,s), proper polar factors O_e(eta,s), and loop H(eta,s)=product_e O_e.

Derive and verify the mixed response coefficient
K = d/deta [ dH/ds (eta,0) ] at eta=0.

Chain to be tested without fitting:
1. D log_rho[G] by the divided-difference Frechet derivative of matrix log.
2. Mixed ETL state derivative by differentiating the normalized exponential tangent with respect to eta.
3. Pair-correlation mixed derivative from exact Pauli expectation differentiation, including product-of-marginal terms.
4. Polar derivative: if C=O S is nonsingular, Omega=O^T dO solves S Omega + Omega S = skew factor 2*skew(O^T dC); dO=O Omega.
5. Loop product rule with one mixed insertion plus cross terms from eta- and s-first edge derivatives.

## Frozen numerical verification
Use all 11 already-adjudicated base fixtures from the frozen grid.
Analytic K is computed from Frechet/Sylvester formulas only.
Reference K_fd is a symmetric four-corner finite difference of H at (eta,s)=(+/-1e-5,+/-1e-5), not used in the analytic formula.
Per-fixture relative Frobenius error <= 1e-4 (absolute <=1e-7 allowed when reference norm is tiny).
All 11 must pass.

Additionally compare ||K|| with the empirical through-origin slope of D(eta) from eta=.001,.002,.003. This is secondary and must agree within 5%.

Verdicts:
ANALYTIC_MIXED_RESPONSE_THEOREM_VERIFIED
ANALYTIC_FORMULA_FAILS
DEGENERATE_STRATUM

No coefficients may be fitted to finite-difference or ensemble response data.
