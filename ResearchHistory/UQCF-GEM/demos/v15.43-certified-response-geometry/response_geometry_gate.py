"""Ordered coordinator for the certified response geometry application."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from evidence import verify_evidence
from firewall import verify_firewall
from projection import FAMILY_KEYS, canonical_bytes, decode_projection


ROOT = HERE.parents[3]
PARENT_DIR = HERE.parent / "v15.42-duality-covariant-transport-repair"
STAGES = ("evidence", "parent_replay", "acquisition_projection", "carriers",
          "actual_carrier_controls", "response_cases", "ledger")
VALID_STATUSES = frozenset(("CANONICAL_RESPONSE_CURVATURE_NULL",
                            "CANONICAL_RESPONSE_CURVATURE_NONZERO",
                            "CANONICAL_RESPONSE_CURVATURE_MIXED"))
MODE_STAGE = {"carriers": "carriers", "controls": "actual_carrier_controls",
              "cases": "response_cases"}


class StageFailure(RuntimeError):
    def __init__(self, stage, category, message, case=None, cases=0, faces=0):
        super().__init__(message)
        self.stage, self.category, self.case = stage, category, case
        self.cases, self.faces = cases, faces


@dataclass(frozen=True)
class Executors:
    evidence: object
    parent_replay: object
    acquisition_projection: object
    carriers: object
    actual_carrier_controls: object
    response_cases: object
    ledger: object


def _claims():
    return {"source_correspondence": "NOT_EVALUATED", "physical_metric": False,
            "physical_curvature": False, "stress_energy": False,
            "einstein_equations": False, "continuum_limit": False,
            "spacetime": False, "physical_gravity": False,
            "scientific_breakthrough": False, "Pillar_3": "OPEN",
            "fundamental_time_introduced": False,
            "dark_matter_primitive_introduced": False,
            "inherited_axiom_dependence": True,
            "isotropic_scalar_lift_dependence": True}


def case_key(case):
    if type(case) is not dict:
        raise ValueError("case_object")
    required = {"L", "family", "scale", "response_index"}
    permitted = required | {"key", "carrier_family", "face_count", "zero_count",
                            "nonzero_count", "histogram", "invariant_sum", "faces",
                            "presentation_receipt"}
    if not required <= set(case) or set(case) - permitted:
        raise ValueError("case_fields")
    L, family, index = case["L"], case["family"], case["response_index"]
    if type(L) is not int or type(index) is not int or type(family) is not str:
        raise ValueError("case_key_type")
    if type(case["scale"]) is not str:
        raise ValueError("case_fraction_type")
    try:
        scale = Fraction(case["scale"])
    except (ValueError, ZeroDivisionError):
        raise ValueError("case_fraction") from None
    if str(scale) != case["scale"]:
        raise ValueError("case_fraction_noncanonical")
    return L, family, scale, index


def _coverage(cases):
    if type(cases) not in (tuple, list) or len(cases) != 740:
        raise ValueError("incomplete_or_duplicate_case_coverage")
    expected = {(L, family, scale, index) for L in (5, 7)
                for scale in (Fraction(1), Fraction(7, 3))
                for family in FAMILY_KEYS for index in range(L * L)}
    actual = tuple(case_key(case) for case in cases)
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError("incomplete_or_duplicate_case_coverage")
    order = _ordered_keys()
    if actual != order:
        raise ValueError("invalid_case_order")
    primary = [case for case in cases if case["family"] == FAMILY_KEYS[0]]
    if len(primary) != 148:
        raise ValueError("canonical_coverage")
    return primary


def _fraction(value, name):
    if type(value) is not str:
        raise ValueError(f"{name}_fraction_type")
    try:
        parsed = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"{name}_fraction") from None
    if str(parsed) != value:
        raise ValueError(f"{name}_fraction_noncanonical")
    return parsed


def _expected_cycles(L):
    def canonical(vertices):
        vertices = tuple(vertices)
        reversed_vertices = tuple(reversed(vertices))
        return min(tuple(vertices[i:] + vertices[:i] for i in range(4)) +
                   tuple(reversed_vertices[i:] + reversed_vertices[:i] for i in range(4)))
    return tuple(sorted(canonical((x + L * y, (x + 1) % L + L * y,
                                    (x + 1) % L + L * ((y + 1) % L),
                                    x + L * ((y + 1) % L)))
                        for y in range(L) for x in range(L)))


def _ordered_keys():
    return tuple((L, family, scale, index) for L in (5, 7)
                 for scale in (Fraction(1), Fraction(7, 3))
                 for family in FAMILY_KEYS for index in range(L * L))


def _strict_int(value, minimum=0):
    return type(value) is int and value >= minimum


def _validate_case(case):
    expected = {"key", "L", "family", "scale", "response_index", "carrier_family",
                "face_count", "zero_count", "nonzero_count", "histogram",
                "invariant_sum", "faces", "presentation_receipt"}
    if type(case) is not dict or set(case) != expected:
        raise ValueError("case_schema")
    key = case_key(case)
    if (type(case["key"]) is not list or case["key"] != [key[0], key[1], str(key[2]), key[3]] or
            tuple(type(value) for value in case["key"]) != (int, str, str, int)):
        raise ValueError("case_key_mismatch")
    if case["carrier_family"] != FAMILY_KEYS[0]:
        raise ValueError("carrier_family")
    counts = (case["face_count"], case["zero_count"], case["nonzero_count"])
    if any(type(value) is not int or value < 0 for value in counts):
        raise ValueError("case_count")
    if counts[0] != key[0] * key[0] or counts[1] + counts[2] != counts[0]:
        raise ValueError("case_count_consistency")
    faces = case["faces"]
    if type(faces) is not list or len(faces) != counts[0]:
        raise ValueError("face_coverage")
    observed_cycles, invariants, nonzero = set(), [], 0
    L = key[0]
    expected_faces = _expected_cycles(L)
    zero_matrix = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    for face in faces:
        if type(face) is not dict or set(face) != {"cycle", "matrix", "invariant", "nonzero"}:
            raise ValueError("face_schema")
        cycle = face["cycle"]
        if (type(cycle) is not list or len(cycle) != 4 or
                any(type(label) is not int or not 0 <= label < key[0] * key[0] for label in cycle)):
            raise ValueError("face_cycle")
        frozen_cycle = tuple(cycle)
        if len(set(frozen_cycle)) != 4 or frozen_cycle in observed_cycles:
            raise ValueError("duplicate_face")
        observed_cycles.add(frozen_cycle)
        matrix = face["matrix"]
        if (type(matrix) is not list or len(matrix) != 2 or
                any(type(row) is not list or len(row) != 2 for row in matrix)):
            raise ValueError("face_matrix")
        parsed_matrix = tuple(tuple(_fraction(value, "matrix") for value in row) for row in matrix)
        invariant = _fraction(face["invariant"], "invariant")
        a, b = parsed_matrix[0]
        c, d = parsed_matrix[1]
        derived = -(a * a + 2 * b * c + d * d) / 2
        if (invariant < 0 or invariant != derived or type(face["nonzero"]) is not bool or
                face["nonzero"] != (parsed_matrix != zero_matrix)):
            raise ValueError("face_value")
        invariants.append(invariant)
        nonzero += int(face["nonzero"])
    if tuple(tuple(face["cycle"]) for face in faces) != expected_faces:
        raise ValueError("face_coverage")
    if nonzero != counts[2]:
        raise ValueError("nonzero_count")
    histogram = case["histogram"]
    if type(histogram) is not list or any(type(item) is not list or len(item) != 2 for item in histogram):
        raise ValueError("histogram_schema")
    parsed_histogram = tuple((_fraction(item[0], "histogram"), item[1]) for item in histogram)
    if any(type(count) is not int or count < 1 for _, count in parsed_histogram):
        raise ValueError("histogram_count")
    actual_histogram = tuple(sorted((value, invariants.count(value)) for value in set(invariants)))
    if parsed_histogram != actual_histogram or _fraction(case["invariant_sum"], "sum") != sum(invariants, Fraction(0)):
        raise ValueError("summary_mismatch")
    receipt = case["presentation_receipt"]
    _exact_tree(receipt)
    receipt_keys = {"L", "scale", "faces", "oriented_faces", "gauge_presentations", "gauge_keys",
                    "gradient_checks", "edge_checks", "gauge_face_checks", "relabelings",
                    "relabel_cycle_rotations", "relabel_cycle_reversals", "transformation_names",
                    "all_exact", "oriented_face_scope", "executed_oriented_face_checks",
                    "executed_oriented_face_scope"}
    gauge_count = 8 * counts[0] + 1
    if (type(receipt) is not dict or receipt.get("all_exact") is not True or
            set(receipt) != receipt_keys or receipt.get("L") != key[0] or receipt.get("scale") != str(key[2]) or
            receipt.get("faces") != counts[0] or receipt.get("oriented_faces") != 8 * counts[0] or
            receipt.get("gauge_presentations") != gauge_count or
            type(receipt.get("gauge_keys")) is not list or len(receipt["gauge_keys"]) != gauge_count or
            receipt.get("gradient_checks") != gauge_count * counts[0] or
            receipt.get("edge_checks") != gauge_count * 4 * counts[0] or
            receipt.get("gauge_face_checks") != gauge_count * counts[0] or
            receipt.get("relabelings") != 2 or
            type(receipt.get("relabel_cycle_rotations")) is not int or receipt["relabel_cycle_rotations"] < 0 or
            type(receipt.get("relabel_cycle_reversals")) is not int or receipt["relabel_cycle_reversals"] < 0 or
            receipt.get("transformation_names") != ["four_basepoints", "both_orientations", "duality",
                "independent_four_terms", "single_site_D4", "fixed_mixed_D4", "label_component_permutation"] or
            receipt.get("executed_oriented_face_checks") != 16 * counts[0] or
            receipt.get("oriented_face_scope") != "distinct_four_basepoints_times_two_orientations" or
            receipt.get("executed_oriented_face_scope") != "identity_plus_fixed_mixed_presentations"):
        raise ValueError("presentation_receipt")
    numeric = ("L", "faces", "oriented_faces", "gauge_presentations", "gradient_checks", "edge_checks",
               "gauge_face_checks", "relabelings", "relabel_cycle_rotations", "relabel_cycle_reversals",
               "executed_oriented_face_checks")
    if any(not _strict_int(receipt[name]) for name in numeric) or type(receipt["scale"]) is not str:
        raise ValueError("presentation_receipt_type")
    expected_gauges = [["site", label, action] for label in range(counts[0]) for action in range(8)] + [["mixed"]]
    if (receipt["gauge_keys"] != expected_gauges or
            any(type(value) is not int for item in receipt["gauge_keys"][:-1] for value in item[1:])):
        raise ValueError("presentation_gauge_coverage")


def _validate_cases(cases):
    primary = _coverage(cases)
    for case in cases:
        _validate_case(case)
    return primary


def _exact_tree(value):
    if value is None or type(value) in (str, int, bool):
        return
    if type(value) is list:
        for item in value:
            _exact_tree(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            _exact_tree(item)
        return
    raise ValueError("nonexact_child_value")


def _validate_origins(receipt, process):
    acquisition = {"pretime_gravity_canary.py", "exact_linear.py", "representation_actions.py",
                   "response_generation.py", "response_geometry.py", "acquire.py", "evidence.py",
                   "projection.py"}
    evaluator = {"exact_algebra", "operational_complex", "protocol_types", "transport", "holonomy",
                 "evaluate.py", "evidence.py", "projection.py", "carriers.py", "application.py",
                 "presentation_checks.py", "application_controls.py"}
    expected = acquisition if process == "acquisition" else evaluator
    if type(receipt) is not dict or set(receipt) != expected:
        raise ValueError(f"{process}_origin_coverage")
    for item in receipt.values():
        if (type(item) is not dict or set(item) != {"blob"} or type(item["blob"]) is not str or
                len(item["blob"]) != 40 or any(char not in "0123456789abcdef" for char in item["blob"])):
            raise ValueError(f"{process}_origin_receipt")


def _validate_carrier_control(receipt, L, scale):
    keys = {"L", "scale", "constants", "constant_keys", "impulses", "impulse_keys",
            "impulse_histogram", "basis_core_comparisons", "identity_core_comparisons",
            "algebraically_certified_gauge_comparisons", "local_linear_certificate",
            "edge_checks", "face_checks", "all_exact"}
    if type(receipt) is not dict or set(receipt) != keys:
        raise ValueError("control_receipt_schema")
    _exact_tree(receipt)
    n = L * L
    if (type(receipt["L"]) is not int or type(receipt["scale"]) is not str or
            type(receipt["constants"]) is not int or receipt["L"] != L or receipt["scale"] != scale or receipt["constants"] != 2 or
            receipt["constant_keys"] != ["0", "7/3"] or receipt["impulses"] != n or
            receipt["impulse_keys"] != list(range(n)) or receipt["identity_core_comparisons"] != n + 2 or
            receipt["all_exact"] is not True):
        raise ValueError("control_receipt_coverage")
    if (type(receipt["impulses"]) is not int or type(receipt["identity_core_comparisons"]) is not int or
            any(type(value) is not int for value in receipt["impulse_keys"])):
        raise ValueError("control_receipt_type")
    histogram = [["0", n - 12], ["1/64", 8], ["1/16", 4]]
    if receipt["impulse_histogram"] != histogram:
        raise ValueError("control_histogram")
    certificate = receipt["local_linear_certificate"]
    cert_keys = {"edge_types", "endpoint_frame_pairs", "linear_basis_dimension",
                 "local_basis_comparisons", "gradient_basis_comparisons", "all_exact"}
    if (type(certificate) is not dict or set(certificate) != cert_keys or
            certificate["endpoint_frame_pairs"] != 64 or certificate["linear_basis_dimension"] != 5 or
            certificate["all_exact"] is not True):
        raise ValueError("control_certificate")
    identity = [["1", "0"], ["0", "1"]]
    directions = [["-1", "0"], ["0", "-1"], ["0", "1"], ["1", "0"]]
    if (certificate["edge_types"] != [[identity, direction] for direction in directions] or
            any(type(certificate[name]) is not int for name in ("endpoint_frame_pairs", "linear_basis_dimension",
                "local_basis_comparisons", "gradient_basis_comparisons")) or
            certificate["local_basis_comparisons"] != 4 * 64 * 5 or
            certificate["gradient_basis_comparisons"] != 8 * 4):
        raise ValueError("control_certificate_coverage")
    for name in ("basis_core_comparisons", "algebraically_certified_gauge_comparisons",
                 "edge_checks", "face_checks"):
        if type(receipt[name]) is not int or receipt[name] <= 0:
            raise ValueError("control_count")
    gauge_count = 8 * n + 1
    certified = (n + 2) * gauge_count
    if (receipt["basis_core_comparisons"] != 9 * n + 2 or
            receipt["algebraically_certified_gauge_comparisons"] != certified or
            receipt["edge_checks"] != certified * 4 * n or receipt["face_checks"] != certified * n):
        raise ValueError("control_count_relationship")


def _validate_response_control(receipt, L):
    keys = {"L", "scale_pairs", "scale_keys", "shift_cases", "shift_keys", "superpositions",
            "superposition_keys", "transformation_names", "all_exact"}
    if type(receipt) is not dict or set(receipt) != keys:
        raise ValueError("response_control_schema")
    _exact_tree(receipt)
    n = L * L
    expected_scale = [[L, family, index] for family in FAMILY_KEYS for index in range(n)]
    expected_shift = [[L, family, scale, index] for family in FAMILY_KEYS for index in range(n)
                      for scale in ("1", "7/3")]
    expected_superposition = [[L, family, scale, 0, 1]
                              for scale in ("1", "7/3") for family in FAMILY_KEYS]
    if (receipt["L"] != L or receipt["scale_pairs"] != 5 * n or len(receipt["scale_keys"]) != 5 * n or
            receipt["shift_cases"] != 10 * n or len(receipt["shift_keys"]) != 10 * n or
            receipt["superpositions"] != 10 or len(receipt["superposition_keys"]) != 10 or
            receipt["transformation_names"] != ["scale_7/3", "shift_7/3", "superposition_2/3_-5/7"] or
            receipt["all_exact"] is not True):
        raise ValueError("response_control_coverage")
    if (any(type(receipt[name]) is not int for name in ("L", "scale_pairs", "shift_cases", "superpositions")) or
            type(receipt["scale_keys"]) is not list or type(receipt["shift_keys"]) is not list or
            type(receipt["superposition_keys"]) is not list or receipt["scale_keys"] != expected_scale or
            receipt["shift_keys"] != expected_shift or receipt["superposition_keys"] != expected_superposition):
        raise ValueError("response_control_key_coverage")
    for entries, types in ((receipt["scale_keys"], (int, str, int)),
                           (receipt["shift_keys"], (int, str, str, int)),
                           (receipt["superposition_keys"], (int, str, str, int, int))):
        if any(type(item) is not list or len(item) != len(types) or
               any(type(value) is not expected_type for value, expected_type in zip(item, types))
               for item in entries):
            raise ValueError("response_control_key_type")


def classify(cases, coverage_complete):
    if not coverage_complete:
        return "RESPONSE_APPLICATION_INVALID", "REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT"
    try:
        primary = _validate_cases(cases)
    except ValueError:
        return "RESPONSE_APPLICATION_INVALID", "REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT"
    nonflat = sum(case.get("nonzero_count", 0) > 0 for case in primary)
    if nonflat == 0:
        return "CANONICAL_RESPONSE_CURVATURE_NULL", "CHARACTERIZE_CERTIFIED_TRANSPORT_KERNEL"
    if nonflat == 148:
        return ("CANONICAL_RESPONSE_CURVATURE_NONZERO",
                "PREREGISTER_INTRINSIC_CURVATURE_INTERPRETATION_WITHOUT_SOURCE_FITTING")
    return "CANONICAL_RESPONSE_CURVATURE_MIXED", "CHARACTERIZE_FINITE_SIZE_OR_RESPONSE_DEPENDENCE"


def _base():
    return {"version": "v15.43", "parent": "0f426fa28d22871ce042e39bf9704695ede8b336",
            "spec_blob": "680f691538b99037b89d52b6c93742495d039d4e",
            "dependency_pins": None, "input_hashes": None, "manifest": None,
            "gate_receipts": {}, "carrier_receipts": None, "control_receipts": None,
            "cases": None, "family_classifications": None,
            "status": "RESPONSE_APPLICATION_INVALID",
            "next_required_object": "REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT",
            "first_failed_gate": None, "failure": None,
            "completed_counts": {"cases": 0, "faces": 0}, "claims": _claims()}


def _sanitize(error):
    lines = str(error).splitlines()
    message = lines[0] if lines else type(error).__name__
    if "/" in message or "\\" in message:
        message = "stage execution failed"
    return {"category": type(error).__name__, "message": message[:240]}


def _audit(executors):
    if type(executors) is not Executors:
        raise TypeError("Executors required")
    result = _base()
    values = {}
    callbacks = {"evidence": executors.evidence, "parent_replay": executors.parent_replay,
                 "acquisition_projection": executors.acquisition_projection}
    for stage in STAGES:
        try:
            if stage in ("evidence", "parent_replay", "acquisition_projection"):
                value = callbacks[stage]()
            elif stage == "carriers":
                value = executors.carriers(values["acquisition_projection"])
            elif stage == "actual_carrier_controls":
                value = executors.actual_carrier_controls(values["acquisition_projection"], values["carriers"])
            elif stage == "response_cases":
                value = executors.response_cases(values["acquisition_projection"], values["carriers"],
                                                 values["actual_carrier_controls"])
                if type(value) is not dict or "cases" not in value:
                    raise ValueError("malformed_evaluator_output")
                _validate_cases(value["cases"])
            else:
                draft = dict(result)
                payload = values["response_cases"]
                cases = payload["cases"]
                draft["cases"] = cases
                draft["carrier_receipts"] = values["carriers"]
                draft["control_receipts"] = list(values["actual_carrier_controls"]) + list(payload.get("response_control_receipts", ()))
                draft["completed_counts"] = {"cases": len(cases), "faces": sum(case["face_count"] for case in cases)}
                result["completed_counts"] = dict(draft["completed_counts"])
                families = {}
                for family in FAMILY_KEYS:
                    selected = [case for case in cases if case["family"] == family]
                    flat = sum(case["nonzero_count"] == 0 for case in selected)
                    families[family] = {"cases": len(selected), "flat": flat, "nonflat": len(selected) - flat}
                draft["family_classifications"] = families
                draft["status"], draft["next_required_object"] = classify(cases, True)
                evidence, acquired = values["evidence"], values["acquisition_projection"]
                draft["dependency_pins"] = evidence.get("pins") if type(evidence) is dict else None
                draft["input_hashes"] = acquired.get("input_hashes") if type(acquired) is dict else None
                draft["manifest"] = {"transport": "v15.42-certified", "families": list(FAMILY_KEYS),
                                     "sizes": [5, 7], "scales": ["1", "7/3"],
                                     "origin_receipts": {"acquisition": acquired.get("origin_receipts"),
                                                         "evaluator": payload.get("origin_receipts")}}
                value = executors.ledger(draft)
                if type(value) is not dict or value.get("status") not in VALID_STATUSES:
                    raise ValueError("invalid_final_ledger")
                result = value
            values[stage] = value
            result["gate_receipts"][stage] = {"passed": True}
        except Exception as error:
            traceback.print_exc(file=sys.stderr)
            failed_stage = error.stage if isinstance(error, StageFailure) else stage
            result["first_failed_gate"] = failed_stage
            result["failure"] = _sanitize(error)
            if isinstance(error, StageFailure):
                result["failure"].update(category=error.category, case=error.case)
                result["completed_counts"] = {"cases": error.cases, "faces": error.faces}
                if failed_stage in result["gate_receipts"]:
                    result["gate_receipts"][failed_stage] = {"passed": False}
            result["gate_receipts"][stage] = {"passed": False}
            return result
    return result


def _run(command, cwd, timeout):
    completed = subprocess.run(command, cwd=cwd, env={"PATH": "/usr/bin:/bin"},
                               capture_output=True, timeout=timeout)
    if completed.returncode:
        if completed.stderr:
            sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError(f"child_process_exit_{completed.returncode}")
    return completed.stdout


def _evidence():
    receipt = verify_evidence(ROOT)
    paths = tuple(HERE / name for name in ("acquire.py", "evaluate.py", "response_geometry_gate.py",
                                            "projection.py", "carriers.py", "application.py",
                                            "presentation_checks.py", "application_controls.py",
                                            "evidence.py", "firewall.py"))
    firewall = verify_firewall(paths)
    pins = {role: {name: item["blob"] for name, item in receipt[role].items()}
            for role in ("evidence", "acquisition", "evaluator", "parent_replay", "regression")}
    pins["spec"] = receipt["spec"]["blob"]
    return {"parent": receipt["parent"], "pins": pins, "external": receipt["external"],
            "firewall": firewall}


def _parent_replay():
    bootstrap = ("import runpy, sys; "
                 "sys.path.insert(0, sys.argv[1]); "
                 "sys.argv = sys.argv[2:]; "
                 "runpy.run_path(sys.argv[0], run_name='__main__')")
    stdout = _run([sys.executable, "-I", "-c", bootstrap, str(PARENT_DIR),
                   str(PARENT_DIR / "protocol_gate.py"), "--check", "docs/RESULTS.json"],
                  PARENT_DIR, 900)
    expected = (PARENT_DIR / "docs/RESULTS.json").read_bytes()
    if stdout != expected:
        raise ValueError("parent_replay_mismatch")
    verdict = json.loads(stdout)
    if verdict.get("status") != "TRANSPORT_PROTOCOL_CERTIFIED":
        raise ValueError("parent_not_certified")
    return {"status": verdict["status"], "ledger_sha256": sha256(stdout).hexdigest()}


def _acquire():
    temporary = tempfile.TemporaryDirectory()
    path = Path(temporary.name) / "INPUTS.json"
    receipt_path = Path(temporary.name) / "ORIGINS.json"
    _run([sys.executable, "-I", str(HERE / "acquire.py"), "--out", str(path),
          "--receipt", str(receipt_path)], HERE, 900)
    raw = path.read_bytes()
    projection = decode_projection(raw)
    origins = _unique_json(receipt_path.read_text())
    _validate_origins(origins, "acquisition")
    docs = HERE / "docs"
    docs.mkdir(exist_ok=True)
    published = docs / "INPUTS.json"
    published.write_bytes(raw)
    temporary.cleanup()
    return {"path": published, "raw": raw, "projection": projection,
            "input_hashes": list(projection.payload_hashes) + [sha256(raw).hexdigest()],
            "origin_receipts": origins}


def _carriers(acquired):
    value = _run_evaluator(acquired, "carriers")
    if set(value) != {"carrier_receipts", "origin_receipts"}:
        raise ValueError("carrier_output_schema")
    _validate_origins(value["origin_receipts"], "evaluator")
    receipts = value.get("carrier_receipts")
    if type(receipts) is not list or len(receipts) != 4:
        raise ValueError("carrier_receipt_coverage")
    expected = ((5, "1"), (5, "7/3"), (7, "1"), (7, "7/3"))
    required = {"L", "scale", "status", "complex_reason", "baseline_status",
                "baseline_reason", "tangent_rank", "gauge_orbit_count", "flat"}
    for receipt, pair in zip(receipts, expected):
        _exact_tree(receipt)
        if (type(receipt) is not dict or set(receipt) != required or
                type(receipt["L"]) is not int or type(receipt["scale"]) is not str or
                type(receipt["status"]) is not str or type(receipt["baseline_status"]) is not str or
                receipt["complex_reason"] is not None and type(receipt["complex_reason"]) is not str or
                receipt["baseline_reason"] is not None and type(receipt["baseline_reason"]) is not str or
                type(receipt["tangent_rank"]) is not int or type(receipt["gauge_orbit_count"]) is not int or
                type(receipt["flat"]) is not bool or
                (receipt["L"], receipt["scale"]) != pair or
                receipt["status"] != "IDENTIFIABLE" or receipt["baseline_status"] != "IDENTIFIABLE" or
                receipt["tangent_rank"] != 2 or receipt["gauge_orbit_count"] != 1 or receipt["flat"] is not True):
            raise ValueError("carrier_receipt")
    return tuple(receipts)


def _controls(acquired, carriers):
    if len(carriers) != 4:
        raise ValueError("carrier_coverage")
    value = _run_evaluator(acquired, "controls")
    if set(value) != {"control_receipts", "origin_receipts"}:
        raise ValueError("control_output_schema")
    _validate_origins(value["origin_receipts"], "evaluator")
    receipts = value.get("control_receipts")
    if (type(receipts) is not list or len(receipts) != 4 or
            any(type(item) is not dict or item.get("all_exact") is not True for item in receipts)):
        raise ValueError("control_receipt_coverage")
    for receipt, (L, scale) in zip(receipts, ((5, "1"), (5, "7/3"), (7, "1"), (7, "7/3"))):
        _validate_carrier_control(receipt, L, scale)
    return tuple(receipts)


def _unique_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate_child_key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def _run_evaluator(acquired, mode):
    output = acquired["path"].with_name(f"EVALUATION-{mode}.json")
    completed = subprocess.run(
        [sys.executable, "-I", str(HERE / "evaluate.py"), "--input", str(acquired["path"]),
         "--out", str(output), "--mode", mode], cwd=HERE, env={"PATH": "/usr/bin:/bin"},
        capture_output=True, timeout=7200)
    if completed.stderr:
        sys.stderr.buffer.write(completed.stderr)
    if not output.exists():
        raise StageFailure(MODE_STAGE[mode], "ChildProcessError", f"evaluator exit {completed.returncode}")
    value = _unique_json(output.read_text())
    if completed.returncode:
        failure = value.get("failure") if type(value) is dict else None
        failure_keys = {"stage", "case", "completed_cases", "completed_faces", "error_category", "message"}
        if type(value) is not dict or set(value) != {"failure"} or type(failure) is not dict or set(failure) != failure_keys:
            raise StageFailure(MODE_STAGE[mode], "ChildProcessError", f"evaluator exit {completed.returncode}")
        stage = failure.get("stage")
        allowed_stages = {"carriers"} if mode == "carriers" else (
            {"carriers", "actual_carrier_controls"} if mode == "controls" else
            {"carriers", "response_cases"})
        category, message = failure.get("error_category"), failure.get("message")
        cases, faces, case = failure.get("completed_cases"), failure.get("completed_faces"), failure.get("case")
        if (stage not in allowed_stages or type(category) is not str or not category or
                type(message) is not str or type(cases) is not int or isinstance(cases, bool) or cases < 0 or
                type(faces) is not int or isinstance(faces, bool) or faces < 0):
            raise StageFailure(MODE_STAGE[mode], "MalformedChildFailure", "invalid evaluator failure receipt")
        ordered = _ordered_keys()
        expected_faces = sum(key[0] * key[0] for key in ordered[:cases])
        expected_case = ([ordered[cases][0], ordered[cases][1], str(ordered[cases][2]), ordered[cases][3]]
                         if stage == "response_cases" and cases < len(ordered) else None)
        case_types = case is None or (type(case) is list and
                                      tuple(type(value) for value in case) == (int, str, str, int))
        if (cases > 740 or faces != expected_faces or case != expected_case or not case_types or
                (stage != "response_cases" and (cases != 0 or faces != 0))):
            raise StageFailure(MODE_STAGE[mode], "MalformedChildFailure", "invalid evaluator progress")
        raise StageFailure(stage, category, message, case, cases, faces)
    if type(value) is not dict or "origin_receipts" not in value or type(value["origin_receipts"]) is not dict:
        raise ValueError("malformed_evaluator_output")
    return value


def _cases(acquired, carriers, controls):
    value = _run_evaluator(acquired, "cases")
    if set(value) != {"cases", "response_control_receipts", "origin_receipts"}:
        raise ValueError("malformed_evaluator_output")
    _validate_origins(value["origin_receipts"], "evaluator")
    _validate_cases(value["cases"])
    receipts = value["response_control_receipts"]
    if (type(receipts) is not list or len(receipts) != 2 or
            any(type(item) is not dict or item.get("all_exact") is not True for item in receipts)):
        raise ValueError("response_control_receipts")
    for receipt, L in zip(receipts, (5, 7)):
        _validate_response_control(receipt, L)
    return value


def _ledger(value):
    return value


def audit():
    executors = Executors(_evidence, _parent_replay, _acquire, _carriers, _controls, _cases, _ledger)
    return _audit(executors)


def render_result(result):
    return canonical_bytes(result)


def main(argv=None):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--out", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args(argv)
    result = audit()
    rendered = render_result(result)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(rendered)
    matches = True
    if args.check:
        try:
            matches = args.check.read_bytes() == rendered
        except OSError:
            matches = False
        if not matches:
            print("canonical ledger mismatch", file=sys.stderr)
    sys.stdout.buffer.write(rendered)
    return 0 if matches and result["status"] in VALID_STATUSES else 1


if __name__ == "__main__":
    raise SystemExit(main())
