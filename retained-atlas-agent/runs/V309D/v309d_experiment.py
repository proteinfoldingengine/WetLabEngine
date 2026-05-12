import json
import math
import os
from dataclasses import dataclass, asdict
from statistics import mean, pstdev
from pathlib import Path
from itertools import product

ROOT = Path('runs/V309D')
ROOT.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388
A_H = 0.1

@dataclass
class SimResult:
    bad_rate: float
    adaptive_rate: float
    trigger_rate: float
    score_mean: float
    score_var: float
    mean_A_norm: float
    min_A_norm: float
    phase_counts: dict
    auc: float
    balanced_accuracy: float
    accuracy: float
    enough_positive_cases: bool
    nondegenerate_bad_rate: bool
    nonzero_score_variance: bool
    nonzero_trigger_rate: bool
    valid_for_interpretation: bool


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate_regime(severity, base_failure, noise_scale, seed):
    # Deterministic toy dynamics: severity raises failure pressure, base_failure shifts baseline,
    # noise_scale adds mild seed-dependent variability.
    rs = (seed * 1103515245 + 12345) & 0x7fffffff
    def rnd():
        nonlocal rs
        rs = (1103515245 * rs + 12345) & 0x7fffffff
        return rs / 0x7fffffff

    A_vals = []
    y_true = []
    scores = []
    triggers = []
    adaptive = 0
    bad = 0
    safe = 0

    for t in range(N_STEPS):
        # latent pressure rises with severity and base_failure; modulated by a mild periodic component
        phase = math.sin((t + 1) * 0.31 + seed * 0.17)
        latent = base_failure + 0.85 * severity + 0.18 * phase + noise_scale * (rnd() - 0.5)
        A_norm = 1.25 - sigmoid(1.8 * latent) + 0.04 * math.cos(0.11 * t + seed * 0.05)
        A_norm = max(0.0, min(1.5, A_norm))
        D_A = max(0.0, A_C - A_norm)
        horizon_area = max(0.0, A_H - A_norm)
        score = D_A + 0.15 * horizon_area
        # bad label driven by low reachability and latent pressure
        bad_prob = sigmoid(4.2 * (0.52 - A_norm) + 1.1 * (latent - 0.65))
        bad_label = 1 if rnd() < bad_prob else 0
        trigger = 1 if score > D_C else 0
        adaptive_label = 1 if A_norm >= 0.7 else 0

        A_vals.append(A_norm)
        y_true.append(bad_label)
        scores.append(score)
        triggers.append(trigger)
        bad += bad_label
        safe += 1 - bad_label
        adaptive += adaptive_label

    bad_rate = bad / N_STEPS
    adaptive_rate = adaptive / N_STEPS
    trigger_rate = sum(triggers) / N_STEPS
    score_mean = mean(scores)
    score_var = pstdev(scores) ** 2 if len(scores) > 1 else 0.0
    mean_A_norm = mean(A_vals)
    min_A_norm = min(A_vals)

    # Simple ranking-based AUC with tie handling
    pos = [(s, y) for s, y in zip(scores, y_true) if y == 1]
    neg = [(s, y) for s, y in zip(scores, y_true) if y == 0]
    if len(pos) == 0 or len(neg) == 0:
        auc = 0.5
    else:
        wins = 0.0
        total = 0
        for ps, _ in pos:
            for ns, _ in neg:
                total += 1
                if ps > ns:
                    wins += 1
                elif ps == ns:
                    wins += 0.5
        auc = wins / total if total else 0.5

    # Threshold classifier at D_C for balanced accuracy / accuracy
    preds = [1 if s > D_C else 0 for s in scores]
    tp = sum(1 for p, y in zip(preds, y_true) if p == 1 and y == 1)
    tn = sum(1 for p, y in zip(preds, y_true) if p == 0 and y == 0)
    fp = sum(1 for p, y in zip(preds, y_true) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(preds, y_true) if p == 0 and y == 1)
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    balanced_accuracy = 0.5 * (tpr + tnr)
    accuracy = (tp + tn) / N_STEPS

    enough_positive_cases = bad >= 8
    nondegenerate_bad_rate = 0.20 <= bad_rate <= 0.40
    nonzero_score_variance = score_var > 0.0
    nonzero_trigger_rate = trigger_rate > 0.05
    valid_for_interpretation = all([
        enough_positive_cases,
        nondegenerate_bad_rate,
        nonzero_score_variance,
        nonzero_trigger_rate,
    ])

    return SimResult(
        bad_rate=bad_rate,
        adaptive_rate=adaptive_rate,
        trigger_rate=trigger_rate,
        score_mean=score_mean,
        score_var=score_var,
        mean_A_norm=mean_A_norm,
        min_A_norm=min_A_norm,
        phase_counts={"bad": bad, "safe": safe},
        auc=auc,
        balanced_accuracy=balanced_accuracy,
        accuracy=accuracy,
        enough_positive_cases=enough_positive_cases,
        nondegenerate_bad_rate=nondegenerate_bad_rate,
        nonzero_score_variance=nonzero_score_variance,
        nonzero_trigger_rate=nonzero_trigger_rate,
        valid_for_interpretation=valid_for_interpretation,
    )


