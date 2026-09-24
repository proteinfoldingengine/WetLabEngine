"""Exhaustive producer adjudication for frozen v15.54 family."""
import json
import operational_family as of
import operational_witness as ow
import classical_comparator as cc
import retained_reduction as rr
import target_equivalence as te

def search_frozen_family(contract):
 family=of.enumerate_raw_candidates(contract)
 admiss=[x for x in family if of.check_admissibility(contract,x)["admissible"]]
 controls={}
 records=[]
 for x in admiss:
  comp=cc.find_classical_comparator(contract,x["operational_table"])
  wit=ow.evaluate_witness(contract,x)
  red=rr.reduce_to_retained(contract,x)
  key=te.canonical_class_key(contract,x)
  records.append((x,comp,wit,red,key))
  if x["control_role"]!="OPERATIONAL_CANDIDATE": controls[x["control_role"]]=comp["status"]
 verdict="NO_NONCLASSICAL_WITNESS_IN_FROZEN_FAMILY"; witness=None
 for x,comp,wit,red,key in records:
  if not wit["passes"]: continue
  for y,ycomp,ywit,yred,ykey in records:
   if x is y: continue
   same=json.dumps(red,sort_keys=True)==json.dumps(yred,sort_keys=True)
   distinct=key!=ykey
   if same and distinct:
    if comp["status"]=="NO_COMPARATOR_IN_FROZEN_CLASS":
     verdict="CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION"
    else: verdict="OBSTRUCTION_PRESENT_BUT_CLASSICALLY_REPRODUCIBLE"
    witness={"candidate":x["id"],"comparator_target":y["id"],"same_retained_readout":same,"distinct_target_classes":distinct,"operational_witness_passes":wit["passes"],"operational_score":wit["score"],"classical_comparator_status":comp["status"]}
    break
  if witness: break
 return {"schema":"uqcf-v1554-producer-result-v1","primary_verdict":verdict,"candidate_count":len(family),"admissible_count":len(admiss),"target_class_count":len({r[4] for r in records}),"retained_fiber_count":len({json.dumps(r[3],sort_keys=True) for r in records}),"controls":controls,"witness":witness,"classical_ontic_bound":contract["classical_ontic_bound"],"source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN","universal_quantum_derivation":False,"physical_gravity":False}
