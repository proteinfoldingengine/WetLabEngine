#!/usr/bin/env python3
from common_parent_audit import run_audit

r = run_audit()
assert r["version"] == "v15.01"
assert r["seed"] == 1501
assert r["parent_dimension"] == 125
assert r["support_dimension"] == 25
assert r["Pillar_3"] == "OPEN"

p = r["parent_support"]
assert p["status"] == "COMPATIBILITY_PARENT_SUPPORT_VERIFIED"
assert p["max_isometry_error"] < 2e-11
assert p["max_reconstruction_error"] < 2e-11
assert p["max_projector_idempotence_error"] < 2e-11
assert p["max_compression_covariance_error"] < 2e-10
assert p["max_projective_descent_error"] < 2e-11

inv = r["archive_inventory"]
assert inv["candidate_count"] >= 5
assert inv["missing_artifact_count"] == 0
assert inv["same_parent_source_class_count"] >= 0
assert inv["support_preserving_parent_tangent_count"] >= 0

ctrl = r["positive_control"]
assert ctrl["classification"] == "SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION"
assert ctrl["noncentral_compressed_source"] is True
assert ctrl["nonzero_hidden_component"] is True
assert ctrl["boundary_simple"] is True
assert ctrl["normal_classification"] == "RAY"
assert ctrl["max_parent_support_covariance_error"] < 2e-9
assert ctrl["max_projective_descent_error"] < 2e-11

assert r["gate_outcome"] in {
    "COMMON_PARENT_INDUCES_SOURCE_RAY",
    "COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE",
    "NO_COMMON_PARENT_REPRESENTATION",
    "UNRESOLVED_COMMON_PARENT_AUDIT",
}
print("V15_01_COMMON_PARENT_REPRESENTATION_CHECKER_PASS")
