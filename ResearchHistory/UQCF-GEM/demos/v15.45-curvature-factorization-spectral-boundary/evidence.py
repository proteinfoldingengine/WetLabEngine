"""Pinned v15.45 Task-1 access to the certified v15.44 carrier/operator closure."""
from __future__ import annotations
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V1542 = HERE.parent / "v15.42-duality-covariant-transport-repair"
V1543 = HERE.parent / "v15.43-certified-response-geometry"
V1544 = HERE.parent / "v15.44-intrinsic-curvature-interpretation"

for path in (V1542, V1543, V1544):
    value = str(path)
    if value not in sys.path:
        sys.path.append(value)

# Load the exact frozen closure under the module names used by the certified code.
for name in ("exact_algebra", "operational_complex", "protocol_types", "transport",
             "holonomy", "projection", "carriers", "operator_types", "exact_matrix"):
    importlib.import_module(name)

_projection = sys.modules["projection"]
_carriers = sys.modules["carriers"]
_operator_types = sys.modules["operator_types"]
_derive = importlib.import_module("derive")

Operator = _operator_types.Operator


def actual_carriers():
    raw = (V1543 / "docs/INPUTS.json").read_bytes()
    projection = _projection.decode_projection(raw)
    return tuple(_carriers.build_carrier(payload) for payload in projection.payloads)


def reference_operator(carrier):
    """Independent frozen v15.44 coefficient oracle for tests only."""
    return _derive.derive_operator(carrier)
