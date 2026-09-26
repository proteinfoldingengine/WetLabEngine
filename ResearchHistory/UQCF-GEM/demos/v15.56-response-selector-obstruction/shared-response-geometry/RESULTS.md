# v15.60 Shared response geometry — COMPLETE

Date: 2026-09-26.

## Verdict

`SHARED_GEOMETRY_MEASURED`.

All 12 frozen asymmetric states passed at filter source amplitudes 0.0685, 0.137, and 0.274. Both exponential and filter maps remained rank nine. All source-activity, non-closure, state-identity, finite-value, artifact-integrity, and rank controls passed.

Every state was classified **amplitude-stable overlap** by the preregistered descriptive rule.

## Main observation

The filter-law response subspace is extraordinarily stable under a four-fold source-amplitude range, while remaining distinctly separated from the exponential-law subspace.

Across all 12 states:

- minimum filter-vs-filter principal cosine across amplitude pairs: **0.9999433985309807**;
- maximum filter amplitude projector drift: **0.017629865781449173**;
- exponential-vs-filter center-amplitude projector distance: **0.6405042321948122–0.8460604814216868**;
- exponential-vs-filter minimum principal cosine at center amplitude: **0.9289480365879007–0.9577807541948985**.

Thus the source-law difference is not plausibly explained by the arbitrary finite filter amplitude used in v15.59: the filter subspace moves very little when source strength is halved or doubled, whereas its separation from exponential tilt is much larger.

## Average-projector spectrum

For each state, the eigenvalues of

[
P_*=(P_{exp}+P_{filter})/2
]

show nine large values near one and nine complementary small values near zero. At center amplitude the ninth large eigenvalue is **0.9644740182939506–0.9788903770974492** across the ensemble.

This is the continuous signature expected from two close but non-identical rank-nine subspaces. It should not be converted post hoc into an integer “intersection dimension”: for generic distinct finite-dimensional subspaces the exact algebraic intersection may be smaller even when all principal angles are small.

## Map-level structure remains law dependent

Although row spaces are close and amplitude stable, the actual normalized maps are not scalar copies. The exponential-filter scalar-fit residual remains approximately **0.203–0.289** at center amplitude, and changes only weakly over the amplitude sweep.

The evidence therefore separates:

1. a stable shared response subspace candidate;
2. source-law-specific weighting/orientation within and near that subspace.

## Reproducibility

- Branch: `research/v15.60-shared-response-geometry`.
- Preregistration: `b04517fd47789ca89ace4993d3b9a76c3f2652ff`.
- RED run: [36273753713](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273753713), expected missing-implementation failure.
- Tested implementation: `9fb33ec8fdd3449f8cde28cc80c3189c57cf42b9`.
- GREEN run: [36273795454](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273795454), job `108492548718`.
- Tests: pass.
- Full three-amplitude measurement: pass.
- Saved-artifact verification: pass.
- Artifact: [10916775441](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273795454/artifacts/10916775441).
- Artifact ZIP SHA-256: `3a1ede28821590dcfb8895ca6a80d4b6770b909f90f3a51a687ae49b156a1eb9`.

## Interpretation

The strongest earned statement is now:

> On the frozen asymmetric ensemble, two structurally different non-closed source laws generate full rank-nine hidden/source responses whose source-domain subspaces strongly overlap. The filter-law subspace is stable over a four-fold finite source-strength range, while the residual separation from exponential tilt is much larger than amplitude drift.

This is a candidate source-class invariant, not yet a universal one.

## Next discriminator

A third source law should now be used only if it is structurally independent enough to test the candidate invariant. Repeating another positive filter-like law would add little.

The better next step is a **source-class theorem/search**: characterize the first-order mixed response of a general differentiable normalized source update (T_s(\rho)) in terms of its Fréchet derivative with respect to hidden completion, and identify which part of that derivative determines the rank-nine row-space projector. Then use a third law chosen from a different derivative class as a theorem-directed falsification test.

That moves the program from empirical accumulation toward first-principles classification.
