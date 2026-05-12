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
Ran a fixed-seed sweep over:
- seeds: 0–19
- n_steps: 60
- A_c: 0.527
- D_c: 0.0388
- A_h: 0.1
- severity_grid: [0.25, 0.3, 0.35, 0.4, 0.45]
- base_failure_grid: [0.02, 0.05, 0.08, 0.11, 0.14, 0.17]
- noise_grid: [0.0, 0.03]

Reported for each candidate:
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

No ablation was run because no valid regime was found.

## Controls
- Fixed seeds
- Shared simulation code across sweep points
- No threshold tuning after validation
- No regime selection outside the target bad-rate window
- Full sweep reported, not only the closest regime

## Results
`chosen_regime`: null

`validity_gate`:
- enough_positive_cases: false
- nondegenerate_bad_rate: false
- nonzero_score_variance: false
- nonzero_trigger_rate: false
- valid_for_interpretation: false

Representative sweep outputs:
- severity 0.25, base_failure 0.02, noise 0.0:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - mean_A_norm: 0.8078889001340697
  - min_A_norm: 0.7882251967461206
  - score_mean: 0.8078889001340697
  - score_var: 0.001300034076770695
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.35, base_failure 0.02, noise 0.0:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - mean_A_norm: 0.7699267652327066
  - min_A_norm: 0.7471287477569254
  - score_mean: 0.7699267652327066
  - score_var: 0.0018464334445966353
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.40, base_failure 0.17, noise 0.03:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - mean_A_norm: 0.7397978786274366
  - min_A_norm: 0.7143964380612723
  - score_var: 0.0023489687559002446
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.45, base_failure 0.17, noise 0.03:
  - bad_rate: 0.0
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.5
  - balanced_accuracy: 0.5
  - accuracy: 1.0
  - mean_A_norm: 0.7207506110902901
  - min_A_norm: 0.6937641081769795
  - score_var: 0.0026977569870459133
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

No sweep point satisfied the validity gate.

## Interpretation
No valid regime was found.

Inside this toy run, the sweep did produce nonzero score variance at the per-regime level, but the run-level validity gate still failed and the selected regime remained null. Because `valid_for_interpretation` is false, this is a harness/regime failure, not interpretable evidence for component ablation.

## Failure / Caveat
- No regime met the required combination of bad_rate, trigger_rate, and interpretability.
- `chosen_regime` was null.
- `valid_for_interpretation` was false.
- `ablation_results` was null.
- The run does not justify component-level claims.
- Do not read the per-regime variance as component evidence.

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to enter a valid bad-rate window with nonzero trigger activity before any component ablation.