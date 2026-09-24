"""v15.48 final mechanical adjudication."""
import json
ALLOWED={
 "RECOVERABILITY_SIGNATURE_SELECTS_REPRESENTATION_CLASS",
 "RECOVERABILITY_SIGNATURE_STILL_NONSELECTIVE",
 "RECOVERABILITY_SIGNATURE_INCONSISTENT",
 "RECOVERABILITY_SIGNATURE_ILL_TYPED",
}
def canonical_bytes(x):
    return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
def adjudicate(contract,verification):
    if verification.get("status")!="VERIFIED_NO_COMMON_TYPE_CERTIFIED":
        raise ValueError("verification_status")
    r={
      "schema":"uqcf-v1548-results-v1",
      "verdict":"RECOVERABILITY_SIGNATURE_ILL_TYPED",
      "type_audit_status":contract["type_audit"]["status"],
      "signature_matching_executed":False,
      "tasks_2_and_3":"NOT_EXECUTED_BY_STOP_RULE",
      "required_new_axiom":verification["required_new_axiom"],
      "source_correspondence":"NOT_EVALUATED",
      "physical_source_law_adopted":False,
      "physical_gravity":False,
      "einstein_equations":False,
      "continuum_limit":False,
      "Pillar_3":"OPEN",
    }
    verify_result(r); return r
def verify_result(r):
    if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
    if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN":
        raise ValueError("claim_boundary")
    if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")):
        raise ValueError("claim_boundary")
    if r["verdict"]=="RECOVERABILITY_SIGNATURE_ILL_TYPED":
        if r.get("signature_matching_executed") is not False or r.get("tasks_2_and_3")!="NOT_EXECUTED_BY_STOP_RULE":
            raise ValueError("stop_rule")
    return True
