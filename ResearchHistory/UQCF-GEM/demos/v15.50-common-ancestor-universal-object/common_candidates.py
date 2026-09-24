"""v15.50 Task 2: deterministic target-blind U candidates."""
def enumerate_candidates(contract):
 u=contract["U"]
 # Minimal family: the frozen U plus structurally equivalent reversal of disjoint listing.
 base={"sort":u["sort"],"objects":list(u["objects"]),"relations":list(u["relations"]),
       "composition":[list(x) for x in u["composition"]],"refinement":dict(u["refinement"]),
       "disjoint_composition":[list(x) for x in u["disjoint_composition"]],
       "pair_object":False}
 alt={**base,"disjoint_composition":list(reversed(base["disjoint_composition"]))}
 return (base,alt)

def check_target_blindness(contract,u):
 if u.get("pair_object"): return {"status":"PAIR_OBJECT_REJECTED"}
 if any(k in u for k in ("quantum_labels","node_site_dictionary","hilbert_dimension")):
  return {"status":"TARGET_LABEL_CONTAMINATION"}
 if any(k in u for k in ("curvature","geometry","source_response","gravity","physical_time")):
  return {"status":"DOWNSTREAM_CONTAMINATION"}
 allowed={"sort","objects","relations","composition","refinement","disjoint_composition","pair_object"}
 if set(u)-allowed: return {"status":"UNDECLARED_FIELD"}
 return {"status":"TARGET_BLIND_PASS"}
