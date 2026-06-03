# === V1472.43 BPI2014 ENTROPY + PHASE-ORDER REPAIR PROOF HARNESS ===
# Expected input: Detail_Incident_Activity.csv
# Expected columns: Incident ID, IncidentActivity_Type

from pathlib import Path
import json, math, random
from dataclasses import dataclass, asdict
from typing import Optional
from collections import defaultdict, deque
import pandas as pd
import numpy as np

SEED = 147243
random.seed(SEED)
np.random.seed(SEED)

DATA_FILE = Path("Detail_Incident_Activity.csv")
MAX_CASES = 1000
CLOSURE_THRESHOLD = 0.70
PASS_FRACTION_THRESHOLD = 0.70
ENTROPY_TOLERANCE = 0.005
OUTPUT_PREFIX = "v1472_43_bpi2014_entropy_phase_repair"

MANIFEST = {
    "document_id": "V1472_43_BPI2014_ENTROPY_PHASE_REPAIR",
    "core_axiom": "No pruning-order trace, no empirical geometry claim.",
    "scoring_law": "M_total = C_topological * P_sequence * E_arrow",
    "claim_boundary": "Evidence candidate only; not proof of physical spacetime, GR, ADM, Einstein equations, or physical curvature."
}

NEUTRAL_WORDS = ["operator update","update from customer","customer update","user update","status update","status","comment","comments","note","notes","information","info","email","mail","phone","call","communication","communicate","message","notification","notify","reminder","request information","request info","provided information","additional information","worklog","work log","log","monitor","check","checked","follow up","follow-up"]
LOSS_WORDS = ["incident opened","open incident","new incident","registered","created","create incident","assignment","assigned","reassignment","reassigned","escalation","escalated","priority changed","impact changed","urgency changed","severity changed","reopen","reopened","failed","failure","error","problem","outage","unavailable","not working","broken","breach","sla breach"]
REPAIR_WORDS = ["resolved","resolve","solution","solved","repair","restored","restore","fixed","fix","implemented","implementation","workaround provided","caused by ci fixed","closed","close","completed","complete","cancelled"]
CLOSURE_WORDS = ["closed","close","completed","complete","resolved","resolve","cancelled"]

def contains_any(text, words):
    return any(w in str(text).strip().lower() for w in words)

def classify_activity(activity, is_first, is_last):
    s = str(activity).strip().lower()
    if is_first:
        return "source"
    if contains_any(s, CLOSURE_WORDS):
        return "recovery" if "resolv" in s else "closure"
    if contains_any(s, REPAIR_WORDS):
        return "repair"
    if contains_any(s, NEUTRAL_WORDS):
        return "neutral"
    if contains_any(s, LOSS_WORDS):
        return "loss"
    if not is_last:
        return "neutral"
    return "closure"

def entropy_for_event_type(event_type, prev_entropy):
    if event_type == "source":
        return prev_entropy, prev_entropy
    if event_type in {"disruption", "loss"}:
        return prev_entropy, min(1.0, prev_entropy + 0.10)
    if event_type == "neutral":
        return prev_entropy, prev_entropy
    if event_type == "repair":
        return prev_entropy, max(0.0, prev_entropy - 0.07)
    if event_type == "recovery":
        return prev_entropy, max(0.0, prev_entropy - 0.12)
    if event_type == "closure":
        return prev_entropy, max(0.0, prev_entropy - 0.15)
    return prev_entropy, prev_entropy

@dataclass(frozen=True)
class PruningEvent:
    event_id: str
    pruning_order_index: int
    event_type: str
    provenance_id: str
    requires_prior: bool
    prior_dependency: Optional[str]
    entropy_before: float
    entropy_after: float
    state_delta: float
    damaged_dependencies: int = 0
    repaired_dependencies: int = 0
    affected_node: Optional[str] = None
    repair_target: Optional[str] = None

