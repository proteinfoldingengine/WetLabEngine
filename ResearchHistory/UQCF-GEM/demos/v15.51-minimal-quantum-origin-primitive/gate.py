"""v15.51 final mechanical adjudication."""
import json
ALLOWED={"MINIMAL_QUANTUM_ORIGIN_PRIMITIVE_IDENTIFIED","QUANTUM_ORIGIN_PRIMITIVE_FAMILY_NONUNIQUE","TESTED_PRIMITIVES_INSUFFICIENT","QUANTUM_ORIGIN_CLASSIFICATION_ILL_TYPED"}
def canonical_bytes(x): return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
def adjudicate(contract,verification):
 if verification.get("status")!="VERIFIED_TESTED_PRIMITIVES_INSUFFICIENT": raise ValueError("verification_status")
 r={"schema":"uqcf-v1551-results-v1","verdict":"TESTED_PRIMITIVES_INSUFFICIENT",
    "tested_packages":verification["tested_packages"],"successful_packages":verification["successful_packages"],
    "minimal_successful_packages":[],"source_correspondence":"NOT_EVALUATED",
    "physical_source_law_adopted":False,"physical_gravity":False,"einstein_equations":False,
    "continuum_limit":False,"Pillar_3":"OPEN"}
 verify_result(r); return r
def verify_result(r):
 if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
 if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN": raise ValueError("claim_boundary")
 if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")): raise ValueError("claim_boundary")
 return True
