# 16.12 — Continuous signed normal response

Completed 2026-09-28. **CONTINUOUS_SIGNED_NORMAL_RESPONSE_CERTIFIED.** All validity controls passed for all 144 frozen physical path families. Retaining singular-value magnitude preserves a continuous sixth-edge matrix response and its signed first derivative. The Gram derivative discards the normal component, while the leading normal energy discards its sign.

This is a positive result about information retention in explicitly defined observables. It does not turn the old polar readout into a continuous transport, derive a source law, or establish gravity.

## What was tested

16.09–16.11 showed that the canonical unweighted polar extraction develops source-dependent boundary values even though the physical state varies smoothly. Here the observable is explicitly changed to its magnitude-weighted product U|C|=C. That identity is standard matrix algebra, not a newly discovered physical law. The scientific question is what response information survives in the continuous matrix and what is lost by replacing it with CᵀC.

The source, normalized physical states and channel paths remain exactly those of 16.11. Their sixth-edge matrices are

`C(s,λ)=C+s(V0+λV1)+s²(W0+λW1+λ²W2)`.

There are 12 archived candidates, three inherited binary middle-channel parameters, two preparation arms and two orders: 144 families. All were retained without exclusions or fitting. The source coherence ranges over −1≤λ≤1 and mixture strength over 0≤s≤1.

## Exact results

An explicit rational coefficient bound gives

`||C(s,λ)−C||F ≤ s Bv+s² Bw`

uniformly across the entire coherence interval. Here Bv is the sum of the entrywise absolute sums of V0 and V1, and Bw is the corresponding sum for W0,W1,W2. Thus C approaches the same baseline continuously, including joint approaches with s→0 and varying λ. This conclusion applies to C, not to the unweighted polar extraction.

With baseline support projectors P,Q held fixed, the projected normal displacement is

`K(s,λ)=(I−P)C(s,λ)(I−Q)=s λ N+ + s² M(λ)`.

All 144 exact families satisfy this identity with N+≠0. Therefore K tends to zero while its signed first derivative K/s tends to λN+. Continuity does not erase the first-order directional information.

| Preparation | Normal rank k | Families |
|---|---:|---:|
| Plane | 1 | 72 |
| Isotropic | 1 | 54 |
| Isotropic | 2 | 18 |

All 72 order pairs share exactly the same baseline and satisfy N_before=a N_after. Consequently the first-order normal ordering contrast is λ(1−a)N_after:

- All **48 nonidentity pairs** have a nonzero contrast coefficient (1−a)N_after. Their first-order contrast is nonzero for every λ≠0.
- All **24 identity-middle pairs** have zero contrast, and their entire ordered path polynomials coincide.
- At λ=0, the first-order normal contrast vanishes even in the nonidentity cases. Higher-order terms remain separately archived.

The equal normalized polar boundary values found in 16.09 therefore do not imply absence of ordering information in the underlying continuous matrix amplitude.

## What squaring loses

For H=CᵀC, the derivative is CᵀV+VᵀC. Here N=λN+ is the normal component at the chosen coherence. All 144 exact tests show that replacing V by V−N leaves it unchanged: the Gram derivative is blind to the normal component because CᵀN=NᵀC=0. Tangential coherence or ordering response may remain; this is not a claim that the whole Gram response vanishes.

The full normal-energy polynomial is

`KᵀK=s² λ² N+ᵀN+ + s³ λ(N+ᵀM+MᵀN+) + s⁴ MᵀM`.

Its leading term is even in λ and loses the source sign. The full finite polynomial need not be even; every higher-order coefficient is preserved in the raw result. The synthetic control diag(2,+s,0) versus diag(2,−s,0) has identical Gram matrices but distinct matrix responses, demonstrating sign loss exactly.

## Numerical execution and controls

[Successful targeted GitHub run 36496955303](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36496955303), job 109178656444, executed scientific commit **`88109eeb3e7f60f73f433f5e0ed33938c943e205`**. Five new tests and six parent tests passed, followed by the complete audit.

