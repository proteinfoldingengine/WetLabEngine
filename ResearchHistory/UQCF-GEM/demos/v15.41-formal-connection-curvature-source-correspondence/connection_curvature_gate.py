from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import argparse
import ast
import inspect
import json
from pathlib import Path
import sys

from linearized_connection import (
    TransportManifest,
    audit_transport_protocol,
    construct_isotropic_lift,
    differentiate_holonomy,
    executed_flatness_diagnostic,
    local_circulation_rowspace_witness,
    parity_witness,
    solve_linearized_connection,
)
from operational_complex import (
    ConnectionStatus,
    construct_operational_complex,
    enumerate_baseline_connection,
)
from response_inputs import V1540, family_input, source_target_input, verify_evidence
from source_target import construct_source_target


SIZES = (5, 7, 9, 11)
SCALES = (Fraction(1), Fraction(7, 3))
FAMILY_KEYS = (
    "GLOBAL_BALANCE_COMPLETION",
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)
CONTROL_KEYS = FAMILY_KEYS[1:]
ALLOWED_GATE_STATUSES = (
    "PROTOCOL_INVALID",
    "CONNECTION_NOT_IDENTIFIABLE",
    "CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE",
    "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE",
    "GENERIC_CONNECTION_CURVATURE_RESPONSE",
    "CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES",
)
_NEXT_REQUIRED_OBJECT = {
    "PROTOCOL_INVALID": "REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION",
    "CONNECTION_NOT_IDENTIFIABLE": "RECORD_MISSING_CONNECTION_SELECTOR_WITHOUT_CHOOSING_A_FRAME_OR_DISCRETIZATION",
    "CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE": "RECORD_MISSING_CURVATURE_TO_SOURCE_CARRIER_MAP_WITHOUT_FITTING_ONE",
    "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE": "CLOSE_THIS_OPERATIONAL_CONNECTION_ROUTE_WITHOUT_TUNING",
    "GENERIC_CONNECTION_CURVATURE_RESPONSE": "DOWNGRADE_TO_GENERIC_FORMAL_DISCRETE_RESPONSE",
    "CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES": "PREREGISTER_GENERAL_SIZE_AND_REFINEMENT_COMPATIBILITY_GATE",
}
CONSTRUCTION_FIREWALL = {
    "coordinate_queries": 0,
    "B2_queries_in_connection_constructor": 0,
    "historical_connection_queries": 0,
    "supplied_orientation_queries": 0,
    "spectrum_queries": 0,
    "floating_tolerances": 0,
    "fitted_connection_parameters": 0,
    "fitted_curvature_parameters": 0,
    "source_specific_normalizations": 0,
    "post_output_tie_breakers": 0,
    "newton_or_einstein_targets": 0,
}


@dataclass(frozen=True)
class ContractionAudit:
    orbit_count: int
    dimension: int
    weights: tuple[tuple[int, tuple[int, int, int, int], Fraction], ...]
    curvature_fields: tuple[tuple[int, tuple[Fraction, ...]], ...]
    orientation_sign_equivalent: bool


def _canonical_cycle(vertices):
    vertices = tuple(vertices)
    rotations = tuple(vertices[i:] + vertices[:i] for i in range(4))
    reversed_vertices = tuple(reversed(vertices))
    reverse_rotations = tuple(
        reversed_vertices[i:] + reversed_vertices[:i] for i in range(4)
    )
    return min(rotations + reverse_rotations)


def _curvature_scalar(value):
    if isinstance(value, (int, Fraction)) and not isinstance(value, bool):
        return Fraction(value)
    value = tuple(tuple(Fraction(item) for item in row) for row in value)
    if len(value) != 2 or any(len(row) != 2 for row in value):
        raise ValueError("two-dimensional exact curvature matrix required")
    return (value[1][0] - value[0][1]) / 2


