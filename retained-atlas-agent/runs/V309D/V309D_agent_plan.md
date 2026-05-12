# V309D — Regime repair for valid component ablation

## Question
Can we find a nondegenerate regime for the reachability-law ablation where the full score is interpretable?

## Hypothesis
If the harness is repaired, then a 2D sweep over severity and base_failure/intercept/noise should produce at least one regime with:
- bad_rate in [0.20, 0.40]
- trigger_rate > 0.05
- score variance > 0
- enough positive bad cases

Only then should component ablation be interpreted.

## Method
Run a compact fixed-seed sweep over severity and base_failure/intercept/noise. For each candidate regime:
1. simulate the toy system
2. compute bad_rate, adaptive_rate, trigger_rate, score variance, phase counts
3. evaluate validity_gate
4. choose the first valid regime only if it satisfies the interpretation gate
5. if no valid regime is found, report that explicitly and stop the branch

## Controls
- fixed seeds
- shared simulation code across sweep points
- no threshold tuning after validation
- no regime selection outside the target bad-rate window
- report the full sweep, not just the closest regime

## Results
Will be filled by execution.

## Interpretation
If no valid regime is found, this is a harness/regime failure, not a law failure.

## Failure / Caveat
Previous V309/V309B/V309C runs were invalid or degenerate. This run must not reuse a regime merely because it is closest.

## Decision
branch if no valid regime is found; otherwise continue to component ablation only inside the valid regime.

## Next
Smallest useful next test: if a valid regime is found, run held-out component ablation in that regime; otherwise branch to a deeper harness redesign.
