#!/usr/bin/env python3
import json
import math
from pathlib import Path

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


def summary_view(live: dict) -> dict:
    f = live["frozen_dependency_audit"]
    p = live["genesis_pin_semantics"]
    r = live["source_role_semantics"]
    n = live["independence_no_go"]
    return {
        "version": live["version"],
        "gate": live["gate"],
        "primary_outcome": live["primary_outcome"],
        "secondary_outcome": live["secondary_outcome"],
        "tertiary_outcome": live["tertiary_outcome"],
        "major_structural_result": live["major_structural_result"],
        "scientific_breakthrough": live["scientific_breakthrough"],
        "Pillar_3": live["Pillar_3"],
        "frozen_dependency_audit": {
            "archive_bindings": f["archive_bindings"],
            "archive_bindings_match_expected": f["archive_bindings_match_expected"],
            "classification": f["classification"],
            "genesis_equals_maximally_mixed_state_axiom_found": f["genesis_equals_maximally_mixed_state_axiom_found"],
            "source_equals_neutral_preparation_axiom_found": f["source_equals_neutral_preparation_axiom_found"],
        },
        "genesis_pin_semantics": {
            "classification": p["classification"],
            "history_legitimacy_certified": p["history_legitimacy_certified"],
            "quantum_neutral_reference_identified": p["quantum_neutral_reference_identified"],
            "neutral_preparation_generator_identified": p["neutral_preparation_generator_identified"],
        },
        "source_role_semantics": {
            "classification": r["classification"],
            "ternary_role_count": r["ternary_role_count"],
            "role_to_hermitian_generator_map_found": r["role_to_hermitian_generator_map_found"],
            "role_to_spectral_response_law_found": r["role_to_spectral_response_law_found"],
            "generator_compatibility_is_identity_selection": r["generator_compatibility_is_identity_selection"],
        },
        "independence_no_go": {
            "classification": n["classification"],
            "same_frozen_provenance_supports_multiple_source_laws": n["same_frozen_provenance_supports_multiple_source_laws"],
            "common_provenance_signature": n["common_provenance_signature"],
            "candidate_source_laws": n["candidate_source_laws"],
            "pairwise_source_ray_separations": n["pairwise_source_ray_separations"],
            "min_pairwise_source_ray_separation": n["min_pairwise_source_ray_separation"],
            "canonical_log_ray_matches_v15_07_generator": n["canonical_log_ray_matches_v15_07_generator"],
            "max_trace_error": n["max_trace_error"],
            "min_output_eigenvalue": n["min_output_eigenvalue"],
            "provenance_only_noncentral_map_blocked_by_v14_04": n["provenance_only_noncentral_map_blocked_by_v14_04"],
        },
        "claim_boundary": live["claim_boundary"],
        "stop_rule": live["stop_rule"],
    }


def assert_archive_equal(actual, expected, path="$"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), f"{path}: expected dict"
        assert set(actual) == set(expected), f"{path}: key mismatch"
        for key in expected:
            assert_archive_equal(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        assert isinstance(actual, list), f"{path}: expected list"
        assert len(actual) == len(expected), f"{path}: length mismatch"
        for idx, (a_item, e_item) in enumerate(zip(actual, expected)):
            assert_archive_equal(a_item, e_item, f"{path}[{idx}]")
        return
    if isinstance(expected, bool) or expected is None or isinstance(expected, (str, int)):
        assert actual == expected, f"{path}: {actual!r} != {expected!r}"
        return
    if isinstance(expected, float):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), f"{path}: expected numeric"
        assert math.isfinite(float(actual)) and math.isfinite(expected), f"{path}: non-finite value"
        tolerance = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(expected))
        assert abs(float(actual) - expected) <= tolerance, (
            f"{path}: numeric mismatch {actual!r} vs {expected!r}, tol={tolerance}"
        )
        return
    raise TypeError(f"{path}: unsupported archive type {type(expected)!r}")

frozen_summary = json.loads(Path("SUMMARY.json").read_text())
assert_archive_equal(summary_view(s), frozen_summary)

print(json.dumps(s, indent=2, sort_keys=True))
