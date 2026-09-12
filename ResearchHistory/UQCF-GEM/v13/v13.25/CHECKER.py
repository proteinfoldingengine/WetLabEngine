#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.25'
r=s['retained_current_control']
assert r['source_balance_residual']<1e-12
assert r['response_selected_rank_RZ']==r['cycle_dimension']
assert r['response_selected_current_error']<1e-12
n=s['normalization_no_go']
assert n['max_covariance_error']<1e-12
assert n['heldout_residual_spread']<1e-12
assert n['wrong_fixed_kappa_residual_range']>1.0
c=s['independent_calibration_positive_control']
assert c['error']<1e-12
a=s['adjudication']
assert a['actual_retained_to_observer_rho_j_map_derived'] is False
assert a['actual_kappa_obs_derived_from_retained_ledger'] is False
assert a['source_current_balance_fixes_common_scale'] is False
assert a['Einstein_residual_can_fix_scale_without_circularity'] is False
assert a['RSLB']=='NOT_CLOSED'
assert s['status']['scientific_breakthrough'] is False
print('V13_25_CHECKER_PASS')
