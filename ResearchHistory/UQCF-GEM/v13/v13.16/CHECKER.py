#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.16'
o=s['ontology_selection_audit']
assert o['ordered_native_triples']==13104
assert o['exact_Petz_gluing_count']==0
m=s['exact_markov_source_stability']
assert m['initial_CMI']<1e-12
assert max(x['max_abs_CMI'] for x in m['clique_source_rows'])<1e-12
assert m['nonclique_source_rows'][-1]['CMI']>1e-3
p=s['parity_hidden_family']
assert p['small_eps_mean_response_over_sqrt2CMI']>0.999
for row in p['rows']:
    assert row['CMI_formula_error']<1e-12
    assert abs(row['response_error']-row['eps'])<1e-12
r=s['recoverability_locality_bound']
assert r['random_lemma_max_error_to_bound_ratio']<=1.0
a=s['adjudication']
assert a['ontology_forces_exact_Markovity'] is False
assert a['small_CMI_gives_certified_approximate_locality'] is True
assert a['linear_in_CMI_response_error_bound'] is False
assert s['status']['scientific_breakthrough'] is False
print('V13_16_CHECKER_PASS')
