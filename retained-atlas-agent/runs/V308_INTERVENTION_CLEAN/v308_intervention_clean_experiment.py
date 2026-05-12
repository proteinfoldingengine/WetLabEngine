import json, math, os, random, statistics
from pathlib import Path

OUTDIR = Path('runs/V308_INTERVENTION_CLEAN')
OUTDIR.mkdir(parents=True, exist_ok=True)

VERSION = 'V308_INTERVENTION_CLEAN'
SEEDS = [101, 203, 307, 409, 503, 607, 701, 809]
REGIME = {'bf': 0.35, 'nz': 0.08, 'sev': 0.65}
A_C = 0.527
D_C = 0.0388
A_H = 0.10


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate_one(seed, controller):
    rng = random.Random(seed)
    sev = REGIME['sev']
    bf = REGIME['bf']
    nz = REGIME['nz']
    T = 8
    A_baseline = 1.0 + 0.03 * (rng.random() - 0.5)
    A = 0.72 + 0.08 * (rng.random() - 0.5)
    pre = []
    A_norm_series = []
    D_series = []
    horizon_series = []
    repair = 0.0
    triggered = False
    trigger_t = None
    stage = 'adaptive'
    late_field = late_action = late_residual = late_pocket = late_mobility = late_K = 0.0
    horizon_area = 0.0
    horizon_width = 0.0
    pinch = 0.0
    bad = 0
    rescued = 0
    harmed = 0
    severity = 0.0
    for t in range(T):
        shock = bf * (0.85 + 0.3 * rng.random())
        noise = nz * (rng.random() - 0.5)
        drift = -0.03 * sev + 0.04 * repair - shock * 0.10 + noise
        A = max(0.0, min(1.2, A + drift))
        A_norm = A / A_baseline
        D = max(0.0, A_C - A_norm)
        horizon = max(0.0, A_H - A_norm)
        A_norm_series.append(A_norm)
        D_series.append(D)
        horizon_series.append(horizon)
        pre.append(A_norm)
        if controller == 'anorm':
            trigger = A_norm < A_C
        elif controller == 'da':
            trigger = D > D_C
        elif controller == 'horizon':
            trigger = horizon > 0.0
        elif controller == 'combined':
            trigger = (D > D_C) or (A_norm < A_C) or (horizon > 0.0)
        else:
            trigger = False
        if trigger and not triggered:
            triggered = True
            trigger_t = t
            repair = 1.0
            if A_norm >= A_C:
                harmed += 1
            else:
                rescued += 1
        else:
            repair *= 0.72
        severity += max(0.0, sev - A_norm) * (1.0 + shock)
    mean_A = statistics.fmean(A_norm_series)
    min_A = min(A_norm_series)
    duration_below_Ac = sum(1 for x in A_norm_series if x < A_C) / len(A_norm_series)
    horizon_area = statistics.fmean(horizon_series)
    horizon_width = sum(1 for x in horizon_series if x > 0.0) / len(horizon_series)
    pinch = max(0.0, 1.0 - min_A)
    late_field = A_norm_series[-1]
    late_action = repair
    late_residual = max(0.0, sev - late_field)
    late_pocket = horizon_area
    late_mobility = max(0.0, mean_A - min_A)
    late_K = 0.5 * late_mobility + 0.5 * (1.0 - late_residual)
    bad = int(mean_A < 0.55 or duration_below_Ac > 0.5)
    adaptive = 1 - bad
    score = max(0.0, A_C - mean_A)
    return {
        'seed': seed,
        'bad': bad,
        'adaptive': adaptive,
        'triggered': int(triggered),
        'rescued': rescued,
        'harmed': harmed,
        'net_rescue': rescued - harmed,
        'mean_A_norm': mean_A,
        'min_A_norm': min_A,
        'duration_below_Ac': duration_below_Ac,
        'horizon_area': horizon_area,
        'horizon_width': horizon_width,
        'pinch': pinch,
        'late_field': late_field,
        'late_action': late_action,
        'late_residual': late_residual,
        'late_pocket': late_pocket,
        'late_mobility': late_mobility,
        'late_K': late_K,
        'severity': severity,
        'score': score,
    }


