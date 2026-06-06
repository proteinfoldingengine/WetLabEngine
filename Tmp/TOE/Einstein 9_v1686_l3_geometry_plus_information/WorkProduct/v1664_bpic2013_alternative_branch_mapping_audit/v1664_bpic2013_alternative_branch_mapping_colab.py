# ============================================================
# V1664 — BPIC 2013 Alternative Branch Mapping Audit, Colab Full Run
# ============================================================
# Purpose:
#   Re-parse BPIC 2013 XES.GZ and test candidate counts undxqer multiple branch mappings.
# Boundary:
#   This does not close L3 or prove empirical geometry.
# ============================================================

from __future__ import annotations
import gzip, json, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("/content/v1664_bpic2013_alternative_branch_mapping")
OUT.mkdir(parents=True, exist_ok=True)
DATA_URL = "https://data.4tu.nl/file/0fc5c579-e544-4fab-9143-fab1f5192432/aa51ffbb-25fd-4b5a-b0b8-9aba659b7e8c"
XES_GZ = OUT / "BPI_Challenge_2013_incidents.xes.gz"

if not XES_GZ.exists():
    subprocess.run(["wget", "--content-disposition", "-O", str(XES_GZ), DATA_URL], check=True)

def local_name(tag): return tag.split("}", 1)[1] if "}" in tag else tag

def attrs_from_xes_node(node):
    out = {}
    for child in node:
        if local_name(child.tag) in {"string","date","int","float","boolean"}:
            k = child.attrib.get("key"); v = child.attrib.get("value")
            if k: out[k] = v
    return out

def parse_xes(path, max_traces=None):
    rows = []
    with gzip.open(path, "rb") as f:
        tree = ET.parse(f)
    root = tree.getroot()
    ti = 0
    for trace in root:
        if local_name(trace.tag) != "trace": continue
        if max_traces is not None and ti >= max_traces: break
        ta = attrs_from_xes_node(trace)
        tid = ta.get("concept:name") or ta.get("case:concept:name") or f"trace_{ti}"
        ei = 0
        for ch in trace:
            if local_name(ch.tag) == "event":
                ev = attrs_from_xes_node(ch)
                rows.append({"trace_id": tid, "event_index": ei, **ev})
                ei += 1
        ti += 1
        if ti % 1000 == 0: print("parsed traces", ti)
    return pd.DataFrame(rows)

def infer_event_type(activity, lifecycle, event_index):
    if event_index == 0: return "source"
    text = f"{activity} {lifecycle}".lower()
    if any(x in text for x in ["closed","resolved","completed"]): return "closure"
    if any(x in text for x in ["queued","awaiting assignment"]): return "disruption"
    if "wait" in text: return "recovery"
    if any(x in text for x in ["accepted","assigned","in progress"]): return "repair"
    return "recovery"

def entropy_proxy(event_type, order_fraction, row):
    impact_weight = {"low":0.05, "medium":0.15, "high":0.30}
    impact = str(row.get("impact","")).lower()
    sev = impact_weight.get(impact, 0.10)
    base = 0.20 + 0.35 * order_fraction + sev
    if event_type in {"disruption","loss"}: return base, min(1.0, base+0.25)
    if event_type in {"repair","recovery","closure"}: return min(1.0, base+0.20), max(0.0, base-0.05)
    return base, base

def normalize_with_branch(events, branch_col):
    rows = []
    for tid, g in events.groupby("trace_id", sort=False):
        g = g.sort_values("event_index").reset_index(drop=True)
        n = len(g); prev = ""
        for i, row in g.iterrows():
            et = infer_event_type(str(row.get("concept:name","")), str(row.get("lifecycle:transition","")), i)
            eb, ea = entropy_proxy(et, i/max(1,n-1), row)
            if branch_col == "__activity__":
                branch = str(row.get("concept:name","unknown")).split()[0]
            elif branch_col in row.index and pd.notna(row[branch_col]) and str(row[branch_col]).strip():
                branch = str(row[branch_col]).strip()
            else:
                branch = "unknown"
            rows.append({
                "trace_id": str(tid),
                "event_id": f"{tid}_{i}",
                "pruning_order_index": int(i),
                "event_type": et,
                "provenance_id": str(tid),
                "branch_id": branch,
                "prior_dependency": prev,
                "entropy_before": float(eb),
                "entropy_after": float(ea),
                "damage_count": 1 if et in {"disruption","loss"} else 0,
                "repair_count": 1 if et in {"repair","recovery","closure"} else 0,
            })
            prev = f"{tid}_{i}"
    return pd.DataFrame(rows)

def metrics_fast(tdf):
    bg = tdf.groupby(tdf["branch_id"].astype(str), sort=False)[["damage_count","repair_count"]].sum()
    bg = bg[~bg.index.astype(str).isin(["ABC","ALL","nan","unknown","None",""])]
    d = bg["damage_count"].to_numpy(float); r = bg["repair_count"].to_numpy(float); B = len(bg)
    C_total = min(1.0, float(r.sum()) / max(1.0, float(d.sum())))
    if B < 2:
        C_pairwise = 0.0
    else:
        ii, jj = np.triu_indices(B, 1)
        pair = np.minimum(1.0, (r[ii]+r[jj]) / np.maximum(1.0, d[ii]+d[jj]))
        C_pairwise = float(pair.mean())
    return {"C_total": C_total, "C_pairwise": C_pairwise, "delta_C_L3": max(0.0, C_total-C_pairwise), "branch_count": B, "closure_events": int((tdf["event_type"]=="closure").sum())}

def candidate_count(df):
    c = 0; deltas = []
    for tid, tdf in df.groupby("trace_id", sort=False):
        if not (tdf["event_type"].eq("source").any() and tdf["event_type"].eq("closure").any()): continue
        m = metrics_fast(tdf)
        if m["branch_count"] >= 3 and m["closure_events"] >= 1 and m["delta_C_L3"] > 0:
            c += 1; deltas.append(m["delta_C_L3"])
    arr = np.array(deltas)
    return {
        "candidate_count": int(c),
        "mean_delta": float(arr.mean()) if len(arr) else 0.0,
        "max_delta": float(arr.max()) if len(arr) else 0.0,
        "count_delta_gt_0_025": int((arr > 0.025).sum()) if len(arr) else 0,
        "count_delta_gt_0_05": int((arr > 0.05).sum()) if len(arr) else 0,
        "count_delta_gt_0_10": int((arr > 0.10).sum()) if len(arr) else 0,
    }

events = parse_xes(XES_GZ, max_traces=None)
branch_cols = [
    "org:group",
    "org:resource",
    "org:role",
    "organization involved",
    "product",
    "impact",
    "__activity__",
]
rows = []
for bc in branch_cols:
    if bc != "__activity__" and bc not in events.columns:
        rows.append({"branch_mapping": bc, "available": False, "candidate_count": None})
        continue
    print("running branch mapping", bc)
    nd = normalize_with_branch(events, bc)
    res = candidate_count(nd)
    res.update({"branch_mapping": bc, "available": True, "row_count": len(nd), "trace_count": nd["trace_id"].nunique()})
    rows.append(res)
pd.DataFrame(rows).to_csv(OUT / "v1664_alternative_branch_mapping_full_results.csv", index=False)
result = {
    "document_id": "V1664_BPIC2013_ALTERNATIVE_BRANCH_MAPPING_AUDIT",
    "status": "completed",
    "results": rows,
    "claim_boundary": "Alternative branch mapping audit only. Does not close L3 or prove empirical geometry."
}
(OUT / "v1664_result.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
