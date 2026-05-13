# V312_LAB_CONTEXT_TEST — Repair Horizon Regime

## Question
Can the regime-search harness produce one valid nondegenerate regime with explicit controller-comparison rows?

## Hypothesis
If the search space is re-centered or broadened and validity gates are enforced strictly, then at least one regime will satisfy:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- `horizon_area > 0` or `horizon_width > 0`
- held-out validation metrics reported
- `balanced_accuracy` reported

## Method
Executed the V312 lab-context test with deterministic validation.  
Inputs used:
- execution return code: `0`
- stdout JSON
- saved results JSON
- scientific execution validation MD / JSON

The harness evaluated candidate regimes and applied the validity gate before any controller interpretation.

## Controls
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no component ablation
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report `mean_A_norm` and `min_A_norm` as normalized-series quantities

## Results
Overall validation:
- `overall_status: pass`
- `interpretation_allowed: true`
- `selected_regime_present: false`
- `valid_row_count: 2`
- `total_row_count: 152`
- `valid_controller_row_count: 0`
- `total_controller_row_count: 0`

Candidate 0:
- `bad_rate: 0.125`
- `trigger_rate: 0.5`
- `AUC: 0.7657004022172739`
- `balanced_accuracy: 0.875`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `valid_for_interpretation: false`

Candidate 1:
- `bad_rate: 0.375`
- `trigger_rate: 0.875`
- `AUC: 0.7260812751379881`
- `balanced_accuracy: 0.625`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `valid_for_interpretation: false`

Additional candidate rows shown in validation:
- candidate 2: `bad_rate: 0.75`, `trigger_rate: 1.0`, `AUC: 0.673273758238148`, `balanced_accuracy: 0.25`, `horizon_area: 0.0`, `horizon_width: 0.0`, `valid_for_interpretation: false`
- candidate 3: `bad_rate: 1.0`, `trigger_rate: 1.0`, `AUC: 0.6104566385477967`, `balanced_accuracy: 0.0`, `horizon_area: 0.0`, `horizon_width: 0.0`, `valid_for_interpretation: false`
- candidate 4: `bad_rate: 1.0`, `trigger_rate: 1.0`, `AUC: 0.5391719159083757`, `balanced_accuracy: 0.0`, `horizon_area: 0.0`, `horizon_width: 0.0`, `valid_for_interpretation: false`
- candidate 5: `bad_rate: 1.0`, `trigger_rate: 1.0`, `AUC: 0.4966681090327391`, `balanced_accuracy: 0.0`, `horizon_area: 0.0`, `horizon_width: 0.0`, `valid_for_interpretation: false`

Selected-regime summary:
- none selected
- warning: `No selected/chosen regime found.`

Validity-gate reasons from the displayed candidates:
- `horizon_nonzero: false` for all shown candidate rows
- controller rows did not survive the validity gate
- `valid_controller_row_count: 0`

## Interpretation
This is a harness/regime-search failure, not controller validation.

Inside the toy:
- the search produced candidate regimes with nonzero `bad_rate` and nonzero `trigger_rate`
- but horizon metrics remained exactly zero in the displayed candidates
- because `horizon_nonzero` never passed, no regime became interpretable for controller comparison

The strongest supported statement is only:
- the harness can generate candidate rows,
- but it did not produce a valid nondegenerate horizon regime in this run.

This does not change the V307 boundary.

## Failure / Caveat
- No selected regime was found.
- `horizon_area` and `horizon_width` were `0.0` for the displayed candidates.
- `valid_controller_row_count` was `0`, so no explicit controller-comparison rows were available.
- Candidate quality was insufficient for interpreting controller competition.
- This run does not validate `D_A` as a controller.
- No branch can be promoted on the basis of these rows.

## Decision
stop

## Next
Smallest useful next test: stop this intervention branch and do not interpret controller comparisons until a new harness produces at least one selected regime with:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- `horizon_area > 0` or `horizon_width > 0`
- held-out validation reported
- valid controller rows surviving the gate