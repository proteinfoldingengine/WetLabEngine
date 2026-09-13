#!/usr/bin/env python3
from equivariant_source_law_audit import run_audit

r = run_audit()

assert r["version"] == "v15.04"
assert r["theorem"]["classification"] == "LOCAL_UNITARY_EQUIVARIANCE_IMPLIES_SPECTRAL_SOURCE_LAW"
assert r["theorem"]["converse_certified"] is True
assert r["qubit_corollary"]["classification"] == "QUBIT_EQUIVARIANT_TRACELESS_MAP_IS_RADIAL"
assert r["qubit_corollary"]["max_linear_square_identity_error"] < 2e-12
assert r["qubit_corollary"]["log_response_nonconstant"] is True
assert r["frozen_axiom_audit"]["classification"] == "FROZEN_SOURCE_AXIOMS_DO_NOT_SELECT_SPECTRAL_RESPONSE_FUNCTION"
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_source_linearity"] is True
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_local_unitary_covariance"] is True
assert r["frozen_axiom_audit"]["all_tested_response_functions_preserve_positive_projective_source_scaling"] is True
assert r["global_ray_controls"]["classification"] == "UNEQUAL_LOCAL_SPECTRA_GENERICALLY_SPLIT_PROJECTIVE_SOURCE_RAYS"
assert r["global_ray_controls"]["A"]["linear_log_projective_residual"] > 1e-6
assert r["global_ray_controls"]["B"]["linear_log_projective_residual"] > 1e-6
assert r["v1503_binding"]["linear_square_residuals_match_theorem"] is True
assert r["v1503_binding"]["linear_log_residuals_match_theorem"] is True
assert r["gate_outcome"] in {
    "COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM",
    "FROZEN_AXIOMS_SELECT_UNIQUE_SPECTRAL_LAW",
}
assert r["scientific_breakthrough"] is False
assert r["Pillar_3"] == "OPEN"

print("V15_04_EQUIVARIANT_SOURCE_LAW_CHECKER_PASS")
