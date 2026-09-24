"""v15.50 final mechanical adjudication."""
import json
ALLOWED={"COMMON_ANCESTOR_UNIQUE_UP_TO_EARNED_GAUGE","COMMON_ANCESTOR_NONUNIQUE","COMMON_ANCESTOR_INSUFFICIENT","COMMON_ANCESTOR_ILL_TYPED"}
def canonical_bytes(x): return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
def adjudicate(contract,verification):
 if verification.get("status")!="VERIFIED_COMMON_ANCESTOR_INSUFFICIENT": raise ValueError("verification_status")
 r={"schema":"uqcf-v1550-results-v1","verdict":"COMMON_ANCESTOR_INSUFFICIENT",
    "U_well_typed":True,"U_target_blind":verification["U_target_blind"],
    "retained_leg_derived":verification["retained_leg_lawful"],"quantum_leg_derived":verification["quantum_leg_derivable"],
    "missing_quantum_information":verification["missing_quantum_information"],
    "source_correspondence":"NOT_EVALUATED","physical_source_law_adopted":False,
    "physical_gravity":False,"einstein_equations":False,"continuum_limit":False,"Pillar_3":"OPEN"}
 verify_result(r); return r
def verify_result(r):
 if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
 if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN": raise ValueError("claim_boundary")
 if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")): raise ValueError("claim_boundary")
 if r["verdict"]=="COMMON_ANCESTOR_INSUFFICIENT" and (r.get("U_well_typed") is not True or r.get("retained_leg_derived") is not True or r.get("quantum_leg_derived") is not False): raise ValueError("insufficiency_support")
 return True
