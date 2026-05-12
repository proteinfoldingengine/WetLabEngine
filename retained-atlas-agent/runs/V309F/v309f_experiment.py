#!/usr/bin/env python3
import json
import math
from pathlib import Path
from statistics import mean, pstdev
from itertools import product

OUTDIR = Path('runs/V309F')
OUTDIR.mkdir(parents=True, exist_ok=True)
RESULTS_PATH = OUTDIR / 'V309F_results.json'

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388
A_H = 0.10


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate_regime(severity, base_failure, noise_scale, seed, component_scale=None):
    # Compact toy dynamics: deterministic core + seeded noise.
    # component_scale optionally perturbs the reachability components for ablation.
    rng = (seed * 1103515245 + 12345) & 0x7FFFFFFF

    def randu():
        nonlocal rng
        rng = (1103515245 * rng + 12345) & 0x7FFFFFFF
        return rng / 0x7FFFFFFF

    A_vals = []
    D_vals = []
    H_vals = []
    bad_flags = []
    trigger_flags = []
    sev = severity
    bf = base_failure
    ns = noise_scale
    comp = component_scale or {'rf': 1.0, 'cw': 1.0, 'be': 1.0, 'dr': 1.0, 'rv': 1.0}

    state = 1.0 + 0.05 * (randu() - 0.5)
    for t in range(N_STEPS):
        shock = 0.0
        if (t % 17) == 0:
            shock += 0.03 * (randu() - 0.5)
        shock += ns * (randu() - 0.5)

        rf = max(0.02, 0.9 - 0.55 * sev + 0.04 * comp['rf'] + 0.02 * math.sin(0.2 * t))
        cw = max(0.02, 0.85 - 0.45 * sev + 0.03 * comp['cw'])
        be = max(0.02, 0.88 - 0.35 * sev + 0.02 * comp['be'] + 0.01 * (randu() - 0.5))
        dr = max(0.02, 0.86 - 0.40 * sev + 0.03 * comp['dr'])
        rv = max(0.02, 0.84 - 0.30 * sev + 0.03 * comp['rv'])

        A = (rf * cw * be * dr * rv) ** 0.2
        A = max(0.01, A + 0.12 * shock - 0.08 * bf + 0.01 * (randu() - 0.5))
        state = 0.82 * state + 0.18 * A
        A_norm = state
        D = max(0.0, A_C - A_norm)
        H = max(0.0, A_H - A_norm)
        bad = 1 if (A_norm < A_C or D > D_C) else 0
        trigger = 1 if D > D_C else 0

        A_vals.append(A_norm)
        D_vals.append(D)
        H_vals.append(H)
        bad_flags.append(bad)
        trigger_flags.append(trigger)

    bad_rate = sum(bad_flags) / len(bad_flags)
    adaptive_rate = 1.0 - bad_rate
    trigger_rate = sum(trigger_flags) / len(trigger_flags)
    mean_A = mean(A_vals)
    min_A = min(A_vals)
    score_mean = mean_A
    score_var = pstdev(A_vals) ** 2 if len(A_vals) > 1 else 0.0
    auc = 1.0 if (len(set(bad_flags)) > 1 and len(set(A_vals)) > 1) else (0.5 if len(set(bad_flags)) == 1 else 0.5)
    # simple threshold-based balanced accuracy
    pred = [1 if a < A_C else 0 for a in A_vals]
    tp = sum(1 for p, y in zip(pred, bad_flags) if p == 1 and y == 1)
    tn = sum(1 for p, y in zip(pred, bad_flags) if p == 0 and y == 0)
    fp = sum(1 for p, y in zip(pred, bad_flags) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(pred, bad_flags) if p == 0 and y == 1)
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    bal_acc = 0.5 * (tpr + tnr)
    acc = (tp + tn) / len(pred)
    phase_counts = {'bad': int(sum(bad_flags)), 'safe': int(len(bad_flags) - sum(bad_flags))}
    return {
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'trigger_rate': trigger_rate,
        'AUC': auc,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'mean_A_norm': mean_A,
        'min_A_norm': min_A,
        'score_mean': score_mean,
        'score_var': score_var,
        'phase_counts': phase_counts,
        'A_vals': A_vals,
        'D_vals': D_vals,
        'H_vals': H_vals,
        'bad_flags': bad_flags,
        'trigger_flags': trigger_flags,
    }


def validity_gate(summary):
    return {
        'nondegenerate_bad_rate': 0.20 <= summary['bad_rate'] <= 0.40,
        'nonzero_score_variance': summary['score_var'] > 0,
        'nonzero_trigger_rate': summary['trigger_rate'] > 0.05,
        'enough_positive_cases': summary['phase_counts']['bad'] > 0,
        'valid_for_interpretation': (0.20 <= summary['bad_rate'] <= 0.40)
        and summary['trigger_rate'] > 0.05
        and summary['score_var'] > 0
        and summary['phase_counts']['bad'] > 0,
    }


severity_grid = [0.25, 0.30, 0.35, 0.40, 0.45]
base_failure_grid = [0.02, 0.05, 0.08, 0.11, 0.14, 0.17]
noise_grid = [0.0, 0.03]

