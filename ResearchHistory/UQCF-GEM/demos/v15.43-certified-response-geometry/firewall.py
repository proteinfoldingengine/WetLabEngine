from __future__ import annotations

import ast
from pathlib import Path


ACQUISITION_FILES = frozenset({"acquire.py"})
ENTRYPOINT_FILES = frozenset({"evaluate.py", "response_geometry_gate.py", "ci_verify.py", "evidence.py", "firewall.py"})
SERIALIZATION_FILES = frozenset({"projection.py"})
ACQUISITION_LOCAL = frozenset({"response_generation", "response_geometry", "representation_actions", "exact_linear", "pretime_gravity_canary", "projection", "evidence"})
PURE_LOCAL = frozenset({"projection", "carriers", "application", "presentation_checks", "application_controls", "exact_algebra", "operational_complex", "protocol_types", "transport", "holonomy"})
STDLIB_PURE = frozenset({"__future__", "collections", "dataclasses", "fractions", "functools", "itertools", "math", "operator", "typing"})
STDLIB_ENTRY = STDLIB_PURE | frozenset({"argparse", "ast", "hashlib", "json", "pathlib", "subprocess", "sys", "tempfile", "importlib"})
STDLIB_ACQUISITION = STDLIB_ENTRY | frozenset({"numpy"})
FORBIDDEN_CALLS = frozenset({"eval", "exec", "compile", "open", "input", "getattr", "setattr", "delattr", "globals", "locals", "vars", "__import__"})
FORBIDDEN_ATTRIBUTES = frozenset({"import_module", "reload", "eval", "exec", "__class__", "__dict__", "__bases__", "__subclasses__", "__getattribute__", "__getattr__", "__setattr__", "__delattr__", "mro"})
ENTRYPOINT_IMPORTS = {
    "evaluate.py": STDLIB_PURE | frozenset({"argparse", "hashlib", "json", "pathlib", "sys"}) | PURE_LOCAL | {"evidence", "firewall"},
    "response_geometry_gate.py": STDLIB_ENTRY | PURE_LOCAL | {"evidence", "firewall", "acquire", "application"},
    "ci_verify.py": STDLIB_ENTRY | {"evidence", "firewall"},
    "evidence.py": STDLIB_PURE | frozenset({"hashlib", "importlib", "json", "pathlib", "subprocess"}),
    "firewall.py": STDLIB_PURE | frozenset({"ast", "pathlib"}),
}
PURE_SYMBOLS = {
    "__future__": frozenset({"annotations"}),
    "collections": frozenset({"Counter", "defaultdict", "deque"}),
    "dataclasses": frozenset({"dataclass", "replace"}),
    "fractions": frozenset({"Fraction"}),
    "functools": frozenset({"lru_cache"}),
    "itertools": frozenset({"combinations", "permutations", "product"}),
    "typing": frozenset({"Any", "Iterable", "Mapping", "Sequence"}),
    "exact_algebra": frozenset({"matrix", "shape", "identity", "transpose", "matmul", "matvec", "add", "scale", "rref", "rank", "nullspace", "solve_unique"}),
    "operational_complex": frozenset({"ConnectionStatus", "OperationalComplex", "OperationalComplexAudit", "BaselineConnection", "BaselineConnectionAudit", "construct_operational_complex", "cycle_holonomy", "enumerate_baseline_connection"}),
    "protocol_types": frozenset({"CarrierKind", "MatrixAction", "TypedMap", "TransportManifest"}),
    "transport": frozenset({"FramePresentation", "LinearizedTransport", "validate_exact_field", "centered_derivatives", "cotangent_pullback_delta", "construct_transport"}),
    "holonomy": frozenset({"CurvatureRecord", "reverse_cycle", "rotate_cycle", "linearized_holonomy", "cotangent_holonomy", "curvature_invariant"}),
    "projection": frozenset({"CaseKey", "Field", "Payload", "Projection", "FAMILY_KEYS", "canonical_bytes", "decode_projection", "encode_projection"}),
    "carriers": frozenset({"Carrier", "build_carrier"}),
    "presentation_checks": frozenset({"check_presentations", "check_gauges", "compare_aligned", "require", "local_linear_certificate"}),
    "application_controls": frozenset({"check_carrier_controls", "check_response_controls"}),
    "application": frozenset({"FieldResult", "evaluate_field", "evaluate_projection", "classify"}),
}


def _role(path: Path) -> str:
    if path.name in ACQUISITION_FILES:
        return "acquisition"
    if path.name in ENTRYPOINT_FILES:
        return "entrypoint"
    if path.name in SERIALIZATION_FILES:
        return "serialization"
    return "pure"


def verify_firewall(paths: tuple[Path, ...]) -> dict:
    if type(paths) is not tuple or not all(isinstance(path, Path) for path in paths):
        raise TypeError("explicit Path tuple required")
    receipts = {}
    for supplied in paths:
        path = supplied.resolve(strict=True)
        role = _role(path)
        allowed = (STDLIB_ACQUISITION | ACQUISITION_LOCAL if role == "acquisition" else
                   ENTRYPOINT_IMPORTS[path.name] if role == "entrypoint" else
                   STDLIB_ENTRY | PURE_LOCAL if role == "serialization" else
                   STDLIB_PURE | PURE_LOCAL)
        tree = ast.parse(path.read_text(), filename=str(path))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if role == "pure" and any(alias.name.split(".")[0] in PURE_SYMBOLS for alias in node.names):
                    raise ValueError(f"pure imports must name approved symbols in {path.name}")
                imports.extend(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level or node.module is None or any(alias.name == "*" for alias in node.names):
                    raise ValueError(f"forbidden import in {path.name}")
                imported = node.module.split(".")[0]
                imports.append(imported)
                if role == "pure" and (imported not in PURE_SYMBOLS or
                                       any(alias.name not in PURE_SYMBOLS[imported] for alias in node.names)):
                    raise ValueError(f"forbidden imported symbol in {path.name}")
            elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
                  node.func.id in FORBIDDEN_CALLS and not (path.name == "evidence.py" and node.func.id == "getattr")):
                raise ValueError(f"forbidden capability {node.func.id} in {path.name}")
            elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRIBUTES:
                raise ValueError(f"forbidden dynamic or reflection capability {node.attr} in {path.name}")
        forbidden = sorted(set(imports) - allowed)
        if forbidden:
            raise ValueError(f"forbidden import in {path.name}: {', '.join(forbidden)}")
        receipts[path.name] = {"role": role, "imports": tuple(imports)}
    return receipts
