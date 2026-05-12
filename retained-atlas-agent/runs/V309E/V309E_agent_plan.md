# V309E — Seed-sensitive harness repair test

## Question
Can the harness produce one valid regime when seeds are actually varied and the scoring metric is computed correctly?

## Hypothesis
If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
1. Use a narrower calibration sweep than before.
2. Vary the actual loop seed in `simulate_regime(sev, bf, nz, seed=seed)`.
3. Use a correct AUC implementation or omit AUC entirely if it is not meaningful.
4. Search only the smallest necessary regime window needed to test validity.
5. Report the full validity gate for the selected regime.
6. If `chosen_regime` remains null, stop and label the run as a harness failure.

## Controls
- fixed seeds, but actually passed into the simulation
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- all reported numbers must be traceable to stdout or saved JSON
- do not reuse a single seed while claiming a seed sweep

## Results
Numbers only where possible.

## Interpretation
The result must be interpreted only inside the toy system.

## Failure / Caveat
If `chosen_regime` is null, the harness failed and ablation must not proceed.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: if a valid regime is found, run held-out component ablation in that same regime; otherwise redesign the harness again.
