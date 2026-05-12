# V310E — Narrow calibration repair test

## Question
Can the harness produce one valid regime when the regime window is narrowed and the scoring metric is computed correctly?

## Hypothesis
If the harness is repaired, then at least one narrow seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
Run a narrow seed/regime sweep with:
- actual varying seeds passed into `simulate_regime(sev, bf, nz, seed=seed)`
- a smaller parameter window than the previous sweep
- only regimes near the smallest plausible failure boundary
- a correct AUC implementation if labels are nondegenerate
- omission of AUC if labels are degenerate and AUC would be meaningless

Suggested narrow sweep shape:
- severity_grid: 1–3 values around the previous failure boundary
- base_failure_grid: 1–3 values around the previous boundary
- noise_grid: 1–2 values
- seeds: a compact set such as 0–7
- n_steps: the minimum needed for validity checking

The run must report:
- chosen_regime
- bad_rate
- adaptive_rate
- AUC
- balanced_accuracy
- accuracy
- trigger_rate
- rescued
- harmed
- horizon_area
- horizon_width
- pinch
- mean_A_norm
- min_A_norm
- score_mean
- score_var
- late_K
- late_mobility
- late_residual
- phase_counts
- validity_gate

## Controls
- actual varying seeds
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- compact seed-wise summary
- no claim escalation
- all numbers grounded in stdout or saved JSON

## Results
To be filled by the next run.

## Interpretation
To be filled by the next run.

## Failure / Caveat
To be filled by the next run.

## Decision
branch

## Next
Smallest useful next test: run a narrower calibration sweep around the previous boundary and verify whether any regime produces nonzero bad cases and nonzero trigger activity.

## Guardrail Reminder
If the new sweep still yields `chosen_regime = null`, stop and report a harness failure. Do not ablate components.