#!/usr/bin/env python3
from shared_label_audit import run_audit

r = run_audit()
assert r["version"] == "v15.02"
assert r["permutation_count"] == 120
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["Pillar_3"] == "OPEN"

assert r["scalar_source_controls"]["constant_source_norm"] < 1e-12
assert r["scalar_source_controls"]["max_permutation_covariance_error"] < 2e-12
assert r["scalar_source_controls"]["max_positive_scale_projective_residual"] < 2e-12

for name in ("V_A", "V_B"):
    c = r["compatibility"][name]
    assert c["support_dimension"] == 25
    assert c["parent_dimension"] == 125
    assert c["max_projector_covariance_error"] < 2e-9

assert r["positive_control"]["classification"] == "SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION"
assert r["incompatible_control"]["classification"] == "INCOMPATIBLE_LABEL_ACTION_REJECTED"

assert r["gate_outcome"] in {
    "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY",
    "SHARED_LABEL_IDENTIFICATION_NONUNIQUE",
    "SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE",
    "NO_CERTIFIED_SHARED_LABEL_CARRIER",
    "UNRESOLVED_EQUIVARIANCE_AUDIT",
}
print("V15_02_SHARED_LABEL_EQUIVARIANCE_CHECKER_PASS")
