# V1472.3 — Geometry-Like Closure on Admissible Ordered Slices

## Status
Completed.

## Decision

```text
admissible_slice_geometry_harness_passed
```

## Core Axiom

```text
No pruning-order trace, no empirical geometry claim.
```

## Key Rule

```text
Geometry-like closure is computed only on hard-admissible ordered slices.
```

A slice is hard-admissible only when:

```text
no sequence/provenance failures exist
source has been established
P_sequence = 1.0
E_arrow = 1.0
```

If a slice is inadmissible:

```text
geometry_like_closure = 0
M_total_admissible = 0
```

This separates raw quantitative margin from hard certification.

## Margin Separation

Raw quantitative margin:

```text
M_total_raw = repair_fraction × P_sequence × E_arrow
```

Admissible geometry margin:

```text
M_total_admissible = C_closure × P_sequence × E_arrow
```

Where:

```text
C_closure = repair_fraction × geometry_like_closure
```

and geometry-like closure is gated by pruning-order admissibility.

## Results Summary

```json
{
  "valid_pruning_order_trace": {
    "passed": true,
    "M_total_raw": 1.0,
    "M_total_admissible": 0.8427348625589725,
    "C_closure": 0.8427348625589725,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.8427348625589725,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 6
  },
  "partial_recovery_trace": {
    "passed": false,
    "M_total_raw": 0.5,
    "M_total_admissible": 0.4173358532703224,
    "C_closure": 0.4173358532703224,
    "repair_fraction": 0.5,
    "geometry_like_closure": 0.8346717065406448,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 4
  },
  "branching_valid_trace": {
    "passed": true,
    "M_total_raw": 1.0,
    "M_total_admissible": 0.8427348625589725,
    "C_closure": 0.8427348625589725,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.8427348625589725,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [],
    "events_processed": 6
  },
  "event_order_shuffle": {
    "passed": false,
    "M_total_raw": 0.65625,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.65625,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "non_source_before_source:e1_disruption",
      "provenance_lineage_violation:e1_disruption:P0",
      "missing_prior_event_dependency:e1_disruption->e0_source",
      "non_source_before_source:e4_recovery",
      "provenance_lineage_violation:e4_recovery:P0",
      "missing_prior_event_dependency:e4_recovery->e3_repair",
      "non_source_before_source:e3_repair",
      "provenance_lineage_violation:e3_repair:P0",
      "missing_prior_event_dependency:e3_repair->e2_loss",
      "non_source_before_source:e2_loss",
      "provenance_lineage_violation:e2_loss:P0"
    ],
    "events_processed": 6
  },
  "provenance_shuffle": {
    "passed": false,
    "M_total_raw": 0.84375,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.84375,
    "E_arrow": 1.0,
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
    "M_total_raw": 0.96875,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.96875,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "missing_prior_event_dependency:e3_repair->e2_loss"
    ],
    "events_processed": 6
  },
  "source_removed_null": {
    "passed": false,
    "M_total_raw": 0.6206896551724138,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.6206896551724138,
    "E_arrow": 1.0,
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
    "M_total_raw": 0.16666666666666666,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 1.0,
    "E_arrow": 0.16666666666666666,
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
    "M_total_raw": 0.4,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.4,
    "E_arrow": 1.0,
    "source_seen": false,
    "source_provenance": null,
    "failure_reasons": [
      "non_source_before_source:static_closure",
      "provenance_lineage_violation:static_closure:P0",
      "missing_prior_event_dependency:static_closure->missing_recovery"
    ],
    "events_processed": 1
  },
  "final_closure_preserved_order_broken_null": {
    "passed": false,
    "M_total_raw": 0.96875,
    "M_total_admissible": 0.0,
    "C_closure": 0.0,
    "repair_fraction": 1.0,
    "geometry_like_closure": 0.0,
    "P_sequence": 0.96875,
    "E_arrow": 1.0,
    "source_seen": true,
    "source_provenance": "P0",
    "failure_reasons": [
      "missing_prior_event_dependency:e3_repair->e2_loss"
    ],
    "events_processed": 6
  }
}
```

## Pass/Fail Summary

```text
valid trace passed: True
branching valid trace passed: True
partial recovery failed certification: True
all critical nulls failed: True
all null geometry zero or inadmissible: True
```

## Interpretation

V1472.3 completes the key protection requested by peer review:

```text
Do not compute geometry-like closure on inadmissible slices.
```

Static closure, broken provenance, broken pruning order, and reversed entropy arrow may retain raw repaired-dependency quantities, but they cannot certify geometry-like closure because the admissible ordered slice condition fails.

## Next

```text
V1472.4 — richer multi-provenance transition records and allowed provenance transitions
```
