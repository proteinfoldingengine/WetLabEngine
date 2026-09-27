# v15.78 preregistration — source-free covariance

Frozen before gate.py exists or new numerical measurements are run.
Parent fdc9c239491d952672457e1ff994fbca7d4b4ed8.
Branch research/v15.78-source-free-covariance.
Folder source-free-covariance. No historical file or verdict is modified.

## Question and frozen inputs

Test the extra hypothesis and theorem in DERIVATION.md. Classify the full
64x64 Pauli commutant and the 36x27 retained/hidden block using all six
local X/Z conjugation characters. Independently enumerate all proper signed
axis permutations at each site (24 each), and their support orbits.
No random seed, fitting, threshold selection, or state reselection is used.
Use inherited frozen states with candidate indices
[13,16,22,25,27,29,37,39,46,50,66,77], all 27 normalized weight-3 hidden Paulis,
and the inherited 36 retained observables. State selector and source helpers
are imported from the exact certified parent tree.

For every reference use the three channels in DERIVATION.md:
active_symmetric (delta=.02, kappa=.01), unitary_XXI (angle=pi/4), identity.
Freeze calibration once per reference, before projection. Compare original
and covariance-projected channels; 12*3*2=72 response rows, each with 27
hidden probes. No finite differences or finite source amplitudes are used.
Evaluate Q and E at the original input reference with the inherited analytic
connected-correlation derivative and polar Sylvester equation.

## Validity controls (failure means INVALID)

- Exact frozen selector; reference domain inherited M.domain is valid.
- 64 orthonormal Pauli basis elements, 27 hidden and 36 retained.
- 24 distinct orthogonal determinant +1 signed permutations per site.
- Their adjoint representations preserve orthonormality; six X/Z characters
  agree with direct Pauli-matrix conjugation, all residuals <=1e-12.
- Transfer matrix conversion and reconstruction on all 64 matrix units for
  every original channel agree <=1e-12 in Frobenius norm, imaginary Pauli
  coefficients <=1e-12; source derivative uses Phi-id consistently.
- Every original and projected Choi matrix: min eigenvalue >=-1e-12,
  Hermiticity and TP error <=1e-12. Original null-channel preparations
  b±.01Y pass the inherited density checks (same 1e-12 tolerance).
- Analytic Sylvester equation residual <=1e-12.
- Before projection: active_symmetric retained norm >=.01, relative
  Q/leak <=1e-9 and E/leak <=1e-8; unitary retained rank 12 and Q/E rank 6
  at all rank thresholds [1e-9,1e-10,1e-11] times each matrix's largest
  singular value, retained norm >=1. Identity leakage/Q/E <=1e-12.
- Structural implementation self-check: independent finite group average
  agrees with support-sector projection <=1e-12 for deterministic dense
  test matrix D_ij=(((i+1)*(j+3)) mod 101-50)/101 and for every channel.
  Projection is idempotent <=1e-12. Its commutators with six generic local
  rotations (X angle pi/7, Z angle pi/5 per site) are <=1e-12.
- Every recorded numerical value finite. Unexpected programming exceptions
  fail CI; they must not be hidden as scientific evidence.

## Primary scientific gate

All 64 six-sign characters distinct; full Pauli-subgroup commutant dimension
64. Every one of 972 hidden-to-retained constraint Gram entries strictly
positive (exact integer test), hence block nullity zero. Axis-permutation
orbits number 8 with sorted sizes [1,3,3,3,9,9,9,27].
YES: SOURCE_FREE_COVARIANCE_FORCES_RETAINED_CLOSURE.
NO: SOURCE_FREE_COVARIANCE_CLOSURE_NOT_CONFIRMED.

## Separate channel erasure gate

For both active_symmetric and unitary_XXI at every reference, projected
retained norm <=1e-12 times original retained norm; projected Q/leak_before
<=1e-10 and E/leak_before <=1e-9. Using original matrix leading singular
values as references, projected retained/Q/E ranks are all zero at each
of [1e-9,1e-10,1e-11]. For original null Q/E matrices whose leading values
are near zero, use the original retained leading singular value instead.
Additionally the projected active_symmetric PTM equals depolarization
(diag(1,0,...,0)) within 1e-12 Frobenius norm.
YES: COVARIANTIZATION_ERASES_POSITIVE_AND_NULL_LEAKAGE.
NO: COVARIANTIZATION_ERASURE_NOT_CONFIRMED.
INVALID overrides both gates if any validity control fails.

Tests must accept a scientifically valid NO; CI success alone is not a YES.
Publish tests while gate.py is absent; inspect expected RED job. Then add
only the frozen measurement; run GREEN, inspect JSON, exact job logs and
artifact, publish full evidence and interpretation boundaries. No thresholds
or amplitudes may be changed after results. No merge to main.
