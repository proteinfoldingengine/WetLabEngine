#!/usr/bin/env python3
import json
from pathlib import Path

from shared_label_audit import run_audit

r = run_audit()

# Independent scientific / structural thresholds.
assert r["version"] == "v15.02"
assert r["permutation_count"] == 120
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["source_side"]["incidence_rank"] == 4
assert r["source_side"]["cycle_dimension"] == 3
assert r["Pillar_3"] == "OPEN"

assert r["scalar_source_controls"]["constant_source_norm"] < 1e-12
assert r["scalar_source_controls"]["max_permutation_covariance_error"] < 2e-12
assert r["scalar_source_controls"]["max_positive_scale_projective_residual"] < 2e-12
assert r["placement_controls"]["max_allowed_placement_equivariance_error"] < 2e-12
assert r["placement_controls"]["partner_symmetric_action_error"] < 2e-12

for name in ("V_A", "V_B"):
    c = r["compatibility"][name]
    assert c["support_dimension"] == 25
    assert c["parent_dimension"] == 125
    assert c["max_projector_covariance_error"] < 2e-9
    assert c["max_state_covariance_error"] < 2e-9

assert r["identification_orbits"]["partition_size"] == 120
assert sum(x["size"] for x in r["identification_orbits"]["classes"]) == 120
assert r["positive_control"]["classification"] == "SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION"
assert r["positive_control"]["success"] is True
assert r["incompatible_control"]["classification"] == "INCOMPATIBLE_LABEL_ACTION_REJECTED"
assert r["incompatible_control"]["success"] is True

assert r["gate_outcome"] in {
    "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY",
    "SHARED_LABEL_IDENTIFICATION_NONUNIQUE",
    "SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE",
    "NO_CERTIFIED_SHARED_LABEL_CARRIER",
    "UNRESOLVED_EQUIVARIANCE_AUDIT",
}

# Frozen archive binding. Scientific thresholds above remain authoritative;
# this section detects drift between executable result and archived adjudication.
summary = json.loads((Path(__file__).parent / "SUMMARY.json").read_text())


def close(actual, frozen):
    actual = float(actual)
    frozen = float(frozen)
    tol = 1e-12 + 1e-9 * max(1.0, abs(actual), abs(frozen))
    assert abs(actual - frozen) <= tol, (actual, frozen, tol)


assert summary["version"] == r["version"]
assert summary["gate_outcome"] == r["gate_outcome"] == "NO_CERTIFIED_SHARED_LABEL_CARRIER"
assert summary["secondary_status"] == r["secondary_status"]
assert summary["scientific_breakthrough"] == r["scientific_breakthrough"] is False
assert summary["Pillar_3"] == r["Pillar_3"] == "OPEN"
assert summary["claim_scope"] == r["claim_scope"]

sf = summary["source_fixture"]
lf = r["source_fixture"]
for key in ("path", "sha256", "fixture_sha256"):
    assert sf[key] == lf[key], (key, sf[key], lf[key])
assert sf["nodes"] == lf["nodes"]
assert sf["edges"] == lf["edges"]
assert sf["source"] == lf["source"]
assert sf["incidence_rank"] == r["source_side"]["incidence_rank"]
assert sf["cycle_dimension"] == r["source_side"]["cycle_dimension"]
assert sf["graph_automorphism_order"] == r["source_side"]["graph_automorphism_order"]
assert sf["source_stabilizer_order"] == r["source_side"]["source_stabilizer_order"]
assert sf["graph_group_sha256"] == r["source_side"]["graph_group_sha256"]

sc = summary["compatibility"]
for name in ("V_A", "V_B"):
    frozen = sc[name]
    live = r["compatibility"][name]
    for key in (
        "arrangement_group_order",
        "fixed_gauge_group_order",
        "fixed_gauge_group",
        "fixed_gauge_group_sha256",
        "support_dimension",
        "parent_dimension",
    ):
        assert frozen[key] == live[key], (name, key, frozen[key], live[key])
    close(live["max_projector_covariance_error"], frozen["max_projector_covariance_error"])
    close(live["max_state_covariance_error"], frozen["max_state_covariance_error"])

