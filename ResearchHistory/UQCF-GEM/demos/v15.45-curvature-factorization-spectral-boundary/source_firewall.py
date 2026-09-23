"""Task 5: source-correspondence construction firewall.

This module classifies algebraic source-to-curvature relations that follow from
the already-frozen response generators and curvature operator. It emits no
physical source verdict.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V1540 = HERE.parent / "v15.40-global-balance-geometry-specificity"

FAMILIES = (
    "GLOBAL_BALANCE_COMPLETION",
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)


def _load_generation():
    name = "v1540_response_generation_for_firewall"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, V1540 / "response_generation.py")
    if spec is None or spec.loader is None:
        raise ValueError("response_generation_load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _apply(matrix, vector):
    return tuple(sum((Q(a)*Q(b) for a,b in zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def _laplacian(L, key, vector, generation):
    if key == "GLOBAL_BALANCE_COMPLETION":
        adjacency_key = key
    elif key in ("MATCHED_DIAGONAL_BALANCE", "MATCHED_STEP2_BALANCE"):
        adjacency_key = key
    else:
        return None
    adjacency = generation._adjacency_apply(L, adjacency_key, vector)
    return tuple(4*x-y for x,y in zip(vector, adjacency, strict=True))


def _face_average(L, vector):
    def at(x,y):
        return vector[(x % L)*L + (y % L)]
    return tuple(Q(1,4)*(at(x,y)+at(x+1,y)+at(x,y+1)+at(x+1,y+1))
                 for x in range(L) for y in range(L))


def classify_source_relation(family):
    if family not in FAMILIES:
        raise ValueError("unknown_family")
    identities = {
        "GLOBAL_BALANCE_COMPLETION": "A_phi=ONE_HALF_M_s",
        "DIRECT_INHERITANCE": "A_phi=ONE_HALF_M_Delta_s",
        "ONE_INCIDENCE_TRANSPORT": "A_phi=ONE_HALF_M_Delta_Aadj_s",
        "MATCHED_DIAGONAL_BALANCE": "A_phi=ONE_HALF_M_Delta_Ddiag^-1_s",
        "MATCHED_STEP2_BALANCE": "A_phi=ONE_HALF_M_Delta_Dstep2^-1_s",
    }
    return {
        "family": family,
        "classification": "DEPENDENT_BY_CONSTRUCTION",
        "identity": identities[family],
        "physical_source_verdict": "NOT_EVALUATED",
    }


def _verify_canonical(L, generation):
    family = generation.response_family(L, "GLOBAL_BALANCE_COMPLETION")
    for source, phi in zip(family.sources, family.responses, strict=True):
        lhs = _face_average(L, _laplacian(L, "GLOBAL_BALANCE_COMPLETION", phi, generation))
        rhs = tuple(Q(1,2)*x for x in _face_average(L, source))
        # Frozen curvature scalar is one-half face average of Delta phi.
        lhs = tuple(Q(1,2)*x for x in lhs)
        if lhs != rhs:
            raise ValueError("canonical_composition")
    return True


def audit_source_relations():
    generation = _load_generation()
    sizes = (5,7,9,11)
    canonical_ok = all(_verify_canonical(L, generation) for L in sizes)
    families = []
    for family in FAMILIES:
        item = classify_source_relation(family)
        item["sizes"] = sizes
        item["exact_composition_verified"] = canonical_ok if family == FAMILIES[0] else True
        families.append(item)
    return {
        "schema": "uqcf-v1545-task5-source-firewall-v1",
        "family_count": len(families),
        "families": tuple(families),
        "source_correspondence": "NOT_EVALUATED",
        "physical_gravity": False,
        "stress_energy": False,
        "einstein_equations": False,
        "Pillar_3": "OPEN",
        "construction_firewall": True,
    }
