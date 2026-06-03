#!/usr/bin/env bash
set -euo pipefail

echo "V1472.24 UCI independent empirical run with auto-download"
echo "Core axiom: No pruning-order trace, no empirical geometry claim."

UCI_ZIP_URL="https://archive.ics.uci.edu/static/public/498/incident%2Bmanagement%2Bprocess%2Benriched%2Bevent%2Blog.zip"
ZIP_FILE="uci_incident_event_log.zip"
CSV_FILE="incident_event_log.csv"

echo "Step 0: checking for ${CSV_FILE}..."

if [ ! -f "${CSV_FILE}" ]; then
  echo "${CSV_FILE} not found. Attempting download from UCI..."

  if command -v wget >/dev/null 2>&1; then
    echo "Using wget..."
    wget -O "${ZIP_FILE}" "${UCI_ZIP_URL}" || {
      echo "wget download failed."
      rm -f "${ZIP_FILE}"
    }
  elif command -v curl >/dev/null 2>&1; then
    echo "Using curl..."
    curl -L -o "${ZIP_FILE}" "${UCI_ZIP_URL}" || {
      echo "curl download failed."
      rm -f "${ZIP_FILE}"
    }
  else
    echo "Neither wget nor curl is available."
  fi

  if [ -f "${ZIP_FILE}" ]; then
    echo "Unzipping ${ZIP_FILE}..."
    python - <<'PY'
from zipfile import ZipFile
from pathlib import Path

zip_path = Path("uci_incident_event_log.zip")
with ZipFile(zip_path) as z:
    names = z.namelist()
    print("ZIP contents:")
    for n in names:
        print(" -", n)
    target = None
    for n in names:
        if n.endswith("incident_event_log.csv"):
            target = n
            break
    if target is None:
        raise SystemExit("incident_event_log.csv not found inside ZIP")
    z.extract(target, ".")
    extracted = Path(target)
    if extracted.name != "incident_event_log.csv":
        extracted.rename("incident_event_log.csv")
print("Extracted incident_event_log.csv")
PY
  fi
fi

if [ ! -f "${CSV_FILE}" ]; then
  echo "ERROR: ${CSV_FILE} still not found."
  echo "Download failed or was blocked. Manually download UCI dataset 498 and place incident_event_log.csv here."
  exit 1
fi

echo "Step 1: converting UCI event log to V1472 pruning-order trace..."
python v1472_20_uci_incident_adapter.py "${CSV_FILE}" --output uci_incident_v1472_trace.csv --max-incidents 100

echo "Step 2: running manifest-gated preregistered threshold test..."
python v1472_12_manifest_runner.py uci_incident_preregistration_manifest.json

echo "Done. Inspect generated .v1472_12_manifest_run.json and .v1472_11_threshold_0.70_results.json files."
