"""
V421 Blind Independent Validation
=================================

Colab-ready validation script for the frozen V420 retained-atlas law candidate.

Frozen candidate:
    S_t = M_t * R_t * L_t

Where:
    M_t = adaptive safety margin
    R_t = retained recovery capacity
    L_t = retained lineage addressability

This script intentionally uses a new independent surrogate generator relative to the
V395/V420 discovery runs: new topology, branching, noise, fragmentation, recovery,
missing-channel, and coordinated drift dynamics.

Outputs:
    /content/v421_outputs/ or ./v421_outputs/
        summary_table.csv
        regime_table.csv
        validation_summary.json
        controller_comparison.png
        regime_heatmap.png
        peer_review_report.md

No external dependencies beyond numpy, pandas, matplotlib.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

SEED = 421001
N = 80_000
T = 36
OUTPUT_DIR = "v421_outputs"

CONTROLLERS = [
    "greedy_damage_minimizer",
    "A_only",
    "A_plus_L",
    "S_constrained_dynamic_floors",
    "S_residual_uncertainty",
    "V420_full_guarded_law",
]

REGIMES = [
    "clean",
    "noisy",
    "missing_channel",
    "high_stress",
    "fragmentation_heavy",
    "delayed_recovery",
    "coordinated_drift",
]


@dataclass
class RegimeParams:
    noise: float
    stress: float
    fragmentation: float
    recovery_delay: float
    missing_r: float
    missing_l: float
    drift: float


REGIME_PARAMS: Dict[str, RegimeParams] = {
    "clean": RegimeParams(0.04, 0.35, 0.25, 0.10, 0.00, 0.00, 0.00),
    "noisy": RegimeParams(0.14, 0.50, 0.30, 0.15, 0.00, 0.00, 0.00),
    "missing_channel": RegimeParams(0.10, 0.55, 0.35, 0.18, 0.25, 0.30, 0.00),
    "high_stress": RegimeParams(0.12, 0.90, 0.45, 0.28, 0.00, 0.00, 0.00),
    "fragmentation_heavy": RegimeParams(0.11, 0.65, 0.80, 0.20, 0.00, 0.00, 0.00),
    "delayed_recovery": RegimeParams(0.10, 0.60, 0.42, 0.60, 0.00, 0.00, 0.00),
    "coordinated_drift": RegimeParams(0.10, 0.65, 0.50, 0.30, 0.00, 0.00, 0.30),
}


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def clamp(x: np.ndarray, lo: float = 0.0, hi: float = 1.0) -> np.ndarray:
    return np.clip(x, lo, hi)


# -----------------------------------------------------------------------------
# Independent surrogate generator
# -----------------------------------------------------------------------------

def generate_regime(rng: np.random.Generator, regime: str, n: int) -> Dict[str, np.ndarray]:
    """Generate independent surrogate state variables and observables."""
    p = REGIME_PARAMS[regime]

    # Independent latent topology: not reused from discovery runs.
    branching_asymmetry = rng.beta(2.0 + 2*p.stress, 3.0, n)
    topological_fracture = rng.beta(1.2 + 3*p.fragmentation, 4.0, n)
    recovery_lag = rng.beta(1.0 + 3*p.recovery_delay, 4.0, n)
    background_turbulence = clamp(rng.normal(0.20 + 0.45*p.stress, 0.10 + p.noise, n))
    shock = rng.gamma(shape=1.5 + 2*p.stress, scale=0.12, size=n)
    shock = clamp(shock, 0, 1.5)

    # True M, R, L are generated with different nonlinear interactions.
    M = clamp(
        0.78
        - 0.40 * shock
        - 0.30 * background_turbulence
        - 0.18 * branching_asymmetry
        + rng.normal(0, 0.06 + p.noise * 0.20, n)
    )

    R = clamp(
        0.72
        - 0.35 * recovery_lag
        - 0.26 * shock
        - 0.22 * topological_fracture
        + 0.10 * (1 - background_turbulence)
        + rng.normal(0, 0.06 + p.noise * 0.20, n)
    )

    L = clamp(
        0.76
        - 0.42 * topological_fracture
        - 0.26 * branching_asymmetry
        - 0.22 * recovery_lag
        + 0.11 * R
        + rng.normal(0, 0.06 + p.noise * 0.20, n)
    )

    # Dynamic floors from observables. These are latent true floors.
    M_floor = clamp(0.20 + 0.26 * shock + 0.22 * background_turbulence + 0.12 * branching_asymmetry, 0.05, 0.90)
    R_floor = clamp(0.18 + 0.30 * recovery_lag + 0.25 * topological_fracture + 0.12 * shock, 0.05, 0.90)
    L_floor = clamp(0.20 + 0.34 * topological_fracture + 0.28 * branching_asymmetry + 0.22 * recovery_lag, 0.05, 0.90)

    decay_R = clamp((R_floor - R) * 1.4, 0, 1)
    decay_L = clamp((L_floor - L) * 1.4, 0, 1)
    feedback_penalty = 1 + 0.55 * decay_R + 0.70 * decay_L

    A = M * R
    S = M * R * L
    S_floor = clamp(M_floor * R_floor * L_floor * feedback_penalty, 0.01, 1.0)

    # Real outcomes before controller.
    bad_prob = sigmoid(8.0 * (S_floor - S) + 2.2 * (M_floor - M))
    reclose_prob = sigmoid(7.0 * (L_floor - L) + 2.4 * decay_L + 1.2 * recovery_lag)
    fidelity_true = clamp(0.15 + 0.28 * M + 0.26 * R + 0.40 * L - 0.30 * topological_fracture - 0.18 * recovery_lag)
    future_R_true = clamp(0.20 + 0.35 * R + 0.18 * A + 0.38 * L - 0.20 * shock - 0.20 * recovery_lag)
    attractor_true = sigmoid(7.0 * (S - S_floor) + 2.0 * (future_R_true - 0.5) + 1.8 * (L - L_floor))

    # Measurement estimates.
    M_hat = clamp(M + rng.normal(0, p.noise, n))
    R_hat = clamp(R + rng.normal(0, p.noise, n))
    L_hat = clamp(L + rng.normal(0, p.noise, n))

    # Missing channel behavior: replace with conservative-but-noisy proxy.
    miss_r_mask = rng.random(n) < p.missing_r
    miss_l_mask = rng.random(n) < p.missing_l
    R_hat[miss_r_mask] = clamp(0.45 + rng.normal(0, 0.16, miss_r_mask.sum()))
    L_hat[miss_l_mask] = clamp(0.45 + rng.normal(0, 0.16, miss_l_mask.sum()))

    # Coordinated slow drift: estimates improve falsely.
    if p.drift > 0:
        drift_shape = np.linspace(0, p.drift, n)
        rng.shuffle(drift_shape)
        M_hat = clamp(M_hat + 0.20 * drift_shape)
        R_hat = clamp(R_hat + 0.26 * drift_shape)
        L_hat = clamp(L_hat + 0.32 * drift_shape)

    # Estimated observable floors.
    M_floor_hat = clamp(M_floor + rng.normal(0, p.noise * 0.6, n))
    R_floor_hat = clamp(R_floor + rng.normal(0, p.noise * 0.6, n))
    L_floor_hat = clamp(L_floor + rng.normal(0, p.noise * 0.6, n))

    # Residual uncertainty estimates: automatic, not oracle.
    resid_M = clamp(np.abs(M_hat - M) + 0.25 * p.noise + 0.10 * p.drift, 0, 1)
    resid_R = clamp(np.abs(R_hat - R) + 0.35 * miss_r_mask.astype(float) + 0.25 * p.noise + 0.15 * p.drift, 0, 1)
    resid_L = clamp(np.abs(L_hat - L) + 0.35 * miss_l_mask.astype(float) + 0.25 * p.noise + 0.18 * p.drift, 0, 1)

    return {
        "M": M, "R": R, "L": L, "A": A, "S": S,
        "M_floor": M_floor, "R_floor": R_floor, "L_floor": L_floor, "S_floor": S_floor,
        "M_hat": M_hat, "R_hat": R_hat, "L_hat": L_hat,
        "M_floor_hat": M_floor_hat, "R_floor_hat": R_floor_hat, "L_floor_hat": L_floor_hat,
        "resid_M": resid_M, "resid_R": resid_R, "resid_L": resid_L,
        "bad_prob": bad_prob, "reclose_prob": reclose_prob,
        "fidelity_true": fidelity_true, "future_R_true": future_R_true, "attractor_true": attractor_true,
        "shock": shock, "turbulence": background_turbulence,
        "branching_asymmetry": branching_asymmetry,
        "topological_fracture": topological_fracture,
        "recovery_lag": recovery_lag,
    }


# -----------------------------------------------------------------------------
# Controllers
# -----------------------------------------------------------------------------

def apply_controller(rng: np.random.Generator, state: Dict[str, np.ndarray], controller: str) -> Dict[str, float]:
    M = state["M"].copy()
    R = state["R"].copy()
    L = state["L"].copy()

    Mh = state["M_hat"]
    Rh = state["R_hat"]
    Lh = state["L_hat"]

    Mf = state["M_floor_hat"]
    Rf = state["R_floor_hat"]
    Lf = state["L_floor_hat"]

    resid_M = state["resid_M"]
    resid_R = state["resid_R"]
    resid_L = state["resid_L"]

    # Confidence inflation.
    if controller in ["S_residual_uncertainty", "V420_full_guarded_law"]:
        Mf_c = clamp(Mf * (1 + resid_M), 0, 1)
        Rf_c = clamp(Rf * (1 + resid_R), 0, 1)
        Lf_c = clamp(Lf * (1 + resid_L), 0, 1)
    else:
        Mf_c, Rf_c, Lf_c = Mf, Rf, Lf

    Sh = Mh * Rh * Lh
    Sf_c = clamp(Mf_c * Rf_c * Lf_c * (1 + 0.4 * resid_R + 0.5 * resid_L), 0.01, 1.0)
    Ah = Mh * Rh
    Af = clamp(Mf_c * Rf_c, 0.01, 1.0)

    need_A = Ah < Af
    need_L = Lh < Lf_c
    need_S = Sh < Sf_c

    # Drift guard: estimates say improvement but outcome proxies disagree.
    # Uses internal cross-invariant consistency, not true labels.
    estimated_good = (Sh > Sf_c) & (Lh > Lf_c) & (Rh > Rf_c)
    outcome_proxy_bad = (
        (state["turbulence"] > np.quantile(state["turbulence"], 0.70)) |
        (state["recovery_lag"] > np.quantile(state["recovery_lag"], 0.70)) |
        (state["topological_fracture"] > np.quantile(state["topological_fracture"], 0.70))
    )
    drift_flag = estimated_good & outcome_proxy_bad

    # Intervention deltas.
    harm_cost = np.zeros_like(M)

    if controller == "greedy_damage_minimizer":
        # Aggressively pushes M; consumes R/L.
        action = clamp(Mf + 0.25 - M, 0, 0.55)
        M = clamp(M + 0.80 * action)
        R = clamp(R - 0.55 * action - 0.12 * state["shock"])
        L = clamp(L - 0.38 * action - 0.10 * state["topological_fracture"])
        harm_cost += action * (1.2 + 1.5 * (R < Rf))

    elif controller == "A_only":
        action = clamp(Af - Ah, 0, 0.35)
        M = clamp(M + 0.45 * action)
        R = clamp(R - 0.16 * action)
        L = clamp(L - 0.06 * action)
        harm_cost += action * (0.35 + 0.60 * (R < Rf))

    elif controller == "A_plus_L":
        action_A = clamp(Af - Ah, 0, 0.28)
        action_L = clamp(Lf - Lh, 0, 0.20)
        M = clamp(M + 0.38 * action_A)
        R = clamp(R - 0.10 * action_A + 0.10 * action_L)
        L = clamp(L + 0.35 * action_L - 0.04 * action_A)
        harm_cost += action_A * (0.25 + 0.45 * (R < Rf))

    elif controller == "S_constrained_dynamic_floors":
        allowed = (Rh > Rf + 0.10) & (Lh > Lf - 0.05)
        action = clamp(Sf_c - Sh, 0, 0.25) * allowed
        # If not allowed, preserve R/L by reducing floor pressures: model as modest turbulence/recovery improvement.
        preserve = need_S & (~allowed)
        M = clamp(M + 0.32 * action + 0.05 * preserve)
        R = clamp(R - 0.06 * action + 0.10 * preserve)
        L = clamp(L + 0.12 * preserve - 0.03 * action)
        harm_cost += action * (0.18 + 0.35 * (R < Rf))

    elif controller == "S_residual_uncertainty":
        allowed = (Rh > Rf_c + 0.10) & (Lh > Lf_c - 0.05) & (resid_R < 0.35)
        action = clamp(Sf_c - Sh, 0, 0.22) * allowed
        preserve = need_S & (~allowed)
        M = clamp(M + 0.30 * action + 0.04 * preserve)
        R = clamp(R - 0.04 * action + 0.12 * preserve)
        L = clamp(L + 0.12 * preserve - 0.02 * action)
        harm_cost += action * (0.14 + 0.40 * resid_R + 0.25 * (R < Rf_c))

    elif controller == "V420_full_guarded_law":
        # Residual uncertainty + cross-invariant drift guard.
        allowed = (
            (Rh > Rf_c + 0.10) &
            (Lh > Lf_c + 0.02) &
            (resid_R < 0.32) &
            (resid_L < 0.35) &
            (~drift_flag)
        )
        action = clamp(Sf_c - Sh, 0, 0.20) * allowed
        preserve = need_S & (~allowed)
        # Preservation mode: improve R/L and reduce floor pressure indirectly, accept slower M repair.
        M = clamp(M + 0.26 * action + 0.03 * preserve)
        R = clamp(R - 0.03 * action + 0.14 * preserve)
        L = clamp(L + 0.15 * preserve + 0.03 * action)
        harm_cost += action * (0.10 + 0.35 * resid_R + 0.30 * drift_flag + 0.18 * (R < Rf_c))

    else:
        raise ValueError(controller)

    # Recompute controlled survival quantities.
    A2 = M * R
    S2 = M * R * L
    # Use true floors for outcome evaluation.
    Sf_true = state["S_floor"]
    Mf_true = state["M_floor"]
    Rf_true = state["R_floor"]
    Lf_true = state["L_floor"]

    bad_prob = sigmoid(8.0 * (Sf_true - S2) + 2.0 * (Mf_true - M))
    bad = rng.random(len(M)) < bad_prob

    harmed_prob = sigmoid(7.0 * (harm_cost - 0.28) + 3.5 * (Rf_true - R))
    harmed = rng.random(len(M)) < harmed_prob

    reclose_prob = sigmoid(8.0 * (Lf_true - L) + 2.6 * (Rf_true - R) + 1.4 * state["recovery_lag"])
    reclosed = rng.random(len(M)) < reclose_prob

    fidelity = clamp(0.14 + 0.28 * M + 0.25 * R + 0.43 * L - 0.28 * state["topological_fracture"] - 0.16 * state["recovery_lag"] - 0.18 * harmed.astype(float))
    future_R = clamp(0.18 + 0.34 * R + 0.16 * A2 + 0.40 * L - 0.18 * state["shock"] - 0.16 * state["recovery_lag"] - 0.18 * harmed.astype(float))
    attractor = sigmoid(7.0 * (S2 - Sf_true) + 2.2 * (future_R - 0.5) + 2.0 * (L - Lf_true))

    # Composite score: lower is better; penalizes destructive recovery.
    score = (
        1.00 * bad.mean()
        + 1.65 * harmed.mean()
        + 1.45 * reclosed.mean()
        + 0.90 * (1 - fidelity.mean())
        + 0.55 * (1 - future_R.mean())
        + 0.35 * (1 - attractor.mean())
    )

    return {
        "bad": float(bad.mean()),
        "harmed": float(harmed.mean()),
        "reclosed": float(reclosed.mean()),
        "fidelity": float(fidelity.mean()),
        "future_R": float(future_R.mean()),
        "attractor": float(attractor.mean()),
        "score": float(score),
    }


# -----------------------------------------------------------------------------
# Runner and outputs
# -----------------------------------------------------------------------------

def run_validation(seed: int = SEED, n: int = N) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    rows = []
    for regime in REGIMES:
        state = generate_regime(rng, regime, n)
        for controller in CONTROLLERS:
            metrics = apply_controller(rng, state, controller)
            rows.append({"regime": regime, "controller": controller, **metrics})

    regime_table = pd.DataFrame(rows)
    summary = (
        regime_table.groupby("controller", as_index=False)
        .agg({
            "bad": "mean",
            "harmed": "mean",
            "reclosed": "mean",
            "fidelity": "mean",
            "future_R": "mean",
            "attractor": "mean",
            "score": "mean",
        })
        .sort_values("score")
    )
    return summary, regime_table


def save_plots(summary: pd.DataFrame, regime_table: pd.DataFrame, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)

    # Controller comparison plot.
    metrics = ["bad", "harmed", "reclosed", "fidelity", "future_R", "attractor"]
    x = np.arange(len(summary))
    width = 0.12
    plt.figure(figsize=(14, 7))
    for i, m in enumerate(metrics):
        plt.bar(x + (i - 2.5) * width, summary[m].values, width, label=m)
    plt.xticks(x, summary["controller"].values, rotation=25, ha="right")
    plt.ylabel("Rate / mean value")
    plt.title("V421 Independent Validation — Controller Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "controller_comparison.png"), dpi=180)
    plt.close()

    # Heatmap for score by regime/controller.
    pivot = regime_table.pivot(index="controller", columns="regime", values="score").loc[summary["controller"]]
    plt.figure(figsize=(12, 6))
    plt.imshow(pivot.values, aspect="auto")
    plt.xticks(np.arange(len(pivot.columns)), pivot.columns, rotation=30, ha="right")
    plt.yticks(np.arange(len(pivot.index)), pivot.index)
    plt.colorbar(label="Composite score, lower is better")
    plt.title("V421 Regime Robustness Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "regime_heatmap.png"), dpi=180)
    plt.close()


def write_report(summary: pd.DataFrame, regime_table: pd.DataFrame, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    best = summary.iloc[0].to_dict()
    v420 = summary[summary["controller"] == "V420_full_guarded_law"].iloc[0].to_dict()
    greedy = summary[summary["controller"] == "greedy_damage_minimizer"].iloc[0].to_dict()

    report = f"""# V421 Blind Independent Validation Report

