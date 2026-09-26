# v15.66 Polar derivative numerical adjudication — preregistration

Date: 2026-09-26.

## Purpose

Determine whether the v15.64/v15.65 finite-difference failures arise from a defect in the v15.61 analytic derivative factorization or from floating-point cancellation in the four-corner polar estimator.

This stage is numerical-method adjudication. It does not alter the v15.64 or v15.65 NO verdicts.

## Frozen cases

Use all 12 v15.58 asymmetric states and the exact v15.64 XXX hidden direction/global symmetric-null lift.

For each state, the analytic retained mixed correlation derivative is the v15.63 target

    delta C_e = O_e I/sqrt(3)

on all three edges.

## Method A — analytic Sylvester derivative

For each edge compute

    Q_e = O_e^T delta C_e - delta C_e^T O_e

and solve

    P_e W_e + W_e P_e = Q_e.

Record ||Q_e|| and ||W_e||. The construction predicts exact zero up to arithmetic roundoff.

## Method B — float64 four-corner estimator

Reuse the v15.64 affine source update with eta=1e-4.

Use source amplitudes

    [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5].

Record:
- raw four-corner numerator norm before division;
- divided mixed estimator norm;
- numerator/(machine epsilon * local polar scale).

No rank verdict.

## Method C — high-precision polar estimator

Use mpmath with 80 decimal digits.

Do NOT use an SVD implementation. Compute the right polar factor for each real 3x3 retained correlation matrix by

    O = C (C^T C)^(-1/2),

where the positive inverse square root is obtained by high-precision symmetric eigendecomposition.

Evaluate the same four corners at eta=1e-4 and source amplitudes

    [1e-3, 3e-4, 1e-4, 3e-5].

Record the mixed estimator norm.

## Frozen adjudication

NUMERICAL_CANCELLATION_CONFIRMED if:
1. analytic Sylvester mixed norm <= 1e-12 on all edges;
2. float64 raw numerator reaches an approximately t-independent floor at small t (last three numerator norms within factor 10 on every state);
3. high-precision mixed estimator at t=3e-5 is at least 1e4 smaller than float64 on every state and <=1e-12 absolute.

ANALYTIC_NUMERIC_DISAGREEMENT if analytic condition passes but high precision shows >1e-12 persistent mixed response.

ANALYTIC_FACTOR_INVALID if analytic Sylvester response itself exceeds 1e-12.

INVALID for positivity/state/provenance/high-precision solver failure.

These criteria are frozen before execution.

## Interpretation

Cancellation confirmation would explain why v15.65 showed an apparent ~1/t blow-up, while leaving both prior finite-double-precision NO verdicts intact. Analytic/high-precision disagreement would instead force revision of the v15.61 classification.
