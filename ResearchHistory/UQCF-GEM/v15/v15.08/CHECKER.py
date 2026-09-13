#!/usr/bin/env python3
import json
from genesis_source_semantics_audit import adjudicate_gate, run_audit

assert adjudicate_gate(True, False) == "GENESIS_PROVENANCE_DOES_NOT_IDENTIFY_NEUTRAL_PREPARATION_SOURCE"
assert adjudicate_gate(False, True) == "FROZEN_GENESIS_IDENTIFIES_NEUTRAL_PREPARATION_SOURCE"
assert adjudicate_gate(False, False) == "V15_08_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.08 adjudications must raise")

s = run_audit()
assert s["version"] == "v15.08"
assert s["primary_outcome"] == "GENESIS_PROVENANCE_DOES_NOT_IDENTIFY_NEUTRAL_PREPARATION_SOURCE"
assert s["secondary_outcome"] == "SOURCE_SEMANTICS_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY"
assert s["tertiary_outcome"] == "LOG_PROJECTIVE_SOURCE_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

p = s["genesis_pin_semantics"]
assert p["history_legitimacy_certified"] is True
assert p["quantum_neutral_reference_identified"] is False
assert p["neutral_preparation_generator_identified"] is False

r = s["source_role_semantics"]
assert r["ternary_role_count"] == 3
assert r["role_to_hermitian_generator_map_found"] is False
assert r["role_to_spectral_response_law_found"] is False

n = s["independence_no_go"]
assert n["same_frozen_provenance_supports_multiple_source_laws"] is True
assert n["min_pairwise_source_ray_separation"] > 1e-2
assert n["canonical_log_ray_matches_v15_07_generator"] < 1e-11
assert n["provenance_only_noncentral_map_blocked_by_v14_04"] is True

f = s["frozen_dependency_audit"]
assert f["archive_bindings_match_expected"] is True
assert f["source_equals_neutral_preparation_axiom_found"] is False
assert f["genesis_equals_maximally_mixed_state_axiom_found"] is False

c = s["claim_boundary"]
assert c["canonical_log_generator_preserved"] is True
assert c["canonical_log_generator_identified_as_source"] is False
assert c["new_source_semantics_axiom_required"] is True
assert c["branch_stop_relative_to_frozen_ontology"] is True
assert c["downstream_gravity_used_as_selector"] is False
assert c["entropy_or_time_used_as_selector"] is False
assert c["Pillar_3_closed"] is False

print(json.dumps(s, indent=2, sort_keys=True))
