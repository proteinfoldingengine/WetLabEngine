# V309C — Regime redesign and nondegenerate component ablation

## Question
Can we put the reachability-law ablation into a non-degenerate regime where the full score has usable variance, enough bad cases, and a meaningful held-out component comparison?

## Hypothesis
If the harness is valid, then redesigning the regime toward a bad rate in the 0.20–0.40 range should produce nonzero score variance, nonzero trigger rate, and enough positive bad cases for component ablation to distinguish the full score from one-component ablations.

## Method
Run a fixed-seed toy simulation across 20 seeds with the same ablation harness, but add an explicit regime sweep over a small set of severity multipliers until the baseline bad rate lands in the target range. Then evaluate:
- `A_full`
- `no_rf`
- `no_cw`
- `no_be`
- `no_dr`
- `no_rv`

Report held-out and summary metrics:
- `bad_rate`
- `adaptive_rate`
- `trigger_rate`
- `AUC`
- `balanced_accuracy`
- `accuracy`
- `score_mean`
- `score_var`
- `mean_bad`
- `mean_safe`
- `corr`
- `phase_counts`
- `validity_gate`

## Controls
- Fixed seeds 0–19
- Shared configuration across variants
- Same train/test split for ablation metrics
- No threshold tuning after validation
- Regime sweep only to enter a non-degenerate bad-rate window

## Results
To be filled by the runnable harness.

## Interpretation
If the full score is still degenerate after regime redesign, the current harness is not informative enough for component ablation. If the score becomes non-degenerate and one or more component drops are detectable on held-out data, then the law stack gains compression and robustness inside the toy.

## Failure / Caveat
If bad rate remains outside 0.20–0.40, or if score variance/trigger rate stay at zero, then the ablation is not interpretable and the branch should remain open.

## Decision
branch

## Next
Smallest useful next test: execute the regime sweep and, only if valid_for_interpretation is true, interpret component ablation results; otherwise redesign the harness again.