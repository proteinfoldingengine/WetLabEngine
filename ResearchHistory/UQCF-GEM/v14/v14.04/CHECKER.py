#!/usr/bin/env python3
import json
from pathlib import Path

from provenance_representation_audit import run_audit

r = run_audit()
expected = json.loads(Path(__file__).with_name("SUMMARY.json").read_text())

# Independent scientific thresholds.
assert r["version"] == "v14.04"
assert r["seed"] == 1404
assert r["support_dimension"] == 25
assert r["Pillar_3"] == "OPEN"
assert r["class_a"]["analytic_theorem"] == "SUPPORT_GAUGE_PROJECTIVE_CENTRALITY"
assert r["class_a"]["central_only"] is True
assert r["class_a"]["identity_pgrl_null"] is True
assert r["class_a"]["max_weyl_twirl_error"] < 2e-11
assert r["class_a"]["max_identity_tangent_norm"] < 2e-11
assert r["class_a"]["min_noncentral_orbit_projective_residual"] > 1e-4
assert r["class_b"]["missing_artifact_count"] == 0
assert r["class_b"]["nontrivial_carrier_count"] >= 1
assert r["class_b"]["certified_natural_support_link_count"] in {0, 1}
assert r["class_c"]["declared_intertwiner_count"] >= 2
assert r["class_c"]["max_isometry_error"] < 2e-12
assert r["class_c"]["min_pair_projective_residual"] > 1e-4
assert r["class_c"]["max_hidden_direction_separation"] > 1e-4
assert r["class_c"]["max_boundary_separation"] > 1e-6
assert r["class_c"]["max_dual_ray_separation"] > 1e-6
assert r["gate_outcome"] in {
    "DERIVED_PROVENANCE_SOURCE_RAY",
    "CENTRAL_ONLY_PGRL_NULL",
    "REQUIRES_NEW_REPRESENTATION_LINK",
    "UNRESOLVED_REPRESENTATION_AUDIT",
}

# Frozen discrete scientific record.
for key in ("version", "seed", "support_dimension", "Pillar_3", "scientific_breakthrough", "gate_outcome"):
    assert r[key] == expected[key], (key, r[key], expected[key])

for key in ("analytic_theorem", "central_only", "identity_pgrl_null", "weyl_design_size", "noncentral_probe_count", "unitary_orbit_control_count"):
    assert r["class_a"][key] == expected["class_a"][key], ("class_a", key)

for key in ("candidate_count", "missing_artifact_count", "nontrivial_carrier_count", "certified_natural_support_link_count"):
    assert r["class_b"][key] == expected["class_b"][key], ("class_b", key)

actual_inv = {x["name"]: x for x in r["class_b"]["inventory"]}
frozen_inv = {x["name"]: x for x in expected["class_b"]["inventory"]}
assert set(actual_inv) == set(frozen_inv)
for name in sorted(frozen_inv):
    for key in ("path", "domain_type", "carrier_class", "transformation_law", "support_map_status", "sha256"):
        assert actual_inv[name][key] == frozen_inv[name][key], (name, key)

for key in ("fixture_status", "attempted_seeds", "declared_intertwiner_count", "genuine_projective_ambiguity"):
    assert r["class_c"][key] == expected["class_c"][key], ("class_c", key)


def close(actual, frozen):
    tol = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(float(frozen)))
    return abs(float(actual) - float(frozen)) <= tol

for key in (
    "max_central_invariance_error",
    "max_identity_tangent_norm",
    "max_weyl_twirl_error",
    "min_noncentral_orbit_projective_residual",
):
    assert close(r["class_a"][key], expected["class_a"][key]), ("class_a", key)

for key in (
    "max_isometry_error",
    "min_pair_projective_residual",
    "max_hidden_direction_separation",
    "max_boundary_separation",
    "max_dual_ray_separation",
):
    assert close(r["class_c"][key], expected["class_c"][key]), ("class_c", key)

actual_pairs = {(x["seed_i"], x["seed_j"]): x for x in r["class_c"]["pair_records"]}
frozen_pairs = {(x["seed_i"], x["seed_j"]): x for x in expected["class_c"]["pair_records"]}
assert set(actual_pairs) == set(frozen_pairs)
for pair in sorted(frozen_pairs):
    for key in ("projective_residual", "hidden_direction_separation", "boundary_separation", "dual_ray_separation"):
        assert close(actual_pairs[pair][key], frozen_pairs[pair][key]), (pair, key)

print("V14_04_PROVENANCE_REPRESENTATION_CHECKER_PASS")
print(json.dumps({
    "gate_outcome": r["gate_outcome"],
    "analytic_theorem": r["class_a"]["analytic_theorem"],
    "max_weyl_twirl_error": r["class_a"]["max_weyl_twirl_error"],
    "max_identity_tangent_norm": r["class_a"]["max_identity_tangent_norm"],
    "nontrivial_carrier_count": r["class_b"]["nontrivial_carrier_count"],
    "certified_natural_support_link_count": r["class_b"]["certified_natural_support_link_count"],
    "declared_intertwiner_count": r["class_c"]["declared_intertwiner_count"],
    "min_pair_projective_residual": r["class_c"]["min_pair_projective_residual"],
    "max_hidden_direction_separation": r["class_c"]["max_hidden_direction_separation"],
    "max_boundary_separation": r["class_c"]["max_boundary_separation"],
    "max_dual_ray_separation": r["class_c"]["max_dual_ray_separation"],
}, indent=2, sort_keys=True))
