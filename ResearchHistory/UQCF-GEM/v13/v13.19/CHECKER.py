#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.19'
f=s['finite_transport_composition']
assert max(x['max_error_over_sum_edge_errors'] for x in f['random_controls'])<=1.000001
assert min(x['path_error_over_m_edge_error'] for x in f['aligned_linear_sharpness'])>.9999
o=s['overlap_and_cocycle']
assert o['max_overlap_ratio']<=1.000001
assert o['max_cocycle_ratio']<=1.000001
assert s['transported_metric_error']['max_random_error_over_bound']<=1.000001
j=s['jet_composition']
assert max(x['max_error_over_jet_bound'] for x in j['random_controls'])<=1.000001
sc=[x['error_over_m2_delta'] for x in j['quadratic_scaling_control']]
assert max(sc)/min(sc)<1.00002
c=s['cocycle_without_global_reference_no_go']
assert c['pair_inverse_residual']<1e-12
assert c['triple_cocycle_residual']>1e-2
a=s['adjudication']
assert a['finite_transport_errors_exponential_in_path_length'] is False
assert a['finite_transport_errors_at_most_linear'] is True
assert a['QMAR_holonomy_jet_quadratic_scaling_attainable'] is True
assert a['scale_independent_continuum_response_atlas']=='NOT_DERIVED'
assert s['status']['scientific_breakthrough'] is False
print('V13_19_CHECKER_PASS')
