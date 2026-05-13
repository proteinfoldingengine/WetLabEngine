# V312_LAB_CONTEXT_TEST — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
freeze

The report says `stop`, which is directionally consistent with the branch failing, but the constitution’s allowed decision set for a failed branch here is better treated as `freeze` rather than a scientific stop decision. More importantly, the report’s interpretation and selected-regime language are not fully aligned with the validator state.

## Execution Validator Check
Did execution_validator.py run?
Yes, execution validation data was provided and overall status was `pass`.

Did interpretation_allowed pass?
Yes, `interpretation_allowed: true`.

If interpretation_allowed is false, did the report avoid scientific interpretation?
N/A.

Did the validator catch saturated trigger rates, invalid rows, dead horizon metrics, or missing/invalid AUC?
Yes.
- saturated trigger rates: yes, many rows had `trigger_rate: 1.0`
- invalid rows: yes, many rows had `valid_for_interpretation: false`
- dead horizon metrics: yes, `horizon_area: 0.0` and `horizon_width: 0.0` for displayed candidates
- missing/invalid AUC: no missing AUC, but some rows had weak AUC values; validator flagged `validity_gate_false`

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No. For the displayed candidate rows, `valid_for_interpretation: false`.

If it failed, did the report avoid interpretation?
Mostly yes, but not cleanly. The report still made a substantive meta-interpretation about harness failure and “candidate quality was insufficient,” which is acceptable only as a toy-level procedural statement. However, it also implied controller-comparison context that was not actually available because `valid_controller_row_count: 0`.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes.

Any invented or unsupported numbers?
Potentially yes / unsupported:
- The report says “the harness can generate candidate rows” — supported.
- The report says “it did not produce a valid nondegenerate horizon regime in this run” — supported.
- The report’s “Selected-regime summary: none selected” is supported.
- However, the report frames `overall validation: pass` as if it supports the run meaningfully, while the actual usable interpretation is blocked by `valid_for_interpretation: false` for all displayed rows.
- The report also mentions “controller comparison rows” as part of the test objective, but no valid controller rows existed. That is not an invented number, but it is an unsupported implication if read as achieved.

## Code/Method Check
Was the code runnable?
Yes. The code is syntactically runnable and deterministic.

Any obvious harness flaws?
Yes, several:
- The harness hard-codes a synthetic rule where `a_series` is “already normalized toy series”; this may be acceptable for a toy, but it means `A_norm` is not derived from a separate baseline in the stated canonical sense.
- `horizon_width` is binary-ish (`1/len(a_series)` if `min_a_norm < A_h`) rather than a genuine width measure.
- `trigger_DA` is never used to select the combined controller in the shown valid rows; `trigger_combined` dominates.
- `acc = max(adaptive_rate, bad_rate)` is not a standard accuracy definition.
- The `validity_gate` requires `horizon_nonzero`, but the results show this is false for all shown candidates.
- Many rows saturate at `trigger_rate: 1.0`, which is exactly the degeneracy the validator warns about.

Any degenerate regime problems?
Yes.
- Several regimes have `bad_rate: 1.0` or `trigger_rate: 1.0`
- horizon metrics are zero across the displayed candidates
- selected regime is absent
- controller rows are absent because no selected valid regime survived

## Claim Boundary Check
Any overclaiming?
No hard forbidden GR/physics overclaiming was present in the report.

Any forbidden GR/physics language?
No forbidden language detected in the report body.

## Current-State Consistency Check
Did the run respect current_state.md?
Partially.
- It respected the toy-model framing.
- It did not produce a valid controller-validation regime, which is consistent with the “stop branch if invalid” rule.
- But the report’s title and method imply a repair test, while the actual result is a branch failure with no interpretable controller comparison.

Did it preserve the V307 law boundary?
Yes. It did not attempt to overturn V307’s `D_A` law status.
But it also did not validate `D_A` as an intervention controller.

## Required Correction
What must be fixed before next loop?
- Freeze or stop this branch explicitly as a failure branch.
- Do not interpret controller comparisons from this run.
- Do not present the branch as a successful repair test.
- If continuing, the next harness must produce at least one selected regime with:
  - `bad_rate > 0`
  - `trigger_rate > 0.05`
  - `horizon_area > 0` or `horizon_width > 0`
  - `valid_for_interpretation: true`
  - explicit controller rows surviving the gate
- If the branch is not fixed, it should not proceed to intervention claims.

## Recommended Next Version
V313_FREEZE

## Recommended Next Test
Smallest useful next test:
freeze this branch and rerun only after the harness is changed so that at least one regime can satisfy the validity gate, especially `horizon_nonzero = true`, before any controller comparison is interpreted.