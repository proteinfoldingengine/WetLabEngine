"""v15.53 Task 5: exhaustive producer-side frozen-family witness search."""
from copy import deepcopy
import json

import realization_family as rf
import reduction as red
import equivalence as eq

def _canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def _structural_record(realization):
    q = deepcopy(realization)
    q.pop("id", None)
    return q

def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(x) for x in value]
    if isinstance(value, list):
        return [_jsonable(x) for x in value]
    if isinstance(value, dict):
        return {k:_jsonable(v) for k,v in value.items()}
    return value

def _base_result():
    return {
        "schema": "uqcf-v1553-producer-search-v1",
        "scope": "FROZEN_V15_53_FINITE_FAMILY_ONLY",
        "candidate_count": 0,
        "admissible_count": 0,
        "retained_fiber_count": 0,
        "target_class_count": 0,
        "primary_verdict": "VERIFICATION_FAILED",
        "witness": None,
        "reasons": [],
        "source_correspondence": "NOT_EVALUATED",
        "Pillar_3": "OPEN",
        "physical_gravity": False,
        "interpretation": "No adjudication completed.",
    }

def search_family(contract, family):
    result = _base_result()
    if not isinstance(family, (tuple, list)) or not family:
        result["primary_verdict"] = "FAMILY_INVALID"
        result["reasons"] = ["EMPTY_OR_MALFORMED_FAMILY"]
        result["interpretation"] = "The frozen-family search input is invalid."
        return result

    family = tuple(deepcopy(x) for x in family)
    result["candidate_count"] = len(family)

    structural = []
    for r in family:
        if not isinstance(r, dict):
            result["primary_verdict"] = "FAMILY_INVALID"
            result["reasons"] = ["MALFORMED_REALIZATION"]
            result["interpretation"] = "At least one realization record is malformed."
            return result
        structural.append(_canonical_json(_structural_record(r)))
    if len(set(structural)) != len(structural):
        result["primary_verdict"] = "FAMILY_INVALID"
        result["reasons"] = ["DUPLICATE_REALIZATION"]
        result["interpretation"] = "The supplied frozen family contains a duplicate structural realization."
        return result

    rows = []
    invalid = []
    for r in family:
        check = rf.check_admissibility(contract, r)
        if check.get("status") != "ADMISSIBLE":
            invalid.append({"id":r.get("id"), "status":check.get("status")})
            continue
        readout = red.reduce_to_retained(contract, r)
        class_key = eq.canonical_class_key(contract, r)
        rows.append({
            "id": r.get("id"),
            "readout": readout,
            "readout_key": _canonical_json(readout),
            "class_key": class_key,
        })

    result["admissible_count"] = len(rows)
    if invalid:
        result["primary_verdict"] = "FAMILY_INVALID"
        result["reasons"] = ["INADMISSIBLE_REALIZATION"]
        result["invalid_candidates"] = invalid
        result["interpretation"] = "At least one member of the frozen realization family is inadmissible."
        return result

    fibers = {}
    for row in rows:
        fibers.setdefault(row["readout_key"], []).append(row)
    result["retained_fiber_count"] = len(fibers)
    all_classes = {_canonical_json(_jsonable(row["class_key"])) for row in rows}
    result["target_class_count"] = len(all_classes)

    witness = None
    for readout_key in sorted(fibers):
        fiber = sorted(fibers[readout_key], key=lambda x:(str(x["id"]), _canonical_json(_jsonable(x["class_key"]))))
        for i,left in enumerate(fiber):
            for right in fiber[i+1:]:
                if left["class_key"] != right["class_key"]:
                    witness = {
                        "left_id": left["id"],
                        "right_id": right["id"],
                        "retained_readout": left["readout"],
                        "left_class_key": _jsonable(left["class_key"]),
                        "right_class_key": _jsonable(right["class_key"]),
                    }
                    break
            if witness is not None:
                break
        if witness is not None:
            break

    if witness is not None:
        result["primary_verdict"] = "CERTIFIED_FAMILY_OBSTRUCTION_WITNESS"
        result["witness"] = witness
        result["interpretation"] = (
            "In the frozen v15.53 finite realization family, the registered retained "
            "reduction does not uniquely determine the registered structural target "
            "equivalence class. This statement is scoped only to this family."
        )
    else:
        result["primary_verdict"] = "NO_WITNESS_IN_FROZEN_FAMILY"
        result["interpretation"] = (
            "No same-readout/distinct-target witness occurs in the frozen v15.53 "
            "finite realization family. This does not extend beyond this family."
        )
    return result

def search_frozen_family(contract):
    return search_family(contract, rf.enumerate_raw_realizations(contract))
