"""v15.56 Task 35: intrinsic pruning obstruction class.

Let P_r be the canonical extensive source pushforward and G_f=Delta_f^+ the
fine connected-lineage Green operator. Let Q quotient only the constant
response gauge. Define the intrinsic obstruction map

    O_r := (Q G_f)|_{ker(P_r)}.

It is independent of any response coarse map A_r. By the elementary
factorization theorem, a linear response T=QG_f factors through P_r iff
ker(P_r) subset ker(T), which is exactly O_r=0.

For connected fine graphs, G_f is injective on the zero-mean subspace.
Any nontrivial retraction fiber contains u!=v and x=e_u-e_v, with P_r x=0
and x zero mean. Then G_f x is nonzero and zero mean, hence QG_f x !=0.
Thus O_r is nonzero for every genuine branch-collapsing fiber.
"""
def classify():
 return {
  "schema":"uqcf-v1556-intrinsic-pruning-obstruction-v1",
  "intrinsic_class":"O_r = (Q G_f)|_{ker(P_r)}",
  "independent_of_response_coarse_map":True,
  "vanishes_iff_factorization_possible":True,
  "factorization_equivalence":"O_r=0 iff exists B with B P_r = Q G_f",
  "branch_collapse_status":"NONZERO_FOR_NONTRIVIAL_FIBERS_ON_CONNECTED_GRAPH",
  "canonical_inputs":["P_r","G_f","constant_gauge_quotient_Q"],
  "witness":"x=e_u-e_v for distinct u,v in one pruning fiber",
  "geometry_used":[],
  "scientific_result":"CANONICAL_PRUNING_OBSTRUCTION_MEASURES_FINE_RESPONSE_INFORMATION_ERASED_BY_PRUNING",
  "boundary":"FINITE_CONNECTED_LINEAGE_LINEAR_RESPONSE_SETTING"
 }
