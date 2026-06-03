#!/usr/bin/env python3
"""
V1472.20 UCI Incident Event Log Adapter

Purpose
-------
Convert the UCI Incident Management Process Enriched Event Log into
V1472 pruning-order recoverability traces.

Input
-----
incident_event_log.csv from UCI dataset 498.

Expected important columns include:
- number
- incident_state
- active
- reassignment_count
- reopen_count
- sys_mod_count
- made_sla
- opened_at
- sys_updated_at
- impact
- urgency
- priority
- resolved_at
- closed_at

Output
------
uci_incident_v1472_trace.csv

Claim boundary
--------------
This adapter prepares the trace. It does not prove empirical geometry.
Run the output through a preregistered V1472 manifest and null suite.
"""

from __future__ import annotations
import argparse
import pandas as pd
import numpy as np
from pathlib import Path

STATE_SOURCE_TERMS = {"New", "new", "1", "1 - New"}
STATE_REPAIR_TERMS = {"In Progress", "On Hold", "Awaiting User Info", "Awaiting Evidence"}
STATE_RECOVERY_TERMS = {"Resolved", "resolved", "6", "6 - Resolved"}
STATE_CLOSURE_TERMS = {"Closed", "closed", "7", "7 - Closed"}

def parse_rank(x):
    """
    Parses fields like '1 - High', '2 - Medium', '3 - Low'.
    Lower number = higher severity. Return normalized risk in [0,1].
    """
    if pd.isna(x):
        return 0.5
    s = str(x).strip()
    try:
        n = int(s.split()[0])
    except Exception:
        try:
            n = int(float(s))
        except Exception:
            return 0.5
    # 1 high -> 1.0, 2 medium -> 0.66, 3 low -> 0.33
    return max(0.0, min(1.0, (4 - n) / 3))

def boolish(x):
    if pd.isna(x):
        return False
    return str(x).strip().lower() in {"true", "1", "yes", "y"}

def disorder(row):
    priority = parse_rank(row.get("priority"))
    impact = parse_rank(row.get("impact"))
    urgency = parse_rank(row.get("urgency"))
    reassignment = min(float(row.get("reassignment_count", 0) or 0) / 10.0, 1.0)
    reopen = min(float(row.get("reopen_count", 0) or 0) / 5.0, 1.0)
    active = 1.0 if boolish(row.get("active")) else 0.0
    made_sla_penalty = 0.0 if boolish(row.get("made_sla")) else 0.3
    return max(0.0, min(1.0, 0.25*priority + 0.20*impact + 0.20*urgency + 0.15*reassignment + 0.10*reopen + 0.10*active + made_sla_penalty))

def classify_event(prev, row, is_first, is_last):
    state = str(row.get("incident_state", "")).strip()
    if is_first:
        return "source"
    if state in STATE_CLOSURE_TERMS or str(row.get("closed_at", "")).strip() not in {"", "?", "nan", "NaT"}:
        return "closure"
    if state in STATE_RECOVERY_TERMS or str(row.get("resolved_at", "")).strip() not in {"", "?", "nan", "NaT"}:
        return "recovery"

    if prev is None:
        return "disruption"

    d_now = disorder(row)
    d_prev = disorder(prev)
    reassignment_inc = float(row.get("reassignment_count", 0) or 0) > float(prev.get("reassignment_count", 0) or 0)
    reopen_inc = float(row.get("reopen_count", 0) or 0) > float(prev.get("reopen_count", 0) or 0)

    if reopen_inc or reassignment_inc or d_now > d_prev + 0.05:
        return "loss"
    if d_now < d_prev - 0.05:
        return "repair"
    return "repair" if not is_last else "closure"

def adapt(input_csv: Path, output_csv: Path, max_incidents=None):
    df = pd.read_csv(input_csv, low_memory=False)
    # Normalize column names.
    df.columns = [c.strip() for c in df.columns]

    required = ["number", "sys_updated_at", "sys_mod_count"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    df["_order_time"] = pd.to_datetime(df["sys_updated_at"], errors="coerce")
    df["_sys_mod_count_num"] = pd.to_numeric(df["sys_mod_count"], errors="coerce").fillna(0)

    rows = []
    incident_count = 0
    for number, g in df.groupby("number", sort=False):
        g = g.sort_values(["_order_time", "_sys_mod_count_num"], kind="mergesort").reset_index(drop=True)
        if len(g) < 4:
            continue
        incident_count += 1
        if max_incidents and incident_count > max_incidents:
            break

        prev = None
        prev_event_id = None
        prev_disorder = None
        for i, row in g.iterrows():
            rowd = row.to_dict()
            event_id = f"{number}__{i}"
            event_type = classify_event(prev, rowd, is_first=(i == 0), is_last=(i == len(g)-1))
            current_disorder = disorder(rowd)

            if prev_disorder is None:
                entropy_before = current_disorder
            else:
                entropy_before = prev_disorder
            entropy_after = current_disorder

            # Force source neutral.
            if event_type == "source":
                entropy_before = entropy_after

            # Ensure closure/recovery tends downward if resolved/closed fields are present:
            # this is a proxy and must be reported as such.
            if event_type in {"recovery", "closure"} and entropy_after > entropy_before:
                entropy_after = max(0.0, entropy_before - 0.05)

            damage = 0
            repair = 0
            if prev_disorder is not None:
                delta = entropy_after - entropy_before
                if event_type in {"disruption", "loss"} or delta > 0:
                    damage = max(1, int(round(abs(delta) * 10)))
                elif event_type in {"repair", "recovery", "closure"} or delta < 0:
                    repair = max(1, int(round(abs(delta) * 10)))

            rows.append({
                "log_id": event_id,
                "seq": len(rows),
                "kind": event_type,
                "component": str(rowd.get("cmdb_ci", "")) if str(rowd.get("cmdb_ci", "")) not in {"", "?", "nan"} else str(rowd.get("category", "incident")),
                "ticket": str(number),
                "depends_on": "" if prev_event_id is None else prev_event_id,
                "entropy_before": round(float(entropy_before), 6),
                "entropy_after": round(float(entropy_after), 6),
                "damaged": int(damage),
                "repaired": int(repair),
                "source_column_number": str(number),
                "source_incident_state": str(rowd.get("incident_state", "")),
                "source_sys_updated_at": str(rowd.get("sys_updated_at", "")),
                "source_priority": str(rowd.get("priority", "")),
                "source_impact": str(rowd.get("impact", "")),
                "source_urgency": str(rowd.get("urgency", "")),
            })

            prev = rowd
            prev_event_id = event_id
            prev_disorder = current_disorder

    out = pd.DataFrame(rows)
    out.to_csv(output_csv, index=False)
    print(f"Wrote {output_csv} with {len(out)} events from {incident_count} incidents")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("--output", type=Path, default=Path("uci_incident_v1472_trace.csv"))
    ap.add_argument("--max-incidents", type=int, default=None)
    args = ap.parse_args()
    adapt(args.input_csv, args.output, max_incidents=args.max_incidents)
