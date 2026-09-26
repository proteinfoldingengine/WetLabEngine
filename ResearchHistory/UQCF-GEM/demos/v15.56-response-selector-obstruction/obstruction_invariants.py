"""v15.56 Task 36: canonical quantitative invariants of intrinsic obstruction.

O_r=(QG_f)|ker(P_r). In the finite connected setting, ker(P_r) lies in the
zero-sum source subspace and G_f is injective there; Q is identity on the
zero-mean Green image. Hence O_r is injective on ker(P_r), so
rank(O_r)=dim ker(P_r).

For a surjective extensive pushforward P_r from n_f identities onto n_c
retained identities, rank(P_r)=n_c and rank-nullity gives
dim ker(P_r)=n_f-n_c. This rank is basis-free and needs no inner product.

For composed surjective pruning f->m->c, ker(P_r) is contained in
ker(P_q P_r), so obstruction rank is monotone, and dimensions satisfy
(n_f-n_c)=(n_f-n_m)+(n_m-n_c).

Singular values, operator norms, and energy magnitudes require chosen inner
products/measures and are therefore not canonical at the present layer.
"""
def classify():
 return {
  "schema":"uqcf-v1556-obstruction-invariants-v1",
  "rank_canonical":True,
  "connected_branch_collapse_rank":"dim ker(P_r)",
  "surjective_rank_formula":"rank(O_r)=dim ker(P_r)=n_f-n_c",
  "kernel_dimension_monotone_under_composed_surjective_pruning":True,
  "composition_dimension_law":"rank(O_{q o r})=(n_f-n_c)=(n_f-n_m)+(n_m-n_c)",
  "singular_spectrum_requires_inner_products":True,
  "operator_norm_requires_inner_products":True,
  "canonical_quantitative_invariant":"OBSTRUCTION_RANK",
  "interpretation":"NUMBER_OF_INDEPENDENT_FINE_SOURCE_DIRECTIONS_ERASED_BY_PRUNING_BUT_RETAINED_BY_FINE_RESPONSE",
  "geometry_used":[],
  "boundary":"RANK_IS_CANONICAL; MAGNITUDE_SPECTRA_ARE_NOT_YET_CANONICAL"
 }
