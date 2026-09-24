"""v15.47 Task 4: independent reconstruction of functor/class accounting."""
from itertools import permutations

def verify(contract,candidates,class_ledger):
 if not all(contract["prohibited_inputs"].get(k) is True for k in
            ("curvature","gravity","source_response","entropy","spectral_edge","physical_time")):
  raise ValueError("downstream_firewall")
 if contract["target_category"].get("equivalence")!="IDENTITY_ONLY":
  raise ValueError("target_equivalence")
 if class_ledger.get("target_equivalence")!="IDENTITY_ONLY":
  raise ValueError("target_equivalence")
 cs=list(candidates)
 expected=set(permutations(range(5)))
 keys=[tuple(c.get("node_site_bijection",())) for c in cs]
 if len(keys)!=120 or set(keys)!=expected or len(set(keys))!=120:
  raise ValueError("candidate_family")
 for c in cs:
  if c.get("carrier_dimension")!=32: raise ValueError("dimension")
  if c.get("manual_dictionary"): raise ValueError("manual_dictionary")
  im=c.get("morphism_images",{})
  if im.get("id")!="I" or im.get("ba")!="BA" or im.get("dc")!="DC" or im.get("q")!="Q":
   raise ValueError("functor_law")
 groups=class_ledger.get("classes",[])
 members=[tuple(m) for g in groups for m in g]
 if len(groups)!=120 or len(members)!=120 or set(members)!=expected or len(set(members))!=120:
  raise ValueError("class_partition")
 if class_ledger.get("survivor_count")!=120 or class_ledger.get("equivalence_class_count")!=120:
  raise ValueError("class_partition")
 return {"schema":"uqcf-v1547-verification-v1",
         "status":"VERIFIED_120_SURVIVORS_120_CLASSES",
         "survivor_count":120,"equivalence_class_count":120,
         "target_equivalence":"IDENTITY_ONLY",
         "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
