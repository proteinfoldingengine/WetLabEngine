"""v15.56 Task 6 retained lineage/recoverability morphism classification.

The retained formalism supplies lineage/provenance and ordered recoverability
inside a fixed retained construction.  It does not presently identify nodes or
events between independently sized periodic-square formula carriers.  Thus the
preservation axioms constrain any proposed cross-carrier map but do not define
one.  No geometric coarse-graining is substituted.
"""
def classify_retained_morphism():
    return {
      "schema":"uqcf-v1556-retained-morphism-v1",
      "primary_verdict":"NO_RETAINED_CROSS_CARRIER_MORPHISM",
      "derivation_basis":"RETAINED_LINEAGE_RECOVERABILITY_ONLY",
      "source_objects":"RETAINED_CONSTRUCTIONS_R_m",
      "target_objects":"RETAINED_CONSTRUCTIONS_R_n",
      "morphism":None,
      "preservation_requirements":[
        "LINEAGE","RECOVERABILITY_ORDER","PROVENANCE","COMPOSITION"
      ],
      "external_maps_used":[],
      "existing_structure_scope":"INTRA_CONSTRUCTION",
      "missing_structure":
        "CANONICAL_INTER_CONSTRUCTION_IDENTIFICATION_OR_COMMON_ANCESTRAL_REFINEMENT",
      "consequence":
        "PRESERVATION_AXIOMS_ALONE_DO_NOT_SELECT_R_mn",
      "next_gate":
        "TEST_COMMON_ANCESTRAL_REFINEMENT_AS_A_DERIVED_SPAN_NOT_A_DIRECT_MAP"
    }
