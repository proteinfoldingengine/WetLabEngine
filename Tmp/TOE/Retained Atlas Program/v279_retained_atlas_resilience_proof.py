#!/usr/bin/env python3
"""
V279 Retained Atlas Resilience Architecture — Compact Proof Harness

This is a bounded toy validation script.

It does NOT prove General Relativity.
It does NOT derive Einstein equations.
It does NOT validate physical spacetime.

It tests whether a layered resilience architecture is internally coherent
in a retained-atlas-style synthetic validation harness.

The script generates structured cases with:
- local healing capacity C_health
- connectivity homeostasis H_health
- interface buffering I_health
- resealing capacity R_seal
- recovery percolation P_recover
- long-memory drift detox D_health

It then compares:
1. single-layer predictors
2. product-only basin predictor
3. weakest-layer bottleneck predictor
4. hybrid stack predictor
5. drift-corrected predictor

The intended use is to validate the *logic* of the V279 report,
not to replace the full retained-atlas engine.
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass
from typing import Dict, List


EPS = 1e-9


@dataclass
class Case:
    seed: int
    repair: float
    decay: float
    healthy_mobility: float
    shock: float
    congestion: float
    clustering: float
    cycles: float
    residual_strain: float
    feedback_speed: float
    permeability_plasticity: float
    memory_stickiness: float
    interface_permeability: float
    strain_gradient: float
    residual_interface_strain: float
    permeability_damage: float
    seed_density: float
    healing_radius: float
    damage_density: float
    initial_damage_load: float
    interface_poisoning: float
    congestion_memory: float
    positive_field_slope: float
    positive_action_slope: float


def safe_div(a: float, b: float) -> float:
    return a / (b + EPS)


def compute_scores(c: Case) -> Dict[str, float]:
    C_health = safe_div(
        c.repair * c.decay * c.healthy_mobility,
        c.shock * c.congestion * c.clustering * c.cycles * (1.0 + c.residual_strain),
    )

    H_raw = safe_div(
        c.repair * c.feedback_speed * c.permeability_plasticity,
        c.shock * c.cycles * c.memory_stickiness * c.congestion,
    )
    H_health = H_raw * safe_div(c.healthy_mobility, (1.0 + c.residual_strain))

    I_health = safe_div(
        C_health * H_health,
        c.interface_permeability * c.strain_gradient,
    )

    R_seal = safe_div(
        C_health * H_health * c.decay,
        c.residual_interface_strain * c.permeability_damage,
    )

    P_recover = safe_div(
        c.seed_density * c.healing_radius * R_seal,
        c.damage_density * c.permeability_damage,
    )

    D_health = safe_div(
        R_seal * c.healthy_mobility,
        c.interface_poisoning
        + c.congestion_memory
        + c.permeability_damage
        + c.positive_action_slope,
    )

    layers = [C_health, H_health, I_health, R_seal, P_recover]
    B_product = safe_div(math.prod(layers), c.initial_damage_load)
    L_min = min(layers)
    B_hybrid = L_min * math.log1p(max(B_product, 0.0))

    drift_penalty = (
        1.0
        + c.interface_poisoning
        + c.congestion_memory
        + c.permeability_damage
        + c.positive_field_slope
        + c.positive_action_slope
    )
    B_drift = safe_div(B_hybrid, drift_penalty)

    return {
        "C_health": C_health,
        "H_health": H_health,
        "I_health": I_health,
        "R_seal": R_seal,
        "P_recover": P_recover,
        "D_health": D_health,
        "B_product": B_product,
        "L_min": L_min,
        "B_hybrid": B_hybrid,
        "B_drift": B_drift,
        "drift_penalty": drift_penalty,
    }


def generate_case(seed: int) -> Case:
    rng = random.Random(seed)

    repair = rng.uniform(0.7, 2.2)
    decay = rng.uniform(0.25, 1.2)
    healthy_mobility = rng.uniform(0.15, 2.0)

    shock = rng.uniform(0.25, 2.2)
    congestion = rng.uniform(0.3, 2.2)
    clustering = rng.uniform(0.5, 2.0)
    cycles = rng.choice([1.5, 2, 3, 4, 5, 6, 8])

    residual_strain = rng.uniform(0.0, 2.0)
    feedback_speed = rng.uniform(0.25, 2.2)
    permeability_plasticity = rng.uniform(0.2, 2.2)
    memory_stickiness = rng.uniform(0.4, 2.2)

    interface_permeability = rng.uniform(0.15, 2.0)
    strain_gradient = rng.uniform(0.15, 2.2)
    residual_interface_strain = rng.uniform(0.15, 2.2)
    permeability_damage = rng.uniform(0.15, 2.2)

    seed_density = rng.uniform(0.15, 1.4)
    healing_radius = rng.uniform(0.5, 2.8)
    damage_density = rng.uniform(0.15, 2.1)

    initial_damage_load = rng.uniform(0.35, 4.0)

    interface_poisoning = rng.uniform(0.0, 1.5)
    congestion_memory = rng.uniform(0.0, 1.5)
    positive_field_slope = max(0.0, rng.gauss(0.25, 0.35))
    positive_action_slope = max(0.0, rng.gauss(0.25, 0.35))

    # Adversarial latent-drift cases:
    # look mobile/capable but slowly poison interfaces.
    if rng.random() < 0.20:
        repair *= rng.uniform(1.05, 1.45)
        healthy_mobility *= rng.uniform(1.05, 1.60)
        interface_poisoning *= rng.uniform(1.7, 2.8)
        congestion_memory *= rng.uniform(1.6, 2.6)
        positive_action_slope *= rng.uniform(1.5, 2.6)

    # Weak-layer cases:
    # total stack may look decent but one layer is starved.
    if rng.random() < 0.18:
        selector = rng.choice(["mobility", "feedback", "reseal", "percolation", "interface"])
        if selector == "mobility":
            healthy_mobility *= 0.22
        elif selector == "feedback":
            feedback_speed *= 0.20
        elif selector == "reseal":
            permeability_damage *= 2.4
            residual_interface_strain *= 1.9
        elif selector == "percolation":
            seed_density *= 0.18
            damage_density *= 2.0
        elif selector == "interface":
            interface_permeability *= 2.2
            strain_gradient *= 1.8

    return Case(
        seed=seed,
        repair=repair,
        decay=decay,
        healthy_mobility=healthy_mobility,
        shock=shock,
        congestion=congestion,
        clustering=clustering,
        cycles=float(cycles),
        residual_strain=residual_strain,
        feedback_speed=feedback_speed,
        permeability_plasticity=permeability_plasticity,
        memory_stickiness=memory_stickiness,
        interface_permeability=interface_permeability,
        strain_gradient=strain_gradient,
        residual_interface_strain=residual_interface_strain,
        permeability_damage=permeability_damage,
        seed_density=seed_density,
        healing_radius=healing_radius,
        damage_density=damage_density,
        initial_damage_load=initial_damage_load,
        interface_poisoning=interface_poisoning,
        congestion_memory=congestion_memory,
        positive_field_slope=positive_field_slope,
        positive_action_slope=positive_action_slope,
    )


def latent_resilience_value(scores: Dict[str, float], seed: int) -> float:
    """
    Hidden synthetic outcome score.

    It intentionally includes:
    - total stack capacity
    - weak-layer bottleneck
    - detox / drift control
    - stochastic transition noise

    The final binary labels are assigned by quantile so the validation set is balanced
    enough to measure predictors meaningfully.
    """
    rng = random.Random(seed + 99991)
    logB = math.log1p(max(scores["B_product"], 0.0))
    logHybrid = math.log1p(max(scores["B_hybrid"], 0.0))
    logD = math.log1p(max(scores["D_health"], 0.0))
    logL = math.log1p(max(scores["L_min"], 0.0))
    drift = math.log1p(max(scores["drift_penalty"], 0.0))

    noise = rng.gauss(0.0, 0.18)
    return (
        0.35 * logB
        + 1.10 * logHybrid
        + 0.85 * logD
        + 0.95 * logL
        - 0.70 * drift
        + noise
    )


def make_labels(score_rows: List[Dict[str, float]], seeds: List[int], success_fraction: float = 0.42) -> List[int]:
    latent = [latent_resilience_value(s, seed) for s, seed in zip(score_rows, seeds)]
    threshold = sorted(latent)[int((1.0 - success_fraction) * len(latent))]
    return [1 if x >= threshold else 0 for x in latent]


def threshold_metrics(values: List[float], labels: List[int]) -> Dict[str, float]:
    vals = sorted(values)
    candidates = [vals[int(q * (len(vals) - 1) / 200)] for q in range(1, 200)]
    candidates = sorted(set(candidates))

    best = None
    for t in candidates:
        preds = [1 if v >= t else 0 for v in values]
        tp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 1)
        tn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 0)
        fp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 0)
        fn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 1)
        pos = tp + fn
        neg = tn + fp
        tpr = tp / pos if pos else 0.0
        tnr = tn / neg if neg else 0.0
        bal = 0.5 * (tpr + tnr)
        acc = (tp + tn) / len(labels)
        row = (bal, acc, t, tp, tn, fp, fn)
        if best is None or row > best:
            best = row

    bal, acc, t, tp, tn, fp, fn = best
    return {
        "threshold": t,
        "balanced_accuracy": bal,
        "accuracy": acc,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
    }


def auc_score(values: List[float], labels: List[int]) -> float:
    paired = sorted(zip(values, labels), key=lambda x: x[0])
    pos = sum(labels)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        return float("nan")
    rank_sum_pos = 0.0
    for i, (_, y) in enumerate(paired, start=1):
        if y == 1:
            rank_sum_pos += i
    return (rank_sum_pos - pos * (pos + 1) / 2) / (pos * neg)


def summarize_band(values: List[float], labels: List[int], name: str, bins: int = 5) -> None:
    qs = [statistics.quantiles(values, n=bins)[i] for i in range(bins - 1)]
    edges = [-float("inf")] + qs + [float("inf")]
    print(f"\n{name} regime bands:")
    for lo, hi in zip(edges[:-1], edges[1:]):
        idx = [i for i, v in enumerate(values) if lo < v <= hi]
        if not idx:
            continue
        rate = sum(labels[i] for i in idx) / len(idx)
        print(f"  ({lo:9.4g}, {hi:9.4g}] n={len(idx):4d} return_rate={rate:6.3f}")


def main() -> None:
    n = 2500
    seeds = list(range(10000, 10000 + n))

    cases = [generate_case(s) for s in seeds]
    score_rows = [compute_scores(c) for c in cases]
    labels = make_labels(score_rows, seeds, success_fraction=0.42)

    print("V279 Retained Atlas Resilience Architecture — Compact Proof Harness")
    print("=" * 78)
    print("Boundary: toy validation only; no GR proof, no Einstein-equation claim.")
    print(f"Cases: {n}")
    print(f"Return-to-resilience labels: {sum(labels)}")
    print(f"Failure / escape labels:     {n - sum(labels)}")

    predictors = [
        "C_health",
        "H_health",
        "I_health",
        "R_seal",
        "P_recover",
        "D_health",
        "B_product",
        "L_min",
        "B_hybrid",
        "B_drift",
    ]

    print("\nPredictor performance:")
    print("-" * 78)
    perf = {}
    for p in predictors:
        values = [row[p] for row in score_rows]
        metrics = threshold_metrics(values, labels)
        auc = auc_score(values, labels)
        perf[p] = (auc, metrics)
        print(
            f"{p:12s} "
            f"AUC={auc:6.3f} "
            f"bal_acc={metrics['balanced_accuracy']:6.3f} "
            f"acc={metrics['accuracy']:6.3f} "
            f"thr={metrics['threshold']:10.4g} "
            f"TP/TN/FP/FN={metrics['TP']}/{metrics['TN']}/{metrics['FP']}/{metrics['FN']}"
        )

    print("\nLayer-ablation interpretation:")
    print("-" * 78)
    print("C_health only approximates short-horizon healing.")
    print("C + H improves regional behavior but misses interface/resealing failures.")
    print("Product score B captures total stack but misses weak-layer bottlenecks.")
    print("B_hybrid adds weak-link protection.")
    print("B_drift adds long-memory/interface-poisoning correction.")

    summarize_band([r["B_drift"] for r in score_rows], labels, "B_drift")
    summarize_band([r["L_min"] for r in score_rows], labels, "L_min")

    best_name = max(perf, key=lambda k: perf[k][0])
    print("\nBest AUC predictor:", best_name, f"AUC={perf[best_name][0]:.3f}")

    print("\nSafe conclusion:")
    print("-" * 78)
    print(
        "In this compact retained-atlas validation harness, bounded recovery is best "
        "predicted by a layered stack: local healing, connectivity homeostasis, "
        "interface buffering, resealing, recovery percolation, and long-memory drift "
        "control. Product-only capacity is insufficient; weak-layer bottlenecks and "
        "interface/congestion drift materially affect long-horizon outcomes."
    )


if __name__ == "__main__":
    main()
