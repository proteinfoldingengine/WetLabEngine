# V310_REPORT_SPLIT_TEST — Valid Regime Repair Test

## Question

Can the harness produce one clearly valid nondegenerate regime with explicit controller comparison rows?

## Hypothesis

If the regime search is narrowed and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

## Method

Executed the V310 narrow-regime repair run using the saved results and deterministic execution validation.

Search target:
- narrow neighborhood around the current validated band
- baseline protocol fixed
- validity gate required before interpretation

Required validity conditions:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- at least one of `horizon_width` or `horizon_area` nonzero
- `balanced_accuracy` reported

Controllers intended for comparison:
- scalar `A_norm` trigger
- duration-below-`A_c` trigger
- integrated deficit `D_A` trigger
- horizon-area trigger
- combined trigger

Deterministic validation status:
- `overall_status: pass`
- `interpretation_allowed: true`

## Controls

- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report whether `mean_A_norm` and `min_A_norm` are computed from the normalized time series, not from raw means divided by baseline

## Results

Validation:
- `overall_status = pass`
- `interpretation_allowed = true`
- `valid_row_count = 3`
- `total_row_count = 4`

Selected baseline:
- `trigger_rate = 0.0`
- `bad_rate = 0.0`
- `AUC = 0.5`
- `valid_for_interpretation = false`
- failures: `trigger_rate_saturated`, `bad_rate_saturated`, `validity_gate_false`
- warning: `horizon_metrics_zero`

Candidate regimes reported in stdout/results:
- `bf = 0.3, nz = 0.02, sev = 0.6`
  - `bad_rate = 0.0`
  - `trigger_rate = 0.0`
  - `AUC = 0.5`
  - `balanced_accuracy = 0.5`
  - `horizon_area = 0.0`
  - `horizon_width = 0.0`
- `bf = 0.3, nz = 0.05, sev = 0.6`
  - `bad_rate = 0.0`
  - `trigger_rate = 0.0`
  - `AUC = 0.5`
  - `balanced_accuracy = 0.5`
  - `horizon_area = 0.0`
  - `horizon_width = 0.0`
- `bf = 0.35, nz = 0.02, sev = 0.65`
  - `bad_rate = 0.0`
  - `trigger_rate = 0.0`
  - `AUC = 0.5`
  - `balanced_accuracy = 0.5`
  - `horizon_area = 0.0`
  - `horizon_width = 0.0`
- `bf = 0.35, nz = 0.05, sev = 0.65`
  - `bad_rate = 0.0`
  - `trigger_rate = 0.0`
  - `AUC = 0.5`
  - `balanced_accuracy = 0.5`
  - `horizon_area = 0.0`
  - `horizon_width = 0.0`
- `bf = 0.4, nz = 0.05, sev = 0.7`
  - `bad_rate = 0.0`
  - `trigger_rate = 0.0`
  - `AUC = 0.5`
  - `balanced_accuracy = 0.5`
  - `horizon_area = 0.0`
  - `horizon_width = 0.0`

Mixed-in variant-level values showed some nonzero `D_A` entries, including:
- `D_A = 0.001158499607474453`
- `D_A = 0.0001020612602420784`

But the regime-level validity gate still failed because:
- `bad_rate_range = false`
- `horizon_nonzero = false`
- `phase_counts_bad_gt_0 = false`
- `trigger_rate_gt_0p05 = false`

Normalization note:
- The run included `mean_A_norm` and `min_A_norm` fields directly in the normalized series outputs.
- These are reported as normalized time-series quantities, not as raw means divided afterward.

## Interpretation

Inside the toy, this run did not produce one clearly valid nondegenerate regime.

The validation gate passed as an execution check, but the selected regimes remained degenerate:
- no bad cases
- no horizon activity
- zero trigger rate

So there is no valid controller-comparison row set to interpret scientifically.

The nonzero `D_A` values in some variant rows are not enough to validate the branch, because they occurred inside regimes that still failed the validity gate.

## Failure / Caveat

- No regime satisfied the required nondegenerate validity conditions.
- Explicit controller comparison rows were not established for a valid regime.
- `AUC` was missing for some controller rows in validation metadata, though the execution itself passed.
- The available regime candidates all had `bad_rate = 0.0`.
- Horizon metrics remained zero at the regime level.
- This is a harness/regime failure, not evidence that the controller branch is valid.

## Decision

stop

## Next

Smallest useful next test: stop the intervention branch unless a new run can first produce a single valid nondegenerate regime with `bad_rate > 0`, `trigger_rate > 0.05`, and nonzero horizon metrics before any controller comparison is interpreted.