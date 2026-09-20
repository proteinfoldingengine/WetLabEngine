"""Isolated exact evaluator for a validated v15.43 projection."""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE = HERE.parent / "v15.42-duality-covariant-transport-repair"
for location in (str(HERE), str(CORE)):
    if location not in sys.path:
        sys.path.insert(0, location)

from application import evaluate_field
from application_controls import check_carrier_controls, check_response_controls
from carriers import build_carrier
from evidence import verify_origins
from presentation_checks import check_presentations
from projection import FAMILY_KEYS, decode_projection


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


def _verify_inherited_origins():
    import exact_algebra, holonomy, operational_complex, protocol_types, transport
    modules = (exact_algebra, operational_complex, protocol_types, transport, holonomy)
    pins = {
        "exact_algebra": "c67ea42b61321469f7735ce589f2e729b241666a",
        "operational_complex": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
        "protocol_types": "e90a98d17baa6028f0d50a165f0b9d0046de13a2",
        "transport": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
        "holonomy": "bad3f06b291bb448a903b4f48344a9e54a633f68",
    }
    return verify_origins(modules, pins)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        projection = decode_projection(args.input.read_bytes())
        origins = _verify_inherited_origins()
        result = evaluate_projection(projection)
        result["origin_receipts"] = {name: {"blob": item["blob"]}
                                     for name, item in origins.items()}
        raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
        args.out.write_bytes(raw)
        return 0
    except Exception as error:
        failure = {"error_category": type(error).__name__,
                   "message": str(error).splitlines()[0][:240]}
        args.out.write_text(json.dumps({"failure": failure}, sort_keys=True, indent=2) + "\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