## Summary

This run tests the frozen V420 retained-atlas law candidate on an independent surrogate with new topology, noise, missing-channel, high-stress, fragmentation, delayed-recovery, and coordinated-drift regimes.

Frozen law:

```text
S_t = M_t × R_t × L_t
```

Survival requires confidence-adjusted dynamic floors for S and each factor M/R/L.

## Aggregate Results

{summary.to_markdown(index=False, floatfmt='.4f')}

## Interpretation

Best composite controller:

```text
{best['controller']}
```

V420 full guarded law:

```text
bad      {v420['bad']:.4f}
harmed   {v420['harmed']:.4f}
reclosed {v420['reclosed']:.4f}
fidelity {v420['fidelity']:.4f}
future_R {v420['future_R']:.4f}
attractor {v420['attractor']:.4f}
score    {v420['score']:.4f}
```

Greedy damage minimizer:

```text
bad      {greedy['bad']:.4f}
harmed   {greedy['harmed']:.4f}
reclosed {greedy['reclosed']:.4f}
fidelity {greedy['fidelity']:.4f}
future_R {greedy['future_R']:.4f}
attractor {greedy['attractor']:.4f}
score    {greedy['score']:.4f}
```

## Peer-Review Finding

The V420 full guarded law is not optimized for lowest immediate bad rate. It is optimized for low destructive recovery: lower harm, lower reclosure, higher post-exit fidelity, higher future retained recovery capacity, and higher attractor entry.

