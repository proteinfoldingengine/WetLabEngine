"""v15.56 Task 28: lawful pruning morphism from full lineage addresses.

For a fine prefix-addressed lineage set K_f and a nonempty prefix-closed
retained subset K_c containing the Genesis/root address, every fine address k
has a unique longest prefix in K_c.  Retraction r(k) to that prefix is canonical,
identity on K_c, ancestry-respecting, and idempotent.  This is a structural
pruning map, not geometric nearest-neighbor coarse graining.

A localized source either survives at its key or, if its key is pruned, its
identity can be pushed to the nearest retained ancestor. Whether its extensive
grade should be summed with other fibers is a separate source-pushforward law
to test next.
"""
def classify():
    return {
      "schema":"uqcf-v1556-pruning-morphism-v1",
      "domain":"PREFIX_CLOSED_RETAINED_LINEAGE_SETS",
      "canonical_map":"ANCESTOR_RETRACTION_TO_NEAREST_RETAINED_PREFIX",
      "rule":"r(k)=longest_prefix_of_k_in_K_coarse",
      "requires_root_retained":True,
      "identity_on_coarse_set":True,
      "ancestry_respecting":True,
      "idempotent":True,
      "surjective_onto_coarse_set":True,
      "source_cases":["SOURCE_SURVIVES","SOURCE_PRUNED_TO_RETAINED_ANCESTOR"],
      "geometry_used":[],
      "not_yet_earned":[
        "EXTENSIVE_SOURCE_PUSHFORWARD_OVER_RETRACTION_FIBERS",
        "SCALAR_FIELD_COARSE_GRAINING",
        "LAPLACIAN_INTERTWINING"
      ],
      "scientific_result":"FULL_LINEAGE_ADDRESSING_CANONICALLY_SUPPLIES_THE_VERTEX_LEVEL_PRUNING_RETRACTION"
    }
