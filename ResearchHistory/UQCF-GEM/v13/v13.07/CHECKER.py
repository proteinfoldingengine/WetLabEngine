#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.07'
t=s['tangent_theorem']
assert t['metric_formula_max_finite_difference_error']<2e-8
assert t['solder_formula_finite_difference_error']<2e-8
c=s['local_source_classification']
assert c['combined_rank']==8
assert c['combined_nullity']==1
assert c['null_residual']<1e-8
assert c['example_sources']['A:z']['Q_tangent_norm']>0.1
assert c['example_sources']['A:z']['Tlike_tangent_norm_fixed_RESA']<1e-8
assert c['example_sources']['A:x']['Q_tangent_norm']>0.1
assert c['example_sources']['A:x']['Tlike_tangent_norm_fixed_RESA']>1e-3
sl=s['solder_lift_nonuniqueness']
assert sl['fixed_RESA_torsionlike_tangent_norm']>1e-3
assert sl['compatible_canceling_solder_lift_norm']<1e-12
i=s['integrability_obstruction']
assert 1.8<i['finite_escape_power']<2.2
iso=s['isotropic_special_point']
assert abs(iso['first_derivative_of_QTC_residual'])<1e-5
assert 1.8<iso['finite_escape_power']<2.2
assert s['adjudication']['PGRL_implies_LC_tangency'] is False
assert s['adjudication']['first_order_LC_tangency_sufficient_for_finite_sector_preservation'] is False
assert s['status']['SCLL']=='NOT_DERIVED'
assert s['status']['scientific_breakthrough'] is False
print('V13_07_CHECKER_PASS')