There are **3,456 numerical rows**: 144 families × three coherence values (−1,0,+1) × two strengths (2^-8,2^-64) × two precisions (80,120 digits) × two inherited frames. Each row contains the finite connected matrix, its SVD magnitude-weighted reconstruction, K/s, KᵀK/s², and all descriptive deviations. Exact finite ranks determine support; no singular-value threshold, regularization or determinant correction is used.

| Control | Maximum residual |
|---|---:|
| Weighted polar reconstruction | 3.0102e-84 |
| Polar identities / positive factor | 3.3535e-80 |
| Full normal-displacement identity | 1.2941e-66 |
| Full normal-energy identity | 4.1669e-69 |
| Gram first-order normal blindness | 2.6224e-88 |
| Frame covariance | 1.2815e-66 |
| Uniform-bound violation | 0 |
| Cross-precision discrepancy | 1.2941e-66 |

Thresholds were frozen at 1e-35 within precision and 1e-30 across precision. All passed.

| Maximum over all sampled cases | s=2^-8 | s=2^-64 |
|---|---:|---:|
| Distance of C(s,λ) from baseline | 2.321047e-5 | 3.221183e-22 |
| Exact coefficient upper bound, numerically evaluated | 3.299784e-5 | 4.579176e-22 |
| Error of K/s from λN+ | 7.300809e-8 | 1.013191e-24 |
| Error of KᵀK/s² from λ²N+ᵀN+ | 3.339094e-10 | 4.633887e-27 |

These maxima need not belong to the same case. No fitted convergence law or finite-step pass criterion was used; the exact polynomial identities provide the proof.

Preregistration commit `d4615a4a5364b6a3fba5a7422deb82998dea55e8`, [RED run 36496625063](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36496625063), failed the five expected absent-implementation controls. Local test development corrected an expanded-versus-factored polynomial comparison before measurement; no scientific input or criterion changed. Independent pre-measurement review passed all tests and found no blockers.

## Complete published evidence

The full raw `result.json` is **19,446,793 bytes**, losslessly compressed to **1,907,732 bytes** in [result.json.xz](result.json.xz). It contains every exact input coefficient, projector, normal block, rank, rational bound, complete energy polynomial, order contrast, numerical matrix and control. It is not a summary or an expiring Actions-only artifact.

- [EVIDENCE.json](EVIDENCE.json): source head, run/artifact identities, hashes, metrics and counts.
- [PUBLICATION_CHECK.json](PUBLICATION_CHECK.json): independent projector, polynomial, contrast and record-completeness checks.
- [verify_publication.py](verify_publication.py): reproduces those checks using column-space bases instead of the audit pseudoinverse routine.
- [PREREGISTRATION.md](PREREGISTRATION.md), [DERIVATION.md](DERIVATION.md), [REVIEW.md](REVIEW.md), source manifest, code and tests.
- Complete `job.log`, `test.log`, `parent-test.log`, `audit.log`, and RED logs.

Decode with `xz -dk result.json.xz`, verify with `sha256sum -c SHA256SUMS`, then run `python verify_publication.py`. `SHA256SUMS-xz` verifies the compressed bytes. The artifact ZIP digest and the decoded source/result hashes were checked before publication.

## Interpretation and next question

The response is not absent: amplitude and sign survive in the continuous sixth-edge matrix. The singular polar boundary came from normalizing newborn directions to unit magnitude. Squaring is smooth but loses specific directional information. This establishes a concrete readout tradeoff, not a preferred geometry by decree.

The original five-edge readout remains distinct and its previous null result is unchanged. The sixth-edge source response remains conditional on the specified CPTP source family. Time is pruning / ordered recoverability update; s is not fundamental time. No external alignment, fitted completion, dark-matter primitive, physical clock or gravity correspondence is introduced.

A next bounded question is whether a closed-loop observable constructed from the full continuous edge matrices retains this signed ordering response in a frame-invariant quantity, or whether composing around a loop removes it. Such a test must explicitly define the observable and its nulls; the present result does not assume that a continuous matrix is already a geometric connection.
