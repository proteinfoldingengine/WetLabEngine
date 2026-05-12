# V309 — Component Ablation of the Reachability Law

## Question
Which components inside the adaptive reachability law contribute to prediction and intervention behavior?

## Hypothesis
If the toy law stack is compressive, then removing a real contributing component should reduce discrimination or trigger behavior relative to the full score.

## Method
Fixed-seed toy simulation across seeds 0–19 with `n_steps = 60`, `train_size = 400`, `test_size = 800`, using:
- `A_full`
- `no_rf`
- `no_cw`
- `no_be`
- `no_dr`
- `no_rv`

Reported metrics:
- `AUC`
- `balanced_accuracy`
- `accuracy`
- `mean_bad`
- `mean_safe`
- `corr`
- `train_auc`
- `train_balanced_accuracy`
- `trigger_rate`

Baseline bad rate and phase counts were also reported.

## Controls
- Fixed seeds: 0–19
- Shared configuration across variants
- Held-out train/test split
- Same thresholds across all variants
- No threshold tuning

## Results
Baseline:
- bad_rate: 0.015
- phase_counts bad: 12, safe: 788

`A_full`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

`no_rf`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

`no_cw`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

`no_be`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

`no_dr`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

`no_rv`
- AUC: 0.5
- balanced_accuracy: 0.5
- accuracy: 0.985
- mean_bad: 0.0
- mean_safe: 0.0
- corr: 0.0
- train_auc: 0.5
- train_balanced_accuracy: 0.5
- trigger_rate: 0.0

Ranking by test AUC:
- `A_full`: 0.5
- `no_rf`: 0.5
- `no_cw`: 0.5
- `no_be`: 0.5
- `no_dr`: 0.5
- `no_rv`: 0.5

## Interpretation
Inside this toy run, the full reachability score and every one-component ablation were numerically identical on the reported classification and trigger metrics. The score carried no detectable predictive separation here: AUC, balanced accuracy, correlation, and trigger rate were all unchanged at degenerate values.

That means this run does not support component importance. It instead suggests the current setup was not informative for testing the internal law, or the score was effectively inactive under this configuration.

## Failure / Caveat
- `A_full` did not separate bad from safe states.
- Every ablation matched `A_full` exactly on all reported metrics.
- `mean_bad` and `mean_safe` were both 0.0 for all variants.
- `trigger_rate` was 0.0 for all variants.
- The tiny baseline bad rate (`0.015`) likely made this a weak test for ablation effects.

## Decision
freeze

## Next
Smallest useful next test: re-run ablation under a regime with non-degenerate bad-state frequency and verified trigger activity, then test whether any single component drops held-out AUC or intervention utility.