def load_and_adapt(path):
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    df = pd.read_csv(path, sep=";", encoding="utf-8", low_memory=False, on_bad_lines="skip")
    df.columns = [str(c).strip() for c in df.columns]
    if "Incident ID" not in df.columns or "IncidentActivity_Type" not in df.columns:
        raise ValueError("Expected columns missing: Incident ID, IncidentActivity_Type")

    time_col = next((c for c in df.columns if any(x in str(c).lower() for x in ["date", "time", "timestamp"])), None)
    if time_col:
        df["_order_time"] = pd.to_datetime(df[time_col], errors="coerce", dayfirst=True)
    else:
        df["_order_time"] = np.arange(len(df))
    df = df.sort_values(["Incident ID", "_order_time"], kind="mergesort")
    cases = df["Incident ID"].drop_duplicates().head(MAX_CASES)
    df = df[df["Incident ID"].isin(cases)].copy()

    events = []
    global_order = 0
    for case_id, g in df.groupby("Incident ID", sort=False):
        g = g.reset_index(drop=True)
        if len(g) < 3:
            continue
        prev_event_id = None
        entropy = 0.35
        for i, row in g.iterrows():
            activity = str(row["IncidentActivity_Type"])
            event_type = classify_activity(activity, i == 0, i == len(g) - 1)
            eb, ea = entropy_for_event_type(event_type, entropy)
            entropy = ea
            damaged = 1 if event_type in {"disruption", "loss"} else 0
            repaired = 1 if event_type in {"repair", "recovery", "closure"} else 0
            event_id = f"{case_id}__{i}"
            component = activity[:80] if activity.strip() else "activity"
            if event_type in {"disruption", "loss"}:
                target = f"{component}_damaged"
            elif event_type in {"repair", "recovery", "closure"}:
                target = f"{component}_restored"
            else:
                target = f"{component}_propagated"
            events.append(PruningEvent(event_id, global_order, event_type, str(case_id), i > 0, prev_event_id, float(eb), float(ea), float(ea-eb), damaged, repaired, component, target))
            prev_event_id = event_id
            global_order += 1
    return events

def reachable_count(adj, source):
    if source not in adj:
        return 0
    seen = {source}
    q = deque([source])
    while q:
        u = q.popleft()
        for v in adj.get(u, set()):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen)

def graph_coherence(adj, active_nodes):
    if not active_nodes or "source" not in active_nodes:
        return 0.0
    reach = reachable_count(adj, "source") / max(1, len(active_nodes))
    edge_count = sum(len(adj.get(n, set())) for n in active_nodes)
    edge_coherence = 1.0 - math.exp(-edge_count / max(1, len(active_nodes)))
    return max(0.0, min(1.0, 0.65 * reach + 0.35 * edge_coherence))

def entropy_transition_valid(e):
    if e.event_type in {"source", "neutral"}:
        return abs(e.entropy_after - e.entropy_before) < 1e-12
    if e.event_type in {"disruption", "loss"}:
        return e.entropy_after >= e.entropy_before
    if e.event_type in {"repair", "recovery", "closure"}:
        return e.entropy_after <= e.entropy_before
    return False