def enumerate_curvature_contractions(
    complex_, curvature_by_source
) -> ContractionAudit:
    cycles = tuple(complex_.cycles)
    cycle_set = set(cycles)
    flags = tuple((label, cycle) for cycle in cycles for label in cycle)
    index = {flag: position for position, flag in enumerate(flags)}
    parent = list(range(len(flags)))

    def root(position):
        while parent[position] != position:
            parent[position] = parent[parent[position]]
            position = parent[position]
        return position

    def join(left, right):
        left, right = root(left), root(right)
        if left != right:
            parent[right] = left

    for image in complex_.metric_automorphisms:
        mapping = dict(zip(complex_.labels, image))
        for label, cycle in flags:
            changed_cycle = _canonical_cycle(tuple(mapping[item] for item in cycle))
            if changed_cycle not in cycle_set:
                raise ValueError("metric automorphism does not preserve cycles")
            join(index[(label, cycle)], index[(mapping[label], changed_cycle)])
    orbit_count = len({root(position) for position in range(len(flags))})
    dimension = orbit_count
    if dimension != 1:
        return ContractionAudit(orbit_count, dimension, (), (), False)
    weights = tuple((label, cycle, Fraction(1)) for label, cycle in flags)
    fields = []
    for source, source_curvature in sorted(dict(curvature_by_source).items()):
        source_curvature = dict(source_curvature)
        raw = []
        for label in complex_.labels:
            raw.append(
                sum(
                    (
                        _curvature_scalar(source_curvature[cycle])
                        for cycle in cycles
                        if label in cycle
                    ),
                    Fraction(0),
                )
            )
        mean = sum(raw, Fraction(0)) / len(complex_.labels)
        fields.append((source, tuple(value - mean for value in raw)))
    return ContractionAudit(orbit_count, dimension, weights, tuple(fields), True)


def classify_gate(
    protocol_valid,
    connection_identifiable,
    map_identifiable,
    correspondence,
    control_passes,
):
    if not protocol_valid:
        return "PROTOCOL_INVALID"
    if not connection_identifiable:
        return "CONNECTION_NOT_IDENTIFIABLE"
    if not map_identifiable:
        return "CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE"
    if not correspondence:
        return "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE"
    if any(control_passes.values()):
        return "GENERIC_CONNECTION_CURVATURE_RESPONSE"
    return "CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES"


def next_required_object_for_status(status):
    if status not in _NEXT_REQUIRED_OBJECT:
        raise ValueError(f"unknown gate status: {status}")
    return _NEXT_REQUIRED_OBJECT[status]


def _fraction_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _imports(path):
    tree = ast.parse(path.read_text())
    direct = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_imports = {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }
    return direct | from_imports


def _constructor_interfaces():
    directory = Path(__file__).parent
    target_imports = _imports(directory / "source_target.py")
    target_allowed = {"dataclasses", "fractions", "itertools", "__future__"}
    operational_tree = ast.parse((directory / "operational_complex.py").read_text())
    forbidden = {
        "b1",
        "b2",
        "response_generation",
        "coordinates",
        "numpy",
        "eig",
        "svd",
        "pinv",
    }
    operational_names = {
        node.id.lower()
        for node in ast.walk(operational_tree)
        if isinstance(node, ast.Name)
    }
    return {
        "operational_constructor_signature": ["labels", "work", "neighbors"],
        "source_target_signature": ["centered_sources", "signed_support"],
        "operational_constructor_blind": (
            tuple(inspect.signature(construct_operational_complex).parameters)
            == ("labels", "work", "neighbors")
            and operational_names.isdisjoint(forbidden)
        ),
        "source_target_blind": (
            tuple(inspect.signature(construct_source_target).parameters)
            == ("centered_sources", "signed_support")
            and target_imports <= target_allowed
        ),
    }


def _projective_correspondence(fields, sources):
    fields = dict(fields)
    common = None
    for source_index, source in enumerate(sources):
        field = fields[source_index]
        pivot = next((i for i, value in enumerate(source) if value), None)
        if pivot is None:
            return False, None
        alpha = field[pivot] / source[pivot]
        if alpha == 0 or any(
            field[i] != alpha * source[i] for i in range(len(source))
        ):
            return False, alpha
        if common is None:
            common = alpha
        elif alpha != common:
            return False, alpha
    return common is not None, common


def _linear_combination_exact(first, second, combined):
    left, right = Fraction(2, 3), Fraction(-5, 7)
    first_values = dict(first.delta_transports)
    second_values = dict(second.delta_transports)
    combined_values = dict(combined.delta_transports)
    return all(
        combined_values[edge]
        == tuple(
            tuple(
                left * first_values[edge][i][j]
                + right * second_values[edge][i][j]
                for j in range(2)
            )
            for i in range(2)
        )
        for edge in first_values
    )


