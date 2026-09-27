# v15.89 — weakest qubit transmission bounds Choi entanglement

The frozen gate returned **WEAKEST_DIRECTION_NEGATIVITY_BOUND_CONFIRMED** and **NEGATIVITY_BOUND_SHARPNESS_CONFIRMED**, with `all_valid: true`. All three tests, 22 exact symbolic checks and 25 frozen channel rows passed. No implementation repair or criterion change was needed.

For any qubit CPTP channel with affine Bloch action r -> T r+t, let delta=s_min(T) and let J be its input-first Choi matrix normalized to trace 2. Then

    N(J/2) <= delta/2.

Here N is the sum of absolute negative eigenvalues of the normalized Choi state's input partial transpose. The constant is sharp for every delta in [0,1], including nonunital equality examples. This quantifies v15.88's exact-erasure result: arbitrarily small transmission can preserve entanglement, but this Choi negativity must become small with the weakest transmission.

## Why the statement is universal

The proof in [DERIVATION.md](DERIVATION.md) applies to an arbitrary real T and any admissible translation t, not just the measured examples. For a unit vector n, put F=diag(1,-1,1), H=I-2nn^T and A=HF. Since A is proper orthogonal, B=J(TA,t) is positive: it represents the original CPTP channel precomposed with a unitary. With G=J^Gamma_input,

    G-B = ((Fn).sigma)^T tensor ((Tn).sigma),
    ||G-B||op = ||Tn||.

Thus lambda_min(G)>=-||Tn||. A two-qubit partial transpose has at most one strictly negative eigenvalue, giving N(J/2)<=||Tn||/2. Choose a weakest right singular vector n. Translation cancels from the comparison exactly; no assumption of unitality or CP of a truncated surrogate enters.

The certificate verifies all 13 independent affine coefficient equations in canonical coordinates, one exact squared-norm identity, and eight Bell eigenvector equations for a sharpness family. The finite rows audit the implementation and inherited native matrices. They do not replace the analytic proof.

The one-negative-eigenvalue ingredient is established literature, reviewed in [Rana (2013)](https://arxiv.org/abs/1304.6775), which attributes the two-qubit result to Sanpera, Tarrach and Vidal (1998). The limited literature check does not establish priority for this particular inequality. No novelty claim is made.

## Frozen numerical evidence

All evaluations used 80-digit full-complex arithmetic. All 25 original and comparison channels passed CPTP validity. Each channel used its own numerically recomputed weakest right singular vector, including rank-zero and degenerate cases. The direct-coordinate comparison, proper input rotations, spectra, state positivity and antipodal trace distances all passed the frozen tolerances.

| Family | Rows | Normalized Choi negativity | Relation to bound |
|---|---:|---|---|
| Inherited native exact-erasure channels | 6 | Numerical zero | Bound zero |
| Inherited soft family T=L/2+epsilon cof(L) | 4 | epsilon/4 | Half the ceiling for epsilon>0 |
| T=((1+epsilon)/2)L+epsilon cof(L) | 7 | epsilon/2 | Attains ceiling |
| Native amplitude damping, q=1-gamma | 5 | q/2 | Attains ceiling, including nonunital rows |
| Depolarizing alpha=0.25,0.5,1 | 3 | 0,0.125,0.5 | Slacks 0.125,0.125,0 |

The seven saturation amplitudes were 0, 1e-6, 1e-4, 0.01, 0.25, 0.5 and 1. At epsilon=1e-6 the negativity was 5e-7, compared with 2.5e-7 for the inherited fixed-plane family. The five damping parameters were gamma=0,0.25,0.5,0.75,1. Their weakest transmission was q=1-gamma and negativity q/2. The exact formulas in DERIVATION establish equality for the continuous families; these finite samples corroborate them.

Largest affine/comparison residual: 2.75e-80 (rounded upward). Largest parent/archive discrepancy: 7.38e-81. Largest expected spectrum/delta discrepancy: 8.44e-81. Largest equality-family attainment residual: 6.07e-81. Largest weakest-axis distance error: 4.22e-81. Every PT had at most one eigenvalue below -1e-40.

The minimum recorded bound slack was about -6.06e-81, and the minimum tested state eigenvalue about -5.27e-81. These are 80-digit roundoff well within the preregistered -1e-40 positivity/bound allowance, not scientific violations. Raw eigenvalues and signed slacks are retained. No clipping was used for classification and no threshold was adjusted after measurement.

## Exact execution provenance

- Branch: `research/v15.89-weakest-direction-entanglement-bound`.
- Certified parent: `8419150d3a8309a247d29ae9cfac337ca0f87b6a`.
- Preregistration, derivation, tests and workflow: `ff79a640ea126d105cfe157181ab02f11243bf7e`.
- Expected RED: [run 36358635443](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36358635443), job `108731253011`, artifact `10945015956`. Setup succeeded; the explicit absent-implementation assertion failed.
- RED ZIP SHA-256: `762c8cb69570cda9720dd36e2a46e290ca8d131cf5034fcbf6b9f163dffc82a9`.
- Tested implementation: `db2711aa012aed6391ea1df28d20b64619b61e46`.
- GREEN: [run 36358816645](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36358816645), job `108731766940`, [artifact 10944876892](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36358816645/artifacts/10944876892).
- GREEN ZIP SHA-256: `5e858941ee69a601faf28e987fb6f3323bbd651957c3be2b137c005a1ee8ed4d`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `760442f2d460af344aa9b1d6d8b1a0305894d301c1e1fddfd90d1cc478fb373c`.

Both exact job logs and downloaded ZIPs were inspected. Archive digests, execution heads, frozen document/test bytes and tested implementation bytes were verified. Every GREEN SHA256SUMS entry matched; parsed scientific JSON in the exact job log matched the downloaded artifact JSON. SHA256SUMS retains the artifact filename `result.json`; the same bytes are published as `RESULT.json`. [EVIDENCE.json](EVIDENCE.json) records machine-readable provenance. Documentation is a subsequent additive commit; no merge to main.

## Interpretation boundary

This is a qubit-channel bound on the entanglement of its normalized Choi state. It is not a quantum-capacity formula, a diamond-distance estimate, or a claim here about negativity for every arbitrary input/reference state. Positive weakest transmission does not force entanglement: the full-rank alpha=0.25 depolarizing control has zero negativity. The bound is an attainable ceiling, not a unique response law.

This work conditionally studies retained maps as qubit channels. It does not identify a physical source law, establish that every retained geometric map must be a channel, or show that a source acting on a state changes the admissible worlds. The original polar-skew source-selection problem remains open. No gravity law has been derived; Genesis Pin and historical verdicts remain intact. No fundamental time, foundational fitting, external alignment trick or dark-matter primitive was introduced.
