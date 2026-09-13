#!/usr/bin/env python3
from quantum_carrier_origin_audit import adjudicate_gate, run_audit

assert adjudicate_gate(True, False) == "CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER"
assert adjudicate_gate(False, True) == "FROZEN_ONTOLOGY_DERIVES_RETAINED_QUANTUM_CARRIER"
assert adjudicate_gate(False, False) == "V15_09_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.09 adjudications must raise")

s = run_audit()
assert s["version"] == "v15.09"
assert s["gate"] == "Quantum Carrier Origin / Tensor-Factorization Blindness Gate"
assert s["primary_outcome"] == "CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER"
assert s["secondary_outcome"] == "FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND"
assert s["tertiary_outcome"] == "SUPPLIED_SITE_FINGERPRINTS_DO_NOT_DEFINE_CROSS_DOMAIN_NODE_SITE_FUNCTOR"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

f = s["factorization_blindness"]
assert f["classification"] == "FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND"
assert f["dimension"] == 32
assert f["unordered_factorization_count"] == 7
assert f["five_nontrivial_factor_decomposition_count"] == 1
assert f["five_nontrivial_factor_decompositions"] == [[2, 2, 2, 2, 2]]
assert f["max_neutral_factorization_error"] < 1e-12
assert f["factorization_selected_by_tau"] is False
assert f["factorization_selected_by_Q_definition"] is False

p = s["five_site_permutation_control"]
assert p["classification"] == "NEUTRAL_FIVE_QUBIT_REFERENCE_HAS_FULL_S5_SITE_PERMUTATION_SYMMETRY"
assert p["permutation_count"] == 120
assert p["accepted_permutation_count"] == 120
assert p["max_neutral_permutation_error"] < 1e-12

x = s["cross_domain_independence"]
assert x["classification"] == "TWO_SORT_REDUCT_DOES_NOT_DEFINE_NODE_SITE_BIJECTION"
assert x["graph_automorphism_order"] == 1
assert x["quantum_site_spectral_stabilizer_order"] == 1
assert x["all_site_spectral_fingerprints_distinct"] is True
assert x["node_site_bijection_count"] == 120
assert x["inequivalent_bijection_count"] == 120
assert x["certified_cross_domain_relation_found"] is False
assert x["same_reduct_supports_all_bijections"] is True

c125 = s["compatibility_parent_boundary"]
assert c125["parent_dimension"] == 125
assert c125["five_nontrivial_factor_decomposition_count"] == 0
assert c125["five_site_carrier_can_equal_parent"] is False
assert c125["natural_supplied_five_qubit_to_C125_map_found"] is False

archive = s["frozen_dependency_audit"]
assert archive["archive_bindings_match_expected"] is True
assert archive["new_v15_07_structure_reopens_v15_02"] is False
assert archive["new_v15_07_structure_reopens_v15_03"] is False
assert archive["v15_08_source_semantics_branch_stop_preserved"] is True

claim = s["claim_boundary"]
assert claim["canonical_neutral_reference_preserved"] is True
assert claim["canonical_log_generator_preserved"] is True
assert claim["five_site_quantum_carrier_derived"] is False
assert claim["retained_node_to_quantum_site_functor_derived"] is False
assert claim["graph_site_to_C125_parent_map_derived"] is False
assert claim["source_semantics_reopened"] is False
assert claim["new_representation_principle_required"] is True
assert claim["downstream_gravity_used_as_selector"] is False
assert claim["entropy_or_time_used_as_selector"] is False
assert claim["Pillar_3_closed"] is False

print("v15.09 checker passed")
