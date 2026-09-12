#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.09'
v=s['visible_sector']
assert v['min_state_eigenvalue']>0
assert v['state_J_commutator']<1e-12
assert v['cyclic_invariance_error']<1e-12
assert v['initial_QTC']<1e-12
assert v['initial_solder_closure']<1e-12
h=s['hidden_completion_counterexample']
assert h['hidden_generator_J_commutator']<1e-12
assert h['hidden_generator_cyclic_error']<1e-12
assert h['hidden_state_min_eigenvalue']>0
assert h['max_initial_one_two_body_difference']<1e-12
assert max(x['max_QTC'] for x in h['flow_rows'])<1e-12
assert h['flow_rows'][-1]['max_polar_shift']>0.05
assert h['flow_rows'][-1]['fixed_RESA_closure']>0.05
assert h['flow_rows'][-1]['holonomy_angle_shift']>0.05
m=s['holonomy_stabilizer_maximality']
assert m['curved_centralizer_dimension']==1
assert m['centralizer_axis_alignment_with_holonomy']>0.999999
assert m['flat_centralizer_dimension']==3
f=s['flat_nonabelian_control']
assert f['min_state_eigenvalue']>0
assert f['initial_QTC']<1e-12
assert max(x['max_QTC'] for x in f['flow_rows'])<1e-12
assert max(x['max_transport_shift'] for x in f['flow_rows'])<1e-12
assert max(f['commutator_residuals'])<1e-12
assert f['noncommuting_ETL_additivity_error']<1e-12
o=s['symmetry_origin_audit']
assert o['positive_symmetry_broken_state_min_eigenvalue']>0
assert o['symmetry_broken_initial_QTC']<1e-12
assert o['broken_transverse_singular_gap']>0.005
assert s['adjudication']['visible_symmetry_sufficient_for_full_LCSP']=='NO'
assert s['status']['scientific_breakthrough'] is False
print('V13_09_CHECKER_PASS')
