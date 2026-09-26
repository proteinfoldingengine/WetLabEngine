# Closed-Form Mixed Response Gate — Preregistration

Parent computational theorem: 0d8bbb51841f517017f44fd4b132c8f1d8bbafb8.

Goal: remove the remaining symmetric eta derivative from K=d_eta d_s H|0.

## Exact derivative chain
For rho_eta=rho+eta G:
L_eta=log(rho_eta), with L'=Dlog_rho[G].
The normalized ETL source tangent is T(rho)=Dexp_log(rho)[P]-rho Tr(Dexp_log(rho)[P]).
Its eta derivative must be computed algebraically as
T' = D2exp_L[L',P] - G Tr(Dexp_L[P]) - rho Tr(D2exp_L[L',P]).
D2exp is the symmetric second Frechet derivative, evaluated by a block-matrix / divided-difference construction, not finite differencing.

Connected-correlation derivatives C_eta, C_s, C_eta_s are computed exactly from state tangents and marginal product rules.

For each nonsingular edge polar C=OS, first polar derivatives satisfy the Sylvester equation. The mixed polar derivative O_eta_s must be obtained by differentiating that Sylvester equation, including derivatives of O, S and its RHS. No SVD finite differencing.

Finally K=d_eta d_s(O1 O2 O3) is the full mixed product rule including edge mixed terms and cross-edge O_eta O_s terms.

## Verification
All same 11 fixtures.
Compare closed-form K_CF against:
1. prior computational K from parent;
2. independent four-corner K_fd.
All 11: relative error <=1e-5 for both comparisons.
No fitted coefficients and no numerical derivative in eta or s inside K_CF.

Verdicts:
CLOSED_FORM_MIXED_RESPONSE_THEOREM_VERIFIED
CLOSED_FORM_FORMULA_FAILS
DEGENERATE_STRATUM