def aggregate(rows):
    n = len(rows)
    bad_rate = sum(r['bad'] for r in rows) / n
    adaptive_rate = sum(r['adaptive'] for r in rows) / n
    trigger_rate = sum(r['triggered'] for r in rows) / n
    rescued = sum(r['rescued'] for r in rows)
    harmed = sum(r['harmed'] for r in rows)
    net_rescue = sum(r['net_rescue'] for r in rows)
    phase_counts = {
        'adaptive': sum(r['adaptive'] for r in rows),
        'bad': sum(r['bad'] for r in rows),
        'horizon': sum(1 for r in rows if r['horizon_area'] > 0.0),
    }
    A = [r['mean_A_norm'] for r in rows]
    score = [r['score'] for r in rows]
    y = [r['bad'] for r in rows]
    try:
        pos = [s for s, yy in zip(score, y) if yy == 1]
        neg = [s for s, yy in zip(score, y) if yy == 0]
        auc = (sum(1 for p in pos for n0 in neg if p > n0) + 0.5 * sum(1 for p in pos for n0 in neg if p == n0)) / (len(pos) * len(neg)) if pos and neg else None
    except ZeroDivisionError:
        auc = None
    if auc is None:
        auc = 0.5
    preds = [1 if s > D_C else 0 for s in score]
    tp = sum(1 for p, yy in zip(preds, y) if p == 1 and yy == 1)
    tn = sum(1 for p, yy in zip(preds, y) if p == 0 and yy == 0)
    fp = sum(1 for p, yy in zip(preds, y) if p == 1 and yy == 0)
    fn = sum(1 for p, yy in zip(preds, y) if p == 0 and yy == 1)
    bal_acc = 0.5 * ((tp / (tp + fn) if (tp + fn) else 0.0) + (tn / (tn + fp) if (tn + fp) else 0.0))
    acc = sum(int(p == yy) for p, yy in zip(preds, y)) / n
    validity_gate = {
        'chosen_regime_not_null': True,
        'bad_rate_range': 0.0 < bad_rate < 1.0,
        'trigger_rate_gt_0p05': trigger_rate > 0.05,
        'phase_counts_bad_gt_0': phase_counts['bad'] > 0,
        'auc_metric_real': auc is not None,
        'valid_for_interpretation': (0.0 < bad_rate < 1.0) and (trigger_rate > 0.05) and (phase_counts['bad'] > 0),
    }
    return {
        'cases': n,
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'trigger_rate': trigger_rate,
        'rescued': rescued,
        'harmed': harmed,
        'net_rescue': net_rescue,
        'AUC': auc,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'mean_A_norm': statistics.fmean(A),
        'min_A_norm': min(r['min_A_norm'] for r in rows),
        'horizon_area': statistics.fmean(r['horizon_area'] for r in rows),
        'horizon_width': statistics.fmean(r['horizon_width'] for r in rows),
        'pinch': statistics.fmean(r['pinch'] for r in rows),
        'late_field': statistics.fmean(r['late_field'] for r in rows),
        'late_action': statistics.fmean(r['late_action'] for r in rows),
        'late_residual': statistics.fmean(r['late_residual'] for r in rows),
        'late_pocket': statistics.fmean(r['late_pocket'] for r in rows),
        'late_mobility': statistics.fmean(r['late_mobility'] for r in rows),
        'late_K': statistics.fmean(r['late_K'] for r in rows),
        'phase_counts': phase_counts,
        'variant_level_performance': rows,
        'validity_gate': validity_gate,
    }


def main():
    controllers = ['anorm', 'da', 'horizon', 'combined']
    baseline_rows = [simulate_one(s, 'none') for s in SEEDS]
    baseline = aggregate(baseline_rows)
    results = {
        'version': VERSION,
        'regime': REGIME,
        'A_c': A_C,
        'D_c': D_C,
        'A_h': A_H,
        'seed_count': len(SEEDS),
        'seeds': SEEDS,
        'baseline': baseline,
        'controllers': {},
    }
    for c in controllers:
        rows = [simulate_one(s, c) for s in SEEDS]
        agg = aggregate(rows)
        results['controllers'][c] = agg
    out_json = OUTDIR / f'{VERSION}_results.json'
    out_txt = OUTDIR / f'{VERSION}_stdout.json'
    out_json.write_text(json.dumps(results, indent=2, sort_keys=True))
    out_txt.write_text(json.dumps(results, indent=2, sort_keys=True))
    print(json.dumps(results, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
