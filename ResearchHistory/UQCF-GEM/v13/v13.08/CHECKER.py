#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.08'
g=s['generic_connected_family']
assert g['stacked_rank']==9 and g['stacked_nullity']==0
p=s['symmetry_selected_exact_sector']
assert p['state_source_commutator_norm']<1e-12
assert p['baseline_holonomy_angle']>0.1
assert max(x['max_QTC'] for x in p['finite_flow_rows'])<1e-12
assert max(x['solder_closure'] for x in p['finite_flow_rows'])<1e-12
assert max(x['holonomy_angle_shift'] for x in p['finite_flow_rows'])<1e-12
assert max(x['max_QTC'] for x in p['rotated_orbit_rows'])<1e-12
a=s['source_algebra']
assert a['physical_dimension_mod_identity']==1
assert a['sequential_ETL_additivity_error']<1e-12
assert a['commutator_norm']<1e-14
b=s['symmetry_break_control']
assert b['initial_QTC']<1e-12
assert b['rows'][-1]['max_QTC']>1e-4
assert s['adjudication']['nontrivial_symmetry_selected_source_algebra']=='YES'
assert s['adjudication']['LCSP_generic']=='NOT_DERIVED'
assert s['status']['scientific_breakthrough'] is False
print('V13_08_CHECKER_PASS')
