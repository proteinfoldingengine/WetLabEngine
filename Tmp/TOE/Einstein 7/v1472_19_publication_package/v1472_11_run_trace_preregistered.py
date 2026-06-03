#!/usr/bin/env python3
"""
V1472.9 Reproducibility Package

Run:
    python v1472_9_run_trace.py sample_incident_trace.csv
    python v1472_9_run_trace.py your_trace.csv
    python v1472_9_run_trace.py your_trace.json
    python v1472_9_run_trace.py your_trace.jsonl

Purpose:
    Validate whether an external pruning-order recoverability trace passes:
    1. import/canonicalization
    2. causal governor
    3. admissible-slice geometry gate
    4. null suite

Core axiom:
    No pruning-order trace, no empirical geometry claim.

Critical rule:
    Geometry-like closure is never computed on inadmissible slices.

Claim boundary:
    This harness does not prove physical spacetime, GR, physical curvature,
    or a full geometry theorem. A real independent trace passing the harness
    is empirical evidence candidate only.
"""

from __future__ import annotations
import csv, json, math, random, sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Literal, Iterable, List, Dict, Any
from collections import defaultdict, deque

SEED = 147290
random.seed(SEED)

EventType = Literal["source", "disruption", "loss", "repair", "recovery", "closure"]
RecoveryStatus = Literal["none", "attempted", "partial", "complete", "failed"]

@dataclass(frozen=True)
class PruningEvent:
    event_id: str
    pruning_order_index: int
    event_type: EventType
    provenance_id: str
    requires_prior: bool
    prior_dependency: Optional[str]
    entropy_before: float
    entropy_after: float
    state_delta: float
    recovery_status: RecoveryStatus
    damaged_dependencies: int = 0
    repaired_dependencies: int = 0
    affected_node: Optional[str] = None
    repair_target: Optional[str] = None
    raw_event_type: Optional[str] = None

ALIASES = {
    "event_id": ["event_id", "log_id", "id"],
    "pruning_order_index": ["pruning_order_index", "seq", "sequence", "order_index"],
    "raw_event_type": ["kind", "event_kind", "event_type", "raw_event_type"],
    "provenance_id": ["provenance_id", "ticket", "session", "trace_id", "run_id", "incident_id"],
    "prior_dependency": ["prior_dependency", "depends_on", "parent_event_id", "previous_event_id"],
    "entropy_before": ["entropy_before", "disorder_before", "risk_before"],
    "entropy_after": ["entropy_after", "disorder_after", "risk_after"],
    "damaged_dependencies": ["damaged_dependencies", "damaged", "failed_count", "lost_dependencies"],
    "repaired_dependencies": ["repaired_dependencies", "repaired", "restored_count", "recovered_dependencies"],
    "affected_node": ["affected_node", "component", "service", "resource"],
    "repair_target": ["repair_target", "target", "restored_node"],
}

EVENT_MAP = {
    "incident_open": ("source", "none"), "start": ("source", "none"), "source": ("source", "none"),
    "failure_detected": ("disruption", "none"), "disruption": ("disruption", "none"), "error": ("disruption", "none"),
    "data_loss_detected": ("loss", "none"), "loss": ("loss", "none"), "degradation": ("loss", "none"),
    "mitigation_started": ("repair", "partial"), "repair": ("repair", "partial"), "rollback": ("repair", "partial"), "retry": ("repair", "partial"),
    "recovery_verified": ("recovery", "complete"), "recovery": ("recovery", "complete"), "restored": ("recovery", "complete"),
    "incident_closed": ("closure", "complete"), "closure": ("closure", "complete"), "closed": ("closure", "complete"), "commit": ("closure", "complete"),
}

def load_rows(path: Path) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    if suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "events" in data:
            return data["events"]
    raise ValueError(f"Unsupported input format or JSON shape: {path}")

def first_present(row: Dict[str, Any], canonical: str):
    for k in ALIASES[canonical]:
        if k in row and row[k] not in ("", None):
            return row[k]
    return None

