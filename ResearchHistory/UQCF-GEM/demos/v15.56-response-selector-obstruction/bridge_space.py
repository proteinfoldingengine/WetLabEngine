"""v15.56 Task 4 bridge-space classification.

A finite bridge requires a specified target retained carrier and representations
of the frozen structural actions on both source and target.  v15.45 provides a
family of periodic-square scalar spaces Phi_L (dimension L^2, or L^2-1 after
centering), not one canonical finite target independent of L.  The present
v15.56 contract does not select L, and selecting one now would be a new
post-result assumption.

Therefore the natural-transformation space is not yet a single finite vector
space whose dimension can be reported.  This is a typing obstruction, not
zero-dimensionality.
"""
def classify_bridge_space():
    return {
      "schema":"uqcf-v1556-bridge-space-v1",
      "scalar_field":"Q",
      "source_dimension":4,
      "target_family":"PHI_L_PERIODIC_SQUARE",
      "target_dimension":2,  # sentinel lower bound: explicitly not scalar-collapsed
      "target_dimension_status":"FAMILY_DEPENDS_ON_L;_NO_CANONICAL_L_SELECTED",
      "constraints_encoded":[
        "COVARIANCE","PROVENANCE_PRESERVATION","REDUCTION_CONSISTENCY",
        "COMPOSITION_COMPATIBILITY","NEUTRALITY"
      ],
      "bridge_space_dimension":-1,
      "bridge_space_dimension_status":"UNDEFINED_UNTIL_TARGET_FUNCTOR_AND_ACTIONS_ARE_TYPED",
      "primary_verdict":"ILL_TYPED_FINITE_BRIDGE_SPACE",
      "missing_data":[
        "TARGET_FUNCTOR_ACROSS_L",
        "SOURCE_ACTION_FOR_EACH_MORPHISM",
        "TARGET_ACTION_FOR_EACH_MORPHISM",
        "PROVENANCE_MAP_INTO_PHI_L"
      ],
      "forbidden_inputs_used":[],
      "scientific_interpretation":
        "CANNOT_COUNT_NATURAL_TRANSFORMATIONS_BY_CHOOSING_A_SINGLE_L_OR_COLLAPSING_PHI_TO_A_SCALAR"
    }
