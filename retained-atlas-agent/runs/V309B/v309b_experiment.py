import json
import math
import os
import random
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, accuracy_score

OUTDIR = Path('runs/V309B')
OUTDIR.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(20))
n_steps = 60
A_c = 0.527
D_c = 0.0388
A_h = 0.10

rng_master = random.Random(309)


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate(seed):
    rng = random.Random(seed)
    # Construct a non-degenerate but still toy regime with moderate bad frequency.
    x = 0.55 + 0.04 * rng.uniform(-1, 1)
    y = 0.45 + 0.04 * rng.uniform(-1, 1)
    A_baseline = 0.60
    rows = []
    shock_p = 0.18
    for t in range(n_steps):
        # latent dynamics with mild mean reversion and shocks
        shock = 1.0 if rng.random() < shock_p else 0.0
        drift = -0.012 * (x - 0.52) + 0.008 * math.sin(0.18 * t + 0.2 * seed)
        x = min(1.0, max(0.0, x + drift - 0.055 * shock + rng.gauss(0, 0.018)))
        y = min(1.0, max(0.0, y + 0.010 * (0.5 - y) + 0.035 * shock + rng.gauss(0, 0.015)))

        rf = max(0.0, min(1.0, 0.9 * x + 0.1 * (1 - shock)))
        cw = max(0.0, min(1.0, 0.75 * y + 0.25 * (1 - abs(x - y))))
        be = max(0.0, min(1.0, 0.55 + 0.35 * (1 - abs(x - 0.5)) + rng.gauss(0, 0.02)))
        dr = max(0.0, min(1.0, 0.8 * (1 - x) + 0.2 * (1 - shock)))
        rv = max(0.0, min(1.0, 0.7 * (1 - abs(y - 0.5)) + 0.3 * x))

        A = (max(rf, 1e-6) * max(cw, 1e-6) * max(be, 1e-6) * max(dr, 1e-6) * max(rv, 1e-6)) ** 0.2
        A_norm = A / A_baseline
        D_A = max(0.0, A_c - A_norm)
        H_A = max(0.0, A_h - A_norm)
        horizon_area = H_A * (1.0 + 0.5 * shock)

        bad = 1 if (A_norm < 0.72 and (shock > 0 or D_A > 0.0)) else 0
        adaptive = 1 if A_norm >= 0.72 else 0
        rows.append({
            't': t,
            'A_norm': A_norm,
            'D_A': D_A,
            'horizon_area': horizon_area,
            'bad': bad,
            'adaptive': adaptive,
            'rf': rf,
            'cw': cw,
            'be': be,
            'dr': dr,
            'rv': rv,
        })
    return rows


def metric_summary(rows):
    y = np.array([r['bad'] for r in rows], dtype=int)
    score = np.array([r['D_A'] for r in rows], dtype=float)
    A_norm = np.array([r['A_norm'] for r in rows], dtype=float)
    pred = (score > D_c).astype(int)
    auc = roc_auc_score(y, score) if len(np.unique(y)) > 1 else 0.5
    ba = balanced_accuracy_score(y, pred) if len(np.unique(y)) > 1 else 0.5
    acc = accuracy_score(y, pred)
    return {
        'bad_rate': float(y.mean()),
        'adaptive_rate': float(np.mean([r['adaptive'] for r in rows])),
        'trigger_rate': float(pred.mean()),
        'AUC': float(auc),
        'balanced_accuracy': float(ba),
        'accuracy': float(acc),
        'mean_A_norm': float(A_norm.mean()),
        'min_A_norm': float(A_norm.min()),
        'score_mean': float(score.mean()),
        'score_var': float(score.var()),
        'phase_counts': {'bad': int(y.sum()), 'safe': int((1 - y).sum())},
    }


all_rows = []
for s in SEEDS:
    all_rows.extend(simulate(s))

summary = metric_summary(all_rows)
validity_gate = {
    'nondegenerate_bad_rate': bool(0.20 <= summary['bad_rate'] <= 0.40),
    'nonzero_score_variance': bool(summary['score_var'] > 1e-8),
    'nonzero_trigger_rate': bool(summary['trigger_rate'] > 0.0),
    'enough_positive_cases': bool(summary['phase_counts']['bad'] >= 50),
}
validity_gate['valid_for_interpretation'] = bool(
    validity_gate['nondegenerate_bad_rate']
    and validity_gate['nonzero_score_variance']
    and validity_gate['nonzero_trigger_rate']
    and validity_gate['enough_positive_cases']
)

decision = 'continue' if validity_gate['valid_for_interpretation'] else 'branch'

result = {
    'version': 'V309B',
    'title': 'Regime validity check for ablation',
    'config': {
        'seeds': SEEDS,
        'n_steps': n_steps,
        'A_c': A_c,
        'D_c': D_c,
        'A_h': A_h,
    },
    'summary': summary,
    'validity_gate': validity_gate,
    'decision': decision,
    'next': 'If valid, run held-out component ablation in the same regime; if invalid, redesign regime toward bad_rate 0.20–0.40.'
}

outpath = OUTDIR / 'V309B_results.json'
outpath.write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
