# V309 — Narrow Regime Validity Test

## Question
Can we find a non-saturated regime where at least one horizon metric becomes nonzero and controller comparisons are meaningful?

## Hypothesis
If the regime is adjusted into a less degenerate range, then trigger rates will not saturate and horizon metrics may become nonzero for at least some seeds.

## Method
Search a compact regime neighborhood around the current validated band using fixed seeds and the existing baseline protocol. Measure whether any candidate regime yields nonzero horizon width/area, non-saturated trigger rates, and a valid controller comparison row. Preserve held-out validation logic if a comparison is made. Do not ablate components or tune thresholds after validation.

## Controls
- same baseline protocol
- fixed seed family
- held-out validation if applicable
- explicit harm accounting
- no threshold tuning after validation without validation metrics
- no component ablation yet
- no claim escalation
- no mixing of invalid and valid rows in interpretation

## Results
To be filled by the run.

## Interpretation
To be filled by the run.

## Failure / Caveat
To be filled by the run.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: determine whether the harness can produce a nondegenerate regime before any ablation.
