"""v15.56 Task 16: native lineage graph Laplacian.

For the undirected graph underlying intrinsic parent-child retained incidence,
choose any orientation and let B_lin be its edge-by-vertex incidence matrix.
Delta_lin=B_lin^T B_lin is orientation independent. Standard incidence
identities give symmetry, PSD, constant kernel on each component, relabeling
covariance, and nullity equal to the number of connected components.
"""
def classify():
    return {
      "schema":"uqcf-v1556-lineage-laplacian-v1",
      "operator":"Delta_lin = B_lin^T B_lin",
      "carrier":"Map(K_R,Q)",
      "incidence":"INTRINSIC_PARENT_CHILD_LINEAGE",
      "orientation_independent":True,
      "symmetric":True,
      "positive_semidefinite":True,
      "quadratic_form":"f^T Delta_lin f = ||B_lin f||^2 = sum_edges (f(child)-f(parent))^2",
      "constants_in_kernel":True,
      "relabeling_covariant":True,
      "relabeling_law":"Delta' = P Delta P^T",
      "nullity_theorem":"nullity(Delta_lin)=connected_components",
      "geometry_used":[],
      "equals_v1545_operator_claimed":False,
      "v1545_relation_status":"UNESTABLISHED",
      "scientific_result":"A_CANONICAL_SECOND_DIFFERENCE_OPERATOR_EXISTS_ON_THE_NATIVE_RETAINED_LINEAGE_GRAPH"
    }
