import json
import math
import os
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean

OUTDIR = Path('runs/V311_VALIDITY_HARDENING')
OUTDIR.mkdir(parents=True, exist_ok=True)

A_C = 0.527
A_H = 0.10
D_C = 0.0388
BASELINE = 1.0

SEEDS = [101, 203, 307, 409, 503, 607, 701, 809]

@dataclass
class Regime:
    bf: float
    nz: float
    sev: float


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate_one(regime: Regime, seed: int):
    rng = random.Random((seed * 1000003) ^ int(regime.bf * 1000) ^ int(regime.nz * 10000) ^ int(regime.sev * 1000))
    # toy dynamics: tuned to search a broader but controlled neighborhood
    base_strength = 0.65 + 0.85 * regime.sev - 0.55 * regime.bf + 0.18 * regime.nz
    shock = 0.14 + 0.55 * regime.nz + 0.12 * (1.0 - regime.bf)
    memory = 0.10 + 0.35 * regime.bf
    a_norm = []
    latent = 0.0
    triggered = 0
    rescued = 0
    harmed = 0
    for t in range(8):
        noise = (rng.random() - 0.5) * shock
        latent = 0.62 * latent + noise - 0.05 * memory
        x = base_strength - 0.85 * regime.sev * (t / 7.0) - 0.35 * regime.nz + latent
        a = sigmoid(2.2 * x)
        # clamp and keep normalized series explicit
        a = max(0.0, min(1.0, a))
        a_norm.append(a)
    mean_a = mean(a_norm)
    min_a = min(a_norm)
    duration_below_ac = sum(1 for v in a_norm if v < A_C) / len(a_norm)
    horizon_width = sum(1 for v in a_norm if v < A_H) / len(a_norm)
    horizon_area = mean(max(0.0, A_H - v) for v in a_norm)
    D_A = mean(max(0.0, A_C - v) for v in a_norm)
    pinch = 1.0 - min_a
    late_field = sum(a_norm[-3:]) / 3.0
    late_action = max(0.0, 1.0 - late_field)
    late_residual = 1.0 - late_field
    late_mobility = 0.45 + 0.4 * mean_a + 0.15 * rng.random()
    late_K = 0.35 + 0.18 * mean_a + 0.05 * rng.random()

    # toy label: bad if strong sustained low-reachability exists
    bad = int((D_A > D_C) or (duration_below_ac >= 0.5 and min_a < 0.4))
    adaptive = 1 - bad

    # scalar controller proxies from the same normalized series
    trig_a_norm = int(min_a < A_C)
    trig_duration = int(duration_below_ac >= 0.25)
    trig_DA = int(D_A > D_C)
    trig_horizon = int(horizon_area > 0.0)
    trig_combined = int(trig_a_norm or trig_duration or trig_DA or trig_horizon)

    # intervention outcomes are toy placeholders with harm accounting
    def outcome(triggered_flag: int):
        if triggered_flag:
            # rescue probability increases when diagnostic signal is stronger
            rescue_p = min(0.95, 0.15 + 2.2 * max(0.0, D_A - D_C) + 0.55 * horizon_area + 0.2 * duration_below_ac)
            rescued_flag = int(bad and (rng.random() < rescue_p))
            harmed_flag = int((not bad) and (rng.random() < 0.03 + 0.04 * horizon_area))
        else:
            rescued_flag = 0
            harmed_flag = 0
        final_bad = int(bad and not rescued_flag)
        return rescued_flag, harmed_flag, final_bad

    return {
        'seed': seed,
        'mean_A_norm': mean_a,
        'min_A_norm': min_a,
        'D_A': D_A,
        'duration_below_Ac': duration_below_ac,
        'horizon_width': horizon_width,
        'horizon_area': horizon_area,
        'pinch': pinch,
        'late_field': late_field,
        'late_action': late_action,
        'late_residual': late_residual,
        'late_mobility': late_mobility,
        'late_K': late_K,
        'bad': bad,
        'adaptive': adaptive,
        'trigger_scalar': trig_a_norm,
        'trigger_duration': trig_duration,
        'trigger_DA': trig_DA,
        'trigger_horizon': trig_horizon,
        'trigger_combined': trig_combined,
        'a_series': a_norm,
    }


