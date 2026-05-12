import json, os, math, random, statistics as stats
from pathlib import Path

ROOT = Path('runs/V309_VALIDATOR_TEST')
ROOT.mkdir(parents=True, exist_ok=True)
OUT = ROOT / 'V309_VALIDATOR_TEST_results.json'

SEEDS = [101, 203, 307, 409, 503, 607, 701, 809]
CANDIDATES = [
    {'bf': 0.25, 'nz': 0.02, 'sev': 0.55},
    {'bf': 0.25, 'nz': 0.05, 'sev': 0.55},
    {'bf': 0.30, 'nz': 0.02, 'sev': 0.60},
    {'bf': 0.30, 'nz': 0.05, 'sev': 0.60},
    {'bf': 0.35, 'nz': 0.02, 'sev': 0.65},
    {'bf': 0.35, 'nz': 0.08, 'sev': 0.65},
    {'bf': 0.40, 'nz': 0.02, 'sev': 0.70},
    {'bf': 0.40, 'nz': 0.08, 'sev': 0.70},
    {'bf': 0.45, 'nz': 0.02, 'sev': 0.75},
    {'bf': 0.45, 'nz': 0.08, 'sev': 0.75},
]
A_c = 0.527
A_h = 0.10
D_c = 0.0388


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def simulate_regime(bf, nz, sev, seed):
    rng = random.Random(seed * 1009 + int(bf * 100) * 13 + int(nz * 1000) * 7 + int(sev * 100) * 3)
    n = 8
    A = []
    curr = clamp(0.72 - 0.35 * sev - 0.15 * bf + 0.08 * (0.08 - nz) + rng.uniform(-0.05, 0.05), 0.05, 0.98)
    for t in range(n):
        drift = -0.04 * sev + 0.02 * (0.4 - bf) - 0.03 * nz + rng.uniform(-0.03, 0.03)
        curr = clamp(curr + drift, 0.0, 1.0)
        A.append(curr)
    mean_A = sum(A) / n
    min_A = min(A)
    A_baseline = max(0.15, 0.85 * mean_A + 0.12)
    A_norm = [clamp(x / A_baseline, 0.0, 1.5) for x in A]
    D_A = sum(max(0.0, A_c - x) for x in A_norm) / n
    duration_below_Ac = sum(1 for x in A_norm if x < A_c) / n
    horizon_width = sum(1 for x in A_norm if x < A_h) / n
    horizon_area = sum(max(0.0, A_h - x) for x in A_norm) / n
    pinch = max(0.0, 1.0 - min_A)
    late_field = sum(A[-3:]) / 3.0
    late_action = clamp((0.8 - late_field) * 0.5 + 0.1 * sev + 0.05 * nz)
    late_residual = clamp(1.0 - late_field)
    late_mobility = clamp(0.5 + 0.4 * mean_A - 0.2 * nz)
    late_K = clamp(0.3 + 0.4 * mean_A + 0.1 * bf - 0.1 * sev)
    score = clamp(0.6 * D_A + 0.25 * duration_below_Ac + 0.15 * horizon_area)
    bad = 1 if (D_A > D_c or duration_below_Ac > 0.5 or score > 0.22) else 0
    adaptive = 1 - bad
    return {
        'bad': bad,
        'adaptive': adaptive,
        'mean_A_norm': mean_A / A_baseline,
        'min_A_norm': min_A / A_baseline,
        'D_A': D_A,
        'duration_below_Ac': duration_below_Ac,
        'horizon_width': horizon_width,
        'horizon_area': horizon_area,
        'pinch': pinch,
        'late_field': late_field,
        'late_action': late_action,
        'late_residual': late_residual,
        'late_mobility': late_mobility,
        'late_K': late_K,
        'score': score,
        'A_norm': A_norm,
    }


def auc_from_scores(labels, scores):
    pos = [s for l, s in zip(labels, scores) if l == 1]
    neg = [s for l, s in zip(labels, scores) if l == 0]
    if not pos or not neg:
        return None
    wins = ties = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


def bacc(labels, preds):
    tp = sum(1 for y, p in zip(labels, preds) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(labels, preds) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(labels, preds) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(labels, preds) if y == 1 and p == 0)
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    return 0.5 * (tpr + tnr)


