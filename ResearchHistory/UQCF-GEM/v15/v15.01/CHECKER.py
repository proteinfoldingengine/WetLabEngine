#!/usr/bin/env python3
import json
from pathlib import Path

from common_parent_audit import run_audit

HERE = Path(__file__).resolve().parent
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
assert inv["same_parent_source_class_count"] == 0
assert inv["support_preserving_parent_tangent_count"] == 0

extended = json.loads((HERE / "ARCHIVE_SWEEP.json").read_text())
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

assert r["gate_outcome"] == "NO_COMMON_PARENT_REPRESENTATION"

summary = json.loads((HERE / "SUMMARY.json").read_text())
assert summary["version"] == r["version"]
assert summary["seed"] == r["seed"]
assert summary["gate_outcome"] == r["gate_outcome"]
assert summary["secondary_status"] == p["status"]
assert summary["parent_dimension"] == r["parent_dimension"]
assert summary["support_dimension"] == r["support_dimension"]
assert summary["Pillar_3"] == r["Pillar_3"]
assert summary["scientific_breakthrough"] is False


def bind_close(name, frozen, live):
    frozen = float(frozen)
    live = float(live)
    delta = abs(frozen - live)
    tol = 2e-12 + 2e-12 * max(1.0, abs(frozen), abs(live))
    assert delta <= tol, (
        f"{name}: frozen={frozen:.17g} live={live:.17g} "
        f"delta={delta:.3e} tol={tol:.3e}"
    )


sp = summary["parent_support"]
for key in (
    "max_isometry_error",
    "max_reconstruction_error",
    "max_projector_hermiticity_error",
    "max_projector_idempotence_error",
    "max_compression_covariance_error",
    "max_projective_descent_error",
):
    bind_close(f"parent_support.{key}", sp[key], p[key])

si = summary["archive_inventory"]
assert si["core_candidate_count"] == inv["candidate_count"]
assert si["extended_candidate_count"] == len(extended["candidates"])
assert si["missing_artifact_count"] == inv["missing_artifact_count"]
assert si["same_parent_source_class_count"] == inv["same_parent_source_class_count"]
assert si["support_preserving_parent_tangent_count"] == inv["support_preserving_parent_tangent_count"]

live_hashes = {x["name"]: x["sha256"] for x in inv["inventory"]}
frozen_hashes = {x["name"]: x["sha256"] for x in si["core_candidates"]}
assert frozen_hashes == live_hashes

frozen_ext = {x["name"]: x["git_blob_sha"] for x in si["extended_candidates"]}
live_ext = {x["name"]: x["git_blob_sha"] for x in extended["candidates"]}
assert frozen_ext == live_ext

sc = summary["positive_control"]
for key in (
    "compressed_noncentral_norm",
    "hidden_norm",
    "boundary_radius",
    "max_parent_support_covariance_error",
    "max_projective_descent_error",
    "support_preserving_tangent_leakage",
    "tangent_roundtrip_projective_residual",
):
    bind_close(f"positive_control.{key}", sc[key], ctrl[key])
assert sc["selected_configuration"] == ctrl["selected_configuration"]
assert sc["selected_control"] == ctrl["selected_control"]
assert sc["normal_classification"] == ctrl["normal_classification"]

print("V15_01_COMMON_PARENT_REPRESENTATION_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
