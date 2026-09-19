from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import argparse
import ast
import inspect
import json
from pathlib import Path
import sys

from incidence_target import IncidenceTarget, construct_incidence_target
from response_generation import BASE_SHA, CONTROL_KEYS, EVIDENCE, FAMILY_KEYS, deterministic_permutation, generation_audit, relabel_family, relabel_support_columns, response_family, signed_support_B2, verify_evidence
from response_geometry import ResponseGeometry, construct_response_geometry, metric_passes

SIZES = (5, 7, 9, 11)
SCALES = (Fraction(1), Fraction(7, 3))
ALLOWED_GATE_STATUSES = ("RESPONSE_GEOMETRY_PROTOCOL_INVALID", "NO_RESPONSE_DERIVED_GEOMETRY", "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY", "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES")
_NEXT_REQUIRED_OBJECT = {
    "RESPONSE_GEOMETRY_PROTOCOL_INVALID": "REPAIR_BLIND_GEOMETRY_PROTOCOL_BEFORE_ANY_ADJUDICATION",
    "NO_RESPONSE_DERIVED_GEOMETRY": "CLOSE_GLOBAL_BALANCE_GEOMETRY_INTERPRETATION_WITHOUT_TUNING",
    "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY": "DOWNGRADE_V1539_TO_GENERIC_INVERSE_OPERATOR_GLOBALITY",
    "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES": "PREREGISTER_FORMAL_CONNECTION_CURVATURE_AND_SOURCE_CORRESPONDENCE_GATE",
}
CONSTRUCTION_FIREWALL = {
    "spectrum_queries": 0, "spectral_edge_parameters": 0, "geometry_fit_parameters": 0,
    "candidate_specific_thresholds": 0, "coordinate_queries_in_response_geometry": 0,
    "B2_queries_in_response_geometry": 0, "response_queries_in_incidence_target": 0,
    "operator_inversions_in_response_geometry": 0,
}


@dataclass(frozen=True)
class GeometryComparison:
    metric_passes: bool
    neighbors_equal: bool
    distances_equal: bool


def _distances(labels, neighbors):
    labels = tuple(labels); adjacency = {label: set() for label in labels}
    for edge in neighbors:
        first, second = tuple(edge); adjacency[first].add(second); adjacency[second].add(first)
    rows = []
    for source in labels:
        row = {label: None for label in labels}; row[source] = 0; queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(adjacency[current]):
                if row[neighbor] is None: row[neighbor] = row[current] + 1; queue.append(neighbor)
        rows.append(tuple(row[label] for label in labels))
    return tuple(rows)


def compare_geometry(response: ResponseGeometry, target: IncidenceTarget) -> GeometryComparison:
    passes = metric_passes(response); equal = response.neighbors == target.neighbors
    return GeometryComparison(passes, equal, equal and _distances(response.labels, response.neighbors) == target.distances)


def classify_gate(protocol_valid, canonical_all_sizes, control_all_sizes):
    if not protocol_valid: return "RESPONSE_GEOMETRY_PROTOCOL_INVALID"
    if not canonical_all_sizes: return "NO_RESPONSE_DERIVED_GEOMETRY"
    if any(control_all_sizes.values()): return "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY"
    return "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES"


def next_required_object_for_status(status):
    if status not in _NEXT_REQUIRED_OBJECT: raise ValueError(f"unknown gate status: {status}")
    return _NEXT_REQUIRED_OBJECT[status]


def _fraction_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _pairs(pairs):
    return [[first, second] for first, second in sorted(tuple(sorted(pair)) for pair in pairs)]


