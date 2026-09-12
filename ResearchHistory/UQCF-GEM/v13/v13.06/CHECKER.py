#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.06'
assert s['baseline_sector']['max_QTC_residual']<1e-12
assert s['baseline_sector']['solder_closure_norm']<1e-12
assert s['baseline_sector']['holonomy_angle']>0.1
src=s['source_insertion']['rows']
assert src[-1]['max_QTC_residual']>1e-3
assert src[-1]['solder_closure_with_fixed_RESA']>1e-3
assert s['source_insertion']['small_source_scaling']['QTC_residual_power']>0.8
assert s['source_insertion']['small_source_scaling']['solder_nonclosure_power']>1.5
assert s['source_insertion']['null_common_unitary']['max_QTC_residual']<1e-12
assert s['source_insertion']['null_common_unitary']['solder_closure_norm']<1e-12
assert s['independent_composition']['block_disjoint_QTC_error']<1e-12
assert s['q_isometry_groupoid']['composed_metric_compatibility_error']<1e-12
assert min(s['q_isometry_groupoid']['bad_inserted_metric_edge_errors'])>1e-2
r=s['refinement']
assert max(r['good']['child_metric_errors'])<1e-12
assert r['good']['solder_refinement_error']<1e-12
assert min(r['generic_unconstrained']['child_metric_errors'])>1e-2
assert r['generic_unconstrained']['solder_refinement_error']>0.05
assert s['atlas_gauge']['qtc_error_after_independent_frame_changes']<1e-12
assert s['adjudication']['LC_sector_closed_under_all_retained_operations'] is False
assert s['adjudication']['LC_sector_closed_under_principled_subcategory'] is True
assert s['status']['scientific_breakthrough'] is False
print('V13_06_CHECKER_PASS')