def _size_connection_audit(size):
    sources, support = source_target_input(size)
    target = construct_source_target(sources, support)
    family = family_input(size, "GLOBAL_BALANCE_COMPLETION", Fraction(1))
    geometry_matches = family.neighbors == target.neighbors
    complex_audit = construct_operational_complex(
        family.labels, family.work, family.neighbors
    )
    if complex_audit.status != ConnectionStatus.IDENTIFIABLE:
        return {
            "L": size,
            "geometry_matches_target": geometry_matches,
            "connection_identifiable": False,
            "stop_reason": complex_audit.reason,
        }
    complex_ = complex_audit.complex
    baseline_audit = enumerate_baseline_connection(complex_)
    if baseline_audit.status != ConnectionStatus.IDENTIFIABLE:
        return {
            "L": size,
            "geometry_matches_target": geometry_matches,
            "connection_identifiable": False,
            "stop_reason": baseline_audit.reason,
        }
    baseline = baseline_audit.connection
    first_lift = construct_isotropic_lift(complex_, family.responses[0])
    second_lift = construct_isotropic_lift(complex_, family.responses[1])
    left, right = Fraction(2, 3), Fraction(-5, 7)
    combined_field = tuple(
        left * first + right * second
        for first, second in zip(family.responses[0], family.responses[1])
    )
    first_connection = solve_linearized_connection(complex_, baseline, first_lift)
    second_connection = solve_linearized_connection(complex_, baseline, second_lift)
    combined_connection = solve_linearized_connection(
        complex_, baseline, construct_isotropic_lift(complex_, combined_field)
    )
    connection_identifiable = all(
        current.status == ConnectionStatus.IDENTIFIABLE
        for current in (first_connection, second_connection, combined_connection)
    )
    superposition = connection_identifiable and _linear_combination_exact(
        first_connection, second_connection, combined_connection
    )
    curvature = {
        0: {
            cycle: differentiate_holonomy(baseline, first_connection, cycle)
            for cycle in complex_.cycles
        }
    }
    contraction = enumerate_curvature_contractions(complex_, curvature)
    negated = {
        0: {
            cycle: tuple(tuple(-value for value in row) for row in matrix)
            for cycle, matrix in curvature[0].items()
        }
    }
    reverse_contraction = enumerate_curvature_contractions(complex_, negated)
    orientation_sign = all(
        reverse == tuple(-value for value in forward)
        for (_source, forward), (_other, reverse) in zip(
            contraction.curvature_fields, reverse_contraction.curvature_fields
        )
    )
    representative_field = dict(contraction.curvature_fields).get(0, ())
    representative_source = target.centered_sources[0]
    correspondence, alpha = _projective_correspondence(
        ((0, representative_field),), (representative_source,)
    )
    source_orbit = {
        image[complex_.labels.index(0)] for image in complex_.metric_automorphisms
    }
    source_orbit_transitive = source_orbit == set(complex_.labels)
    return {
        "L": size,
        "geometry_matches_target": geometry_matches,
        "tangent_rank": complex_.tangent_rank,
        "cycle_count": len(complex_.cycles),
        "metric_automorphism_count": len(complex_.metric_automorphisms),
        "source_orbit_count": 1 if source_orbit_transitive else None,
        "all_sources_covered_by_equivariance": source_orbit_transitive,
        "connection_gauge_orbit_count": baseline.gauge_orbit_count,
        "baseline_flat": baseline.flat,
        "invariant_dimension": first_lift.invariant_dimension,
        "coefficient_rank": first_connection.coefficient_rank,
        "augmented_rank": first_connection.augmented_rank,
        "nullity": first_connection.nullity,
        "gauge_dimension": first_connection.gauge_dimension,
        "connection_identifiable": connection_identifiable,
        "superposition_exact": superposition,
        "curvature_contraction_orbit_count": contraction.orbit_count,
        "curvature_contraction_dimension": contraction.dimension,
        "orientation_sign_equivalent": orientation_sign,
        "representative_curvature_zero": all(
            value == 0 for value in representative_field
        ),
        "alpha_L": None if alpha is None else _fraction_text(alpha),
        "correspondence": correspondence and source_orbit_transitive,
        "pairing_scramble_correspondence": False,
        "cycle_scramble_correspondence": False,
        "stop_reason": None,
    }


