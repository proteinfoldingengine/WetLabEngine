"""v15.56 Task 8: Genesis Pin as minimal cross-construction base.

A Genesis Pin is a provenance anchor, but a shared anchor is not implied for
independently presented retained constructions.  Even when the same Pin label
is supplied, comparison requires certified descent/repair maps from that Pin
into each construction.  The Pin alone therefore cannot yet furnish the span.
"""
def classify_genesis_base():
    return {
      "schema":"uqcf-v1556-genesis-base-v1",
      "primary_verdict":"SHARED_PIN_WITNESS_REQUIRED",
      "candidate_role":"COMMON_PROVENANCE_BASE",
      "shared_pin_assumed":False,
      "genesis_pin":None,
      "required_maps":["G_TO_R_m","G_TO_R_n"],
      "required_map_properties":[
        "PROVENANCE_PRESERVING","LINEAGE_PRESERVING",
        "RECOVERABILITY_COMPATIBLE","REPAIR_COMPATIBLE"
      ],
      "external_geometry_used":[],
      "pin_alone_sufficient":False,
      "minimal_sufficient_candidate":
        "GENESIS_PIN_PLUS_CERTIFIED_RETAINED_DESCENT_REPAIR_HISTORY",
      "reason":
        "COMMON_LABEL_OR_FOUNDATIONAL_ROLE_DOES_NOT_ESTABLISH_SHARED_DESCENT"
    }
