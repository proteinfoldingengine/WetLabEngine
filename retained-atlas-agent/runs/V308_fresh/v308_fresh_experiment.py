import json
import math
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean, pstdev
from itertools import product

ROOT = Path('runs') / 'V308_fresh'
ROOT.mkdir(parents=True, exist_ok=True)

# Fixed seeds for reproducibility
SEEDS = list(range(8))

# Narrow sweep near a plausible boundary; intentionally compact.
severity_grid = [0.45, 0.55, 0.65]
base_failure_grid = [0.35, 0.45, 0.55]
noise_grid = [0.0, 0.08]

A_C = 0.527
D_C = 0.0388
A_H = 0.10


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def auc_score(y_true, y_score):
    pos = [s for y, s in zip(y_true, y_score) if y == 1]
    neg = [s for y, s in zip(y_true, y_score) if y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    wins = 0.0
    ties = 0.0
    total = len(pos) * len(neg)
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    return (wins + 0.5 * ties) / total


def balanced_accuracy(y_true, y_pred):
    tp = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 0)
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    return 0.5 * (tpr + tnr)


def simulate_regime(sev, bf, nz, seed=0, n_steps=80):
    # Toy dynamics: lower reachability under higher severity/base failure/noise.
    # Seed perturbs phase and noise, but regime parameters matter.
    phase = (seed * 0.73 + sev * 4.1 + bf * 5.7) % (2 * math.pi)
    rng = __import__('random').Random(seed)
    A_norm = []
    horizon_mask = []
    late_residual = []
    late_mobility = []
    late_K = []
    late_action = []
    late_field = []
    for t in range(n_steps):
        x = t / max(1, n_steps - 1)
        trend = 1.0 - sev * (0.18 + 0.55 * x) - bf * (0.10 + 0.35 * x)
        osc = 0.06 * math.sin(2 * math.pi * (x * 1.4) + phase)
        noise = nz * rng.gauss(0.0, 1.0)
        a = max(0.0, min(1.2, trend + osc + noise))
        A_norm.append(a)
        horizon_mask.append(1 if a < A_H else 0)
        late_residual.append(max(0.0, 0.55 - a))
        late_mobility.append(max(0.0, 0.2 + 0.7 * a + 0.05 * rng.random()))
        late_K.append(max(0.0, 0.3 + 0.4 * (1.0 - a) + 0.03 * rng.random()))
        late_action.append(max(0.0, 0.25 + 0.5 * (1.0 - a)))
        late_field.append(max(0.0, 0.15 + 0.45 * (1.0 - a)))
    D_A = sum(max(0.0, A_C - a) for a in A_norm) / len(A_norm)
    bad = 1 if D_A > D_C or sum(1 for a in A_norm if a < A_H) > 0.45 * n_steps else 0
    adaptive = 1 - bad
    trigger_da = 1 if D_A > D_C else 0
    trigger_scalar = 1 if min(A_norm) < A_C else 0
    trigger_horizon = 1 if sum(horizon_mask) / n_steps > 0.2 else 0
    trigger_combined = 1 if (trigger_da or trigger_scalar or trigger_horizon) else 0
    trigger = trigger_da
    rescued = 1 if (trigger and bad == 1 and D_A < D_C * 1.25) else 0
    harmed = 1 if (trigger and bad == 0) else 0
    phase_counts = {
        'bad': bad,
        'adaptive': adaptive,
        'horizon': int(sum(horizon_mask) > 0),
    }
    horizon_width = sum(horizon_mask) / n_steps
    horizon_area = sum(max(0.0, A_H - a) for a in A_norm) / n_steps
    pinch = 1.0 - min(A_norm)
    score = D_A
    return {
        'sev': sev,
        'bf': bf,
        'nz': nz,
        'seed': seed,
        'A_norm': A_norm,
        'D_A': D_A,
        'bad': bad,
        'adaptive': adaptive,
        'trigger_da': trigger_da,
        'trigger_scalar': trigger_scalar,
        'trigger_horizon': trigger_horizon,
        'trigger_combined': trigger_combined,
        'trigger': trigger,
        'rescued': rescued,
        'harmed': harmed,
        'horizon_area': horizon_area,
        'horizon_width': horizon_width,
        'pinch': pinch,
        'mean_A_norm': sum(A_norm) / len(A_norm),
        'min_A_norm': min(A_norm),
        'score': score,
        'late_K': sum(late_K) / len(late_K),
        'late_mobility': sum(late_mobility) / len(late_mobility),
        'late_residual': sum(late_residual) / len(late_residual),
        'late_action': sum(late_action) / len(late_action),
        'late_field': sum(late_field) / len(late_field),
        'phase_counts': phase_counts,
    }


