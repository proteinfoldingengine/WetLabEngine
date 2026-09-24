"""Stage C4: independent verification of a representation-nonuniqueness witness."""
def verify_witness(contract,witness):
 left=witness["left"]; right=witness["right"]
 expected=list(contract["constraints"])
 if left.get("constraints")!=expected or right.get("constraints")!=expected:
  raise ValueError("constraint_mismatch")
 if left.get("frozen_reduct")!=right.get("frozen_reduct"):
  raise ValueError("reduct_mismatch")
 reduct=left["frozen_reduct"]
 expected_reduct={"retained_sort":contract["retained_sort"]["status"],
                  "quantum_carrier_origin":contract["quantum_sort"]["carrier_origin"],
                  "cross_domain_relations":contract["cross_domain_relations"]}
 if reduct!=expected_reduct:
  raise ValueError("reduct_mismatch")
 if witness.get("gauge_test",{}).get("earned_node_site_gauge") != contract["earned_gauge"]["node_site"]:
  raise ValueError("gauge_mismatch")
 if left.get("added_selector") is not None or right.get("added_selector") is not None:
  raise ValueError("unearned_selector")
 a=tuple(left["node_site_bijection"]); b=tuple(right["node_site_bijection"])
 if a==b: raise ValueError("not_distinct")
 if sorted(a)!=list(range(len(a))) or sorted(b)!=list(range(len(b))) or len(a)!=len(b):
  raise ValueError("invalid_bijection")
 related=contract["earned_gauge"]["node_site"]!="NONE_CERTIFIED"
 if related: raise ValueError("earned_gauge_relation_requires_explicit_action")
 return {"schema":"uqcf-v1546-stage-c-verification-v1",
         "status":"VERIFIED_INEQUIVALENT_REPRESENTATIONS",
         "same_frozen_constraints":True,"same_frozen_reduct":True,
         "distinct_expansions":True,"related_by_earned_gauge":False,
         "physical_gravity":False,"source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
