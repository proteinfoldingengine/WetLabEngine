#!/usr/bin/env python3
import json
from pathlib import Path

from graph_site_source_audit import run_audit

r = run_audit()

# Independent scientific/structural thresholds remain primary checks.
assert r["version"] == "v15.03"
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["source_fixture"]["incidence_rank"] == 4
assert r["source_fixture"]["cycle_dimension"] == 3
assert r["dimension_theorem"]["compatibility_parent_dimension"] == 125
assert r["dimension_theorem"]["five_nontrivial_factorization_possible"] is False
assert r["dimension_theorem"]["solution_count"] == 0
assert r["centrality_theorem"]["analytic_classification"] == "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER"
assert r["centrality_theorem"]["pgrl_classification"] == "CENTRAL_PGRL_NULL"
assert r["centrality_controls"]["identity_invariance_error"] < 2e-12
assert r["centrality_controls"]["noncentral_independent_frame_violation"] > 1e-6
assert r["centrality_controls"]["swap_independent_frame_violation"] > 1e-6
assert r["centrality_controls"]["swap_tied_frame_error"] < 2e-12
assert r["state_dependent_controls"]["classification"] == "SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION"
assert r["state_dependent_controls"]["constant_family_max_norm"] < 2e-12
assert r["state_dependent_controls"]["max_covariance_error"] < 2e-10
assert r["state_dependent_controls"]["max_positive_scale_projective_residual"] < 2e-12
assert r["state_dependent_controls"]["family_status"] == "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
assert r["archive_graph_site_audit"]["factorization_status"] == "GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED"
assert r["archive_graph_site_audit"]["exact_graph_site_factorization_certified"] is False
assert r["archive_graph_site_audit"]["natural_map_to_compatibility_parent_certified"] is False
assert r["gate_outcome"] == "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION"
assert r["scientific_breakthrough"] is False
assert r["Pillar_3"] == "OPEN"

# Freeze the entire measured result. Numeric comparisons tolerate only normal
# machine-level variation; categorical, hash, path, and structural data are exact.
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
print("V15_03_GRAPH_SITE_SOURCE_LIFT_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
