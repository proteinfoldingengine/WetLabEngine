# V309 — Narrow Regime Validity Test

## Question
Can we find a non-saturated regime where at least one horizon metric becomes nonzero and controller comparisons are meaningful?

## Hypothesis
If the regime is adjusted into a less degenerate range, then trigger rates will not saturate and horizon metrics may become nonzero for at least some seeds.

## Method
Searched a compact regime neighborhood around the current validated band using the existing baseline protocol and fixed seed family. Evaluated candidate regimes on:
- `bad_rate`
- `adaptive_rate`
- `AUC`
- `balanced_accuracy`
- `trigger_rate`
- `rescued`
- `harmed`
- `net_rescue`
- `horizon_width`
- `horizon_area`
- `phase_counts`
- variant-level performance

Applied the validity gate before interpretation.

## Controls
- same baseline protocol
- fixed seed family
- held-out validation logic through validity gate
- explicit harm accounting
- no threshold tuning after validation
- no component ablation
- no claim escalation
- invalid rows excluded from interpretation

## Results
```text
A_c = 0.527
A_h = 0.1
D_c = 0.0388
candidate_count = 10
valid_candidate_count = 1
```

Chosen regime:
```text
bf = 0.45
nz = 0.08
sev = 0.75
```

Chosen result:
```text
cases = 8
AUC = 1.0
accuracy = 0.625
balanced_accuracy = 0.5
adaptive_rate = 0.625
bad_rate = 0.375
trigger_rate = 0.375
rescued = 3
harmed = 0
net_rescue = 3
horizon_width = 0.015625
horizon_area = 0.0009444676716278774
mean_A_norm = 0.7007971990647466
min_A_norm = 0.03955406901581585
pinch = 0.8982301005046848
phase_counts = {"adaptive": 5, "bad": 3, "horizon": 1}
```

Validity gate:
```text
auc_metric_real = true
bad_rate_range = true
chosen_regime_not_null = true
horizon_nonzero = true
phase_counts_bad_gt_0 = true
trigger_rate_gt_0p05 = true
valid_for_interpretation = true
```

Variant-level performance for the valid regime:
```text
seed 101: D_A 0.05402744593696994, adaptive 0, bad 1, duration_below_Ac 0.5, horizon_area 0.0, horizon_width 0.0, triggered 1
seed 203: D_A 0.032896886060629286, adaptive 1, bad 0, duration_below_Ac 0.25, horizon_area 0.0, horizon_width 0.0, triggered 0
seed 307: D_A 0.018630248681391383, adaptive 1, bad 0, duration_below_Ac 0.25, horizon_area 0.0, horizon_width 0.0, triggered 0
seed 409: D_A 0.10476994346414584, adaptive 0, bad 1, duration_below_Ac 0.5, horizon_area 0.0, horizon_width 0.0, triggered 1
seed 503: D_A 0.02646396861854749, adaptive 1, bad 0, duration_below_Ac 0.25, horizon_area 0.0, horizon_width 0.0, triggered 0
seed 607: D_A 0.024269113948985892, adaptive 1, bad 0, duration_below_Ac 0.25, horizon_area 0.0, horizon_width 0.0, triggered 0
seed 701: D_A 0.003617396580164245, adaptive 1, bad 0, duration_below_Ac 0.125, horizon_area 0.0, horizon_width 0.0, triggered 0
seed 809: D_A 0.14018158461988756, adaptive 0, bad 1, duration_below_Ac 0.5, horizon_area 0.007555741373023019, horizon_width 0.125, triggered 1
```

## Interpretation
This run found one nondegenerate regime inside the search neighborhood. Inside that toy regime, horizon-like metrics became nonzero for at least one seed, and the controller produced non-saturated outcomes:
- bad rate was 0.375, not degenerate
- trigger rate was 0.375, not saturated
- horizon width and horizon area were nonzero
- harm remained 0
- net rescue was 3

This supports the claim that the harness can produce a valid comparison row in a narrow regime band. It does not by itself update the core law. It only shows that the previous all-adaptive degeneracy was regime-limited, not necessarily a failure of the reachability stack.

## Failure / Caveat
Most candidates still failed validity:
- `valid_candidate_count = 1` out of `10`
- many regimes had `bad_rate = 0.0`
- many regimes had `trigger_rate = 0.0`
- many regimes had `horizon_area = 0.0`
- several rows had `balanced_accuracy = 0.5`, so discrimination was limited
- one valid row does not establish broad robustness

## Decision
branch

## Next
Smallest useful next test: run V309 ablation only on the valid nondegenerate regime, then compare whether removing `recovery-front speed`, `corridor width`, `branching entropy`, `detox radius`, or `reversible-state fraction` changes `D_A`-based explanation or intervention behavior.