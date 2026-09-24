"""v15.47 Task 5: mechanical functoriality adjudication."""
import json
ALLOWED={"FUNCTORIALITY_STILL_NONSELECTIVE","FUNCTORIALITY_SELECTS_REPRESENTATION_CLASS",
         "FUNCTORIALITY_INCONSISTENT_WITH_FROZEN_RETAINED_STRUCTURE","FUNCTORIALITY_ILL_TYPED"}
def canonical_bytes(x):
 return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
def adjudicate(contract,classes,verification):
 if verification.get("status")!="VERIFIED_120_SURVIVORS_120_CLASSES": raise ValueError("verification_status")
 n=verification["equivalence_class_count"]
 verdict="FUNCTORIALITY_SELECTS_REPRESENTATION_CLASS" if n==1 else "FUNCTORIALITY_STILL_NONSELECTIVE" if n>1 else "FUNCTORIALITY_INCONSISTENT_WITH_FROZEN_RETAINED_STRUCTURE"
 r={"schema":"uqcf-v1547-results-v1","verdict":verdict,"survivor_count":verification["survivor_count"],
    "equivalence_class_count":n,"target_equivalence":verification["target_equivalence"],
    "new_assumption":"RETAINED_TO_QUANTUM_FUNCTORIALITY","source_correspondence":"NOT_EVALUATED",
    "physical_source_law_adopted":False,"physical_gravity":False,"einstein_equations":False,
    "continuum_limit":False,"Pillar_3":"OPEN"}
 verify_result(r); return r
def verify_result(r):
 if r.get("verdict") not in ALLOWED: raise ValueError("verdict")
 if r.get("source_correspondence")!="NOT_EVALUATED" or r.get("Pillar_3")!="OPEN": raise ValueError("claim_boundary")
 if any(r.get(k) is not False for k in ("physical_source_law_adopted","physical_gravity","einstein_equations","continuum_limit")): raise ValueError("claim_boundary")
 return True
