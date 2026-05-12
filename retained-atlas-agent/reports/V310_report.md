# V310 — Harness repair validation test

## Question
Can the harness produce one valid regime with nonzero bad cases and nonzero trigger activity?

## Hypothesis
If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
Executed a fixed-seed sweep over:
- seeds `0–19`
- `n_steps = 60`
- `A_c = 0.527`
- `D_c = 0.0388`
- `A_h = 0.1`
- `severity_grid = [0.22, 0.26, 0.3, 0.34, 0.38]`
- `base_failure_grid = [0.06, 0.09, 0.12, 0.15, 0.18]`
- `noise_grid = [0.0, 0.02]`

Reported per candidate:
- `bad_rate`
- `adaptive_rate`
- `AUC`
- `balanced_accuracy`
- `accuracy`
- `trigger_rate`
- `rescued`
- `harmed`
- `horizon_area`
- `horizon_width`
- `pinch`
- `mean_A`
- `min_A`
- `mean_A_norm`
- `min_A_norm`
- `score_mean`
- `score_var`
- `late_K`
- `late_mobility`
- `late_residual`
- `phase_counts`
- `validity_gate`

## Controls
- fixed seeds
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component interpretation unless `valid_for_interpretation = true`
- no regime selection outside the validity gate

## Results
`chosen_regime`: `null`

Run-level validity gate:
- `enough_positive_cases`: `false`
- `nondegenerate_bad_rate`: `false`
- `nonzero_score_variance`: `false`
- `nonzero_trigger_rate`: `false`
- `valid_for_interpretation`: `false`

Sweep outputs:
- all listed regimes had `valid_for_interpretation: false`
- `trigger_rate` was `0.0` for every listed regime
- `AUC` was `1.0` for every listed regime
- `balanced_accuracy` was `1.0` for every listed regime
- `accuracy` was `1.0` for every listed regime

Selected sweep entries:
- `severity 0.22`, `base_failure 0.06`, `noise 0.0`:
  - `bad_rate`: `0.6666666666666666`
  - `adaptive_rate`: `0.33333333333333337`
  - `trigger_rate`: `0.0`
  - `AUC`: `1.0`
  - `balanced_accuracy`: `1.0`
  - `accuracy`: `1.0`
  - `mean_A_norm`: `0.5094408812861148`
  - `min_A_norm`: `0.4152785601399009`
  - `score_mean`: `0.5094408812861148`
  - `score_var`: `0.0020986181932340702`
  - `phase_counts`: bad `40`, safe `20`
  - `valid_for_interpretation`: `false`

- `severity 0.22`, `base_failure 0.09`, `noise 0.0`:
  - `bad_rate`: `0.8666666666666667`
  - `adaptive_rate`: `0.1333333333333333`
  - `trigger_rate`: `0.0`
  - `AUC`: `1.0`
  - `balanced_accuracy`: `1.0`
  - `accuracy`: `1.0`
  - `mean_A_norm`: `0.47488594953029484`
  - `min_A_norm`: `0.37672640841071964`
  - `score_mean`: `0.47488594953029484`
  - `score_var`: `0.0025046865366489804`
  - `phase_counts`: bad `52`, safe `8`
  - `valid_for_interpretation`: `false`

- `severity 0.22`, `base_failure 0.12`, `noise 0.0`:
  - `bad_rate`: `0.9`
  - `adaptive_rate`: `0.09999999999999998`
  - `trigger_rate`: `0.0`
  - `AUC`: `1.0`
  - `balanced_accuracy`: `1.0`
  - `accuracy`: `1.0`
  - `mean_A_norm`: `0.4439782704789545`
  - `min_A_norm`: `0.3427127827700221`
  - `score_mean`: `0.4439782704789545`
  - `score_var`: `0.0029222961649190684`
  - `phase_counts`: bad `54`, safe `6`
  - `valid_for_interpretation`: `false`

- `severity 0.22`, `base_failure 0.15`, `noise 0.0`:
  - `bad_rate`: `0.9166666666666666`
  - `adaptive_rate`: `0.08333333333333337`
  - `trigger_rate`: `0.0`
  - `AUC`: `1.0`
  - `balanced_accuracy`: `1.0`
  - `accuracy`: `1.0`
  - `mean_A_norm`: `0.4168412250324038`
  - `min_A_norm`: `0.313349333730973`
  - `score_mean`: `0.4168412250324038`
  - `score_var`: `0.003303878919827256`
  - `phase_counts`: bad `55`, safe `5`
  - `valid_for_interpretation`: `false`

- `severity 0.22`, `base_failure 0.18`, `noise 0.0`:
  - `bad_rate`: `0.9333333333333333`
  - `adaptive_rate`: `0.06666666666666665`
  - `trigger_rate`: `0.0`
  - `AUC`: `1.0`
  - `balanced_accuracy`: `1.0`
  - `accuracy`: `1.0`
  - `mean_A_norm`: `0.3933864123145263`
  - `min_A_norm`: `0.2884727379565541`
  - `score_mean`: `0.3933864123145263`
  - `score_var`: `0.0036188166366869627`
  - `phase_counts`: bad `56`, safe `4`
  - `valid_for_interpretation`: `false`

Additional listed regimes at `severity 0.26`, `0.3`, `0.34`, and `0.38` also had:
- `trigger_rate = 0.0`
- `valid_for_interpretation = false`

## Interpretation
Inside this toy run, no valid regime was found.

That means the harness did not enter a regime that supports interpretation. The output is a harness/regime failure, not a component-law result.

Because `valid_for_interpretation` is `false`, the sweep numbers should not be read as evidence about internal components.

## Failure / Caveat
- `chosen_regime` is `null`
- run-level validity gate failed
- `nondegenerate_bad_rate` is `false`
- `nonzero_trigger_rate` is `false`
- `enough_positive_cases` is `false`
- every listed regime had `trigger_rate = 0.0`
- no valid regime was found, so no valid interpretive regime was available
- the reported high classification metrics do not override the failed validity gate

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to find a regime with `valid_for_interpretation = true` before any ablation or component reading.