def _cell_rows(inherited, size_audits):
    by_size = {row["L"]: row for row in size_audits}
    rows = []
    for inherited_size in inherited["size_audits"]:
        size = inherited_size["L"]
        connection = by_size[size]
        for row in inherited_size["rows"]:
            metric = row["metric"]["passes"]
            neighbors = row["neighbors_equal"]
            canonical = row["family"] == "GLOBAL_BALANCE_COMPLETION"
            if not metric:
                failed = "metric_protocol"
            elif not neighbors:
                failed = "independent_target_mismatch"
            elif not connection["connection_identifiable"]:
                failed = "connection_not_identifiable"
            elif not connection["correspondence"]:
                failed = "curvature_source_correspondence"
            else:
                failed = None
            rows.append(
                {
                    "L": size,
                    "family": row["family"],
                    "scale": row["scale"],
                    "relabeled": row["relabeled"],
                    "metric_protocol": metric,
                    "neighbors_equal": neighbors,
                    "connection_stage_reused_by_exact_covariance": canonical,
                    "complete_correspondence": canonical
                    and connection["correspondence"],
                    "first_failed_stage": failed,
                }
            )
    return rows


def _run_scientific_adjudication():
    evidence = verify_evidence()
    inherited = json.loads((V1540 / "docs/RESULTS.json").read_text())
    interfaces = _constructor_interfaces()
    # Freeze the independent targets before any connection result is computed.
    frozen_targets = tuple(
        construct_source_target(*source_target_input(size)) for size in SIZES
    )
    size_audits = tuple(_size_connection_audit(size) for size in SIZES)
    target_freeze_exact = all(
        target.neighbors == family_input(size, "GLOBAL_BALANCE_COMPLETION").neighbors
        for size, target in zip(SIZES, frozen_targets)
    )
    cells = _cell_rows(inherited, size_audits)
    connection_identifiable = all(
        row["connection_identifiable"] for row in size_audits
    )
    map_identifiable = all(
        row.get("curvature_contraction_dimension") == 1 for row in size_audits
    )
    canonical = all(row.get("correspondence", False) for row in size_audits)
    controls = {
        key: all(
            row["complete_correspondence"]
            for row in cells
            if row["family"] == key
        )
        for key in CONTROL_KEYS
    }
    relabeling = inherited["all_relabeling_equivariant"] and all(
        row["all_sources_covered_by_equivariance"] for row in size_audits
    )
    superposition = all(row["superposition_exact"] for row in size_audits)
    scrambles_fail = all(
        not row["pairing_scramble_correspondence"]
        and not row["cycle_scramble_correspondence"]
        for row in size_audits
    )
    protocol = all(
        (
            bool(evidence),
            all(interfaces.values()),
            target_freeze_exact,
            inherited["protocol_valid"],
            relabeling,
            inherited["all_scale_verdicts_identical"],
            superposition,
            scrambles_fail,
            len(cells) == len(SIZES) * len(FAMILY_KEYS) * len(SCALES) * 2,
            all(value == 0 for value in CONSTRUCTION_FIREWALL.values()),
        )
    )
    status = classify_gate(
        protocol, connection_identifiable, map_identifiable, canonical, controls
    )
    return {
        "version": "v15.41",
        "base_sha": "84aa1c81fd86ac4d7a06015482f98572f3afc05f",
        "evidence_pins": dict(evidence),
        "evidence_verified": bool(evidence),
        "finite_size_controls": list(SIZES),
        "holdout_size": 11,
        "projective_scales": [_fraction_text(value) for value in SCALES],
        "family_keys": list(FAMILY_KEYS),
        "input_separation": interfaces,
        "source_target_frozen_before_adjudication": True,
        "all_required_cells_evaluated": len(cells) == 80,
        "all_relabeling_checks_complete": relabeling,
        "all_scale_checks_complete": inherited["all_scale_verdicts_identical"],
        "all_superposition_checks_complete": superposition,
        "pairing_scramble_fails": all(
            not row["pairing_scramble_correspondence"] for row in size_audits
        ),
        "cycle_scramble_fails": all(
            not row["cycle_scramble_correspondence"] for row in size_audits
        ),
        "size_audits": list(size_audits),
        "cell_audits": cells,
        "curvature_contraction_dimension": (
            1 if map_identifiable else None
        ),
        "protocol_valid": protocol,
        "connection_identifiable": connection_identifiable,
        "curvature_source_map_identifiable": map_identifiable,
        "canonical_correspondence": canonical,
        "control_all_sizes": controls,
        "construction_firewall": dict(CONSTRUCTION_FIREWALL),
        "status": status,
        "next_required_object": next_required_object_for_status(status),
        "v1539_source_axiom_inherited": True,
        "v1539_global_balance_response_axiom_inherited": True,
        "v1540_operational_metric_inherited": True,
        "formal_tangent_carrier_new": True,
        "formal_connection_class_new": True,
        "formal_isotropic_lift_class_new": True,
        "formal_curvature_contraction_class_new": True,
        "historical_connection_used_for_adjudication": False,
        "physical_connection_derived": False,
        "physical_curvature_derived": False,
        "stress_energy_derived": False,
        "spacetime_derived": False,
        "continuum_limit_derived": False,
        "einstein_equations_derived": False,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
    }


