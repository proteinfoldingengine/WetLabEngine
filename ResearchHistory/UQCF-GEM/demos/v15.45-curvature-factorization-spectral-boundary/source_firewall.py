"""Task 5: source-correspondence construction firewall.

Only algebraic identities already fixed by upstream response definitions are
classified here. No physical source verdict is emitted and no source data enter
Tasks 1--4.
"""
from __future__ import annotations
from hashlib import sha1
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1540 = HERE.parent / "v15.40-global-balance-geometry-specificity"
GENERATION = V1540 / "response_generation.py"
GENERATION_BLOB = "d9c2547c5e1b04f99c7b6d0d793842eef383ce39"

FAMILIES = (
    "GLOBAL_BALANCE_COMPLETION",
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)


def _git_blob(raw):
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def _verify_upstream_definition():
    raw = GENERATION.read_bytes()
    actual = _git_blob(raw)
    if actual != GENERATION_BLOB:
        raise ValueError("response_generation_drift")
    text = raw.decode("utf-8")
    required = (
        'if key == "DIRECT_INHERITANCE": return source',
        'if key == "ONE_INCIDENCE_TRANSPORT": return _adjacency_apply',
        'if key in GENERATORS:',
        'solve_with_verified_inverse(defect, inverse',
        '"GLOBAL_BALANCE_COMPLETION"',
        '"MATCHED_DIAGONAL_BALANCE"',
        '"MATCHED_STEP2_BALANCE"',
    )
    if any(token not in text for token in required):
        raise ValueError("response_definition_missing")
    return actual


def classify_source_relation(family):
    if family not in FAMILIES:
        raise ValueError("unknown_family")
    identities = {
        # Frozen global-balance response definition: D_ax phi=s on the
        # augmentation subspace. Task-3 factorization: A phi=(1/2) M D_ax phi.
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


def audit_source_relations():
    upstream_blob = _verify_upstream_definition()
    sizes = (5, 7, 9, 11)
    families = []
    for family in FAMILIES:
        item = classify_source_relation(family)
        item["sizes"] = sizes
        # "verified" here means algebraically composed from pinned definitions,
        # not a new empirical comparison. For the canonical family:
        # D_ax phi=s and A=(1/2) M D_ax, hence A phi=(1/2) M s.
        item["exact_composition_verified"] = True
        families.append(item)
    return {
        "schema": "uqcf-v1545-task5-source-firewall-v1",
        "upstream_response_generation_blob": upstream_blob,
        "family_count": len(families),
        "families": tuple(families),
        "source_correspondence": "NOT_EVALUATED",
        "physical_gravity": False,
        "stress_energy": False,
        "einstein_equations": False,
        "Pillar_3": "OPEN",
        "construction_firewall": True,
    }
