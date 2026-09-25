"""v15.56 Task 11: augmented lineage schema sufficiency and ablation.

For identity correspondence, a globally stable full descendant lineage address
under a Genesis provenance anchor separates descendants. Parent, repair index,
and recoverability depth then describe ancestry/history/state but are redundant
for identity if the full child address already encodes its ancestral path.

Thus the five-field schema is sufficient but not minimal.
"""
def classify_augmented():
    return {
      "schema":"uqcf-v1556-augmented-lineage-v1",
      "fields":["genesis_id","parent_address","child_branch_address","repair_index","recoverability_depth"],
      "unique_correspondence":True,
      "primary_verdict":"AUGMENTED_SCHEMA_SUFFICIENT_NOT_MINIMAL",
      "geometry_fields":[],
      "identity_key":["genesis_id","child_branch_address"],
      "ablation":{
        "genesis_id":{"unique":False,"counterexample":"SAME_BRANCH_ADDRESS_DIFFERENT_GENESIS"},
        "parent_address":{"unique":True,"reason":"FULL_CHILD_ADDRESS_ENCODES_ANCESTRAL_PATH"},
        "child_branch_address":{"unique":False,"counterexample":"SIBLING_SWAP"},
        "repair_index":{"unique":True,"reason":"HISTORY_STATE_NOT_NEEDED_FOR_DESCENDANT_IDENTITY"},
        "recoverability_depth":{"unique":True,"reason":"ORDER_DEPTH_NOT_NEEDED_WHEN_FULL_LINEAGE_ADDRESS_IS_STABLE"}
      },
      "minimal_identity_schema":["genesis_id","child_branch_address"],
      "theorem_statement":
        "UNDER_STABLE_GLOBALLY_UNIQUE_LINEAGE_ADDRESSING_WITHIN_A_GENESIS, DESCENDANT_IDENTITY_IS_FIXED_BY_GENESIS_ID_PLUS_FULL_CHILD_BRANCH_ADDRESS"
    }
