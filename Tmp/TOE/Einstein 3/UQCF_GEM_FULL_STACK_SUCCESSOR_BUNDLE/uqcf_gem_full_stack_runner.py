#!/usr/bin/env python3
"""
UQCF-GEM / Recoverability Accessibility Framework
Full-Stack ADM-Like Constraint Runner

Document ID:
    V832_FULL_STACK_SUCCESSOR_RUNNER

Purpose:
    Give a successor AI / researcher a single reproducible Python script that runs the
    mature empirical stack:

    1. Ordered-update accessibility-flow simulation
    2. Accessibility density A and potential psi = log(A)
    3. Conformal ADM-like scalar and momentum analog quantities
    4. Flow-frame decomposition of momentum
    5. Compact same-slice law fitting
    6. Frozen-coefficient transfer
    7. Adversarial falsification
    8. Resolution scaling / discretization audit
    9. Outputs: JSON, CSV, Markdown report

Claim boundary:
    This script tests ADM-like same-slice constraint analogs in an informational
    accessibility-flow simulation.

    It DOES NOT prove:
        - physical General Relativity
        - Einstein equations
        - physical spacetime curvature
        - continuum-limit closure
        - ontology of reality

    It DOES support, if metrics reproduce:
        - compact ADM-like same-slice constraint structure
        - accessibility-flow momentum in the local flow frame
        - frozen coefficient transfer
        - falsification against shuffled/rotated controls
        - resolution-sensitive residual behavior
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


EPS = 1e-9


# -----------------------------
# Numerical operators
# -----------------------------

def d1_central(F: np.ndarray, h: float, axis: int) -> np.ndarray:
    """Second-order central first derivative with periodic roll."""
    return (np.roll(F, -1, axis=axis) - np.roll(F, 1, axis=axis)) / (2.0 * h)


def d1_fourth(F: np.ndarray, h: float, axis: int) -> np.ndarray:
    """Fourth-order central first derivative with periodic roll."""
    return (
        -np.roll(F, -2, axis=axis)
        + 8.0 * np.roll(F, -1, axis=axis)
        - 8.0 * np.roll(F, 1, axis=axis)
        + np.roll(F, 2, axis=axis)
    ) / (12.0 * h)


def lap2_second(F: np.ndarray, dx: float) -> np.ndarray:
    """Second-order 2D Laplacian over spatial axes 1,2 for F[t,x,y]."""
    return (
        np.roll(F, 1, axis=1)
        + np.roll(F, -1, axis=1)
        + np.roll(F, 1, axis=2)
        + np.roll(F, -1, axis=2)
        - 4.0 * F
    ) / (dx * dx)


def lap2_fourth(F: np.ndarray, dx: float) -> np.ndarray:
    """Fourth-order 2D Laplacian as sum of 1D fourth-order second derivatives."""
    d2x = (
        -np.roll(F, -2, axis=1)
        + 16.0 * np.roll(F, -1, axis=1)
        - 30.0 * F
        + 16.0 * np.roll(F, 1, axis=1)
        - np.roll(F, 2, axis=1)
    ) / (12.0 * dx * dx)
    d2y = (
        -np.roll(F, -2, axis=2)
        + 16.0 * np.roll(F, -1, axis=2)
        - 30.0 * F
        + 16.0 * np.roll(F, 1, axis=2)
        - np.roll(F, 2, axis=2)
    ) / (12.0 * dx * dx)
    return d2x + d2y


def robust_scale(x: np.ndarray) -> float:
    """Median absolute deviation style scale."""
    x = np.asarray(x).ravel()
    return float(np.nanmedian(np.abs(x - np.nanmedian(x))) + EPS)


def safe_r2(y: np.ndarray, pred: np.ndarray) -> float:
    y = np.asarray(y).ravel()
    pred = np.asarray(pred).ravel()
    return float(1.0 - np.sum((y - pred) ** 2) / (np.sum((y - y.mean()) ** 2) + EPS))


def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    if np.std(a) < EPS or np.std(b) < EPS:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(x).ravel() ** 2)))


# -----------------------------
# Simulation configuration
# -----------------------------

@dataclass
class RunConfig:
    seed: int = 832
    bound: float = 8.0
    nt: int = 12
    defects: int = 7
    complexity: int = 4
    eta: float = 0.35
    alpha: float = 0.127348327184804
    operator_order: int = 2
    train_nx: int = 32
    ladder: Tuple[int, ...] = (12, 16, 20, 24, 28, 32)
    train_modes: Tuple[str, ...] = ("standard", "radial", "shear", "counterrot")
    test_modes: Tuple[str, ...] = ("standard", "radial", "shear", "counterrot", "pulse")


class FrozenPhysics:
    """
    Analytic defect paths and phases are fixed, then sampled at arbitrary grid resolution.
    This avoids changing the physics when nx changes.
    """

    def __init__(self, config: RunConfig):
        self.config = config
        rng = np.random.default_rng(config.seed)
        self.nodes = rng.uniform(
            -config.bound / 2.0,
            config.bound / 2.0,
            (config.defects, 2),
        )
        self.phases = rng.uniform(0.0, 2.0 * np.pi, config.defects)

    def render(self, nx: int, mode: str = "mixed") -> Dict[str, np.ndarray | float]:
        cfg = self.config
        tau = np.linspace(0.0, 6.0, cfg.nt)
        x = np.linspace(-cfg.bound, cfg.bound, nx)
        dt = float(tau[1] - tau[0])
        dx = float(x[1] - x[0])

        X, Y = np.meshgrid(x, x, indexing="xy")
        R = np.sqrt(X * X + Y * Y)

        mus, repairs, Cs, phis = [], [], [], []

        for t in tau:
            mu = np.zeros_like(X)

            for i, (cx, cy) in enumerate(self.nodes):
                sign = -1.0 if i % 2 else 1.0

                if mode == "radial":
                    scale = 1.0 + 0.08 * t
                    rx, ry = cx * scale, cy * scale

                elif mode == "shear":
                    a = sign * t * (0.18 + 0.08 * cfg.complexity) + self.phases[i]
                    rx = cx * np.cos(a) - cy * np.sin(a) + 0.30 * t * np.sin(cy)
                    ry = cx * np.sin(a) + cy * np.cos(a) + 0.15 * t * np.cos(cx)

                elif mode == "counterrot":
                    a = sign * t * (0.30 + 0.12 * cfg.complexity) + self.phases[i]
                    rx = cx * np.cos(a) - cy * np.sin(a)
                    ry = cx * np.sin(a) + cy * np.cos(a)

                elif mode == "pulse":
                    a = t * (0.20 + 0.10 * cfg.complexity) + self.phases[i]
                    pulse = 1.0 + 0.25 * np.sin(2.5 * t + self.phases[i])
                    rx = pulse * (cx * np.cos(a) - cy * np.sin(a))
                    ry = pulse * (cx * np.sin(a) + cy * np.cos(a))

                else:  # standard / mixed
                    a = sign * t * (0.22 + 0.10 * cfg.complexity) + self.phases[i]
                    pulse = 1.0 + 0.12 * np.sin(2.1 * t + self.phases[i])
                    rx = pulse * (cx * np.cos(a) - cy * np.sin(a)) + 0.10 * t * np.sin(cy)
                    ry = pulse * (cx * np.sin(a) + cy * np.cos(a)) + 0.07 * t * np.cos(cx)

                width = max(1.15, 2.75 - 0.20 * cfg.complexity)
                amp = 1.0 + 0.22 * np.sin((1.4 + 0.2 * cfg.complexity) * t + self.phases[i])
                mu += amp * np.exp(-((X - rx) ** 2 + (Y - ry) ** 2) / width)

            repair = (
                np.cos(R * (1.15 + 0.08 * cfg.complexity) - t * (2.25 + 0.18 * cfg.complexity))
                * np.exp(-R / (cfg.bound * 0.8))
                + 0.45
                * np.sin(X * (1.0 + 0.08 * cfg.complexity) - t)
                * np.cos(Y * (1.0 + 0.06 * cfg.complexity) - 1.4 * t)
            )

            C = cfg.eta * repair - 0.25 * mu
            phi = np.clip(
                0.42 * np.log1p(np.clip(mu, 0.0, 10.0))
                - 0.22 * np.tanh(cfg.eta * repair),
                -1.2,
                1.2,
            )

            mus.append(mu)
            repairs.append(repair)
            Cs.append(C)
            phis.append(phi)

        return {
            "tau": tau,
            "x": x,
            "dt": dt,
            "dx": dx,
            "mu": np.stack(mus),
            "repair": np.stack(repairs),
            "C": np.stack(Cs),
            "phi": np.stack(phis),
        }


# -----------------------------
# ADM-like quantities and features
# -----------------------------

def get_ops(order: int):
    if order == 4:
        return d1_fourth, lap2_fourth
    return d1_central, lap2_second


def compute_feature_frame(render: Dict[str, np.ndarray | float], config: RunConfig) -> pd.DataFrame:
    D, L = get_ops(config.operator_order)

    C = render["C"]
    mu = render["mu"]
    repair = render["repair"]
    phi = render["phi"]
    dt = float(render["dt"])
    dx = float(render["dx"])

    a = np.exp(phi)

    # Lapse-like normalization proxy. This is not physical lapse; it is an analog.
    N = np.exp(0.15 * np.tanh(C / (np.std(C) + EPS)))

    h = a * a
    ht = D(h, dt, axis=0)

    Kcov = -(0.5 / (N + EPS)) * ht
    hi = np.exp(-2.0 * phi)

    K = 2.0 * hi * Kcov
    K2 = 2.0 * (hi * hi * Kcov * Kcov)

    R2 = -2.0 * np.exp(-2.0 * phi) * L(phi, dx)
    H = R2 + K * K - K2

    Axx = hi * Kcov - K
    Ayy = hi * Kcov - K

    Mx = D(Axx, dx, axis=1)
    My = D(Ayy, dx, axis=2)

    A = np.exp(C - mu + config.eta * repair)
    psi = np.log(A + 1e-6)

    psix, psiy = D(psi, dx, axis=1), D(psi, dx, axis=2)

    Jx, Jy = -psix, -psiy
    dJx, dJy = D(Jx, dt, axis=0), D(Jy, dt, axis=0)
    divJ = D(Jx, dx, axis=1) + D(Jy, dx, axis=2)

    access_curv = 2.0 * config.alpha * L(psi, dx)

    Jnorm = np.sqrt(Jx * Jx + Jy * Jy) + EPS

    M_parallel = (Mx * Jx + My * Jy) / Jnorm
    M_perp = (-Mx * Jy + My * Jx) / Jnorm

    dJ_parallel = (dJx * Jx + dJy * Jy) / Jnorm
    dJ_perp = (-dJx * Jy + dJy * Jx) / Jnorm

    # Adversarial wrong frame: fixed coordinate rotation, not local J-frame.
    ang = np.pi / 4.0
    M_bad_parallel = Mx * np.cos(ang) + My * np.sin(ang)
    M_bad_perp = -Mx * np.sin(ang) + My * np.cos(ang)

    nx = phi.shape[-1]
    margin = max(3 if config.operator_order == 4 else 2, int(nx * 0.10))
    time_margin = 3 if config.operator_order == 4 else 2
    sl = (slice(time_margin, -time_margin), slice(margin, -margin), slice(margin, -margin))

    df = pd.DataFrame({
        "H": (H / robust_scale(H))[sl].ravel(),
        "M_parallel": (M_parallel / robust_scale(M_parallel))[sl].ravel(),
        "M_perp": (M_perp / robust_scale(M_perp))[sl].ravel(),
        "M_bad_parallel": (M_bad_parallel / robust_scale(M_bad_parallel))[sl].ravel(),
        "M_bad_perp": (M_bad_perp / robust_scale(M_bad_perp))[sl].ravel(),

        "access_curv": (access_curv / robust_scale(access_curv))[sl].ravel(),
        "A_n": ((A - np.nanmedian(A)) / robust_scale(A))[sl].ravel(),
        "K_n": (K / robust_scale(K))[sl].ravel(),
        "K2_n": (K2 / robust_scale(K2))[sl].ravel(),

        "Jmag": (Jnorm / robust_scale(Jnorm))[sl].ravel(),
        "dJ_parallel": (dJ_parallel / robust_scale(dJ_parallel))[sl].ravel(),
        "dJ_perp": (dJ_perp / robust_scale(dJ_perp))[sl].ravel(),
        "divJ": (divJ / robust_scale(divJ))[sl].ravel(),
    })

    return df


# -----------------------------
# Compact law
# -----------------------------

LAW_FEATURES = {
    "H": ["access_curv", "A_n", "K_n", "K2_n"],
    "M_parallel": ["Jmag", "dJ_parallel", "divJ"],
    "M_perp": ["Jmag", "dJ_perp", "divJ"],
}


def fit_compact_law(df: pd.DataFrame) -> Dict[str, Dict[str, object]]:
    betas = {}
    for target, cols in LAW_FEATURES.items():
        X = df[cols].values
        y = df[target].values
        beta = np.linalg.lstsq(np.column_stack([np.ones(len(X)), X]), y, rcond=None)[0]
        betas[target] = {
            "features": cols,
            "coef": [float(v) for v in beta],
        }
    return betas


def predict_target(df: pd.DataFrame, law: Dict[str, Dict[str, object]], target: str, shuffled: bool = False, rng=None) -> np.ndarray:
    if rng is None:
        rng = np.random.default_rng(0)
    info = law[target]
    cols = info["features"]
    X = df[cols].copy()

    if shuffled:
        for c in cols:
            vals = X[c].values.copy()
            rng.shuffle(vals)
            X[c] = vals

    beta = np.array(info["coef"], dtype=float)
    return np.column_stack([np.ones(len(X)), X.values]) @ beta


def evaluate_law(df: pd.DataFrame, law: Dict[str, Dict[str, object]], model_name: str = "true_law") -> Tuple[List[dict], float]:
    rows = []
    rmses = []
    for target in LAW_FEATURES:
        pred = predict_target(df, law, target)
        y = df[target].values
        err = y - pred
        rr = safe_r2(y, pred)
        cc = safe_corr(y, pred)
        rm = rms(err)
        rows.append({"model": model_name, "target": target, "r2": rr, "corr": cc, "rms": rm})
        rmses.append(rm)
    compat = float(np.sqrt(np.mean(np.array(rmses) ** 2)))
    return rows, compat


def evaluate_adversarial(df: pd.DataFrame, law: Dict[str, Dict[str, object]]) -> Tuple[List[dict], float]:
    """
    Correct H, but momentum law scored against wrong rotated momentum targets.
    """
    rows = []
    rmses = []

    # H normal
    pred_H = predict_target(df, law, "H")
    y_H = df["H"].values
    rm = rms(y_H - pred_H)
    rows.append({"model": "bad_rotated_frame", "target": "H", "r2": safe_r2(y_H, pred_H), "corr": safe_corr(y_H, pred_H), "rms": rm})
    rmses.append(rm)

    # M parallel law against bad target
    pred_Mp = predict_target(df, law, "M_parallel")
    y_badp = df["M_bad_parallel"].values
    rm = rms(y_badp - pred_Mp)
    rows.append({"model": "bad_rotated_frame", "target": "M_bad_parallel", "r2": safe_r2(y_badp, pred_Mp), "corr": safe_corr(y_badp, pred_Mp), "rms": rm})
    rmses.append(rm)

    # M perp law against bad target
    pred_Mt = predict_target(df, law, "M_perp")
    y_badt = df["M_bad_perp"].values
    rm = rms(y_badt - pred_Mt)
    rows.append({"model": "bad_rotated_frame", "target": "M_bad_perp", "r2": safe_r2(y_badt, pred_Mt), "corr": safe_corr(y_badt, pred_Mt), "rms": rm})
    rmses.append(rm)

    compat = float(np.sqrt(np.mean(np.array(rmses) ** 2)))
    return rows, compat


def evaluate_shuffled(df: pd.DataFrame, law: Dict[str, Dict[str, object]], seed: int = 123) -> Tuple[List[dict], float]:
    rows = []
    rmses = []
    rng = np.random.default_rng(seed)
    for target in LAW_FEATURES:
        pred = predict_target(df, law, target, shuffled=True, rng=rng)
        y = df[target].values
        rm = rms(y - pred)
        rows.append({"model": "shuffled_features", "target": target, "r2": safe_r2(y, pred), "corr": safe_corr(y, pred), "rms": rm})
        rmses.append(rm)
    compat = float(np.sqrt(np.mean(np.array(rmses) ** 2)))
    return rows, compat


# -----------------------------
# Full-stack runner
# -----------------------------

def run_full_stack(config: RunConfig, outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)

    physics = FrozenPhysics(config)

    # 1. Build training stack at train_nx over several modes.
    train_frames = []
    for mode in config.train_modes:
        render = physics.render(config.train_nx, mode=mode)
        frame = compute_feature_frame(render, config)
        frame["nx"] = config.train_nx
        frame["mode"] = mode
        train_frames.append(frame)
    train_df = pd.concat(train_frames, ignore_index=True)

    # 2. Fit frozen compact law.
    law = fit_compact_law(train_df)

    # 3. Frozen transfer across test modes at train resolution.
    transfer_rows = []
    for mode in config.test_modes:
        frame = compute_feature_frame(physics.render(config.train_nx, mode=mode), config)
        frame["nx"] = config.train_nx
        frame["mode"] = mode

        rows, compat = evaluate_law(frame, law, model_name="true_law")
        for r in rows:
            r.update({"mode": mode, "nx": config.train_nx})
            transfer_rows.append(r)
        transfer_rows.append({"model": "true_law", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat, "mode": mode, "nx": config.train_nx})

        rows_bad, compat_bad = evaluate_adversarial(frame, law)
        for r in rows_bad:
            r.update({"mode": mode, "nx": config.train_nx})
            transfer_rows.append(r)
        transfer_rows.append({"model": "bad_rotated_frame", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat_bad, "mode": mode, "nx": config.train_nx})

        rows_shuf, compat_shuf = evaluate_shuffled(frame, law, seed=config.seed + 99)
        for r in rows_shuf:
            r.update({"mode": mode, "nx": config.train_nx})
            transfer_rows.append(r)
        transfer_rows.append({"model": "shuffled_features", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat_shuf, "mode": mode, "nx": config.train_nx})

    transfer_df = pd.DataFrame(transfer_rows)

    # 4. Resolution scaling using frozen law.
    scaling_rows = []
    for nx in config.ladder:
        frame = compute_feature_frame(physics.render(nx, mode="mixed"), config)
        frame["nx"] = nx
        frame["mode"] = "mixed"

        rows, compat = evaluate_law(frame, law, model_name="true_law")
        for r in rows:
            r.update({"nx": nx, "dx": 2.0 * config.bound / (nx - 1)})
            scaling_rows.append(r)
        scaling_rows.append({"model": "true_law", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat, "nx": nx, "dx": 2.0 * config.bound / (nx - 1)})

        rows_bad, compat_bad = evaluate_adversarial(frame, law)
        for r in rows_bad:
            r.update({"nx": nx, "dx": 2.0 * config.bound / (nx - 1)})
            scaling_rows.append(r)
        scaling_rows.append({"model": "bad_rotated_frame", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat_bad, "nx": nx, "dx": 2.0 * config.bound / (nx - 1)})

        rows_shuf, compat_shuf = evaluate_shuffled(frame, law, seed=config.seed + nx)
        for r in rows_shuf:
            r.update({"nx": nx, "dx": 2.0 * config.bound / (nx - 1)})
            scaling_rows.append(r)
        scaling_rows.append({"model": "shuffled_features", "target": "compatibility", "r2": np.nan, "corr": np.nan, "rms": compat_shuf, "nx": nx, "dx": 2.0 * config.bound / (nx - 1)})

    scaling_df = pd.DataFrame(scaling_rows)

    # 5. Summaries.
    transfer_summary = (
        transfer_df[transfer_df["target"] != "compatibility"]
        .groupby(["model", "target"])
        .agg(mean_r2=("r2", "mean"), min_r2=("r2", "min"), mean_corr=("corr", "mean"), mean_rms=("rms", "mean"))
        .reset_index()
    )

    transfer_compat = (
        transfer_df[transfer_df["target"] == "compatibility"]
        .groupby("model")
        .agg(mean_compat_rms=("rms", "mean"), max_compat_rms=("rms", "max"))
        .reset_index()
    )

    scaling_compat = scaling_df[scaling_df["target"] == "compatibility"].copy()

    scaling_summary_rows = []
    for model in scaling_compat["model"].unique():
        sub = scaling_compat[scaling_compat["model"] == model].sort_values("dx")
        if len(sub) >= 2:
            p, logc = np.polyfit(np.log(sub["dx"].values), np.log(sub["rms"].values), 1)
            p = float(p)
        else:
            p = float("nan")
        scaling_summary_rows.append({
            "model": model,
            "nx_min": int(sub["nx"].min()),
            "nx_max": int(sub["nx"].max()),
            "rms_at_lowest_nx": float(sub[sub["nx"] == sub["nx"].min()]["rms"].iloc[0]),
            "rms_at_highest_nx": float(sub[sub["nx"] == sub["nx"].max()]["rms"].iloc[0]),
            "improvement_low_to_high": float(sub[sub["nx"] == sub["nx"].min()]["rms"].iloc[0] - sub[sub["nx"] == sub["nx"].max()]["rms"].iloc[0]),
            "p_no_offset": p,
        })
    scaling_summary = pd.DataFrame(scaling_summary_rows)

    # 6. Verdict.
    true_transfer = transfer_summary[
        (transfer_summary["model"] == "true_law")
        & (transfer_summary["target"].isin(["H", "M_parallel", "M_perp"]))
    ]
    mean_true_r2 = float(true_transfer["mean_r2"].mean()) if not true_transfer.empty else float("nan")

    bad_compat = transfer_compat[transfer_compat["model"] == "bad_rotated_frame"]["mean_compat_rms"]
    true_compat = transfer_compat[transfer_compat["model"] == "true_law"]["mean_compat_rms"]
    shuf_compat = transfer_compat[transfer_compat["model"] == "shuffled_features"]["mean_compat_rms"]

    true_compat_v = float(true_compat.iloc[0]) if len(true_compat) else float("nan")
    bad_compat_v = float(bad_compat.iloc[0]) if len(bad_compat) else float("nan")
    shuf_compat_v = float(shuf_compat.iloc[0]) if len(shuf_compat) else float("nan")

    verdict = {
        "compact_law_supported": bool(mean_true_r2 > 0.80),
        "bad_frame_falsification_passed": bool(true_compat_v < bad_compat_v),
        "shuffled_falsification_passed": bool(true_compat_v < shuf_compat_v),
        "claim_boundary": "ADM-like same-slice constraint analog only; no GR/Einstein/physical-spacetime claim.",
    }

    result = {
        "document_id": "V832_FULL_STACK_SUCCESSOR_RUNNER",
        "config": asdict(config),
        "law": law,
        "summary": {
            "mean_true_transfer_r2": mean_true_r2,
            "true_compat_rms": true_compat_v,
            "bad_rotated_compat_rms": bad_compat_v,
            "shuffled_compat_rms": shuf_compat_v,
        },
        "verdict": verdict,
    }

    # 7. Write artifacts.
    law_path = outdir / "frozen_compact_flow_frame_law.json"
    result_path = outdir / "full_stack_results.json"
    transfer_path = outdir / "transfer_scores.csv"
    transfer_summary_path = outdir / "transfer_summary.csv"
    transfer_compat_path = outdir / "transfer_compatibility.csv"
    scaling_path = outdir / "resolution_scaling_scores.csv"
    scaling_summary_path = outdir / "resolution_scaling_summary.csv"
    report_path = outdir / "FULL_STACK_REPORT.md"

    law_path.write_text(json.dumps(law, indent=2))
    result_path.write_text(json.dumps(result, indent=2))
    transfer_df.to_csv(transfer_path, index=False)
    transfer_summary.to_csv(transfer_summary_path, index=False)
    transfer_compat.to_csv(transfer_compat_path, index=False)
    scaling_df.to_csv(scaling_path, index=False)
    scaling_summary.to_csv(scaling_summary_path, index=False)

    transfer_summary_md = transfer_summary.to_markdown(index=False)
    transfer_compat_md = transfer_compat.to_markdown(index=False)
    scaling_summary_md = scaling_summary.to_markdown(index=False)

    report = f"""# UQCF-GEM / Recoverability Accessibility Full-Stack Run Report

