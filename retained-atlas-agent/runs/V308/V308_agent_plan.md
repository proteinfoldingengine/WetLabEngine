# V308 — Deficit Intervention Threshold Test

## Question
Does triggering repair at `D_A > D_c` outperform simpler `A_norm` or `horizon_area` triggers?

## Hypothesis
If the deficit law is the better toy diagnostic, then a `D_A` trigger should yield lower bad rate and better rescue efficiency than single-metric triggers, with acceptable harm and stable threshold behavior.

## Method
Run a fixed-seed toy simulation across multiple seeds and variants. Compare four intervention policies:
1. `A_norm` trigger
2. `D_A` trigger
3. `horizon_area` trigger
4. combined trigger (`D_A` OR `horizon_area`)

Compute:
- bad_rate
- adaptive_rate
- trigger_rate
- rescued
- harmed
- net_rescue
- severity_reduction
- AUC
- balanced_accuracy

## Controls
- Fixed seeds
- Shared dynamics across policies
- Baseline no-intervention comparator
- Held-out evaluation split for AUC / balanced accuracy
- Same shock schedule across policies

## Results
Numbers only where possible.

## Interpretation
Use only toy-model language. Determine whether `D_A` improves intervention quality or whether simpler triggers match it.

## Failure / Caveat
Watch for threshold overfitting, redundant metrics, or gains that only appear through tuning.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: ablation of the components contributing to `A(t)` if `D_A` remains competitive, or freeze/report if it does not.