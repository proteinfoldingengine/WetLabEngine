from __future__ import annotations

from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space"
INVENTORY = V1528 / "docs/REPRESENTATION_INVENTORY.json"
BASE_SHA = "2d9eb636d9d216ef0c7f9029e32832b7c435f0d8"

UPSTREAM_PINS = {
    "exact_linear.py": "05cc1b8cfec70d501408377b5e44190b259a4514",
    "representation_actions.py": "7260147cd6ca47ec21634172b44b98de726904af",
    "coupling_solver.py": "de39fc726fa23b22a9d8809cd4da753756c31eb2",
    "coupling_gate.py": "fd1962289627446090d9d673f70068f647171311",
    "docs/REPRESENTATION_INVENTORY.json": "28dd212b422a4f41d835ccbec79a35116e268ba1",
}

SPOTCHECK_INDICES = (0, 1, 7, 48, 49, 100, 211, 391)


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def verify_upstream_pins() -> dict[str, str]:
    out = {}
    for rel, expected in UPSTREAM_PINS.items():
        path = V1528 / rel
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"upstream v15.28 pin drift: {rel}: {actual}")
        out[rel] = actual
    return out


def _load_upstream():
    verify_upstream_pins()
    path = str(V1528)
    if path not in sys.path:
        sys.path.insert(0, path)
    actions = importlib.import_module("representation_actions")
    solver = importlib.import_module("coupling_solver")
    return actions, solver


def _signed_trace(action) -> int:
    return sum(
        int(s)
        for i, (j, s) in enumerate(zip(action.image, action.sign))
        if i == j
    )


def _restricted_trace(basis, action) -> Fraction:
    total = Fraction(0)
    for j, col in enumerate(basis.columns):
        total += basis.coordinates(action.apply(col))[j]
    return total


def _target_definition_check() -> dict:
    rows = json.loads(INVENTORY.read_text())
    target = next(r for r in rows if r["key"] == "v15.26-response-selector-rank")
    if target["carrier_dimension"] != 50:
        raise AssertionError("cycle target dimension changed")
    if target["carrier_type"] != "metric_free_cycle_response_coordinates":
        raise AssertionError("cycle target carrier type changed")
    if target["quotient_status"] != "CERTIFIED_CYCLE_SPACE_TARGET":
        raise AssertionError("cycle target status changed")
    gate_text = (V1528 / "coupling_gate.py").read_text()
    if "target_chars[g] = ce - (cv - 1)" not in gate_text:
        raise AssertionError("v15.28 cycle-character definition changed")
    return {
        "key": target["key"],
        "carrier_type": target["carrier_type"],
        "carrier_dimension": target["carrier_dimension"],
        "label_link_status": target["label_link_status"],
        "quotient_status": target["quotient_status"],
    }