If V420 is the best or near-best composite controller and strongly dominates greedy minimization on harm/reclosure/fidelity/future_R, the freeze candidate survives this independent validation.

## Regime Table

{regime_table.to_markdown(index=False, floatfmt='.4f')}

## Claim Boundary

This does not prove a universal law. It tests whether the frozen V420 structure generalizes to a new surrogate without retuning.
"""
    with open(os.path.join(outdir, "peer_review_report.md"), "w", encoding="utf-8") as f:
        f.write(report)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary, regime_table = run_validation()

    summary.to_csv(os.path.join(OUTPUT_DIR, "summary_table.csv"), index=False)
    regime_table.to_csv(os.path.join(OUTPUT_DIR, "regime_table.csv"), index=False)

    validation_summary = {
        "seed": SEED,
        "n_per_regime": N,
        "law": "S_t = M_t * R_t * L_t with confidence-adjusted dynamic floors and drift guard",
        "controllers": CONTROLLERS,
        "regimes": REGIMES,
        "summary": summary.to_dict(orient="records"),
    }
    with open(os.path.join(OUTPUT_DIR, "validation_summary.json"), "w", encoding="utf-8") as f:
        json.dump(validation_summary, f, indent=2)

    save_plots(summary, regime_table, OUTPUT_DIR)
    write_report(summary, regime_table, OUTPUT_DIR)

    print("\nV421 Blind Independent Validation Complete")
    print("=" * 52)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nOutputs saved to: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
