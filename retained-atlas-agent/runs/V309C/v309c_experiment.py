import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Dict, List, Tuple

import numpy as np

OUTDIR = Path('runs/V309C')
OUTDIR.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388
A_H = 0.1

rng_global = np.random.default_rng(12345)

@dataclass
class SimResult:
    bad: np.ndarray
    adaptive: np.ndarray
    score_full: np.ndarray
    score_map: Dict[str, np.ndarray]
    phase_counts: Dict[str, int]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def simulate_one(seed: int, severity: float = 1.0) -> SimResult:
    rng = np.random.default_rng(seed)
    T = N_STEPS
    x = np.zeros(T)
    y = np.zeros(T)
    z = np.zeros(T)
    bad = np.zeros(T, dtype=int)
    adaptive = np.zeros(T, dtype=int)
    rf = np.zeros(T)
    cw = np.zeros(T)
    be = np.zeros(T)
    dr = np.zeros(T)
    rv = np.zeros(T)
    score_full = np.zeros(T)
    score_map = {k: np.zeros(T) for k in ['no_rf', 'no_cw', 'no_be', 'no_dr', 'no_rv']}

    for t in range(T):
        shock = 0.0
        if t in (12, 13, 24, 25, 36, 37, 48, 49):
            shock += severity * (0.85 + 0.3 * rng.random())
        if rng.random() < 0.08 * severity:
            shock += severity * (0.25 + 0.5 * rng.random())

        x[t] = 1.0 + 0.08 * rng.normal() - 0.35 * shock
        y[t] = 1.0 + 0.07 * rng.normal() - 0.30 * shock
        z[t] = 1.0 + 0.06 * rng.normal() - 0.28 * shock

        # reachability components; clipped positive to avoid degenerate negatives
        rf[t] = max(0.02, 1.05 + 0.20 * np.tanh(0.8 * x[t] - 0.7 * shock) + 0.05 * rng.normal())
        cw[t] = max(0.02, 1.00 + 0.18 * np.tanh(0.7 * y[t] - 0.6 * shock) + 0.05 * rng.normal())
        be[t] = max(0.02, 0.95 + 0.22 * np.tanh(0.6 * z[t] - 0.5 * shock) + 0.06 * rng.normal())
        dr[t] = max(0.02, 0.90 + 0.24 * np.tanh(0.7 * (x[t] + y[t]) - 0.7 * shock) + 0.06 * rng.normal())
        rv[t] = max(0.02, 0.92 + 0.21 * np.tanh(0.5 * (x[t] + z[t]) - 0.6 * shock) + 0.05 * rng.normal())

        score_full[t] = (rf[t] * cw[t] * be[t] * dr[t] * rv[t]) ** 0.2
        score_map['no_rf'][t] = (1.0 * cw[t] * be[t] * dr[t] * rv[t]) ** 0.2
        score_map['no_cw'][t] = (rf[t] * 1.0 * be[t] * dr[t] * rv[t]) ** 0.2
        score_map['no_be'][t] = (rf[t] * cw[t] * 1.0 * dr[t] * rv[t]) ** 0.2
        score_map['no_dr'][t] = (rf[t] * cw[t] * be[t] * 1.0 * rv[t]) ** 0.2
        score_map['no_rv'][t] = (rf[t] * cw[t] * be[t] * dr[t] * 1.0) ** 0.2

        A_norm = score_full[t]
        # bad state is induced when reachability is low and deficit/horizon are high
        deficit = max(0.0, A_C - A_norm)
        horizon = max(0.0, A_H - A_norm)
        bad_prob = sigmoid(-1.0 + 7.0 * deficit + 8.5 * horizon + 1.8 * shock)
        adaptive_prob = sigmoid(1.4 + 2.0 * (A_norm - A_C) - 0.8 * shock)
        bad[t] = int(rng.random() < bad_prob)
        adaptive[t] = int(rng.random() < adaptive_prob)

        # mild autocorrelation to produce a realistic sequence structure
        if t > 0:
            bad[t] = int((bad[t] or (bad[t-1] and rng.random() < 0.35)))
            adaptive[t] = int((adaptive[t] or (adaptive[t-1] and rng.random() < 0.30)))

    phase_counts = {'bad': int(bad.sum()), 'safe': int(T * len(SEEDS) - bad.sum())}
    return SimResult(bad=bad, adaptive=adaptive, score_full=score_full, score_map=score_map, phase_counts=phase_counts)


def auc_score(y_true: np.ndarray, scores: np.ndarray) -> float:
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores).astype(float)
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    # Mann-Whitney U / AUC
    ranks = scores.argsort().argsort().astype(float) + 1.0
    rank_sum_pos = ranks[y_true == 1].sum()
    n1 = len(pos)
    n0 = len(neg)
    u = rank_sum_pos - n1 * (n1 + 1) / 2.0
    return float(u / (n0 * n1))


def balanced_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    return float(0.5 * (tpr + tnr))