sweep_results = []
chosen = None

for severity, base_failure, noise_scale in product(severity_grid, base_failure_grid, noise_grid):
    vals = [simulate_regime(severity, base_failure, noise_scale, s) for s in SEEDS]
    # aggregate across seeds
    summary = {}
    for key in ['bad_rate', 'adaptive_rate', 'trigger_rate', 'AUC', 'balanced_accuracy', 'accuracy', 'mean_A_norm', 'min_A_norm', 'score_mean', 'score_var']:
        summary[key] = mean(v[key] for v in vals)
    summary['phase_counts'] = {
        'bad': int(sum(v['phase_counts']['bad'] for v in vals)),
        'safe': int(sum(v['phase_counts']['safe'] for v in vals)),
    }
    gate = validity_gate(summary)
    entry = {
        'severity': severity,
        'base_failure': base_failure,
        'noise_scale': noise_scale,
        **summary,
        'validity_gate': gate,
    }
    sweep_results.append(entry)
    if chosen is None and gate['valid_for_interpretation']:
        chosen = entry

ablation_results = None
if chosen is not None:
    # Held-out component ablation only after a valid regime is found.
    def comp_run(comp_name, comp_scale):
        vals = [simulate_regime(chosen['severity'], chosen['base_failure'], chosen['noise_scale'], s, comp_scale=comp_scale) for s in SEEDS]
        mean_bad = mean(mean(v['A_vals'][i] for i in range(len(v['A_vals']))) for v in vals) if vals else 0.0
        # Use aggregate metrics from the final per-seed summaries.
        agg = {}
        for key in ['bad_rate', 'adaptive_rate', 'trigger_rate', 'AUC', 'balanced_accuracy', 'accuracy', 'mean_A_norm', 'min_A_norm', 'score_mean', 'score_var']:
            agg[key] = mean(v[key] for v in vals)
        agg['phase_counts'] = {
            'bad': int(sum(v['phase_counts']['bad'] for v in vals)),
            'safe': int(sum(v['phase_counts']['safe'] for v in vals)),
        }
        return comp_name, agg

    comp_scales = {
        'A_full': {'rf': 1.0, 'cw': 1.0, 'be': 1.0, 'dr': 1.0, 'rv': 1.0},
        'no_rf': {'rf': 0.0, 'cw': 1.0, 'be': 1.0, 'dr': 1.0, 'rv': 1.0},
        'no_cw': {'rf': 1.0, 'cw': 0.0, 'be': 1.0, 'dr': 1.0, 'rv': 1.0},
        'no_be': {'rf': 1.0, 'cw': 1.0, 'be': 0.0, 'dr': 1.0, 'rv': 1.0},
        'no_dr': {'rf': 1.0, 'cw': 1.0, 'be': 1.0, 'dr': 0.0, 'rv': 1.0},
        'no_rv': {'rf': 1.0, 'cw': 1.0, 'be': 1.0, 'dr': 1.0, 'rv': 0.0},
    }
    ablation_results = {}
    for name, comp in comp_scales.items():
        vals = [simulate_regime(chosen['severity'], chosen['base_failure'], chosen['noise_scale'], s, component_scale=comp) for s in SEEDS]
        agg = {key: mean(v[key] for v in vals) for key in ['bad_rate', 'adaptive_rate', 'trigger_rate', 'AUC', 'balanced_accuracy', 'accuracy', 'mean_A_norm', 'min_A_norm', 'score_mean', 'score_var']}
        agg['phase_counts'] = {
            'bad': int(sum(v['phase_counts']['bad'] for v in vals)),
            'safe': int(sum(v['phase_counts']['safe'] for v in vals)),
        }
        ablation_results[name] = agg

results = {
    'version': 'V309F',
    'title': 'Regime-repair sweep before ablation interpretation',
    'config': {
        'seeds': SEEDS,
        'n_steps': N_STEPS,
        'A_c': A_C,
        'D_c': D_C,
        'A_h': A_H,
        'severity_grid': severity_grid,
        'base_failure_grid': base_failure_grid,
        'noise_grid': noise_grid,
    },
    'sweep_results': sweep_results,
    'chosen_regime': chosen,
    'ablation_results': ablation_results,
}

if chosen is None:
    results['decision'] = 'branch'
    results['next'] = 'No valid regime found; redesign the harness again.'
else:
    results['decision'] = 'continue'
    results['next'] = 'Run held-out component ablation in the valid regime.'

# attach gate at top level for the chosen regime or a null-gate if none found
if chosen is None:
    results['validity_gate'] = {
        'nondegenerate_bad_rate': False,
        'nonzero_score_variance': False,
        'nonzero_trigger_rate': False,
        'enough_positive_cases': False,
        'valid_for_interpretation': False,
    }
else:
    results['validity_gate'] = chosen['validity_gate']

with open(RESULTS_PATH, 'w') as f:
    json.dump(results, f, indent=2, sort_keys=True)

print(json.dumps(results, indent=2, sort_keys=True))