def adapt_rows(rows: List[Dict[str, Any]]) -> List[PruningEvent]:
    events = []
    for row in rows:
        raw_kind = str(first_present(row, "raw_event_type") or "").strip()
        if raw_kind not in EVENT_MAP:
            raise ValueError(f"Unmapped event type: {raw_kind}")
        event_type, recovery_status = EVENT_MAP[raw_kind]
        event_id = str(first_present(row, "event_id") or "")
        order = int(first_present(row, "pruning_order_index"))
        provenance = str(first_present(row, "provenance_id") or "")
        prior = first_present(row, "prior_dependency")
        entropy_before = float(first_present(row, "entropy_before"))
        entropy_after = float(first_present(row, "entropy_after"))
        damaged = int(float(first_present(row, "damaged_dependencies") or 0))
        repaired = int(float(first_present(row, "repaired_dependencies") or 0))
        affected = first_present(row, "affected_node")
        target = first_present(row, "repair_target")

        if target is None and affected:
            # Generic adapter relation:
            # source introduces the affected component;
            # disruptions/losses mark damaged states;
            # repair/recovery/closure restore toward a stable component node.
            if event_type == "source":
                target = affected
            elif event_type in {"disruption", "loss"}:
                target = f"{affected}_damaged"
            elif event_type in {"repair", "recovery", "closure"}:
                target = f"{affected}_restored"

        events.append(PruningEvent(
            event_id=event_id,
            pruning_order_index=order,
            event_type=event_type,  # type: ignore[arg-type]
            provenance_id=provenance,
            requires_prior=(event_type != "source"),
            prior_dependency=prior if event_type != "source" else None,
            entropy_before=entropy_before,
            entropy_after=entropy_after,
            state_delta=entropy_after - entropy_before,
            recovery_status=recovery_status,  # type: ignore[arg-type]
            damaged_dependencies=damaged,
            repaired_dependencies=repaired,
            affected_node=affected,
            repair_target=target,
            raw_event_type=raw_kind,
        ))
    return sorted(events, key=lambda e: e.pruning_order_index)

def entropy_valid(e: PruningEvent) -> bool:
    if e.event_type == "source":
        return True
    if e.event_type in {"disruption", "loss"}:
        return e.entropy_after >= e.entropy_before
    if e.event_type in {"repair", "recovery", "closure"}:
        return e.entropy_after <= e.entropy_before
    return False

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
    edge_coherence = 1 - math.exp(-edge_count / max(1, len(active_nodes)))
    return max(0.0, min(1.0, 0.65 * reach + 0.35 * edge_coherence))

def certify(events: Iterable[PruningEvent], closure_threshold=0.0) -> Dict[str, Any]:
    ordered = sorted(list(events), key=lambda e: e.pruning_order_index)
    active_ids, seen_ids, seen_idx = set(), set(), set()
    source_seen = False
    source_prov = None
    failure = []
    hist = []
    events_seen = []
    seq_checks = seq_valid = 0
    ent_checks = ent_valid = 0
    active_nodes = set()
    adj = defaultdict(set)
    last_idx = None

    for tau, e in enumerate(ordered):
        local = []
        seq_checks += 1
        if e.pruning_order_index in seen_idx:
            local.append(f"duplicate_pruning_order_index:{e.pruning_order_index}")
        else:
            seen_idx.add(e.pruning_order_index)
            seq_valid += 1

        if last_idx is not None:
            seq_checks += 1
            if e.pruning_order_index > last_idx:
                seq_valid += 1
            else:
                local.append(f"non_monotonic_pruning_order:{e.event_id}")
        last_idx = e.pruning_order_index

        seq_checks += 1
        if e.event_id in seen_ids:
            local.append(f"duplicate_event_id:{e.event_id}")
        else:
            seen_ids.add(e.event_id)
            seq_valid += 1

        if e.event_type == "source" and not source_seen:
            source_seen = True
            source_prov = e.provenance_id
            active_nodes.add("source")

        if e.event_type != "source":
            seq_checks += 1
            if source_seen:
                seq_valid += 1
            else:
                local.append(f"non_source_before_source:{e.event_id}")

        if e.requires_prior:
            seq_checks += 1
            # critical rule: prior_dependency must be a prior event_id only
            if e.prior_dependency in active_ids:
                seq_valid += 1
            else:
                local.append(f"missing_prior_event_dependency:{e.event_id}->{e.prior_dependency}")

        if e.event_type != "source":
            seq_checks += 1
            if source_prov is not None and e.provenance_id == source_prov:
                seq_valid += 1
            else:
                local.append(f"unauthorized_provenance:{e.event_id}:{e.provenance_id}")

        ent_checks += 1
        if entropy_valid(e):
            ent_valid += 1
        else:
            local.append(f"entropy_arrow_violation:{e.event_id}")

        active_ids.add(e.event_id)
        events_seen.append(e)
        if e.affected_node:
            active_nodes.add(e.affected_node)
        if e.repair_target:
            active_nodes.add(e.repair_target)
        if e.event_type == "source" and e.affected_node:
            adj["source"].add(e.affected_node)
            if e.repair_target:
                adj["source"].add(e.repair_target)
        if e.event_type in {"repair", "recovery", "closure"} and e.affected_node and e.repair_target:
            adj[e.affected_node].add(e.repair_target)

        failure.extend(local)
        P = seq_valid / max(1, seq_checks)
        E = ent_valid / max(1, ent_checks)
        admissible = (len(failure) == 0 and source_seen and P == 1.0 and E == 1.0)

        damaged = sum(max(0, x.damaged_dependencies) for x in events_seen)
        repaired = sum(max(0, x.repaired_dependencies) for x in events_seen)
        repaired_fraction = 0.0 if damaged <= 0 else max(0.0, min(1.0, repaired / damaged))

        if admissible:
            geom = graph_coherence(adj, active_nodes)
            computed = True
        else:
            geom = None
            computed = False

        C = repaired_fraction * geom if computed else 0.0
        M = C * P * E if admissible else 0.0
        hist.append({
            "tau": tau,
            "event_id": e.event_id,
            "event_type": e.event_type,
            "pruning_order_index": e.pruning_order_index,
            "provenance_id": e.provenance_id,
            "admissible_slice": admissible,
            "P_sequence": P,
            "E_arrow": E,
            "repaired_fraction": repaired_fraction,
            "geometry_like_closure": geom,
            "geometry_computed": computed,
            "C_closure": C,
            "M_total": M,
            "local_failures": local,
            "failure_count_so_far": len(failure),
        })

    final = hist[-1] if hist else {}
    bad_geom = any((not h["admissible_slice"]) and h["geometry_computed"] for h in hist)
    passed = bool(len(failure) == 0 and source_seen and final.get("M_total", 0.0) >= closure_threshold and not bad_geom)
    return {
        "passed": passed,
        "M_total": final.get("M_total", 0.0),
        "C_closure": final.get("C_closure", 0.0),
        "P_sequence": final.get("P_sequence", 0.0),
        "E_arrow": final.get("E_arrow", 0.0),
        "repaired_fraction": final.get("repaired_fraction", 0.0),
        "geometry_like_closure": final.get("geometry_like_closure", None),
        "geometry_computed_final": final.get("geometry_computed", False),
        "geometry_computed_on_inadmissible_slice": bad_geom,
        "source_seen": source_seen,
        "source_provenance": source_prov,
        "failure_reasons": failure,
        "events_processed": len(events_seen),
        "slice_history": hist,
    }