## Document ID

V832_FULL_STACK_SUCCESSOR_RUNNER_OUTPUT

## Claim Boundary

This run tests ADM-like same-slice constraint analogs in an ordered accessibility-flow simulation.

It does **not** establish Einstein equations, physical GR, physical spacetime curvature, or a continuum theorem.

## Compact Law

```text
H          ~ access_curv + A_n + K_n + K2_n
M_parallel ~ Jmag + dJ_parallel + divJ
M_perp     ~ Jmag + dJ_perp + divJ
```

## Summary

```json
{json.dumps(result["summary"], indent=2)}
```

## Verdict

```json
{json.dumps(verdict, indent=2)}
```

## Transfer Summary

{transfer_summary_md}

## Compatibility Summary

{transfer_compat_md}

## Resolution Scaling Summary

{scaling_summary_md}

## Successor-AI Instructions

1. Treat this as an empirical bounded-lattice full stack.
2. Do not claim GR or Einstein recovery.
3. Do not add heuristic smoothing terms.
4. If continuing, prioritize:
   - variational formalization
   - boundary/operator analysis
   - non-Cartesian graph/mesh tests
   - spectral or Green-function operators
5. Preserve the ordered-update guardrail: the simulation index is not physical time.
"""

    report_path.write_text(report)

    return {
        "result": result,
        "paths": {
            "law": str(law_path),
            "result": str(result_path),
            "transfer_scores": str(transfer_path),
            "transfer_summary": str(transfer_summary_path),
            "transfer_compatibility": str(transfer_compat_path),
            "resolution_scaling_scores": str(scaling_path),
            "resolution_scaling_summary": str(scaling_summary_path),
            "report": str(report_path),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run UQCF-GEM full-stack ADM-like accessibility-flow audit.")
    parser.add_argument("--outdir", type=str, default="uqcf_gem_full_stack_output", help="Output directory.")
    parser.add_argument("--seed", type=int, default=832, help="Frozen physics seed.")
    parser.add_argument("--operator-order", type=int, default=2, choices=[2, 4], help="Finite difference stencil order.")
    parser.add_argument("--train-nx", type=int, default=32, help="Training resolution.")
    parser.add_argument("--nt", type=int, default=12, help="Ordered-update slices.")
    parser.add_argument("--defects", type=int, default=7, help="Number of defect sources.")
    parser.add_argument("--complexity", type=int, default=4, help="Dynamics complexity.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = RunConfig(
        seed=args.seed,
        operator_order=args.operator_order,
        train_nx=args.train_nx,
        nt=args.nt,
        defects=args.defects,
        complexity=args.complexity,
    )
    out = run_full_stack(config, Path(args.outdir))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
