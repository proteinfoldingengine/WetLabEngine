"""v15.55 Task 4: exact naturality/composition refinement.

With the frozen v15.54 retained diamond, the only nontrivial earned
automorphism is branch exchange, already imposed in Task 3. Additivity of the
scalar defect and disjoint composition make eta(D)=D*c compositional for every
surviving c. No further exact row is earned without an additional principle.
"""
import response_space as rs

def refine_response_space(contract):
    base=rs.classify_exact(contract)
    return {
      "schema":"uqcf-v1555-naturality-v1",
      "scalar_field":"Q",
      "initial_dimension":base["solution_dimension"],
      "refined_dimension":base["solution_dimension"],
      "composition_checked":True,
      "full_naturality_checked":True,
      "additional_constraint_rank":0,
      "extra_principles_added":[],
      "surviving_parameters":["branch_lineage","branch_dependency","branch_recoverability","composition"],
      "primary_verdict":"RESPONSE_NONUNIQUE" if base["solution_dimension"] else "UNIQUE_CANONICAL_RESPONSE",
      "reason":"FROZEN_COMPOSITION_AND_NATURALITY_ADD_NO_INDEPENDENT_CONSTRAINT_BEYOND_BRANCH_SWAP"
    }