def rows_from_events(events: List[PruningEvent]) -> List[Dict[str, Any]]:
    rows = []
    for e in events:
        rows.append({
            "log_id": e.event_id,
            "seq": e.pruning_order_index,
            "kind": e.raw_event_type or e.event_type,
            "ticket": e.provenance_id,
            "depends_on": e.prior_dependency or "",
            "entropy_before": e.entropy_before,
            "entropy_after": e.entropy_after,
            "damaged": e.damaged_dependencies,
            "repaired": e.repaired_dependencies,
            "component": e.affected_node or "",
            "target": e.repair_target or "",
        })
    return rows

def event_order_shuffle(events):
    rows = rows_from_events(events)
    random.shuffle(rows)
    for i, r in enumerate(rows):
        r["seq"] = i
    return adapt_rows(rows)

def provenance_shuffle(events):
    rows = rows_from_events(events)
    for i, r in enumerate(rows):
        r["ticket"] = f"BAD-{i}"
    return adapt_rows(rows)

def repair_before_disruption(events):
    rows = rows_from_events(events)
    priority = {
        "incident_open": 0, "source": 0,
        "mitigation_started": 1, "repair": 1, "retry": 1, "rollback": 1,
        "recovery_verified": 2, "recovery": 2,
        "incident_closed": 3, "closure": 3,
        "failure_detected": 4, "disruption": 4, "error": 4,
        "data_loss_detected": 5, "loss": 5,
    }
    rows = sorted(rows, key=lambda r: priority.get(r["kind"], 99))
    for i, r in enumerate(rows):
        r["seq"] = i
    return adapt_rows(rows)

def source_removed(events):
    rows = [r for r in rows_from_events(events) if EVENT_MAP.get(r["kind"], (r["kind"], ""))[0] != "source"]
    return adapt_rows(rows)

def entropy_reverse(events):
    rows = rows_from_events(events)
    for r in rows:
        r["entropy_before"], r["entropy_after"] = r["entropy_after"], r["entropy_before"]
    return adapt_rows(rows)

def closure_only_static(events):
    rows = rows_from_events(events)
    damaged = sum(int(float(r.get("damaged") or 0)) for r in rows)
    repaired = sum(int(float(r.get("repaired") or 0)) for r in rows)
    return adapt_rows([{
        "log_id": "STATIC_CLOSE",
        "seq": 0,
        "kind": "incident_closed",
        "ticket": rows[0].get("ticket", "TRACE") if rows else "TRACE",
        "depends_on": "MISSING_RECOVERY",
        "entropy_before": 0.25,
        "entropy_after": 0.12,
        "damaged": damaged,
        "repaired": repaired,
        "component": "static",
    }])


