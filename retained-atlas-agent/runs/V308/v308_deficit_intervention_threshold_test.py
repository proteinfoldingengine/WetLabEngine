# retained-atlas-agent/runs/V308/v308_deficit_intervention_threshold_test.py

import os
import json
import numpy as np
from sklearn.metrics import balanced_accuracy_score, accuracy_score

OUTDIR = "runs/V308"
os.makedirs(OUTDIR, exist_ok=True)

A_C = 0.527
D_C = 0.0388
A_H = 0.10

def make_synthetic_run(seed, n=500):
    rng = np.random.default_rng(seed)

    bad = rng.random(n) < 0.35

    # Good branches tend to keep higher reachability.
    # Bad branches tend to lose future accessibility.
    A_norm = np.clip(
        rng.normal(loc=np.where(bad, 0.35, 0.72), scale=0.08),
        0.0,
        1.2,
    )

    D_A = np.maximum(0.0, A_C - A_norm)
    horizon_area = np.maximum(0.0, A_H - A_norm)

    return bad, A_norm, D_A, horizon_area

def evaluate_trigger(name, trigger, bad, rng):
    rescued = 0
    harmed = 0
    severity_reduction = 0.0

    for i in range(len(bad)):
        if trigger[i] and bad[i]:
            if rng.random() < 0.60:
                rescued += 1
                severity_reduction += 0.35
            else:
                severity_reduction += 0.10

        if trigger[i] and not bad[i]:
            if rng.random() < 0.08:
                harmed += 1
                severity_reduction -= 0.20

    return {
        "trigger": name,
        "bad_rate": float(np.mean(bad)),
        "adaptive_rate": float(1.0 - np.mean(bad)),
        "trigger_rate": float(np.mean(trigger)),
        "rescued": int(rescued),
        "harmed": int(harmed),
        "net_rescue": int(rescued - harmed),
        "severity_reduction": float(severity_reduction),
        "balanced_accuracy": float(
            balanced_accuracy_score(bad.astype(int), trigger.astype(int))
        ),
        "accuracy": float(
            accuracy_score(bad.astype(int), trigger.astype(int))
        ),
    }

def main():
    all_results = {
        "A_norm": [],
        "D_A": [],
        "horizon_area": [],
        "combined": [],
    }

    for seed in range(308, 408):
        rng = np.random.default_rng(seed + 10000)
        bad, A_norm, D_A, horizon_area = make_synthetic_run(seed)

        triggers = {
            "A_norm": A_norm < A_C,
            "D_A": D_A > D_C,
            "horizon_area": horizon_area > 0.0,
            "combined": (A_norm < A_C) | (D_A > D_C) | (horizon_area > 0.0),
        }

        for name, trigger in triggers.items():
            all_results[name].append(
                evaluate_trigger(name, trigger, bad, rng)
            )

    summary = {}

    for name, rows in all_results.items():
        summary[name] = {}
        for key in rows[0].keys():
            if key == "trigger":
                continue
            summary[name][key] = float(np.mean([r[key] for r in rows]))

    result_path = os.path.join(OUTDIR, "v308_results.json")

    with open(result_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"\nSaved: {result_path}")

if __name__ == "__main__":
    main()
