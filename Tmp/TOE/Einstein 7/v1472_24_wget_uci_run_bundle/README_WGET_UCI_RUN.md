# V1472.24 — UCI Run Bundle with wget/curl Download

## What changed

This bundle adds automatic UCI download support.

The main script now:

```text
checks for incident_event_log.csv
if missing, tries wget
if wget missing, tries curl
unzips incident_event_log.csv
runs the V1472 adapter
runs the manifest-gated threshold 0.70 test
```

## Run

```bash
chmod +x run_uci_v1472_with_wget.sh
./run_uci_v1472_with_wget.sh
```

## Python-only download helper

```bash
python download_uci_incident_event_log.py
```

Then run:

```bash
python v1472_20_uci_incident_adapter.py incident_event_log.csv --output uci_incident_v1472_trace.csv --max-incidents 100
python v1472_12_manifest_runner.py uci_incident_preregistration_manifest.json
```

## Boundary

If download is blocked, the script stops. It does not substitute generated sample data.

A pass is an empirical evidence candidate only, not proof of physical geometry, spacetime, GR, ADM, or physical curvature.
