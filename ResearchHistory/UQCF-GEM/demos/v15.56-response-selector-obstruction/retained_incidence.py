"""v15.56 Task 15: classify incidence relations on the native identity set.

A full lineage address canonically determines its immediate prefix parent
(provided the parent is retained), so parent-child incidence is intrinsic to
the retained identity/address structure. Repair succession and recoverability
cover require the corresponding history/order data. Dependency is not encoded
by identity keys alone.
"""
def classify():
    relations=[
      {"name":"PARENT_CHILD_LINEAGE","status":"INTRINSIC",
       "rule":"EDGE(parent_prefix(k),k)_WHEN_PARENT_RETAINED",
       "requires":["FULL_LINEAGE_ADDRESS"]},
      {"name":"REPAIR_SUCCESSION","status":"CONDITIONAL",
       "rule":None,"requires":["CERTIFIED_REPAIR_HISTORY"]},
      {"name":"RECOVERABILITY_COVER","status":"CONDITIONAL",
       "rule":None,"requires":["RECOVERABILITY_PARTIAL_ORDER"]},
      {"name":"DEPENDENCY","status":"NOT_DEFINED_ON_IDENTITY_SET",
       "rule":None,"requires":["SEPARATE_DEPENDENCY_RELATION"]}
    ]
    return {
      "schema":"uqcf-v1556-retained-incidence-v1",
      "candidates":[x["name"] for x in relations],
      "relations":relations,
      "selected_by_operator_goal":False,
      "geometry_used":[],
      "canonical_identity_level_incidence":"PARENT_CHILD_LINEAGE",
      "orientation":"PARENT_TO_CHILD",
      "next_operator_candidate":"UNWEIGHTED_LINEAGE_INCIDENCE_B_AND_BtB",
      "boundary":"NO_CLAIM_THAT_LINEAGE_LAPLACIAN_EQUALS_V1545_OPERATOR"
    }
