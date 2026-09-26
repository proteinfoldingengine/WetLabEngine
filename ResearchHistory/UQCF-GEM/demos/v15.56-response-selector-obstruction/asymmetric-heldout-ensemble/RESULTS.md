# v15.58 Asymmetric held-out ensemble — COMPLETE

Date: 2026-09-26.

## Verdict

```
ASYMMETRIC_SOURCE_SPECIFICITY_REPLICATED
```

The v15.57 source-law contrast survives removal of the original axial/cyclic fixture symmetry.

Twelve states were selected before response measurement by the frozen deterministic generator and conditioning/asymmetry rules. Candidate indices were:

`13, 16, 22, 25, 27, 29, 37, 39, 46, 50, 66, 77`.

No response, rank, E-spectrum, or source-law comparison entered selection.

On all 12 held-out states:

- normalized exponential tilt mixed source-to-edge map rank = **9**;
- matched local-unitary mixed source-to-edge map effective rank = **0**;
- all **9/9** local-unitary source generators were active;
- all rank decisions were stable at the frozen 1e-9, 1e-10 and 1e-11 relative cuts;
- saved-artifact verification independently recomputed the verdict successfully.

Rank nine was an outcome, not an acceptance criterion.

## Symmetry was genuinely broken

Across the accepted states:

- pair-block asymmetry ranged **0.1755624226046246–0.3277526213369962**, versus the frozen minimum 0.06;
- local-Bloch asymmetry ranged **0.05326516738148017–0.1834344537961518**, versus the frozen minimum 0.025;
- loop holonomy angle ranged **0.5839526968873382–1.9615451794014807 rad**, versus the frozen minimum 0.15.

Thus this is not a near-cyclic perturbation selected at the boundary of the asymmetry criteria.

## Source-law contrast

Across the 12 states:

- `||E_exp||_F`: **386.1814738920642–535.4445116423748**;
- `||E_unitary||_F`: **8.225149591009977e-12–1.2684318121809554e-11**;
- `||E_unitary||_F / ||E_exp||_F`: **1.8593493772797414e-14–3.108845675323351e-14**;
- maximum proper-marginal closure residual: **1.1102230246251565e-16**.

The frozen unitary/exponential ratio ceiling was 1e-9 and the closure ceiling was 1e-11.

The result therefore replicates the mechanistic distinction established in v15.57: hidden global completion can feed the retained pair geometry under the normalized exponential tilt, while a retained-marginally closed local-unitary update using the same one-body generators does not transmit that hidden dependence.

## Reproducibility

- Branch: `research/v15.58-asymmetric-heldout-ensemble`.
- Preregistration commit: `6d5c3578f88d63d7f211bb64b81cc55844f77bdd`.
- RED head: `c444fa52b36863039876578663014b60dba29ba9`; GitHub run [36272998258](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36272998258) failed because `gate.py` was absent.
- Implementation/tested head: `3c3475face2da1e260a196a18323dc5be0be5cdd`.
- GREEN GitHub run: [36273048652](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273048652), job `108490507181`, completed SUCCESS.
- Tests, full 12-state measurement, saved-artifact verification, and evidence upload all passed.
- Artifact: [10915709031](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273048652/artifacts/10915709031).
- Artifact ZIP SHA-256: `151ee3e86c6f53125bbdaab6acee0aceaba8e0a9574af091e9e209da607fc8ac`.
- Extracted `report.json` SHA-256: `b7fdca87718db17a0c7f27676143bea28fb5466f4c90fdd15c44306eba66218c`.

The artifact ZIP digest was recomputed after download and matches GitHub.

## What is now earned

The source-law-specific hidden-completion response is no longer confined to the original axial/cyclic fixture family. In two materially different state ensembles, the same qualitative separation holds:

[
E_{\rm exp}\neq0,\qquad E_{\rm local\ unitary}\simeq0.
]

Moreover, the exponential edge image saturated all nine available edge-tangent coordinates on every state in both ensembles.

This does not make rank nine a theorem, nor establish a physical source law. It does make a simple “artifact of cyclic symmetry” explanation inconsistent with this held-out test.

## Interpretation boundary

Still not established:

- that normalized exponential tilt is physically preferred;
- that the response is gravitational;
- that a unique source law follows from first principles;
- Einstein dynamics;
- emergent spatial dimension from rank three;
- behavior at singular polar strata.

## Next bounded question

The next scientific bottleneck is no longer fixture symmetry. It is **source-law class**.

A useful next task is to classify source updates by whether they are retained-marginally closed. The v15.57 theorem gives one direction: autonomous retained evolution forces the hidden mixed response to vanish. The next nontrivial test is to introduce a second, independently defined **non-closed** source law—frozen without reference to the exponential result—and ask whether non-closure alone is sufficient for a nonzero response, and whether its nine-dimensional image aligns with or differs from the exponential image.

That separates:

1. generic consequence of violating retained-marginal closure,
2. special structure of normalized exponential tilt,
3. any candidate universality that could justify deeper physical interpretation.

No second non-closed source law has been tested in v15.58.
