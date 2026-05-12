# V308 — Deficit Intervention Threshold Test

## Question
Does triggering full staged repair at `D_A > D_c` outperform scalar `A_norm`, horizon area, and combined triggers on the valid regime?

## Hypothesis
If the deficit law is the better controller, then `D_A` trigger should match or slightly outperform scalar `A_norm` trigger on rescue, with similar or lower harm, across the same seed set.

## Method
Evaluate four controllers on the validated regime:
- scalar `A_norm` trigger
- `D_A` trigger
- horizon-area trigger
- combined trigger

Use the same seed set and the same baseline protocol for all controllers. Report baseline bad rate, treated bad rate, adaptive rate, trigger rate, rescued, harmed, net rescue, severity reduction, and phase counts.

## Controls
- same seeds across all controller conditions
- same baseline protocol
- explicit harm accounting
- no threshold tuning after validation
- no component ablation
- no claim escalation
- all numbers grounded in stdout or saved JSON
- do not hardwire one trigger rule and call it a comparison

## Results
To be filled by execution.

## Interpretation
To be filled by execution.

## Failure / Caveat
To be filled by execution.

## Decision
branch

## Next
Smallest useful next test: run the actual controller comparison on the valid regime and verify whether `D_A` trigger outperforms or at least matches the scalar trigger without increasing harm.
