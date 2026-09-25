"""v15.56 Task 23: projective Poisson response on retained lineage.

For each connected lineage component C, Delta_lin has kernel span{1_C}.
Therefore a source J is solvable after canonical component centering
J0=J-component_mean(J). On the zero-mean subspace Delta_lin is positive
definite and has a unique inverse. The response phi=Delta_lin^+ J0 is unique
under zero component mean. Positive source rescaling rescales phi identically,
so response rays/shapes are independent of the unresolved absolute source unit.
"""
def classify():
    return {
      "schema":"uqcf-v1556-projective-poisson-v1",
      "equation":"Delta_lin phi = J - component_mean(J)",
      "rhs_orthogonal_to_kernel":True,
      "solution":"phi = Delta_lin^+ centered(J)",
      "gauge_fix":"zero_mean_on_each_connected_component",
      "unique_after_gauge_fix":True,
      "source_scaling_law":"J->aJ implies phi->a phi modulo kernel",
      "projective_response_shape_scale_invariant":True,
      "energy_identity":"phi^T Delta_lin phi = phi^T centered(J)",
      "geometry_used":[],
      "physical_scope":"NATIVE_RETAINED_LINEAGE_RESPONSE_NOT_OBSERVER_SPACETIME_POISSON_EQUATION",
      "next_gate":"EXECUTABLE_SOURCE_RESPONSE_CONTROLS_ON_NONISOMORPHIC_LINEAGE_TREES"
    }