def compute_metrics(y_true, scores, threshold):
    y_pred = (scores >= threshold).astype(int)
    return {
        'AUC': auc_score(y_true, scores),
        'balanced_accuracy': balanced_accuracy(y_true, y_pred),
        'accuracy': float((y_true == y_pred).mean()),
        'trigger_rate': float(y_pred.mean()),
        'mean_bad': float(scores[y_true == 1].mean()) if np.any(y_true == 1) else 0.0,
        'mean_safe': float(scores[y_true == 0].mean()) if np.any(y_true == 0) else 0.0,
        'corr': float(np.corrcoef(y_true, scores)[0, 1]) if np.std(scores) > 0 and np.std(y_true) > 0 else 0.0,
    }


def eval_policy(y_true, base_scores, policy_name, threshold):
    scores = base_scores.copy()
    if policy_name == 'A_full':
        pass
    elif policy_name == 'no_rf':
        pass
    elif policy_name == 'no_cw':
        pass
    elif policy_name == 'no_be':
        pass
    elif policy_name == 'no_dr':
        pass
    elif policy_name == 'no_rv':
        pass
    return compute_metrics(y_true, scores, threshold)


def run_regime(severity: float):
    all_bad = []
    all_adaptive = []
    all_scores = []
    all_scores_map = {k: [] for k in ['A_full', 'no_rf', 'no_cw', 'no_be', 'no_dr', 'no_rv']}
    phase_counts = {'bad': 0, 'safe': 0}

    for seed in SEEDS:
        sim = simulate_one(seed, severity=severity)
        all_bad.append(sim.bad)
        all_adaptive.append(sim.adaptive)
        all_scores.append(sim.score_full)
        all_scores_map['A_full'].append(sim.score_full)
        all_scores_map['no_rf'].append(sim.score_map['no_rf'])
        all_scores_map['no_cw'].append(sim.score_map['no_cw'])
        all_scores_map['no_be'].append(sim.score_map['no_be'])
        all_scores_map['no_dr'].append(sim.score_map['no_dr'])
        all_scores_map['no_rv'].append(sim.score_map['no_rv'])
        phase_counts['bad'] += sim.phase_counts['bad']
        phase_counts['safe'] += sim.phase_counts['safe']

    y = np.concatenate(all_bad)
    adaptive = np.concatenate(all_adaptive)
    full_scores = np.concatenate(all_scores)

    # threshold from calibration on full score, no tuning per variant
    threshold = float(np.quantile(full_scores, 0.60))

    metrics = {}
    for name, arrs in all_scores_map.items():
        scores = np.concatenate(arrs)
        metrics[name] = compute_metrics(y, scores, threshold)

    summary = {
        'bad_rate': float(y.mean()),
        'adaptive_rate': float(adaptive.mean()),
        'mean_A_norm': float(full_scores.mean()),
        'min_A_norm': float(full_scores.min()),
        'score_mean': float(full_scores.mean()),
        'score_var': float(full_scores.var()),
        'threshold': threshold,
        'phase_counts': phase_counts,
    }

    validity_gate = {
        'nondegenerate_bad_rate': 0.20 <= summary['bad_rate'] <= 0.40,
        'nonzero_score_variance': summary['score_var'] > 0.0,
        'nonzero_trigger_rate': metrics['A_full']['trigger_rate'] > 0.0,
        'enough_positive_cases': int(y.sum()) >= 50,
    }
    validity_gate['valid_for_interpretation'] = all(validity_gate.values())

    return summary, metrics, validity_gate


def choose_regime():
    candidates = [0.8, 1.0, 1.2, 1.4, 1.6]
    scored = []
    for sev in candidates:
        summary, metrics, gate = run_regime(sev)
        scored.append((sev, summary, metrics, gate))
        if gate['nondegenerate_bad_rate']:
            return sev, summary, metrics, gate, scored
    # fallback to closest bad rate
    scored.sort(key=lambda x: abs(x[1]['bad_rate'] - 0.30))
    return scored[0][0], scored[0][1], scored[0][2], scored[0][3], scored


def main():
    severity, summary, metrics, gate, sweep = choose_regime()
    results = {
        'version': 'V309C',
        'title': 'Regime redesign and nondegenerate component ablation',
        'config': {
            'seeds': SEEDS,
            'n_steps': N_STEPS,
            'A_c': A_C,
            'D_c': D_C,
            'A_h': A_H,
            'chosen_severity': severity,
            'sweep': [
                {
                    'severity': float(sev),
                    'bad_rate': float(sumr['bad_rate']),
                    'score_var': float(sumr['score_var']),
                    'trigger_rate': float(met['A_full']['trigger_rate']),
                    'valid_for_interpretation': bool(g['valid_for_interpretation'])
                }
                for sev, sumr, met, g in sweep
            ],
        },
        'summary': summary,
        'results': metrics,
        'validity_gate': gate,
        'decision': 'branch' if not gate['valid_for_interpretation'] else 'continue',
        'next': 'If valid_for_interpretation is true, interpret component drops; otherwise redesign harness again.',
    }

    outpath = OUTDIR / 'V309C_results.json'
    with outpath.open('w') as f:
        json.dump(results, f, indent=2, sort_keys=True)
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
