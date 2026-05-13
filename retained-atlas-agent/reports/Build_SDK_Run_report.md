# Build_SDK_Run — V312 Regenerate Regimes

## Question
Can the regime-search harness produce one valid nondegenerate regime with explicit controller comparison rows?

## Hypothesis
If the search space is widened or re-centered and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

## Method
Executed the V312 deterministic regime-search harness with fixed seeds and preserved baseline protocol.  
Validation required:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- `horizon_area > 0` or `horizon_width > 0`
- `balanced_accuracy` reported
- held-out validation present

The run produced:
- execution return code `0`
- validation status `pass`
- `interpretation_allowed: true`
- `selected_regime_present: true`

However, the selected regime set contained:
- `valid_row_count: 5`
- `total_row_count: 342`
- `valid_controller_row_count: 0`
- `total_controller_row_count: 0`

## Controls
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation
- `mean_A_norm` and `min_A_norm` were computed from the normalized time series in the reported variant rows
- `AUC` was reported as real in the validation gate checks, not hard-coded for the selected rows

## Results
Selected regime summaries from `RESULTS JSON`:

1. Regime `{"bf":0.18,"nz":0.0,"sev":0.45}`
- `cases: 8`
- `bad_rate: 0.25`
- `trigger_rate: 0.5`
- `AUC: 1.0`
- `balanced_accuracy: 0.5`
- `accuracy: 0.75`
- `adaptive_rate: 0.75`
- `rescued: 0`
- `harmed: 0`
- `net_rescue: 0`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `D_A_mean: 0.0030667029452948105`
- `D_A_max: 0.014130695428119039`
- `mean_A_norm: 0.6034656807554329`
- `min_A_norm: 0.490403737953025`
- `phase_counts: {"adaptive":6,"bad":2,"horizon":0}`
- `valid_for_interpretation: false`

2. Regime `{"bf":0.18,"nz":0.0,"sev":0.5}`
- `cases: 8`
- `bad_rate: 0.25`
- `trigger_rate: 0.375`
- `AUC: 1.0`
- `balanced_accuracy: 0.5`
- `accuracy: 0.75`
- `adaptive_rate: 0.75`
- `rescued: 0`
- `harmed: 0`
- `net_rescue: 0`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `D_A_mean: 0.005181063110334154`
- `D_A_max: 0.02944447179868899`
- `mean_A_norm: 0.5769807181531543`
- `min_A_norm: 0.4692723593566811`
- `phase_counts: {"adaptive":6,"bad":2,"horizon":0}`
- `valid_for_interpretation: false`

3. Regime `{"bf":0.18,"nz":0.0,"sev":0.55}`
- `cases: 8`
- `bad_rate: 0.125`
- `trigger_rate: 0.375`
- `AUC: 1.0`
- `balanced_accuracy: 0.5`
- `accuracy: 0.875`
- `adaptive_rate: 0.875`
- `rescued: 1`
- `harmed: 0`
- `net_rescue: 1`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `D_A_mean: 0.0024791837516353766`
- `D_A_max: 0.016663109426133388`
- `mean_A_norm: 0.6006158999422676`
- `min_A_norm: 0.4482995767362633`
- `phase_counts: {"adaptive":7,"bad":1,"horizon":0}`
- `valid_for_interpretation: false`

4. Regime `{"bf":0.18,"nz":0.0,"sev":0.6}`
- `cases: 8`
- `bad_rate: 0.5`
- `trigger_rate: 0.5`
- `AUC: 1.0`
- `balanced_accuracy: 0.625`
- `accuracy: 0.625`
- `adaptive_rate: 0.5`
- `rescued: 3`
- `harmed: 0`
- `net_rescue: 3`
- `horizon_area: 0.0`
- `horizon_width: 0.0`
- `D_A_mean: 0.00832007711108358`
- `D_A_max: 0.04364411827629811`
- `mean_A_norm: 0.5682545804089714`
- `min_A_norm: 0.4568552201778157`
- `phase_counts: {"adaptive":4,"bad":4,"horizon":0}`
- `valid_for_interpretation: false`

Validation metadata:
- `overall_status: pass`
- `selected_regime_present: true`
- `valid_row_count: 5`
- `valid_controller_row_count: 0`
- `row_counts.total_row_count: 342`
- `controller row outputs for explicit comparisons: none`

Per-row gate failures were dominated by:
- `horizon_metrics_zero`
- `balanced_accuracy_at_chance`
- `trigger_rate_saturated_one` in some candidates
- `auc_at_chance` in some candidates
- `validity_gate_false` on invalid rows

## Interpretation
The harness executed successfully, but the reported candidate set did not produce any valid controller-comparison rows. The key failure is not numeric instability of the toy law; it is that no nondegenerate horizon-bearing comparison row survived the validity gate.

Inside the toy, this means:
- there are candidate regimes with nonzero `bad_rate` and nonzero `trigger_rate`
- but all reported candidates had `horizon_area = 0.0` and `horizon_width = 0.0`
- therefore no controller branch is interpretable yet
- the validity gate correctly prevented overinterpretation

This does not validate controller superiority or horizon control. It only shows the search harness can run and report candidate summaries, but not yet a valid regime for comparison.

## Failure / Caveat
- No candidate had `horizon_area > 0` or `horizon_width > 0`
- No valid controller comparison rows were emitted
- `valid_controller_row_count = 0`
- Multiple candidates were invalid despite having nonzero `bad_rate` and `trigger_rate`
- The strongest toy-law boundary from V307 remains unchanged
- The run is a harness/regime-search failure for controller validation, not evidence for controller success

## Decision
branch

## Next
Smallest useful next test: repair the regime-search harness so it can produce one valid nondegenerate regime with `horizon_area > 0` or `horizon_width > 0` before any controller comparison is interpreted.