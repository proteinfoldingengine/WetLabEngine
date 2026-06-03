#!/usr/bin/env python3
"""
Standalone V1472.1 causal governor synthetic trace harness.
Run:
    python v1472_1_causal_governor_harness.py
"""
from dataclasses import dataclass
from typing import Optional, Literal, Iterable
import random, json

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

def entropy_arrow_score(event):
    if event.event_type in {"source"}:
        return 1.0
    if event.event_type in {"disruption", "loss"}:
        return 1.0 if event.entropy_after >= event.entropy_before else 0.0
    if event.event_type in {"repair", "recovery", "closure"}:
        return 1.0 if event.entropy_after <= event.entropy_before else 0.0
    return 0.0

def certify_pruning_order_trace(events: Iterable[PruningEvent], closure_threshold: float = 0.7):
    ordered = sorted(list(events), key=lambda e: e.pruning_order_index)
    active_ledger, provenance_ledger = set(), set()
    seen_indices, seen_ids = set(), set()
    p_sequence, e_arrow_total, c_closure = 1.0, 1.0, 0.0
    last_idx, failure_reason = None, None

    for event in ordered:
        if event.pruning_order_index in seen_indices:
            return {"passed": False, "M_total": 0.0, "failure_reason": "duplicate_pruning_order_index"}
        seen_indices.add(event.pruning_order_index)
        if last_idx is not None and event.pruning_order_index <= last_idx:
            return {"passed": False, "M_total": 0.0, "failure_reason": "non_monotonic_pruning_order_index"}
        last_idx = event.pruning_order_index
        if event.event_id in seen_ids:
            return {"passed": False, "M_total": 0.0, "failure_reason": "duplicate_event_id"}
        if event.requires_prior and event.prior_dependency not in active_ledger and event.prior_dependency not in provenance_ledger:
            return {"passed": False, "M_total": 0.0, "failure_reason": f"missing_prior_dependency:{event.prior_dependency}"}
        if entropy_arrow_score(event) == 0.0:
            return {"passed": False, "M_total": 0.0, "failure_reason": f"entropy_arrow_violation:{event.event_id}"}

        seen_ids.add(event.event_id)
        active_ledger.add(event.event_id)
        provenance_ledger.add(event.provenance_id)

        if event.event_type == "closure" and event.recovery_status == "complete":
            c_closure = 1.0

    m_total = c_closure * p_sequence * e_arrow_total
    return {"passed": bool(m_total >= closure_threshold), "M_total": m_total, "failure_reason": failure_reason}

def valid_trace():
    return [
        PruningEvent("e0_source", 0, "source", "P0", False, None, 0.10, 0.10, 0.0, "none"),
        PruningEvent("e1_disruption", 1, "disruption", "P0", True, "e0_source", 0.10, 0.75, 0.65, "none"),
        PruningEvent("e2_loss", 2, "loss", "P0", True, "e1_disruption", 0.75, 0.90, 0.15, "none"),
        PruningEvent("e3_repair", 3, "repair", "P0", True, "e2_loss", 0.90, 0.55, -0.35, "attempted"),
        PruningEvent("e4_recovery", 4, "recovery", "P0", True, "e3_repair", 0.55, 0.25, -0.30, "complete"),
        PruningEvent("e5_closure", 5, "closure", "P0", True, "e4_recovery", 0.25, 0.12, -0.13, "complete"),
    ]

if __name__ == "__main__":
    base = valid_trace()
    bad = [e for e in base if e.event_type != "source"]
    print(json.dumps({
        "valid": certify_pruning_order_trace(base),
        "source_removed_null": certify_pruning_order_trace(bad)
    }, indent=2))
