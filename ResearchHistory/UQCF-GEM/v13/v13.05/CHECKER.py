#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.05'
m=s['metric_affine_decomposition']
assert m['reconstruction_error']<1e-12
assert m['LC_plus_contortion_nonmetricity_error']<1e-12
assert m['LC_plus_disformation_torsion_error']<1e-12
d=s['delete_one_minimality']
assert d['Q_zero_T_nonzero']['Q_norm']<1e-12
assert d['Q_zero_T_nonzero']['T_norm']>0.1
assert d['T_zero_Q_nonzero']['T_norm']<1e-12
assert d['T_zero_Q_nonzero']['Q_norm']>0.1
c=s['levi_civita_sector_can_be_curved']
assert abs(c['scalar_curvature'])>0.5
assert c['error']<1e-12
r=s['retained_sector_nonempty_control']
assert r['min_state_eigenvalue']>0
assert r['max_one_body_marginal_error']<1e-12
assert r['max_BKM_QTC_edge_error']<1e-12
assert r['solder_loop_closure_norm']<1e-12
assert r['polar_holonomy_angle']>0.1
p=s['restriction_vs_projection']['generic_projection']
assert p['loop_similarity_error_before_projection']<1e-12
assert p['holonomy_trace_shift']>1e-3
assert p['mathematical_projection_idempotence_error']<1e-12
assert s['adjudication']['Q_T_zero_minimality']=='CLOSED_THEOREM'
assert s['status']['scientific_breakthrough'] is False
print('V13_05_CHECKER_PASS')
