# v15.57 Source-law specificity gate — preregistration

Date: 2026-09-26.

## Question

Does the previously measured hidden/source response depend on the chosen normalized exponential-tilt source law, or does it persist under a source update whose retained one- and two-body marginals are autonomous?

This task compares the historical exponential tilt with a **local-unitary control using exactly the same nine one-body Pauli generators**. It does not tune fixtures, source coefficients, or thresholds after seeing the answer.

## Frozen inputs

- Parent research head: `f0684514f1430cd02d097ffe9516c934ff26ffba`.
- Historical source commit remains `0b7e9ca67cfa98831e60eb3e2add7c42a806f513`.
- The 11 fixtures are exactly the source-edge-factorization fixtures.
- Hidden basis: all 27 exact-weight-three Pauli products from `response_quotient_rank.HB`.
- Source basis: the same 9 one-body Pauli generators from `response_quotient_rank.PB`.
- No fitting or fixture selection based on response.

## Two source laws

Historical law:
[
T^{\mathrm{exp}}_s(\rho;p)=
\frac{\exp(\log\rho+s p)}
{\mathrm{Tr}\exp(\log\rho+s p)}.
]

Control law:
[
T^{\mathrm{U}}_s(\rho;p)=
U_p(s)\rho U_p(s)^\dagger,
\qquad U_p(s)=\exp(-i s p/2).
]

Because each (p) is one-body, (T^{\mathrm{U}}_s) is a tensor-product local unitary. If two global states have the same proper one- and two-body marginals, their retained marginals remain the same after this control for every finite (s). Exact-weight-three hidden directions therefore predict a zero mixed hidden/source retained-geometry response on the regular stratum.

## Frozen numerical probe

- Hidden amplitude: `ETA = 1e-3`.
- Unitary source amplitude: `S = 0.137`.
- The mixed unitary edge response is the symmetric four-corner quotient in ((\eta,s)). Because the null is finite-(s) algebraic under marginal closure, no infinitesimal extrapolation is needed.
- The ordinary unitary source must be demonstrably active: at least one of the 9 generators must change the edge polar geometry by Frobenius norm > `1e-4` at (s=S).
- Proper-marginal closure residual across every hidden/source pair must be <= `1e-11`.
- Unitariy mixed-response norm is judged relative to the historical exponential edge map: `||E_U||_F / ||E_exp||_F <= 1e-9`.
- Effective unitary mixed rank must be zero at parent-scaled relative cuts `1e-9, 1e-10, 1e-11`.
- Historical exponential edge rank is not assumed by validity. It is measured and reported.

## Outcomes

- `SOURCE_LAW_SPECIFICITY_CONFIRMED`: all controls pass, the local-unitary source is active, retained marginals remain closed, and its hidden/source mixed edge map is null under the frozen resolution rule while the historical exponential response is non-null.
- `SOURCE_LAW_SPECIFICITY_NOT_SHOWN`: controls pass but the above contrast is absent.
- `INVALID`: provenance, fixture, finite-value, regular-stratum, closure, or artifact-integrity controls fail.

A controlled null under the local-unitary law would show **source-law specificity**, not prove the exponential tilt is physical, unique, gravitational, or universal.

## Evidence requirements

The run must save per-fixture raw matrices for the exponential edge map, unitary mixed edge map, unitary finite source effects, closure residuals, labels, and conditioning metadata; a JSON report with hashes; and a verifier that rereads artifacts. Scientific invalidity must exit nonzero.
