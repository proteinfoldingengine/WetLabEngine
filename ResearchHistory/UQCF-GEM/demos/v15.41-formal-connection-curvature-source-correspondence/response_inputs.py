from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib
import json
import sys

VectorQ = tuple[Fraction, ...]
SignedSupport = tuple[tuple[int, ...], ...]
REPO_ROOT = Path(__file__).resolve().parents[4]
V1540 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity"
V1540_SPEC = REPO_ROOT / "docs/superpowers/specs/2026-09-19-v1540-global-balance-geometry-specificity-design.md"
V1541_SPEC = REPO_ROOT / "docs/superpowers/specs/2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md"
BASE_SHA = "84aa1c81fd86ac4d7a06015482f98572f3afc05f"
EVIDENCE = {
    "v15.40-response-generation": (V1540 / "response_generation.py", "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5"),
    "v15.40-response-geometry": (V1540 / "response_geometry.py", "9128c24b695c1b539ac60dc93aeaf0bd4795c57b"),
    "v15.40-incidence-target": (V1540 / "incidence_target.py", "03c1f62279865aac396ea4b85f75a8d38c1629cf"),
    "v15.40-gate": (V1540 / "geometry_specificity_gate.py", "2e75867e6aedb82ebe3d9c1f04733e2c0d33018a"),
    "v15.40-tests": (V1540 / "test_gate.py", "349d500bd97178ac0e341e65699d0ce5f581b7cf"),
    "v15.40-results": (V1540 / "docs/RESULTS.json", "c56ca48110b3341e2d68289be717bf1e5308a20a"),
    "v15.40-design": (V1540_SPEC, "5f75f9a7ba1df5b21715f775d26bedbedc07297f"),
    "v15.41-design": (V1541_SPEC, "6d35aae0ccb6c2584d26d5a83d522b3cc7036728"),
}


@dataclass(frozen=True)
class FamilyInput:
    key: str
    labels: tuple[int, ...]
    sources: tuple[VectorQ, ...]
    responses: tuple[VectorQ, ...]
    work: tuple[tuple[Fraction, ...], ...]
    neighbors: frozenset[frozenset[int]]


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


@lru_cache(None)
def verify_evidence():
    verified = {}
    for key, (path, expected) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"evidence drift: {key}: {actual}")
        verified[key] = actual
    inherited = json.loads((V1540 / "docs/RESULTS.json").read_text())
    if inherited["status"] != "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES":
        raise AssertionError("v15.40 status drift")
    if inherited["finite_size_controls"] != [5, 7, 9, 11]:
        raise AssertionError("v15.40 size drift")
    if any(inherited["construction_firewall"].values()):
        raise AssertionError("v15.40 firewall drift")
    if inherited["Pillar_3"] != "OPEN":
        raise AssertionError("v15.40 Pillar 3 drift")
    return verified


@lru_cache(None)
def _modules():
    verify_evidence()
    if str(V1540) not in sys.path:
        sys.path.insert(0, str(V1540))
    generation = importlib.import_module("response_generation")
    geometry = importlib.import_module("response_geometry")
    return generation, geometry


@lru_cache(None)
def family_input(L: int, key: str, scale: Fraction = Fraction(1)) -> FamilyInput:
    generation, geometry_module = _modules()
    family = generation.response_family(L, key, scale)
    geometry = geometry_module.construct_response_geometry(
        family.labels, family.sources, family.responses
    )
    return FamilyInput(
        str(family.key),
        tuple(family.labels),
        tuple(tuple(Fraction(value) for value in row) for row in family.sources),
        tuple(tuple(Fraction(value) for value in row) for row in family.responses),
        tuple(tuple(Fraction(value) for value in row) for row in geometry.work),
        frozenset(frozenset(int(label) for label in edge) for edge in geometry.neighbors),
    )


@lru_cache(None)
def source_target_input(L: int):
    generation, _geometry = _modules()
    sources = family_input(L, "GLOBAL_BALANCE_COMPLETION", Fraction(1)).sources
    support = tuple(
        tuple(int(value) for value in row)
        for row in generation.signed_support_B2(L)
    )
    return sources, support
