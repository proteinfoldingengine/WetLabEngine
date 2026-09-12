#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.18'
e=s['ETL_tangent_theorem']
assert e['random_bound_max_ratio']<=1.000001
assert e['random_sample_count']>100
p=s['polar_jet_regularity']
assert p['evaluated_scaling_controls'][0]['max_Dpolar_norm_unit_direction'] > p['evaluated_scaling_controls'][-1]['max_Dpolar_norm_unit_direction']*5
q=s['QMAR_jet_theorem']
assert q['numerical_conditioned_controls']['sample_count']>=20
c=s['CMI_only_no_go']
assert c['rows'][-1]['response_error']>c['rows'][0]['response_error']*49
a=s['adjudication']
assert a['static_CMI_controls_ETL_state_tangent_with_bounded_source'] is True
assert a['QMAR_jet_locality_on_conditioned_compact_strata'] is True
assert a['CMI_alone_without_source_bound_controls_jet'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_18_CHECKER_PASS')
