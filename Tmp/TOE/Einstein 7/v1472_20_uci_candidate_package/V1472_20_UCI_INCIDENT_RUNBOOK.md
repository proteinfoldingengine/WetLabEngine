# V1472.20 — UCI Incident Dataset Runbook

## Candidate

UCI Machine Learning Repository dataset 498: Incident management process enriched event log.

## Why this is the best first candidate

It is a real incident-management event log, not a generated sample. It is sequential, anonymized, and includes 141,712 events across 24,918 incidents with incident state, active/closed status, reassignment/reopen counts, sys_mod_count, impact, urgency, priority, resolved_at, and closed_at fields.

## Download

Use UCI dataset 498 and download `incident_event_log.csv`.

## Convert to V1472 trace

```bash
python v1472_20_uci_incident_adapter.py incident_event_log.csv --output uci_incident_v1472_trace.csv --max-incidents 100
```

For full run, omit `--max-incidents`.

## Prepare manifest

Copy:

```text
uci_incident_preregistration_manifest_template.json
```

Set:

```text
input_file = uci_incident_v1472_trace.csv
threshold = 0.70
pilot_small_trace = false
```

## Run

```bash
python v1472_12_manifest_runner.py uci_incident_preregistration_manifest.json
```

## Must report

```text
continuous M_total
threshold decision
threshold sweep
all nulls
geometry_computed_on_inadmissible_slice
exclusion counts
mapping assumptions
```

## Claim boundary

A pass would be an empirical evidence candidate, not proof of physical geometry.