def certify_lineage(events):
    ordered = sorted(events, key=lambda e: e.pruning_order_index)
    active_ids, seen_ids = set(), set()
    structural_failures, entropy_failures, phase_failures = [], [], []
    any_source, damage_seen = False, False
    adj, active_nodes = defaultdict(set), set()
    entropy_checks = entropy_valid = 0

    for e in ordered:
        if e.event_id in seen_ids:
            structural_failures.append(f"duplicate_event_id:{e.event_id}")
        seen_ids.add(e.event_id)
        if e.event_type == "source":
            any_source = True
        if e.event_type != "source" and not any_source:
            structural_failures.append(f"non_source_before_source:{e.event_id}")
        if e.requires_prior and e.prior_dependency not in active_ids:
            structural_failures.append(f"missing_prior_event_dependency:{e.event_id}->{e.prior_dependency}")
        if e.event_type != "source":
            prior_ok = any(x.event_id == e.prior_dependency and x.provenance_id == e.provenance_id for x in ordered)
            if not prior_ok:
                structural_failures.append(f"provenance_lineage_violation:{e.event_id}:{e.provenance_id}")

        entropy_checks += 1
        if entropy_transition_valid(e):
            entropy_valid += 1
        else:
            entropy_failures.append(f"entropy_arrow_violation:{e.event_id}")

        if e.event_type in {"disruption", "loss"}:
            damage_seen = True
        if e.event_type in {"repair", "recovery", "closure"} and not damage_seen:
            phase_failures.append(f"repair_before_damage:{e.event_id}:{e.event_type}")

        active_ids.add(e.event_id)
        a, t = e.affected_node or "activity", e.repair_target or "activity"
        active_nodes.update(["source", a, t])
        if e.event_type == "source":
            adj["source"].update([a, t])
        elif e.event_type in {"disruption", "loss"}:
            adj["source"].add(a)
            adj[a].add(t)
        elif e.event_type in {"neutral", "repair", "recovery", "closure"}:
            adj["source"].add(a)
            adj[a].add(t)
            adj[t].add("source")

    P = 1.0 if len(structural_failures) == 0 and len(phase_failures) == 0 and any_source else 0.0
    E = entropy_valid / max(1, entropy_checks)
    entropy_violation_rate = len(entropy_failures) / max(1, entropy_checks)
    terminal_state = ordered[-1].event_type if ordered else "none"
    eligible = terminal_state in {"recovery", "closure"} and damage_seen
    admissible = P == 1.0 and entropy_violation_rate <= ENTROPY_TOLERANCE

    if admissible:
        repaired_fraction = 1.0 if eligible else 0.0
        geom = graph_coherence(adj, active_nodes)
        C = repaired_fraction * geom
        M = C * P * E
    else:
        geom = C = M = 0.0

    return {
        "eligible": bool(eligible),
        "passed": bool(eligible and M >= CLOSURE_THRESHOLD),
        "M_total": float(M),
        "C_topological": float(C),
        "P_sequence": float(P),
        "E_arrow": float(E),
        "entropy_violation_rate": float(entropy_violation_rate),
        "geom": float(geom),
        "structural_failure_count": len(structural_failures),
        "entropy_failure_count": len(entropy_failures),
        "phase_failure_count": len(phase_failures),
        "damage_seen": bool(damage_seen),
        "terminal_state": terminal_state,
        "geometry_computed_on_inadmissible_slice": False,
    }

def group_by_provenance(events):
    groups = defaultdict(list)
    for e in events:
        groups[e.provenance_id].append(e)
    return dict(groups)

def aggregate(rows, label):
    df = pd.DataFrame(rows)
    eligible = df[df["eligible"] == True] if len(df) else df
    if len(eligible) == 0:
        return {"label": label, "n": 0, "passed": False, "mean_M_total": 0.0, "pass_fraction": 0.0, "no_inadmissible_geometry": True}

    m = eligible["M_total"].to_numpy(float)
    pass_fraction = float(np.mean(m >= CLOSURE_THRESHOLD))
    return {
        "label": label,
        "n": int(len(eligible)),
        "passed": bool(float(np.mean(m)) >= CLOSURE_THRESHOLD and pass_fraction >= PASS_FRACTION_THRESHOLD),
        "mean_M_total": float(np.mean(m)),
        "median_M_total": float(np.median(m)),
        "pass_fraction": pass_fraction,
        "mean_geom": float(eligible["geom"].mean()),
        "mean_E_arrow": float(eligible["E_arrow"].mean()),
        "structural_failure_count": int(eligible["structural_failure_count"].sum()),
        "entropy_failure_count": int(eligible["entropy_failure_count"].sum()),
        "phase_failure_count": int(eligible["phase_failure_count"].sum()),
        "no_inadmissible_geometry": bool((~eligible["geometry_computed_on_inadmissible_slice"]).all()),
    }

def clone_event(e, **kwargs):
    d = asdict(e)
    d.update(kwargs)
    return PruningEvent(**d)

def null_event_order_shuffle(events):
    s = events[:]
    random.shuffle(s)
    return [clone_event(e, pruning_order_index=i) for i, e in enumerate(s)]

def null_provenance_shuffle(events):
    return [clone_event(e, provenance_id=f"SHUFFLED_{i % 97}") for i, e in enumerate(events)]

def null_repair_before_disruption(events):
    priority = {"source": 0, "repair": 1, "recovery": 2, "closure": 3, "neutral": 4, "disruption": 5, "loss": 6}
    s = sorted(events, key=lambda e: (e.provenance_id, priority.get(e.event_type, 9), e.pruning_order_index))
    return [clone_event(e, pruning_order_index=i) for i, e in enumerate(s)]

def null_source_removed(events):
    return [clone_event(e, pruning_order_index=i) for i, e in enumerate([x for x in events if x.event_type != "source"])]

