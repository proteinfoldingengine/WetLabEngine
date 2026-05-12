# V309F — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
branch is only justified if the report cleanly shows the validity gate failed and no interpretation was made beyond that. The decision itself matches the null regime, but the audit must reject this run because the report/code/results are internally inconsistent and the required validity structure is not clearly respected.

## Validity Gate Check
Did validity_gate exist?
Yes, at least in the code and in the JSON/results shown.

Did valid_for_interpretation pass?
No.

If it failed, did the report avoid interpretation?
Mostly yes at the top level, but the report still includes component-style language about “reachability-law component tests” and claims the sweep is a “regime-repair sweep before ablation” with detailed numeric summaries that are not cleanly tied to a valid regime. Since `chosen_regime` is null, component interpretation should be fully rejected.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Partly, but not reliably.

Any invented or unsupported numbers?
Yes, there are signs of unsupported or at least ungrounded numbers:
- The user-provided report contains selected “representative sweep outputs” that are not obviously traceable from the truncated stdout alone.
- The stdout is truncated mid-entry, so the audit cannot verify the completeness of the reported sweep values.
- The code prints and saves the full JSON, but the report presents only a subset of sweep points without a demonstrated selection rule beyond “representative.”
- The top-level summary says `chosen_regime: null`, but the report still implies the sweep found meaningful per-regime variance; that is numerically true, but not enough for interpretation.
- More importantly, the code itself contains a questionable `AUC` implementation that collapses to `0.5` or `1.0` based on set cardinality, not true ranking performance. That makes the reported AUC numerically weak and potentially misleading.

## Code/Method Check
Was the code runnable?
Likely yes, syntactically runnable.

Any obvious harness flaws?
Yes:
- `AUC` is not computed as a real AUC; it is a degenerate placeholder.
- The sweep target is a bad-rate window, but all shown regimes have `bad_rate = 0.0`, so the harness failed to generate the required regime.
- `accuracy = 1.0` everywhere shown, which suggests the classification setup is degenerate.
- The report says “No ablation was run because no valid regime was found,” which is consistent.
- The code includes a dead/irrelevant line `mean_bad = ...` inside `comp_run`, which is unused.
- The component ablation block is present but should not execute because no valid regime was found; that part is fine.
- There is a regime-selection issue: all entries shown have `trigger_rate = 0.0`, so the validity gate cannot pass.

Any degenerate regime problems?
Yes, severe degeneracy:
- zero bad cases across the displayed sweep
- zero trigger activity across the displayed sweep
- AUC stuck at 0.5
- balanced accuracy stuck at 0.5
- accuracy stuck at 1.0
This is exactly the kind of degenerate regime the constitution says should not be interpreted.

## Claim Boundary Check
Any overclaiming?
Some, but not extreme.
- The phrase “reachability-law component tests” is acceptable toy language, but it edges toward component-law interpretation without a valid regime.
- The report correctly says not to interpret ablation if the validity gate fails.
- No strong overclaiming into physics appears in the report.

Any forbidden GR/physics language?
No forbidden GR/physics claims appear in the report text provided.

## Required Correction
What must be fixed before next loop?
- Use a real metric implementation for AUC, or drop AUC entirely if it is not meaningful.
- Produce a regime with nonzero bad cases and nonzero trigger activity before any component-level interpretation.
- Ensure the report explicitly rejects interpretation whenever `chosen_regime` is null.
- Remove any hint of component-law inference from a failed harness sweep.
- Make the validity gate a first-class reported object at the top level and ensure the report states it clearly and consistently.
- Verify that every numeric value in the narrative is directly traceable to stdout or the saved JSON.

## Recommended Next Version
V309G

## Recommended Next Test
Smallest useful next test:
repair the harness to generate at least one held-out regime with:
- `0.20 <= bad_rate <= 0.40`
- `trigger_rate > 0.05`
- `phase_counts.bad > 0`
- a real AUC calculation
Then rerun the sweep and only if valid, attempt ablation.