assert sc["common_fixed_gauge_order"] == r["common_fixed_gauge_order"]
assert sc["common_fixed_gauge_group"] == r["common_fixed_gauge_group"]
assert sc["common_group_sha256"] == r["common_group_sha256"]

si = summary["identification_orbits"]
li = r["identification_orbits"]
assert si["permutation_count"] == r["permutation_count"]
assert si["double_coset_count"] == li["double_coset_count"] == 120
assert si["partition_size"] == li["partition_size"] == 120
assert all(x["size"] == si["all_class_sizes"] == 1 for x in li["classes"])
assert si["canonical_up_to_gauge"] == li["canonical_up_to_gauge"] is False
assert si["downstream_projectively_inert"] == li["downstream_projectively_inert"] is False
assert si["classes_sha256"] == li["sha256"]

sd = summary["representation_diagnostics"]
ld = r["representation_diagnostics"]
close(ld["max_identification_projective_residual"], sd["max_identification_projective_residual"])
close(ld["max_factor_projective_residual"], sd["max_factor_projective_residual"])
for name in ("V_A", "V_B"):
    live = ld["by_configuration"][name]
    frozen = sd[name]
    for key, val in frozen["max_identification_residual_by_placement"].items():
        close(live["max_identification_residual_by_placement"][key], val)
    for key, val in frozen["factor_pair_residuals"].items():
        close(live["factor_pair_residuals_first_class"][key], val)
    for key, val in frozen["centered_norms"].items():
        close(live["centered_norms_first_class"][key], val)

for key, val in summary["scalar_source_controls"].items():
    close(r["scalar_source_controls"][key], val)
for key, val in summary["placement_controls"].items():
    close(r["placement_controls"][key], val)

cc = summary["current_control"]
lc = r["current_control"]
assert cc["scientific_evidence"] == lc["scientific_evidence"] is False
assert cc["classification"] == lc["classification"]
for key in ("balance_residual", "operator_hermiticity_error", "operator_norm"):
    close(lc[key], cc[key])

ss = summary["semantic_link"]
ls = r["semantic_link"]
assert ss["explicit_cross_model_label_functor_found"] == ls["explicit_cross_model_label_functor_found"] is False
assert ss["audited_artifacts"] == ls["sha256"]

sp = summary["positive_control"]
lp = r["positive_control"]
assert sp["classification"] == lp["classification"]
assert sp["scientific_evidence"] == lp["scientific_evidence"] is False
assert sp["success"] == lp["success"] is True
for key in ("configuration", "source_name", "hidden_classification", "boundary_simple", "normal_classification"):
    assert sp["selected"][key] == lp["selected"][key]
for key in ("compressed_noncentral_norm", "hidden_norm", "boundary_radius"):
    close(lp["selected"][key], sp["selected"][key])

sn = summary["incompatible_control"]
ln = r["incompatible_control"]
assert sn["classification"] == ln["classification"]
assert sn["scientific_evidence"] == ln["scientific_evidence"] is False
assert sn["success"] == ln["success"] is True
assert sn["permutation"] == ln["permutation"]
for name in ("V_A", "V_B"):
    assert sn[name]["arrangement_invariant"] == ln["errors"][name]["arrangement_invariant"]
    close(ln["errors"][name]["projector_error"], sn[name]["projector_error"])
    close(ln["errors"][name]["state_error"], sn[name]["state_error"])

# The frozen report/summary is intentionally richer than the executable's
# generic downstream not-derived list. Require every live boundary to be
# preserved, plus the two v15.02-specific upstream boundaries.
frozen_not_derived = set(summary["not_derived"])
assert set(r["not_derived"]).issubset(frozen_not_derived)
assert "a natural node-to-quantum-label functor" in frozen_not_derived
assert "a canonical parent factor action" in frozen_not_derived

print("V15_02_SHARED_LABEL_EQUIVARIANCE_CHECKER_PASS")
print(json.dumps(r, indent=2, sort_keys=True))
