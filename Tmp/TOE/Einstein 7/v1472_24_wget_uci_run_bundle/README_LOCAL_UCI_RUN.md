# V1472.23 — Local UCI Independent Empirical Run Bundle

## Decision

```text
runtime_download_blocked_local_bundle_ready
```

## Why this exists

The runtime could not download the UCI ZIP directly. This bundle lets the test run immediately once `incident_event_log.csv` is placed in this folder.

## Required file

```text
incident_event_log.csv
```

Download from UCI dataset 498: **Incident Management Process Enriched Event Log**.

## Run

```bash
chmod +x run_uci_v1472_local.sh
./run_uci_v1472_local.sh
```

Equivalent manual commands:

```bash
python v1472_20_uci_incident_adapter.py incident_event_log.csv --output uci_incident_v1472_trace.csv --max-incidents 100
python v1472_12_manifest_runner.py uci_incident_preregistration_manifest.json
```

## Preregistered threshold

```text
threshold = 0.70
pilot_small_trace = false
```

## Evidence candidate only if

```text
real UCI trace passes threshold 0.70
event_order_shuffle null fails
provenance_shuffle null fails
repair_before_disruption null fails
source_removed null fails
entropy_arrow_reverse null fails
closure_only_static null fails
geometry_computed_on_inadmissible_slice = false
```

## Boundary

A pass is an empirical evidence candidate only. It is not proof of physical geometry, spacetime, GR, ADM, or physical curvature.
