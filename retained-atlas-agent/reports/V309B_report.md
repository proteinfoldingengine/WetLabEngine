# V309B — Regime Validity Check for Ablation

## Question
Are the reachability-law ablation metrics interpretable in a non-degenerate regime, or is the current harness still too sparse for component testing?

## Hypothesis
If the harness is valid, then the full score should show nonzero variance, nonzero trigger rate, and enough positive bad cases for ablation comparisons to be meaningful.

## Method
Fixed-seed toy simulation across seeds 0–19 with `n_steps = 60`, using the reachability score harness and a validity gate before any component interpretation.

Reported quantities:
- `bad_rate`
- `adaptive_rate`
- `trigger_rate`
- `AUC`
- `balanced_accuracy`
- `accuracy`
- `mean_A_norm`
- `min_A_norm`
- `score_mean`
- `score_var`
- `phase_counts`
- `validity_gate`

## Controls
- Fixed seeds: 0–19
- Shared configuration
- No threshold tuning
- Interpretation gated on regime validity
- Same toy harness across the run

## Results
- `bad_rate`: 0.02666666666666667
- `adaptive_rate`: 0.9733333333333334
- `trigger_rate`: 0.0125
- `AUC`: 0.75
- `balanced_accuracy`: 0.734375
- `accuracy`: 0.9858333333333333
- `mean_A_norm`: 1.0062339423221693
- `min_A_norm`: 0.07199132514077879
- `score_mean`: 0.00477540640768214
- `score_var`: 0.002048530535617192
- `phase_counts` bad: 32, safe: 1168

`validity_gate`:
- `nondegenerate_bad_rate`: false
- `nonzero_score_variance`: true
- `nonzero_trigger_rate`: true
- `enough_positive_cases`: false
- `valid_for_interpretation`: false

## Interpretation
Inside this toy run, the score was not completely inert: score variance was nonzero and trigger rate was nonzero. However, the regime was still too sparse for component ablation interpretation because the bad rate was low and the validity gate failed.

This supports classifying the run as a harness/regime failure, not as a meaningful law test.

## Failure / Caveat
- `bad_rate` was only 0.02666666666666667.
- `phase_counts` were heavily imbalanced: 32 bad vs 1168 safe.
- `valid_for_interpretation` was false.
- The run does not justify component-level claims.
- This is not a freeze condition because the gate failed but the branch is still informative.

## Decision
branch

## Next
Redesign the regime toward `bad_rate` in `0.20–0.40`, then rerun held-out component ablation in that regime.