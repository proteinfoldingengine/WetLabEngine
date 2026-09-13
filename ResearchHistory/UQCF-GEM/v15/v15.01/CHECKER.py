#!/usr/bin/env python3
import json
from pathlib import Path

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

extended = json.loads((Path(__file__).with_name("ARCHIVE_SWEEP.json")).read_text())
assert extended["version"] == "v15.01"
assert len(extended["candidates"]) >= 2
assert all(c["same_parent_source_class"] is False for c in extended["candidates"])

ctrl = r["positive_control"]
assert ctrl["classification"] == "SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION"
assert ctrl["noncentral_compressed_source"] is True
assert ctrl["nonzero_hidden_component"] is True
assert ctrl["boundary_simple"] is True
assert ctrl["normal_classification"] == "RAY"
assert ctrl["max_parent_support_covariance_error"] < 2e-9
assert ctrl["max_projective_descent_error"] < 2e-11
assert ctrl["support_preserving_tangent_leakage"] < 2e-11
assert ctrl["tangent_roundtrip_projective_residual"] < 2e-9

assert r["gate_outcome"] in {
    "COMMON_PARENT_INDUCES_SOURCE_RAY",
    "COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE",
    "NO_COMMON_PARENT_REPRESENTATION",
    "UNRESOLVED_COMMON_PARENT_AUDIT",
}
print("V15_01_COMMON_PARENT_REPRESENTATION_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
