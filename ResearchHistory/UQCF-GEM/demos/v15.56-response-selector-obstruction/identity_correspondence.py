"""v15.56 Task 12: correspondence induced by minimal retained identity key.

Matching equal (genesis_id, full lineage address) defines a canonical partial
bijection on the intersection of keys.  It does not force unmatched descendants
to correspond.  This identity map alone does not act on v15.45 scalar-field
coordinates because those coordinates have not been canonically attached to
retained lineage keys.
"""
def classify():
    return {
      "schema":"uqcf-v1556-identity-correspondence-v1",
      "identity_key":["genesis_id","child_branch_address"],
      "correspondence_kind":"PARTIAL_BIJECTION_ON_SHARED_KEYS",
      "rule":"MATCH_EQUAL_IDENTITY_KEYS_ONLY",
      "unmatched_descendants_preserved":True,
      "forced_total_matching":False,
      "geometry_used":[],
      "scalar_map_earned":False,
      "missing_for_scalar_map":[
        "SCALAR_VALUE_TO_LINEAGE_KEY_ATTACHMENT",
        "CENTERING_COMPATIBILITY_ON_SHARED_AND_UNMATCHED_KEYS"
      ],
      "scientific_conclusion":
        "RETAINED_IDENTITY_CORRESPONDENCE_IS_CANONICAL_ON_SHARED_KEYS_BUT_DOES_NOT_BY_ITSELF_IDENTIFY_PERIODIC_SQUARE_SCALAR_COORDINATES"
    }