def threshold_decision(results: Dict[str, Any], threshold: float) -> Dict[str, Any]:
    real = results["real_trace"]
    nulls = {k: v for k, v in results.items() if k != "real_trace"}

    real_passes_threshold = (
        len(real["failure_reasons"]) == 0
        and real["source_seen"]
        and real["M_total"] >= threshold
        and not real["geometry_computed_on_inadmissible_slice"]
    )

    nulls_passing = []
    for name, nr in nulls.items():
        null_pass = (
            len(nr["failure_reasons"]) == 0
            and nr["source_seen"]
            and nr["M_total"] >= threshold
            and not nr["geometry_computed_on_inadmissible_slice"]
        )
        if null_pass:
            nulls_passing.append(name)

    no_inadmissible_geometry = all(
        not r["geometry_computed_on_inadmissible_slice"] for r in results.values()
    )

    return {
        "threshold": threshold,
        "real_M_total": real["M_total"],
        "real_passes_threshold": real_passes_threshold,
        "nulls_passing": nulls_passing,
        "all_nulls_fail": len(nulls_passing) == 0,
        "no_inadmissible_geometry": no_inadmissible_geometry,
        "certified_at_threshold": bool(real_passes_threshold and len(nulls_passing) == 0 and no_inadmissible_geometry),
    }


def make_threshold_sweep(results: Dict[str, Any]) -> list[Dict[str, Any]]:
    return [threshold_decision(results, th) for th in [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]]


def run_pipeline(input_path: Path, threshold: float, pilot_small_trace: bool = False) -> Dict[str, Any]:
    rows = load_rows(input_path)
    trace = adapt_rows(rows)

    families = {
        "real_trace": trace,
        "event_order_shuffle_null": event_order_shuffle(trace),
        "provenance_shuffle_null": provenance_shuffle(trace),
        "repair_before_disruption_null": repair_before_disruption(trace),
        "source_removed_null": source_removed(trace),
        "entropy_arrow_reverse_null": entropy_reverse(trace),
        "closure_only_static_null": closure_only_static(trace),
    }
    results = {k: certify(v, closure_threshold=0.0) for k, v in families.items()}

    threshold_result = threshold_decision(results, threshold)
    sweep = make_threshold_sweep(results)

    decision = (
        "trace_certified_at_preregistered_threshold"
        if threshold_result["certified_at_threshold"]
        else "trace_not_certified_at_preregistered_threshold"
    )

    return {
        "document_id": "V1472_11_THRESHOLD_PREREGISTERED_RUN",
        "input_file": str(input_path),
        "decision": decision,
        "preregistered_threshold": threshold,
        "pilot_small_trace": pilot_small_trace,
        "core_axiom": "No pruning-order trace, no empirical geometry claim.",
        "claim_boundary": (
            "Threshold must be declared before scoring. Passing this harness is an empirical evidence candidate, "
            "not proof of physical geometry, physical spacetime, GR, or ADM closure."
        ),
        "threshold_result": threshold_result,
        "threshold_sweep": sweep,
        "results": results,
        "canonical_trace": [asdict(e) for e in trace],
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="V1472.11 threshold-preregistered pruning-order trace runner")
    parser.add_argument("trace", help="Input CSV/JSON/JSONL trace")
    parser.add_argument("--threshold", type=float, required=True, help="Preregistered certification threshold, e.g. 0.70")
    parser.add_argument("--pilot-small-trace", action="store_true", help="Declare this as a small-trace pilot before scoring")
    args = parser.parse_args()

    if args.threshold <= 0 or args.threshold > 1:
        raise SystemExit("--threshold must be in (0, 1]")

    if args.pilot_small_trace and args.threshold > 0.40:
        print("Warning: --pilot-small-trace declared with threshold > 0.40. That is allowed but stricter than the default pilot policy.")

    if not args.pilot_small_trace and args.threshold < 0.70:
        print("Warning: Non-pilot real traces should normally use threshold >= 0.70 per V1472.10 preregistration policy.")

    path = Path(args.trace)
    result = run_pipeline(path, threshold=args.threshold, pilot_small_trace=args.pilot_small_trace)

    suffix = f".v1472_11_threshold_{args.threshold:.2f}_results.json"
    out = path.with_suffix(path.suffix + suffix)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps({
        "input_file": str(path),
        "decision": result["decision"],
        "preregistered_threshold": args.threshold,
        "pilot_small_trace": args.pilot_small_trace,
        "real_M_total": result["threshold_result"]["real_M_total"],
        "real_passes_threshold": result["threshold_result"]["real_passes_threshold"],
        "all_nulls_fail": result["threshold_result"]["all_nulls_fail"],
        "no_inadmissible_geometry": result["threshold_result"]["no_inadmissible_geometry"],
        "certified_at_threshold": result["threshold_result"]["certified_at_threshold"],
        "output": str(out),
    }, indent=2))

if __name__ == "__main__":
    main()
