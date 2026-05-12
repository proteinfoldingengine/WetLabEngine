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
Ran a fixed-seed sweep over severity, base_failure, and noise_scale with:
- seeds: 0–19
- n_steps: 60
- A_c: 0.527
- D_c: 0.0388
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

No valid regime was found, so no component ablation was run.

## Controls
- Fixed seeds
- Shared simulation code across sweep points
- No threshold tuning after validation
- No regime selection outside the target bad-rate window
- Full sweep reported

## Results
`chosen_regime`: null

`validity_gate`:
- enough_positive_cases: false
- nondegenerate_bad_rate: false
- nonzero_score_variance: false
- nonzero_trigger_rate: false
- valid_for_interpretation: false

Selected sweep points:
- severity 0.25, base_failure 0.02, noise 0.0:
  - bad_rate: 0
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: NaN
  - balanced_accuracy: 1.0
  - accuracy: 1.0
  - mean_A_norm: 0.8395186164875962
  - min_A_norm: 0.7892359528882226
  - score_mean: 0.8395186164875962
  - score_var: 0.0011792316096504623
  - phase_counts bad: 0, safe: 1200
  - valid_for_interpretation: false

- severity 0.35, base_failure 0.14, noise 0.0:
  - bad_rate: 0.10333333333333333
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.9618484458598409
  - balanced_accuracy: 0.5
  - accuracy: 0.8966666666666666
  - mean_A_norm: 0.8097193144400797
  - min_A_norm: 0.7585626956719961
  - score_mean: 0.8097193144400797
  - score_var: 0.0012132676234578388
  - phase_counts bad: 124, safe: 1076
  - valid_for_interpretation: false

- severity 0.35, base_failure 0.17, noise 0.0:
  - bad_rate: 0.2175
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.9748121536462142
  - balanced_accuracy: 0.5
  - accuracy: 0.7825
  - mean_A_norm: 0.8072591733346612
  - min_A_norm: 0.7563900330894834
  - score_var: 0.0012001671077582713
  - phase_counts bad: 261, safe: 939
  - valid_for_interpretation: false

- severity 0.45, base_failure 0.11, noise 0.0:
  - bad_rate: 0.24916666666666668
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.9770849831889927
  - balanced_accuracy: 0.5
  - accuracy: 0.7508333333333334
  - mean_A_norm: 0.8054217932672576
  - min_A_norm: 0.7532708786628571
  - score_var: 0.0012570095872117104
  - phase_counts bad: 299, safe: 901
  - valid_for_interpretation: false

- severity 0.45, base_failure 0.17, noise 0.03:
  - bad_rate: 0.375
  - adaptive_rate: 1.0
  - trigger_rate: 0.0
  - AUC: 0.9579135334226541
  - balanced_accuracy: 0.5
  - accuracy: 0.625
  - mean_A_norm: 0.8004990343439363
  - min_A_norm: 0.7247648510971918
  - score_var: 0.0018740475554099272
  - phase_counts bad: 450, safe: 750
  - valid_for_interpretation: false

## Interpretation
Inside this toy run, no valid regime was found.

That means the component-ablation branch is not interpretable here. The sweep did produce some regimes with nonzero bad cases and nonzero score variance, but the run-level validity gate still failed, so those ablation-style quantities would not be valid evidence for component importance.

The result supports a harness/regime failure classification, not a component-law conclusion.

## Failure / Caveat
- No valid regime was found.
- `valid_for_interpretation` was false for the run-level gate.
- Some sweep points had `bad_rate` in or near the target region, but `trigger_rate` remained 0.0 there.
- Several points had nonzero score variance, but the gate still failed.
- AUC was undefined when only one class was present, and many metrics were therefore not informative.
- The reported warnings are consistent with degenerate label distributions in parts of the sweep.

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to produce a regime with `bad_rate` in `[0.20, 0.40]`, `trigger_rate > 0.05`, and a valid interpretation gate before attempting component ablation.