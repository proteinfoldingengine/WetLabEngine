# V311_VALIDITY_HARDENING — Valid Regime Search

## Question
Can the regime-search harness produce one valid nondegenerate regime with explicit controller comparison rows?

## Hypothesis
If the search space is widened or re-centered and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

## Method
Executed the V311 validity-gated regime search and consumed:
- execution output
- saved JSON results
- deterministic execution validation

Validation rule used as authority:
- `interpretation_allowed = false` means no scientific interpretation is permitted.

The run searched 4 shown regimes in the results JSON summary:
- `bf=0.22, nz=0.0, sev=0.5`
- `bf=0.22, nz=0.03, sev=0.55`
- `bf=0.22, nz=0.06, sev=0.6`
- `bf=0.28, nz=0.0, sev=0.55`

## Controls
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report whether `mean_A_norm` and `min_A_norm` are computed from the normalized time series, not from raw means divided by baseline
- if AUC is missing or degenerate, state that plainly

## Results
Validation status:
- `overall_status: fail`
- `interpretation_allowed: false`
- `selected_regime_present: false`

Row counts:
- `valid_row_count: 2`
- `total_row_count: 17`
- `valid_controller_row_count: 0`
- `total_controller_row_count: 0`

Gate failures:
- all available `bad_rate` values are saturated
- all available `trigger_rate` values are saturated
- all available `horizon metrics` are zero

Per-candidate validity summary from validation:
- `all_candidates_0` through `all_candidates_14`:
  - `bad_rate: 0.0`
  - `trigger_rate: 0.0`
  - `AUC: 0.5`
  - `balanced_accuracy: 0.5`
  - `horizon_area: 0.0`
  - `horizon_width: 0.0`
  - `valid_for_interpretation: false`
- `controller_rows`:
  - `bad_rate: null`
  - `trigger_rate: null`
  - `auc: null`
  - `balanced_accuracy: null`
  - `validity_gate_missing_or_no_valid_for_interpretation`
- `validity_gate`:
  - same missing-metric warnings as above

Selected numeric regime outputs from results JSON:
- `A_c = 0.527`
- `A_h = 0.1`
- `D_c = 0.0388`

For each shown regime:
- `cases: 8`
- `bad_rate: 0`
- `adaptive_rate: 1`
- `trigger_rate: 0`
- `AUC: 0.5`
- `balanced_accuracy: 0.5`
- `accuracy: 1.0`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `D_A_mean: 0.0`
- `D_A_max: 0.0`
- `rescued: 0`
- `harmed: 0`
- `net_rescue: 0`

Example regime fields:
- `regime bf=0.22, nz=0.0, sev=0.5`
  - `mean_A_norm: 0.8307170221772933`
  - `min_A_norm: 0.7125919133612024`
  - `late_field: 0.7867060076479396`
  - `late_action: 0.21329399235206037`
  - `late_residual: 0.21329399235206037`
  - `late_mobility: 0.8667666500818281`
  - `late_K: 0.5210904076546131`
- `regime bf=0.22, nz=0.03, sev=0.55`
  - `mean_A_norm: 0.8360192491611994`
  - `min_A_norm: 0.7157337996894955`
  - `late_field: 0.7940458838888704`
  - `late_action: 0.20595411611112954`
  - `late_residual: 0.20595411611112954`
  - `late_mobility: 0.8730935201769167`
  - `late_K: 0.5278527662079829`
- `regime bf=0.22, nz=0.06, sev=0.6`
  - `mean_A_norm: 0.8299469906961651`
  - `min_A_norm: 0.6682566379151224`
  - `late_field: 0.7703049995141176`
  - `late_action: 0.22969500048588237`
  - `late_residual: 0.22969500048588237`
  - `late_mobility: 0.850711099234464`
  - `late_K: 0.5343058333230176`
- `regime bf=0.28, nz=0.0, sev=0.55`
  - `mean_A_norm: 0.8250550038494495`
  - `min_A_norm: 0.6682566379151224`
  - `late_field: 0.7727067437659072`
  - `late_action: 0.2272932562340928`
  - `late_residual: 0.2272932562340928`
  - `late_mobility: 0.8388251178131423`
  - `late_K: 0.528898835085515`

Normalization note:
- `mean_A_norm` and `min_A_norm` are reported from the normalized time series in the saved results.
- No evidence here suggests they were computed as raw means divided by baseline after the fact.

## Interpretation
No valid nondegenerate regime was found.

Inside the toy, this means the harness failed the required validity gate:
- no nonzero failure rate,
- no nonzero trigger activity,
- no nonzero horizon metrics,
- no selected regime,
- no controller comparison rows that can be interpreted.

This does not weaken the retained-atlas toy law by itself.
It does mean the V311 harness-search branch did not produce an interpretable controller-validation case.

## Failure / Caveat
- All candidate regimes were degenerate in the same direction: `bad_rate = 0`, `trigger_rate = 0`, `horizon_area = 0`, `horizon_width = 0`.
- `AUC = 0.5` and `balanced_accuracy = 0.5` throughout the candidates.
- There was no selected/chosen regime.
- Controller comparison rows were absent.
- Because `interpretation_allowed = false`, no scientific controller conclusion is permitted.

## Decision
stop

## Next
Smallest useful next test: stop this branch and do not add new metrics or reinterpret invalid rows as evidence. If the project continues, restart with a different regime-generation strategy that can produce nonzero bad and trigger activity before any controller comparison is attempted.