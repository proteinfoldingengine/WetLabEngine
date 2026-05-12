import json
import math
from pathlib import Path
import random
from statistics import mean, pstdev

OUTDIR = Path('runs/V309E')
OUTDIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = OUTDIR / 'V309E_results.json'

SEEDS = list(range(20))
N_STEPS = 60
A_c = 0.527
D_c = 0.0388
A_h = 0.10

# Narrow calibration sweep: smallest useful window around prior failure boundary.
severity_grid = [0.30, 0.32, 0.34, 0.36]
base_failure_grid = [0.08, 0.10, 0.12, 0.14]
noise_grid = [0.0, 0.01]


def simulate_regime(sev, bf, nz, seed=0):
    rng = random.Random(seed)
    rows = []
    for _ in range(N_STEPS):
        # Toy dynamics engineered to remain seed-sensitive while keeping the harness compact.
        latent = 1.0 - sev * 0.55 - bf * 0.85 + rng.gauss(0.0, nz + 0.015)
        drift = rng.gauss(0.0, 0.02 + nz)
        a = max(0.0, min(1.2, latent + drift))
        score = a
        bad = 1 if a < A_c else 0
        trigger = 1 if a < A_h else 0
        rows.append({'A_norm': a, 'score': score, 'bad': bad, 'trigger': trigger})
    return rows


def auc_score(y_true, y_score):
    pos = [(s, y) for s, y in zip(y_score, y_true) if y == 1]
    neg = [(s, y) for s, y in zip(y_score, y_true) if y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    wins = 0.0
    ties = 0.0
    for ps, _ in pos:
        for ns, _ in neg:
            if ps > ns:
                wins += 1
            elif ps == ns:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


def balanced_accuracy(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    return 0.5 * (tpr + tnr)


def eval_regime(sev, bf, nz):
    all_rows = []
    for seed in SEEDS:
        all_rows.extend(simulate_regime(sev, bf, nz, seed=seed))
    y_true = [r['bad'] for r in all_rows]
    y_score = [r['score'] for r in all_rows]
    y_pred = [1 if s < A_c else 0 for s in y_score]
    bad_rate = sum(y_true) / len(y_true)
    adaptive_rate = 1.0 - bad_rate
    trigger_rate = sum(r['trigger'] for r in all_rows) / len(all_rows)
    mean_A = mean(r['A_norm'] for r in all_rows)
    min_A = min(r['A_norm'] for r in all_rows)
    score_mean = mean(y_score)
    score_var = pstdev(y_score) ** 2 if len(y_score) > 1 else 0.0
    phase_counts = {'bad': int(sum(y_true)), 'safe': int(len(y_true) - sum(y_true))}
    AUC = auc_score(y_true, y_score)
    if AUC is None:
        AUC = 0.5
    bal_acc = balanced_accuracy(y_true, y_pred)
    acc = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true)
    horizon_width = sum(1 for r in all_rows if r['A_norm'] < A_h) / len(all_rows)
    horizon_area = mean(max(0.0, A_h - r['A_norm']) for r in all_rows)
    D_A = mean(max(0.0, A_c - r['A_norm']) for r in all_rows)
    duration_below_Ac = sum(1 for r in all_rows if r['A_norm'] < A_c) / len(all_rows)
    pinch = duration_below_Ac
    late_residual = mean(r['A_norm'] for r in all_rows[-max(1, len(all_rows)//5):])
    late_mobility = mean(abs(all_rows[i]['A_norm'] - all_rows[i-1]['A_norm']) for i in range(1, len(all_rows))) if len(all_rows) > 1 else 0.0
    late_K = mean_A - min_A
    return {
        'severity': sev,
        'base_failure': bf,
        'noise_scale': nz,
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'trigger_rate': trigger_rate,
        'AUC': AUC,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'mean_A_norm': mean_A,
        'min_A_norm': min_A,
        'score_mean': score_mean,
        'score_var': score_var,
        'D_A': D_A,
        'duration_below_Ac': duration_below_Ac,
        'horizon_width': horizon_width,
        'horizon_area': horizon_area,
        'pinch': pinch,
        'late_residual': late_residual,
        'late_mobility': late_mobility,
        'late_K': late_K,
        'phase_counts': phase_counts,
    }


sweep_results = []
chosen_regime = None
for sev in severity_grid:
    for bf in base_failure_grid:
        for nz in noise_grid:
            res = eval_regime(sev, bf, nz)
            validity_gate = {
                'nondegenerate_bad_rate': 0.20 <= res['bad_rate'] <= 0.40,
                'nonzero_score_variance': res['score_var'] > 0.0,
                'nonzero_trigger_rate': res['trigger_rate'] > 0.05,
                'enough_positive_cases': res['phase_counts']['bad'] > 0,
                'valid_for_interpretation': False,
            }
            validity_gate['valid_for_interpretation'] = (
                validity_gate['nondegenerate_bad_rate'] and
                validity_gate['nonzero_score_variance'] and
                validity_gate['nonzero_trigger_rate'] and
                validity_gate['enough_positive_cases']
            )
            res['validity_gate'] = validity_gate
            sweep_results.append(res)
            if chosen_regime is None and validity_gate['valid_for_interpretation']:
                chosen_regime = {'severity': sev, 'base_failure': bf, 'noise_scale': nz}

summary = {
    'chosen_regime': chosen_regime,
    'sweep_count': len(sweep_results),
    'valid_count': sum(1 for r in sweep_results if r['validity_gate']['valid_for_interpretation']),
}

# If a valid regime exists, we keep it selected; otherwise this is a harness failure.
if chosen_regime is None:
    decision = 'branch'
    note = 'no valid regime found'
else:
    decision = 'continue'
    note = 'valid regime found'

results = {
    'version': 'V309E',
    'title': 'Seed-sensitive harness repair test with narrow calibration sweep',
    'config': {
        'seeds': SEEDS,
        'n_steps': N_STEPS,
        'A_c': A_c,
        'D_c': D_c,
        'A_h': A_h,
        'severity_grid': severity_grid,
        'base_failure_grid': base_failure_grid,
        'noise_grid': noise_grid,
    },
    'chosen_regime': chosen_regime,
    'decision': decision,
    'next': 'If valid, run held-out component ablation in the same regime; otherwise redesign the harness again before any ablation.',
    'note': note,
    'sweep_results': sweep_results,
}

# Global validity gate summary for the chosen regime if present.
if chosen_regime is None:
    results['validity_gate'] = {
        'nondegenerate_bad_rate': False,
        'nonzero_score_variance': False,
        'nonzero_trigger_rate': False,
        'enough_positive_cases': False,
        'valid_for_interpretation': False,
    }
else:
    chosen = next(r for r in sweep_results if r['severity'] == chosen_regime['severity'] and r['base_failure'] == chosen_regime['base_failure'] and r['noise_scale'] == chosen_regime['noise_scale'])
    results['validity_gate'] = chosen['validity_gate']
    results['summary'] = chosen

with open(RESULTS_PATH, 'w') as f:
    json.dump(results, f, indent=2, sort_keys=True)

print(json.dumps(results, indent=2, sort_keys=True))
