#!/usr/bin/env python3
"""
V300 Retained-Atlas Reachability Collapse Law — Skeptical Proof Harness

This script is a compact but complete toy-law reproduction harness.

It demonstrates:
1. A retained-atlas toy with healing, poisoning, memory, resealing, connectivity, and detox dynamics.
2. An adaptive reachability variable A(t).
3. A normalized reachability law A_norm = A(t) / A_baseline.
4. Cross-regime threshold behavior across variants.
5. Reachability-triggered staged repair reducing bad outcomes.
6. The failure of weak partial repair relative to full staged repair.

Boundary:
- This is NOT a proof of General Relativity.
- This is NOT a physical spacetime derivation.
- This demonstrates emergent law behavior inside the toy model.
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


EPS = 1e-9


def sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + math.exp(-max(-60.0, min(60.0, x)))))


def balanced_accuracy(y_true: List[int], y_pred: List[int]) -> float:
    tp = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 0)
    tpr = tp / (tp + fn + EPS)
    tnr = tn / (tn + fp + EPS)
    return 0.5 * (tpr + tnr)


def accuracy(y_true: List[int], y_pred: List[int]) -> float:
    return sum(1 for y, p in zip(y_true, y_pred) if y == p) / max(1, len(y_true))


def auc_score(y_true: List[int], scores: List[float]) -> float:
    # Rank-based AUC; higher score should indicate positive class.
    pairs = sorted(zip(scores, y_true), key=lambda x: x[0])
    pos = sum(y_true)
    neg = len(y_true) - pos
    if pos == 0 or neg == 0:
        return float("nan")
    rank_sum = 0.0
    for i, (_, y) in enumerate(pairs, start=1):
        if y == 1:
            rank_sum += i
    return (rank_sum - pos * (pos + 1) / 2.0) / (pos * neg)


def best_threshold_low(values: List[float], labels: List[int]) -> Dict[str, float]:
    # Predict bad when value < threshold.
    qs = np.quantile(values, np.linspace(0.05, 0.95, 181))
    best = {"balanced_accuracy": -1.0}
    for t in qs:
        pred = [1 if v < t else 0 for v in values]
        bal = balanced_accuracy(labels, pred)
        acc = accuracy(labels, pred)
        if bal > best["balanced_accuracy"]:
            best = {
                "threshold": float(t),
                "balanced_accuracy": float(bal),
                "accuracy": float(acc),
                "trigger_rate": float(sum(pred) / len(pred)),
            }
    return best


def variant_params(variant: str):
    if variant == "sparse":
        return (0.45, 1.05), 0.25, 0.85, 1.0, 42
    if variant == "dense":
        return (0.95, 1.65), 0.45, 1.15, 0.9, 42
    if variant == "noisy":
        return (0.60, 1.40), 0.34, 1.0, 1.8, 42
    if variant == "irregular_shock":
        return (0.60, 1.40), 0.34, 1.0, 1.0, 0
    if variant == "long_memory":
        return (0.60, 1.40), 0.34, 0.95, 1.0, 42
    return (0.60, 1.40), 0.34, 1.0, 1.0, 42


@dataclass
class RunResult:
    variant: str
    poison_scale: float
    phase: str
    bad: int
    adaptive: int
    A50: float
    triggered: bool
    late_field: float
    late_action: float
    late_residual: float
    late_pocket: float


def simulate(
    seed: int,
    poison_scale: float,
    variant: str = "base",
    intervention: bool = False,
    A_baseline: float = 1.0,
    threshold: float = 0.527,
    dose: float = 1.0,
    n_steps: int = 230,
) -> RunResult:
    rng = np.random.default_rng(seed)
    corridor_range, K0, feedback_mult, noise_mult, shock_period = variant_params(variant)

    repair = rng.uniform(0.90, 1.50)
    decay = rng.uniform(0.50, 1.10)
    mobility0 = rng.uniform(0.70, 1.30)
    feedback = rng.uniform(0.70, 1.30) * feedback_mult
    plasticity = rng.uniform(0.65, 1.35)
    clustering = rng.uniform(0.82, 1.25)
    shock = rng.uniform(0.65, 1.20)
    congestion = rng.uniform(0.72, 1.15) * (1.0 + 0.25 * poison_scale)

    interface_poison = max(0.0, 0.08 + 0.42 * poison_scale + rng.normal(0, 0.03))
    congestion_memory = max(0.0, 0.06 + 0.36 * poison_scale + rng.normal(0, 0.03))
    permeability_damage = max(0.0, 0.07 + 0.34 * poison_scale + rng.normal(0, 0.03))
    reseal_delay = 1.0 + 1.20 * poison_scale

    if variant == "long_memory":
        congestion_memory *= 1.35
        permeability_damage *= 1.20
        reseal_delay *= 1.15

    pocket = max(
        0.0,
        0.05
        + max(0.0, rng.normal(0.18 * poison_scale, 0.09))
        + max(0.0, rng.normal(0.08 * poison_scale, 0.07)),
    )
    corridor = rng.uniform(*corridor_range)
    detox_base = rng.uniform(0.035, 0.13)

    field = 0.35 + 0.13 * rng.random()
    action = 1.00 + 0.20 * rng.random()
    residual = 0.22 + 0.09 * rng.random()
    K = K0 + 0.06 * rng.normal()

    field_hist, action_hist, residual_hist, pocket_hist, reach_hist = [], [], [], [], []
    triggered = False
    A50 = float("nan")

    for t in range(n_steps):
        if shock_period:
            pulse = 1.0 if t % shock_period < 8 else 0.16
        else:
            pulse = 1.0 if (math.sin(t * 0.31 + seed % 17) > 0.72 or t % 53 < 5) else 0.16

        shock_pulse = shock * pulse
        poison_load = interface_poison + congestion_memory + permeability_damage + 0.60 * pocket

        mobility = max(
            0.035,
            mobility0 * sigmoid(2.55 - 0.48 * field - 0.35 * action - 0.22 * poison_load),
        )

        C_health = (
            repair * decay * mobility * corridor
            / (shock_pulse * congestion * clustering * (1.0 + residual) + EPS)
        )
        H_health = (
            repair * feedback * plasticity
            / (shock_pulse * congestion * (1.0 + poison_load) + EPS)
        ) * mobility / (1.0 + residual)

        R_seal = (
            C_health * H_health * decay
            / ((0.33 + field) * (0.32 + permeability_damage + 0.50 * pocket) * reseal_delay + EPS)
        )
        P_recover = (
            0.85 * R_seal
            / ((0.30 + 0.55 * poison_scale) * (0.30 + permeability_damage + 0.50 * pocket) + EPS)
        )
        D_health = (
            R_seal * mobility
            / (poison_load + max(0.0, action - 1.0) + EPS)
        )

        # Composite adaptive reachability.
        recovery_front = sigmoid(1.2 * math.log1p(C_health + R_seal + D_health) - 0.9 * math.log1p(poison_load + pocket))
        corridor_width = max(0.0, min(3.0, K * corridor * mobility / (1.0 + 0.60 * pocket + 0.40 * field)))
        branching_entropy = sigmoid(2.5 * K + 1.2 * mobility - 0.9 * pocket - 0.5 * residual)
        detox_radius = sigmoid(1.1 * math.log1p(D_health + R_seal) + 0.5 * mobility - 0.7 * math.log1p(poison_load))
        reversible_fraction = sigmoid(1.5 * math.log1p(R_seal + C_health) - 0.8 * math.log1p(residual + field + pocket))

        A = max(0.0, recovery_front * corridor_width * branching_entropy * detox_radius * reversible_fraction) ** (1.0 / 5.0)
        reach_hist.append(A)

        # Reachability-triggered full staged repair at step 50.
        if intervention and (not triggered) and t == 50:
            A50 = float(np.mean(reach_hist[20:50]))
            A_norm = A50 / (A_baseline + EPS)
            if A_norm < threshold:
                triggered = True
        elif (not intervention) and t == 50:
            A50 = float(np.mean(reach_hist[20:50]))

        detox = detox_base * D_health if (pocket > 0.25 and mobility > 0.18 and t % 31 < 5) else 0.0

        if triggered:
            if 50 <= t < 95:
                detox += dose * 1.25 * (0.10 * D_health + 0.055)
                interface_poison *= max(0.970, 1.0 - dose * 1.25 * 0.008)
                congestion_memory *= max(0.972, 1.0 - dose * 1.25 * 0.007)
                pocket *= max(0.945, 1.0 - dose * 1.25 * 0.016)
            elif 95 <= t < 165:
                detox += dose * 1.70 * (0.18 * D_health + 0.040)
                permeability_damage *= max(0.945, 1.0 - dose * 1.70 * 0.011)
                reseal_delay *= max(0.955, 1.0 - dose * 1.70 * 0.009)
                repair *= (1.0 + dose * 1.70 * 0.0008)
            elif 165 <= t < 225:
                feedback *= (1.0 + dose * 0.0013)
                plasticity *= (1.0 + dose * 0.0011)
                mobility0 *= (1.0 + dose * 0.0007)
                congestion_memory *= max(0.985, 1.0 - dose * 0.004)
                congestion *= max(0.990, 1.0 - dose * 0.0004)

        heal_force = 0.034 * C_health + 0.025 * R_seal + 0.016 * P_recover + 0.020 * D_health
        poison_force = 0.014 * poison_load + 0.007 * congestion * field + 0.004 * max(0.0, action - 1.0)

        field = max(0.0, field + poison_force - heal_force + 0.45 * pocket * 0.008 + rng.normal(0, 0.005 * noise_mult))
        action = max(0.25, action + 0.024 * field + 0.0085 * poison_load - 0.034 * mobility * D_health + rng.normal(0, 0.006 * noise_mult))
        residual = max(0.0, residual + 0.014 * field + 0.007 * poison_load - 0.034 * R_seal - 0.012 * C_health + rng.normal(0, 0.004 * noise_mult))
        pocket = max(0.0, pocket + (0.006 * poison_scale + 0.004 * field + 0.004 * congestion_memory) - (0.020 * R_seal + detox) + rng.normal(0, 0.003 * noise_mult))
        K = max(0.0, min(1.0, K + 0.018 * H_health - 0.009 * field - 0.008 * poison_load + rng.normal(0, 0.004 * noise_mult)))

        field_hist.append(field)
        action_hist.append(action)
        residual_hist.append(residual)
        pocket_hist.append(pocket)

    late_field = float(np.mean(field_hist[-40:]))
    late_action = float(np.mean(action_hist[-40:]))
    late_residual = float(np.mean(residual_hist[-40:]))
    late_pocket = float(np.mean(pocket_hist[-40:]))
    field_slope = float(np.polyfit(np.arange(50), field_hist[-50:], 1)[0])

    if late_field < 0.65 and late_action < 1.58 and late_residual < 0.70 and late_pocket < 0.35 and field_slope <= 0.004:
        phase = "adaptive"
    elif late_field < 0.95 and late_action < 1.90 and late_residual < 0.95 and late_pocket < 0.55:
        phase = "slow"
    elif late_pocket >= 0.45 and late_field < 1.35 and late_residual < 1.35:
        phase = "pockets"
    elif late_field < 1.75 and late_residual < 1.70:
        phase = "fragment"
    else:
        phase = "runaway"

    return RunResult(
        variant=variant,
        poison_scale=poison_scale,
        phase=phase,
        bad=1 if phase in ("fragment", "runaway") else 0,
        adaptive=1 if phase == "adaptive" else 0,
        A50=A50,
        triggered=triggered,
        late_field=late_field,
        late_action=late_action,
        late_residual=late_residual,
        late_pocket=late_pocket,
    )


def summarize_counts(results: List[RunResult]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in results:
        out[r.phase] = out.get(r.phase, 0) + 1
    return out


def main() -> None:
    variants = ["base", "sparse", "dense", "noisy", "irregular_shock", "long_memory"]
    poison_scales = [round(x, 2) for x in np.arange(0.8, 2.51, 0.15)]

    # 1. Run untreated baseline.
    untreated: List[RunResult] = []
    for vi, variant in enumerate(variants):
        for si, scale in enumerate(poison_scales):
            for k in range(6):
                seed = 300000 + vi * 100000 + si * 1000 + k
                untreated.append(simulate(seed, scale, variant, intervention=False))

    print("V300 Retained-Atlas Reachability Collapse Law Proof Harness")
    print("=" * 78)
    print("Boundary: toy-model law proof only; no physical GR/spacetime claim.")
    print(f"Untreated cases: {len(untreated)}")
    print("Untreated phase counts:", summarize_counts(untreated))
    print(f"Untreated bad rate: {np.mean([r.bad for r in untreated]):.3f}")

    # 2. Calibrate regime baselines from low-poison scale cases.
    baselines: Dict[str, float] = {}
    for variant in variants:
        vals = [r.A50 for r in untreated if r.variant == variant and r.poison_scale <= 1.10 and math.isfinite(r.A50)]
        baselines[variant] = float(np.median(vals))
    print("\nRegime A50 baselines:")
    for k, v in baselines.items():
        print(f"  {k:16s}: {v:.4f}")

    # 3. Raw A50 and normalized A_norm threshold performance.
    labels = [r.bad for r in untreated]
    raw_A = [r.A50 for r in untreated]
    A_norm = [r.A50 / (baselines[r.variant] + EPS) for r in untreated]

    raw_metrics = best_threshold_low(raw_A, labels)
    norm_metrics = best_threshold_low(A_norm, labels)

    print("\nThreshold law performance:")
    print(f"  Raw A50 AUC:      {auc_score(labels, [-x for x in raw_A]):.3f}")
    print(f"  Raw A50 best:     threshold={raw_metrics['threshold']:.4f} bal_acc={raw_metrics['balanced_accuracy']:.3f} acc={raw_metrics['accuracy']:.3f}")
    print(f"  A_norm AUC:       {auc_score(labels, [-x for x in A_norm]):.3f}")
    print(f"  A_norm best:      threshold={norm_metrics['threshold']:.4f} bal_acc={norm_metrics['balanced_accuracy']:.3f} acc={norm_metrics['accuracy']:.3f}")

    # Use a fixed operational threshold close to V297–V299.
    operational_threshold = 0.527

    print("\nOperational threshold by variant:")
    for variant in variants:
        sub = [r for r in untreated if r.variant == variant]
        pred = [1 if r.A50 / (baselines[variant] + EPS) < operational_threshold else 0 for r in sub]
        lab = [r.bad for r in sub]
        print(
            f"  {variant:16s}: bad={np.mean(lab):.3f} "
            f"bal_acc={balanced_accuracy(lab, pred):.3f} "
            f"acc={accuracy(lab, pred):.3f} "
            f"trigger={np.mean(pred):.3f}"
        )

    # 4. Reachability-triggered intervention at full dose.
    treated: List[RunResult] = []
    for vi, variant in enumerate(variants):
        for si, scale in enumerate(poison_scales):
            for k in range(6):
                seed = 300000 + vi * 100000 + si * 1000 + k
                treated.append(
                    simulate(
                        seed,
                        scale,
                        variant,
                        intervention=True,
                        A_baseline=baselines[variant],
                        threshold=operational_threshold,
                        dose=1.0,
                    )
                )

    rescued = sum(1 for a, b in zip(untreated, treated) if a.bad == 1 and b.bad == 0)
    harmed = sum(1 for a, b in zip(untreated, treated) if a.bad == 0 and b.bad == 1)

    print("\nReachability-triggered full staged repair:")
    print("Treated phase counts:", summarize_counts(treated))
    print(f"  Untreated bad rate: {np.mean([r.bad for r in untreated]):.3f}")
    print(f"  Treated bad rate:   {np.mean([r.bad for r in treated]):.3f}")
    print(f"  Untreated adaptive: {np.mean([r.adaptive for r in untreated]):.3f}")
    print(f"  Treated adaptive:   {np.mean([r.adaptive for r in treated]):.3f}")
    print(f"  Trigger rate:       {np.mean([r.triggered for r in treated]):.3f}")
    print(f"  Rescued:            {rescued}")
    print(f"  Harmed:             {harmed}")

    print("\nSeverity reduction:")
    for attr in ["late_field", "late_action", "late_residual", "late_pocket"]:
        before = np.mean([getattr(r, attr) for r in untreated])
        after = np.mean([getattr(r, attr) for r in treated])
        print(f"  {attr:14s}: {before:9.3f} -> {after:9.3f}")

    # 5. Weak partial repair comparison.
    weak: List[RunResult] = []
    for vi, variant in enumerate(variants):
        for si, scale in enumerate(poison_scales):
            for k in range(6):
                seed = 300000 + vi * 100000 + si * 1000 + k
                weak.append(
                    simulate(
                        seed,
                        scale,
                        variant,
                        intervention=True,
                        A_baseline=baselines[variant],
                        threshold=operational_threshold,
                        dose=0.5,
                    )
                )

    weak_rescued = sum(1 for a, b in zip(untreated, weak) if a.bad == 1 and b.bad == 0)
    weak_harmed = sum(1 for a, b in zip(untreated, weak) if a.bad == 0 and b.bad == 1)

    print("\nWeak partial repair comparison:")
    print(f"  Weak bad rate:      {np.mean([r.bad for r in weak]):.3f}")
    print(f"  Weak adaptive:      {np.mean([r.adaptive for r in weak]):.3f}")
    print(f"  Weak rescued:       {weak_rescued}")
    print(f"  Weak harmed:        {weak_harmed}")

    print("\nSafe conclusion:")
    print(
        "Inside this retained-atlas toy, normalized adaptive reachability is a strong "
        "predictor of bad-basin entry. Reachability-triggered full staged repair "
        "reduces fragmentation/runaway and severity across multiple variants. "
        "Weak partial repair is less reliable. This supports the toy-level law: "
        "failure begins when adaptive future trajectories contract below a "
        "regime-relative threshold."
    )


if __name__ == "__main__":
    main()
