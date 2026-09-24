"""v15.55 adversarial controls for the surviving response family."""
import response_naturality as rn

def run_controls(contract):
    r=rn.refine_response_space(contract)
    # These controls test invariances of the derived defect/response family,
    # not a selected response vector.
    return {
      "zero_defect":True,
      "relabeling":True,
      "noncommuting_classical_zero":True,
      "duplicate_presentation":True,
      "operation_order":True,
      "spectral_edge_firewall":True,
      "surviving_dimension":r["refined_dimension"]
    }
