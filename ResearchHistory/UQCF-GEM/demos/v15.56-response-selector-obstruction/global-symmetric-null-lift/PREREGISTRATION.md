# v15.63 Global symmetric-null lift — preregistration

Date: 2026-09-26.

## Question

Can the v15.62 retained-observable symmetric-null leakage be realized by a legitimate Hermitian trace-zero global tangent Y on the three-qubit state space?

This is an existence problem, not yet a construction of a complete finite source flow.

## Global tangent basis

Use the 63 nonidentity three-qubit Pauli strings, Hilbert-Schmidt normalized. Any Hermitian trace-zero tangent is

    Y = sum_a y_a B_a.

For each edge e=(i,j), compute the induced first-order one- and two-body expectation changes from Y and therefore the induced connected-correlation derivative

    delta C_e(Y).

This map is linear in y.

## Target sectors

For each of the 12 frozen asymmetric states and each edge, use the regular polar rotation O_e.

Two feasibility tests are frozen.

### A. Single-edge symmetric-null lift

For each edge and each of the six symmetric basis matrices H_a, solve

    delta C_e(Y) = O_e H_a

while requiring the one-body derivative on all three sites to be zero.

No constraint is placed on the other two edge correlation derivatives.

This asks whether each local v15.62 null direction is globally liftable.

### B. Simultaneous three-edge symmetric-null lift

Use a fixed target H=I/sqrt(3) on all three edges:

    delta C_e(Y) = O_e H   for e=0,1,2,

with all one-body derivatives zero.

This asks whether a nontrivial symmetric-null leakage pattern can be realized simultaneously across the complete retained atlas.

## Solver

Build the exact linear map from Pauli coefficients to one-body and pair-correlation derivatives. Solve by SVD/pseudoinverse with no regularization.

Report:
- feasibility residual relative to target norm;
- coefficient norm of minimum-norm lift;
- rank and nullity of each constraint matrix;
- direct recomputation residual from reconstructed Y;
- trace and Hermiticity residuals.

Frozen feasibility tolerance: relative residual <= 1e-10.

No response rank is used in choosing targets or solver settings.

## Adjudication

- GLOBAL_SYMMETRIC_NULL_LIFT_EXISTS: every single-edge target is feasible on all states and the simultaneous fixed target is feasible on all states.
- PARTIAL_GLOBAL_LIFT_ONLY: all single-edge targets are feasible but at least one simultaneous target is infeasible.
- GLOBAL_LIFT_OBSTRUCTED: at least one single-edge target is infeasible.
- INVALID: numerical/provenance/state-identity failure.

## Interpretation boundary

Existence of Y proves only that the retained symmetric-null sector is compatible with a global normalized-state tangent. It does not by itself prove that Y arises as D X_rho[h] from a covariant, positive, finite source update. That stronger source-vector-field realization is a later problem.
