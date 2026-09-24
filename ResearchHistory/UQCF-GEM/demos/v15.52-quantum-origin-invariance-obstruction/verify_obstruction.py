"""Independent Task-4 audit; not a quantum-realization or proof-assistant checker.

The archived contract registers no quantum model family/admissibility/reduct
validator. This module therefore deliberately has NO quantum-certification path.
It checks finite relational premises and rejects unearned semantic promotion.
"""
from __future__ import annotations

from itertools import permutations
from hashlib import sha1
from pathlib import Path
import argparse
import json

FIELDS = ("objects", "lineage", "dependency", "recoverability", "composition",
          "refinement", "disjoint_composition")
OBSERVABLES = ("object_count", "lineage_incidence", "dependency_incidence",
               "recoverability_relation", "composition_table", "refinement_diagram",
               "disjoint_partition")
TARGET_FIELDS = ("carrier_representation_class", "subsystem_composition",
                 "recovery_capable_operations", "typed_quantum_leg")
FORBIDDEN = ("target_labels", "target_dimension", "hilbert_space", "matrix_algebra",
             "node_site_dictionary", "quantum_leg", "fixture_order_selector")
PREFIX = "ResearchHistory/UQCF-GEM/demos/"
SOURCE_PINS = {
    "v1551_result": (PREFIX+"v15.51-minimal-quantum-origin-primitive/docs/RESULTS.json", "e52c2d1e8330d6699f84b293ec456b375f7fc7d0"),
    "v1550_U": (PREFIX+"v15.50-common-ancestor-universal-object/common_contract.py", "3dada32767cad81dbf02dd78107e8ede7f89fca7"),
    "v1546_stage_c": (PREFIX+"v15.46-primitive-joint-source-admissibility/docs/STAGE_C_RESULTS.json", "30e0b10c9317f81c7f7627a15919148a31583c73"),
}
ARCHIVED_PINS = {
    "obstruction_contract.py": "a8e018c19072f28f9b9820e158a4e76abd559699",
    "source_automorphisms.py": "73329451ac43ab291c1e019c09e76b4352eb3359",
    "obstruction_witness.py": "fcf5eb6dbb998f09818d3382b23f11820c86ba12",
    "test_obstruction_contract.py": "afe9a91aa987ff78fe6bfee1aed736dd3d9383b0",
    "test_source_automorphisms.py": "cbeed6b60f0a4919552146f5b70348d8e9298500",
    "test_obstruction_witness.py": "73e0fb3cfc2164a62012375cc55ff646b7027fad",
}


def canonical(value):
    """Exact JSON-like values; tuples/lists have the same serialized meaning."""
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise ValueError("non_string_record_key")
        return ("record", tuple((k, canonical(v)) for k, v in sorted(value.items())))
    if isinstance(value, (list, tuple)):
        return ("sequence", tuple(canonical(v) for v in value))
    if type(value) in (str, int, bool, type(None)):
        return (type(value).__name__, value)
    raise ValueError("unsupported_nonexact_value")


def expected_contract():
    """Independent copy of the archived contract, not a new equivalence law."""
    return {
        "schema": "uqcf-v1552-obstruction-contract-v1",
        "sources": {k: {"path": p, "git_blob_sha": h} for k, (p, h) in SOURCE_PINS.items()},
        "E": {"allowed_fields": list(FIELDS),
              "observables": [{"id": x, "source_definable": True} for x in OBSERVABLES],
              "automorphism_requirement": "COMPLETE_FINITE_ACTION"},
        "quantum_equivalence": "IDENTITY_ONLY",
        "theorems": ["T1_INVARIANCE_OBSTRUCTION", "T2_REPRESENTATION_ORIGIN_COROLLARY", "T3_NECESSARY_NEW_DATUM"],
        "forbidden_fields": list(FORBIDDEN),
        "prohibited_inputs": {x: True for x in ("geometry", "curvature", "source_response", "gravity", "continuum", "empirical_fit", "physical_time")},
        "source_correspondence": "NOT_EVALUATED", "Pillar_3": "OPEN",
    }


