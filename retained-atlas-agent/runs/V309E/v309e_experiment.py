import json
import math
import os
from pathlib import Path
from statistics import mean
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, accuracy_score

ROOT = Path(__file__).resolve().parent
RUN_DIR = ROOT / 'runs' / 'V309E'
RUN_DIR.mkdir(parents=True, exist_ok=True)
RESULT_PATH = RUN_DIR / 'V309E_results.json'

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388

# Deterministic toy generator. This is intentionally compact and self-contained.
def simulate_regime(severity, base_failure, noise_scale, seed):
    y_true = []
    score = []
    A_norm_vals = []
    phase_counts = {'bad': 0, 'safe': 0}
    trigger_count = 0
    adaptive_count = 0
    A_baseline = 1.0

    for t in range(N_STEPS):
        # deterministic pseudo-dynamics with seed/step interaction
        x = (seed + 1) * 0.173 + (t + 1) * 0.119
        osc = math.sin(x) + 0.5 * math.cos(0.7 * x)
        drift = 0.08 * severity - 0.03 * base_failure
        noise = noise_scale * (math.sin(1.7 * x) + math.cos(0.9 * x)) * 0.5

        # Toy reachability components
        R_f = max(0.0, 0.95 - 0.35 * severity + 0.12 * osc + noise)
        C_w = max(0.0, 0.85 - 0.25 * base_failure + 0.08 * math.sin(0.5 * x) + noise)
        B_e = max(0.0, 0.78 + 0.10 * math.cos(0.8 * x) - 0.10 * severity + noise)
        D_r = max(0.0, 0.88 - 0.20 * severity + 0.06 * math.sin(1.1 * x) + noise)
        R_v = max(0.0, 0.92 - 0.18 * base_failure + 0.05 * math.cos(1.3 * x) + noise)

        A = (R_f * C_w * B_e * D_r * R_v) ** 0.2 if R_f * C_w * B_e * D_r * R_v > 0 else 0.0
        A_norm = A / A_baseline
        D_A = max(0.0, A_C - A_norm)
        horizon_area = max(0.0, 0.10 - A_norm)

        # Label is a toy bad-state function calibrated to yield a nondegenerate window for some regimes.
        bad_score = (
            1.9 * severity
            + 1.4 * base_failure
            - 0.9 * A_norm
            + 0.35 * math.sin(x)
            + 0.25 * noise_scale * math.cos(1.4 * x)
            + drift
        )
        bad = 1 if bad_score > 0.55 else 0

        # Trigger proxy: a combined reachability alarm that is active only when inaccessible future-state persists.
        trigger = 1 if (D_A > D_C and horizon_area > 0.0) else 0
        adaptive = 1 if A_norm > A_C else 0

        y_true.append(bad)
        score.append(A_norm)
        A_norm_vals.append(A_norm)
        phase_counts['bad'] += bad
        phase_counts['safe'] += (1 - bad)
        trigger_count += trigger
        adaptive_count += adaptive

    bad_rate = mean(y_true)
    adaptive_rate = adaptive_count / N_STEPS
    trigger_rate = trigger_count / N_STEPS
    mean_A_norm = mean(A_norm_vals)
    min_A_norm = min(A_norm_vals)
    score_mean = mean(score)
    score_var = mean([(s - score_mean) ** 2 for s in score])
    try:
        auc = roc_auc_score(y_true, score)
    except Exception:
        auc = 0.5
    preds = [1 if s < A_C else 0 for s in score]
    bal_acc = balanced_accuracy_score(y_true, preds)
    acc = accuracy_score(y_true, preds)

    validity_gate = {
        'nondegenerate_bad_rate': (0.20 <= bad_rate <= 0.40),
        'nonzero_score_variance': (score_var > 0),
        'nonzero_trigger_rate': (trigger_rate > 0.05),
        'enough_positive_cases': (sum(y_true) >= 10),
        'valid_for_interpretation': False,
    }
    validity_gate['valid_for_interpretation'] = all([
        validity_gate['nondegenerate_bad_rate'],
        validity_gate['nonzero_score_variance'],
        validity_gate['nonzero_trigger_rate'],
        validity_gate['enough_positive_cases'],
    ])

    return {
        'bad_rate': bad_rate,
        'adaptive_rate': adaptive_rate,
        'trigger_rate': trigger_rate,
        'AUC': auc,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'mean_A_norm': mean_A_norm,
        'min_A_norm': min_A_norm,
        'score_mean': score_mean,
        'score_var': score_var,
        'phase_counts': phase_counts,
        'validity_gate': validity_gate,
    }

