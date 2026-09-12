#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.15'
g=s['generic_path_counterexample']
assert g['min_state_eigenvalue']>0
assert g['max_difference_over_all_proper_marginals']<1e-12
assert g['QMAR_edge_response_gap']>1e-3
m=s['commuting_markov_positive_sector']
assert m['max_finite_flow_pair_error']<1e-12
assert m['max_response_derivative_error']<1e-9
for row in m['path_controls']:
    assert row['separator_message_dimension']==2
n=s['noncommuting_source_boundary']
assert n['offdiagonal_norm_after_local_sigma_x_tilt']>1e-3
assert s['adjudication']['bounded_radius_marginals_generic_exact_closure'] is False
assert s['adjudication']['commuting_markov_separator_closure'] is True
assert s['status']['scientific_breakthrough'] is False
print('V13_15_CHECKER_PASS')
