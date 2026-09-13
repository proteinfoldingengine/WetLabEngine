#!/usr/bin/env python3
import json
from pruning_order_emergent_time_audit import adjudicate_gate, run_audit

assert adjudicate_gate(True, False) == "FROZEN_PRUNING_DOES_NOT_YET_DERIVE_INTRINSIC_TIME_ORDER"
assert adjudicate_gate(False, True) == "INTRINSIC_IRREVERSIBLE_PRUNING_ORDER_DERIVED"
assert adjudicate_gate(False, False) == "V15_10_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.10 adjudications must raise")

s = run_audit()
assert s["version"] == "v15.10"
assert s["gate"] == "Pruning-Order / Emergent-Time Bridge Reassessment"
assert s["primary_outcome"] == "FROZEN_PRUNING_DOES_NOT_YET_DERIVE_INTRINSIC_TIME_ORDER"
assert s["secondary_outcome"] == "V1153_REWEIGHTING_IS_SUPPORT_PRESERVING_AND_INVERTIBLE_ON_SIMPLEX_INTERIOR"
assert s["tertiary_outcome"] == "PROVENANCE_LEDGER_HAS_INTRINSIC_ANCESTRY_ORDER_BUT_NO_FROZEN_IDENTIFICATION_WITH_PRUNING_TIME"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

r = s["v1153_reweighting"]
assert r["classification"] == "SELECTION_PRESSURE_WITHOUT_IRREVERSIBLE_SUPPORT_PRUNING"
assert r["positive_support_preserved"] is True
assert r["support_cardinality_before"] == 7
assert r["support_cardinality_after"] == 7
assert r["max_inverse_error"] < 1e-12
assert r["max_composition_error"] < 1e-12
assert r["reweighting_bijective_on_simplex_interior"] is True
assert r["intrinsic_arrow_from_weight_map"] is False
assert r["ordered_update_loop_is_exogenous"] is True
assert r["hard_accept_reject_filter_drives_dynamics"] is False

p = s["provenance_order"]
assert p["classification"] == "INTRINSIC_PROVENANCE_ORDER_EXISTS_BUT_IS_NOT_DERIVED_FROM_PRUNING"
assert p["rooted_orientation"] is True
assert p["append_only_order_composable"] is True
assert p["ancestry_relation_antisymmetric"] is True
assert p["physical_time_identified"] is False
assert p["pruning_generates_ledger_order"] is False

c = s["conditional_irreversible_pruning_theorem"]
assert c["classification"] == "NONINJECTIVE_RECOVERABILITY_UPDATE_INDUCES_ORIENTED_INFORMATION_ORDER_CONDITIONALLY"
assert c["map_count"] == 3
assert c["all_maps_noninjective"] is True
assert c["composition_noninjective"] is True
assert c["two_sided_inverse_exists"] is False
assert c["orientation_intrinsic_to_information_loss"] is True
assert c["frozen_pruning_realizes_this_structure"] is False

f = s["frozen_dependency_audit"]
assert f["archive_bindings_match_expected"] is True
assert f["v1153_external_order_loop_found"] is True
assert f["v1153_support_reduction_rule_found"] is False
assert f["v995_append_only_order_found"] is True
assert f["v997_warns_update_index_is_not_physical_time"] is True
assert f["frozen_pruning_to_provenance_order_identification_found"] is False

b = s["claim_boundary"]
assert b["pruning_pressure_derived"] is True
assert b["intrinsic_provenance_order_derived"] is True
assert b["pruning_derived_order_derived"] is False
assert b["irreversible_information_loss_update_derived"] is False
assert b["emergent_time_order_derived"] is False
assert b["metric_duration_derived"] is False
assert b["physical_time_primitive_used"] is False
assert b["entropy_used_as_selector"] is False
assert b["adm_or_spacetime_time_used_as_selector"] is False
assert b["Pillar_3_closed"] is False

print(json.dumps(s, indent=2, sort_keys=True))
