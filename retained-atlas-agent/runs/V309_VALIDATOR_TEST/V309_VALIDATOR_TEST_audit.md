# V309_VALIDATOR_TEST — Audit Report

## Audit Verdict
warning

## Decision Check
Was the reported decision justified?
No, not fully. The report chose `branch`, which is consistent with the validation failure pattern, but the scientific interpretation is not justified because the run did not clearly produce a valid comparison row.

Expected decision if different:
`freeze` or `branch` are both defensible, but only with explicit note that the harness did not yield an interpretable candidate and that the loop should not be treated as successful validation.

## Execution Validator Check
Did execution_validator.py run?
No evidence that `execution_validator.py` itself ran; only an execution-validation payload was provided.

Did interpretation_allowed pass?
Yes, `interpretation_allowed: true`.

If interpretation_allowed is false, did the report avoid scientific interpretation?
N/A.

Did the validator catch saturated trigger rates, invalid rows, dead horizon metrics, or missing/invalid AUC?
Partially yes. The validity gate flagged:
- invalid rows
- dead horizon metrics
- saturated / zero trigger rates
- bad-rate range failures
- AUC present in most cases, but `chosen_regime` had `auc_missing` warning

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
For `chosen_result`, yes: `valid_for_interpretation: true`.
But the broader run is still weak because most candidates were invalid and the chosen row appears to be only one valid regime out of ten.

If it failed, did the report avoid interpretation?
N/A for the chosen row, but the report correctly limited interpretation.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes. The report numbers match the provided `chosen_result` payload:
- `cases = 8`
- `AUC = 1.0`
- `accuracy = 0.625`
- `balanced_accuracy = 0.5`
- `adaptive_rate = 0.625`
- `bad_rate = 0.375`
- `trigger_rate = 0.375`
- `rescued = 3`
- `harmed = 0`
- `net_rescue = 3`
- `horizon_width = 0.015625`
- `horizon_area = 0.0009444676716278774`
- `mean_A_norm = 0.7007971990647466`
- `min_A_norm = 0.03955406901581585`
- `pinch = 0.8982301005046848`

Any invented or unsupported numbers?
Yes, potentially two issues:
1. The report says “one nondegenerate regime inside the search neighborhood” and “controller comparisons are meaningful,” but the output provided does not actually show a controller comparison among multiple triggers. It only shows one chosen valid regime and no evidence of the requested comparison set.
2. The report says “horizon-like metrics became nonzero for at least one seed,” which is supported, but the broader claim that the harness can produce a valid comparison row is only weakly supported because most candidate rows are invalid and there is no full controller comparison output.

## Code/Method Check
Was the code runnable?
Mostly yes. The code is syntactically runnable.

Any obvious harness flaws?
Yes:
- `mean_A_norm` is computed as `mean_A / A_baseline`, not the mean of the normalized time series `A_norm`; that is likely inconsistent with the stated metric.
- `min_A_norm` is `min_A / A_baseline`, not `min(A_norm)`.
- The code computes `horizon_width` and `horizon_area`, but no actual controller comparison beyond a single `D_A` trigger is shown in the summarized output.
- The chosen-regime search is narrow and seems predisposed to invalidity; many candidates have `bad_rate = 0.0`, `trigger_rate = 0.0`, and `horizon_area = 0.0`.
- The selection rule uses `max(valid, ...)` with a default of `None`, but the report does not explicitly state whether the selected row came from a genuine controller-comparison set or only from a regime search.

Any degenerate regime problems?
Yes. Most candidates are degenerate:
- `bad_rate = 0.0`
- `trigger_rate = 0.0`
- `horizon_width = 0.0`
- `horizon_area = 0.0`
- balanced accuracy often `0.5`

## Claim Boundary Check
Any overclaiming?
A little. The statement “This supports the claim that the harness can produce a valid comparison row in a narrow regime band” is too strong relative to the evidence. It supports only that one regime passed the validity gate.

Forbidden GR/physics language?
No obvious forbidden claim escalation in the report. It stays within toy-model language.

## Current-State Consistency Check
Did the run respect current_state.md?
Mostly yes:
- stayed within toy-model framing
- preserved the `D_A` boundary
- did not claim GR recovery
- did not elevate to physical interpretation

Did it preserve the V307 law boundary?
Yes. It did not revise the `D_A` law.

## Required Correction
What must be fixed before next loop?
1. Remove or correct the inconsistent normalization metrics:
   - `mean_A_norm` should be the mean of `A_norm`
   - `min_A_norm` should be the minimum of `A_norm`
2. Provide explicit controller comparison output if the loop is about intervention thresholds.
3. State clearly that most candidate regimes were invalid and that only one regime passed validation.
4. Avoid phrasing that implies broad robustness from a single valid regime.
5. If the next loop is ablation, restrict it to the valid nondegenerate regime and report held-out validation, not just seed-wise outputs.

## Recommended Next Version
V309_CLEAN

## Recommended Next Test
Smallest useful next test:
Run the requested intervention comparison on the single valid regime, with explicit controllers:
- scalar `A_norm` trigger
- duration-below-`A_c` trigger
- integrated deficit `D_A` trigger
- horizon-area trigger
- combined trigger

Report:
- bad rate
- adaptive rate
- trigger rate
- rescued
- harmed
- net rescue
- severity reduction
- phase counts

