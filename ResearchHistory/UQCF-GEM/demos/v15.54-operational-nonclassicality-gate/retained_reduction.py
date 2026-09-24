"""Target-blind retained reduction for v15.54."""
def reduce_to_retained(contract,candidate):
 # Frozen coarse retained skeleton. Operational probabilities, candidate ID,
 # carrier size, and target structure are deliberately not retained.
 return {
  "object_count":4,
  "lineage_incidence":[[0,1],[0,2],[1,3],[2,3]],
  "dependency_incidence":[[0,1],[0,2],[1,3],[2,3]],
  "recoverability_relation":[[0,1],[0,2],[1,3],[2,3]],
  "composition_table":[[0,1,3],[0,2,3]],
  "refinement_diagram":[[[0,1],[1,3]],[[0,2],[2,3]]],
  "disjoint_partition":[[0,1],[2,3]],
 }
