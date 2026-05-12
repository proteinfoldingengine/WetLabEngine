# V310 — Harness Repair Validation Test

## Question
Can the harness produce one valid regime with nonzero bad cases and nonzero trigger activity?

## Hypothesis
If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
1. Sweep a narrow 2D grid over severity and base_failure, with a small noise check.
2. Use fixed seeds across all candidates.
3. Compute real classification metrics only when both labels are present; otherwise omit AUC.
4. Select a regime only if `valid_for_interpretation = true`.
5. If no valid regime is found, report harness failure and stop before ablation.

## Controls
- fixed seeds
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- all reported numbers written to JSON and stdout

## Results
Numbers only where possible.

## Interpretation
Inside the toy, this test only asks whether the harness can enter a valid regime.
It does not interpret component ablation unless the validity gate passes.

## Failure / Caveat
If `chosen_regime` is null, the run is a harness failure.

## Decision
continue / branch / stop / freeze based on validity gate

## Next
Smallest useful next test: if no valid regime is found, redesign the harness again before any ablation.
