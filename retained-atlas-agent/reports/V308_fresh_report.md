# V308_fresh — Narrow Calibration Repair Test

## Question
Can the repaired narrow calibration sweep produce one valid regime with nonzero bad cases and nonzero trigger activity?

## Hypothesis
If the harness is repaired, then at least one narrow seed/regime combination should satisfy the validity gate and produce interpretable scores.

## Method
Executed a narrow regime sweep over compact parameter settings with actual varying seeds passed into `simulate_regime(sev, bf, nz, seed=seed)`. The run evaluated 18 candidate regimes and used the reported validity gate to select a regime only if labels and trigger activity were nondegenerate.

## Controls
- Actual varying seeds were used.
- Shared simulation code was used across all candidate regimes.
- No threshold tuning was performed after validation.
- No ablation was performed before the validity gate passed.
- A compact seed-wise sweep was used.
- Interpretation was limited to stdout values only.

## Results
- `version`: `V308_fresh`
- `candidate_count`: `18`
- `chosen_regime`: `{ "bf": 0.35, "nz": 0.08, "sev": 0.65 }`
- `validity_gate`: `true`
- `bad_rate`: `0.25`
- `adaptive_rate`: `0.75`
- `AUC`: `1.0`
- `balanced_accuracy`: `1.0`
- `accuracy`: `1.0`
- `trigger_rate`: `0.25`
- `rescued`: `2`
- `harmed`: `0`
- `net_rescue`: `2`
- `horizon_area`: `0.0`
- `horizon_width`: `0.0`
- `pinch`: `0.7581631378918791`
- `mean_A_norm`: `0.6092966375811072`
- `min_A_norm`: `0.20304312114241085`
- `score_mean`: `0.03279126411103692`
- `score_var`: `3.05226861143741e-05`
- `late_K`: `0.4713381728052584`
- `late_mobility`: `0.651815174475219`
- `late_residual`: `0.04101561764065294`
- `phase_counts`: `{ "adaptive": 6, "bad": 2, "horizon": 0 }`

Selected candidate details:
- `bf`: `0.35`
- `nz`: `0.08`
- `sev`: `0.65`
- `bad_rate`: `0.25`
- `trigger_rate`: `0.25`
- `rescued`: `2`
- `harmed`: `0`

## Interpretation
This run produced one valid narrow regime and therefore repaired the immediate calibration failure. Inside the toy, the controller now has a nondegenerate case where bad outcomes occur and are partially rescued.

The result supports the current toy-level intervention claim:
- the sweep can now find a regime with both bad cases and trigger activity,
- the chosen regime is interpretable under the current gate,
- the harness is no longer stuck in the null-regime failure mode.

It does not show that the controller is optimal across the full space, only that the narrow calibration branch now yields a valid test case.

## Failure / Caveat
- `horizon_area` and `horizon_width` were both `0.0` in the selected regime.
- The run does not establish broader robustness outside this narrow window.
- Several candidate regimes still had `bad_rate = 0.0` or `bad_rate = 1.0`, so the sweep remains regime-sensitive.
- This is a toy-model calibration result only.

## Decision
branch

## Next
Smallest useful next test: run the full V308 intervention comparison on the valid regime and compare trigger rules against the baseline using the same seed set, with harm accounting preserved.