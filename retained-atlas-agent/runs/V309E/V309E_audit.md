# V309E — Audit Report

## Audit Verdict
warning

## Decision Check
Was the reported decision justified?
Yes, given the reported gate failure and `chosen_regime: null`, `branch` was justified.

Expected decision if different:
None; `branch` matches the stated validity failure.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No.

If it failed, did the report avoid interpretation?
Mostly yes. The interpretation stayed at harness/regime-failure level and did not claim component importance.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes. The listed regime values match the provided stdout.

Any invented or unsupported numbers?
Potentially yes:
- The report presents only selected sweep points, but not the full sweep. That is acceptable if clearly labeled as selected, which it was.
- However, the `REPORT` text says “No valid regime was found,” which is supported by `chosen_regime: null`.
- One caution: the JSON file is missing in the prompt, so I cannot independently verify stdout against the saved results file.

## Code/Method Check
Was the code runnable?
Mostly yes.

Any obvious harness flaws?
Yes:
- The code averages per-seed AUC values even when some seeds have undefined AUC; it catches exceptions and substitutes `0.5`, which can mask degeneracy.
- The `validity_gate` is computed twice: once per seed and once on aggregated regime values. That is not necessarily wrong, but it complicates interpretation.
- The trigger condition may be too strict or poorly coupled to the bad-label regime, since `trigger_rate` stayed at `0.0` across the shown points.
- The sweep appears to have many degenerate points with all-safe labels, making AUC undefined and some metrics uninformative.

Degenerate regime problems?
Yes:
- Multiple regimes had `bad_rate = 0`.
- Many points had `trigger_rate = 0.0`.
- The intended nondegenerate window was not found.

## Claim Boundary Check
Any overclaiming?
No major overclaiming in the report itself.

Any forbidden GR/physics language?
No forbidden claims. Only toy-model / GR-adjacent language appears, and it stays within the boundary.

## Required Correction
What must be fixed before next loop?
- The harness must be redesigned so the sweep can actually reach a regime with:
  - `bad_rate` in `[0.20, 0.40]`
  - `trigger_rate > 0.05`
  - nonzero score variance
  - enough positive bad cases
- Avoid using fallback AUC values that hide degenerate label cases, or report them explicitly as undefined.
- Provide the full sweep results or a compact table with the best candidate and the worst degenerate cases, so the gate failure is transparent.

## Recommended Next Version
V309F

## Recommended Next Test
Smallest useful next test:
Run a narrower harness calibration that explicitly tunes the trigger definition and bad-label calibration on held-out seeds, then re-check whether any regime satisfies the interpretation gate before attempting component ablation.