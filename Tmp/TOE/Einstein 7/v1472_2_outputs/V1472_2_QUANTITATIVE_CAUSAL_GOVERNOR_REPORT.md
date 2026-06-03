# V1472.2 — Quantitative Causal Governor

## Status
Completed.

## Decision

```text
quantitative_causal_governor_harness_passed
```

## Critical Bug Fixed

```text
prior_dependency now checks only prior event_id.
provenance labels can no longer satisfy event dependencies.
```

Old invalid logic:

```python
prior_dependency in active_ledger or provenance_ledger
```

New valid logic:

```python
prior_dependency in active_event_ids
```

## Added Provenance Continuity

For the current simple harness:

```text
the first source establishes source_provenance
every non-source event must preserve that provenance lineage
unless a future protocol explicitly permits provenance transition records
```

## Quantitative Margin

```text
M_total = C_closure × P_sequence × E_arrow
```

Where:

```text
C_closure = repaired_dependencies / damaged_dependencies
P_sequence = valid_sequence_edges / required_sequence_edges
E_arrow = correct_entropy_transitions / total_entropy_transitions
```

## Results Summary

```json
{
  "valid_pruning_order_trace": {
    "passed": true,
    "M_total": 1.0,
    "C_closure": 1.0,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "sequence_checks": 32,
    "sequence_valid": 32,
    "entropy_checks": 6,
    "entropy_valid": 6,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 6
  },
  "partial_recovery_trace": {
    "passed": false,
    "M_total": 0.5,
    "C_closure": 0.5,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "sequence_checks": 20,
    "sequence_valid": 20,
    "entropy_checks": 4,
    "entropy_valid": 4,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 4
  },
  "branching_valid_trace": {
    "passed": true,
    "M_total": 1.0,
    "C_closure": 1.0,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "sequence_checks": 32,
    "sequence_valid": 32,
    "entropy_checks": 6,
    "entropy_valid": 6,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 6
  },
  "event_order_shuffle": {
    "passed": false,
    "M_total": 0.8125,
    "C_closure": 1.0,
    "P_sequence": 0.8125,
    "E_arrow": 1.0,
    "sequence_checks": 32,
    "sequence_valid": 26,
    "entropy_checks": 6,
    "entropy_valid": 6,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "non_source_before_source:e3_repair",
      "provenance_lineage_violation:e3_repair:P0",
      "missing_prior_event_dependency:e3_repair->e2_loss",
      "non_source_before_source:e2_loss",
      "provenance_lineage_violation:e2_loss:P0",
      "missing_prior_event_dependency:e2_loss->e1_disruption"
    ],
    "events_processed": 6
  },
  "provenance_shuffle": {
    "passed": false,
    "M_total": 0.84375,
    "C_closure": 1.0,
    "P_sequence": 0.84375,
    "E_arrow": 1.0,
    "sequence_checks": 32,
    "sequence_valid": 27,
    "entropy_checks": 6,
    "entropy_valid": 6,
    "source_seen": true,
    "source_provenance": "PX0",
    "failure_reasons": [
      "provenance_lineage_violation:e1_disruption:PX1",
      "provenance_lineage_violation:e2_loss:PX2",
      "provenance_lineage_violation:e3_repair:PX3",
      "provenance_lineage_violation:e4_recovery:PX4",
      "provenance_lineage_violation:e5_closure:PX5"
    ],
    "events_processed": 6
  },
  "repair_before_disruption_null": {
    "passed": false,
    "M_total": 0.96875,
    "C_closure": 1.0,
    "P_sequence": 0.96875,
    "E_arrow": 1.0,
    "sequence_checks": 32,
    "sequence_valid": 31,
    "entropy_checks": 6,
    "entropy_valid": 6,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "missing_prior_event_dependency:e3_repair->e2_loss"
    ],
    "events_processed": 6
  },
  "source_removed_null": {
    "passed": false,
    "M_total": 0.6206896551724138,
    "C_closure": 1.0,
    "P_sequence": 0.6206896551724138,
    "E_arrow": 1.0,
    "sequence_checks": 29,
    "sequence_valid": 18,
    "entropy_checks": 5,
    "entropy_valid": 5,
    "source_seen": false,
    "source_provenance": null,
    "failure_reasons": [
      "non_source_before_source:e1_disruption",
      "provenance_lineage_violation:e1_disruption:P0",
      "missing_prior_event_dependency:e1_disruption->e0_source",
      "non_source_before_source:e2_loss",
      "provenance_lineage_violation:e2_loss:P0",
      "non_source_before_source:e3_repair",
      "provenance_lineage_violation:e3_repair:P0",
      "non_source_before_source:e4_recovery",
      "provenance_lineage_violation:e4_recovery:P0",
      "non_source_before_source:e5_closure",
      "provenance_lineage_violation:e5_closure:P0"
    ],
    "events_processed": 5
  },
  "entropy_arrow_reverse_null": {
    "passed": false,
    "M_total": 0.16666666666666666,
    "C_closure": 1.0,
    "P_sequence": 1.0,
    "E_arrow": 0.16666666666666666,
    "sequence_checks": 32,
    "sequence_valid": 32,
    "entropy_checks": 6,
    "entropy_valid": 1,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "entropy_arrow_violation:e1_disruption",
      "entropy_arrow_violation:e2_loss",
      "entropy_arrow_violation:e3_repair",
      "entropy_arrow_violation:e4_recovery",
      "entropy_arrow_violation:e5_closure"
    ],
    "events_processed": 6
  },
  "closure_only_static_null": {
    "passed": false,
    "M_total": 0.4,
    "C_closure": 1.0,
    "P_sequence": 0.4,
    "E_arrow": 1.0,
    "sequence_checks": 5,
    "sequence_valid": 2,
    "entropy_checks": 1,
    "entropy_valid": 1,
    "source_seen": false,
    "source_provenance": null,
    "failure_reasons": [
      "non_source_before_source:static_closure",
      "provenance_lineage_violation:static_closure:P0",
      "missing_prior_event_dependency:static_closure->missing_recovery"
    ],
    "events_processed": 1
  }
}
```

## Pass/Fail Summary

```text
valid trace passed: True
branching valid trace passed: True
partial recovery failed certification: True
all critical nulls failed: True
```

## Interpretation

The V1472.2 governor fixes the V1472.1 provenance bug and moves from binary certification to quantitative scoring.

This is now a proper causal governor prototype:

```text
pruning order enforced
event dependency enforced
provenance lineage enforced
entropy arrow enforced
partial recovery scored quantitatively
closure-only static null rejected
```

## Next

```text
V1472.3 — geometry-like closure computed only on admissible ordered slices
```
