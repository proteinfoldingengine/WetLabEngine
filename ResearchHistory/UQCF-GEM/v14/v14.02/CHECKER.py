#!/usr/bin/env python3
import json
import math
from pathlib import Path

from dual_normal_audit import run_audit

result = run_audit()

assert result["version"] == "v14.02"
assert result["seed"] == 1402
assert result["survey"]["V_A"]["sample_count"] == 64
assert result["survey"]["V_B"]["sample_count"] == 64
assert result["primary_sample_count"] == 128
assert result["construction"]["uses_full_hidden_kernel"] is True
assert result["construction"]["uses_visualization_section"] is False
assert result["typed_dual_control"] == "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE"
assert result["interior_control"]["classification"] == "NO_BOUNDARY_SELECTOR"
assert result["interior_control"]["minimum_center_eigenvalue"] > 0.0
assert result["synthetic_degenerate_control"]["classification"] == "NONUNIQUE_NORMAL_CONE"
assert result["synthetic_degenerate_control"]["projected_normal_span_rank"] >= 2
assert result["max_boundary_psd_residual"] < 2e-9
assert result["max_support_identity_relative_error"] < 2e-9
assert result["max_basis_invariance_relative_error"] < 2e-9
assert result["zero_projected_normal_count"] == 0

# The executed gate is now frozen: every primary point certified one intrinsic local ray.
assert result["gate_outcome"] == "CANONICAL_DUAL_RAY"
assert result["simple_boundary_count"] == 128
assert result["near_degenerate_boundary_count"] == 0
assert result["nonunique_normal_count"] == 0
assert result["unresolved_numerical_count"] == 0
assert result["normal_cone_rank_histogram"] == {"1": 128}
assert result["source_lift_status"] == "CANONICAL_DUAL_DIRECTION_BUT_SOURCE_LIFT_UNDERIVED"
assert result["Pillar_3"] == "OPEN"

summary = json.loads((Path(__file__).parent / "SUMMARY.json").read_text())


def close(actual, frozen):
    assert math.isclose(float(actual), float(frozen), rel_tol=5e-12, abs_tol=5e-12), (actual, frozen)


assert summary["version"] == result["version"]
assert summary["adjudication"] == result["gate_outcome"]
assert summary["scientific_breakthrough"] == result["scientific_breakthrough"]
assert summary["scope"] == result["claim_scope"]
assert summary["typed_dual_control"] == result["typed_dual_control"]
assert summary["source_lift_status"] == result["source_lift_status"]
assert summary["Pillar_3"] == result["Pillar_3"]

assert summary["construction"]["archived_lab_path"] == result["construction"]["archived_lab_path"]
assert summary["construction"]["uses_full_hidden_kernel"] == result["construction"]["uses_full_hidden_kernel"]
assert summary["construction"]["uses_visualization_section"] == result["construction"]["uses_visualization_section"]
close(result["construction"]["fixed_t"], summary["construction"]["fixed_t"])
close(result["construction"]["max_hidden_basis_hermiticity_residual"], summary["construction"]["max_hidden_basis_hermiticity_residual"])
close(result["construction"]["max_hidden_marginal_null_residual"], summary["construction"]["max_hidden_marginal_null_residual"])

assert summary["survey"]["seed"] == result["seed"]
assert summary["survey"]["primary_sample_count"] == result["primary_sample_count"]
for name in ("V_A", "V_B"):
    frozen = summary["survey"][name]
    live = result["survey"][name]
    for key in (
        "sample_count",
        "hidden_dimension",
        "support_dimension",
        "direction_sha256",
        "simple_boundary_count",
        "near_degenerate_boundary_count",
        "nonunique_normal_count",
        "zero_projected_normal_count",
        "unresolved_numerical_count",
        "normal_cone_rank_histogram",
    ):
        assert live[key] == frozen[key], (name, key, live[key], frozen[key])
    close(live["minimum_center_eigenvalue"], frozen["minimum_center_eigenvalue"])
    close(live["hidden_marginal_residual"], frozen["hidden_marginal_residual"])

aggregate = summary["aggregate"]
for key in (
    "simple_boundary_count",
    "near_degenerate_boundary_count",
    "nonunique_normal_count",
    "zero_projected_normal_count",
    "unresolved_numerical_count",
    "normal_cone_rank_histogram",
):
    assert result[key] == aggregate[key], (key, result[key], aggregate[key])
for key in (
    "minimum_simple_boundary_spectral_gap",
    "max_boundary_psd_residual",
    "max_support_identity_relative_error",
    "max_basis_invariance_relative_error",
):
    close(result[key], aggregate[key])

assert result["objective_independence_control"] == summary["objective_independence_control"]
assert result["interior_control"]["classification"] == summary["interior_control"]["classification"]
assert result["interior_control"]["relative_normal_cone_rank"] == summary["interior_control"]["relative_normal_cone_rank"]
close(result["interior_control"]["minimum_center_eigenvalue"], summary["interior_control"]["minimum_center_eigenvalue"])
for key in ("fixture", "kernel_dimension", "projected_normal_span_rank", "classification", "scientific_evidence"):
    assert result["synthetic_degenerate_control"][key] == summary["synthetic_degenerate_control"][key]

print("V14_02_CONVEX_DUAL_NORMAL_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
