# V310 — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
freeze or stop, not branch.

Reason: the report correctly found `chosen_regime = null` and `valid_for_interpretation = false`, so there was no valid interpretive regime. Per the constitution, that should reject component interpretation and halt this branch rather than continue as a normal branch toward ablation.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
No.

If it failed, did the report avoid interpretation?
Yes, mostly. The report explicitly said no component-law result should be read from the sweep numbers.

However, the presence of several detailed per-regime values is fine only as raw output; they were not interpreted as internal laws, so this part is acceptable.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes for the numbers actually listed.

Any invented or unsupported numbers?
Potentially unsupported / not fully grounded:
- The report says “all listed regimes had `valid_for_interpretation: false`” and `trigger_rate = 0.0` for every listed regime. This is consistent with the visible data, but the provided stdout is truncated, so the audit can only confirm the sampled entries and the top-level summary.
- No obvious fabricated summary metrics were introduced beyond the provided JSON.
- The `AUC = 1.0`, `balanced_accuracy = 1.0`, `accuracy = 1.0` values are grounded in stdout, but they are not evidence of validity because the gate failed.

No clear invented numbers were found in the report itself.

## Code/Method Check
Was the code runnable?
Yes, structurally runnable Python.

Any obvious harness flaws?
Yes, several:

1. **Seeds are not actually used in the sweep**
   - The loop iterates over `seeds 0–19`, but `simulate_regime()` is always called with `seed=12345`.
   - That means the sweep is not a fixed-seed sweep across seeds; it is a single-seed repeated-grid sweep.
   - This weakens the validity of any seed-based interpretation.

2. **The AUC computation is incorrect**
   - It uses `np.argsort(np.argsort(...))` over concatenated positive and negative scores.
   - That is not a proper rank-based AUC implementation when splitting after ranking this way.
   - For this data it may still return 1.0, but the method is fragile and potentially wrong.

3. **Degenerate regime problem persists**
   - `trigger_rate` is 0.0 for every listed regime.
   - `nonzero_trigger_rate` fails everywhere.
   - The harness does not successfully produce a valid regime.

4. **Validity gate is internally inconsistent with the method**
   - `narrow 2D grid over severity and base_failure, with a small noise check`
   - Yet seeds are not actually varied.
   - The test is not doing what the description claims.

## Claim Boundary Check
Any overclaiming?
No direct physics overclaiming in this report.

Any forbidden GR/physics language?
No forbidden claims like proving GR or spacetime were made.

The language stayed inside the toy-model boundary.

## Required Correction
What must be fixed before next loop?
- Fix the sweep so seeds are actually varied and used.
- Replace the AUC implementation with a correct rank-based or library-backed calculation.
- Redesign the harness so at least one regime can plausibly satisfy `valid_for_interpretation = true`.
- If no valid regime exists, stop this branch rather than proceeding to ablation.
- Do not call this a normal branch continuation when the gate fails.

## Recommended Next Version
V310E

## Recommended Next Test
Smallest useful next test:
- run a true seed sweep over a smaller grid
- use the actual loop seed in `simulate_regime(sev, bf, nz, seed=seed)`
- verify whether any regime achieves:
  - `nondegenerate_bad_rate = true`
  - `nonzero_trigger_rate = true`
  - `valid_for_interpretation = true`

If none do, freeze this branch and redesign the harness before any component reading.