def score_regime(results):
    y = [r['bad'] for r in results]
    s = [r['score'] for r in results]
    preds = [1 if v > D_C else 0 for v in s]
    auc = auc_score(y, s)
    ba = balanced_accuracy(y, preds)
    acc = sum(1 for yt, yp in zip(y, preds) if yt == yp) / len(y)
    bad_rate = sum(y) / len(y)
    adaptive_rate = 1 - bad_rate
    trigger_rate = sum(r['trigger'] for r in results) / len(results)
    rescued = sum(r['rescued'] for r in results)
    harmed = sum(r['harmed'] for r in results)
    net_rescue = rescued - harmed
    phase_counts = {
        'bad': sum(r['phase_counts']['bad'] for r in results),
        'adaptive': sum(r['phase_counts']['adaptive'] for r in results),
        'horizon': sum(r['phase_counts']['horizon'] for r in results),
    }
    return {
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'AUC': auc,
        'balanced_accuracy': ba,
        'accuracy': acc,
        'trigger_rate': trigger_rate,
        'rescued': rescued,
        'harmed': harmed,
        'net_rescue': net_rescue,
        'phase_counts': phase_counts,
        'horizon_area': mean(r['horizon_area'] for r in results),
        'horizon_width': mean(r['horizon_width'] for r in results),
        'pinch': mean(r['pinch'] for r in results),
        'mean_A_norm': mean(r['mean_A_norm'] for r in results),
        'min_A_norm': min(r['min_A_norm'] for r in results),
        'score_mean': mean(s),
        'score_var': pstdev(s) ** 2 if len(s) > 1 else 0.0,
        'late_K': mean(r['late_K'] for r in results),
        'late_mobility': mean(r['late_mobility'] for r in results),
        'late_residual': mean(r['late_residual'] for r in results),
    }


candidate_records = []
for sev, bf, nz in product(severity_grid, base_failure_grid, noise_grid):
    results = [simulate_regime(sev, bf, nz, seed=s) for s in SEEDS]
    summary = score_regime(results)
    chosen = (
        summary['bad_rate'] >= 0.20 and summary['bad_rate'] <= 0.40 and
        summary['trigger_rate'] > 0.05 and
        summary['phase_counts']['bad'] > 0 and
        summary['AUC'] is not None and
        summary['balanced_accuracy'] >= 0.5
    )
    validity_gate = {
        'chosen_regime_not_null': chosen,
        'bad_rate_range': 0.20 <= summary['bad_rate'] <= 0.40,
        'trigger_rate_gt_0p05': summary['trigger_rate'] > 0.05,
        'phase_counts_bad_gt_0': summary['phase_counts']['bad'] > 0,
        'valid_for_interpretation': bool(chosen),
        'auc_metric_real': summary['AUC'] is not None,
    }
    rec = {
        'regime': {'sev': sev, 'bf': bf, 'nz': nz},
        **summary,
        'validity_gate': validity_gate,
    }
    candidate_records.append(rec)

valid = [r for r in candidate_records if r['validity_gate']['valid_for_interpretation']]
chosen_regime = None
if valid:
    valid.sort(key=lambda r: (abs(r['bad_rate'] - 0.30), -r['balanced_accuracy'], -r['trigger_rate']))
    chosen_regime = valid[0]
else:
    candidate_records.sort(key=lambda r: (abs(r['bad_rate'] - 0.30), -r['balanced_accuracy']))
    chosen_regime = None

results = {
    'version': 'V308_fresh',
    'chosen_regime': chosen_regime['regime'] if chosen_regime else None,
    'bad_rate': chosen_regime['bad_rate'] if chosen_regime else None,
    'adaptive_rate': chosen_regime['adaptive_rate'] if chosen_regime else None,
    'AUC': chosen_regime['AUC'] if chosen_regime else None,
    'balanced_accuracy': chosen_regime['balanced_accuracy'] if chosen_regime else None,
    'accuracy': chosen_regime['accuracy'] if chosen_regime else None,
    'trigger_rate': chosen_regime['trigger_rate'] if chosen_regime else None,
    'rescued': chosen_regime['rescued'] if chosen_regime else None,
    'harmed': chosen_regime['harmed'] if chosen_regime else None,
    'net_rescue': chosen_regime['net_rescue'] if chosen_regime else None,
    'horizon_area': chosen_regime['horizon_area'] if chosen_regime else None,
    'horizon_width': chosen_regime['horizon_width'] if chosen_regime else None,
    'pinch': chosen_regime['pinch'] if chosen_regime else None,
    'mean_A_norm': chosen_regime['mean_A_norm'] if chosen_regime else None,
    'min_A_norm': chosen_regime['min_A_norm'] if chosen_regime else None,
    'score_mean': chosen_regime['score_mean'] if chosen_regime else None,
    'score_var': chosen_regime['score_var'] if chosen_regime else None,
    'late_K': chosen_regime['late_K'] if chosen_regime else None,
    'late_mobility': chosen_regime['late_mobility'] if chosen_regime else None,
    'late_residual': chosen_regime['late_residual'] if chosen_regime else None,
    'phase_counts': chosen_regime['phase_counts'] if chosen_regime else None,
    'validity_gate': chosen_regime['validity_gate'] if chosen_regime else {
        'chosen_regime_not_null': False,
        'bad_rate_range': False,
        'trigger_rate_gt_0p05': False,
        'phase_counts_bad_gt_0': False,
        'valid_for_interpretation': False,
        'auc_metric_real': any(r['AUC'] is not None for r in candidate_records),
    },
    'candidate_count': len(candidate_records),
    'all_candidates': candidate_records,
}

out_json = ROOT / 'V308_fresh_results.json'
out_txt = ROOT / 'V308_fresh_results.txt'
out_json.write_text(json.dumps(results, indent=2, sort_keys=True))
out_txt.write_text(json.dumps(results, indent=2, sort_keys=True))
print(json.dumps(results, indent=2, sort_keys=True))