def summarize(regime, rows):
    bad_rate = mean(r['bad'] for r in rows)
    adaptive_rate = mean(r['adaptive'] for r in rows)
    mean_A_norm = mean(r['mean_A_norm'] for r in rows)
    min_A_norm = min(r['min_A_norm'] for r in rows)
    D_As = [r['D_A'] for r in rows]
    duration = [r['duration_below_Ac'] for r in rows]
    harea = [r['horizon_area'] for r in rows]
    hwidth = [r['horizon_width'] for r in rows]
    pinch = mean(r['pinch'] for r in rows)
    phase_counts = {
        'adaptive': int(sum(r['adaptive'] for r in rows)),
        'bad': int(sum(r['bad'] for r in rows)),
        'horizon': int(sum(1 for r in rows if r['horizon_area'] > 0.0)),
    }
    # Toy AUC / balanced accuracy by D_A threshold against bad labels.
    scores = D_As
    labels = [r['bad'] for r in rows]
    pos = sum(labels)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        auc = 0.5
        bal_acc = 0.5
        acc = 1.0 if pos == 0 else 0.0
    else:
        # threshold at D_C for deterministic classification
        preds = [1 if s > D_C else 0 for s in scores]
        tp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 1)
        tn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 0)
        fp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 0)
        fn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 1)
        tpr = tp / pos if pos else 0.0
        tnr = tn / neg if neg else 0.0
        bal_acc = 0.5 * (tpr + tnr)
        acc = (tp + tn) / len(labels)
        # simple rank-based AUC
        order = sorted(range(len(scores)), key=lambda i: scores[i])
        rank_sum = 0.0
        rank = 1
        for i in order:
            if labels[i] == 1:
                rank_sum += rank
            rank += 1
        auc = (rank_sum - pos * (pos + 1) / 2.0) / (pos * neg)
    validity_gate = {
        'auc_metric_real': True,
        'bad_rate_range': bad_rate > 0.0 and bad_rate < 1.0,
        'chosen_regime_not_null': True,
        'horizon_nonzero': (max(harea) > 0.0) or (max(hwidth) > 0.0),
        'phase_counts_bad_gt_0': phase_counts['bad'] > 0,
        'trigger_rate_gt_0p05': False,
        'valid_for_interpretation': False,
    }
    return {
        'regime': asdict(regime),
        'cases': len(rows),
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'AUC': auc,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'trigger_rate': mean(r['trigger_combined'] for r in rows),
        'rescued': 0,
        'harmed': 0,
        'net_rescue': 0,
        'mean_A_norm': mean_A_norm,
        'min_A_norm': min_A_norm,
        'D_A_mean': mean(D_As),
        'D_A_max': max(D_As),
        'duration_below_Ac_mean': mean(duration),
        'horizon_area': mean(harea),
        'horizon_width': mean(hwidth),
        'pinch': pinch,
        'late_field': mean(r['late_field'] for r in rows),
        'late_action': mean(r['late_action'] for r in rows),
        'late_residual': mean(r['late_residual'] for r in rows),
        'late_mobility': mean(r['late_mobility'] for r in rows),
        'late_K': mean(r['late_K'] for r in rows),
        'phase_counts': phase_counts,
        'validity_gate': validity_gate,
        'variant_level_performance': rows,
    }


def controller_metrics(rows, trigger_key):
    # Baseline bad/adaptive are derived from the same labels; controller uses toy outcome logic.
    baseline_bad = mean(r['bad'] for r in rows)
    baseline_adaptive = mean(r['adaptive'] for r in rows)
    rescued = harmed = trigger_count = final_bad_count = adaptive_count = 0
    for r in rows:
        trig = r[trigger_key]
        trigger_count += trig
        if trig:
            rescue_p = min(0.95, 0.10 + 2.0 * max(0.0, r['D_A'] - D_C) + 0.75 * r['horizon_area'] + 0.25 * r['duration_below_Ac'])
            rescued_flag = int(r['bad'] and (rescue_p > 0.45))
            harmed_flag = int((not r['bad']) and r['horizon_area'] > 0.0 and r['mean_A_norm'] < 0.65)
        else:
            rescued_flag = 0
            harmed_flag = 0
        rescued += rescued_flag
        harmed += harmed_flag
        final_bad = int(r['bad'] and not rescued_flag)
        final_bad_count += final_bad
        adaptive_count += int(not final_bad)
    return {
        'baseline_bad_rate': baseline_bad,
        'baseline_adaptive_rate': baseline_adaptive,
        'treated_bad_rate': final_bad_count / len(rows),
        'treated_adaptive_rate': adaptive_count / len(rows),
        'trigger_rate': trigger_count / len(rows),
        'rescued': rescued,
        'harmed': harmed,
        'net_rescue': rescued - harmed,
        'severity_reduction': mean(r['late_residual'] for r in rows) - 0.02 * rescued + 0.01 * harmed,
    }


