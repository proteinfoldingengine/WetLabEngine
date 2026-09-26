# v15.69 Local-frame covariance of the symmetric-null construction — preregistration

Date: 2026-09-26.

## Question

Does the v15.64/v15.68 symmetric-null source-vector construction survive arbitrary local quantum-frame changes, or was the counterexample an artifact of the preferred Pauli frame?

This is a covariance test. It does not yet test source uniqueness, composition, or selection from a physical source generator.

## Frozen objects

Use all 12 v15.58 asymmetric full-rank states.

For each base state rho:
- hidden tangent h = X⊗X⊗X/sqrt(8);
- minimum-Hilbert-Schmidt-norm global lift Y_rho from v15.63/v15.64:
  - zero one-body derivative;
  - delta C_e = O_e I/sqrt(3) on all three edges;
- local source vector field
  X_{rho,h}(sigma) = a_{rho,h}(sigma) Y_rho,
  a = Tr[h(sigma-rho)]/Tr[h^2].

Freeze eta=1e-4 and t=1e-3 for the finite covariance probe.

## Local frame ensemble

Generate 8 deterministic independent local SU(2)^3 frames with NumPy seed 20260969.

Each local SU(2) is generated response-blind from a normalized four-dimensional Gaussian quaternion q=(w,x,y,z), mapped to

    U = w I - i(x X + y Y + z Z).

The three-qubit frame is U0⊗U1⊗U2.

No frame is selected or rejected after measurement.

## Covariance identities

For every base state and every frame U, form

    rho' = U rho U†
    h'   = U h U†
    Y_transport = U Y_rho U†.

Independently recompute the minimum-norm lift Y_{rho'} from the transformed state using the unchanged v15.63 algorithm.

Primary lift-covariance criterion:

    ||Y_{rho'} - Y_transport||_F / ||Y_transport||_F <= 1e-9.

Also verify the induced SO(3) edge polar rotations:

    O'_ij = R_i O_ij R_j^T

to Frobenius residual <=1e-10 on every edge.

Verify transformed target covariance:

    delta C'_ij = R_i delta C_ij R_j^T

to relative residual <=1e-9.

## Vector-field covariance

For hidden signs ie=±1 and source signs jt=±1, define

    sigma = rho + ie eta h
    T = sigma + jt t X_{rho,h}(sigma).

Transform it directly:

    U T U†.

Independently construct with transformed inputs:

    sigma' = rho' + ie eta h'
    T' = sigma' + jt t X_{rho',h'}(sigma').

Require

    ||T' - U T U†||_F <= 1e-11

for every sign pair, state, and frame.

Also require transformed finite states remain trace-one and positive with minimum eigenvalue >= -1e-12.

## Null preservation

For the independently recomputed Y_{rho'}, require the analytic polar-skew projection

    O_e'^T delta C_e' - delta C_e'^T O_e'

to have norm / ||delta C_e'|| <=1e-10 on every edge.

## Verdicts

LOCAL_FRAME_COVARIANT_NULL_CONFIRMED
LOCAL_FRAME_COVARIANT_NULL_FALSIFIED
INVALID

Confirmation means the symmetric-null counterexample is not a preferred-Pauli-frame artifact.

It does NOT establish:
- a unique or physically selected source law;
- covariance when h is held fixed instead of transformed as part of the source data;
- composition/atlas naturality;
- global finite-amplitude positivity beyond the local affine neighborhood.
