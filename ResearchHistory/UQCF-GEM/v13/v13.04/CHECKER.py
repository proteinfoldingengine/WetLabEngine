#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.04'
assert s['adjudication']['existing_architecture_forces_Q_convergence'] is False
assert s['adjudication']['existing_architecture_forces_Q_zero'] is False
a=s['existing_law_audit']
assert a['PGRL']['max_exponential_tilt_derivative_error']<1e-8
assert a['RESA']['max_exact_collinear_geometry_error']<1e-14
assert a['CRCL_AVT']['curvature_CRCL_jump_in_countermodel']==0
assert a['CRCL_AVT']['AVT_density_gap_in_countermodel']==0
assert a['CRCL_AVT']['nonmetricity_density_tail_jump_min']>0.05
assert a['polar_composition']['tensor_product_error']<1e-12
assert a['polar_composition']['sequential_composition_error']>1e-2
m=s['SMRRL_control']
assert m['deepest_error_to_limit']<m['predicted_tail_bound']+1e-12
assert m['nonzero_limit_norm']>0.05
assert abs(s['metric_compatibility_strengthening']['executed_decay_power']-0.75)<1e-10
assert s['section_independence']['two_SMRRL_towers_limit_gap']>0.05
assert s['status']['SMRRL']=='IRREDUCIBLE_REQUIRED_INPUT_OR_NEW_DERIVATION'
assert s['status']['scientific_breakthrough'] is False
print('V13_04_CHECKER_PASS')