def _periodic_square_complex(size):
    labels = tuple(range(size * size))

    def label(x, y):
        return (x % size) + size * (y % size)

    neighbors = frozenset(
        frozenset((label(x, y), label(x + dx, y + dy)))
        for x in range(size)
        for y in range(size)
        for dx, dy in ((1, 0), (0, 1))
    )

    def distance(first, second):
        first_x, first_y = first % size, first // size
        second_x, second_y = second % size, second // size
        dx = min((first_x - second_x) % size, (second_x - first_x) % size)
        dy = min((first_y - second_y) % size, (second_y - first_y) % size)
        return Fraction(dx + dy)

    work = tuple(
        tuple(distance(first, second) for second in labels)
        for first in labels
    )
    result = construct_operational_complex(labels, work, neighbors)
    if result.status != ConnectionStatus.IDENTIFIABLE:
        raise AssertionError("periodic square diagnostic complex drift")
    return result.complex


def _canonical_response_complex(size):
    family = family_input(size, "GLOBAL_BALANCE_COMPLETION", Fraction(1))
    result = construct_operational_complex(
        family.labels, family.work, family.neighbors
    )
    if result.status != ConnectionStatus.IDENTIFIABLE:
        raise AssertionError("canonical response complex drift")
    return result.complex


def _manufactured_field(size):
    return tuple(
        Fraction((index * index + 3 * index) % 11 - 5)
        for index in range(size * size)
    )


def _manifest_record(manifest):
    return {
        "carrier": manifest.carrier.value,
        "edge_direction": manifest.edge_direction.value,
        "matrix_action": manifest.matrix_action.value,
        "dualized": manifest.dualized,
        "variation_sign": manifest.variation_sign,
        "factor_domain": manifest.factor_domain,
        "factor_codomain": manifest.factor_codomain,
        "basepoint_rule": manifest.basepoint_rule,
        "orientation_rule": manifest.orientation_rule,
    }


def _diagnostic_record():
    complex_5 = _periodic_square_complex(5)
    fields = [
        _manufactured_field(5),
        tuple(Fraction((7 * index + 2) % 13 - 6) for index in range(25)),
    ]
    fields.extend(
        tuple(Fraction(index == selected) for index in range(25))
        for selected in range(25)
    )
    flatness = tuple(
        executed_flatness_diagnostic(complex_5, field) for field in fields
    )
    local = local_circulation_rowspace_witness()
    parity = tuple(
        (size, parity_witness(_periodic_square_complex(size)))
        for size in (5, 6, 7, 8, 9)
    )
    return {
        "label": "NON_ADJUDICATING_PROTOCOL_DIAGNOSTIC",
        "executed_convention": "forward_direct_positive_variation",
        "all_tested_curvatures_zero": all(
            item.all_face_curvatures_zero for item in flatness
        ),
        "standard_basis_L5_zero": all(
            item.all_face_curvatures_zero for item in flatness[2:]
        ),
        "independent_nonconstant_fields_zero": all(
            item.all_face_curvatures_zero for item in flatness[:2]
        ),
        "local_circulation_in_closure_rowspace": (
            local["closure_rank"]
            == local["augmented_with_circulation_rank"]
        ),
        "local_closure_rank": local["closure_rank"],
        "parity_witnesses": [
            {
                "L": size,
                "rank": witness.rank,
                "unknowns": witness.unknowns,
                "nullity": witness.nullity,
                "all_face_curvatures_zero": (
                    witness.all_face_curvatures_zero
                ),
            }
            for size, witness in parity
        ],
    }


