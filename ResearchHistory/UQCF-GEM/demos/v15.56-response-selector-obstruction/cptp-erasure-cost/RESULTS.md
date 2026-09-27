# v15.87 — exact erasure has an unavoidable CPTP distortion cost

The frozen measurement returned **ERASURE_COST_BOUND_ATTAINED**, **OPTIMAL_ERASURE_TRANSLATION_RIGID**, and **OPTIMAL_ERASURE_DISTINGUISHABILITY_CONFIRMED**, with `all_valid: true`. Three tests passed. All six new exact symbolic checks and the inherited thirteen-coefficient spin-flip certificate passed. No scientific criterion or amplitude changed after preregistration.

## Universal statement and attained bound

Let L be the certified rank-two partial isometry with singular values (1,1,0), P=L^T L, and K=I-P. Consider all affine qubit CPTP maps r -> T r+t satisfying exact erasure TK=0. Retained-plane distortion, output orientation, and translation are otherwise unrestricted.

The proof in [DERIVATION.md](DERIVATION.md) gives

    ||T||_* <= 1,
    ||T-L||op >= 1/2,
    ||T-L||F >= 1/sqrt(2).

Both distortion bounds have the same unique affine minimizer: **T=L/2 and t=0**. This is not a scan restricted to scalar multiples of L. Exact erasure gives rank(T)<=2; v15.85's spin-flip argument reduces the necessary CP condition to the unital part; its Bell eigenvalues bound the sum of surviving singular values by 1. Norm duality and its equality conditions then establish optimality and uniqueness over the entire stated class. An exact Choi-kernel argument forces the optimal translation to vanish.

The norms are explicit diagnostic objectives, not a derived physical selection principle. No optimizer, fitted amplitude, or claim that a physical source minimizes these norms is used.

## Inherited-loop evidence

The unchanged candidate-46 loop at 80-digit precision attains the predicted costs:

| Quantity | Measured value |
|---|---|
| Nuclear norm of T* | 1 |
| Operator-norm distortion | 0.5 |
| Frobenius distortion | 0.7071067811865475244 |
| Unnormalized Choi spectrum | (0, 0.5, 0.5, 1), within 3.59e-81 |
| Kernel-erasure residual | 2.45e-81 |
| Measure-and-prepare reconstruction error | 1.77e-81 |

The minimum computed Choi eigenvalue was approximately -3.58e-81, within the frozen -1e-40 tolerance. No eigenvalues were clipped. The equal mixture of two measure-and-prepare channels reproduces the optimal channel on all four matrix units. Consequently this particular optimal map is entanglement breaking, including for arbitrary ancillas, by its explicit construction.

All three tested retained-plane antipodal pairs have input trace distance 1 and output trace distance 0.5. Their positive-input outputs differ from the formal L outputs by trace distance 0.25. The kernel pair's output distance is approximately 1.34e-81 (numerical zero). Maximum distance-identity error was 4.22e-81. The formula T*=L/2 extends these conclusions to every direction in the retained plane; the three pairs are numerical controls.

These numbers have different meanings: 0.5 is distinguishability between two optimal-channel outputs; 0.25 is distance between an optimal-channel output and its formal target output. Neither is a diamond-norm claim.

## Frozen controls

The isotropic ladder alpha=(0,0.25,0.5,0.75,1) gave (CPTP,CPTP,CPTP,NON_CP,NON_CP), with spectrum-formula errors at most 4.22e-81.

| Unequal retained strengths (a,b) | CPTP | Operator distortion | Frobenius distortion |
|---|---|---|---|
| (0.75,0.25) | Yes | 0.75 | sqrt(10)/4 |
| (1,0) | Yes | 1 | 1 |
| (0.25,0.25) | Yes | 0.75 | 3sqrt(2)/4 |

These controls show why the universal result must not be phrased as requiring every channel to halve both directions: some channels preserve one direction more strongly at the expense of the other. Equal halving is the unique optimum for the two frozen distortion objectives.

At the optimum, all six shifts +/-0.1 along the three coordinate axes were NON_CP, with minimum Choi eigenvalues approximately -0.00493324, -0.00266097, and -0.00480532 for the respective axis pairs. Zero shift was CPTP. Universal translation rigidity follows from the exact kernel proof, not these six samples.

Inherited affine synthetic controls passed. Parent comparison error was 5.28e-81; affine identity errors were at most 3.96e-82; anisotropic formula errors were at most 6.44e-81. Tested state Hermiticity and trace errors were zero. The smallest state eigenvalue, -2.90e-81, was within the frozen numerical tolerance. These residuals are roundoff, not scientific failures.

## Exact provenance

- Branch: `research/v15.87-cptp-erasure-cost`.
- Certified parent documentation: `3b1c4d29db91b2bfac7f6fe447de131671fd9206`.
- Preregistration/tests commit: `b95fd7d520e32fc10095ee547642ed0f758ef637`.
- Expected RED: [run 36355650537](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36355650537), job `108722730060`, artifact `10943696576`. All setup steps passed; tests stopped at the explicit absent-implementation assertion.
- RED ZIP SHA-256: `fc0cac28b7977e6c92c99eede7aabce7a2f15de9f3f17ea164b47ebf30a79fe6`.
- Tested implementation: `c8069c5066ca0e6188796ebbd16fa47835572b6a`.
- GREEN: [run 36355858560](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36355858560), job `108723324207`, [artifact 10943726742](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36355858560/artifacts/10943726742).
- GREEN ZIP SHA-256: `aa2739b82cf47cd9221b6164c5477ea9b384dcfd919546b18baac64feb030018`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `4167a743c5e2da6fa0de9a00e3a2cf56778286eb58dbee4e2cb31a807dbb5c66`.

Exact logs and downloaded artifacts were inspected. ZIP hashes, execution heads, frozen source bytes, and all GREEN SHA256SUMS entries were verified. Scientific verdicts were read from the result JSON. SHA256SUMS uses the artifact filename `result.json`, published here byte-for-byte as `RESULT.json`. Documentation follows the tested implementation in a separate additive commit. Theorem and implementation review found no important defects.

## Interpretation limits and remaining question

v15.86 showed that exact isometric retention forces a unitary completion that supplies the missing direction. v15.87 quantifies the unavoidable distortion when exact erasure is instead retained. It does not establish that geometric transport must be a CPTP qubit channel, or select an extraction functor or physical source law. The result is conditional mathematical structure, not a derivation of gravity or a mechanism that changes admissible worlds.

Entanglement breaking was established here for the unique optimal map through its measure-and-prepare construction. Whether it is forced for every exact-erasure qubit CPTP map, independent of these norm objectives and including nonunital maps, remains outside this gate. That is a sharper subsequent structural question than retuning the optimum.

No fundamental time, external alignment, heuristic foundational fit, or dark-matter primitive was introduced. Genesis Pin and all historical scientific verdicts remain unchanged. No merge to main.
