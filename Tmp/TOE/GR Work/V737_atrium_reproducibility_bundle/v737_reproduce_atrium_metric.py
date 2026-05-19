"""
V737 Reproduce Atrium Metric

Independent reproducibility harness for the frozen V725/V726 result.

Boundary:
  - no direct k in certified metric
  - no adm_z-only shortcut
  - no GR claim
  - no tensor claim

Run:
  python v737_reproduce_atrium_metric.py
"""

from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

EPS = 1e-9
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)


def roc_auc(y_true, scores):
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores).astype(float)
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    return float(np.mean([(p > neg).mean() + 0.5 * (p == neg).mean() for p in pos]))


def second_var(v):
    return float(np.mean(np.diff(v, n=2) ** 2))


def second_diff(v):
    return np.r_[0.0, np.diff(v, n=2), 0.0]


def make_target(n, rng):
    x = np.linspace(0, 2 * np.pi, n)
    y = (
        0.50 * np.sin(1.15 * x + 0.2)
        + 0.24 * np.cos(3.1 * x - 0.4)
        + 0.12 * np.sin(7.4 * x + 0.1)
    )
    return y + rng.normal(0, 0.025, n)


def perturbation(n, fam, rng):
    x = np.linspace(0, 1, n)
    p = np.zeros(n)

    if fam == "gaussian_packet":
        c = rng.uniform(0.2, 0.8)
        w = rng.uniform(0.035, 0.10)
        p = np.exp(-((x - c) ** 2) / (2 * w * w)) * rng.choice([-1, 1])
    elif fam == "sawtooth":
        freq = rng.integers(3, 7)
        p = 2 * ((freq * x + rng.uniform()) % 1) - 1
    elif fam == "double_kink":
        c1, c2 = np.sort(rng.uniform(0.15, 0.85, 2))
        p = np.tanh((x - c1) / 0.025) - np.tanh((x - c2) / 0.025)
    elif fam == "colored_noise":
        raw = rng.normal(0, 1, n)
        kernel = np.exp(-np.linspace(-2, 2, 9) ** 2)
        kernel /= kernel.sum()
        p = np.convolve(raw, kernel, mode="same")
    else:
        p = np.sin(2 * np.pi * (2 * x + rng.uniform())) + 0.25 * rng.normal(0, 1, n)

    p -= p.mean()
    p /= p.std() + EPS
    return p


def simulate(target, pert, k, rng, steps=28):
    state = target + 0.55 * pert
    traj = [state.copy()]
    for _ in range(steps):
        force = -k * 0.20 * (state - target) - k * 0.030 * second_diff(state) - 0.010 * state
        noise = rng.normal(0, 0.007 + 0.005 * (1 - k), len(state))
        state = state + force + noise
        traj.append(state.copy())
    return np.asarray(traj), target + 0.55 * pert


def metrics_for_run(pair_id, label, k, family, target, perturbed, traj):
    initial = traj[0]
    final = traj[-1]
    n = len(target)

    d0 = float(np.linalg.norm(initial - target) / np.sqrt(n))
    dT = float(np.linalg.norm(final - target) / np.sqrt(n))
    restoration_residual = dT / (d0 + EPS)

    path_len = float(np.sum(np.linalg.norm(np.diff(traj, axis=0), axis=1)) / np.sqrt(n))
    direct = float(np.linalg.norm(final - initial) / np.sqrt(n))
    trajectory_deviation = np.log1p(max(path_len / (direct + EPS) - 1.0, 0.0))

    c0 = second_var(initial - target)
    cT = second_var(final - target)
    curvature_residual = np.log1p(max(cT / (c0 + EPS), 0.0))

    observation_boundary = float(
        np.mean(np.abs(traj[-5:] - target[None, :]))
        / (np.mean(np.abs(traj[:5] - target[None, :])) + EPS)
    )

    metric_strain = np.log1p(path_len / (max(d0 - dT, 0.0) + EPS))

    atrium_scalar = (
        1.50 * restoration_residual
        + 0.75 * trajectory_deviation
        + 0.75 * curvature_residual
        + 0.50 * observation_boundary
        + 0.25 * metric_strain
    )

    return {
        "pair_id": pair_id,
        "label": label,
        "k": k,
        "family": family,
        "restoration_residual": restoration_residual,
        "trajectory_deviation": trajectory_deviation,
        "curvature_residual": curvature_residual,
        "observation_boundary": observation_boundary,
        "metric_strain": metric_strain,
        "atrium_scalar": atrium_scalar,
        "passive_mean": float(np.mean(perturbed)),
        "passive_curvature": second_var(perturbed),
    }


