"""Stage C5: mechanical adjudication for the primitive joint-record derivation gate."""
from __future__ import annotations
import json

ALLOWED={"UNIQUE_UP_TO_EARNED_GAUGE","REPRESENTATION_NONUNIQUE","NO_REPRESENTATION_DERIVED","ILL_TYPED"}

def canonical_bytes(value):
    return (json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")

def adjudicate(contract,witness,verification):
    if verification.get("status")!="VERIFIED_INEQUIVALENT_REPRESENTATIONS":
        raise ValueError("verification_status")
    result={
      "schema":"uqcf-v1546-stage-c-results-v1",
      "verdict":"REPRESENTATION_NONUNIQUE",
      "basis":"VERIFIED_TWO_SORT_BIJECTION_EXPANSIONS",
      "same_frozen_constraints":verification["same_frozen_constraints"],
      "same_frozen_reduct":verification["same_frozen_reduct"],
      "related_by_earned_gauge":verification["related_by_earned_gauge"],
      "source_correspondence":"NOT_EVALUATED",
      "physical_source_law_adopted":False,
      "physical_gravity":False,
      "einstein_equations":False,
      "continuum_limit":False,
      "Pillar_3":"OPEN",
      "interpretation":"AUDITED_FROZEN_ONTOLOGY_DOES_NOT_UNIQUELY_DERIVE_JOINT_QUANTUM_REPRESENTATION_UP_TO_EARNED_GAUGE"
    }
    verify_result(result)
    return result

def verify_result(r):
    if r.get("schema")!="uqcf-v1546-stage-c-results-v1": raise ValueError("schema")
    if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
    if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN": raise ValueError("claim_boundary")
    if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")):
        raise ValueError("claim_boundary")
    if r["verdict"]=="REPRESENTATION_NONUNIQUE":
        if r.get("same_frozen_constraints") is not True or r.get("same_frozen_reduct") is not True or r.get("related_by_earned_gauge") is not False:
            raise ValueError("nonuniqueness_support")
    return True
