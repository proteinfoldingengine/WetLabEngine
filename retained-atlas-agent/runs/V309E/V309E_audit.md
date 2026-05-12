# V309E — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No. The report’s `branch` decision is consistent with `chosen_regime: null` and `valid_for_interpretation: false`.

Expected decision if different:
If the code had found a valid regime, the decision should have been `continue`. Given the reported outputs, `branch` is appropriate.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No.

If it failed, did the report avoid interpretation?
Mostly yes. The report explicitly says no valid regime was found and does not make component-level claims. However, it still provides an interpretation section; that is acceptable only because it stays within the toy and says the run is a harness/regime failure.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes for the numbers explicitly shown in `STDOUT` / `RESULTS JSON`.

Any invented or unsupported numbers?
Potentially yes by omission/ambiguity:
- The report states “Selected sweep outputs” and lists several regimes, but the provided JSON/stdout are truncated before the full sweep is shown in the prompt. Those specific listed rows are present in the visible `RESULTS JSON` section, so they are grounded.
- No obvious invented numbers inside the visible portion.
- However, the report does not state whether the listed sweep points were the only ones examined or just examples. That is a presentation issue, not necessarily fabrication.

## Code/Method Check
Was the code runnable?
Yes, it appears runnable Python.

Any obvious harness flaws?
Yes, a major one:
- `bad_rate` is 0.0 for all shown regimes, so the validity gate is impossible to satisfy under the current parameterization.
- `trigger_rate` is also 0.0 everywhere shown.
- The harness may be “seed-sensitive” in code, but the chosen dynamics still do not produce any bad cases in the tested grid.

Any degenerate regime problems?
Yes:
- All reported regimes are degenerate on the target labels (`bad_rate = 0.0`).
- This makes `AUC = 0.5` and balanced accuracy = 0.5 for the shown cases.
- Because `valid_for_interpretation = false`, no component interpretation should proceed.
- The code computes a custom AUC, which is acceptable, but it is uninformative under all-safe labels.

## Claim Boundary Check
Any overclaiming?
No major overclaiming. The report stays inside the toy boundary and labels the result as a harness/regime failure.

Any forbidden GR/physics language?
No forbidden claim-level language detected in the report. It uses toy-model wording appropriately.

## Required Correction
What must be fixed before next loop?
- The harness must produce at least one nondegenerate regime with `bad_rate > 0` and `trigger_rate > 0`.
- Do not proceed to any component ablation while `chosen_regime` is null.
- The sweep window likely needs expansion or dynamics need retuning so the bad class actually occurs.
- If the run is meant to audit seed sensitivity, the report should include a compact seed-by-seed summary or a seed-wise variance check, not only aggregated values.

## Recommended Next Version
Example: V309F

## Recommended Next Test
Smallest useful next test:
Expand the regime search just enough to find any regime with nonzero `bad_rate` and nonzero `trigger_rate`, then re-run the validity gate before any ablation.