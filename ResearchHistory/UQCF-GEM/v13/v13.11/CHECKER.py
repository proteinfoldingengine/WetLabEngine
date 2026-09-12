#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.11'
b=s['baseline']
assert b['min_global_state_eigenvalue']>0.05
assert b['metric_response_formula_error']<1e-8
assert b['holonomy_response_formula_error']<1e-8
assert b['solder_response_formula_error']<1e-8
q=s['quantum_to_geometry_response_operator']
assert q['source_linearity_relative_error']<2e-8
g=s['gauge_covariance']
assert g['max_error']<1e-7
w=s['BKM_trace_exactness_theorem']
assert w['edge_potential_error']<1e-12
assert w['baseline_cycle_error']<1e-12
assert w['finite_source_max_cycle_error']<1e-11
assert w['finite_source_max_edge_potential_error']<1e-11
assert w['max_source_response_cycle_error']<1e-9
t=s['torsionlike_response']
assert t['fixed_RESA_response_norm']>1e-4
assert t['same_quantum_response_with_canceling_solder_lift_norm']<1e-15
n=s['geometric_nonautonomy']
assert n['current_geometry_error']<1e-12
assert n['edge_transport_jet_difference']>0.05
assert n['holonomy_jet_difference']>0.2
assert n['fixed_solder_jet_difference']>0.1
a=s['linear_conservation_audit']
assert a['response_span_rank']==23
assert a['left_null_alignment_with_trace_cycle_identity']>0.999999999
assert a['theory_trace_null_residual']<1e-10
assert a['max_direct_trace_cycle_response_residual']<1e-10
assert s['adjudication']['exact_Weyl_trace_conservation'] is True
assert s['adjudication']['metric_affine_field_equation_derived'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_11_CHECKER_PASS')
