#!/usr/bin/env python3
import json
import math
from pathlib import Path

from recoverability_multiplicativity_audit import adjudicate_gate, run_audit

EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.16/REPORT.md": "cf2420b2545f801869a617092f4955b7a57ddc60",
    "ResearchHistory/UQCF-GEM/v13/v13.22/REPORT.md": "e6920facaa4d133e2767951612c608d0e514806c",
    "ResearchHistory/UQCF-GEM/v15/v15.05/REPORT.md": "b191c08c22ded0439cc4c2c125fbccfdb677dcbc",
    "ResearchHistory/UQCF-GEM/v15/v15.05/SUMMARY.json": "7aed8e530edc54c5b3a0b3556b54d72c0f7aa932",
    "Tmp/TOE/Einstein Phase 1/V822_peer_review_packet/V818_THEOREM_SHAPE_ACCESSIBILITY_LAW.md": "a92b414c7394f6db8b85b4e2938ca5011d6ee5a3",
    "Tmp/TOE/Einstein Phase 1/V824_accessibility_curvature_paper_python_proof/accessibility_curvature_proof.py": "01e291fa2c490033bdc91e48f3877d0440343ef1",
}

# A failed verification may not be reinterpreted as the opposite scientific result.
assert adjudicate_gate(True, False) == "MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW"
assert adjudicate_gate(False, True) == "RECOVERABILITY_MULTIPLICATIVITY_SELECTS_LOCAL_SOURCE_LAW"
assert adjudicate_gate(False, False) == "V15_06_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.06 adjudications must raise")

s = run_audit()

assert s["version"] == "v15.06"
assert s["gate"] == "Recoverability Multiplicativity / Scalar-to-Operator Source Boundary"
assert s["primary_outcome"] == "MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW"
assert s["secondary_outcome"] == "LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_WAS_ASSUMED_OR_DEFINED_NOT_DERIVED"
assert s["tertiary_outcome"] == "NEGATIVE_LOG_ROOT_FIDELITY_IS_ADDITIVE_ON_INDEPENDENT_RECOVERY_PAIRS"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

frozen = s["frozen_dependency_audit"]
assert frozen["archive_bindings"] == EXPECTED_BINDINGS
assert frozen["archive_bindings_match_expected"] is True
assert frozen["v13_16"]["root_fidelity_recoverability_bound_present"] is True
assert frozen["v13_16"]["canonical_recovery_map_selected"] is False
assert frozen["v15_05"]["unique_state_to_source_law_selected"] is False
legacy = frozen["legacy_accessibility"]
assert legacy["classification"] == "LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_NOT_FROZEN_DERIVATION"
assert legacy["v818_multiplicativity_statement_is_conditional"] is True
assert legacy["v824_accessibility_is_defined_exponentially"] is True
assert legacy["independent_multiplicativity_derivation_present"] is False

mult = s["exact_recovery_pair_multiplicativity"]
assert mult["classification"] == "ROOT_FIDELITY_MULTIPLIES_ON_INDEPENDENT_RECOVERY_PAIRS"
assert mult["max_root_fidelity_product_error"] < 1e-12
assert mult["max_negative_log_additivity_error"] < 1e-12
assert mult["num_random_controls"] >= 16
assert mult["uses_entropy_or_time"] is False

sector = s["exact_recovery_sector_nonselection"]
assert sector["classification"] == "EXACT_RECOVERY_SCALAR_IS_CONSTANT_ACROSS_ALL_FAITHFUL_LOCAL_QUBIT_SPECTRA"
assert sector["max_exact_recovery_infidelity"] < 1e-12
assert sector["max_product_state_cmi"] < 1e-12
assert sector["tested_radius_min"] < 0.1
assert sector["tested_radius_max"] > 0.9
assert sector["log_response_coefficient_span"] > 1.0
assert sector["min_pairwise_source_ray_separation"] > 1e-2
assert sector["same_recoverability_scalar_multiple_source_rays"] is True

boundary = s["source_type_boundary"]
assert boundary["classification"] == "MULTIPLICATIVE_SCALAR_NEEDS_NEW_MAP_TO_BECOME_OPERATOR_SOURCE"
assert boundary["scalar_is_pair_or_recovery_context_dependent"] is True
assert boundary["state_context_reduces_qubit_operator_freedom_to_a_of_r_A"] is True
assert boundary["exact_recovery_sector_leaves_a_of_r_1_unconstrained"] is True
assert boundary["frozen_natural_scalar_to_operator_selector_found"] is False

claims = s["claim_boundary"]
assert claims["multiplicative_quantum_recovery_scalar_exists"] is True
assert claims["legacy_accessibility_multiplicativity_derived"] is False
assert claims["accessibility_identified_with_root_fidelity"] is False
assert claims["log_rho_source_law_derived"] is False
assert claims["entropy_or_time_used_as_source_selector"] is False
assert claims["downstream_gravity_used_as_selector"] is False
assert claims["Pillar_3_closed"] is False

# Once SUMMARY.json exists, freeze the complete telemetry. Scientific thresholds
# above remain independent of this floating-value reproducibility tolerance.
summary_path = Path("SUMMARY.json")
if summary_path.exists():
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

    assert_archive_equal(s, json.loads(summary_path.read_text()))

print(json.dumps(s, indent=2, sort_keys=True))
