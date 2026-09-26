# v15.65 Null asymptotic scaling — preregistration

Date: 2026-09-26.

## Purpose

Adjudicate the v15.64 finite-strength failure without changing its verdict.

v15.61 predicts that the mixed rotational derivative at source amplitude t=0 vanishes for the constructed symmetric-null source vector field. v15.64 showed that the centered finite-t estimator is not exactly zero at finite t. v15.65 asks whether that residual is a higher-order nonlinear correction that collapses with the expected centered-estimator scaling.

## Frozen construction

Use the exact v15.64 states, XXX hidden tangent, global minimum-norm symmetric-null lifts, affine source vector field, hidden probe eta=1e-4, and polar-rotation observable. No construction parameter is refit.

## Source amplitudes

Freeze

    t = [1e-3, 5e-4, 2.5e-4, 1.25e-4, 6.25e-5].

These are chosen before measurement as a factor-two ladder spanning 16x.

## Observable

For each state and t compute the Frobenius norm of the full three-edge centered mixed-rotation estimator

    M(t) = [O(+eta,+t)-O(+eta,-t)-O(-eta,+t)+O(-eta,-t)]/(4 eta t).

Do not threshold M(t) into a rank for the primary test.

## Scaling prediction

For a smooth observable and an exact zero mixed derivative at t=0, symmetric centering in t cancels odd estimator errors so the leading source-amplitude correction to the derivative estimator is generically O(t^2), with eta fixed.

Fit log ||M(t)|| versus log t over all five frozen amplitudes by ordinary least squares.

Primary criteria, on every one of 12 states:

- fitted slope in [1.7, 2.3];
- ||M(t_min)|| < ||M(t_max)|| / 100;
- finite source states remain positive and normalized.

Secondary diagnostics:
- adjacent factor-two effective slopes;
- R^2 of log-log fit;
- absolute residual at smallest t;
- analytic polar-skew projection remains zero.

Verdicts:

NULL_DERIVATIVE_ASYMPTOTICS_CONFIRMED
NULL_DERIVATIVE_ASYMPTOTICS_NOT_CONFIRMED
INVALID

The v15.64 verdict remains FALSIFIED regardless of v15.65 outcome.

## Interpretation

Confirmation supports the explanation that v15.64 failed because a finite-amplitude nonlinear polar correction survives while the t=0 mixed derivative is zero. Failure would require revisiting the derivative implementation/factorization or the assumed asymptotic regime.
