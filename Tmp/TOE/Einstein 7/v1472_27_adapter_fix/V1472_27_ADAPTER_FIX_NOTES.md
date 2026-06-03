# V1472.27 — UCI Adapter Fix Notes

## Diagnosis from uploaded V1472.26 outputs

The full certification did not pass.

Key results from `v1472_26_uci_full_certification_summary.json`:

```text
final_verdict = FAIL_FULL_CERTIFICATION
real_trace.passed = false
real_trace.M_total = 0.0
real_trace.P_sequence = 1.0
real_trace.E_arrow = 1.0
real_trace.failure_count = 0
all_nulls_fail = true
no_inadmissible_geometry_computed = true
```

This means:

```text
causal order passed
provenance passed
entropy arrow passed
null protection passed
geometry gate passed
but closure score collapsed because repaired_fraction = 0.0
```

## Root cause

The adapter used `resolved_at` and `closed_at` as row-level state classifiers.

In this UCI file, those fields appear to be final incident timestamps repeated across many rows of the same incident. Example: rows with raw `incident_state = Active` can still have `resolved_at` and `closed_at` populated.

So the adapter misclassified active rows as closure/recovery.

Observed adapted trace:

```text
event_type counts:
closure = 2787
source = 430
disruption = 0
loss = 0
repair = 0
recovery = 0
```

And totals:

```text
damaged_dependencies = 0
repaired_dependencies = 2804
repaired_fraction = 0.0
```

Because damaged total was zero, the real trace could not certify.

## Correct fix

Use `incident_state` and state transitions as the primary classifier.

Use `resolved_at` and `closed_at` only as audit metadata, not as row-level classifiers.

Correct state mapping:

```text
first row per incident -> source
New / Active / Awaiting* before resolution -> disruption/loss/repair depending disorder delta
Resolved -> recovery
Closed -> closure
```

## Important boundary

This is an adapter bug / schema interpretation issue, not yet a physics result.

The V1472.26 full-certification result remains:

```text
FAIL_FULL_CERTIFICATION
```

Next: rerun with corrected adapter.
