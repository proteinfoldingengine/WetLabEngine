# V309E — Regime repair gate before ablation

## Question
Can we find a nondegenerate regime for component ablation where the full score is interpretable?

## Hypothesis
If the harness is repaired, a 2D sweep over severity and base_failure/intercept/noise will produce at least one regime with:
- bad_rate in [0.20, 0.40]
- trigger_rate > 0.05
- score variance > 0
- enough positive bad cases

Only then should component ablation be interpreted.

## Method
Run a fixed-seed sweep over severity, base_failure, and noise_scale. For each candidate regime compute:
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

If a valid regime is found, run held-out component ablation there. If not, report no valid regime found and branch.

## Controls
- Fixed seeds
- Shared simulation code across sweep points
- No threshold tuning after validation
- No regime selection outside the target bad-rate window
- Full sweep reported, not only the closest regime

## Results
To be filled by execution.

## Interpretation
Inside the toy, only a regime satisfying the validity gate can support component interpretation.

## Failure / Caveat
If no valid regime is found, the failure is a harness/regime failure, not a law failure.

## Decision
branch unless a valid regime is found

## Next
If valid regime found, run held-out component ablation there; otherwise redesign harness again.