def null_entropy_arrow_reverse(events):
    return [clone_event(e, entropy_before=e.entropy_after, entropy_after=e.entropy_before, state_delta=-e.state_delta) for e in events]

def null_closure_only_static(events):
    return [PruningEvent("STATIC_CLOSURE_ONLY", 0, "closure", "STATIC", True, "MISSING", 0.2, 0.1, -0.1, damaged_dependencies=1, repaired_dependencies=1, affected_node="static", repair_target="static_restored")]

def null_neutral_only_static(events):
    return [PruningEvent("STATIC_NEUTRAL_ONLY", 0, "neutral", "STATIC", True, "MISSING", 0.35, 0.35, 0.0, damaged_dependencies=0, repaired_dependencies=0, affected_node="static", repair_target="static_propagated")]

def null_terminal_label_only(events):
    s = events[:]
    return [clone_event(e, event_type="closure" if i == len(s) - 1 else "neutral") for i, e in enumerate(s)]

NULL_BUILDERS = {
    "event_order_shuffle": null_event_order_shuffle,
    "provenance_shuffle": null_provenance_shuffle,
    "repair_before_disruption": null_repair_before_disruption,
    "source_removed": null_source_removed,
    "entropy_arrow_reverse": null_entropy_arrow_reverse,
    "closure_only_static": null_closure_only_static,
    "neutral_only_static": null_neutral_only_static,
    "terminal_label_only_null": null_terminal_label_only,
}

def certify_dataset(events, label):
    rows = [certify_lineage(g) for g in group_by_provenance(events).values()]
    return rows, aggregate(rows, label)

def main():
    print("=== V1472.43 BPI2014 ENTROPY + PHASE-ORDER REPAIR ===")
    print(json.dumps(MANIFEST, indent=2))

    events = load_and_adapt(DATA_FILE)
    real_rows, real_agg = certify_dataset(events, "bpi2014_true_trace")
    print(f"\n[TRUE TRACE] Mean M_total: {real_agg['mean_M_total']:.4f} | Pass: {real_agg['passed']}")

    null_aggs = {}
    all_nulls_fail = True
    print("\n--- NULL SUITE ATTACKS ---")
    for name, builder in NULL_BUILDERS.items():
        null_events = builder(events)
        _, null_agg = certify_dataset(null_events, name)
        null_aggs[name] = null_agg
        if null_agg["passed"]:
            all_nulls_fail = False
        print(f"[{name}] Mean M_total: {null_agg['mean_M_total']:.4f} | Pass: {null_agg['passed']} | PhaseFail: {null_agg.get('phase_failure_count', 0)} | EntropyFail: {null_agg.get('entropy_failure_count', 0)}")

    no_bad_geometry = real_agg.get("no_inadmissible_geometry", False) and all(a.get("no_inadmissible_geometry", True) for a in null_aggs.values())
    final_pass = bool(real_agg["passed"] and all_nulls_fail and no_bad_geometry)

    summary = {
        "manifest": MANIFEST,
        "real_aggregate": real_agg,
        "null_aggregates": null_aggs,
        "all_nulls_fail": all_nulls_fail,
        "no_inadmissible_geometry_computed": no_bad_geometry,
        "final_verdict": "PASS_FULL_NULL_SUITE_REPAIRED_CERTIFICATION" if final_pass else "FAIL_FULL_NULL_SUITE_REPAIRED_CERTIFICATION",
        "interpretation": "Entropy + phase-order repaired law survived full null suite. Evidence candidate only." if final_pass else "Repaired law did not survive full null suite. Preserve as negative/partial evidence."
    }

    with open(f"{OUTPUT_PREFIX}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    pd.DataFrame(real_rows).to_csv(f"{OUTPUT_PREFIX}_real_lineages.csv", index=False)
    pd.DataFrame([real_agg]).to_csv(f"{OUTPUT_PREFIX}_real_aggregate.csv", index=False)
    pd.DataFrame([{"null": k, **v} for k, v in null_aggs.items()]).to_csv(f"{OUTPUT_PREFIX}_null_aggregates.csv", index=False)

    print("\n=== FINAL VERDICT ===")
    print(summary["final_verdict"])
    print(summary["interpretation"])

if __name__ == "__main__":
    main()
