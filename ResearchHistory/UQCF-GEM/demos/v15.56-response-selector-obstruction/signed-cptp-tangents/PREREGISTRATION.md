# v15.80 preregistration — signed CPTP tangent extensions

Frozen before gate.py exists or any new scientific measurement.
Parent 659c078f47f1b6732c310701bd3fd4170787fc43.
Branch research/v15.80-signed-cptp-tangents; folder signed-cptp-tangents.
Historical source and verdicts remain untouched.

## Frozen measurement

Implement DERIVATION.md's full global extension. Enumerate source supports
nonempty by size then lexicographic subset; input/output supports include
empty then the same ordering. Canonical local coefficients are unscaled
scalar/delta/epsilon, epsilon_123=+1. Source coordinates are raw Paulis;
input/output coordinates are all 64 HS-normalized Paulis, lexicographic.
Compute local Lie-algebra multiplicities for all eight scalar/vector triples,
then full 117 tensors and 110 trace-annihilating tensors. Separate by source
support. For every one of 63 raw source Paulis, form each full generator's
Choi matrix, project with P=I-|vec(I)/sqrt(8)><vec(I)/sqrt(8)|, stack its real
and imaginary entries, and take the coefficient SVD within each support.
No retained-only zero extension is used for the physical classification.

Project the resulting coefficient kernel to the certified 18 coupling
coordinates, and measure Q/E on all 12 frozen states and all 63*27 source/
hidden basis pairs. Candidate indices:
[13,16,22,25,27,29,37,39,46,50,66,77]. No reselection or random seed.
Use thresholds [1e-9,1e-10,1e-11] times each matrix's leading singular value.
Kernel projectors use the middle threshold 1e-10. Report exact global ranks
as sums over disjoint source-support blocks; do not square condition numbers
by deriving nullities from a Gram eigendecomposition.

Freeze the physical even-source control a=(ZII+XXI)/sqrt(2), epsilon=.1,
and the two explicit hidden witnesses YYZ and XXX divided by sqrt(8).
Unitary curve checks use U=cos(epsilon/2)I-i sin(epsilon/2)P_a for each of
63 source Paulis and both signs of epsilon. Parameters label source updates,
not fundamental time. Use exact formulas, no finite differences or fitting.

## Validity checks (failure => both verdicts INVALID)

- Frozen selector identity and inherited M.domain valid for all references.
- Local analytic tensors agree with local Lie-kernel projectors <=1e-10;
  kernel residual <=1e-12. Global tensor coefficient Gram equals its
  analytic diagonal (product of local squared tensor norms) <=1e-10.
- All source-support blocks are independent; output identity row is zero
  for every admitted trace-annihilating tensor, <=1e-12.
- Every basis Choi Hermiticity and output-partial-trace error <=1e-12.
  Complex transport retained. Fast PTM-to-Choi reshuffle agrees with the
  independent matrix-unit Choi builder <=1e-12 for every basis tensor at
  the first lexicographic source Pauli of its support and for the control.
- Analytic Hamiltonian coefficient vectors reconstruct direct -i[P/2,z]
  on all64 input basis elements for every63 sourcePauli within1e-12 maximum
  absolute error. Their conditional Choi norms <=1e-12. No requirement
  that a finite Euler map I+epsilon L be CP is imposed.
- The projection to the 18 retained tensors agrees with direct full-map
  retained/hidden blocks for all63 sources within1e-12 max absolute error.
- All126 unitary curves have unitarity <=1e-12 and Choi CP/TP diagnostics
  min eigenvalue >=-1e-12, Hermiticity/TP error <=1e-12.
- Inherited analytic Q/E Sylvester residual <=1e-11. Full-map Hamiltonian
  response at all source/hidden inputs agrees with projected tensor assembly
  within1e-12 coefficient error; the inherited v15.79 direct Q/E assembly
  check <=1e-10. No geometry is evaluated at a singular output state.
- Even-source control: a Hermiticity, a²=I, D(-a)=D(a), both explicit
  retained witness errors <=1e-12; D's trace-annihilation/Hermiticity
  residuals <=1e-12. K(D) eigenvalues equal [0 repeated63,8] within1e-11,
  and K(-D) minimum eigenvalue equals -8 within1e-11. Its epsilon=.1
  channel passes the above CP/TP tests; reversed-strength Choi remains
  Hermitian/TP within1e-12 and has min eigenvalue <=-.1 (intentional NO).
  Original D retained rank12, aggregate Q/E rank6, and each responding edge
  (1,2),(2,0) Q/E rank3 at every frozen state; source edge(0,1) Q/E norm
  <=1e-12 times full-map norm. Rank thresholds as above.
- All recorded numeric values finite. Unexpected implementation exceptions
  fail CI; repair only defects, never the frozen criterion.

## Primary signed-CP classification gate

Local multiplicities for triples 000,001,010,011,100,101,110,111 are
[1,0,0,1,0,1,1,1] at all thresholds. Full dimension117; trace-annihilating
110, with blocks [11,11,11,17,17,17,26]. Conditional-Choi constraint rank
103, nullity7; each source-support block has exactly one kernel direction
at all thresholds. Its kernel projector agrees with the canonical
Hamiltonian coefficient projector within1e-9.
YES: SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_CONFIRMED.
NO: SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_NOT_CONFIRMED.

## Separate retained image and observability gate

The seven-dimensional conditional-Choi kernel projects to rank4 in the
18-dimensional retained coupling space at all thresholds. Its image projector
agrees within1e-9 with the four canonical patterns: one per two-site source
support (two tied one-cross coefficients), and one three-site source support
(three tied one-body-output coefficients). The seven canonical Hamiltonian
columns, measured on the stacked12-state Q and E maps, have rank4 at all
thresholds; their right-kernel projector agrees within1e-9 with the three
local-source coefficient coordinates. Individual state ranks are diagnostics.
YES: SIGNED_CPTP_RETAINED_IMAGE_FOUR_CONFIRMED.
NO: SIGNED_CPTP_RETAINED_IMAGE_FOUR_NOT_CONFIRMED.
Validity failure overrides both as INVALID. Tests allow scientifically valid
NOs; green CI does not itself imply a positive verdict.

## Execution and publication

Publish this file, DERIVATION.md, tests and workflow with gate.py absent.
Inspect the expected GitHub RED before implementing. Run GREEN, read exact
logs and downloaded artifact JSON, verify execution SHA and checksums, then
publish lossless results with exact SHAs/run/job/artifact IDs. No criterion
changes after measurement. No merge to main.
