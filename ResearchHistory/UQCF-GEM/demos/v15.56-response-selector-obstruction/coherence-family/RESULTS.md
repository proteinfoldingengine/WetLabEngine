# 16.11 — Three fixed-coherence boundary classes

**THREE_COHERENCE_BOUNDARY_CLASSES_CERTIFIED.** All 144 physical path families have exact symbolic certificates across the full coherence interval −1≤λ≤1. The zero-coherence path keeps its baseline rank in a neighborhood of s=0. Every fixed nonzero coherence adds k polar directions, with the sign selecting their orientation.

Let Uc=polar(C) and Un=polar(N+), with the canonical polar partial isometry zero on the kernel. Then, for each fixed λ,

| Coherence | One-sided limit as s↓0 | Limit rank | Distance from baseline polar |
|---|---|---:|---:|
| λ>0 | Uc+Un | r+k | √k |
| λ=0 | Uc | r | 0 |
| λ<0 | Uc−Un | r+k | √k |

The distance between positive and negative classes is 2√k. All 72 before/after pairs agree within each fixed coherence class. This includes the identity middle channel, where the entire ordered paths coincide.

## Exact continuum proof and physicality

The already-defined source family is Lλ=((1+λ)/2)L+ + ((1−λ)/2)L−. Eλ,s=I+sLλ has nonnegative normalized weights 1−s, s(1+λ)/2 and s(1−λ)/2 on the identity and the two unitary channels for the whole rectangle 0≤s≤1, −1≤λ≤1. Exact unitary/transfer checks and the explicit input positivity and normalization certificates passed.

For every case the connected matrix was constructed directly as C+s(V0+λV1)+s²(W0+λW1+λ²W2). Both endpoint polynomials match 16.10. The exact normal block satisfies N(λ)=λN+ with N+≠0. For every fixed λ≠0, common-plane coefficient identities or ambient dimension saturate the first-order rank lower bound r+k. The continuum claim is symbolic, not an extrapolation from a parameter grid.

At zero coherence, exact polynomial minors show rank(C(s,0))=r near the baseline. A nonzero baseline r-minor persists locally, while all larger minors vanish identically. Thus continuity of the constant-rank polar factor proves the zero-class limit. A vanishing first-order normal alone would not have justified it.

| Preparation | Baseline rank r | Normal rank k at λ=1 | Families | Zero-coherence polynomial rank |
|---|---:|---:|---:|---:|
| Plane | 1 | 1 | 72 | 1 |
| Isotropic | 2 | 1 | 54 | 2 |
| Isotropic | 1 | 2 | 18 | 1 |

## Numerical checks

The complete result contains 144 symbolic families, 72 order comparisons, 1,728 limit evaluations at λ=−1/2,0,+1/2 with 80/120 digits in both inherited frames, and 2,592 finite polar evaluations. Maximum class-gap residual is 8.434e-80, limit partial-isometry residual 2.443e-67, cross-precision discrepancy 1.529e-67, and finite covariance residual 1.287e-63. All frozen controls passed: 1e-35 within precision, 1e-30 across precision.

| λ | Max error at s=2^-32 | At s=2^-128 | At s=2^-192 |
|---|---:|---:|---:|
| −1/2 | ≈2 | 9.74705e-23 | 5.28388e-42 |
| 0 | 1.73286e-10 | 2.18717e-39 | 1.18567e-58 |
| +1/2 | ≈2 | 6.13539e-23 | 3.32600e-42 |

The finite grid is descriptive. Exact ranks, not numerical singular-value thresholds, determine support. Tiny stored baseline singular values explain why nonzero-coherence asymptotics can require very small s. No rate fit, convergence cutoff, determinant correction or arbitrary kernel frame was used.

Independent publication verification reconstructed the normal identities using column-basis projectors; checked every zero-coherence rank through exact minors, all 288 endpoint coefficient matches, all 72 order identities, and every expected numerical record key. The verifier is included as `verify_publication.py`.

## Execution and preserved failed attempt

Preregistered RED head `da2c1a90708c2376bd8be58420df3e131bda7855`, [run 36494298208](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36494298208), produced the five expected absent-implementation failures.

Initial implementation `2122ebd4972223d66504520003e5e4ae7f8453e5`, [run 36494592601](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36494592601), remains **INVALID**. After processing the symbolic candidates, it failed while recording a rank-one polar determinant: mpmath 1.3.0's LU determinant selected a None pivot and raised TypeError. The failure artifact, original code/tests, checksums and logs are preserved as `failed-*`; `FAILED_ATTEMPT.json` and `failed-file-map.json` identify them.

The regression fixture preserves exact internal mpmath numbers for the already-audited candidate22/a1/isotropic/after/native baseline polar at 80 digits. It reproduces the old error. The correction uses the ordinary division-free 3×3 determinant formula for that descriptive output. A RED/GREEN regression and independent review verified the fix. No scientific input, threshold, path or certificate changed.

[Successful targeted run 36495025125](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36495025125), job 109172476086, executed scientific head **`12e477696c361f919c9c947db24503e9ac64153d`**. Six new tests and four parent tests passed, followed by the complete audit. The full run logs are published.

## Complete evidence and scope

`result.json.xz` contains the full 7,209,898-byte raw result, compressed losslessly to 565,672 bytes. It includes every exact coefficient, normal block, rank certificate, numerical limit, finite polar matrix, density certificate and control. Decode with `xz -dk result.json.xz`; verify with `sha256sum -c SHA256SUMS`. `SHA256SUMS-xz` verifies the compressed bytes. `EVIDENCE.json` binds the run, execution head and artifact digest; `PUBLICATION_CHECK.json` records the independent checks. Protocol, derivation, source manifest, code, tests, reviews and failure evidence accompany the result.

These are fixed-λ limits followed by s↓0. No uniform convergence in λ, interchange of limits or uniquely defined joint limit is claimed. The physical density-state family is smooth in its parameters; the canonical polar extraction discards singular-value magnitude and acquires the discontinuous boundary classes.

The three loops show fixed-source order agreement without source independence. An intrinsic rule selecting a source remains unproved, and a smooth alternative observable would be a separate explicitly defined readout. No physical clock, source-emergence law, dark-matter primitive or gravity correspondence has been derived. Time remains pruning / ordered recoverability update.