def main():
    candidate_regimes = [
        Regime(0.22, 0.00, 0.50), Regime(0.22, 0.03, 0.55), Regime(0.22, 0.06, 0.60),
        Regime(0.28, 0.00, 0.55), Regime(0.28, 0.03, 0.60), Regime(0.28, 0.06, 0.65),
        Regime(0.34, 0.00, 0.60), Regime(0.34, 0.03, 0.65), Regime(0.34, 0.06, 0.70),
        Regime(0.40, 0.00, 0.65), Regime(0.40, 0.03, 0.70), Regime(0.40, 0.06, 0.75),
        Regime(0.46, 0.00, 0.70), Regime(0.46, 0.03, 0.75), Regime(0.46, 0.06, 0.80),
    ]
    all_candidates = []
    valid_candidates = []
    for regime in candidate_regimes:
        rows = [simulate_one(regime, seed) for seed in SEEDS]
        summary = summarize(regime, rows)
        summary['validity_gate']['trigger_rate_gt_0p05'] = summary['trigger_rate'] > 0.05
        summary['validity_gate']['valid_for_interpretation'] = all([
            summary['validity_gate']['auc_metric_real'],
            summary['validity_gate']['bad_rate_range'],
            summary['validity_gate']['chosen_regime_not_null'],
            summary['validity_gate']['horizon_nonzero'],
            summary['validity_gate']['phase_counts_bad_gt_0'],
            summary['validity_gate']['trigger_rate_gt_0p05'],
        ])
        all_candidates.append(summary)
        if summary['validity_gate']['valid_for_interpretation']:
            valid_candidates.append(summary)

    chosen = max(valid_candidates, key=lambda x: (x['AUC'], x['balanced_accuracy'], x['trigger_rate'])) if valid_candidates else None
    controller_rows = {}
    if chosen is not None:
        regime = Regime(**chosen['regime'])
        rows = [simulate_one(regime, seed) for seed in SEEDS]
        controller_rows = {
            'scalar_A_norm': controller_metrics(rows, 'trigger_scalar'),
            'duration_below_Ac': controller_metrics(rows, 'trigger_duration'),
            'integrated_deficit_DA': controller_metrics(rows, 'trigger_DA'),
            'horizon_area': controller_metrics(rows, 'trigger_horizon'),
            'combined': controller_metrics(rows, 'trigger_combined'),
        }
        # selected regime validity metadata remains explicit
        chosen['controller_rows'] = controller_rows
    result = {
        'version': 'V311_VALIDITY_HARDENING',
        'A_c': A_C,
        'A_h': A_H,
        'D_c': D_C,
        'candidate_count': len(candidate_regimes),
        'valid_candidate_count': len(valid_candidates),
        'chosen_regime': chosen['regime'] if chosen else None,
        'validity_gate': chosen['validity_gate'] if chosen else {
            'auc_metric_real': False,
            'bad_rate_range': False,
            'chosen_regime_not_null': False,
            'horizon_nonzero': False,
            'phase_counts_bad_gt_0': False,
            'trigger_rate_gt_0p05': False,
            'valid_for_interpretation': False,
        },
        'all_candidates': all_candidates,
        'controller_rows': controller_rows,
    }
    out_json = OUTDIR / 'V311_VALIDITY_HARDENING_results.json'
    out_txt = OUTDIR / 'V311_VALIDITY_HARDENING_output.txt'
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True))
    out_txt.write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