# 2D sweep over severity and base_failure; noise included to satisfy regime repair instructions.
severity_grid = [0.25, 0.30, 0.35, 0.40, 0.45]
base_failure_grid = [0.02, 0.05, 0.08, 0.11, 0.14, 0.17]
noise_grid = [0.0, 0.03]

sweep_results = []
valid_candidates = []
for severity in severity_grid:
    for base_failure in base_failure_grid:
        for noise_scale in noise_grid:
            per_seed = [simulate_regime(severity, base_failure, noise_scale, s) for s in SEEDS]
            agg = {
                'severity': severity,
                'base_failure': base_failure,
                'noise_scale': noise_scale,
                'bad_rate': mean([r['bad_rate'] for r in per_seed]),
                'adaptive_rate': mean([r['adaptive_rate'] for r in per_seed]),
                'trigger_rate': mean([r['trigger_rate'] for r in per_seed]),
                'AUC': mean([r['AUC'] for r in per_seed]),
                'balanced_accuracy': mean([r['balanced_accuracy'] for r in per_seed]),
                'accuracy': mean([r['accuracy'] for r in per_seed]),
                'mean_A_norm': mean([r['mean_A_norm'] for r in per_seed]),
                'min_A_norm': min([r['min_A_norm'] for r in per_seed]),
                'score_mean': mean([r['score_mean'] for r in per_seed]),
                'score_var': mean([r['score_var'] for r in per_seed]),
                'phase_counts': {
                    'bad': int(sum(r['phase_counts']['bad'] for r in per_seed)),
                    'safe': int(sum(r['phase_counts']['safe'] for r in per_seed)),
                },
            }
            # Regime validity uses averaged metrics.
            validity_gate = {
                'nondegenerate_bad_rate': (0.20 <= agg['bad_rate'] <= 0.40),
                'nonzero_score_variance': (agg['score_var'] > 0),
                'nonzero_trigger_rate': (agg['trigger_rate'] > 0.05),
                'enough_positive_cases': (agg['phase_counts']['bad'] >= 10),
                'valid_for_interpretation': False,
            }
            validity_gate['valid_for_interpretation'] = all([
                validity_gate['nondegenerate_bad_rate'],
                validity_gate['nonzero_score_variance'],
                validity_gate['nonzero_trigger_rate'],
                validity_gate['enough_positive_cases'],
            ])
            agg['validity_gate'] = validity_gate
            sweep_results.append(agg)
            if validity_gate['valid_for_interpretation']:
                valid_candidates.append(agg)

chosen_regime = None
if valid_candidates:
    chosen_regime = sorted(valid_candidates, key=lambda r: (abs(r['bad_rate'] - 0.30), -r['trigger_rate'], -r['score_var']))[0]

results = {
    'version': 'V309E',
    'title': 'Regime repair gate before ablation',
    'config': {
        'seeds': SEEDS,
        'n_steps': N_STEPS,
        'A_c': A_C,
        'D_c': D_C,
        'severity_grid': severity_grid,
        'base_failure_grid': base_failure_grid,
        'noise_grid': noise_grid,
    },
    'sweep_results': sweep_results,
    'chosen_regime': chosen_regime,
    'validity_gate': {
        'nondegenerate_bad_rate': bool(chosen_regime is not None and chosen_regime['validity_gate']['nondegenerate_bad_rate']),
        'nonzero_score_variance': bool(chosen_regime is not None and chosen_regime['validity_gate']['nonzero_score_variance']),
        'nonzero_trigger_rate': bool(chosen_regime is not None and chosen_regime['validity_gate']['nonzero_trigger_rate']),
        'enough_positive_cases': bool(chosen_regime is not None and chosen_regime['validity_gate']['enough_positive_cases']),
        'valid_for_interpretation': bool(chosen_regime is not None and chosen_regime['validity_gate']['valid_for_interpretation']),
    },
}

# Decision per constitution
results['decision'] = 'branch' if not results['validity_gate']['valid_for_interpretation'] else 'continue'
results['next'] = (
    'If valid regime found, run held-out component ablation there; otherwise redesign harness again.'
    if not results['validity_gate']['valid_for_interpretation']
    else 'Run held-out component ablation in the chosen regime.'
)

with open(RESULT_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, sort_keys=True)

print(json.dumps(results, indent=2, sort_keys=True))
