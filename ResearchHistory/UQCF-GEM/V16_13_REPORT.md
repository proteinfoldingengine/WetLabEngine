# UQCF-GEM 16.13 — final gauge-content report

Completed 2026-09-28. **LOCAL_NORMAL_SIGN_GAUGE_CLASSIFIED.** All five new tests, five parent tests, exact controls and 576 high-precision numerical rows passed in [targeted run 36499944642](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36499944642).

The continuous response from 16.12 contains invariant amplitude information, but its local sign is not uniformly invariant:

| Local baseline-response pair | Cases | Finding |
|---|---:|---|
| Rank-one baseline | 90 | A proper endpoint rotation leaves C fixed and reverses N. No invariant of this local pair distinguishes the signs. |
| Rank-two baseline | 54 | A determinant coefficient distinguishes signs under SO(3), but its normalized sensitivity is only 5.3194e-15 to 1.4944e-14 and vanishes at the rank-one boundary. |
| All cases under the larger O(3) group | 144 | An orthogonal sign-flip witness exists. |

All 48 nonidentity order pairs retain unequal invariant normal-amplitude coefficients; all 24 identity pairs coincide. The actual normal derivative λN vanishes at zero coherence. This is a classification of (C,N), not a proof of equivalence of full physical paths or neighboring-edge data.

The small orientation witness is mathematically exact but does not supply a rank-boundary-stable physical canary. No singular values were truncated, and no small cofactor was divided out to manufacture robust orientation information.

[Read the complete report](demos/v15.56-response-selector-obstruction/local-gauge-content/RESULTS.md), including the derivation, exact spectral bound, raw [result archive](demos/v15.56-response-selector-obstruction/local-gauge-content/result.json.xz), [execution provenance](demos/v15.56-response-selector-obstruction/local-gauge-content/EVIDENCE.json), tests, independent verification and full logs. The raw result is 3,311,171 bytes, compressed losslessly to 344,204 bytes.

Scientific head: `1a9d5d80f80385af2ba1771cadd21c5a4f8f976b`. The independent verifier checked all 144 stabilizers, determinant pencils and full physical determinant polynomials, all 72 order pairs and all 576 numerical keys.

The revised [16.13–16.15 brief](V16_13-15_BRIEF.md) is now grounded in this result. **16.13 is complete; 16.14 and 16.15 have not been measured.** The next question is whether intrinsic neighboring-edge information allows a closed-network invariant to retain the signed normal response, or whether the contraction cancels it. Only after that test comes controlled physical interpretation.

The source remains specified, not derived. Time is pruning / ordered recoverability update. No external alignment, physical clock, dark-matter primitive, curvature or gravity derivation is asserted. Work is published on a research branch, not merged into main.
