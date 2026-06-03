# Independent Trace Data Request

## Needed file type

CSV, JSON array, or JSONL.

## Needed columns

```text
event_id / log_id
seq / pruning_order_index
kind / raw_event_type
ticket / provenance_id
depends_on / prior_dependency
entropy_before
entropy_after
damaged / damaged_dependencies
repaired / repaired_dependencies
component / affected_node
target / repair_target
```

## Good trace examples

```text
incident recovery logs
database transaction rollback/retry logs
packet-routing failure/recovery logs
system repair timelines
protein folding trajectory converted into event ledger
```

## Important

A static graph is not enough.

The dataset must show ordered information loss and recovery:

```text
source → disruption/loss → repair/recovery → closure
```
