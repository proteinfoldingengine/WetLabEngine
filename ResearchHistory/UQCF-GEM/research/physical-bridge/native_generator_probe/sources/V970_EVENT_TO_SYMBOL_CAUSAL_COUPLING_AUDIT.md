# V970 Event-to-Symbol Causal Coupling Audit

## Verdict

`event_to_symbol_causal_coupling_certified`

Closed for V970 event-symbol coupling: **True**

## Purpose

V969 found a stronger boundary:

```text
a near-manifold symbolic mimic can pass behavior-only checks and radius-envelope checks.
```

V970 tests whether the emitted Q/S symbols are predictable from event dynamics in certified generators, and whether the mimic breaks that coupling.

## Certified event-to-symbol predictability

| symbol_target   |   leave_domain_out_accuracy |   n_classes |
|:----------------|----------------------------:|------------:|
| Q_obs           |                    0.954861 |           5 |
| S_ternary       |                    0.878968 |           3 |
| QS_pair         |                    0.876488 |          11 |
| true_class      |                    0.870536 |           7 |

## Thresholds

```text
QS-pair coupling threshold: 0.8265
Q/S component coupling threshold: 0.8290
```

## Candidate coupling scores

| candidate_generator                    | candidate_family                |   rows |   q_match_rows |   s_match_rows |   pair_match_rows |   qs_component_match_rows |   true_class_match_rows |   q_match_rate |   s_match_rate |   pair_match_rate |   qs_component_match_rate |   true_class_match_rate | event_symbol_coupling_certified   | behavior_only_certified   | radius_envelope_certified   | causal_coupling_certified   |
|:---------------------------------------|:--------------------------------|-------:|---------------:|---------------:|------------------:|--------------------------:|------------------------:|---------------:|---------------:|------------------:|--------------------------:|------------------------:|:----------------------------------|:--------------------------|:----------------------------|:----------------------------|
| candidate_certified_control_V957       | compatible_control              |    240 |            240 |            240 |               240 |                       240 |                     240 |       1        |       1        |         1         |                 1         |                1        | True                              | True                      | True                        | True                        |
| candidate_certified_control_V960       | compatible_control              |    240 |            240 |            240 |               240 |                       240 |                     239 |       1        |       1        |         1         |                 1         |                0.995833 | True                              | True                      | True                        | True                        |
| candidate_near_manifold_symbolic_mimic | adversarial_near_manifold_mimic |    420 |            114 |            138 |                37 |                        35 |                      77 |       0.271429 |       0.328571 |         0.0880952 |                 0.0833333 |                0.183333 | False                             | True                      | True                        | False                       |

## Criteria

| criterion                                                | passed   |
|:---------------------------------------------------------|:---------|
| certified_event_dynamics_predict_symbols_above_threshold | True     |
| causal_coupling_preserves_v957_control                   | True     |
| causal_coupling_preserves_v960_control                   | True     |
| causal_coupling_rejects_near_manifold_mimic              | True     |
| v969_radius_envelope_would_accept_mimic                  | True     |

## Interpretation

The missing condition from V969 is event-to-symbol causal coupling.

A generator cannot merely emit valid symbols while moving inside the event manifold.

The emitted symbols must be predictable from the event dynamics themselves.

## Updated generator compatibility

```text
generator_compatibility =
  clean symbolic transfer
  + sufficient symbolic support
  + tolerant event-dynamics manifold compatibility
  + event-to-symbol causal coupling
```