def validate_source(fixture):
    """Validate finite incidence typing, not quantum/category admissibility."""
    if not isinstance(fixture, dict) or set(fixture) != set(FIELDS):
        raise ValueError("source_fields")
    objects = fixture["objects"]
    if not isinstance(objects, (list, tuple)) or not all(type(x) is str for x in objects):
        raise ValueError("object_labels")
    n = len(objects)
    if n > 7 or len(set(objects)) != n:
        raise ValueError("finite_audit_domain_or_duplicate_objects")

    def relation(rows, arity):
        if not isinstance(rows, (list, tuple)):
            raise ValueError("relation_type")
        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) != arity:
                raise ValueError("relation_arity")
            if any(type(i) is not int or not 0 <= i < n for i in row):
                raise ValueError("relation_endpoint")

    for key in ("lineage", "dependency", "recoverability", "disjoint_composition"):
        relation(fixture[key], 2)
    relation(fixture["composition"], 3)
    if not isinstance(fixture["refinement"], (list, tuple)):
        raise ValueError("refinement_type")
    for diagram in fixture["refinement"]:
        if not isinstance(diagram, (list, tuple)) or len(diagram) != 2:
            raise ValueError("refinement_arity")
        relation(diagram, 2)
    return n


def independent_automorphisms(fixture):
    """Enumerate all n! maps; preserve every diagram, not only diagram zero.

    Binary incidences remain ordered, matching the archived executable. The
    two paths inside each refinement diagram are unordered. No target action
    or nontrivial source symmetry is inferred from this enumeration.
    """
    n = validate_source(fixture)
    keys = ("lineage", "dependency", "recoverability", "composition", "disjoint_composition")
    relations = {k: frozenset(tuple(row) for row in fixture[k]) for k in keys}
    diagrams = frozenset(frozenset(tuple(row) for row in d) for d in fixture["refinement"])
    result = []
    for p in permutations(range(n)):
        if any(frozenset(tuple(p[i] for i in row) for row in relations[k]) != relations[k] for k in keys):
            continue
        mapped = frozenset(frozenset(tuple(p[i] for i in row) for row in d) for d in diagrams)
        if mapped == diagrams:
            result.append(p)
    return tuple(result)


def source_readouts(fixture):
    validate_source(fixture)
    return dict(zip(OBSERVABLES, (
        len(fixture["objects"]), fixture["lineage"],
        fixture["dependency"], fixture["recoverability"],
        fixture["composition"], fixture["refinement"],
        fixture["disjoint_composition"])))


def finite_factorization(observations, target_classes):
    """Check existence of h on im(O) with target = h o O for a finite table.

    target_classes are supplied exact mathematical classes, NOT validated
    quantum equivalence classes. See docs/TASK4_THEOREM_AUDIT.md for the proof.
    """
    if len(observations) != len(target_classes):
        raise ValueError("domain_length_mismatch")
    fibers = {}
    for index, (obs, target) in enumerate(zip(observations, target_classes)):
        key, value = canonical(obs), canonical(target)
        if key in fibers and fibers[key][0] != value:
            return {"factorable": False, "conflict": [fibers[key][1], index]}
        fibers.setdefault(key, (value, index))
    return {"factorable": True, "conflict": None}


