"""v15.56 Task 5: cross-carrier target-functor obstruction.

The v15.45 periodic-square formula defines centered scalar spaces Phi_L^0
objectwise.  No canonical cross-size morphism was earned by that construction.
Padding, interpolation, Fourier restriction, averaging, and nearest-neighbor
maps would each add structure and are therefore not silently selected here.
"""
def classify_target_functor():
    return {
      "schema":"uqcf-v1556-target-functor-v1",
      "primary_verdict":"MISSING_CANONICAL_CROSS_CARRIER_MORPHISM",
      "objects":"CENTERED_PHI_L_FOR_ADMISSIBLE_L",
      "object_dimension":"L^2-1_FOR_ODD_PERIODIC_FORMULA_CARRIERS",
      "cross_carrier_morphism":None,
      "source_cross_carrier_morphism":None,
      "naturality_equation":"T_mn B_m = B_n S_mn",
      "candidate_maps_not_earned":[
        "PADDING","INTERPOLATION","FOURIER_TRUNCATION",
        "BLOCK_AVERAGING","NEAREST_NEIGHBOR","MODE_MATCHING"
      ],
      "forbidden_inputs_used":[],
      "obstruction":
        "OBJECTWISE_PHI_L_DOES_NOT_DEFINE_A_FUNCTOR_WITHOUT_CANONICAL_MORPHISMS",
      "next_required_object":
        "RETAINED_REFINEMENT_OR_COARSENING_MORPHISM_DERIVED_FROM_LINEAGE_RECOVERABILITY"
    }