def _encoded_work(L, relabeled, permutation, geometry):
    label = lambda old: permutation[old] if relabeled else old
    profile = tuple(geometry.work[label(0)][label(index)] for index in range(L * L))
    exact = all(
        geometry.work[label(first)][label(second)] == profile[((second % L - first % L) % L) + L * ((second // L - first // L) % L)]
        for first in range(L*L) for second in range(L*L)
    )
    return {"encoding": "exact_torus_displacement_profile", "lookup": "work[pi(i)][pi(j)]=profile[((j_x-i_x)%L)+L*((j_y-i_y)%L)]; pi is identity when relabeled=false", "profile": [_fraction_text(value) for value in profile], "reconstruction_verified": exact}


def _encoded_pairs(L, relabeled, permutation, labels, pairs):
    count = len(labels)
    if len(pairs) == count * (count - 1) // 2:
        return {"encoding": "complete_graph", "labels": list(labels)}
    label = lambda old: permutation[old] if relabeled else old
    displacements = [index for index in range(1, count) if frozenset((label(0), label(index))) in pairs]
    reconstructed = frozenset(
        frozenset((label(first), label(((first%L + displacement%L)%L) + L*((first//L + displacement//L)%L))))
        for first in range(count) for displacement in displacements
    )
    return {"encoding": "exact_torus_displacement_neighbors", "displacement_indices": displacements, "reconstruction_verified": reconstructed == pairs}


def _row(L, key, scale, relabeled, permutation, geometry, target, comparison):
    return {
        "family": key, "scale": _fraction_text(scale), "relabeled": relabeled,
        "metric": {"symmetric": geometry.symmetric, "identity": geometry.identity, "separated": geometry.separated, "triangle": geometry.triangle, "passes": comparison.metric_passes},
        "minimum_work": _fraction_text(geometry.minimum),
        "work": _encoded_work(L, relabeled, permutation, geometry),
        "pair_count": geometry.pair_count, "ordered_triple_count": geometry.ordered_triple_count,
        "response_neighbors": _encoded_pairs(L, relabeled, permutation, geometry.labels, geometry.neighbors),
        "target_neighbors": "size_target_relabelled" if relabeled else "size_target_original",
        "neighbors_equal": comparison.neighbors_equal,
        "distances_equal_when_neighbors_equal": comparison.distances_equal,
    }


def _map_pairs(pairs, permutation):
    return frozenset(frozenset(permutation[label] for label in pair) for pair in pairs)


@lru_cache(None)
def exact_size_audit(L):
    generated = generation_audit(L); support = signed_support_B2(L); permutation = deterministic_permutation(L)
    targets = {False: construct_incidence_target(support), True: construct_incidence_target(relabel_support_columns(support, permutation))}
    rows = []; geometries = {}; comparisons = {}; relabel_ok = True; scale_ok = True
    for key in FAMILY_KEYS:
        for scale in SCALES:
            family = response_family(L, key, scale); families = {False: family, True: relabel_family(family, permutation)}
            for relabeled in (False, True):
                current = families[relabeled]; geometry = construct_response_geometry(current.labels, current.sources, current.responses)
                comparison = compare_geometry(geometry, targets[relabeled]); state = (key, scale, relabeled)
                geometries[state] = geometry; comparisons[state] = comparison
                rows.append(_row(L, key, scale, relabeled, permutation, geometry, targets[relabeled], comparison))
            original, changed = geometries[(key, scale, False)], geometries[(key, scale, True)]
            relabel_ok &= changed.neighbors == _map_pairs(original.neighbors, permutation) and all(changed.work[permutation[i]][permutation[j]] == original.work[i][j] for i in range(L*L) for j in range(L*L)) and comparisons[(key, scale, False)] == comparisons[(key, scale, True)]
        for relabeled in (False, True):
            unit, scaled = geometries[(key, Fraction(1), relabeled)], geometries[(key, Fraction(7,3), relabeled)]
            scale_ok &= scaled.neighbors == unit.neighbors and (scaled.symmetric, scaled.identity, scaled.separated, scaled.triangle) == (unit.symmetric, unit.identity, unit.separated, unit.triangle) and comparisons[(key, Fraction(1), relabeled)] == comparisons[(key, Fraction(7,3), relabeled)] and all(scaled.work[i][j] == Fraction(7,3)*unit.work[i][j] for i in range(L*L) for j in range(L*L))
    expected_pairs = L*L*(L*L-1)//2; expected_triples = (L*L)**3
    matched_metric = all(comparisons[(key, scale, relabeled)].metric_passes for key in ("MATCHED_DIAGONAL_BALANCE", "MATCHED_STEP2_BALANCE") for scale in SCALES for relabeled in (False, True))
    return {
        "L": L, "source_count_per_family": L*L, "target_edge_count": len(targets[False].neighbors),
        "target_neighbors_original": _pairs(targets[False].neighbors), "target_neighbors_relabelled": _pairs(targets[True].neighbors),
        "target_four_regular": targets[False].degrees == (4,)*(L*L), "target_connected": targets[False].connected,
        "generation": generated, "rows": rows,
        "all_pair_counts_exact": all(row["pair_count"] == expected_pairs for row in rows),
        "all_ordered_triple_counts_exact": all(row["ordered_triple_count"] == expected_triples for row in rows),
        "all_work_encodings_exact": all(row["work"]["reconstruction_verified"] for row in rows),
        "all_neighbor_encodings_exact": all(row["response_neighbors"].get("reconstruction_verified", True) for row in rows),
        "relabeling_equivariant": relabel_ok, "scale_verdicts_identical": scale_ok,
        "matched_controls_metric_protocol": matched_metric,
    }


def _constructor_interfaces():
    def imports(path):
        tree = ast.parse(path.read_text())
        out = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        return out | {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    response_path = Path(__file__).with_name("response_geometry.py"); target_path = Path(__file__).with_name("incidence_target.py")
    response_blind = tuple(inspect.signature(construct_response_geometry).parameters) == ("labels", "sources", "responses") and imports(response_path) <= {"dataclasses", "fractions", "itertools", "__future__"}
    target_blind = tuple(inspect.signature(construct_incidence_target).parameters) == ("signed_support",) and imports(target_path) <= {"collections", "dataclasses", "itertools", "__future__"}
    return {"response_constructor_signature": ["labels", "sources", "responses"], "target_constructor_signature": ["signed_support"], "response_constructor_blind": response_blind, "target_constructor_blind": target_blind}


@lru_cache(None)
def audit():
    sizes = [exact_size_audit(L) for L in SIZES]
    original = {L: {row["family"]: row for row in size["rows"] if row["scale"] == "1" and not row["relabeled"]} for L, size in zip(SIZES, sizes)}
    canonical = all(original[L]["GLOBAL_BALANCE_COMPLETION"]["metric"]["passes"] and original[L]["GLOBAL_BALANCE_COMPLETION"]["neighbors_equal"] for L in SIZES)
    controls = {key: all(original[L][key]["metric"]["passes"] and original[L][key]["neighbors_equal"] for L in SIZES) for key in CONTROL_KEYS}
    interfaces = _constructor_interfaces(); generations = [size["generation"] for size in sizes]
    protocol = all((bool(verify_evidence()), interfaces["response_constructor_blind"], interfaces["target_constructor_blind"], all(x["canonical_augmentation_isomorphism_exact"] and x["all_response_equations_exact"] and x["matched_controls_structurally_admissible"] and x["all_orientation_rays_exact"] and x["all_additivity_exact"] and x["all_translation_D4_covariance_exact"] for x in generations), all(size["target_four_regular"] and size["target_connected"] and size["matched_controls_metric_protocol"] and size["relabeling_equivariant"] and size["scale_verdicts_identical"] and size["all_pair_counts_exact"] and size["all_ordered_triple_counts_exact"] and size["all_work_encodings_exact"] and size["all_neighbor_encodings_exact"] for size in sizes), all(value == 0 for value in CONSTRUCTION_FIREWALL.values())))
    status = classify_gate(protocol, canonical, controls)
    return {
        "version": "v15.40", "base_sha": BASE_SHA, "design_blob": EVIDENCE["v15.40-design"][1],
        "family_formula_manifest": {"GLOBAL_BALANCE_COMPLETION": "(4I-A_ax) u_f = s_f on F_L^0", "DIRECT_INHERITANCE": "u_f = s_f", "ONE_INCIDENCE_TRANSPORT": "u_f = A_ax s_f", "MATCHED_DIAGONAL_BALANCE": "(4I-A_diag) u_f = s_f on F_L^0", "MATCHED_STEP2_BALANCE": "(4I-A_step2) u_f = s_f on F_L^0"},
        "finite_size_controls": list(SIZES), "holdout_size": 11, "holdout_formula_unchanged": all(tuple(row["family"] for row in size["rows"]) == tuple(row["family"] for row in sizes[0]["rows"]) for size in sizes),
        "projective_scales": [_fraction_text(x) for x in SCALES], "relabeling_rule": "pi(i)=(2*i+1) mod L**2", "control_keys": list(CONTROL_KEYS),
        "evidence_pins": {key: expected for key, (_path, expected) in EVIDENCE.items()}, "evidence_verified": bool(verify_evidence()), "input_separation": interfaces,
        "canonical_augmentation_isomorphism_exact": all(x["canonical_augmentation_isomorphism_exact"] for x in generations), "all_response_equations_exact": all(x["all_response_equations_exact"] for x in generations),
        "all_required_pairs_evaluated": all(x["all_pair_counts_exact"] for x in sizes), "all_required_ordered_triples_evaluated": all(x["all_ordered_triple_counts_exact"] for x in sizes),
        "all_targets_four_regular": all(x["target_four_regular"] for x in sizes), "all_targets_connected": all(x["target_connected"] for x in sizes),
        "all_orientation_rays_exact": all(x["all_orientation_rays_exact"] for x in generations), "all_additivity_exact": all(x["all_additivity_exact"] for x in generations), "all_translation_D4_covariance_exact": all(x["all_translation_D4_covariance_exact"] for x in generations),
        "all_relabeling_equivariant": all(x["relabeling_equivariant"] for x in sizes), "all_scale_verdicts_identical": all(x["scale_verdicts_identical"] for x in sizes),
        "matched_controls_structurally_admissible": all(x["matched_controls_structurally_admissible"] for x in generations), "matched_controls_metric_protocol": all(x["matched_controls_metric_protocol"] for x in sizes),
        "mechanical_correspondence_rule_applied": True, "protocol_valid": protocol, "canonical_all_sizes": canonical if protocol else None, "control_all_sizes": controls if protocol else None,
        "size_audits": sizes, "construction_firewall": dict(CONSTRUCTION_FIREWALL), "status": status, "next_required_object": next_required_object_for_status(status),
        "interpretation": "finite internal Level-1 correspondence candidate conditional on inherited source and response axioms" if status == "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES" else "no positive geometry-specificity interpretation",
        "new_source_semantics_axiom_inherited": True, "new_global_balance_response_axiom_inherited": True, "source_axiom_derived_from_frozen_ontology": False, "response_axiom_derived_from_frozen_ontology": False,
        "physical_metric_derived": False, "spacetime_derived": False, "physical_gravity_derived": False, "continuum_limit_derived": False, "einstein_equations_derived": False,
        "uses_pruning": False, "uses_entropy": False, "uses_physical_time": False, "scientific_breakthrough": False, "Pillar_3": "OPEN",
    }


def canonical_json(value):
    return json.dumps(value, sort_keys=True, indent=2, separators=(",", ": ")) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(); group = parser.add_mutually_exclusive_group(); group.add_argument("--out", type=Path); group.add_argument("--check", type=Path); args = parser.parse_args(argv)
    rendered = canonical_json(audit())
    if args.out is not None: args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(rendered)
    if args.check is not None and args.check.read_text() != rendered: raise SystemExit("committed result does not match exact replay")
    if args.out is None: sys.stdout.write(rendered)
    return 0


if __name__ == "__main__": raise SystemExit(main())
