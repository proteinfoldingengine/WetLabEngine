#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.01'
assert s['status']['local_SMI']=='CLOSED_CONDITIONAL_ON_MEA'
assert s['status']['QTC']=='NOT_DERIVED'
assert s['status']['HLCB']=='OPEN_BUT_NOW_REDUCED_TO_QTC_PLUS_TFHC_AFTER_MEA'
assert s['branch_stop']['metric_origin_search']=='STOP'
q=s['QTC']
assert q['positive_control']['qtc_error']<1e-12
assert q['positive_control']['q_orthonormal_transport_error']<1e-12
assert q['positive_control']['coframe_gauge_relation_error']<1e-12
assert q['negative_control']['relative_qtc_error']>0.05
assert q['negative_control']['induced_transport_orthogonality_defect']>0.05
n=s['normalization_role']
assert n['universal_constant_scale']['induced_transport_error']<1e-12
assert n['universal_constant_scale']['Levi_Civita_Gamma_error']<1e-12
assert n['state_or_node_dependent_scale']['Gamma_defect']>0.05
assert n['state_or_node_dependent_scale']['discrete_transport_orthogonality_defect']>0.1
c=s['coframe_gauge_theorem']
assert c['LC_torsion_norm']<1e-12
assert c['x_dependent_gauge_torsion_norm']<1e-12
assert c['torsion_covariance_error']<1e-12
assert c['contorsion_torsion_norm']>0.05
assert c['contorsion_covariance_error']<1e-12
assert s['status']['scientific_breakthrough'] is False
print('V13_01_CHECKER_PASS')
