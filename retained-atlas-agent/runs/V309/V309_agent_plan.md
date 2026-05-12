# V309 — Component Ablation Test

## Question
Which components inside the adaptive reachability law contribute the most to prediction and intervention behavior?

## Hypothesis
If the toy law stack is genuinely compressive, then ablation of one component at a time should measurably degrade discrimination or intervention utility, especially for components that carry unique information.

## Method
Run a fixed-seed toy simulation across the same seeds and dynamics used in prior loops. Compute the full adaptive reachability score and one-component ablations by removing each factor from the geometric mean:
- recovery-front speed
- corridor width
- branching entropy
- detox radius
- reversible-state fraction

Then compare each ablated score against the full score on held-out seeds using:
- AUC
- balanced accuracy
- accuracy
- correlation with bad state label
- mean separation between bad and safe states

Also report whether ablation changes intervention trigger behavior under the same D_A threshold.

## Controls
- Fixed seeds
- Shared shock schedule
- Held-out split for evaluation
- Same threshold across all variants
- No threshold tuning

## Results
Numbers only.

## Interpretation
Identify which components are redundant and which are necessary for the toy law to keep explanatory power.

## Failure / Caveat
If all ablations behave similarly, the current composite law may be overbuilt or internally redundant.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: if one ablation clearly degrades performance, stress that component under noisy and sparse topologies; otherwise freeze and report redundancy.
