"""Isolated exact evaluator for a validated v15.43 projection."""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE = HERE.parent / "v15.42-duality-covariant-transport-repair"
for location in (str(HERE), str(CORE)):
    while location in sys.path:
        sys.path.remove(location)
sys.path[:0] = [str(HERE), str(CORE)]

from application import evaluate_field
from application_controls import check_carrier_controls, check_response_controls
from carriers import build_carrier
from evidence import git_blob, verify_origins
from presentation_checks import check_presentations
from projection import FAMILY_KEYS, decode_projection

MODE_STAGE = {"carriers": "carriers", "controls": "actual_carrier_controls",
              "cases": "response_cases"}


def _wire(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _wire(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_wire(item) for item in value]
    if value is None or type(value) in (str, int, bool):
        return value
    raise TypeError(f"unsupported exact value: {type(value).__name__}")


def _case(payload, carrier, field):
    result = evaluate_field(carrier, field.values)
    presentation = check_presentations(carrier, field.values)
    distinct = 8 * len(result.records)
    presentation.update(oriented_faces=distinct,
                        oriented_face_scope="distinct_four_basepoints_times_two_orientations",
                        executed_oriented_face_checks=2 * distinct,
                        executed_oriented_face_scope="identity_plus_fixed_mixed_presentations")
    faces = tuple({"cycle": cycle, "matrix": matrix, "invariant": invariant,
                   "nonzero": matrix != ((Fraction(0), Fraction(0)),
                                         (Fraction(0), Fraction(0)))}
                  for cycle, matrix, invariant in result.records)
    return {"key": (payload.L, field.family, payload.scale, field.response_index),
            "L": payload.L, "family": field.family, "scale": payload.scale,
            "response_index": field.response_index,
            "carrier_family": "GLOBAL_BALANCE_COMPLETION",
            "face_count": len(faces), "zero_count": result.zero_count,
            "nonzero_count": result.nonzero_count, "histogram": result.histogram,
            "invariant_sum": result.invariant_sum, "faces": faces,
            "presentation_receipt": presentation}


def evaluate_projection(projection):
    carriers = tuple(build_carrier(payload) for payload in projection.payloads)
    carrier_receipts = tuple({"L": carrier.L, "scale": carrier.scale,
                              **dict(carrier.receipt)} for carrier in carriers)
    carrier_controls = tuple(check_carrier_controls(carrier) for carrier in carriers)
    cases = tuple(_case(payload, carrier, field)
                  for payload, carrier in zip(projection.payloads, carriers)
                  for field in payload.fields)
    response_controls = tuple(check_response_controls(
        carriers[index], carriers[index + 1], projection.payloads[index].fields,
        projection.payloads[index + 1].fields) for index in (0, 2))
    return _wire({"carrier_receipts": carrier_receipts,
                  "control_receipts": carrier_controls + response_controls,
                  "cases": cases})


class ProgressError(RuntimeError):
    def __init__(self, stage, case, completed_cases, completed_faces, error):
        super().__init__(str(error))
        self.stage, self.case = stage, case
        self.completed_cases, self.completed_faces = completed_cases, completed_faces
        self.error_category = type(error).__name__


def _evaluate_mode(projection, mode):
    try:
        carriers = tuple(build_carrier(payload) for payload in projection.payloads)
    except Exception as error:
        raise ProgressError("carriers", None, 0, 0, error) from error
    carrier_receipts = tuple({"L": carrier.L, "scale": carrier.scale,
                              **dict(carrier.receipt)} for carrier in carriers)
    if mode == "carriers":
        return {"carrier_receipts": carrier_receipts}
    if mode == "controls":
        try:
            carrier_controls = tuple(check_carrier_controls(carrier) for carrier in carriers)
        except Exception as error:
            raise ProgressError("actual_carrier_controls", None, 0, 0, error) from error
        return {"control_receipts": carrier_controls}
    cases = []
    completed_faces = 0
    for payload, carrier in zip(projection.payloads, carriers):
        for field in payload.fields:
            key = (payload.L, field.family, payload.scale, field.response_index)
            try:
                case = _case(payload, carrier, field)
            except Exception as error:
                raise ProgressError("response_cases", key, len(cases), completed_faces, error) from error
            cases.append(case)
            completed_faces += case["face_count"]
    try:
        response_controls = tuple(check_response_controls(
            carriers[index], carriers[index + 1], projection.payloads[index].fields,
            projection.payloads[index + 1].fields) for index in (0, 2))
    except Exception as error:
        raise ProgressError("response_cases", None, len(cases), completed_faces, error) from error
    return {"cases": tuple(cases), "response_control_receipts": response_controls}


def _verify_process_origins():
    import exact_algebra, holonomy, operational_complex, protocol_types, transport
    modules = (exact_algebra, operational_complex, protocol_types, transport, holonomy)
    pins = {
        "exact_algebra": "c67ea42b61321469f7735ce589f2e729b241666a",
        "operational_complex": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
        "protocol_types": "e90a98d17baa6028f0d50a165f0b9d0046de13a2",
        "transport": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
        "holonomy": "bad3f06b291bb448a903b4f48344a9e54a633f68",
    }
    inherited = verify_origins(modules, pins, "evaluator")
    root = HERE.parents[3]
    local = {HERE / name for name in ("evaluate.py", "evidence.py", "projection.py",
             "carriers.py", "application.py", "presentation_checks.py", "application_controls.py")}
    inherited_paths = {CORE / (name + ".py") for name in pins}
    permitted = {path.resolve() for path in local | inherited_paths}
    observed = set()
    for module in tuple(sys.modules.values()):
        origin = module.__file__ if hasattr(module, "__file__") else None
        if type(origin) is not str:
            continue
        path = Path(origin).resolve()
        if path == root or root in path.parents:
            if path not in permitted:
                raise ValueError(f"unexpected evaluator repository module: {path.name}")
            observed.add(path)
    if observed != permitted:
        raise ValueError("incomplete evaluator module closure")
    return {**inherited, **{path.name: {"blob": git_blob(path.read_bytes())}
                             for path in sorted(local)}}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("carriers", "controls", "cases"))
    args = parser.parse_args(argv)
    try:
        projection = decode_projection(args.input.read_bytes())
        origins = _verify_process_origins()
        result = _wire(_evaluate_mode(projection, args.mode))
        result["origin_receipts"] = {name: {"blob": item["blob"]}
                                     for name, item in origins.items()}
        raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
        args.out.write_bytes(raw)
        return 0
    except Exception as error:
        traceback.print_exc(file=sys.stderr)
        message = str(error).splitlines()
        failure = {"stage": error.stage if isinstance(error, ProgressError) else MODE_STAGE[args.mode],
                   "case": _wire(error.case) if isinstance(error, ProgressError) else None,
                   "completed_cases": error.completed_cases if isinstance(error, ProgressError) else 0,
                   "completed_faces": error.completed_faces if isinstance(error, ProgressError) else 0,
                   "error_category": error.error_category if isinstance(error, ProgressError) else type(error).__name__,
                   "message": (message[0] if message else type(error).__name__)[:240]}
        args.out.write_text(json.dumps({"failure": failure}, sort_keys=True, indent=2) + "\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
