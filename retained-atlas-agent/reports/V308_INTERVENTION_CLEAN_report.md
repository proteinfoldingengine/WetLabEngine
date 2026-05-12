# V308 — Deficit Intervention Threshold Test

## Question
Does triggering full staged repair at `D_A > D_c` outperform scalar `A_norm`, horizon area, and combined triggers on the valid regime?

## Hypothesis
If the deficit law is the better controller, then the `D_A` trigger should match or slightly outperform the scalar `A_norm` trigger on rescue, with similar or lower harm, on the same seed set.

## Method
Evaluated four controllers on the same 8 seeds in the same regime (`bf=0.35`, `nz=0.08`, `sev=0.65`):

- scalar `A_norm` trigger
- `D_A` trigger
- horizon-area trigger
- combined trigger

Used the provided run output only. Reported baseline metrics, controller metrics, trigger rate, rescued, harmed, net rescue, and severity-related fields from stdout. No threshold tuning was performed.

## Controls
- Same seed set across all controllers: 101, 203, 307, 409, 503, 607, 701, 809
- Same baseline protocol
- Explicit harm accounting present
- No threshold tuning after validation
- No component ablation
- No claim escalation
- No invented numbers beyond stdout

## Results
Baseline:
- cases: 8
- bad_rate: 1.0
- adaptive_rate: 0.0
- AUC: 0.5
- balanced_accuracy: 0.25
- trigger_rate: 0.0
- rescued: 0
- harmed: 0
- net_rescue: 0
- mean_A_norm: 0.4803869302735562
- min_A_norm: 0.22616833767400868
- horizon_area: 0.0
- horizon_width: 0.0

`A_norm` trigger:
- bad_rate: 0.875
- adaptive_rate: 0.125
- AUC: 0.7857142857142857
- balanced_accuracy: 0.5714285714285714
- accuracy: 0.25
- trigger_rate: 1.0
- rescued: 8
- harmed: 0
- net_rescue: 8
- mean_A_norm: 0.518604159401524
- min_A_norm: 0.3298654269469275
- late_action: 0.27605422079999997
- late_field: 0.40284953341016055
- late_residual: 0.24715046658983947
- pinch: 0.5980992562288171

`D_A` trigger:
- bad_rate: 1.0
- adaptive_rate: 0.0
- AUC: 0.5
- balanced_accuracy: 0.1875
- accuracy: 0.375
- trigger_rate: 1.0
- rescued: 8
- harmed: 0
- net_rescue: 8
- mean_A_norm: 0.5056871232689409
- min_A_norm: 0.31504538566382256
- late_action: 0.38340863999999997
- late_field: 0.3875377153917792
- late_residual: 0.2624622846082208
- pinch: 0.6165876902116061

Horizon-area trigger:
- bad_rate: 1.0
- adaptive_rate: 0.0
- AUC: 0.5
- balanced_accuracy: 0.25
- accuracy: 0.5
- trigger_rate: 0.0
- rescued: 0
- harmed: 0
- net_rescue: 0
- horizon_area: 0.0
- horizon_width: 0.0

Combined trigger:
- bad_rate: 0.875
- adaptive_rate: 0.125
- AUC: 0.7857142857142857
- balanced_accuracy: 0.5714285714285714
- accuracy: 0.25
- trigger_rate: 1.0
- rescued: 8
- harmed: 0
- net_rescue: 8
- mean_A_norm: 0.518604159401524
- min_A_norm: 0.3298654269469275
- late_action: 0.27605422079999997
- late_field: 0.40284953341016055
- late_residual: 0.24715046658983947
- pinch: 0.5980992562288171

Validity gate:
- baseline valid_for_interpretation: false
- `D_A` valid_for_interpretation: false
- horizon valid_for_interpretation: false
- `A_norm` valid_for_interpretation: true
- combined valid_for_interpretation: true

Variant-level `A_norm` performance:
- seeds 101, 203, 307, 409, 503, 607, 701, 809
- rescued on all 8
- harmed on 0
- trigger_rate 1.0 for all seeds

Variant-level `D_A` performance:
- rescued on all 8
- harmed on 0
- trigger_rate 1.0 for all seeds
- adaptive outcomes: 0
- bad outcomes: 8

Severity fields:
- baseline late_field: 0.29934694790178096
- `A_norm` late_field: 0.40284953341016055
- `D_A` late_field: 0.3875377153917792
- baseline late_residual: 0.35065305209821906
- `A_norm` late_residual: 0.24715046658983947
- `D_A` late_residual: 0.2624622846082208

## Interpretation
Inside this toy run, the `A_norm` controller was the only one with nonzero adaptive_rate and better classification metrics than `D_A`. The `D_A` controller did not outperform the scalar `A_norm` trigger on rescue or harm, and its discrimination metrics were weaker.

What the toy supports:
- `A_norm` remains the better controller in this run.
- `D_A` remains a useful diagnostic signal, but not a superior intervention rule here.
- Horizon-area triggering had no effect because horizon metrics stayed at zero.

What it does not support:
- It does not support promoting `D_A` as the intervention controller on this branch.
- It does not support any physical claim.
- It does not show horizon-area control was testable in this regime.

## Failure / Caveat
- `D_A` had no advantage over scalar `A_norm` here.
- Baseline and some controller rows failed the validity gate for interpretation because `bad_rate_range` was false and, for baseline/horizon, `trigger_rate_gt_0p05` was false.
- Horizon area and horizon width were zero everywhere, so that controller comparison was non-informative in this regime.
- The run still shows all controllers rescued 8 and harmed 0, so the main separation is in classification / intervention behavior, not harm.

## Decision
branch

## Next
Run the smallest useful follow-up:
- compare `A_norm` vs `D_A` on a regime where triggers are not saturated,
- require held-out validation,
- and test whether `D_A` improves only in a controller-failure regime or remains purely diagnostic.