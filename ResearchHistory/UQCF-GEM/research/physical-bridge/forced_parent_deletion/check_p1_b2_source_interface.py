"""Audit whether the archived B2 source is an inherited P1 source interface."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import sys


BASE = Path("ResearchHistory/UQCF-GEM")
PHYS = BASE / "research/physical-bridge/forced_parent_deletion"
PINS = {
    BASE / "demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py":
        "620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a",
    BASE / "demos/v15.39-higher-incidence-source-axioms/docs/RESULTS.json":
        "ac8eb10ed90360fee6dcc0f170f19fffd0d74116",
    BASE / "demos/v15.40-global-balance-geometry-specificity/response_generation.py":
        "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5",
    BASE / "demos/v15.43-certified-response-geometry/acquire.py":
        "90f76146e7f6a875531a941290ad15679a8fb52f",
    BASE / "demos/v15.43-certified-response-geometry/README.md":
        "c939816a8b5b528fad2e82846e47dc7104cdc247",
    PHYS / "P1_WORK_CONNECTION.md":
        "c927a82fef384bdbc40bfa679cf2b2f404a98cb1",
    PHYS / "P1_WORK_CONNECTION_RESULT.md":
        "3a680f917bed6e9d4e9bea19ffc5bb05bc8a2765",
    BASE / "foundational-closure-verification/PROOFS.md":
        "a21acad73c80cb748f2e42c244f6db53146c2bf2",
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def function_text(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.unparse(node)
    raise AssertionError(f"missing function {name} in {path}")


def run(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    source_pins = []
    for path, expected in PINS.items():
        data = path.read_bytes()
        actual = git_blob(data)
        assert actual == expected, (path, actual)
        target = out / (path.parent.name + "__" + path.name)
        target.write_bytes(data)
        source_pins.append({
            "path": str(path),
            "blob": actual,
            "sha256": hashlib.sha256(data).hexdigest(),
        })

    ledger = json.loads(
        (BASE / "demos/v15.39-higher-incidence-source-axioms/docs/RESULTS.json").read_text()
    )
    protocol = ledger["source_protocol"]
    assert ledger["source_axiom_derived_from_frozen_ontology"] is False
    assert ledger["source_axiom_user_approved_before_execution"] is True
    assert ledger["uses_pruning"] is False
    assert protocol["all_B1_B2_zero"] is True
    assert protocol["closed_face_coarse_q_null"] is True
    assert protocol["closed_face_higher_incidence_source_nonnull"] is True
    assert protocol["source_additivity_exact"] is True
    assert protocol["source_reversal_exact"] is True
    assert protocol["source_carrier"] == "Q_PLUS_BOUNDARY_INCIDENCE_PROVENANCE"
    assert all(
        row["closed_face_delta_is_B2_column"]
        and row["closed_face_coarse_q_null"]
        and row["closed_face_higher_incidence_source_nonnull"]
        for row in protocol["size_rows"]
    )

    source_path = BASE / "demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py"
    lift = function_text(source_path, "source_lift")
    assert "q = _int_matvec(c.B1, delta)" in lift
    assert "c.B2[e, face_index]" in lift
    assert "kappa = _scale(a * sigma, boundary)" in lift

    generation_path = BASE / "demos/v15.40-global-balance-geometry-specificity/response_generation.py"
    centered = function_text(generation_path, "centered_source")
    family = function_text(generation_path, "_unit_family")
    assert "source[face_index] += 1" in centered
    assert "centered_source(L, label)" in family

    acquire_path = BASE / "demos/v15.43-certified-response-geometry/acquire.py"
    acquisition = function_text(acquire_path, "_project_modules")
    imports = {
        alias.name
        for node in ast.parse(acquire_path.read_text()).body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert "generation.response_family" in acquisition
    assert "geometry_module.construct_response_geometry" in acquisition
    assert not any("lineage" in name.lower() or "prun" in name.lower() for name in imports)

    readme = (BASE / "demos/v15.43-certified-response-geometry/README.md").read_text()
    assert "Source correspondence is NOT_EVALUATED" in readme

    proof = (PHYS / "P1_WORK_CONNECTION.md").read_text()
    assert "SUPPLIED. The same-Genesis trees, periodic address catalog, source preparations" in proof
    assert "Building the required multi-address preparation from a native source" in proof

    return {
        "source_pins": source_pins,
        "positive_candidate": {
            "closed_face_delta_is_B2_column_all_sizes": True,
            "closed_face_higher_incidence_nonnull": True,
            "additive_and_reversible": True,
            "coarse_vertex_q_is_B1_delta": True,
        },
        "boundary": {
            "source_axiom_derived_from_frozen_ontology": False,
            "source_axiom_user_approved_before_execution": True,
            "uses_pruning": False,
            "closed_face_coarse_q_null": True,
            "v1543_source_correspondence": "NOT_EVALUATED",
            "v1543_acquisition_consumes_p1": False,
            "p1_four_corner_preparation_supplied": True,
        },
        "conclusion": (
            "the inspected B2 higher-incidence source does not provide an inherited "
            "P1-retained-grade-to-periodic-source correspondence"
        ),
        "native_bridge_status": "OPEN",
    }


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
