#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.02'
assert s['adjudication']['QTC']=='NOT_DERIVED'
assert s['adjudication']['QTC_generic_status']=='GENERALLY_FALSE_FOR_POLAR_CORRELATION_TRANSPORT'
c=s['same_C_countermodels']['cases']
assert c['matched']['QTC_relative_residual']<1e-12
assert c['spectral_mismatch']['QTC_relative_residual']>0.1
assert c['axis_mismatch']['QTC_relative_residual']>0.03
for x in c.values():
    assert x['min_rho_eigenvalue']>0
    assert x['connected_C_error_to_fixed']<1e-12
    assert x['polar_O_error_to_fixed_R']<1e-12
t=s['qubit_QTC_theorem']
assert t['max_positive_control_error']<1e-12
assert t['min_radius_mismatch_error']>1e-4
assert t['min_axis_mismatch_error']>1e-5
n=s['nonmetricity']
assert n['gauge_Delta_error']<1e-12
assert n['gauge_dimensionless_norm_error']<1e-12
r=s['random_pair_survey']
assert r['accepted']>=900
assert r['count_below_1e_3']==0
assert r['qtc_relative_median']>0.05
assert s['status']['BKM_nonmetricity_channel']=='DERIVED_AS_DEFECT_OBSERVABLE'
assert s['status']['scientific_breakthrough'] is False
print('V13_02_CHECKER_PASS')
