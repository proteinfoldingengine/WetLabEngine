# V308_INTERVENTION_CLEAN — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
freeze or stop this branch, not branch.

Reason: the report itself says `D_A` did not outperform `A_norm`, and the validity gate is false for `D_A`, horizon, and baseline. Under the constitution, that is not a successful controller-validation loop.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
- baseline: false
- `D_A`: false
- horizon: false
- `A_norm`: true
- combined: true

If it failed, did the report avoid interpretation?
Not fully. The report interprets baseline and `D_A` in places despite their invalidity for interpretation. It also treats the comparison as meaningful even though the regime is degenerate for some controllers.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes for the listed aggregate numbers.

Any invented or unsupported numbers?
Yes, at least one clear issue:
- `A_norm` and `combined` are identical in the report, which is plausible from the supplied JSON, but the method claims four controllers were compared and “same seed set, same regime.” The equality itself is not invented, but it raises a harness concern because `combined` appears to collapse to `A_norm` behavior in this regime.
- The report says “baseline bad_rate range false and trigger_rate_gt_0p05 false” correctly, but then discusses severity reduction as if the comparison were valid across all controllers.
- The `Results` section mixes valid and invalid rows without clearly separating interpretation eligibility.

No obvious fabricated numeric values were found beyond the more serious issue that the harness design makes `horizon` and baseline non-informative in this regime.

## Code/Method Check
Was the code runnable?
Yes, superficially. It is syntactically runnable.

Any obvious harness flaws?
Yes:
- `horizon` trigger is effectively dead because `horizon = max(0.0, A_H - A_norm)` with `A_H = 0.1` and the simulated `A_norm` values appear always above 0.1, so horizon area and width stay zero.
- `baseline` is not a controller but is aggregated like one, then used in the same comparison table.
- `AUC` is computed from `score = max(0.0, A_C - mean_A)` for every row, but then controller labels are compared against `bad`; this is not a controller-specific scoring comparison.
- The intervention logic is saturated: both `A_norm` and `D_A` triggers fire on every seed (`trigger_rate = 1.0`), so the controller comparison is partially degenerate.
- Harm accounting is present, but all harmed counts are zero, so the controller distinction is mostly driven by bad/adaptive classification, not intervention harm.
- The validity gate is not used to block interpretation in the report.

Any degenerate regime problems?
Yes:
- `horizon_area = 0.0` and `horizon_width = 0.0` everywhere, so the horizon-area controller is non-testable here.
- `baseline.bad_rate = 1.0`, which fails the validity gate by construction.
- `D_A` validity gate is false because `bad_rate_range` is false, so it should not be used for interpretation as a controller outcome.

## Claim Boundary Check
Any overclaiming?
Yes, mild but real:
- The report frames the run as a controller comparison on a “valid regime,” but the validity gate rejects baseline, `D_A`, and horizon.
- It says `D_A` is a useful diagnostic signal, which is acceptable, but the surrounding discussion overstates the testability of the controller comparison.
- It implies the comparison can support conclusions about severity reduction without first establishing a valid comparative regime.

Any forbidden GR/physics language?
No obvious forbidden GR or universal-physics claims in the report.

## Current-State Consistency Check
Did the run respect current_state.md?
Partially.

Did it preserve the V307 law boundary?
No, not cleanly.
- It correctly concludes `D_A` did not outperform `A_norm`.
- But it violates the current-state protocol by using invalid rows for interpretation and by calling the branch “branch” rather than stopping/freezing after a negative controller-validation result.
- The current state says if `D_A` does not outperform scalar `A_norm`, preserve `D_A` as diagnostic law but keep scalar as controller. The report should therefore not escalate `D_A`; it should freeze this controller branch and keep `A_norm` as controller.
- Since the harness is degenerate for horizon and baseline, the proper response is not “branch” but a narrower retest or freeze.

## Required Correction
What must be fixed before next loop?
1. Do not interpret rows whose `valid_for_interpretation` is false.
2. Do not present the `D_A` controller as a viable intervention rule in this regime.
3. Explicitly state that horizon-area control was non-informative because horizon metrics were zero everywhere.
4. Separate valid controller comparison from invalid baseline/diagnostic rows.
5. Replace the `branch` decision with `freeze` or a narrower retest only after fixing saturation.
6. Fix the harness so at least one controller regime is not saturated and horizon is actually observable if it is to be tested.

## Recommended Next Version
V309_CLEAN

## Recommended Next Test
Smallest useful next test:
- retest `A_norm` vs `D_A` on a regime with non-saturated trigger rates and nonzero horizon metrics,
- require held-out seeds,
- and only report interpretation for rows where `valid_for_interpretation` is true.