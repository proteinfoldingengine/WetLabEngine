# V309D — Regime repair for valid component ablation

## Question
Can we find a nondegenerate regime for the reachability-law ablation where the full score is interpretable?

## Hypothesis
If the harness is repaired, then a 2D sweep over severity and base_failure/intercept/noise should produce at least one regime with:
- bad_rate in [0.20, 0.40]
- trigger_rate > 0.05
- score variance > 0
- enough positive bad cases

Only then should component ablation be interpreted.

## Method
Ran the fixed-seed sweep reported in the execution output over severity, base_failure, and noise_scale. For each candidate regime, the run computed:
- bad_rate
- adaptive_rate
- trigger_rate
- auc
- balanced_accuracy
- accuracy
- mean_A_norm
- min_A_norm
- score_mean
- score_var
- phase_counts
- validity_gate

Controls were the shared fixed seeds and shared simulation code across sweep points.

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

Sweep highlights:
- `severity 0.35`, `base_failure 0.05`, `noise 0.0`:
  - bad_rate: 0.3833333333333333
  - trigger_rate: 0.0
  - score_var: 5.292906861088098e-05
  - valid_for_interpretation: 0.0
- `severity 0.35`, `base_failure 0.12`, `noise 0.0`:
  - bad_rate: 0.4225
  - trigger_rate: 0.08
  - score_var: 0.0002237679340583792
  - valid_for_interpretation: 0.35
- `severity 0.35`, `base_failure 0.19`, `noise 0.0`:
  - bad_rate: 0.46416666666666667
  - trigger_rate: 0.17333333333333334
  - score_var: 0.0005520030795764399
  - valid_for_interpretation: 0.25
- `severity 0.35`, `base_failure 0.26`, `noise 0.0`:
  - bad_rate: 0.49833333333333335
  - trigger_rate: 0.2791666666666667
  - score_var: 0.001007696825698457
  - valid_for_interpretation: 0.05
- `severity 0.35`, `base_failure 0.33`, `noise 0.0`:
  - bad_rate: 0.5341666666666667
  - trigger_rate: 0.44666666666666666
  - score_var: 0.001495881047494534
  - valid_for_interpretation: 0.0

Other sweep entries all reported `valid_for_interpretation: 0.0`, `0.05`, `0.1`, `0.2`, `0.25`, or `0.35`, but no entry was selected as a valid regime.

## Interpretation
This is a harness/regime failure inside the toy system.

No valid regime was found, so the ablation numbers should not be interpreted as component evidence. The sweep did show nonzero score variance and nonzero trigger rates in many settings, but the validity gate still failed overall and `chosen_regime` remained null.

Inside the toy, that means the current harness still does not support a clean component-ablation test.

## Failure / Caveat
- No valid regime was found.
- `valid_for_interpretation` was false for the run-level gate.
- The reported `valid_for_interpretation` values in the sweep did not produce a chosen regime.
- Component-level conclusions are not justified here.
- This is not a freeze case; the branch remains unresolved.

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to satisfy the validity gate before attempting any component ablation.