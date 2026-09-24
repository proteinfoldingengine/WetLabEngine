"""v15.49 final mechanical bridge adjudication."""
import json
ALLOWED={"BRIDGE_UNIQUE_UP_TO_EARNED_GAUGE","BRIDGE_FAMILY_NONUNIQUE","BRIDGE_INCONSISTENT","BRIDGE_ILL_TYPED"}
def canonical_bytes(x): return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
def adjudicate(contract,verification):
 if verification.get("status")!="VERIFIED_NO_CROSS_DOMAIN_MORPHISM_TYPE": raise ValueError("verification_status")
 r={"schema":"uqcf-v1549-results-v1","verdict":"BRIDGE_ILL_TYPED",
    "typing_status":contract["typing"]["status"],"bridge_enumeration_executed":False,
    "tasks_2_and_3":"NOT_EXECUTED_BY_TYPE_GATE","required_new_object":verification["required_new_object"],
    "source_correspondence":"NOT_EVALUATED","physical_source_law_adopted":False,
    "physical_gravity":False,"einstein_equations":False,"continuum_limit":False,"Pillar_3":"OPEN"}
 verify_result(r); return r
def verify_result(r):
 if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
 if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN": raise ValueError("claim_boundary")
 if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")): raise ValueError("claim_boundary")
 if r["verdict"]=="BRIDGE_ILL_TYPED" and (r.get("bridge_enumeration_executed") is not False or r.get("tasks_2_and_3")!="NOT_EXECUTED_BY_TYPE_GATE"): raise ValueError("type_gate")
 return True
