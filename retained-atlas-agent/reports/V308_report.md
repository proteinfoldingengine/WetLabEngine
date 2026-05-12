# V308 — Deficit Intervention Threshold Test

## Question
Does triggering repair at `D_A > D_c` outperform simpler `A_norm` or `horizon_area` triggers?

## Hypothesis
If the deficit law is the better toy diagnostic, then a `D_A` trigger should yield lower bad rate and better rescue efficiency than single-metric triggers, with acceptable harm and stable threshold behavior.

## Method
Fixed-seed toy simulation across 20 seeds and 60 steps, using shared dynamics and the same shock schedule across four intervention policies:
1. `A_norm` trigger
2. `D_A` trigger
3. `horizon_area` trigger
4. combined trigger (`D_A` OR `horizon_area`)

Reported metrics:
- bad_rate
- adaptive_rate
- trigger_rate
- rescued
- harmed
- net_rescue
- severity_reduction
- AUC
- balanced_accuracy
- phase_counts

## Controls
- Fixed seeds: 0–19
- Shared dynamics across policies
- Baseline no-intervention comparator
- Held-out evaluation split for AUC / balanced accuracy
- Same shock schedule across policies

## Results
`A_norm`
- bad_rate: 0.3383333333333333
- adaptive_rate: 0.23666666666666666
- trigger_rate: 0.5875
- rescued: 25.55
- harmed: 0
- net_rescue: 25.55
- severity_reduction: 0.943141018549082
- AUC: 1.0
- balanced_accuracy: 0.8350125944584383
- phase_counts bad: 406, safe: 794

`D_A`
- bad_rate: 0.4083333333333333
- adaptive_rate: 0.23666666666666666
- trigger_rate: 0.5583333333333333
- rescued: 28.15
- harmed: 0
- net_rescue: 28.15
- severity_reduction: 0.927240684969509
- AUC: 1.0
- balanced_accuracy: 0.8542253521126761
- phase_counts bad: 490, safe: 710

`horizon_area`
- bad_rate: 0.5775
- adaptive_rate: 0.23666666666666666
- trigger_rate: 0.2375
- rescued: 14.25
- harmed: 0
- net_rescue: 14.25
- severity_reduction: 0.7674369688454329
- AUC: 1.0
- balanced_accuracy: 0.970414201183432
- phase_counts bad: 693, safe: 507

`combined`
- bad_rate: 0.4083333333333333
- adaptive_rate: 0.23666666666666666
- trigger_rate: 0.5583333333333333
- rescued: 28.15
- harmed: 0
- net_rescue: 28.15
- severity_reduction: 0.927240684969509
- AUC: 1.0
- balanced_accuracy: 0.8542253521126761
- phase_counts bad: 490, safe: 710

Best policy by bad rate: `A_norm`

## Interpretation
Inside this toy run, `D_A` did not minimize bad rate. It did produce higher rescued count and higher balanced accuracy than `A_norm`, but with worse bad_rate and lower severity_reduction. The `combined` policy matched `D_A` exactly here, so `horizon_area` did not add new behavior under this configuration.

The toy evidence supports `D_A` as a usable diagnostic with some classification benefit, but not as the best intervention trigger on bad_rate in this run.

## Failure / Caveat
- `AUC` was 1.0 for all policies, so discrimination was not informative here.
- `horizon_area` showed very high balanced_accuracy but much worse bad_rate and rescue magnitude.
- No harmed cases occurred, so harm accounting did not distinguish policies.
- `D_A` and `combined` were identical in all reported outcomes, suggesting redundancy under this setup.
- The result does not justify threshold tuning beyond the reported values.

## Decision
branch

## Next
Smallest useful next test: ablation of the components contributing to `A(t)` if `D_A` remains competitive, or freeze/report if it does not.