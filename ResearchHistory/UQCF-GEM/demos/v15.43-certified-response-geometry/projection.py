from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256


SCHEMA = "uqcf-v1543-inputs-v1"
PARENT = "0f426fa28d22871ce042e39bf9704695ede8b336"
FAMILY_KEYS = (
    "GLOBAL_BALANCE_COMPLETION",
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)
DEPENDENCIES = tuple(sorted((
    ("ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py", "99110f943550751645539c0c8a7339024d7fefd3"),
    ("ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py", "05cc1b8cfec70d501408377b5e44190b259a4514"),
    ("ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py", "7260147cd6ca47ec21634172b44b98de726904af"),
    ("ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_generation.py", "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5"),
    ("ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py", "9128c24b695c1b539ac60dc93aeaf0bd4795c57b"),
)))

CaseKey = tuple[int, str, Fraction, int]


@dataclass(frozen=True)
class Field:
    family: str
    response_index: int
    values: tuple[Fraction, ...]


@dataclass(frozen=True)
class Payload:
    L: int
    scale: Fraction
    labels: tuple[int, ...]
    work: tuple[tuple[Fraction, ...], ...]
    neighbors: tuple[tuple[int, int], ...]
    fields: tuple[Field, ...]


@dataclass(frozen=True)
class Projection:
    parent: str
    dependencies: tuple[tuple[str, str], ...]
    payloads: tuple[Payload, ...]
    payload_hashes: tuple[str, ...]


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, separators=(",", ": ")) + "\n").encode("utf-8")


def _field_wire(field: Field) -> dict:
    return {"family": field.family, "response_index": field.response_index,
            "values": [str(value) for value in field.values]}


def _payload_wire(payload: Payload) -> dict:
    return {"L": payload.L, "scale": str(payload.scale), "labels": list(payload.labels),
            "work": [[str(value) for value in row] for row in payload.work],
            "neighbors": [list(edge) for edge in payload.neighbors],
            "fields": [_field_wire(field) for field in payload.fields]}


def _projection_wire(value: Projection) -> dict:
    return {"schema": SCHEMA, "parent": value.parent,
            "dependencies": [list(item) for item in value.dependencies],
            "payloads": [_payload_wire(payload) for payload in value.payloads],
            "payload_hashes": list(value.payload_hashes)}


def _exact_keys(value, keys):
    if type(value) is not dict:
        raise ValueError("invalid_type: object required")
    if set(value) != set(keys):
        raise ValueError("unknown_field" if set(value) - set(keys) else "missing_field")


def _integer(value):
    if type(value) is not int:
        raise ValueError("invalid_type: integer required")
    return value


def _fraction(value):
    if type(value) is not str:
        raise ValueError("invalid_type: fraction string required")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError("malformed_fraction") from None
    if str(result) != value:
        raise ValueError("noncanonical_fraction")
    return result


def _parse_field(raw, count):
    _exact_keys(raw, ("family", "response_index", "values"))
    if type(raw["family"]) is not str or type(raw["values"]) is not list:
        raise ValueError("invalid_type")
    index = _integer(raw["response_index"])
    values = tuple(_fraction(value) for value in raw["values"])
    if len(values) != count:
        raise ValueError("field_dimension")
    if sum(values, Fraction(0)) != 0:
        raise ValueError("nonzero_field_sum")
    return Field(raw["family"], index, values)


