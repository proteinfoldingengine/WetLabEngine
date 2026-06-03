# V1472.3 — Admissible-Slice Geometry Causal Governor

## Status

```text
admissible_slice_geometry_harness_passed
```

## Core Axiom

```text
No pruning-order trace, no empirical geometry claim.
```

## What Changed from V1472.2

V1472.2 made the causal governor quantitative. V1472.3 adds the missing geometry rule:

```text
Geometry-like closure is computed only on admissible pruning-order slices.
```

A slice is admissible only when the trace has preserved source, prior event dependency, provenance lineage, and entropy-arrow consistency up to that slice.

## Margin

```text
M_total = C_closure × P_sequence × E_arrow
```

Where:

```text
P_sequence = valid_sequence_edges / required_sequence_edges
E_arrow = correct_entropy_transitions / total_entropy_transitions
C_closure = repaired_fraction × geometry_like_slice_coherence
```

`geometry_like_slice_coherence` is not physical curvature. It is a model-native coherence score over the active dependency/recovery graph.

## Result Summary

| trace_name                    | passed   |   M_total |   C_closure |   P_sequence |   E_arrow |   repaired_fraction |   geometry_like_closure | geometry_computed_final   | geometry_computed_on_inadmissible_slice   |   failure_count | failure_reasons                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:------------------------------|:---------|----------:|------------:|-------------:|----------:|--------------------:|------------------------:|:--------------------------|:------------------------------------------|----------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| valid_pruning_order_trace     | True     |  0.873821 |    0.873821 |     1        |  1        |                 1   |                0.873821 | True                      | False                                     |               0 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| partial_recovery_trace        | False    |  0.425008 |    0.425008 |     1        |  1        |                 0.5 |                0.850016 | True                      | False                                     |               0 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| branching_valid_trace         | True     |  0.895386 |    0.895386 |     1        |  1        |                 1   |                0.895386 | True                      | False                                     |               0 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| event_order_shuffle           | False    |  0        |    0        |     0.828571 |  1        |                 1   |              nan        | False                     | False                                     |               6 | non_source_before_source:e3_repair;provenance_lineage_violation:e3_repair:P0;missing_prior_event_dependency:e3_repair->e2_loss;non_source_before_source:e2_loss;provenance_lineage_violation:e2_loss:P0;missing_prior_event_dependency:e2_loss->e1_disruption                                                                                                                                                                                                      |
| provenance_shuffle            | False    |  0        |    0        |     0.857143 |  1        |                 1   |              nan        | False                     | False                                     |               5 | provenance_lineage_violation:e1_disruption:PX1;provenance_lineage_violation:e2_loss:PX2;provenance_lineage_violation:e3_repair:PX3;provenance_lineage_violation:e4_recovery:PX4;provenance_lineage_violation:e5_closure:PX5                                                                                                                                                                                                                                        |
| repair_before_disruption_null | False    |  0        |    0        |     0.971429 |  1        |                 1   |              nan        | False                     | False                                     |               1 | missing_prior_event_dependency:e3_repair->e2_loss                                                                                                                                                                                                                                                                                                                                                                                                                  |
| source_removed_null           | False    |  0        |    0        |     0.633333 |  1        |                 1   |              nan        | False                     | False                                     |              11 | non_source_before_source:e1_disruption;provenance_lineage_violation:e1_disruption:P0;missing_prior_event_dependency:e1_disruption->e0_source;non_source_before_source:e2_loss;provenance_lineage_violation:e2_loss:P0;non_source_before_source:e3_repair;provenance_lineage_violation:e3_repair:P0;non_source_before_source:e4_recovery;provenance_lineage_violation:e4_recovery:P0;non_source_before_source:e5_closure;provenance_lineage_violation:e5_closure:P0 |
| entropy_arrow_reverse_null    | False    |  0        |    0        |     1        |  0.166667 |                 1   |              nan        | False                     | False                                     |               5 | entropy_arrow_violation:e1_disruption;entropy_arrow_violation:e2_loss;entropy_arrow_violation:e3_repair;entropy_arrow_violation:e4_recovery;entropy_arrow_violation:e5_closure                                                                                                                                                                                                                                                                                     |
| closure_only_static_null      | False    |  0        |    0        |     0.5      |  1        |                 1   |              nan        | False                     | False                                     |               3 | non_source_before_source:static_closure;provenance_lineage_violation:static_closure:P0;missing_prior_event_dependency:static_closure->missing_recovery                                                                                                                                                                                                                                                                                                             |

## Interpretation

The valid ordered trace passes. The branching valid trace passes. Partial recovery does not certify. Critical nulls fail. Geometry-like closure is never computed on inadmissible slices.

## Claim Boundary

This is a pruning-order recoverability geometry harness. It does not claim physical spacetime, physical time, GR, Einstein equations, physical curvature, or a full ADM derivation.
