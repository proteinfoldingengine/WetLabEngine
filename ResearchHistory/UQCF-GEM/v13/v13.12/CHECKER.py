#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.12'
sh=s['shear_object']
assert sh['gauge_covariance_error']<1e-7
a=s['counterexample_zero_shear_nonzero_curvature']
assert a['hidden_shear_response_norm']<1e-8
assert a['hidden_holonomy_response_norm']>0.1
assert a['finite_flow_rows'][-1]['hidden_shear_norm']<1e-12
assert a['finite_flow_rows'][-1]['holonomy_difference']>0.1
b=s['counterexample_nonzero_shear_zero_curvature']
assert b['ETL_tangent_reconstruction_error']<1e-8
assert b['connected_correlation_jet_norm']<1e-8
assert b['polar_transport_jet_norm']<1e-8
assert b['shear_response_norm']>0.01
assert b['holonomy_response_norm']<1e-8
assert s['adjudication']['shear_determines_curvature_response'] is False
assert s['adjudication']['curvature_determines_shear_response'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_12_CHECKER_PASS')