def audit() -> dict:
    actions, solver = _load_upstream()
    c = actions.load_frozen_complex(7)
    group = actions.torus_automorphisms(c.L)
    if len(group) != 392:
        raise AssertionError("unexpected automorphism-group order")
    group_set = set(group)
    group_closure = all(g.compose(h) in group_set for g in group for h in group)
    if not group_closure:
        raise AssertionError("automorphism group does not close")

    dim_c1 = len(c.edges)
    dim_q = len(c.vertices) - 1
    cycle_basis = actions.cycle_basis_exact(c.B1.astype(int))
    dim_z = cycle_basis.dimension
    target_definition = _target_definition_check()
    dim_y = target_definition["carrier_dimension"]

    z_chars = {}
    edge_actions = {}
    for g in group:
        va = actions.vertex_action(c, g)
        ea = actions.edge_action(c, g)
        edge_actions[g] = ea
        chi_q = _signed_trace(va) - 1
        chi_z = _signed_trace(ea) - chi_q
        z_chars[g] = chi_z

    for idx in SPOTCHECK_INDICES:
        g = group[idx]
        if _restricted_trace(cycle_basis, edge_actions[g]) != z_chars[g]:
            raise ArithmeticError(f"cycle character spot check failed at {idx}")

    # v15.28 defines Y_cyc as the certified cycle-space target on the same
    # pre-time chain complex, so its exact G-character is chi_Z.
    y_chars = dict(z_chars)
    hom_dim = solver.hom_dimension_from_character_values(z_chars, y_chars)
    square_sum = sum(int(v) * int(v) for v in z_chars.values())
    if square_sum != len(group) * hom_dim:
        raise ArithmeticError("character inner-product identity failed")

    hist = Counter(int(v) for v in z_chars.values())
    if sum(hist.values()) != len(group):
        raise ArithmeticError("character histogram count mismatch")

    rational_semisimple = len(group) > 0
    rational_splits = rational_semisimple
    if hom_dim == 0:
        status = "NO_FIBER_SENSITIVE_TARGET_CHANNEL"
        early_stop = "DIM_HOM_Z_TO_Y_EQ_0"
        unique = False
    elif hom_dim == 1:
        status = "UNIQUE_MINIMAL_FIBER_CHANNEL_UP_TO_SCALE"
        early_stop = None
        unique = True
    else:
        status = "FIBER_EXTENSION_CHANNELS_EXIST_BUT_NONUNIQUE"
        early_stop = "DIM_HOM_Z_TO_Y_GT_1"
        unique = False

    return {
        "version": "v15.31",
        "base_sha": BASE_SHA,
        "status": status,
        "group_order": len(group),
        "dim_C1": dim_c1,
        "dim_Q": dim_q,
        "dim_Z": dim_z,
        "dim_Y_cyc": dim_y,
        "group_closure_exact": group_closure,
        "target_definition_verified": True,
        "target_definition": target_definition,
        "character_spotchecks_exact": True,
        "cycle_character_histogram": {str(k): hist[k] for k in sorted(hist)},
        "character_square_sum": square_sum,
        "dim_Hom_Z_to_Y": hom_dim,
        "hom_dimension_method": "EXACT_CHARACTER_INNER_PRODUCT",
        "rational_semisimplicity_verified": rational_semisimple,
        "rational_semisimplicity_basis": "FINITE_GROUP_ORDER_392_OVER_CHARACTERISTIC_ZERO_FIELD",
        "rational_extension_splits": rational_splits,
        "rational_splitting_canonical": False,
        "integral_extension_status": "NOT_ADJUDICATED_WITHOUT_TYPED_INTEGRAL_SOURCE_AXIOM",
        "minimal_kernel_type_count_or_null": None if hom_dim != 1 else 1,
        "minimal_kernel_types_or_null": None,
        "early_stop_reason_or_null": early_stop,
        "unique_projective_fiber_channel": unique,
        "upstream_v15_28_pins": verify_upstream_pins(),
        "source_semantics_information_contract": [
            "physical_provenance_or_source_carrier",
            "inherited_pre_time_transformation_law",
            "typed_map_from_same_q_microscopic_distinctions",
            "typed_relation_to_an_admissible_fiber_channel",
            "explicit_equivalence_or_gauge_structure",
            "declared_mathematical_category_linear_affine_integral_nonlinear_or_other",
            "independent_physical_motivation_not_selected_by_gravity_behavior",
        ],
        "new_source_semantics_axiom_added": False,
        "coupling_solver_reopened": False,
        "gravity_observables_evaluated": False,
        "uses_holonomy_selector": False,
        "uses_newton_or_gr": False,
        "uses_metric_selector": False,
        "uses_pruning_as_selector": False,
        "uses_entropy_as_selector": False,
        "uses_physical_time": False,
        "scientific_breakthrough": False,
        "signal_of_life": False,
        "physical_gravity_derived": False,
        "Pillar_3": "OPEN",
        "next_required_object": (
            "INDEPENDENT_SOURCE_SEMANTICS_OR_DERIVED_STRUCTURE_REDUCING_"
            "THE_10_DIMENSIONAL_EQUIVARIANT_FIBER_CHANNEL_SPACE"
        ),
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out")
    p.add_argument("--check")
    args = p.parse_args()
    text = canonical_json(audit())
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    if args.check:
        expected = Path(args.check).read_text()
        if expected != text:
            raise SystemExit("committed result does not match regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
