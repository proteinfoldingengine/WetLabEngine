# v15.58 Asymmetric held-out ensemble — preregistration

Date: 2026-09-26.

## Question

Does the v15.57 source-law contrast survive after removing the axial/cyclic symmetry of the original 11 fixtures?

The state selector is frozen **before any hidden/source response is evaluated**. Selection uses only positivity, edge conditioning, nontrivial loop geometry, and explicit asymmetry diagnostics.

## Candidate-state generator

Use the three-qubit Pauli expansion

[
\rho = \frac{1}{8}\left[
I + \sum_{q,a} m_{qa}\sigma_a^{(q)}
+ \sum_{(i,j),a,b} C_{ij}^{ab}\sigma_a^{(i)}\sigma_b^{(j)}
\right].
]

No three-body Pauli coefficient is included in the base state. Candidate coefficients are generated deterministically with NumPy `default_rng(20260928)`:

- one-body coefficients: iid normal, standard deviation 0.035;
- two-body coefficients on oriented edges (0,1), (1,2), (2,0): iid normal, standard deviation 0.055;
- add to each edge block a deterministic nonsymmetric baseline
  `diag(0.11,0.085,0.060)` plus off-diagonal entries `C[0,1]-=0.045`, `C[1,0]+=0.025`, with independent random perturbations above;
- candidate index is the RNG draw index and is immutable.

This generator is intentionally generic and non-cyclic; it is not fit to the response.

## Selector

Scan candidate indices 0 through 4999 and accept the first 12 satisfying every condition:

1. minimum state eigenvalue >= 0.025;
2. every oriented connected-correlation block has minimum singular value >= 0.020;
3. every polar rotation has determinant > 0 and regular positive polar factor;
4. loop holonomy angle >= 0.15 radians;
5. pair-block asymmetry: `max_{e>0} ||C_e-C_0||_F >= 0.06`;
6. one-body asymmetry: maximum pairwise Euclidean difference among the three local Bloch vectors >= 0.025;
7. no pair of accepted states has Frobenius distance < 0.02.

No response quantity, rank, singular spectrum of E, or source-law comparison may enter selection.

If fewer than 12 candidates pass, verdict is INVALID; do not change thresholds.

## Measurement

For every accepted state, reuse unchanged:

- 27 exact-weight-three hidden Pauli directions;
- 9 one-body Pauli source generators;
- normalized exponential-tilt derivative machinery from the historical v15.56 code;
- local-unitary control law from v15.57;
- hidden amplitude `ETA=1e-3`;
- unitary source amplitude `S=0.137`;
- parent-scaled rank cuts `1e-9,1e-10,1e-11`;
- marginal-closure tolerance `1e-11`;
- active-unitary-source threshold `1e-4`;
- local-unitary/exponential mixed norm ratio ceiling `1e-9`.

The exponential edge map must be measured directly on each new state; no original-fixture lookup is allowed.

## Outcomes

`ASYMMETRIC_SOURCE_SPECIFICITY_REPLICATED` if:

- all 12 selected states satisfy the frozen selector and controls;
- exponential mixed edge map is nonzero on all 12;
- local-unitary mixed edge map has effective rank zero on all 12 and ratio <= 1e-9;
- all nine local-unitary source generators are active on every state.

Rank nine is **reported, not required**. Its distribution is an outcome.

`ASYMMETRIC_SOURCE_SPECIFICITY_NOT_REPLICATED` if controls pass but the contrast fails.

`INVALID` for selector, provenance, regularity, finite-value, closure, activity, or artifact-integrity failure.

## Interpretation boundary

Replication would show that source-law specificity is not an artifact of the original axial/cyclic fixture family. It would not establish that exponential tilt is the physical source law, nor derive gravity, Einstein dynamics, or spatial dimension.

## Evidence

Save accepted candidate indices and base-state matrices, selection diagnostics, both raw 9x243 maps, unitary source activity, closure residuals, rank spectra, hashes, report JSON, and a verifier that recomputes the adjudication from saved arrays.
