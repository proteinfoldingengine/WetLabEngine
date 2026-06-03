# Run Instructions

## Input

```text
Detail_Incident_Activity.csv
```

with columns:

```text
Incident ID
IncidentActivity_Type
```

## Command

```bash
python v1472_43_bpi2014_entropy_phase_repair_proof.py
```

## Outputs

```text
v1472_43_bpi2014_entropy_phase_repair_summary.json
v1472_43_bpi2014_entropy_phase_repair_real_lineages.csv
v1472_43_bpi2014_entropy_phase_repair_real_aggregate.csv
v1472_43_bpi2014_entropy_phase_repair_null_aggregates.csv
```

## Full Null Suite

```text
event_order_shuffle
provenance_shuffle
repair_before_disruption
source_removed
entropy_arrow_reverse
closure_only_static
neutral_only_static
terminal_label_only_null
```
