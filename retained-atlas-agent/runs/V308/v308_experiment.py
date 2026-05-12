import json
import math
import os
from pathlib import Path
import random
from statistics import mean

RUN_DIR = Path('runs/V308')
RUN_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = Path('reports')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388
A_H = 0.10


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def simulate(seed, policy):
    rng = random.Random(seed)
    baseline = 1.0
    a = 0.85 + 0.05 * rng.random()
    hist_a = []
    trigger_count = 0
    bad = 0
    adaptive = 0
    rescued = 0
    harmed = 0
    severity_sum = 0.0
    late_residual_sum = 0.0
    labels = []
    scores = []

    repair_cooldown = 0
    for t in range(N_STEPS):
        shock = 0.0
        if t in (12, 25, 38, 49):
            shock = 0.10 + 0.12 * rng.random()
        drift = -0.012 + 0.008 * rng.random()
        recovery = 0.020 if repair_cooldown > 0 else 0.0
        a = clamp(a + drift - shock + recovery, 0.0, 1.0)
        hist_a.append(a)

        window = hist_a[-8:]
        a_norm = mean(window) / baseline
        d_a = mean(max(0.0, A_C - x) for x in window)
        horizon_area = mean(max(0.0, A_H - x) for x in window)

        score = {
            'A_norm': a_norm,
            'D_A': d_a,
            'horizon_area': horizon_area,
            'combined': max(d_a / max(D_C, 1e-9), horizon_area / max(0.03, 1e-9)),
        }[policy]

        trigger = False
        if policy == 'A_norm':
            trigger = a_norm < A_C
        elif policy == 'D_A':
            trigger = d_a > D_C
        elif policy == 'horizon_area':
            trigger = horizon_area > 0.03
        elif policy == 'combined':
            trigger = (d_a > D_C) or (horizon_area > 0.03)
        else:
            raise ValueError(policy)

        if trigger:
            trigger_count += 1
            repair_cooldown = 2
            if a < 0.45:
                rescued += 1
            elif a > 0.75:
                harmed += 1

        if a < 0.42:
            bad += 1
        if a > 0.62:
            adaptive += 1

        severity = max(0.0, 0.50 - a) + 0.25 * max(0.0, 0.35 - a)
        severity_sum += severity
        late_residual_sum += max(0.0, 0.45 - a)

        labels.append(1 if a < 0.42 else 0)
        scores.append(1.0 - a)

    bad_rate = bad / N_STEPS
    adaptive_rate = adaptive / N_STEPS
    trigger_rate = trigger_count / N_STEPS
    net_rescue = rescued - harmed
    severity_reduction = 1.0 - (severity_sum / N_STEPS)
    return {
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'trigger_rate': trigger_rate,
        'rescued': rescued,
        'harmed': harmed,
        'net_rescue': net_rescue,
        'severity_reduction': severity_reduction,
        'labels': labels,
        'scores': scores,
        'late_residual': late_residual_sum / N_STEPS,
    }


def auc_score(y_true, y_score):
    pos = [(s, y) for s, y in zip(y_score, y_true) if y == 1]
    neg = [(s, y) for s, y in zip(y_score, y_true) if y == 0]
    if not pos or not neg:
        return 0.5
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
    p = sum(y_true)
    n = len(y_true) - p
    tpr = tp / p if p else 0.0
    tnr = tn / n if n else 0.0
    return 0.5 * (tpr + tnr)


policies = ['A_norm', 'D_A', 'horizon_area', 'combined']
results = {}

for policy in policies:
    per_seed = [simulate(seed, policy) for seed in SEEDS]
    flat_labels = [y for r in per_seed for y in r['labels']]
    flat_scores = [s for r in per_seed for s in r['scores']]
    flat_preds = [1 if s >= 0.5 else 0 for s in flat_scores]
    results[policy] = {
        'bad_rate': mean(r['bad_rate'] for r in per_seed),
        'adaptive_rate': mean(r['adaptive_rate'] for r in per_seed),
        'trigger_rate': mean(r['trigger_rate'] for r in per_seed),
        'rescued': mean(r['rescued'] for r in per_seed),
        'harmed': mean(r['harmed'] for r in per_seed),
        'net_rescue': mean(r['net_rescue'] for r in per_seed),
        'severity_reduction': mean(r['severity_reduction'] for r in per_seed),
        'AUC': auc_score(flat_labels, flat_scores),
        'balanced_accuracy': balanced_accuracy(flat_labels, flat_preds),
        'phase_counts': {
            'bad': sum(flat_labels),
            'safe': len(flat_labels) - sum(flat_labels),
        },
    }

best_policy = min(policies, key=lambda p: results[p]['bad_rate'])

output = {
    'version': 'V308',
    'title': 'Deficit Intervention Threshold Test',
    'config': {
        'seeds': SEEDS,
        'n_steps': N_STEPS,
        'A_c': A_C,
        'D_c': D_C,
        'A_h': A_H,
    },
    'results': results,
    'best_policy_by_bad_rate': best_policy,
}

out_path = RUN_DIR / 'V308_results.json'
out_path.write_text(json.dumps(output, indent=2))
report_path = REPORT_DIR / 'V308_report.md'
report_path.write_text(
    '# V308 — Deficit Intervention Threshold Test\n\n'
    + 'This run executed a fixed-seed toy intervention comparison.\n\n'
    + 'Best policy by bad_rate: ' + best_policy + '\n'
)
print(json.dumps(output, indent=2))
