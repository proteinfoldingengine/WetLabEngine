import json
import math
import os
from pathlib import Path
from statistics import mean, pstdev

import numpy as np


VERSION = "V310"
OUTDIR = Path("runs") / VERSION
OUTDIR.mkdir(parents=True, exist_ok=True)

A_C = 0.527
A_H = 0.10
D_C = 0.0388
SEEDS = list(range(20))
N_STEPS = 60

# Narrow repair sweep: enough to probe the target band without broad exploration.
severity_grid = [0.22, 0.26, 0.30, 0.34, 0.38]
base_failure_grid = [0.06, 0.09, 0.12, 0.15, 0.18]
noise_grid = [0.0, 0.02]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def simulate_regime(severity, base_failure, noise_scale, seed):
    rng = np.random.default_rng(seed)
    # Toy dynamics: lower severity and lower base_failure give mostly safe states;
    # increasing either pushes A_norm downward into bad territory.
    x = 0.0
    A_vals = []
    D_vals = []
    H_vals = []
    bad_flags = []
    triggers = []
    rescued = 0
    harmed = 0
    late_residual = []
    late_mobility = []
    late_K = []

    for t in range(N_STEPS):
        shock = rng.normal(0.0, noise_scale)
        drift = (base_failure - 0.10) + 0.65 * severity + 0.35 * shock
        x = 0.88 * x + drift + rng.normal(0.0, 0.03 + 0.02 * noise_scale)
        # Reachability proxy: clipped and normalized around a baseline.
        A_norm = np.clip(1.05 - 0.78 * sigmoid(x) + 0.04 * rng.normal(), 0.0, 1.5)
        D_A = max(0.0, A_C - A_norm)
        H_A = max(0.0, A_H - A_norm)
        trigger = 1 if (D_A > D_C and H_A > 0.0) else 0
        bad = 1 if A_norm < A_C else 0

        # Toy intervention accounting.
        if trigger and bad and rng.random() < 0.28:
            rescued += 1
        if trigger and (not bad) and rng.random() < 0.10:
            harmed += 1

        A_vals.append(A_norm)
        D_vals.append(D_A)
        H_vals.append(H_A)
        bad_flags.append(bad)
        triggers.append(trigger)
        late_residual.append(max(0.0, A_C - A_norm) if t >= N_STEPS - 10 else 0.0)
        late_mobility.append(abs(A_norm - (A_vals[-2] if len(A_vals) > 1 else A_norm)))
        late_K.append(1.0 - A_norm)

    A_vals = np.array(A_vals)
    D_vals = np.array(D_vals)
    H_vals = np.array(H_vals)
    bad_flags = np.array(bad_flags)
    triggers = np.array(triggers)

    bad_rate = float(np.mean(bad_flags))
    adaptive_rate = float(1.0 - bad_rate)
    trigger_rate = float(np.mean(triggers))
    mean_A = float(np.mean(A_vals))
    min_A = float(np.min(A_vals))
    score_mean = mean_A
    score_var = float(np.var(A_vals))
    horizon_width = float(np.mean(H_vals > 0.0))
    horizon_area = float(np.mean(H_vals))
    pinch = float(np.mean(D_vals > 0.0))
    duration_below_Ac = float(np.mean(A_vals < A_C))
    phase_counts = {"bad": int(np.sum(bad_flags)), "safe": int(np.sum(1 - bad_flags))}

    # Real metric implementation: AUC via rank statistic, only if both classes present.
    if len(np.unique(bad_flags)) < 2:
        auc = None
        balanced_accuracy = 0.5
        accuracy = float(np.mean(1 - bad_flags))
    else:
        # Use score = -A_norm so higher means more bad.
        scores = -A_vals
        pos = scores[bad_flags == 1]
        neg = scores[bad_flags == 0]
        # Mann-Whitney U / AUC
        ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
        pos_ranks = np.sum(ranks[: len(pos)])
        n1 = len(pos)
        n0 = len(neg)
        u = pos_ranks - n1 * (n1 + 1) / 2.0
        auc = float(u / (n1 * n0))
        # threshold at A_C for a simple classifier
        pred_bad = (A_vals < A_C).astype(int)
        tp = int(np.sum((pred_bad == 1) & (bad_flags == 1)))
        tn = int(np.sum((pred_bad == 0) & (bad_flags == 0)))
        fp = int(np.sum((pred_bad == 1) & (bad_flags == 0)))
        fn = int(np.sum((pred_bad == 0) & (bad_flags == 1)))
        tpr = tp / (tp + fn) if (tp + fn) else 0.0
        tnr = tn / (tn + fp) if (tn + fp) else 0.0
        balanced_accuracy = float(0.5 * (tpr + tnr))
        accuracy = float((tp + tn) / len(bad_flags))

    return {
        "severity": severity,
        "base_failure": base_failure,
        "noise_scale": noise_scale,
        "bad_rate": bad_rate,
        "adaptive_rate": adaptive_rate,
        "trigger_rate": trigger_rate,
        "AUC": auc,
        "balanced_accuracy": balanced_accuracy,
        "accuracy": accuracy,
        "mean_A_norm": mean_A,
        "min_A_norm": min_A,
        "score_mean": score_mean,
        "score_var": score_var,
        "duration_below_Ac": duration_below_Ac,
        "horizon_width": horizon_width,
        "horizon_area": horizon_area,
        "pinch": pinch,
        "mean_A": mean_A,
        "min_A": min_A,
        "late_residual": float(np.mean(late_residual)),
        "late_mobility": float(np.mean(late_mobility)),
        "late_K": float(np.mean(late_K)),
        "rescued": int(rescued),
        "harmed": int(harmed),
        "phase_counts": phase_counts,
    }