def sweep():
    # 2D sweep over severity and base_failure/noise. We will not pick a regime unless it passes the gate.
    severities = [0.35, 0.45, 0.55, 0.65, 0.75]
    base_failures = [0.05, 0.12, 0.19, 0.26, 0.33]
    noise_scales = [0.00, 0.03, 0.06]
    rows = []
    for sev, bf, ns in product(severities, base_failures, noise_scales):
        per_seed = [simulate_regime(sev, bf, ns, seed) for seed in SEEDS]
        avg = lambda x: mean(getattr(r, x) for r in per_seed)
        row = {
            "severity": sev,
            "base_failure": bf,
            "noise_scale": ns,
            "bad_rate": avg("bad_rate"),
            "adaptive_rate": avg("adaptive_rate"),
            "trigger_rate": avg("trigger_rate"),
            "score_mean": avg("score_mean"),
            "score_var": avg("score_var"),
            "mean_A_norm": avg("mean_A_norm"),
            "min_A_norm": avg("min_A_norm"),
            "auc": avg("auc"),
            "balanced_accuracy": avg("balanced_accuracy"),
            "accuracy": avg("accuracy"),
            "enough_positive_cases": sum(r.enough_positive_cases for r in per_seed) / len(per_seed),
            "nondegenerate_bad_rate": sum(r.nondegenerate_bad_rate for r in per_seed) / len(per_seed),
            "nonzero_score_variance": sum(r.nonzero_score_variance for r in per_seed) / len(per_seed),
            "nonzero_trigger_rate": sum(r.nonzero_trigger_rate for r in per_seed) / len(per_seed),
            "valid_for_interpretation": sum(r.valid_for_interpretation for r in per_seed) / len(per_seed),
            "phase_counts": {
                "bad": sum(r.phase_counts["bad"] for r in per_seed),
                "safe": sum(r.phase_counts["safe"] for r in per_seed),
            },
        }
        rows.append(row)
    return rows


def main():
    rows = sweep()
    valid_rows = [r for r in rows if r["bad_rate"] >= 0.20 and r["bad_rate"] <= 0.40 and r["trigger_rate"] > 0.05 and r["score_var"] > 0 and r["phase_counts"]["bad"] > 0]

    chosen = valid_rows[0] if valid_rows else None
    results = {
        "version": "V309D",
        "title": "Regime repair for valid component ablation",
        "sweep_results": rows,
        "chosen_regime": chosen,
        "validity_gate": {
            "nondegenerate_bad_rate": bool(chosen and chosen["bad_rate"] >= 0.20 and chosen["bad_rate"] <= 0.40),
            "nonzero_score_variance": bool(chosen and chosen["score_var"] > 0),
            "nonzero_trigger_rate": bool(chosen and chosen["trigger_rate"] > 0.05),
            "enough_positive_cases": bool(chosen and chosen["phase_counts"]["bad"] >= 8),
            "valid_for_interpretation": bool(chosen and chosen["bad_rate"] >= 0.20 and chosen["bad_rate"] <= 0.40 and chosen["trigger_rate"] > 0.05 and chosen["score_var"] > 0 and chosen["phase_counts"]["bad"] >= 8),
        },
        "decision": "continue" if chosen else "branch",
        "next": "If valid regime found, run held-out component ablation there; otherwise redesign harness again.",
    }

    out_path = ROOT / 'V309D_results.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, sort_keys=True)
    print(json.dumps(results, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
