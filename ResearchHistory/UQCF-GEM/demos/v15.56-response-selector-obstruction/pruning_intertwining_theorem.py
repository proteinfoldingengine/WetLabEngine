"""v15.56 Task 33: quotient-factorization obstruction for pruning naturality.

Let V_f be the fine source space modulo constants, P:V_f->V_c the extensive
pruning pushforward, and G_f the fine Green operator. Any all-source coarse
response depending only on PJ factors through the quotient V_f/ker(P).
Therefore a necessary and sufficient condition for a linear factor B with
B P = Q G_f (for a chosen response quotient Q) is ker(P) subset ker(Q G_f).
Equivalently, G_f must not carry a pruned-away source distinction into a
response distinction visible after Q.

For the strongest identity-response quotient Q that removes constants only,
this is stated as invariance/annihilation of ker(P) by G_f modulo constants.
Branch-collapsing retractions generally create nonzero within-fiber contrasts
in ker(P); on a connected graph G_f is invertible on the zero-mean subspace,
so such a nonzero contrast cannot map to a constant. Hence the condition fails
whenever pruning has a fiber containing at least two distinct fine vertices.

This theorem is finite linear algebra. It does not assert continuum gravity.
"""
def classify():
 return {
  "schema":"uqcf-v1556-pruning-intertwining-theorem-v1",
  "scope":"FINITE_CONNECTED_LINEAGE_GRAPHS_LINEAR_ALL_SOURCE_NATURALITY",
  "necessary_condition":"ker(P) invariant under G_f modulo constants",
  "precise_factorization_condition":"ker(P) subset ker(Q G_f)",
  "quotient_factorization_equivalence":True,
  "theorem":"B P = Q G_f exists iff ker(P) subset ker(Q G_f)",
  "connected_green_fact":"G_f is invertible on the zero-mean source subspace",
  "branch_collapse_status":"GENERALLY_VIOLATES_CONDITION",
  "branch_collapse_corollary":"ANY_RETRACTION_FIBER_WITH_TWO_DISTINCT_VERTICES_HAS_A_NONZERO_ZERO_SUM_CONTRAST_x_IN_ker(P); G_f x_IS_NONCONSTANT",
  "geometry_used":[],
  "interpretation":"PRUNING_IDENTIFIES_SOURCE_DISTINCTIONS_THAT_FINE_GREEN_RESPONSE_RETAINS",
  "boundary":"NO_CLAIM_OF_OBSERVER_SPACETIME_OR_CONTINUUM_GRAVITY"
 }
