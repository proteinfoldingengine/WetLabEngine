#!/usr/bin/env python3
import json
from pathlib import Path

from equivariant_source_law_audit import adjudicate_gate, run_audit

# Adjudication semantics: failed verification is unresolved, not evidence for
# the opposite scientific conclusion. A uniqueness outcome requires its own
# positive certificate.
assert adjudicate_gate(freedom_certified=True, unique_selection_certified=False) == (
    "COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM"
)
assert adjudicate_gate(freedom_certified=False, unique_selection_certified=True) == (
    "FROZEN_AXIOMS_SELECT_UNIQUE_SPECTRAL_LAW"
)
assert adjudicate_gate(freedom_certified=False, unique_selection_certified=False) == (
    "V15_04_GATE_UNRESOLVED"
)
try:
    adjudicate_gate(freedom_certified=True, unique_selection_certified=True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.04 outcomes cannot both be certified")

r = run_audit()

# Independent analytic/numerical thresholds remain primary checks.
assert r["version"] == "v15.04"
assert r["theorem"]["classification"] == "LOCAL_UNITARY_EQUIVARIANCE_IMPLIES_SPECTRAL_SOURCE_LAW"
assert r["theorem"]["converse_certified"] is True
assert r["theorem"]["regularity_assumption_required"] is False
assert r["theorem_controls"]["max_commutator_norm"] < 2e-12
assert r["theorem_controls"]["max_covariance_error"] < 2e-12
assert r["theorem_controls"]["max_stabilizer_invariance_error"] < 2e-12
assert r["theorem_controls"]["nonspectral_stabilizer_violation"] > 1e-6
assert r["qubit_corollary"]["classification"] == "QUBIT_EQUIVARIANT_TRACELESS_MAP_IS_RADIAL"
assert r["qubit_corollary"]["max_linear_square_identity_error"] < 2e-12
assert r["qubit_corollary"]["max_log_formula_error"] < 2e-12
assert r["qubit_corollary"]["log_response_nonconstant"] is True
assert r["frozen_axiom_audit"]["classification"] == "FROZEN_SOURCE_AXIOMS_DO_NOT_SELECT_SPECTRAL_RESPONSE_FUNCTION"
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_source_linearity"] is True
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_local_unitary_covariance"] is True
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_positive_projective_source_scaling"] is True
assert r["frozen_axiom_audit"]["max_source_additivity_error"] < 2e-12
assert r["frozen_axiom_audit"]["max_source_homogeneity_error"] < 2e-12
assert r["frozen_axiom_audit"]["max_local_unitary_covariance_error"] < 2e-10
assert r["frozen_axiom_audit"]["max_positive_scale_projective_residual"] < 2e-12
assert r["frozen_axiom_audit"]["max_null_source_norm"] < 2e-12
assert r["frozen_axiom_audit"]["selection_result"] == "NO_UNIQUE_A_OF_R"
assert r["global_ray_controls"]["classification"] == "UNEQUAL_LOCAL_SPECTRA_GENERICALLY_SPLIT_PROJECTIVE_SOURCE_RAYS"
assert r["global_ray_controls"]["A"]["source_support_spectra_unequal"] is True
assert r["global_ray_controls"]["B"]["source_support_spectra_unequal"] is True
assert r["global_ray_controls"]["A"]["linear_log_projective_residual"] > 1e-6
assert r["global_ray_controls"]["B"]["linear_log_projective_residual"] > 1e-6
assert r["global_ray_controls"]["A"]["linear_polynomial_projective_residual"] > 1e-6
assert r["global_ray_controls"]["B"]["linear_polynomial_projective_residual"] > 1e-6
assert r["v1503_binding"]["linear_square_residuals_match_theorem"] is True
assert r["v1503_binding"]["linear_log_residuals_match_theorem"] is True
assert r["gate_outcome"] == "COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM"
assert r["major_structural_result"] is True
assert r["scientific_breakthrough"] is False
assert r["Pillar_3"] == "OPEN"

# Freeze the full measured result. Categorical/hash/path/structural fields are
# exact; numerical diagnostics use the same reproducibility policy as v15.03:
# scientific thresholds are independently enforced above, while archive binding
# tolerates normal machine-level floating variation.
frozen = json.loads((Path(__file__).with_name("SUMMARY.json")).read_text(encoding="utf-8"))


def compare(actual, expected, path="root"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), path
        assert set(actual) == set(expected), (path, set(actual) ^ set(expected))
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        assert isinstance(actual, list), path
        assert len(actual) == len(expected), path
        for i, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, f"{path}[{i}]")
    elif isinstance(expected, bool) or expected is None or isinstance(expected, str):
        assert actual == expected, (path, actual, expected)
    elif isinstance(expected, (int, float)):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), path
        tol = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(float(expected)))
        assert abs(float(actual) - float(expected)) <= tol, (path, actual, expected, tol)
    else:
        assert actual == expected, (path, actual, expected)


compare(r, frozen)
print("V15_04_EQUIVARIANT_SOURCE_LAW_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