def build_dataset(k_gap=0.80, n_pairs=360, seed=7370):
    rng = np.random.default_rng(seed)
    families = ["gaussian_packet", "sawtooth", "double_kink", "colored_noise", "mixed"]
    high_k = 0.82
    low_k = max(0.0, high_k - k_gap)
    rows = []

    for pair_id in range(n_pairs):
        target = make_target(72, rng)
        fam = families[pair_id % len(families)]
        pert = perturbation(72, fam, rng)
        pair_seed = rng.integers(0, 2**32 - 1)

        for label, k in [(0, high_k), (1, low_k)]:
            traj, perturbed = simulate(target, pert, k, np.random.default_rng(pair_seed))
            rows.append(metrics_for_run(pair_id, label, k, fam, target, perturbed, traj))

    return pd.DataFrame(rows)


def summarize(df):
    y = df["label"].to_numpy()
    return {
        "n": int(len(df)),
        "atrium_auc": roc_auc(y, df["atrium_scalar"]),
        "restoration_residual_auc": roc_auc(y, df["restoration_residual"]),
        "passive_mean_auc": roc_auc(y, df["passive_mean"]),
        "passive_curvature_auc": roc_auc(y, df["passive_curvature"]),
        "mean_atrium_high_k": float(df[df.label == 0]["atrium_scalar"].mean()),
        "mean_atrium_low_k": float(df[df.label == 1]["atrium_scalar"].mean()),
    }


def main():
    main_df = build_dataset(k_gap=0.80, n_pairs=420, seed=7370)
    main_summary = summarize(main_df)

    gap_results = []
    gap_frames = []
    for i, gap in enumerate([0.80, 0.65, 0.50, 0.30, 0.15, 0.05, 0.00]):
        df = build_dataset(k_gap=gap, n_pairs=260, seed=8000 + i)
        sc = summarize(df)
        sc["k_gap"] = gap
        gap_results.append(sc)
        gap_frames.append(df)

    family_results = []
    for fam, sub in main_df.groupby("family"):
        sc = summarize(sub)
        sc["family"] = fam
        family_results.append(sc)

    results = {
        "version": "V737",
        "title": "Independent Atrium Metric Reproducibility Harness",
        "direct_k_in_metric": False,
        "uses_adm_z": False,
        "main": main_summary,
        "gap_results": gap_results,
        "family_results": family_results,
        "pass_conditions": {
            "atrium_auc_high": main_summary["atrium_auc"] > 0.90,
            "passive_controls_chance": abs(main_summary["passive_mean_auc"] - 0.5) < 0.05
            and abs(main_summary["passive_curvature_auc"] - 0.5) < 0.05,
            "null_gap_chance": abs(gap_results[-1]["atrium_auc"] - 0.5) < 0.08,
        },
        "boundary": [
            "No direct k inside metric.",
            "No adm_z-only shortcut.",
            "No GR or tensor claim.",
            "Synthetic reproducibility only."
        ]
    }

    main_df.to_csv(OUT / "v737_main_metrics.csv", index=False)
    pd.concat(gap_frames, ignore_index=True).to_csv(OUT / "v737_gap_metrics.csv", index=False)
    (OUT / "v737_results.json").write_text(json.dumps(results, indent=2))

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
