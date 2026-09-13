#!/usr/bin/env python3
import json

from graph_site_source_audit import run_audit

r = run_audit()
assert r["version"] == "v15.03"
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["dimension_theorem"]["compatibility_parent_dimension"] == 125
assert r["dimension_theorem"]["five_nontrivial_factorization_possible"] is False
assert r["centrality_theorem"]["analytic_classification"] == "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER"
assert r["centrality_controls"]["identity_invariance_error"] < 2e-12
assert r["centrality_controls"]["noncentral_independent_frame_violation"] > 1e-6
assert r["state_dependent_controls"]["classification"] == "SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION"
assert r["Pillar_3"] == "OPEN"
assert r["gate_outcome"] in {
    "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY",
    "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION",
    "GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT",
    "STATE_INDEPENDENT_GRAPH_SOURCE_CENTRAL_PGRL_NULL",
    "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE",
    "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT",
}
print("V15_03_GRAPH_SITE_SOURCE_LIFT_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
