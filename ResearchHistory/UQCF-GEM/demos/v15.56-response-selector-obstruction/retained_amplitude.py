"""v15.56 Task 22: localized retained source grade.

v13.26 preserves a protected retained source grading: relative/extensive source
amount g_ret is earned on the retained side, while absolute observer
normalization has an irreducible positive rescaling freedom. Combining that
earned grade with v15.56 typed localization yields a retained source field
J_s(k)=g_ret(s) delta_{k,k(s)}. This is a retained/projective construction, not
an observer stress-energy calibration.
"""
def classify():
    return {
      "schema":"uqcf-v1556-retained-amplitude-v1",
      "relative_retained_grade_earned":True,
      "prior_evidence":"ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
      "localized_source_form":"J_s = g_ret(s) delta_{k,k(s)}",
      "localization_key":"k(s)=(genesis_id,full_lineage_address)",
      "absolute_observer_scale_earned":False,
      "positive_rescaling_freedom":True,
      "rescaling":"g_ret -> a g_ret, a>0",
      "projective_source_class_earned":True,
      "geometry_used":[],
      "scientific_result":"LOCALIZATION_PLUS_RELATIVE_RETAINED_AMPLITUDE_DEFINE_A_NATIVE_PROJECTIVE_SOURCE_FIELD",
      "next_gate":"TEST_PROJECTIVE_POISSON_RESPONSE_DELTA_LIN_PHI_EQUALS_CENTERED_J"
    }
