#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.14'
a=s['exchange_twirl_ETL_test']
assert a['same_exchange_twirl_state_error']<1e-12
assert a['fixed_site_source_projected_response_gap']>1e-3
assert a['covariantly_rotated_source_response_error']<1e-8
b=s['exchange_invariant_ETL_sector']
assert max(x['projection_error'] for x in b['flow_rows'])<1e-10
c=s['collective_plus_exchange_block_sector']
for row in c['dimension_rows']:
    assert row['collective_plus_exchange_block_dim']==row['closed_form']
assert max(x['block_projection_error'] for x in c['N4_ETL_flow_rows'])<1e-9
d=s['generic_local_source_obstruction']
assert d['N3_same_J_block_projection_error']<1e-12
assert d['N3_site_source_projected_response_gap']>1e-3
e=s['local_geometry_full_algebra_collapse']
for row in e['rows']:
    assert row['center_commutant_dimension_after_local_source']==1
    assert row['generated_algebra_dimension_by_double_commutant']==4**row['N']
assert s['adjudication']['system_size_independent_finite_symmetry_reduced_state'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_14_CHECKER_PASS')
