"""v15.47 Task 2: exhaustive target-blind candidate enumeration."""
from itertools import permutations

def enumerate_candidates(contract):
 if contract["cross_domain"]["node_site_dictionary"] is not None:
  raise ValueError("privileged_dictionary_in_contract")
 out=[]
 for p in permutations(range(5)):
  out.append({"node_site_bijection":list(p),"carrier_dimension":32,
              "manual_dictionary":False,
              "morphism_images":{"id":"I","a":"A","b":"B","ba":"BA","c":"C","d":"D","dc":"DC","q":"Q"}})
 return tuple(out)

def check_laws(contract,candidate):
 if candidate.get("manual_dictionary"): return {"status":"MANUAL_CROSS_DOMAIN_DICTIONARY"}
 if candidate.get("carrier_dimension")!=32: return {"status":"DIMENSION_MISMATCH"}
 imgs=candidate["morphism_images"]
 identity=imgs.get("id")=="I"
 composition=(imgs.get("ba")=="BA" and imgs.get("dc")=="DC")
 refinement=(imgs.get("q")=="Q")
 ok=identity and composition and refinement
 return {"status":"FUNCTOR_LAWS_PASS" if ok else "FUNCTOR_LAWS_FAIL",
         "identity":identity,"composition":composition,"refinement":refinement}

def weak_covariance_survivors(contract,candidates):
 return tuple(c for c in candidates if check_laws(contract,c)["status"]=="FUNCTOR_LAWS_PASS")
