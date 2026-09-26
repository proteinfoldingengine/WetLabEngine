# Response quotient rank gate

Frozen before implementation.

For each of the same 11 base states, construct the linearization of the closed-form mixed response over:
- all 27 exact-weight-three Pauli hidden directions;
- all 9 one-body Pauli source directions;
- all 9 matrix entries of the loop-holonomy mixed response.

The resulting response matrix has 9 rows and 243 columns.

Use only the closed-form response construction. No response finite differences are allowed in the matrix columns.

For every fixture record singular values, numerical rank using relative threshold 1e-10, nullity, and quotient dimension.

Controls:
1. deterministic orthogonal basis changes in both input spaces must preserve rank and nonzero singular spectrum to relative tolerance 1e-8;
2. the previously tested hidden operator and collective Z source must reconstruct their existing closed-form response to relative error at most 1e-9.

Frozen adjudication:
- STRONG_COLLAPSE: every fixture rank is at most 3.
- PARTIAL_COLLAPSE: every fixture rank is below 9 and at least one is above 3.
- FULL_OUTPUT_RANK: at least one fixture has rank 9.
- INVALID: a covariance or reconstruction control fails.

No parameters may be fitted to the rank result. This gate measures only how much microscopic hidden/source ambiguity is invisible to the derived geometric response. It does not assert that Genesis identifies kernel-equivalent microscopic inputs.
