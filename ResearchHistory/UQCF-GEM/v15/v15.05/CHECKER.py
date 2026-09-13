#!/usr/bin/env python3
import json

from composition_selector_audit import adjudicate_gate, run_audit

EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.04/REPORT.md": "e857d81f58a540833a7672fe769b2a301bad4459",
    "ResearchHistory/UQCF-GEM/v13/v13.22/REPORT.md": "e6920facaa4d133e2767951612c608d0e514806c",
    "ResearchHistory/UQCF-GEM/v13/v13.23/REPORT.md": "1162d8f8378cb5292d6c2f8526dd5bd53198d2c4",
    "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md": "9917085b211ca0e1f4737082227f55097cc72b66",
    "ResearchHistory/UQCF-GEM/v14/v14.03/REPORT.md": "03d5e8df43d1f163901d33b1182fbfd3f21b626a",
    "ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md": "6c3aed73c63c9c7554107d163e15b8fae7549c1c",
    "ResearchHistory/UQCF-GEM/v15/v15.04/REPORT.md": "9a6a289cc5471def4c4d4f86756c3183802d1cc4",
    "ResearchHistory/UQCF-GEM/v15/v15.04/SUMMARY.json": "a2c4cf211e625dfb3a7673fd7d6c008e382e3d8d",
}

# Adjudication must never infer the opposite scientific result merely because
# a verification path failed.
assert adjudicate_gate(True, False) == "FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE"
assert adjudicate_gate(False, True) == "FROZEN_COMPOSITION_LAW_SELECTS_UNIQUE_SPECTRAL_RESPONSE"
assert adjudicate_gate(False, False) == "V15_05_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.05 adjudications must raise")

s = run_audit()

assert s["version"] == "v15.05"
assert s["gate"] == "Frozen Composition-Law Audit / Monoidal Non-Selection and Log-Selector Boundary"
assert s["primary_outcome"] == "FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE"
assert s["secondary_outcome"] == "LOG_SHAPE_REQUIRES_NEW_FUNCTIONAL_CALCULUS_ASSUMPTION"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

frozen = s["frozen_dependency_audit"]
assert frozen["classification"] == "NO_FROZEN_STATE_TO_SOURCE_COMPOSITION_SELECTOR"
assert frozen["archive_bindings"] == EXPECTED_BINDINGS
assert frozen["v13_04_polar_tensor_naturality"]["selects_state_to_source_response"] is False
assert frozen["v13_22_refinement_naturality"]["source_rule"] == "SUPPLIED_P_TO_P_TENSOR_I"
assert frozen["v13_22_refinement_naturality"]["state_to_source_functional_equation"] is False
assert frozen["v13_22_refinement_naturality"]["selects_a_of_r"] is False
assert frozen["v13_23_qrsl"]["status"] == "IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_ONTOLOGY"
assert frozen["v13_26_source_scale"]["absolute_source_scale_selected"] is False
assert frozen["v14_03_projective_source"]["source_ray_is_supplied"] is True
assert frozen["v15_03_log_warning"]["pgrl_log_coordinate_selects_log_source_law"] is False
assert frozen["v15_04_spectral_freedom"]["unique_a_of_r"] is False

mono = s["labeled_monoidal_nonselection"]
assert mono["classification"] == "LABELED_MONOIDAL_COMPOSITION_PRESERVES_ARBITRARY_LOCAL_SPECTRAL_RESPONSE"
assert mono["theorem_scope"] == "LABELED_PRODUCT_STATES_WITH_FIXED_TENSOR_FACTORS"
assert mono["witnesses"] == ["linear", "log", "polynomial"]
assert mono["max_local_covariance_error"] < 1e-12
assert mono["max_associativity_error"] < 1e-12
assert mono["max_swap_naturality_error"] < 1e-12
assert mono["min_pairwise_projective_ray_separation"] > 1e-2
assert mono["all_three_monoidal"] is True
assert mono["all_three_projectively_distinct"] is True

strong = s["stronger_selector_boundary"]
assert strong["classification"] == "CONTINUOUS_UNIVERSAL_SCALAR_FUNCTIONAL_CALCULUS_PLUS_CENTERED_TENSOR_DERIVATION_SELECTS_LOG_SHAPE"
assert strong["status"] == "NEW_ASSUMPTION_NOT_FROZEN"
assert strong["log_centered_tensor_error"] < 1e-12
assert strong["linear_centered_tensor_error"] > 1e-2
assert strong["cubic_centered_tensor_error"] > 1e-2
assert strong["proof"]["centered_tensor_law_implies_scale_independent_pairwise_differences"] is True
assert strong["proof"]["continuity_reduces_multiplicative_cauchy_to_log"] is True
assert strong["proof"]["result"] == "f(x)=alpha*log(x)+beta"
assert strong["proof"]["projective_shape"] == "[log(rho)]"

boundary = s["claim_boundary"]
assert boundary["frozen_monoidal_selector_found"] is False
assert boundary["log_source_law_derived_from_frozen_ontology"] is False
assert boundary["downstream_gravity_used_as_selector"] is False
assert boundary["entropy_or_time_used_as_selector"] is False
assert boundary["new_assumption_needed_for_log_selector"] is True

print(json.dumps(s, indent=2, sort_keys=True))
