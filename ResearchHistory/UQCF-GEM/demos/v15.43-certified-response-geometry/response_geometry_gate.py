"""Ordered coordinator for the certified response geometry application."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from evidence import verify_evidence
from firewall import verify_firewall
from projection import FAMILY_KEYS, canonical_bytes, decode_projection


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT_DIR = HERE.parent / "v15.42-duality-covariant-transport-repair"
STAGES = ("evidence", "parent_replay", "acquisition_projection", "carriers",
          "actual_carrier_controls", "response_cases", "ledger")
VALID_STATUSES = frozenset(("CANONICAL_RESPONSE_CURVATURE_NULL",
                            "CANONICAL_RESPONSE_CURVATURE_NONZERO",
                            "CANONICAL_RESPONSE_CURVATURE_MIXED"))


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
    order = tuple((L, family, scale, index) for L in (5, 7)
                  for scale in (Fraction(1), Fraction(7, 3))
                  for family in FAMILY_KEYS for index in range(L * L))
    if actual != order:
        raise ValueError("invalid_case_order")
    primary = [case for case in cases if case["family"] == FAMILY_KEYS[0]]
    if len(primary) != 148:
        raise ValueError("canonical_coverage")
    return primary


def classify(cases, coverage_complete):
    if not coverage_complete:
        return "RESPONSE_APPLICATION_INVALID", "REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT"
    try:
        primary = _coverage(cases)
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
    message = str(error).splitlines()[0]
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
                _coverage(value["cases"])
            else:
                value = executors.ledger(result)
            values[stage] = value
            result["gate_receipts"][stage] = {"passed": True}
        except Exception as error:
            result["first_failed_gate"] = stage
            result["failure"] = _sanitize(error)
            result["gate_receipts"][stage] = {"passed": False}
            return result
    payload = values["response_cases"]
    cases = payload["cases"]
    result["cases"] = cases
    result["carrier_receipts"] = payload.get("carrier_receipts", values["carriers"])
    result["control_receipts"] = payload.get("control_receipts", values["actual_carrier_controls"])
    result["completed_counts"] = {"cases": len(cases),
                                  "faces": sum(case["face_count"] for case in cases)}
    families = {}
    for family in FAMILY_KEYS:
        selected = [case for case in cases if case["family"] == family]
        flat = sum(case["nonzero_count"] == 0 for case in selected)
        families[family] = {"cases": len(selected), "flat": flat,
                            "nonflat": len(selected) - flat}
    result["family_classifications"] = families
    result["status"], result["next_required_object"] = classify(cases, True)
    evidence = values["evidence"]
    acquired = values["acquisition_projection"]
    if type(evidence) is dict:
        result["dependency_pins"] = evidence.get("pins")
    if type(acquired) is dict:
        result["input_hashes"] = acquired.get("input_hashes")
    result["manifest"] = {"transport": "v15.42-certified",
                          "families": list(FAMILY_KEYS), "sizes": [5, 7],
                          "scales": ["1", "7/3"]}
    return result


def _run(command, cwd, timeout):
    completed = subprocess.run(command, cwd=cwd, env={"PATH": "/usr/bin:/bin"},
                               capture_output=True, timeout=timeout)
    if completed.returncode:
        raise RuntimeError(f"child_process_exit_{completed.returncode}")
    return completed.stdout


def _evidence():
    receipt = verify_evidence(ROOT)
    paths = tuple(HERE / name for name in ("acquire.py", "evaluate.py", "response_geometry_gate.py",
                                            "projection.py", "carriers.py", "application.py",
                                            "presentation_checks.py", "application_controls.py",
                                            "evidence.py", "firewall.py"))
    firewall = verify_firewall(paths)
    pins = {role: {name: item["blob"] for name, item in items.items()}
            for role, items in receipt.items() if type(items) is dict and role != "external"}
    return {"parent": receipt["parent"], "pins": pins, "external": receipt["external"],
            "firewall": firewall}


def _parent_replay():
    stdout = _run([sys.executable, "-I", "protocol_gate.py", "--check", "docs/RESULTS.json"],
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
    _run([sys.executable, "-I", str(HERE / "acquire.py"), "--out", str(path)], HERE, 900)
    raw = path.read_bytes()
    projection = decode_projection(raw)
    docs = HERE / "docs"
    docs.mkdir(exist_ok=True)
    published = docs / "INPUTS.json"
    published.write_bytes(raw)
    temporary.cleanup()
    return {"path": published, "raw": raw, "projection": projection,
            "input_hashes": list(projection.payload_hashes) + [sha256(raw).hexdigest()]}


def _carriers(acquired):
    return tuple({"L": payload.L, "scale": str(payload.scale), "identified_in_evaluator": True}
                 for payload in acquired["projection"].payloads)


def _controls(acquired, carriers):
    if len(carriers) != 4:
        raise ValueError("carrier_coverage")
    return {"scheduled_in_evaluator": True}


def _cases(acquired, carriers, controls):
    output = acquired["path"].with_name("EVALUATION.json")
    try:
        _run([sys.executable, "-I", str(HERE / "evaluate.py"), "--input",
              str(acquired["path"]), "--out", str(output)], HERE, 7200)
    except RuntimeError:
        if output.exists():
            failure = json.loads(output.read_text()).get("failure", {})
            raise RuntimeError(f"evaluator_failure:{failure.get('error_category', 'unknown')}") from None
        raise
    value = json.loads(output.read_text())
    if type(value) is not dict or set(value) != {"carrier_receipts", "control_receipts", "cases", "origin_receipts"}:
        raise ValueError("malformed_evaluator_output")
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
