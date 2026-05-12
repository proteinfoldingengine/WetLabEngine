# V309F — Regime-repair sweep before ablation

## Question
Can we find a nondegenerate regime for the reachability-law component tests where the full score is interpretable?

## Hypothesis
If the harness is repairable, then a 2D sweep over severity and base_failure/intercept/noise will produce at least one regime with:
- bad_rate in [0.20, 0.40]
- trigger_rate > 0.05
- score variance > 0
- enough positive bad cases

Only then should component ablation be interpreted.

## Method
Run a fixed-seed sweep over severity, base_failure, and noise_scale. For each candidate regime, compute:
- bad_rate
- adaptive_rate
- trigger_rate
- AUC
- balanced_accuracy
- accuracy
- mean_A_norm
- min_A_norm
- score_mean
- score_var
- phase_counts
- validity_gate

If and only if a valid regime is found, run a small held-out component ablation there.

## Controls
- Fixed seeds
- Shared simulation code across sweep points
- No threshold tuning after validation
- No regime selection outside the target bad-rate window
- Full sweep reported, not only the closest regime

## Results
- The experiment will print numerical results and save them to `runs/V309F/V309F_results.json`.
- If no valid regime is found, the decision is `branch`.

## Interpretation
This is a harness/regime-failure repair test, not a component-law claim.

## Failure / Caveat
- Do not interpret ablation if the validity gate fails.
- Do not pick a regime merely because it is closest.
- Do not overclaim GR-adjacent meaning.

## Decision
branch if no valid regime is found; otherwise continue to held-out ablation.

## Next
Smallest useful next test: if a valid regime is found, run held-out component ablation there; otherwise redesign the harness again.