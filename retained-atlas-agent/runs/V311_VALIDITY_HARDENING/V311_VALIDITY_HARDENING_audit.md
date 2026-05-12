# V311_VALIDITY_HARDENING — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
freeze or stop this branch, not “continue” toward interpretation.

Reason:
The report itself says `overall_status: fail`, `interpretation_allowed: false`, `selected_regime_present: false`, and no valid nondegenerate regime exists. That supports stopping/freezing the branch, not treating the run as a usable validation step.

## Execution Validator Check
Did execution_validator.py run?
Yes, based on the provided execution validation MD and JSON.

Did interpretation_allowed pass?
No. It was `false`.

If interpretation_allowed is false, did the report avoid scientific interpretation?
Mostly yes. It correctly states no scientific controller conclusion is permitted. However, it still includes interpretive framing in the Results/Interpretation sections beyond the allowed boundary of a hard failure report. That is a caution, not the main error.

Did the validator catch saturated trigger rates, invalid rows, dead horizon metrics, or missing/invalid AUC?
Yes.
- saturated `bad_rate`
- saturated `trigger_rate`
- zero horizon metrics
- chance-level `AUC = 0.5`
- chance-level `balanced_accuracy = 0.5`
- no selected regime

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No.

If it failed, did the report avoid interpretation?
Mostly yes, but not completely. The report should have been more strictly non-interpretive once the gate failed.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes.

Any invented or unsupported numbers?
Yes, there are a few problems:
- The report says “for each shown regime” and lists `cases: 8`, `bad_rate: 0`, `adaptive_rate: 1`, etc. That part matches stdout.
- But the narrative claim “the harness failed the required validity gate” is grounded.
- The main numerical integrity issue is that the report presents the run as a “valid regime search” even though no valid regime exists. That is a framing error, not a fabricated number.
- The `A_c`, `A_h`, and `D_c` values match the results.
- No obvious fabricated numeric values were detected in the quoted fields.

## Code/Method Check
Was the code runnable?
Yes, structurally runnable.

Any obvious harness flaws?
Yes, several:
1. **The search space is still degenerate**  
   All tested regimes produced `bad_rate = 0`, `trigger_rate = 0`, `horizon_area = 0`, `horizon_width = 0`.

2. **Validity gate effectively cannot pass**  
   The chosen validity conditions require:
   - nonzero bad rate,
   - nonzero horizon,
   - nonzero trigger rate above 0.05.  
   But the dynamics as written appear biased toward all-adaptive outcomes. This makes the branch unlikely to produce interpretable controller rows.

3. **Controller accounting is not actually exercised**  
   Because `chosen_regime` is `null`, `controller_rows` is empty. So the stated goal of explicit controller comparison rows was not met.

4. **Potential metric mismatch**
   The code computes `horizon_area = mean(max(0.0, A_H - v) for v in a_norm)`, which is fine as a toy metric, but it still never becomes nonzero in this run.

5. **AUC logic is unstable in degenerate class regimes**
   The code falls back to `AUC = 0.5` when only one class is present, which is acceptable as a guard, but here it also hides the fact that the search produced no discriminative regime.

Any degenerate regime problems?
Yes. This is the central issue of the branch.

## Claim Boundary Check
Any overclaiming?
Yes, mildly. The report title and hypothesis imply a valid regime search, but the actual outcome is failure to find one. The report’s final decision “stop” is consistent, but the framing before that is stronger than the evidence supports.

Forbidden GR/physics language?
No forbidden overclaims were found. The report stays within toy-model language.

## Current-State Consistency Check
Did the run respect current_state.md?
Mostly yes:
- It preserved the toy-law boundary.
- It used `D_A`, `A_norm`, `A_c`, `D_c`.
- It did not elevate the claim beyond the toy.

Did it preserve the V307 law boundary?
No, not in the sense of producing a meaningful V308-style controller validation. It failed to generate the required nondegenerate control regime needed to test the V307 law in a controller setting. The law boundary itself was not contradicted, but the test did not advance it.

## Required Correction
What must be fixed before next loop?
1. Stop treating this branch as a valid controller-validation result.
2. Do not claim interpretability when `interpretation_allowed = false`.
3. Add a regime-generation strategy that can actually produce:
   - some bad cases,
   - some trigger activity,
   - nonzero horizon metrics,
   - a selected valid regime.
4. Keep a hard freeze condition if the search continues to produce all-zero horizon / all-zero trigger rows.
5. If no valid regime can be found after a revised search, stop the branch rather than expanding metrics.

## Recommended Next Version
V312_REGENERATE_REGIMES

## Recommended Next Test
Smallest useful next test:
Run a revised regime-generation sweep designed specifically to produce mixed outcomes, then require at least one candidate with:
- `bad_rate` in `(0, 1)`
- `trigger_rate > 0.05`
- `horizon_area > 0`
- valid controller rows
- held-out validation not at chance

If that still fails, freeze the controller branch.