def eval_regime(regime):
    rows = [simulate_regime(regime['bf'], regime['nz'], regime['sev'], seed) for seed in SEEDS]
    labels = [r['bad'] for r in rows]
    scores = [r['score'] for r in rows]
    auc = auc_from_scores(labels, scores)
    if auc is None:
        auc = 0.5
    pred = [1 if s >= 0.5 else 0 for s in scores]
    trigger = [1 if r['D_A'] > D_c else 0 for r in rows]
    result = {
        'regime': regime,
        'cases': len(rows),
        'bad_rate': sum(labels) / len(labels),
        'adaptive_rate': sum(1 - y for y in labels) / len(labels),
        'AUC': auc,
        'balanced_accuracy': bacc(labels, pred),
        'accuracy': sum(int(y == p) for y, p in zip(labels, pred)) / len(labels),
        'trigger_rate': sum(trigger) / len(trigger),
        'rescued': sum(1 for t, y in zip(trigger, labels) if t == 1 and y == 1),
        'harmed': sum(1 for t, y in zip(trigger, labels) if t == 1 and y == 0),
        'net_rescue': sum(1 if (t == 1 and y == 1) else 0 for t, y in zip(trigger, labels)) - sum(1 if (t == 1 and y == 0) else 0 for t, y in zip(trigger, labels)),
        'mean_A_norm': sum(r['mean_A_norm'] for r in rows) / len(rows),
        'min_A_norm': min(r['min_A_norm'] for r in rows),
        'horizon_width': sum(r['horizon_width'] for r in rows) / len(rows),
        'horizon_area': sum(r['horizon_area'] for r in rows) / len(rows),
        'pinch': sum(r['pinch'] for r in rows) / len(rows),
        'late_field': sum(r['late_field'] for r in rows) / len(rows),
        'late_action': sum(r['late_action'] for r in rows) / len(rows),
        'late_residual': sum(r['late_residual'] for r in rows) / len(rows),
        'late_mobility': sum(r['late_mobility'] for r in rows) / len(rows),
        'late_K': sum(r['late_K'] for r in rows) / len(rows),
        'phase_counts': {
            'adaptive': sum(1 for y in labels if y == 0),
            'bad': sum(1 for y in labels if y == 1),
            'horizon': sum(1 for r in rows if r['horizon_width'] > 0),
        },
        'variant_level_performance': [
            {
                'seed': SEEDS[i],
                'bad': rows[i]['bad'],
                'adaptive': rows[i]['adaptive'],
                'triggered': trigger[i],
                'D_A': rows[i]['D_A'],
                'duration_below_Ac': rows[i]['duration_below_Ac'],
                'horizon_width': rows[i]['horizon_width'],
                'horizon_area': rows[i]['horizon_area'],
                'score': rows[i]['score'],
                'late_field': rows[i]['late_field'],
                'late_action': rows[i]['late_action'],
                'late_residual': rows[i]['late_residual'],
                'late_mobility': rows[i]['late_mobility'],
                'late_K': rows[i]['late_K'],
            } for i in range(len(rows))
        ],
    }
    result['validity_gate'] = {
        'auc_metric_real': auc is not None,
        'bad_rate_range': 0.0 < result['bad_rate'] < 1.0,
        'chosen_regime_not_null': regime is not None,
        'phase_counts_bad_gt_0': result['phase_counts']['bad'] > 0,
        'trigger_rate_gt_0p05': result['trigger_rate'] > 0.05,
        'horizon_nonzero': result['horizon_width'] > 0.0 or result['horizon_area'] > 0.0,
        'valid_for_interpretation': (0.0 < result['bad_rate'] < 1.0) and (result['trigger_rate'] > 0.05) and ((result['horizon_width'] > 0.0) or (result['horizon_area'] > 0.0)),
    }
    return result


all_results = [eval_regime(r) for r in CANDIDATES]
valid = [r for r in all_results if r['validity_gate']['valid_for_interpretation']]
chosen = max(valid, key=lambda r: (r['AUC'], r['balanced_accuracy'], r['trigger_rate']), default=None)
summary = {
    'version': 'V309_VALIDATOR_TEST',
    'A_c': A_c,
    'A_h': A_h,
    'D_c': D_c,
    'candidate_count': len(CANDIDATES),
    'valid_candidate_count': len(valid),
    'chosen_regime': chosen['regime'] if chosen else None,
    'chosen_result': chosen,
    'all_candidates': all_results,
    'report_path': str(ROOT / 'V309_VALIDATOR_TEST_report.md'),
}
with open(OUT, 'w') as f:
    json.dump(summary, f, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
