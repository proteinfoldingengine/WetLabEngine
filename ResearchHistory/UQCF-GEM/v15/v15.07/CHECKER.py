#!/usr/bin/env python3
import json
from canonical_neutral_reference_audit import adjudicate_gate, run_audit

# Adjudication must not infer an opposite result merely because verification fails.
assert adjudicate_gate(True, False) == "CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED"
assert adjudicate_gate(False, True) == "FROZEN_ONTOLOGY_IDENTIFIES_CANONICAL_GENERATOR_AS_SOURCE"
assert adjudicate_gate(False, False) == "V15_07_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.07 adjudications must raise")

s = run_audit()

assert s["version"] == "v15.07"
assert s["gate"] == "Canonical Neutral Reference / Relative-Density Generator Gate"
assert s["primary_outcome"] == "CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED"
assert s["secondary_outcome"] == "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED"
assert s["tertiary_outcome"] == "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

neutral = s["canonical_neutral_reference"]
assert neutral["classification"] == "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED"
assert neutral["max_commutant_residual"] < 1e-12
assert neutral["max_reference_tensor_error"] < 1e-12
assert neutral["tested_dimensions"] == [2, 3, 4, 5]

relative = s["relative_density_generator"]
assert relative["classification"] == "CANONICAL_RELATIVE_DENSITY_OPERATOR_IS_MULTIPLICATIVE"
assert relative["max_relative_operator_tensor_error"] < 1e-12
assert relative["max_log_tensor_additivity_error"] < 1e-11
assert relative["max_centered_log_identity_error"] < 1e-12
assert relative["max_local_frame_covariance_error"] < 1e-11
assert relative["generator_shape"] == "centered_log_rho"

endpoint = s["neutral_to_state_endpoint"]
assert endpoint["classification"] == "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY"
assert endpoint["status"] == "CONDITIONAL_ON_SOURCE_AS_NEUTRAL_TO_STATE_PREPARATION_GENERATOR"
assert endpoint["max_endpoint_reconstruction_error"] < 1e-11
assert endpoint["max_generator_identity_error"] < 1e-11
assert endpoint["product_endpoint_error"] < 1e-11

boundary = s["source_identification_boundary"]
assert boundary["classification"] == "CANONICAL_OPERATOR_GENERATOR_DOES_NOT_BY_ITSELF_DEFINE_THE_SOURCE"
assert boundary["same_state_multiple_valid_pgrl_generators"] is True
assert boundary["min_pairwise_global_source_ray_separation"] > 1e-2
assert boundary["frozen_source_equals_neutral_relative_generator_axiom_found"] is False

claim = s["claim_boundary"]
assert claim["canonical_neutral_reference_derived"] is True
assert claim["canonical_multiplicative_local_operator_derived"] is True
assert claim["centered_log_generator_derived"] is True
assert claim["log_generator_identified_as_physical_source"] is False
assert claim["new_source_semantics_needed"] is True
assert claim["downstream_gravity_used_as_selector"] is False
assert claim["entropy_or_time_used_as_selector"] is False
assert claim["Pillar_3_closed"] is False

print(json.dumps(s, indent=2, sort_keys=True))
