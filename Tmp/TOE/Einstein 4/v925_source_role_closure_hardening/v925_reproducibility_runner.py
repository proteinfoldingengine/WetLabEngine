#!/usr/bin/env python3
from pathlib import Path
import json, pandas as pd
BASE=Path(__file__).parent
result=json.loads((BASE/'v925_source_role_closure_hardening_result.json').read_text())
ladder=pd.read_csv(BASE/'v925_lift_ladder_final_recheck.csv')
targeted=pd.read_csv(BASE/'v925_targeted_ternary_role_flip_scores.csv')
noise=pd.read_csv(BASE/'v925_random_ternary_role_noise_summary.csv')
single=pd.read_csv(BASE/'v925_single_bit_code_flip_scores.csv')
assert result['closed'] is True
assert ladder.loc[ladder.lift.eq('ternary_source_role_primitive'),'accuracy'].iloc[0] == 1.0
assert ladder.loc[ladder.lift.eq('ternary_source_role_primitive'),'false_cases'].iloc[0] == 0
assert targeted.false_cases.max() > 0
assert noise.mean_accuracy.is_monotonic_decreasing
assert single.query("scheme == 'minimal_single_error_correcting_d3'").accuracy.min() == 1.0
print(json.dumps(result, indent=2))
