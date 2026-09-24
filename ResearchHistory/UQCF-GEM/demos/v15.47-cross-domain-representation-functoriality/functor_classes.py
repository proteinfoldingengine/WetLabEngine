"""v15.47 Task 3: exact quotient by preregistered target equivalence."""
from math import factorial

def surviving_classes(contract,candidates):
 if contract["target_category"].get("equivalence")!="IDENTITY_ONLY":
  raise ValueError("unearned_target_equivalence")
 cs=list(candidates)
 expected=factorial(5)
 if len(cs)!=expected: raise ValueError("incomplete_candidate_family")
 keys=[tuple(c["node_site_bijection"]) for c in cs]
 if len(set(keys))!=len(keys): raise ValueError("duplicate_candidate")
 expected_set=set(__import__("itertools").permutations(range(5)))
 if set(keys)!=expected_set: raise ValueError("incomplete_candidate_family")
 classes=[ [list(k)] for k in sorted(keys) ]
 return {"schema":"uqcf-v1547-classes-v1","target_equivalence":"IDENTITY_ONLY",
         "survivor_count":len(keys),"equivalence_class_count":len(classes),
         "classes":classes,"source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
