# V309E — Seed-sensitive harness repair test with narrow calibration sweep

## Question
Can the harness produce one valid regime when seeds are actually varied and the scoring metric is computed correctly?

## Hypothesis
If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
A fixed-seed sweep was run with:
- seeds: 0–19
- n_steps: 60
- A_c: 0.527
- D_c: 0.0388
- A_h: 0.1
- severity_grid: [0.3, 0.32, 0.34, 0.36]
- base_failure_grid: [0.08, 0.1, 0.12, 0.14]
- noise_grid: [0.0, 0.01]

The run reported:
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
- fixed seeds
- actual seed passed into the simulation
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- full sweep reported
- no regime selection outside the validity gate

## Results
- `chosen_regime`: `null`
- `note`: `no valid regime found`

Run-level `validity_gate`:
- `enough_positive_cases`: `false`
- `nondegenerate_bad_rate`: `false`
- `nonzero_score_variance`: `false`
- `nonzero_trigger_rate`: `false`
- `valid_for_interpretation`: `false`

Selected sweep outputs:
- severity 0.3, base_failure 0.08, noise 0.0:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - trigger_rate: 0.0
  - D_A: 0.0
  - duration_below_Ac: 0.0
  - horizon_area: 0.0
  - horizon_width: 0.0
  - pinch: 0.0
  - mean_A_norm: 0.7672835238340817
  - min_A_norm: 0.6852989406268641
  - score_mean: 0.7672835238340817
  - score_var: 0.0006339052101931765
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.3, base_failure 0.1, noise 0.01:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - trigger_rate: 0.0
  - D_A: 0.0
  - duration_below_Ac: 0.0
  - horizon_area: 0.0
  - horizon_width: 0.0
  - pinch: 0.0
  - mean_A_norm: 0.7504492483991925
  - min_A_norm: 0.6242943545593486
  - score_mean: 0.7504492483991925
  - score_var: 0.0015474073153165235
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.34, base_failure 0.14, noise 0.01:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - trigger_rate: 0.0
  - D_A: 0.0
  - duration_below_Ac: 0.0
  - horizon_area: 0.0
  - horizon_width: 0.0
  - pinch: 0.0
  - mean_A_norm: 0.7054492483991925
  - min_A_norm: 0.5792943545593485
  - score_mean: 0.7054492483991925
  - score_var: 0.0015474073153165242
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.36, base_failure 0.14, noise 0.01:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - trigger_rate: 0.0
  - D_A: 0.0
  - duration_below_Ac: 0.0
  - horizon_area: 0.0
  - horizon_width: 0.0
  - pinch: 0.0
  - mean_A_norm: 0.6834492483991925
  - min_A_norm: 0.5572943545593486
  - score_mean: 0.6834492483991925
  - score_var: 0.0015474073153165235
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

Other listed regimes also had:
- `bad_rate = 0.0`
- `trigger_rate = 0.0`
- `valid_for_interpretation = false`

## Interpretation
This is a harness/regime failure inside the toy system.

No valid regime was found, so the run does not support interpretation of any ablation or component behavior. The per-regime scores varied numerically, but the run-level validity gate still failed, so those values are not interpretable as evidence for the law stack.

Inside the toy, the current harness still does not produce a usable regime for component testing.

## Failure / Caveat
- No valid regime was found.
- `chosen_regime` remained `null`.
- `valid_for_interpretation` was false.
- `bad_rate` was 0.0 in the reported sweep points.
- `trigger_rate` was 0.0 in the reported sweep points.
- `AUC` was 0.5 in the reported sweep points.
- The run does not justify component-level conclusions.

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to find a regime with nonzero bad cases and nonzero trigger activity before attempting any component ablation.