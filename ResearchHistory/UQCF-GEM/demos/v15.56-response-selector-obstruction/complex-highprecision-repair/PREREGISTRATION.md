# v15.68 Complex high-precision repair — preregistration

Date: 2026-09-26.

## Purpose

Repair only the v15.66 high-precision complex-number transport defect identified by v15.67, verify frozen-corner identity, then rerun the v15.66 analytic/float64/80-digit adjudication unchanged.

## Frozen inputs

- same 12 asymmetric states;
- same v15.64 XXX hidden tangent and global symmetric-null Y;
- eta = 1e-4;
- float64 amplitudes = [1e-2,3e-3,1e-3,3e-4,1e-4,3e-5];
- high-precision amplitudes = [1e-3,3e-4,1e-4,3e-5];
- mpmath precision = 80 digits;
- same v15.66 verdict thresholds.

## Only permitted repair

Replace the real-only matrix conversion with exact complex transport:

    A_ij -> mp.mpc(real(A_ij), imag(A_ij)).

High-precision Pauli expectations use the full complex state and operator and take the real part only after the trace is accumulated.

No state, amplitude, polar formula, target, or threshold changes are permitted.

## Gate 1 — frozen-corner identity

For candidate 13, eta=1e-4, t=1e-3, +hidden/+source corner:
- state max entry difference <=1e-13 after conversion;
- one-/two-body moments <=1e-13;
- connected C <=1e-13;
- polar factor <=1e-11.

If this gate fails: INVALID and no full adjudication.

## Gate 2 — full v15.66 rerun

Reuse the exact v15.66 adjudication:
NUMERICAL_CANCELLATION_CONFIRMED if
1. analytic skew <=1e-12 on all edges;
2. float64 last-three raw numerator floor factor <=10 on every state;
3. 80-digit mixed norm at t=3e-5 <=1e-12 and at least 1e4 smaller than float64 on every state.

Otherwise:
ANALYTIC_NUMERIC_DISAGREEMENT,
ANALYTIC_FACTOR_INVALID,
or INVALID under the same definitions as v15.66.

v15.64 and v15.65 remain unchanged NO results regardless of outcome.
