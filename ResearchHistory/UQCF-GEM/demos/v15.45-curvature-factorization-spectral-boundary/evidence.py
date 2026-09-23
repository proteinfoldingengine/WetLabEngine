"""Pinned v15.45 Task-1 access to the certified v15.44 carrier/operator closure."""
from __future__ import annotations
import importlib
import sys
from hashlib import sha1
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V1542 = HERE.parent / "v15.42-duality-covariant-transport-repair"
V1543 = HERE.parent / "v15.43-certified-response-geometry"
V1544 = HERE.parent / "v15.44-intrinsic-curvature-interpretation"

PINS = {
    V1542 / "exact_algebra.py": "c67ea42b61321469f7735ce589f2e729b241666a",
    V1542 / "operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    V1542 / "protocol_types.py": "e90a98d17baa6028f0d50a165f0b9d0046de13a2",
    V1542 / "transport.py": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
    V1542 / "holonomy.py": "bad3f06b291bb448a903b4f48344a9e54a633f68",
    V1543 / "projection.py": "f857f2cf1cd4c265c193121236af8e441b1f01dc",
    V1543 / "carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    V1543 / "docs/INPUTS.json": "f6435267950cde0985889056a67d5427f60f637f",
    V1544 / "operator_types.py": "1856a3b53738c4e1a84718826c19a1955848cd24",
    V1544 / "exact_matrix.py": "71a39f29f5499faabfb859ed3fd4d68dfa280c2f",
    V1544 / "derive.py": "ce72e488e17fba63a37cff46d07c64e42ffa14df",
}


def git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def verify_evidence():
    receipt = {}
    for path, expected in PINS.items():
        actual = git_blob(path.read_bytes())
        if actual != expected:
            raise ValueError("evidence_drift:" + str(path.relative_to(ROOT)))
        receipt[str(path.relative_to(ROOT))] = actual
    receipt["input_blob"] = PINS[V1543 / "docs/INPUTS.json"]
    receipt["derive_blob"] = PINS[V1544 / "derive.py"]
    return receipt


verify_evidence()
for path in (V1542, V1543, V1544):
    value = str(path)
    if value not in sys.path:
        sys.path.append(value)

for name in ("exact_algebra", "operational_complex", "protocol_types", "transport",
             "holonomy", "projection", "carriers", "operator_types", "exact_matrix"):
    importlib.import_module(name)

_projection = sys.modules["projection"]
_carriers = sys.modules["carriers"]
_operator_types = sys.modules["operator_types"]
_derive = importlib.import_module("derive")

Operator = _operator_types.Operator


def actual_carriers():
    verify_evidence()
    raw = (V1543 / "docs/INPUTS.json").read_bytes()
    projection = _projection.decode_projection(raw)
    return tuple(_carriers.build_carrier(payload) for payload in projection.payloads)


def reference_operator(carrier, presentation=None):
    """Independent frozen v15.44 coefficient oracle for tests only."""
    verify_evidence()
    return _derive.derive_operator(carrier, presentation)
