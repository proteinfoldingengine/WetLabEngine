# V309 — Component Ablation Test

## Question
Which components inside the adaptive reachability law contribute the most to prediction and intervention behavior?

## Hypothesis
Ablating one component should degrade discrimination if that factor carries unique information.

## Method
Fixed-seed toy simulation, held-out evaluation, fixed D_c threshold, no tuning.

## Controls
seeds=0..19, train_size=400, test_size=800

## Results
{
  "version": "V309",
  "title": "Component ablation of the reachability law",
  "config": {
    "seeds": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19
    ],
    "n_steps": 60,
    "A_c": 0.527,
    "D_c": 0.0388,
    "train_size": 400,
    "test_size": 800
  },
  "baseline": {
    "bad_rate": 0.015,
    "phase_counts": {
      "bad": 12,
      "safe": 788
    }
  },
  "results": {
    "A_full": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    },
    "no_rf": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    },
    "no_cw": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    },
    "no_be": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    },
    "no_dr": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    },
    "no_rv": {
      "AUC": 0.5,
      "balanced_accuracy": 0.5,
      "accuracy": 0.985,
      "mean_bad": 0.0,
      "mean_safe": 0.0,
      "corr": 0.0,
      "train_auc": 0.5,
      "train_balanced_accuracy": 0.5,
      "trigger_rate": 0.0
    }
  },
  "ranking_by_test_auc": [
    [
      "A_full",
      0.5
    ],
    [
      "no_rf",
      0.5
    ],
    [
      "no_cw",
      0.5
    ],
    [
      "no_be",
      0.5
    ],
    [
      "no_dr",
      0.5
    ],
    [
      "no_rv",
      0.5
    ]
  ]
}

## Interpretation
Ablations can be compared by test AUC and balanced accuracy; lower scores indicate a more necessary component.

## Failure / Caveat
If scores cluster tightly, the composite may be redundant or the toy labels may be too easy.

## Decision
continue

## Next
Stress the weakest component under noisy and sparse topology variants.