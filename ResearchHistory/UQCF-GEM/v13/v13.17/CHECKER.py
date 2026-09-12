#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.17'
assert s['analytic_BKM_regularities']['random_bound_max_ratio']<=1.000001
assert s['polar_regularities']['random_bound_max_ratio']<=1.000001
assert s['geometric_error_theorem']['holonomy_product_bound_max_ratio']<=1.000001
assert max(x['max_amplification'] for x in s['source_trajectory_boundary']['rows'])>100
a=s['adjudication']
assert a['approximate_geometric_locality_O_sqrt_CMI'] is True
assert a['uniform_source_trajectory_from_static_CMI_only'] is False
assert a['uniform_source_trajectory_with_uniform_CMI_and_conditioning'] is True
assert s['status']['scientific_breakthrough'] is False
print('V13_17_CHECKER_PASS')
