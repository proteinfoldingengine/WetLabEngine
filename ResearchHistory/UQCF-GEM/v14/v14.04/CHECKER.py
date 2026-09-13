#!/usr/bin/env python3
import json

from provenance_representation_audit import run_audit

r = run_audit()
assert r["version"] == "v14.04"
assert r["seed"] == 1404
assert r["support_dimension"] == 25
assert r["Pillar_3"] == "OPEN"
assert r["class_a"]["analytic_theorem"] == "SUPPORT_GAUGE_PROJECTIVE_CENTRALITY"
assert r["class_a"]["central_only"] is True
assert r["class_a"]["identity_pgrl_null"] is True
assert r["class_a"]["max_weyl_twirl_error"] < 2e-11
assert r["class_a"]["min_noncentral_orbit_projective_residual"] > 1e-4
assert r["class_b"]["nontrivial_carrier_count"] >= 1
assert r["class_b"]["certified_natural_support_link_count"] in {0, 1}
assert r["class_c"]["declared_intertwiner_count"] >= 2
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
print("V14_04_PROVENANCE_REPRESENTATION_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
