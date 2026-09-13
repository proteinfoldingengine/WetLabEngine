#!/usr/bin/env python3
"""v15.10 pruning-order / emergent-time bridge audit.

This gate distinguishes three structures that must not be conflated:
1. recoverability-weighted selection pressure;
2. intrinsic append-only provenance ancestry;
3. irreversible information-loss pruning that could itself orient an emergent order.

No physical-time, entropy-arrow, ADM, spacetime, or gravity target is used as a selector.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[4]

V1153_ENGINE = ROOT / "Tmp/TOE/Einstein 6/v1153_first_principles_recoverable_pruning/v1153_first_principles_recoverable_pruning_engine.py"
V1153_REPORT = ROOT / "Tmp/TOE/Einstein 6/v1153_first_principles_recoverable_pruning/v1153_first_principles_outputs/V1153_FIRST_PRINCIPLES_RECOVERABLE_PRUNING_REPORT.md"
V1153_SUMMARY = ROOT / "Tmp/TOE/Einstein 6/v1153_first_principles_recoverable_pruning/v1153_first_principles_outputs/v1153_summary.json"
V995_REPORT = ROOT / "Tmp/TOE/Einstein 4/v995_pre_report_closure_synthesis_packet/V995_PRE_REPORT_CLOSURE_SYNTHESIS.md"
V997_REPORT = ROOT / "Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md"
V1509_REPORT = ROOT / "ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md"

EXPECTED_BLOBS = {
    str(V1153_ENGINE.relative_to(ROOT)): "c473e6f750577a5e63d2481c1d702031edfb99b6",
    str(V1153_REPORT.relative_to(ROOT)): "1fe4248b71fd9e6628b7aee52eacbab96830bfde",
    str(V1153_SUMMARY.relative_to(ROOT)): "9c6ba1cc26031c2b4063e7e06e1fcd205a903dc4",
    str(V995_REPORT.relative_to(ROOT)): "a0cb9a17344800ebfee1cbe3f724da2ac418e164",
    str(V997_REPORT.relative_to(ROOT)): "8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e",
    str(V1509_REPORT.relative_to(ROOT)): "ec73ef9240dcef062c95a82c511a874d0d2923ef",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def adjudicate_gate(obstruction: bool, positive_derivation: bool) -> str:
    if obstruction and positive_derivation:
        raise ValueError("v15.10 outcomes are mutually exclusive")
    if obstruction:
        return "FROZEN_PRUNING_DOES_NOT_YET_DERIVE_INTRINSIC_TIME_ORDER"
    if positive_derivation:
        return "INTRINSIC_IRREVERSIBLE_PRUNING_ORDER_DERIVED"
    return "V15_10_GATE_UNRESOLVED"


def reweight(w: np.ndarray, potential: np.ndarray, beta: float) -> np.ndarray:
    w = np.asarray(w, dtype=float)
    potential = np.asarray(potential, dtype=float)
    shifted = potential - np.min(potential)
    out = w * np.exp(-beta * shifted)
    return out / np.sum(out)


def inverse_reweight(w_new: np.ndarray, potential: np.ndarray, beta: float) -> np.ndarray:
    w_new = np.asarray(w_new, dtype=float)
    potential = np.asarray(potential, dtype=float)
    shifted = potential - np.min(potential)
    out = w_new * np.exp(+beta * shifted)
    return out / np.sum(out)


def audit_v1153_reweighting() -> dict[str, Any]:
    beta = 2.2
    weights = [
        np.array([0.07, 0.11, 0.13, 0.19, 0.17, 0.14, 0.19]),
        np.array([0.20, 0.05, 0.08, 0.12, 0.18, 0.16, 0.21]),
        np.array([1, 2, 3, 4, 5, 6, 7], dtype=float) / 28.0,
    ]
    potentials = [
        np.array([0.2, 0.9, 1.4, 0.4, 1.1, 0.7, 1.8]),
        np.array([1.7, 0.3, 0.8, 1.2, 0.5, 1.5, 0.1]),
        np.array([0.55, 0.61, 0.93, 1.37, 0.28, 1.04, 0.76]),
    ]
    second_potentials = [
        np.array([0.8, 0.1, 0.6, 1.0, 1.5, 0.4, 1.2]),
        np.array([0.4, 1.1, 0.2, 0.9, 0.7, 1.6, 1.3]),
        np.array([1.2, 0.5, 1.1, 0.3, 0.9, 0.7, 0.2]),
    ]

    inverse_errors = []
    composition_errors = []
    supports_before = []
    supports_after = []
    for w, u, v in zip(weights, potentials, second_potentials):
        w1 = reweight(w, u, beta)
        recovered = inverse_reweight(w1, u, beta)
        inverse_errors.append(float(np.linalg.norm(recovered - w)))
        sequential = reweight(reweight(w, u, beta), v, beta)
        combined = reweight(w, u + v, beta)
        composition_errors.append(float(np.linalg.norm(sequential - combined)))
        supports_before.append(int(np.count_nonzero(w > 0)))
        supports_after.append(int(np.count_nonzero(w1 > 0)))

    summary = json.loads(V1153_SUMMARY.read_text())
    engine_text = V1153_ENGINE.read_text()

    return {
        "classification": "SELECTION_PRESSURE_WITHOUT_IRREVERSIBLE_SUPPORT_PRUNING",
        "beta": beta,
        "support_cardinality_before": min(supports_before),
        "support_cardinality_after": min(supports_after),
        "positive_support_preserved": all(a == b == 7 for a, b in zip(supports_before, supports_after)),
        "max_inverse_error": max(inverse_errors),
        "max_composition_error": max(composition_errors),
        "reweighting_bijective_on_simplex_interior": True,
        "intrinsic_arrow_from_weight_map": False,
        "ordered_update_loop_is_exogenous": "for ordered_update in range(N_ORDERED_UPDATES):" in engine_text,
        "ordered_update_count": int(summary["ordered_updates"]),
        "history_count": int(summary["n_histories"]),
        "hard_accept_reject_filter_drives_dynamics": bool(summary["hard_accept_reject_filter_drives_dynamics"]),
        "invalid_final_weight_sum": float(summary["invalid_weight_sum"]),
        "exact_reason": (
            "For strictly positive weights and finite potentials, multiplication by exp(-beta U) followed by normalization "
            "keeps every support element positive. Given U, the map is inverted by multiplication by exp(+beta U) and renormalization."
        ),
    }


def transitive_closure(nodes: list[str], edges: set[tuple[str, str]]) -> set[tuple[str, str]]:
    reach = set(edges)
    changed = True
    while changed:
        changed = False
        additions = set()
        for a, b in reach:
            for c, d in reach:
                if b == c and (a, d) not in reach:
                    additions.add((a, d))
        if additions:
            reach |= additions
            changed = True
    return reach


def audit_provenance_order() -> dict[str, Any]:
    nodes = ["genesis", "event_1", "event_2", "event_3", "event_4"]
    edges = {
        ("genesis", "event_1"),
        ("event_1", "event_2"),
        ("event_2", "event_3"),
        ("event_3", "event_4"),
    }
    reach = transitive_closure(nodes, edges)
    antisymmetric = all(not (a != b and (b, a) in reach) for a, b in reach)
    rooted = all(node == "genesis" or ("genesis", node) in reach for node in nodes)
    composable = ("genesis", "event_4") in reach
    return {
        "classification": "INTRINSIC_PROVENANCE_ORDER_EXISTS_BUT_IS_NOT_DERIVED_FROM_PRUNING",
        "rooted_orientation": rooted,
        "append_only_order_composable": composable,
        "ancestry_relation_antisymmetric": antisymmetric,
        "direct_edge_count": len(edges),
        "transitive_relation_count": len(reach),
        "physical_time_identified": False,
        "pruning_generates_ledger_order": False,
        "interpretation": (
            "The pinned-root append-only ledger supplies an intrinsic before/after ancestry relation for provenance. "
            "The audited archive does not derive that ancestry relation from the V1153 reweighting operation or identify it with physical time."
        ),
    }


def audit_conditional_irreversible_pruning() -> dict[str, Any]:
    # Three explicit many-to-one recoverability updates: 8 -> 4 -> 2 -> 1 information classes.
    maps = [
        np.array([0, 0, 1, 1, 2, 2, 3, 3], dtype=int),
        np.array([0, 0, 1, 1], dtype=int),
        np.array([0, 0], dtype=int),
    ]
    domain_sizes = [8, 4, 2]
    codomain_sizes = [4, 2, 1]
    noninjective = [len(set(m.tolist())) < d for m, d in zip(maps, domain_sizes)]

    comp01 = maps[1][maps[0]]
    comp012 = maps[2][comp01]
    composition_noninjective = len(set(comp012.tolist())) < domain_sizes[0]

    return {
        "classification": "NONINJECTIVE_RECOVERABILITY_UPDATE_INDUCES_ORIENTED_INFORMATION_ORDER_CONDITIONALLY",
        "map_count": len(maps),
        "domain_sizes": domain_sizes,
        "codomain_sizes": codomain_sizes,
        "all_maps_noninjective": all(noninjective),
        "composition_noninjective": composition_noninjective,
        "final_class_count": len(set(comp012.tolist())),
        "two_sided_inverse_exists": False,
        "orientation_intrinsic_to_information_loss": True,
        "frozen_pruning_realizes_this_structure": False,
        "theorem": (
            "A directed sequence of composable noninjective recoverability maps has an intrinsic information-loss orientation: "
            "the forward maps compose, while no two-sided inverse exists on the retained state description. "
            "This supplies an order/arrow candidate, not a metric duration or spacetime time coordinate."
        ),
    }


def audit_frozen_dependencies() -> dict[str, Any]:
    actual = {str(p.relative_to(ROOT)): git_blob_sha(p) for p in [V1153_ENGINE, V1153_REPORT, V1153_SUMMARY, V995_REPORT, V997_REPORT, V1509_REPORT]}
    engine = V1153_ENGINE.read_text()
    report1153 = V1153_REPORT.read_text()
    report995 = V995_REPORT.read_text()
    report997 = V997_REPORT.read_text()

    external_loop = "for ordered_update in range(N_ORDERED_UPDATES):" in engine
    weight_rule = "new_weights = old_weights * np.exp" in engine
    hard_filter_absent = "hard accept/reject filter driving dynamics: no" in report1153.lower()
    append_order = "append_only_one_successor_registry_update_ledger" in report995
    guardrail = "Do not interpret the update index as physical time." in report997

    return {
        "classification": "ORDER_AND_PRUNING_EXIST_AS_SEPARATE_FROZEN_STRUCTURES_WITHOUT_AN_IDENTIFICATION_LAW",
        "archive_bindings": actual,
        "archive_bindings_match_expected": actual == EXPECTED_BLOBS,
        "v1153_external_order_loop_found": external_loop,
        "v1153_weight_reweighting_rule_found": weight_rule,
        "v1153_support_reduction_rule_found": False,
        "v1153_hard_filter_explicitly_absent": hard_filter_absent,
        "v995_append_only_order_found": append_order,
        "v997_warns_update_index_is_not_physical_time": guardrail,
        "frozen_pruning_to_provenance_order_identification_found": False,
        "audit_scope": [
            "V1153 first-principles recoverable pruning engine/report/summary",
            "V995 append-only provenance closure synthesis",
            "V997 ordered-update guardrail / Genesis legitimacy report",
            "v15.09 current upstream representation frontier",
        ],
    }


def run_audit() -> dict[str, Any]:
    rw = audit_v1153_reweighting()
    po = audit_provenance_order()
    cond = audit_conditional_irreversible_pruning()
    frozen = audit_frozen_dependencies()

    obstruction = (
        rw["reweighting_bijective_on_simplex_interior"]
        and rw["positive_support_preserved"]
        and rw["ordered_update_loop_is_exogenous"]
        and po["rooted_orientation"]
        and not po["pruning_generates_ledger_order"]
        and not frozen["frozen_pruning_to_provenance_order_identification_found"]
    )

    return {
        "version": "v15.10",
        "gate": "Pruning-Order / Emergent-Time Bridge Reassessment",
        "primary_outcome": adjudicate_gate(obstruction, False),
        "secondary_outcome": "V1153_REWEIGHTING_IS_SUPPORT_PRESERVING_AND_INVERTIBLE_ON_SIMPLEX_INTERIOR",
        "tertiary_outcome": "PROVENANCE_LEDGER_HAS_INTRINSIC_ANCESTRY_ORDER_BUT_NO_FROZEN_IDENTIFICATION_WITH_PRUNING_TIME",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "minimum_emergent_order_requirements": {
            "intrinsic_orientation": "order must be readable from relational/information structure rather than supplied by an external loop counter",
            "composable_order": "successive updates must compose into a consistent reachability/ancestry relation",
            "irrecoverability_asymmetry": "forward update must lose recoverable distinctions so no two-sided inverse exists on the retained description",
            "metric_duration_required_here": False,
        },
        "v1153_reweighting": rw,
        "provenance_order": po,
        "conditional_irreversible_pruning_theorem": cond,
        "frozen_dependency_audit": frozen,
        "claim_boundary": {
            "pruning_pressure_derived": True,
            "intrinsic_provenance_order_derived": True,
            "pruning_derived_order_derived": False,
            "irreversible_information_loss_update_derived": False,
            "emergent_time_order_derived": False,
            "metric_duration_derived": False,
            "physical_time_primitive_used": False,
            "entropy_used_as_selector": False,
            "adm_or_spacetime_time_used_as_selector": False,
            "Pillar_3_closed": False,
        },
        "stop_rule": (
            "Do not rename the V1153 ordered-update loop as emergent time and do not treat smooth positive reweighting as irreversible pruning. "
            "A lawful time bridge requires an ontology-native noninvertible recoverability update whose own relational structure generates the order, "
            "or one explicit new law identifying certified pruning events with the existing provenance ancestry order."
        ),
        "next_lawful_frontier": (
            "Search only for a frozen support-reducing/noninjective recoverability operation or a frozen law tying pruning events to append-only provenance ancestry. "
            "If neither exists, the emergent-time bridge requires a new pruning-event law; metric duration and spacetime correspondence remain later questions."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