def verify_obstruction(contract, fixture, automorphisms, witness, selector_mode="deterministic"):
    """Audit archived packets independently; never promote labels to physics."""
    reasons = ["QUANTUM_ADMISSIBILITY_AND_REDUCTION_NOT_REGISTERED"]
    result = {
        "schema": "uqcf-v1552-independent-audit-v1", "status": "WITNESS_REJECTED",
        "quantum_origin_certified": False,
        "T1": "GENERAL_FACTORIZATION_LEMMA_WITH_FINITE_REGRESSION_CHECKS",
        "T2": "NOT_CERTIFIED", "T3": "CONDITIONAL_ON_VALID_TARGET_WITNESS",
        "proof_assistant_certification": False,
        "arbitrary_choice_obstructed": False, "full_E_class_coverage": False,
        "quantum_witness_search": "NOT_PERFORMED_NO_REGISTERED_REALIZATION_FAMILY",
        "observable_scope": "SEVEN_REGISTERED_READOUTS_NO_QUANTUM_REDUCT_MAP",
        "source_correspondence": "NOT_EVALUATED", "Pillar_3": "OPEN",
        "physical_gravity": False, "reported_separating_observables": [],
        "nontrivial_source_automorphism_count": None, "reasons": reasons,
    }
    try:
        if canonical(contract) != canonical(expected_contract()):
            reasons.append("FROZEN_CONTRACT_CHANGED")
    except (ValueError, TypeError):
        reasons.append("FROZEN_CONTRACT_CHANGED")
    if selector_mode != "deterministic":
        reasons.append("RANDOMIZED_OR_UNKNOWN_SELECTOR")
    try:
        actual = independent_automorphisms(fixture)
        readouts = source_readouts(fixture)
    except (ValueError, TypeError):
        reasons.append("SOURCE_SCHEMA_INVALID")
        return result
    identity = tuple(range(len(fixture["objects"])))
    result["independent_automorphisms"] = [list(p) for p in actual]
    result["nontrivial_source_automorphism_count"] = sum(p != identity for p in actual)
    valid_maps = []
    if not isinstance(automorphisms, (tuple, list)):
        reasons.append("INVALID_AUTOMORPHISM")
    else:
        for p in automorphisms:
            if (not isinstance(p, (tuple, list)) or any(type(i) is not int for i in p)
                    or sorted(p) != list(identity)):
                reasons.append("INVALID_AUTOMORPHISM")
            else:
                valid_maps.append(tuple(p))
    if len(set(valid_maps)) != len(valid_maps):
        reasons.append("DUPLICATE_AUTOMORPHISM")
    if set(valid_maps) != set(actual):
        reasons.append("AUTOMORPHISM_ACTION_INCOMPLETE")
    if not isinstance(witness, dict):
        reasons.append("WITNESS_SCHEMA_INVALID")
        return result
    if type(witness.get("automorphism_count")) is not int or witness["automorphism_count"] != len(actual):
        reasons.append("AUTOMORPHISM_COUNT_MISMATCH")
    if canonical(witness.get("construction_inputs")) != canonical(FIELDS):
        reasons.append("CONSTRUCTION_INPUTS_CHANGED")
    if canonical(witness.get("E_observables_checked")) != canonical(OBSERVABLES):
        reasons.append("OBSERVABLE_CHECKLIST_MISMATCH")
    q1, q2 = witness.get("Q1"), witness.get("Q2")
    if not isinstance(q1, dict) or not isinstance(q2, dict):
        reasons.append("WITNESS_SCHEMA_INVALID")
        return result
    if canonical(q1) == canonical(q2):
        reasons.append("IDENTICAL_TARGET_RECORDS")
    if all(type(q.get(k)) is str for q in (q1, q2) for k in TARGET_FIELDS):
        reasons.append("LABEL_ONLY_QUANTUM_OUTPUTS")
    o1, o2 = q1.get("E_observables"), q2.get("E_observables")
    if o1 is o2 and isinstance(o1, dict):
        reasons.append("ALIASED_OBSERVABLE_RECORDS")
    for name, obs in (("Q1", o1), ("Q2", o2)):
        if not isinstance(obs, dict) or set(obs) != set(OBSERVABLES):
            reasons.append("OBSERVABLE_DOMAIN_MISMATCH:"+name)
        if isinstance(obs, dict):
            for key in OBSERVABLES:
                if key in obs and canonical(obs[key]) != canonical(readouts[key]):
                    reasons.append("SOURCE_OBSERVABLE_MISMATCH:"+name+":"+key)
    if isinstance(o1, dict) and isinstance(o2, dict):
        result["reported_separating_observables"] = [k for k in OBSERVABLES if k in o1 and k in o2 and canonical(o1[k]) != canonical(o2[k])]
    result["reasons"] = sorted(set(reasons))
    return result


def archived_integrity(root, here):
    pins = {p: h for p, h in SOURCE_PINS.values()}
    pins.update({str((here/name).relative_to(root)): h for name, h in ARCHIVED_PINS.items()})
    for path, expected in pins.items():
        raw = (root/path).read_bytes()
        actual = sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        if actual != expected:
            raise ValueError("archived_blob_mismatch:"+path)
    return pins


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[3]
    pins = archived_integrity(root, here)
    # Import the producer only to obtain its packet, never its validity checks.
    import obstruction_contract as oc
    import source_automorphisms as sa
    import obstruction_witness as ow
    contract = oc.load_contract(root)
    fixture = sa.frozen_fixture(contract)
    autos = sa.enumerate_automorphisms(contract, fixture)
    witness = ow.find_witness(contract, fixture, autos)
    report = verify_obstruction(contract, fixture, autos, witness)
    report["audited_source_head"] = "9623fcefdef304ed9e22a64625e170a622094b8f"
    report["verified_archived_blobs"] = pins
    raw = json.dumps(report, sort_keys=True, separators=(",", ":"))+"\n"
    if args.output:
        args.output.write_text(raw, encoding="utf-8")
    else:
        print(raw, end="")


if __name__ == "__main__":
    main()
