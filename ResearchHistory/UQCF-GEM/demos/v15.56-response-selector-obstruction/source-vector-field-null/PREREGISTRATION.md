# v15.64 Source-vector-field symmetric null — preregistration

Date: 2026-09-26.

## Question

Can the globally valid symmetric-null tangent from v15.63 be realized as D X_rho[h] for an explicit normalized differentiable source vector field X, with a locally positive finite source update?

## Frozen states and hidden direction

Use the same 12 asymmetric states.

Freeze one hidden tangent h to the Hilbert-Schmidt normalized XXX Pauli string:

    h = (X tensor X tensor X) / sqrt(8).

This has zero proper one- and two-body marginals.

## Frozen global symmetric-null target

For each base state rho, use the v15.63 minimum-norm simultaneous lift Y_rho satisfying

    one-body derivative(Y_rho) = 0
    delta C_e(Y_rho) = O_e I/sqrt(3),  e=0,1,2.

No response quantity is used to choose Y.

## Explicit source vector field

Define the scalar hidden coordinate around the base point

    a_rho(sigma) = Tr[h (sigma-rho)] / Tr[h^2].

Define

    X_rho(sigma) = a_rho(sigma) Y_rho.

Because Tr(Y_rho)=0, X is trace preserving as a tangent field. It is Hermiticity preserving. At sigma=rho,

    X_rho(rho)=0
    D X_rho[h]=Y_rho.

This field is base-point-local; covariance/universality is NOT claimed.

## Finite source update

Use the explicit affine local flow

    T_t(sigma) = sigma + t X_rho(sigma).

Freeze hidden probe eta = 1e-4 and source amplitudes

    t in {1e-4, 3e-4, 1e-3}.

For sigma = rho +/- eta h require T_t(sigma) positive semidefinite and trace one at all frozen amplitudes.

## Measurements

For every state:

1. verify D X[h]=Y analytically and by centered finite difference;
2. verify Y is nonzero and has the v15.63 simultaneous symmetric-null retained targets;
3. verify the polar-skew projection of its retained correlation derivative is zero;
4. verify finite T_t positivity and normalization for rho +/- eta h;
5. directly compute the four-corner mixed polar-rotation response under T_t and require effective rotational rank zero against a positive skew-sector parent scale.

## Verdicts

SOURCE_VECTOR_FIELD_NULL_REALIZED
SOURCE_VECTOR_FIELD_NULL_FALSIFIED
INVALID

Frozen tolerances:
- lift/derivative relative residual <= 1e-10;
- trace/Hermiticity <= 1e-12;
- minimum finite-state eigenvalue >= -1e-12;
- projected symmetric-null / positive parent scale <= 1e-10;
- mixed rotational effective rank zero at 1e-9,1e-10,1e-11.

## Interpretation boundary

Success is an existence counterexample: a normalized differentiable locally positive source update can access a hidden global coordinate and generate nonzero globally compatible retained leakage while producing zero rotational response.

It does not establish covariance, locality, composition laws, physical naturalness, or a preferred source law. Those are stronger constraints and remain open.
