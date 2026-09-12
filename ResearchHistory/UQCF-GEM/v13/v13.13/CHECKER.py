#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.13'
a=s['single_chiral_scalar_test']
assert a['max_one_body_difference']<1e-12
assert a['max_two_body_difference']<1e-12
assert a['chiral_value_difference']<1e-12
assert a['response_gap_same_low_data_same_chiral']>1e-4
assert a['orthogonal_hidden_direction_chiral_overlap']<1e-10
b=s['fixed_N3_hidden_rank']
assert b['hidden_weight3_dimension']==27
assert b['sensitivity_rank']==27
assert b['max_low_order_difference_under_weight3_perturbations']<1e-12
c=s['fixed_N3_exact_closure']
assert c['reconstruction_error']<1e-12
assert c['QMAR_response_reconstruction_error']<1e-8
h=s['ETL_hierarchy_no_go']
assert h['minimum_derivative_gap']>0.39
for row in h['rows']:
    assert row['max_low_order_Z_moment_difference']<1e-12
    assert row['derivative_gap']>0.39
f=s['factorization_control']
assert f['initial_connected_pair_norm']<1e-12
assert f['connected_pair_derivative_norm']>0.1
assert s['adjudication']['fixed_finite_body_order_closure_uniform_in_N'] is False
assert s['adjudication']['RCCL_or_equivalent_required'] is True
assert s['status']['scientific_breakthrough'] is False
print('V13_13_CHECKER_PASS')
