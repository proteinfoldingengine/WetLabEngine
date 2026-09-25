"""v15.56 Task 27: classify refinement naturality of rooted Green response.

The current stack earns identity correspondence on shared lineage keys and an
intrinsic parent-child graph inside each retained construction.  It does not yet
define a lawful refinement/coarsening morphism that specifies how new/removed
vertices, edges, sources, and scalar fields are pushed or pulled while
intertwining the two lineage Laplacians.  Therefore a commutation claim for
rooted Green response cannot yet be typed, let alone proved.  This is a precise
map-class obstruction, not evidence of failure of naturality.
"""
def classify():
    return {
      "schema":"uqcf-v1556-refinement-naturality-v1",
      "object":"ROOTED_PROJECTIVE_GREEN_RESPONSE",
      "requires_lineage_preserving_refinement":True,
      "primary_verdict":"REFINEMENT_MAP_CLASS_UNDERSPECIFIED",
      "geometry_used":[],
      "available":[
        "PARTIAL_BIJECTION_ON_SHARED_LINEAGE_KEYS",
        "INTRINSIC_PARENT_CHILD_INCIDENCE_WITHIN_EACH_CONSTRUCTION",
        "ROOTED_PROJECTIVE_GREEN_RESPONSE"
      ],
      "missing":[
        "LAWFUL_REFINEMENT_MAP_ON_VERTICES_AND_EDGES",
        "SOURCE_PUSHFORWARD_OR_PULLBACK_RULE",
        "SCALAR_FIELD_RESTRICTION_OR_AGGREGATION_RULE_ON_REMOVED_KEYS",
        "LAPLACIAN_INTERTWINING_CONDITION"
      ],
      "candidate_naturality_equation":"R Delta_fine^+ J_fine ~ Delta_coarse^+ J_coarse",
      "scientific_result":"FIXED_GRAPH_SIGNAL_EARNED; CROSS_REFINEMENT_NATURALITY_NOT_YET_TYPED"
    }
