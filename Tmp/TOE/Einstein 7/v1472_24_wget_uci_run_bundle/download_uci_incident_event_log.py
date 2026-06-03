#!/usr/bin/env python3
"""
download_uci_incident_event_log.py

Downloads UCI dataset 498 ZIP and extracts incident_event_log.csv.

Usage:
    python download_uci_incident_event_log.py
"""

from pathlib import Path
from zipfile import ZipFile
import subprocess
import sys
import shutil

URL = "https://archive.ics.uci.edu/static/public/498/incident%2Bmanagement%2Bprocess%2Benriched%2Bevent%2Blog.zip"
ZIP = Path("uci_incident_event_log.zip")
CSV = Path("incident_event_log.csv")

def run(cmd):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, check=False)

def main():
    if CSV.exists():
        print(f"{CSV} already exists")
        return

    if shutil.which("wget"):
        r = run(["wget", "-O", str(ZIP), URL])
    elif shutil.which("curl"):
        r = run(["curl", "-L", "-o", str(ZIP), URL])
    else:
        raise SystemExit("Neither wget nor curl is available")

    if r.returncode != 0 or not ZIP.exists():
        raise SystemExit("Download failed. Manually download the UCI ZIP and place incident_event_log.csv here.")

    with ZipFile(ZIP) as z:
        print("ZIP contents:")
        for n in z.namelist():
            print(" -", n)
        target = next((n for n in z.namelist() if n.endswith("incident_event_log.csv")), None)
        if target is None:
            raise SystemExit("incident_event_log.csv not found inside ZIP")
        z.extract(target, ".")
        extracted = Path(target)
        if extracted.name != CSV.name:
            extracted.rename(CSV)

    print(f"Extracted {CSV}")

if __name__ == "__main__":
    main()
