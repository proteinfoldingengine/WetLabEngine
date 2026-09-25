"""v15.56 Task 7 common ancestral refinement span classification.

A common ancestor is meaningful only when the two retained constructions are
known to descend from a shared retained history.  Independently parameterized
periodic-square formula carriers do not carry such a shared lineage witness.
Thus no universal pullback-like ancestral object can be formed from the frozen
data alone.
"""
def classify_span():
    return {
      "schema":"uqcf-v1556-ancestral-span-v1",
      "primary_verdict":"NO_COMMON_ANCESTRAL_SPAN",
      "shape":"R_m <- R_* -> R_n",
      "derivation_basis":"COMMON_RETAINED_LINEAGE",
      "span":None,
      "universal_property_verified":False,
      "external_maps_used":[],
      "missing_witness":"SHARED_RETAINED_HISTORY_OR_COMMON_GENESIS_PIN",
      "reason":
        "FORMULA_CARRIER_SIZE_LABELS_DO_NOT_ESTABLISH_COMMON_DESCENT",
      "scientific_consequence":
        "CROSS_SCALE_COMPARISON_REQUIRES_A_SHARED_PROVENANCE_OBJECT_NOT_MERE_CARRIER_SIZE",
      "next_gate":
        "CLASSIFY_SHARED_GENESIS_PIN_AS_THE_MINIMAL_CROSS_CONSTRUCTION_BASE"
    }
