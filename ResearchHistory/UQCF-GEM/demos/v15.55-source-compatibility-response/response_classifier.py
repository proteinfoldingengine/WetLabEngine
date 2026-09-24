"""v15.55 Task 1 interface only.

Scientific classification is intentionally unavailable until the defect datum D
and exact response constraint system are derived in later tasks.
"""
def classify_response_space(contract):
    required={"schema","input_basis","response_target","axioms","allowed_verdicts",
              "exact_arithmetic_required","post_result_selection_forbidden"}
    if not isinstance(contract,dict) or set(contract)!=required:
        return {"primary_verdict":"ILL_TYPED_RESPONSE_PROBLEM","stage":"CONTRACT_ONLY"}
    if contract["exact_arithmetic_required"] is not True or contract["post_result_selection_forbidden"] is not True:
        return {"primary_verdict":"ILL_TYPED_RESPONSE_PROBLEM","stage":"CONTRACT_ONLY"}
    return {"primary_verdict":"ILL_TYPED_RESPONSE_PROBLEM","stage":"DEFECT_NOT_YET_DERIVED"}
