#!/usr/bin/env bash
set -euo pipefail

echo "V1472.23 local UCI independent empirical run"
echo "Core axiom: No pruning-order trace, no empirical geometry claim."

if [ ! -f "incident_event_log.csv" ]; then
  echo "ERROR: incident_event_log.csv not found in current directory."
  echo "Download UCI dataset 498 and place incident_event_log.csv here."
  exit 1
fi

echo "Step 1: converting UCI event log to V1472 pruning-order trace..."
python v1472_20_uci_incident_adapter.py incident_event_log.csv --output uci_incident_v1472_trace.csv --max-incidents 100

echo "Step 2: running manifest-gated preregistered threshold test..."
python v1472_12_manifest_runner.py uci_incident_preregistration_manifest.json

echo "Done. Inspect generated .v1472_12_manifest_run.json and .v1472_11_threshold_0.70_results.json files."
