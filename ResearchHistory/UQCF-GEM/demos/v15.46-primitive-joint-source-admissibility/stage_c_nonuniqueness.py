"""Stage C3: exact two-sort nonuniqueness witness."""
def find_witness(contract):
 if contract["cross_domain_relations"]:
  raise ValueError("cross_domain_relation_already_supplied")
 if contract["earned_gauge"].get("node_site")!="NONE_CERTIFIED":
  raise ValueError("unexpected_earned_node_site_gauge")
 constraints=list(contract["constraints"])
 reduct={"retained_sort":"FROZEN_PREDECESSOR_STRUCTURE",
         "quantum_carrier_origin":"NOT_DERIVED",
         "cross_domain_relations":[]}
 left=(0,1,2,3,4)
 right=(1,0,2,3,4)
 def side(phi):
  return {"frozen_reduct":reduct,"node_site_bijection":list(phi),
          "constraints":constraints,"added_selector":None}
 return {"schema":"uqcf-v1546-stage-c-witness-v1",
         "status":"INEQUIVALENT_REPRESENTATIONS_FOUND",
         "witness_kind":"TWO_SORT_BIJECTION_EXPANSIONS",
         "left":side(left),"right":side(right),
         "gauge_test":{"earned_node_site_gauge":"NONE_CERTIFIED",
                       "related_by_earned_gauge":False},
         "interpretation":"SAME_FROZEN_REDUCT_ADMITS_DISTINCT_CROSS_DOMAIN_EXPANSIONS"}
