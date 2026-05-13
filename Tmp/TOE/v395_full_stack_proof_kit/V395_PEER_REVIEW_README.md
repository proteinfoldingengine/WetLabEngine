# V395 Full-Stack Proof Kit — Reachable Adaptive Futures Law

## Law candidate

The tested structure is:

```text
A_t = M_t × R_t
```

where:

```text
M_t = adaptive safety margin
R_t = retained memory / future capacity
```

Collapse risk is modeled as:

```text
A_t < A_floor(t)
```

where the dynamic floor is internally generated:

```text
A_floor(t) rises with turbulence
A_floor(t) falls with recovery velocity
A_floor(t) rises mildly when retained capacity is depleted
```

The controller is not just “reduce bad outcomes.” It is:

```text
maximize future reachability subject to reserve preservation
```

## What the script tests

The Python script tests five layers:

1. **Product law**: whether `M × R` predicts collapse better than treating margin and memory separately.
2. **Dynamic floor**: whether collapse is better expressed as product below a moving survivability floor.
3. **Reserve rule**: whether product repair is safe only when retained capacity can absorb intervention cost.
4. **Hierarchy**: whether the explicit sequence holds:
   - preserve R
   - lower A_floor
   - repair M × R
   - exit with reserve confirmation
5. **Emergence test**: whether a single future-reachability optimizer naturally selects the same action pattern without being given the hierarchy.

## How to run in Colab

Upload `v395_full_stack_proof.py`, then run:

```python
!python v395_full_stack_proof.py
```

The script creates:

```text
v395_outputs/
  summary_results.csv
  ablation_results.csv
  regime_results.csv
  trajectory_sample.csv
  v395_summary.json
  plots/
    controller_tradeoff.png
    hierarchy_ablation.png
    regime_robustness.png
    trajectory_explicit_hierarchy.png
    trajectory_future_reachability_optimizer.png
    trajectory_greedy_bad_minimizer.png
```

## What would validate the claim

The law candidate is supported if:

```text
1. A_floor - (M × R) predicts collapse with useful AUC.
2. Future-reachability optimizer behaves similarly to explicit hierarchy.
3. Greedy bad minimizer reduces collapse only by increasing harm or reclosure.
4. Removing hierarchy steps creates distinct failure modes.
5. Results are stable across seeds, regimes, and horizons.
```

## What would falsify or weaken it

The law candidate is weakened if:

```text
1. M-only or R-only control consistently matches product control.
2. A_floor cannot be reconstructed from internal variables.
3. Future-reachability optimization does not recover the hierarchy.
4. Ablations do not produce distinct failure modes.
5. The result disappears under seed sweeps or parameter perturbations.
```

## Important peer-review caveat

This is a computational proof-of-structure, not a proof of physical reality. The surrogate is synthetic. The correct scientific next step is to map:

```text
M_t, R_t, turbulence, recovery velocity, intervention cost
```

to concrete observables in the real target domain and rerun the same ablation stack.
