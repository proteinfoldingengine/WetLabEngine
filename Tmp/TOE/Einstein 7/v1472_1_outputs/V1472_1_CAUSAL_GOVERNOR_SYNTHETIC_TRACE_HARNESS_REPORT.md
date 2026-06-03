# V1472.1 — Causal Governor Synthetic Trace Harness

## Status
Completed.

## Decision

```text
causal_governor_synthetic_trace_harness_not_closed
```

## Core Axiom

```text
No pruning-order trace, no empirical geometry claim.
```

## Purpose

Build and test the first sequential causal governor for pruning-order recoverability traces.

This is not legacy coordinate time. The engine processes an ordered pruning/provenance ledger and evaluates whether closure is admissible only after source, disruption, loss, repair, and recovery survive the entropy arrow.

## Margin

```text
M_total = C_closure × P_sequence × E_arrow
```

Where:

```text
C_closure = closure signal on admissible ordered slice
P_sequence = pruning/provenance order validity
E_arrow = entropy-arrow consistency
```

## Results

```json
{
  "valid_pruning_order_trace": {
    "passed": true,
    "M_total": 1.0,
    "C_closure": 1.0,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "failure_reason": null,
    "events_processed": 6
  },
  "event_order_shuffle": {
    "passed": false,
    "M_total": 0.0,
    "C_closure": 0.0,
    "P_sequence": 0.0,
    "E_arrow": 1.0,
    "failure_reason": "missing_prior_dependency:e0_source",
    "events_processed": 0
  },
  "provenance_shuffle": {
    "passed": true,
    "M_total": 1.0,
    "C_closure": 1.0,
    "P_sequence": 1.0,
    "E_arrow": 1.0,
    "failure_reason": null,
    "events_processed": 6
  },
  "repair_before_disruption_null": {
    "passed": false,
    "M_total": 0.0,
    "C_closure": 0.0,
    "P_sequence": 0.0,
    "E_arrow": 1.0,
    "failure_reason": "missing_prior_dependency:e2_loss",
    "events_processed": 1
  },
  "source_removed_null": {
    "passed": false,
    "M_total": 0.0,
    "C_closure": 0.0,
    "P_sequence": 0.0,
    "E_arrow": 1.0,
    "failure_reason": "missing_prior_dependency:e0_source",
    "events_processed": 0
  },
  "entropy_arrow_reverse_null": {
    "passed": false,
    "M_total": 0.0,
    "C_closure": 0.0,
    "P_sequence": 1.0,
    "E_arrow": 0.0,
    "failure_reason": "entropy_arrow_violation:e1_disruption",
    "events_processed": 1
  },
  "closure_only_static_null": {
    "passed": false,
    "M_total": 0.0,
    "C_closure": 0.0,
    "P_sequence": 0.0,
    "E_arrow": 1.0,
    "failure_reason": "missing_prior_dependency:e4_recovery",
    "events_processed": 0
  }
}
```

## Interpretation

```text
The valid pruning-order trace passes.
Every null trace fails.

This confirms the first causal governor does what the static graph harness could not:
it collapses geometry-like closure when pruning order, provenance, or entropy-arrow consistency is broken.
```

## Next

```text
V1472.2 — add quantitative closure metric and richer synthetic trace family
```
