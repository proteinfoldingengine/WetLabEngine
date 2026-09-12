#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.03'
assert s['adjudication']['raw_N_to_zero_implies_Levi_Civita']=='FALSE'
assert s['adjudication']['canonical_continuum_nonmetricity_density']=='DERIVED'
a=s['smooth_quantum_BKM_tower']
assert 0.95<a['raw_N_power']<1.05
assert a['analytic_limit_norm']>0.05
assert a['deepest_density_error_to_analytic_limit']<5e-4
assert s['metric_compatible_control']['max_Q_density_norm']<1e-10
p=s['persistent_raw_mismatch_control']
assert abs(p['raw_N_power'])<1e-8
assert -1.01<p['Q_density_power']<-0.99
assert s['oscillatory_control']['tail_even_odd_gap']>0.02
g=s['gauge_control']
assert g['Q_density_covariance_error']<1e-12
pr=s['projection_no_go']
assert pr['original_loop_similarity_error']<1e-12
assert pr['holonomy_trace_shift']>1e-3
assert pr['alternate_metric_compatible_repair_trace_shift']>1e-3
assert s['status']['scientific_breakthrough'] is False
print('V13_03_CHECKER_PASS')
