# v15.62 Symmetric-leakage null — preregistration

Date: 2026-09-26.

## Purpose

Falsify or support v15.61 Theorem 2 with an explicit retained-observable perturbation.

The test does not introduce a purported physical source law. It isolates the exact mathematical layer that v15.61 claims controls rotational visibility.

## Frozen states

Use the 12 v15.58 asymmetric states, candidate indices:
13,16,22,25,27,29,37,39,46,50,66,77.

## Construction

For each state and each edge, let the regular polar decomposition of the connected correlation matrix be

    C_e = O_e P_e.

Use six fixed Hilbert-Schmidt orthonormal symmetric 3x3 basis matrices H_a: three diagonal directions and three symmetric off-diagonal directions.

Construct retained mixed-correlation leakage columns

    delta C_{e,a} = O_e H_a.

These columns are nonzero by construction and satisfy exactly

    O_e^T delta C_{e,a} - delta C_{e,a}^T O_e = H_a - H_a^T = 0.

Thus they are explicit nonzero retained-observable leakage in the polar-symmetric null.

As a positive control use the three fixed skew basis matrices K_b and

    delta C^+_{e,b} = O_e K_b,

for which the O_e-skew projection is 2 K_b and spans so(3).

## Measurements

For every state and edge:

1. leakage Frobenius norms;
2. O_e-skew projected norms;
3. Sylvester-solved rotational tangent W;
4. numerical rank of the six-column symmetric-null response;
5. numerical rank of the three-column skew-positive response.

The symmetric-null rank is evaluated against a parent scale taken from the positive-control rotational map, not self-scaled numerical residue.

## Frozen criteria

- all symmetric leakage columns must have norm > 0.5;
- maximum symmetric projected norm / positive parent scale <= 1e-12;
- symmetric rotational effective rank = 0 at cuts 1e-9, 1e-10, 1e-11;
- positive control rank = 3 on every edge;
- all states remain on regular positive polar stratum.

Verdicts:

- SYMMETRIC_LEAKAGE_NULL_CONFIRMED
- SYMMETRIC_LEAKAGE_NULL_FALSIFIED
- INVALID

## Interpretation boundary

Success confirms the observable-projection part of the v15.61 factorization for an exact constructed sector. It does not demonstrate that a physically motivated normalized global source law naturally realizes this sector. A later lift to a global source vector field would be a separate existence problem.