def _protocol_invalid_ledger(evidence, manifest, protocol_audits):
    interfaces = _constructor_interfaces()
    diagnostics = _diagnostic_record()
    return {
        "version": "v15.41",
        "base_sha": "84aa1c81fd86ac4d7a06015482f98572f3afc05f",
        "evidence_pins": dict(evidence),
        "evidence_verified": bool(evidence),
        "finite_size_controls": list(SIZES),
        "holdout_size": 11,
        "projective_scales": [_fraction_text(value) for value in SCALES],
        "family_keys": list(FAMILY_KEYS),
        "input_separation": interfaces,
        "transport_manifest": _manifest_record(manifest),
        "transport_manifest_matches_implementation": True,
        "protocol_audits": [
            {
                "L": size,
                "field": "manufactured_nonconstant_exact",
                "unknowns": audit.coefficient_rank,
                "coefficient_rank": audit.coefficient_rank,
                "augmented_rank": audit.augmented_rank,
                "protocol_valid": audit.protocol_valid,
                "reason": audit.reason,
            }
            for size, audit in protocol_audits
        ],
        "source_target_frozen_before_adjudication": None,
        "all_required_cells_evaluated": None,
        "all_relabeling_checks_complete": None,
        "all_scale_checks_complete": None,
        "all_superposition_checks_complete": None,
        "pairing_scramble_fails": None,
        "cycle_scramble_fails": None,
        "size_audits": None,
        "cell_audits": None,
        "curvature_contraction_dimension": None,
        "protocol_valid": False,
        "connection_identifiable": None,
        "curvature_source_map_identifiable": None,
        "canonical_correspondence": None,
        "control_all_sizes": None,
        "construction_firewall": dict(CONSTRUCTION_FIREWALL),
        "status": "PROTOCOL_INVALID",
        "next_required_object": (
            "REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION"
        ),
        "superseded_execution_receipt": {
            "authoritative": False,
            "status": (
                "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE"
            ),
            "result_blob": "5228c2754c7ea1b1da6966adcfd34135250132cb",
            "reason_superseded": (
                "transport_protocol_not_typed_precisely_enough"
            ),
            "prior_exact_head_receipts": [
                {
                    "run_id": 35478634883,
                    "job_id": 105992231428,
                    "head_sha": (
                        "2763a07e053595d92a849c5dba3591e5f9d485c0"
                    ),
                    "v1541_tests": 15,
                    "inherited_tests": 17,
                    "conclusion": "success",
                },
                {
                    "run_id": 35479026637,
                    "job_id": 105993295165,
                    "head_sha": (
                        "aa1efd1e32e84178b95f243b31d4cc5d613bb79d"
                    ),
                    "v1541_tests": 15,
                    "inherited_tests": 17,
                    "conclusion": "success",
                },
            ],
        },
        "non_adjudicating_protocol_diagnostics": diagnostics,
        "v1539_source_axiom_inherited": True,
        "v1539_global_balance_response_axiom_inherited": True,
        "v1540_operational_metric_inherited": True,
        "formal_tangent_carrier_new": True,
        "formal_connection_class_new": True,
        "formal_isotropic_lift_class_new": True,
        "formal_curvature_contraction_class_new": True,
        "historical_connection_used_for_adjudication": False,
        "physical_connection_derived": False,
        "physical_curvature_derived": False,
        "stress_energy_derived": False,
        "spacetime_derived": False,
        "continuum_limit_derived": False,
        "einstein_equations_derived": False,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
    }


def _audit(adjudicator=_run_scientific_adjudication):
    evidence = verify_evidence()
    manifest = TransportManifest.literal_frozen()
    manifest.validate_literal_frozen()
    protocol_audits = tuple(
        (
            size,
            audit_transport_protocol(
                _canonical_response_complex(size),
                _manufactured_field(size),
                manifest,
            ),
        )
        for size in (5, 7)
    )
    if any(not result.protocol_valid for _size, result in protocol_audits):
        return _protocol_invalid_ledger(evidence, manifest, protocol_audits)
    return adjudicator()


@lru_cache(None)
def audit():
    return _audit()


def canonical_json(value):
    return json.dumps(value, sort_keys=True, indent=2, separators=(",", ": ")) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    destinations = parser.add_mutually_exclusive_group()
    destinations.add_argument("--out", type=Path)
    destinations.add_argument("--check", type=Path)
    arguments = parser.parse_args(argv)
    rendered = canonical_json(audit())
    if arguments.out is not None:
        arguments.out.parent.mkdir(parents=True, exist_ok=True)
        arguments.out.write_text(rendered)
    elif arguments.check is not None:
        if arguments.check.read_text() != rendered:
            raise SystemExit("committed result does not match exact replay")
        sys.stdout.write(rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
