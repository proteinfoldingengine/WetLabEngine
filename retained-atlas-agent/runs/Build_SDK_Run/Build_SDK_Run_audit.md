# Build_SDK_Run — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
stop or freeze, not branch.

Reason:
The report says `branch` because no valid controller-comparison rows survived the validity gate. That part is justified. But the writeup also mixes in unsupported controller-specific claims and treats the run as a regime-search success in places. More importantly, the constitution says if a branch fails to produce a valid regime, stop that branch rather than interpreting invalid rows.

## Execution Validator Check
Did execution_validator.py run?
Yes, per the provided execution validation output/JSON.

Did interpretation_allowed pass?
Yes, `interpretation_allowed: true`.

If interpretation_allowed is false, did the report avoid scientific interpretation?
Not applicable.

Did the validator catch saturated trigger rates, invalid rows, dead horizon metrics, or missing/invalid AUC?
Yes. It flagged:
- `trigger_rate_saturated_one`
- `validity_gate_false`
- `horizon_metrics_zero`
- `balanced_accuracy_at_chance`
- `auc_at_chance`
- `bad_rate_zero`
- `phase_counts_bad_zero`

So the validation layer correctly rejected interpretation for all candidate rows.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No. The selected regime summaries show `valid_for_interpretation: false` for all listed regimes.

If it failed, did the report avoid interpretation?
Mostly yes at the regime level, but not completely. The report still presented some interpretive language about “the harness can run” and “controller validation,” which is too strong given that no valid controller rows existed. The safe conclusion should have been failure/stop, not a branch with implied forward interpretability.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes. The report quotes numbers that appear in `RESULTS JSON` and `STDOUT`, such as:
- `valid_row_count: 5`
- `total_row_count: 342`
- `valid_controller_row_count: 0`
- `selected_regime_present: true`
- regime summaries for `bf: 0.18`, `nz: 0.0`, `sev: 0.45/0.5/0.55/0.6`

Any invented or unsupported numbers?
A few concerns:
- The report implies “explicit controller-comparison rows” were available in the run, but the validation output shows `valid_controller_row_count: 0` and the report itself says controller rows were none. That is a structural mismatch.
- The report mentions `mean_A_norm` and `min_A_norm` “were computed from the normalized time series in the reported variant rows,” which is supported by the code, but this is not independently validated by the execution validator.
- The report’s statement that the run “can produce one valid nondegenerate regime” is unsupported by the provided validation: `valid_for_interpretation` is false for every displayed regime because `horizon_nonzero` is false.
- If the report later contains truncated or omitted regime summaries, those must not be assumed valid.

## Code/Method Check
Was the code runnable?
Yes, likely runnable. It is syntactically coherent and produced output.

Any obvious harness flaws?
Yes:
1. The strict validity gate requires `horizon_area > 0 or horizon_width > 0`, but the simulation as written appears to produce `horizon_area = 0.0` and `horizon_width = 0.0` for the reported candidates. That makes valid regimes impossible in practice.
2. The selection logic depends on `valid_candidates`, but none of the displayed regimes pass `valid_for_interpretation`.
3. The controller comparison section is contingent on `selected is not None`, so no controller rows are emitted. This matches the output but defeats the stated purpose.
4. The controller scoring logic is inconsistent:
   - `controller_eval('D_A', 'trigger_DA')` uses `D_A` as a score and `D_c` as threshold.
   - `controller_eval('A_norm', 'trigger_scalar')` uses `mean_A_norm` and `A_c`.
   - But the “combined” score is `max(D_A, horizon_area)`, which is not clearly justified as a controller metric.
5. The trigger definitions are not aligned with the requested test sequence from current state:
   - V308 was supposed to compare `A_norm` trigger, `D_A` trigger, `horizon_area` trigger, combined trigger.
   - The code also adds duration trigger, which is acceptable only if treated as an extra comparison, but the report should not imply it was part of the canonical minimal test.
6. Degenerate regime problem:
   - All displayed candidate regimes have `horizon_area = 0.0` and `horizon_width = 0.0`.
   - The branch therefore cannot satisfy its own gate.

## Claim Boundary Check
Any overclaiming?
Yes, mild overclaiming.
The report says the run “produced one valid nondegenerate regime” in the question/hypothesis framing, but the results do not support that. The correct statement is the opposite: no valid nondegenerate regime survived the gate.

Any forbidden GR/physics language?
No forbidden GR escalation is present in the provided report. The language stays at toy-level / horizon-like / diagnostic. That part is acceptable.

## Current-State Consistency Check
Did the run respect current_state.md?
Partially.

Respected:
- It stayed within toy-model language.
- It preserved `D_A` and `A_norm` as central metrics.
- It used fresh deterministic seeds.
- It did not claim GR recovery.

Did it preserve the V307 law boundary?
Not cleanly.
The current state says V308 should compare interventions at `D_A > D_c`, `A_norm`, horizon area, and combined triggers. But this run never achieved a valid regime with nonzero horizon metrics, so it did not meaningfully validate the V308 intervention branch. The decision to `branch` is only barely defensible as a harness-failure branch, but not as an advance in the law stack.

## Required Correction
What must be fixed before next loop?
1. Stop interpreting this as a successful V308 controller-validation run.
2. Repair the regime-search harness so at least one candidate can satisfy the gate with:
   - `bad_rate > 0`
   - `trigger_rate > 0.05`
   - `horizon_area > 0` or `horizon_width > 0`
3. Do not add new metrics to paper over the failure.
4. Report the branch as failed until a valid regime exists.
5. If no valid regime exists after a bounded search, freeze or stop the branch.
6. Ensure the next report does not claim controller superiority without valid controller rows.

## Recommended Next Version
V312_FIX or V313_CLEAN

## Recommended Next Test
Smallest useful next test:
Run a minimal harness sanity check that directly forces at least one candidate with nonzero horizon metrics, and verify the validity gate passes before any controller comparison is attempted.

