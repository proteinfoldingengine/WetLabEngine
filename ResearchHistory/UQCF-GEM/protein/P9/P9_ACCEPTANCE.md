# Protein P9 — Final Retained-Coherence / State-Completeness Falsifier

**Status:** preregistered before P9 implementation or result exposure.

**Parent head:** `1908dad8cb7b0e4512298842bc44636a470fb35b`

## Program purpose

P9 is the final scientific continuation gate for the protein/WetLabEngine program.

It does **not** ask whether generic history dependence exists in protein dynamics. Non-Markovianity, reaction coordinates, history-augmented state models, folding funnels, contact order, and local preorganization all have substantial prior art.

The only remaining program-level hypothesis worth testing is narrower:

> A native-blind retained multiscale coherence state carries transferable information about future structural realizability that is not already contained in the instantaneous reduced state, elapsed optimization time, or simple generic history.

P9A is an archival predictive falsifier. No new folding trajectories are authorized unless P9A passes.

## Frozen source packet

Use only the canonical frozen v9 verification traces/results already present in this repository:

- 1UAO traces — Git blob `95bf84ad9d19ee84533190787889bb1d1420c330`
- 1UAO results — Git blob `2768ccbad6c694282a689bba799d14d65c0bb0d7`
- 1L2Y traces — Git blob `819e8cecda27ba4248b64288de88d672c7b705bc`
- 1L2Y results — Git blob `aa3565a2a597ef93ba81d3d9d078cf452f29edbb`

Only rows with `mode == bridge_patch_v9` are eligible.

## Prediction instances

For each target/seed, use current checkpoints at completed steps:

`100, 200, 300, 400`.

The future checkpoint is the next archived checkpoint:

- 100 -> 200
- 200 -> 300
- 300 -> 400
- 400 -> 499

Step 0 may be used only to construct prior-history features for the step-100 instance.

The evaluation label is future Kabsch C-alpha RMSD change:

[
y_t = RMSD_{future} - RMSD_t
]

Lower is more favorable. RMSD is evaluation-only and may never appear in predictor features.

## Frozen model families

All models must use the same deterministic ridge-regression implementation, fixed alpha `1.0`, train-only standardization, and intercept.

### M0 — instantaneous state

Features:

- normalized step = step / 500
- energy
- instantaneous `sigma_bridge`
- instantaneous `closure_ready`
- instantaneous `rg`

### M1 — ordinary-history control

M0 plus:

- energy change from the immediately previous archived checkpoint
- Rg change from the immediately previous archived checkpoint

This is the required generic history/time control.

### M2 — retained-coherence candidate

M1 plus exactly four frozen retained-coherence features, computed from archived checkpoints strictly **before** the current checkpoint:

- mean prior `sigma_bridge`
- mean prior `closure_ready`
- slope of prior `sigma_bridge` versus normalized step
- slope of prior `closure_ready` versus normalized step

No other bridge observable, coefficient search, window search, nonlinear transform, feature selection, or target-specific tuning is permitted.

## Native-information firewall

Predictor construction must not read:

- current RMSD;
- future RMSD;
- native contacts;
- native torsions;
- native coordinates;
- result-table metrics.

Those quantities may be read only when constructing the post-feature evaluation label.

A test must show that replacing every RMSD value in the input traces leaves every predictor matrix byte-for-byte identical.

## Transfer design

The primary test is leave-one-target-out transfer, in both directions:

1. train on all eligible 1UAO instances and evaluate on all eligible 1L2Y instances;
2. train on all eligible 1L2Y instances and evaluate on all eligible 1UAO instances.

No seed-wise random split is a primary result because adjacent checkpoints from the same trajectory are dependent.

Primary loss: RMSE of the frozen future-RMSD-change label.

Secondary diagnostic: Pearson correlation between prediction and label.

## Permutation falsifier

For each transfer direction, compute the observed test-RMSE improvement:

[
\Delta = RMSE(M1)-RMSE(M2).
]

Generate exactly 2,000 deterministic null replicates using seed `20260918`.

Within each training target, independently permute the four retained-coherence columns across instances **within current-step strata** while leaving M1 features and labels unchanged. Fit M2 on each permuted training matrix and score the untouched held-out target.

One-sided empirical p-value:

[
p=(1 + \#\{\Delta_{null} \ge \Delta_{obs}\})/(2001).
]

## P9A GO rule

Return `GO_RETAINED_COHERENCE_TRANSFER_SIGNAL` only if **all** are true in **both** transfer directions:

1. M2 RMSE is at least 10% lower than M1 RMSE;
2. observed retained-coherence improvement `Delta > 0`;
3. permutation p < 0.05;
4. M2 Pearson correlation exceeds M1 correlation;
5. native-information firewall passes;
6. source blob identities and matrix cardinalities pass.

Otherwise return:

`NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL`.

## Consequence

A P9A NO-GO closes the remaining protein/WetLabEngine scientific continuation hypothesis. Do not rescue it by changing history windows, adding observables, tuning ridge alpha, substituting targets, selecting checkpoints, or changing the label after exposure.

A P9A GO does **not** establish a novel folding mechanism. It only authorizes P9B: a new preregistered matched-present-state / divergent-history prospective experiment with stronger prior-art controls and causal intervention.

## Claim boundary

P9A can establish only that the frozen retained bridge/coherence history contains transferable predictive information beyond the specified instantaneous and ordinary-history baselines in these two archived small-protein systems.

It cannot establish de novo folding, a fundamental law, physical non-Markovianity, or novelty over the protein-folding literature.
