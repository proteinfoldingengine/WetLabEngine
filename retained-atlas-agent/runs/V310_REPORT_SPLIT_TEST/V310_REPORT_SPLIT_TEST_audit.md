# V310_REPORT_SPLIT_TEST — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
stop or freeze, not continue in the sense of scientific interpretation.

## Execution Validator Check
Did execution_validator.py run?
Yes, per the provided execution validation output.

Did interpretation_allowed pass?
Yes.

If interpretation_allowed is false, did the report avoid scientific interpretation?
Not applicable.

Did the validator catch saturated trigger rates, invalid rows, dead horizon metrics, or missing/invalid AUC?
Yes. It flagged:
- `trigger_rate_saturated`
- `bad_rate_saturated`
- `validity_gate_false`
- `horizon_metrics_zero`
- `auc_missing` warnings on some controller rows

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No for the selected baseline and all shown candidate regimes.

If it failed, did the report avoid interpretation?
No. The report still offered toy-level interpretation language around the run, even though the validity gate failed for all displayed regimes.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes for the regimes and metrics explicitly shown.

Any invented or unsupported numbers?
Yes, the report contains unsupported framing in the abstract sense:
- It calls the run a “repair” test, but the results show no valid nondegenerate regime.
- It implies controller comparison was intended, but no valid controller-comparison row set was actually established.

The numerical values themselves in the visible sections appear consistent with stdout/results:
- selected baseline: `bad_rate = 0.0`, `trigger_rate = 0.0`, `AUC = 0.5`
- candidate regimes all shown with `bad_rate = 0.0`, `horizon_area = 0.0`, `horizon_width = 0.0`

## Code/Method Check
Was the code runnable?
Yes, syntactically it appears runnable.

Any obvious harness flaws?
Yes:
- `selected_valid` can remain false, so controller rows are never generated.
- The validity gate is applied to the baseline candidate, but all current candidates are degenerate.
- `AUC` is hard-coded to `0.5` whenever `0 < bad_rate < 1` is false, so it cannot discriminate degenerate rows.
- `accuracy = 1.0 - (bad * 0.5)` is not a proper classification accuracy over mixed outcomes; it is a surrogate tied directly to `bad`.
- `bad_rate` is only based on the simulated regime, while trigger effects are not enough to create valid regimes here.
- The run is structurally engineered to stop because the candidate space yields only `bad_rate = 0.0`.

Any degenerate regime problems?
Yes, severe:
- `bad_rate = 0.0` for all displayed candidates
- `horizon_width = 0.0` and `horizon_area = 0.0` throughout
- `trigger_rate = 0.0` throughout
- this makes controller comparison non-interpretable

## Claim Boundary Check
Any overclaiming?
Yes, mild but real.
The report says:
- “one clearly valid nondegenerate regime”
- “controller rows will be interpretable”

The actual output does not support that.

Any forbidden GR/physics language?
No major forbidden GR claims appear in the report text provided. The boundary is mostly respected.

## Current-State Consistency Check
Did the run respect current_state.md?
Partially.
It respected the current boundary by not claiming GR recovery.

Did it preserve the V307 law boundary?
No, not cleanly.
The current state says the next step is intervention validation and ablation, but only after a valid nondegenerate regime exists. This run failed to produce one, so the correct action is to stop/branch, not interpret controller comparisons.

## Required Correction
What must be fixed before next loop?
- Do not interpret this as a successful controller-validation run.
- Explicitly state that no regime passed the validity gate.
- Freeze or stop the intervention branch until a genuinely nondegenerate regime exists.
- If continuing, expand the search or alter the harness so that `bad_rate > 0`, `trigger_rate > 0.05`, and horizon metrics are nonzero in at least one selected regime.
- Ensure any future report includes the actual controller rows only if `selected_valid_for_interpretation = true`.
- Remove any claim that a valid regime was found.

## Recommended Next Version
V311_BRANCH_STOP or V311_CLEAN_FROZEN

## Recommended Next Test
Smallest useful next test:
Run a regime-search stress test designed to produce at least one nondegenerate regime with:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- nonzero `horizon_width` or `horizon_area`
before attempting controller comparisons again.