def _parse_payload(raw):
    _exact_keys(raw, ("L", "scale", "labels", "work", "neighbors", "fields"))
    L = _integer(raw["L"])
    scale = _fraction(raw["scale"])
    if type(raw["labels"]) is not list:
        raise ValueError("invalid_type")
    labels = tuple(_integer(label) for label in raw["labels"])
    if len(set(labels)) != len(labels):
        raise ValueError("duplicate_labels")
    count = L * L
    if labels != tuple(range(count)):
        raise ValueError("invalid_label_order")
    if type(raw["work"]) is not list or any(type(row) is not list for row in raw["work"]):
        raise ValueError("invalid_type")
    work = tuple(tuple(_fraction(value) for value in row) for row in raw["work"])
    if len(work) != count or any(len(row) != count for row in work):
        raise ValueError("work_dimension")
    if any(work[i][i] != 0 for i in range(count)):
        raise ValueError("work_diagonal")
    if any(work[i][j] != work[j][i] for i in range(count) for j in range(count)):
        raise ValueError("work_asymmetry")
    if type(raw["neighbors"]) is not list:
        raise ValueError("invalid_type")
    neighbors = tuple(tuple(_integer(endpoint) for endpoint in edge) if type(edge) is list else ()
                      for edge in raw["neighbors"])
    if any(len(edge) != 2 or not 0 <= edge[0] < edge[1] < count for edge in neighbors):
        raise ValueError("invalid_neighbor")
    if neighbors != tuple(sorted(set(neighbors))):
        raise ValueError("neighbor_order")
    if type(raw["fields"]) is not list:
        raise ValueError("invalid_type")
    fields = tuple(_parse_field(field, count) for field in raw["fields"])
    expected = tuple((family, index) for family in FAMILY_KEYS for index in range(count))
    actual = tuple((field.family, field.response_index) for field in fields)
    if actual != expected:
        raise ValueError("wrong_field_order")
    return Payload(L, scale, labels, work, neighbors, fields)


def _validate_projection(value: Projection) -> None:
    if (type(value.dependencies) is not tuple or type(value.payloads) is not tuple or
            type(value.payload_hashes) is not tuple or
            any(type(item) is not tuple for item in value.dependencies)):
        raise ValueError("tuple_backing")
    for payload in value.payloads:
        if (type(payload) is not Payload or type(payload.labels) is not tuple or
                type(payload.work) is not tuple or type(payload.neighbors) is not tuple or
                type(payload.fields) is not tuple or
                any(type(row) is not tuple for row in payload.work) or
                any(type(edge) is not tuple for edge in payload.neighbors) or
                any(type(field) is not Field or type(field.values) is not tuple
                    for field in payload.fields)):
            raise ValueError("tuple_backing")
    if value.parent != PARENT:
        raise ValueError("parent")
    if value.dependencies != DEPENDENCIES:
        raise ValueError("dependency_list")
    for payload in value.payloads:
        if _parse_payload(_payload_wire(payload)) != payload:
            raise ValueError("invalid_payload")
    cases = tuple((payload.L, payload.scale) for payload in value.payloads)
    expected = ((5, Fraction(1)), (5, Fraction(7, 3)), (7, Fraction(1)), (7, Fraction(7, 3)))
    if len(set(cases)) != len(cases):
        raise ValueError("duplicate_case")
    if len(cases) != len(expected) or set(cases) != set(expected):
        raise ValueError("incomplete_cases")
    if cases != expected:
        raise ValueError("wrong_payload_order")
    if len(value.payload_hashes) != 4 or any(type(item) is not str for item in value.payload_hashes):
        raise ValueError("payload_hash")
    actual = tuple(sha256(canonical_bytes(_payload_wire(payload))).hexdigest() for payload in value.payloads)
    if value.payload_hashes != actual:
        raise ValueError("payload_hash")


def encode_projection(value: Projection) -> bytes:
    if type(value) is not Projection:
        raise TypeError("Projection required")
    _validate_projection(value)
    return canonical_bytes(_projection_wire(value))


def decode_projection(raw: bytes) -> Projection:
    if type(raw) is not bytes:
        raise TypeError("bytes required")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate_key")
            result[key] = value
        return result
    try:
        wire = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except UnicodeDecodeError:
        raise ValueError("invalid_encoding") from None
    _exact_keys(wire, ("schema", "parent", "dependencies", "payloads", "payload_hashes"))
    if wire["schema"] != SCHEMA:
        raise ValueError("schema")
    if type(wire["parent"]) is not str or type(wire["dependencies"]) is not list or type(wire["payloads"]) is not list or type(wire["payload_hashes"]) is not list:
        raise ValueError("invalid_type")
    dependencies = tuple(tuple(item) if type(item) is list and len(item) == 2 and all(type(x) is str for x in item) else ()
                         for item in wire["dependencies"])
    if dependencies != DEPENDENCIES:
        raise ValueError("dependency_list")
    payloads = tuple(_parse_payload(payload) for payload in wire["payloads"])
    projection = Projection(wire["parent"], dependencies, payloads, tuple(wire["payload_hashes"]))
    _validate_projection(projection)
    if canonical_bytes(wire) != raw:
        raise ValueError("noncanonical_json")
    return projection
