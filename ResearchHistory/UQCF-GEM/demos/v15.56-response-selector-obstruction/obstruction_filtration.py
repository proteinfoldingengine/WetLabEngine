"""v15.56 Task 37: canonical filtration from ordered pruning.

Let P_{i->j} be the functorial extensive source pushforward for an ordered
sequence of surjective pruning maps V_0->V_1->...->V_m. Pull every loss
subspace back to the initial source space and define
K_j = ker(P_{0->j}).

Because P_{0->j+1}=P_{j->j+1} P_{0->j}, K_j subset K_{j+1}. Thus the pruning
history canonically defines a filtration 0 subset K_1 subset ... subset K_m.
It is strict exactly when the next pruning erases at least one additional
independent source direction.

The jth associated graded piece is K_j/K_{j-1}. For finite surjective maps,
dim K_j=n_0-n_j, so dim(K_j/K_{j-1})=n_{j-1}-n_j.

This filtration retains the order at which distinctions become unrecoverable,
not merely the final total dimension loss. No external time coordinate or
geometry is introduced.
"""
def classify():
 return {
  "schema":"uqcf-v1556-obstruction-filtration-v1",
  "kernel_flag_canonical":True,
  "filtration":"0 subset K_1 subset K_2 subset ... subset K_m; K_j=ker(P_{0->j})",
  "strict_when_each_step_prunes_new_direction":True,
  "graded_piece":"ker(P_{0->k}) / ker(P_{0->k-1})",
  "graded_dimension":"n_{k-1}-n_k",
  "order_information_retained":True,
  "external_time_used":False,
  "geometry_used":[],
  "scientific_result":"ORDERED_PRUNING_CANONICALLY_DEFINES_A_FILTRATION_OF_IRRECOVERABLE_SOURCE_DIRECTIONS",
  "boundary":"FINITE_SURJECTIVE_RETAINED_PRUNING_SEQUENCE"
 }