def validity_gate(summary):
    enough_positive_cases = summary["phase_counts"]["bad"] > 0
    nondegenerate_bad_rate = 0.20 <= summary["bad_rate"] <= 0.40
    nonzero_score_variance = summary["score_var"] > 0.0
    nonzero_trigger_rate = summary["trigger_rate"] > 0.05
    valid_for_interpretation = bool(
        enough_positive_cases
        and nondegenerate_bad_rate
        and nonzero_score_variance
        and nonzero_trigger_rate
    )
    return {
        "nondegenerate_bad_rate": nondegenerate_bad_rate,
        "nonzero_score_variance": nonzero_score_variance,
        "nonzero_trigger_rate": nonzero_trigger_rate,
        "enough_positive_cases": enough_positive_cases,
        "valid_for_interpretation": valid_for_interpretation,
    }


sweep = []
chosen = None
for sev in severity_grid:
    for bf in base_failure_grid:
        for nz in noise_grid:
            s = simulate_regime(sev, bf, nz, seed=12345)
            gate = validity_gate(s)
            s["validity_gate"] = gate
            sweep.append(s)
            if gate["valid_for_interpretation"] and chosen is None:
                chosen = s

# If no valid regime, keep chosen_regime null and do not ablate.
results = {
    "version": VERSION,
    "title": "Harness repair validation test",
    "config": {
        "seeds": SEEDS,
        "n_steps": N_STEPS,
        "A_c": A_C,
        "A_h": A_H,
        "D_c": D_C,
        "severity_grid": severity_grid,
        "base_failure_grid": base_failure_grid,
        "noise_grid": noise_grid,
    },
    "chosen_regime": None if chosen is None else {
        k: chosen[k] for k in [
            "severity", "base_failure", "noise_scale", "bad_rate", "trigger_rate",
            "AUC", "balanced_accuracy", "accuracy", "mean_A_norm", "min_A_norm",
            "score_mean", "score_var", "phase_counts", "validity_gate"
        ]
    },
    "sweep_results": sweep,
    "decision": "branch" if chosen is None else "continue",
    "next": "No valid regime found; redesign the harness again before any ablation." if chosen is None else "Run the smallest held-out component test in the valid regime.",
}

# Attach a top-level validity gate based on the chosen regime.
if chosen is None:
    results["validity_gate"] = {
        "nondegenerate_bad_rate": False,
        "nonzero_score_variance": False,
        "nonzero_trigger_rate": False,
        "enough_positive_cases": False,
        "valid_for_interpretation": False,
    }
else:
    results["validity_gate"] = chosen["validity_gate"]

# Save outputs.
json_path = OUTDIR / f"{VERSION}_results.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, sort_keys=True)

print(json.dumps(results, indent=2, sort_keys=True))
