# UQCF-GEM 16.09–16.11: final research report

Completed 2026-09-28. All three targeted research audits passed their scientific validity controls. Full reports, code, exact results, numerical records, checksums and execution logs accompany this report in Git. The initial 16.11 implementation failure is preserved separately as INVALID.

**Main finding:** changing the order of the two frozen channel operations does not change their one-sided boundary polar limit, but changing the allowed source coherence does. No single continuous extension of this polar readout at the common baseline can agree with both source approaches. The complete coherence family has three fixed-parameter boundary classes.

## What the project is trying to determine

The research asks which features of an effective geometric description are actually determined by retained quantum information and lawful operations on it, and which features enter through a supplied source, readout or completion rule. A feature cannot be called intrinsic merely because one chosen implementation produces it.

The preceding 16-series audits localized the ordering response to the sixth edge, which the original five-edge readout omitted. That edge's connected correlation matrix lies outside the old polar domain. Actual CPTP channel paths then showed that activating the source creates new supported directions. The underlying quantum states remain valid and vary smoothly; the singularity arises when the readout converts arbitrarily small nonzero singular values into unit polar directions.

These three loops asked, in sequence: do the physical paths have well-defined one-sided limits; do the two orderings select the same limit; and is that limit independent of the allowed source choice? Each question was frozen before its measurement. No source was selected to obtain a desired downstream gravitational result.

## Results

| Loop | Question and result | Complete evidence |
|---|---|---|
| 16.09 | All 144 paths have certified one-sided limits; all 72 order pairs agree exactly for the fixed source. | [Full report](demos/v15.56-response-selector-obstruction/boundary-polar-limits/RESULTS.md) · [Raw result](demos/v15.56-response-selector-obstruction/boundary-polar-limits/result.json.xz) |
| 16.10 | Reversing source coherence changes the limit in every one of 144 paired cases with the same baseline. The exact gap is 2√k. | [Full report](demos/v15.56-response-selector-obstruction/source-reversal/RESULTS.md) · [Raw result](demos/v15.56-response-selector-obstruction/source-reversal/result.json.xz) |
| 16.11 | All 144 families have a symbolic classification for the entire coherence interval. Zero coherence keeps baseline rank; positive and negative coherence select opposite new polar contributions. | [Full report](demos/v15.56-response-selector-obstruction/coherence-family/RESULTS.md) · [Raw result](demos/v15.56-response-selector-obstruction/coherence-family/result.json.xz) |

For a baseline connected matrix C, let P and Q be its column- and row-support projectors. The source-dependent normal block is N=(I−P)V(I−Q), where V is the path derivative. Write r=rank(C), k=rank(N+) and Uc=polar(C), Un=polar(N+). Exact rank saturation establishes the one-sided limit, rather than relying on a finite-step extrapolation.

| Fixed coherence λ | Certified limit as source mixture s↓0 | Gap from Uc |
|---|---|---:|
| Positive | Uc+Un | √k |
| Zero | Uc | 0 |
| Negative | Uc−Un | √k |

The table holds for both orders. The 144 families comprise 72 planar cases (r=1,k=1), 54 isotropic cases (r=2,k=1), and 18 isotropic cases (r=1,k=2). All candidates and identity-middle controls are included. The zero-coherence conclusion uses exact polynomial-rank checks, not merely a zero first-order normal block.

The family is physically admissible: Eλ,s is the convex mixture of the identity and Ad(U±), where U±=(ZI±XX)/√2, with weights 1−s, s(1+λ)/2 and s(1−λ)/2. All are nonnegative for 0≤s≤1 and −1≤λ≤1. Physical inputs use the explicit normalization established in 16.08; historical raw binary inputs remain preserved in that parent record.

## What this resolves and what it leaves open

Order agreement is established within each fixed source class. Source independence is disproved for this canonical boundary readout: two actual admissible paths with the same baseline have different certified limits. Labeling a path by its source would distinguish them, but that label is extra information, not a source law derived from the common baseline.

The result concerns the canonical polar partial isometry, including zero on its kernel. No determinant correction is used, and some full-rank limits have negative orientation. This is not an automatic SO(3) transport or a derivation of curvature. It does not prohibit smooth state observables, other explicitly specified readouts, or richer descriptions.

The 16.11 classification is for each fixed λ followed by s↓0. Uniformity in λ, interchange of limits, and a unique joint limit are not asserted. Some exact binary residues make the asymptotic neighborhood extremely small; the numerical grids display this rather than hiding it with rank thresholds or fits.

The source family remains specified, not derived from retained consistency. Time is pruning / ordered recoverability update; s is a channel-mixture parameter, not fundamental time. No physical clock, dark-matter primitive, Einstein/ADM correspondence or universal source law is supplied. Pillar 3 remains open.

## Execution and reproducibility

| Loop | Executed scientific head | Successful GitHub run | New / parent tests | Exact records | Limit rows | Finite rows |
|---|---|---|---:|---:|---:|---:|
| 16.09 | `b8bfa7cd3abf99884b6627ab2a42d0fa035154be` | [36492791730](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36492791730) | 5 / 6 | 144 | 576 | 1,440 |
| 16.10 | `1e9a5e8029e53b09998f99b122a9df3324178b1b` | [36493793738](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36493793738) | 4 / 5 | 144 paired | 576 paired | 1,728 |
| 16.11 | `12e477696c361f919c9c947db24503e9ac64153d` | [36495025125](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36495025125) | 6 / 4 | 144 families | 1,728 | 2,592 |

Every numerical audit used 80/120 digits and both inherited frames. Exact algebra controls support and polynomial ranks. Independent post-run verification used column-basis projectors and exact minors and checked record completeness. Each stage includes its preregistration, RED evidence, implementation review, SHA-256 manifest, complete logs and artifact provenance. `verify_publication.py` reproduces the independent checks after decoding the raw file.

16.11's first implementation [run 36494592601](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36494592601) was INVALID due to a singular-matrix determinant bug in the pinned numerical library. The corrected implementation only changes determinant recording to a division-free 3×3 formula. An exact reproducer, regression test, original failed code/results/logs and independent re-review are published. It is not counted as a successful scientific run.

The raw JSON files are losslessly compressed, not truncated or replaced by summaries:

| Loop | Original bytes | Published .xz bytes |
|---|---:|---:|
| 16.09 | 4,613,515 | 427,444 |
| 16.10 | 5,003,210 | 474,064 |
| 16.11 | 7,209,898 | 565,672 |

These files fit comfortably in Git and do not depend on expiring workflow artifact downloads. In any result directory, decode `result.json.xz` with `xz -dk result.json.xz`, check `sha256sum -c SHA256SUMS`, and run `python verify_publication.py`. The targeted workflow records the pinned execution environment. To reproduce a measurement rather than verify its archived output, use that loop's executed scientific commit.

## Next research decision

The baseline-only canonical polar extension route is now obstructed by an explicit physical source family. A bounded next test would ask whether a continuous, explicitly specified observable that retains singular-value magnitude preserves the useful response information, or whether the intended readout fundamentally requires a source/approach label. Such a test would change the readout question openly; it would not repair this polar boundary by choosing a hidden completion or derive a physical source. No 16.12 measurement is included in this delivery.
