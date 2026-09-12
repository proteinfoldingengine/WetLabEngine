#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.20'
t=s['threshold_theorem']
assert t['value_atlas_bounded']=='alpha >= 2 beta + 2'
assert t['jet_local_bounded']=='alpha >= 4 beta + 2 - 2 sigma'
assert t['jet_context_bounded']=='alpha >= 2 beta + 4 - 2 lambda'
sp=s['important_special_cases']['stable_gap_bounded_source_O1_edge_jet']
assert sp['value_bounded_alpha_min']==2
assert sp['jet_bounded_alpha_min']==4
for row in s['threshold_tables']['synthetic_powerlaw_controls']:
    p=row['predicted']; m=row['measured_slopes']
    assert abs(p['path_value']-m['path_value'])<1e-12
    assert abs(p['path_jet_local']-m['path_jet_local'])<1e-12
    assert abs(p['path_jet_context']-m['path_jet_context'])<1e-12
a=s['archive_adjudication']
assert a['v12_70_supports_CMI_exponent'] is False
assert a['v12_73_supports_CMI_exponent'] is False
assert s['adjudication']['archived_data_certify_required_exponents'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_20_CHECKER_PASS')
