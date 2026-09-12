#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.10'
i=s['initial_equivalence']
assert i['min_eigenvalue_rigid']>0 and i['min_eigenvalue_hidden']>0
assert i['max_one_body_difference']<1e-12
assert i['max_two_body_difference']<1e-12
assert i['max_BKM_metric_difference']<1e-12
assert i['max_connected_pair_difference']<1e-12
assert i['max_polar_transport_difference']<1e-12
assert i['initial_F3_difference']<1e-12
assert i['schema_complete_projection_identical'] is True
h=s['hidden_discriminator']
assert abs(h['Ghidden_expectation_rigid'])<1e-12
assert abs(h['Ghidden_expectation_hidden'])>1e-3
j=s['source_response_jet']
assert j['rigid']['max_edge_transport_jet_norm']<1e-8
assert j['hidden']['max_edge_transport_jet_norm']>0.05
assert j['rigid']['holonomy_jet_norm']<1e-8
assert j['hidden']['holonomy_jet_norm']>0.1
assert j['rigid']['fixed_RESA_closure_jet_norm']<1e-8
assert j['hidden']['fixed_RESA_closure_jet_norm']>0.05
assert s['future_diagnostic']['flow_rows'][-1]['F3_difference']>0.1
assert s['nonfactorization']['ledger_identical'] is True
assert s['adjudication']['HCPR_derivable_from_current_frozen_ledger'] is False
assert s['law_freeze']['status']=='IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_LEDGER'
assert s['status']['scientific_breakthrough'] is False
print('V13_10_CHECKER_PASS')
