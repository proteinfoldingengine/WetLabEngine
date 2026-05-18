#!/usr/bin/env python3
# ==============================================================================
# V724 STRESS-TEST RECOVERABILITY AUDIT
# Retained Atlas / Active Restoration Observability Harness
#
# Purpose:
#   V723 showed that active post-perturbation restoration deficit can separate
#   low restorative capacity from high restorative capacity while passive burden
#   is held equivalent. V724 deliberately makes the assay harder.
#
# Observation-only posture:
#   This script reports what is observed in a controlled synthetic assay. It does
#   not claim a universal law, physical proof, GR result, quantum result, or
#   real-world generalization.
#
# Stressors added beyond V723:
#   - overlapping high/low k distributions
#   - nonlinear restoration saturation
#   - reserve fatigue across repeated probes
#   - stochastic restoration stalls
#   - perturbation-family variation
#   - short/aliased observation-window sweep
#
# Specificity control retained from V723:
#   Passive burden is generated once per pair and shared by both counterfactual
#   branches. Passive metrics are therefore identical within a pair. Only the
#   active relaxation response sees k and stressor effects.
# ==============================================================================

from __future__ import annotations

import argparse
import json
import math
import warnings
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

try:
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

try:
    from sklearn.metrics import roc_auc_score, f1_score, roc_curve
    HAVE_SKLEARN = True
except Exception:
    HAVE_SKLEARN = False


@dataclass
class HarnessConfig:
    seed: int = 724
    n_grid: int = 24
    n_steps: int = 170
    probe_times: Tuple[int, ...] = (50, 85, 120)
    relax_steps: int = 14
    n_calibration_pairs: int = 24
    n_test_pairs: int = 48
    perturb_amp: float = 1.20
    field_noise: float = 0.009
    relax_noise: float = 0.010
    evolve_dt: float = 0.055
    relax_dt: float = 0.080
    diffusion_coupling: float = 0.035
    passive_background_restore: float = 0.012
    damping: float = 1.0
    # Overlapping capacity distributions. These are intentionally not cleanly separated.
    high_k_mean: float = 0.86
    high_k_sd: float = 0.08
    low_k_mean: float = 0.66
    low_k_sd: float = 0.10
    k_min: float = 0.20
    k_max: float = 1.10
    # Stress physics for active branch only.
    saturation_strength: float = 0.55
    fatigue_strength: float = 0.16
    stall_base: float = 0.035
    stall_low_k_boost: float = 0.18
    overshoot_prob: float = 0.035
    bootstrap_n: int = 100
    make_png: bool = True
    output_dir: str = "v724_stress_test_outputs"


PERTURBATION_FAMILIES = ("gaussian", "ring", "stripe", "multi_site", "sinusoidal")


def initialize_geometry(n: int) -> Dict[str, np.ndarray]:
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)

    T = (np.exp(-((X - 0.35) ** 2 + (Y - 0.40) ** 2) / 0.080)
         + np.exp(-((X - 0.72) ** 2 + (Y - 0.65) ** 2) / 0.090)) * 1.15
    T = np.clip(T, 0.05, 1.8)

    lineage_weak = np.exp(-((X - 0.52) ** 2 + (Y - 0.48) ** 2) / 0.025)
    pinch = np.exp(-((X - 0.62) ** 2 + (Y - 0.50) ** 2) / 0.045)

    M = np.clip(0.65 - 0.35 * T, 0.15, 1.10)
    R = np.clip(0.55 + 0.35 * (1 - lineage_weak) - 0.25 * pinch, 0.10, 1.20)
    L = np.clip(0.45 + 0.45 * (1 - pinch) - 0.20 * T, 0.10, 1.15)

    C = M * R * L
    C_floor = np.clip(0.18 + 0.32 * T + 0.22 * pinch, 0.08, 0.85)
    Omega_target = np.clip(1.0 + 0.75 * (C - C_floor), 0.30, 4.50)

    return {"X": X, "Y": Y, "T": T, "lineage_weak": lineage_weak, "pinch": pinch,
            "M": M, "R": R, "L": L, "C": C, "C_floor": C_floor,
            "Omega_target": Omega_target}


def laplacian(A: np.ndarray) -> np.ndarray:
    return (np.roll(A, 1, axis=0) + np.roll(A, -1, axis=0)
            + np.roll(A, 1, axis=1) + np.roll(A, -1, axis=1) - 4 * A)


def curvature_like(A: np.ndarray) -> np.ndarray:
    return laplacian(A)


def mean_abs_to_target(A: np.ndarray, target: np.ndarray) -> float:
    return float(np.mean(np.abs(A - target)))


def l2_to_target(A: np.ndarray, target: np.ndarray) -> float:
    return float(np.sqrt(np.mean((A - target) ** 2)))


def safe_auc(y: Iterable[int], score: Iterable[float]) -> float:
    y = np.asarray(list(y))
    score = np.asarray(list(score))
    if len(np.unique(y)) < 2 or len(np.unique(score)) < 2:
        return float("nan")
    return float(roc_auc_score(y, score))


def safe_f1(y: Iterable[int], pred: Iterable[int]) -> float:
    y = np.asarray(list(y))
    pred = np.asarray(list(pred))
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(f1_score(y, pred))


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, n_boot: int = 300) -> Tuple[float, float]:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return float("nan"), float("nan")
    draws = []
    for _ in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        draws.append(float(np.mean(sample)))
    return float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, rng: np.random.Generator, n_boot: int = 300) -> Tuple[float, float]:
    y = np.asarray(y)
    score = np.asarray(score)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        if len(np.unique(y[idx])) < 2:
            continue
        vals.append(safe_auc(y[idx], score[idx]))
    if not vals:
        return float("nan"), float("nan")
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


class RetainedAtlasEngine:
    def __init__(self, cfg: HarnessConfig):
        self.cfg = cfg
        self.state = initialize_geometry(cfg.n_grid)
        self.Source = self.state["T"] / (np.maximum(self.state["C"] - self.state["C_floor"], 0.02) + 1e-8)
        self.Repair = 0.28 * self.state["M"] + 0.32 * self.state["R"] + 0.28 * self.state["L"]
        self.mu_defect = 0.55 * self.state["T"] * (1 - self.state["L"])

    @property
    def target(self) -> np.ndarray:
        return self.state["Omega_target"]

    def make_perturbation(self, rng: np.random.Generator, family: str) -> np.ndarray:
        X, Y = self.state["X"], self.state["Y"]
        sign = rng.choice([-1.0, 1.0])
        cx = 0.48 + 0.18 * rng.normal()
        cy = 0.52 + 0.18 * rng.normal()
        if family == "gaussian":
            mask = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.035)
        elif family == "ring":
            r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
            mask = np.exp(-((r - 0.18) ** 2) / 0.006)
        elif family == "stripe":
            theta = rng.uniform(0, np.pi)
            coord = np.cos(theta) * (X - cx) + np.sin(theta) * (Y - cy)
            mask = np.exp(-(coord ** 2) / 0.010)
        elif family == "multi_site":
            mask = np.zeros_like(X)
            for _ in range(3):
                cx_i = 0.50 + 0.25 * rng.normal()
                cy_i = 0.50 + 0.25 * rng.normal()
                s_i = rng.choice([-1.0, 1.0])
                mask += s_i * np.exp(-((X - cx_i) ** 2 + (Y - cy_i) ** 2) / 0.025)
            return mask / (np.max(np.abs(mask)) + 1e-12)
        elif family == "sinusoidal":
            fx = rng.integers(1, 5)
            fy = rng.integers(1, 5)
            phase = rng.uniform(0, 2 * np.pi)
            mask = np.sin(2 * np.pi * (fx * X + fy * Y) + phase)
        else:
            raise ValueError(f"Unknown perturbation family: {family}")
        mask = sign * mask
        return mask / (np.max(np.abs(mask)) + 1e-12)

    def make_streams(self, seed: int, relax_steps: int | None = None):
        cfg = self.cfg
        relax_steps = cfg.relax_steps if relax_steps is None else int(relax_steps)
        rng = np.random.default_rng(seed)
        shape = self.target.shape
        initial_noise = rng.normal(0, 0.015, shape)
        field_noises = rng.normal(0, cfg.field_noise, (cfg.n_steps, *shape))
        perturbations = []
        relax_noises = []
        for i, _t in enumerate(cfg.probe_times):
            family = PERTURBATION_FAMILIES[i % len(PERTURBATION_FAMILIES)]
            perturbations.append((family, self.make_perturbation(rng, family)))
            relax_noises.append(rng.normal(0, cfg.relax_noise, (relax_steps, *shape)))
        branch_randoms = rng.random((len(cfg.probe_times), 4))
        return initial_noise, field_noises, relax_noises, perturbations, branch_randoms

    def passive_baseline(self, initial_noise: np.ndarray, field_noises: np.ndarray):
        cfg = self.cfg
        Omega = np.clip(self.target + initial_noise, 0.25, 5.0)
        pre_probe_states = {}
        passive_distances, passive_peak_trace, passive_l2 = [], [], []
        curv, defect = [], []
        for t in range(cfg.n_steps):
            dOmega = 0.040 * (self.Source - self.Repair - self.mu_defect)
            dOmega += cfg.diffusion_coupling * laplacian(Omega)
            dOmega += -cfg.passive_background_restore * (Omega - self.target)
            Omega += cfg.evolve_dt * dOmega + field_noises[t]
            Omega = np.clip(Omega, 0.25, 5.0)
            if t in set(cfg.probe_times):
                pre_probe_states[t] = Omega.copy()
            d = mean_abs_to_target(Omega, self.target)
            passive_distances.append(d)
            passive_peak_trace.append(d)
            passive_l2.append(l2_to_target(Omega, self.target))
            curv.append(float(np.mean(np.abs(curvature_like(Omega)))))
            defect.append(float(np.mean(np.abs(Omega - self.target) * self.mu_defect)))
        meta = {
            "passive_mean_distance": float(np.mean(passive_distances)),
            "passive_peak_distance": float(np.max(passive_peak_trace)),
            "passive_l2_mean": float(np.mean(passive_l2)),
            "mean_curvature_like_energy": float(np.mean(curv)),
            "mean_defect_weighted_error": float(np.mean(defect)),
        }
        return pre_probe_states, meta

    def active_relax_once(self, pre: np.ndarray, perturb: np.ndarray, relax_noise: np.ndarray,
                          k: float, damping: float, branch_random: np.ndarray,
                          fatigue_load: float) -> Tuple[float, float, float, float, float, float]:
        cfg = self.cfg
        Omega = np.clip(pre + cfg.perturb_amp * perturb, 0.25, 5.0)
        start_dist = mean_abs_to_target(Omega, self.target)

        # Stressors: nonlinear saturation, fatigue, stochastic stalls, occasional overshoot.
        # All are active-response terms. Passive baseline remains unchanged.
        initial_error = np.abs(Omega - self.target)
        saturation = 1.0 / (1.0 + cfg.saturation_strength * float(np.mean(initial_error)))
        fatigue = 1.0 / (1.0 + cfg.fatigue_strength * fatigue_load)
        stall_prob = np.clip(cfg.stall_base + cfg.stall_low_k_boost * max(0.0, 0.75 - k), 0.0, 0.55)
        stalled = branch_random[0] < stall_prob
        overshoot = branch_random[1] < cfg.overshoot_prob
        stall_factor = 0.22 if stalled else 1.0
        effective_k = k * saturation * fatigue * stall_factor
        if overshoot:
            effective_k *= 1.35

        for j in range(relax_noise.shape[0]):
            flow = -(effective_k / damping) * (Omega - self.target)
            smooth = 0.040 * laplacian(Omega)
            if overshoot and j > relax_noise.shape[0] // 2:
                # Small late overshoot term: correction can go too far in stressed systems.
                flow += 0.025 * (Omega - self.target)
            Omega += cfg.relax_dt * flow + smooth + relax_noise[j]
            Omega = np.clip(Omega, 0.25, 5.0)
        post_dist = mean_abs_to_target(Omega, self.target)
        post_l2 = l2_to_target(Omega, self.target)
        gain = start_dist - post_dist
        shock = float(np.mean(np.abs(cfg.perturb_amp * perturb)))
        return start_dist, post_dist, post_l2, gain, shock, effective_k

    def run_pair(self, pair_id: str, seed: int, k_high: float, k_low: float,
                 split: str, relax_steps: int | None = None, damping: float | None = None):
        cfg = self.cfg
        relax_steps = cfg.relax_steps if relax_steps is None else int(relax_steps)
        damping = cfg.damping if damping is None else float(damping)
        initial_noise, field_noises, relax_noises, perturbations, branch_randoms = self.make_streams(seed, relax_steps)
        pre_states, passive_meta = self.passive_baseline(initial_noise, field_noises)
        rows = []
        probe_rows = []
        for condition, k, label in [("high_k_admissible", k_high, 0), ("low_k_test", k_low, 1)]:
            post, post_l2, start, gain, shock, effks = [], [], [], [], [], []
            fams = []
            fatigue_load = 0.0
            for idx, t in enumerate(cfg.probe_times):
                fam, perturb = perturbations[idx]
                branch_rand = branch_randoms[idx].copy()
                # Same branch random coordinates, but active stall threshold depends on k.
                s, p, pl2, g, sh, ek = self.active_relax_once(
                    pre_states[t], perturb, relax_noises[idx], k, damping, branch_rand, fatigue_load
                )
                fatigue_load += max(0.0, sh - g)
                start.append(s); post.append(p); post_l2.append(pl2); gain.append(g); shock.append(sh); effks.append(ek); fams.append(fam)
                probe_rows.append({
                    "pair_id": pair_id, "run_id": f"{pair_id}_{condition}", "condition": condition,
                    "failure_label": label, "split": split, "probe_time": int(t), "family": fam,
                    "k_nominal": float(k), "effective_k": float(ek), "start_dist": s,
                    "post_dist": p, "post_l2": pl2, "raw_restoration_gain": g,
                    "shock_magnitude": sh, **passive_meta,
                })
            rows.append({
                "pair_id": pair_id, "run_id": f"{pair_id}_{condition}", "condition": condition,
                "failure_label": label, "admissible_flag": condition == "high_k_admissible", "split": split,
                "k_nominal": float(k), "effective_k_mean": float(np.mean(effks)),
                "restoration_measure": float(np.mean(post)), "restoration_measure_l2": float(np.mean(post_l2)),
                "probe_start_mean": float(np.mean(start)), "probe_post_mean": float(np.mean(post)),
                "probe_gain_mean": float(np.mean(gain)), "probe_gain_std": float(np.std(gain, ddof=1)),
                "shock_magnitude_mean": float(np.mean(shock)),
                "families": ";".join(fams), **passive_meta,
            })
        return rows, probe_rows


def sample_k_values(cfg: HarnessConfig, rng: np.random.Generator, overlap_shift: float = 0.0) -> Tuple[float, float]:
    high = rng.normal(cfg.high_k_mean - overlap_shift, cfg.high_k_sd)
    low = rng.normal(cfg.low_k_mean + overlap_shift, cfg.low_k_sd)
    return float(np.clip(high, cfg.k_min, cfg.k_max)), float(np.clip(low, cfg.k_min, cfg.k_max))


def add_calibration(run_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    cal = run_df[(run_df["split"] == "calibration") & (run_df["admissible_flag"] == True)]
    out = run_df.copy()
    adm_mean = cal["restoration_measure"].mean()
    adm_std = cal["restoration_measure"].std(ddof=1) + 1e-12
    adm_l2_mean = cal["restoration_measure_l2"].mean()
    adm_l2_std = cal["restoration_measure_l2"].std(ddof=1) + 1e-12
    out["adm_z"] = (out["restoration_measure"] - adm_mean) / adm_std
    out["adm_z_l2"] = (out["restoration_measure_l2"] - adm_l2_mean) / adm_l2_std
    for src, dst in [
        ("passive_mean_distance", "passive_mean_z"),
        ("passive_peak_distance", "passive_peak_z"),
        ("probe_start_mean", "probe_start_z"),
        ("mean_curvature_like_energy", "curvature_like_z"),
        ("mean_defect_weighted_error", "defect_weighted_z"),
        ("effective_k_mean", "effective_k_z"),
    ]:
        mu = cal[src].mean()
        sd = cal[src].std(ddof=1) + 1e-12
        out[dst] = (out[src] - mu) / sd
    return out, {
        "adm_mean_restoration": float(adm_mean),
        "adm_std_restoration": float(adm_std),
        "n_calibration_admissible": int(len(cal)),
    }


def evaluate_scores(df: pd.DataFrame, prefix: str = "") -> Dict:
    y = df["failure_label"].to_numpy()
    out = {f"{prefix}n": int(len(df)), f"{prefix}n_positive": int(y.sum()), f"{prefix}n_negative": int((y == 0).sum())}
    for score in ["adm_z", "adm_z_l2", "passive_mean_z", "passive_peak_z", "probe_start_z", "curvature_like_z", "defect_weighted_z", "effective_k_z"]:
        out[f"{prefix}auc_{score}"] = safe_auc(y, df[score].to_numpy())
    for threshold in [0.75, 1.0, 1.5, 2.0]:
        pred = (df["adm_z"].to_numpy() > threshold).astype(int)
        out[f"{prefix}f1_adm_z_gt_{threshold}"] = safe_f1(y, pred)
        out[f"{prefix}flag_rate_adm_z_gt_{threshold}"] = float(pred.mean())
    return out


def paired_deltas(test_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pair_id, g in test_df.groupby("pair_id"):
        if len(g) != 2:
            continue
        hi = g[g["failure_label"] == 0].iloc[0]
        lo = g[g["failure_label"] == 1].iloc[0]
        row = {"pair_id": pair_id}
        for col in ["adm_z", "restoration_measure", "probe_gain_mean", "passive_mean_distance", "passive_peak_distance", "probe_start_mean", "mean_curvature_like_energy", "mean_defect_weighted_error", "effective_k_mean"]:
            row[f"delta_{col}"] = float(lo[col] - hi[col])
        rows.append(row)
    return pd.DataFrame(rows)


def run_main(cfg: HarnessConfig):
    engine = RetainedAtlasEngine(cfg)
    rng = np.random.default_rng(cfg.seed)
    rows, probe_rows = [], []
    for i in range(cfg.n_calibration_pairs):
        kh, kl = sample_k_values(cfg, rng)
        r, p = engine.run_pair(f"cal_{i:04d}", cfg.seed + i, kh, kl, "calibration")
        rows.extend(r); probe_rows.extend(p)
    for i in range(cfg.n_test_pairs):
        kh, kl = sample_k_values(cfg, rng)
        r, p = engine.run_pair(f"test_{i:04d}", cfg.seed + 10000 + i, kh, kl, "test")
        rows.extend(r); probe_rows.extend(p)
    run_df = pd.DataFrame(rows)
    probe_df = pd.DataFrame(probe_rows)
    run_df, cal = add_calibration(run_df)
    test_df = run_df[run_df["split"] == "test"].copy()
    pdeltas = paired_deltas(test_df)
    brng = np.random.default_rng(cfg.seed + 44)
    ev = evaluate_scores(test_df, prefix="test_")
    auc_lo, auc_hi = bootstrap_auc_ci(test_df["failure_label"].to_numpy(), test_df["adm_z"].to_numpy(), brng, cfg.bootstrap_n)
    p_auc_lo, p_auc_hi = bootstrap_auc_ci(test_df["failure_label"].to_numpy(), test_df["passive_mean_z"].to_numpy(), brng, cfg.bootstrap_n)
    d_lo, d_hi = bootstrap_ci(pdeltas["delta_adm_z"].to_numpy(), brng, cfg.bootstrap_n)
    summary = {
        "version": "V724_StressTestRecoverabilityAudit",
        "seed": cfg.seed,
        "observation_posture": "controlled synthetic assay; observation-only reporting; no universal claim",
        "stressors": ["overlapping_k", "nonlinear_saturation", "reserve_fatigue", "stochastic_stalls", "perturbation_families", "short_window_sweep"],
        **cal,
        **ev,
        "paired_delta_adm_z_mean": float(pdeltas["delta_adm_z"].mean()),
        "paired_delta_adm_z_ci95_low": d_lo,
        "paired_delta_adm_z_ci95_high": d_hi,
        "paired_delta_passive_mean_distance_mean": float(pdeltas["delta_passive_mean_distance"].mean()),
        "paired_delta_passive_mean_distance_abs_max": float(np.abs(pdeltas["delta_passive_mean_distance"]).max()),
        "auc_adm_z_ci95_low": auc_lo,
        "auc_adm_z_ci95_high": auc_hi,
        "auc_passive_mean_z_ci95_low": p_auc_lo,
        "auc_passive_mean_z_ci95_high": p_auc_hi,
        "specificity_gap_auc_adm_minus_passive_mean": float(ev["test_auc_adm_z"] - ev["test_auc_passive_mean_z"]),
        "mean_high_k_nominal_test": float(test_df[test_df.failure_label == 0]["k_nominal"].mean()),
        "mean_low_k_nominal_test": float(test_df[test_df.failure_label == 1]["k_nominal"].mean()),
        "min_high_k_nominal_test": float(test_df[test_df.failure_label == 0]["k_nominal"].min()),
        "max_low_k_nominal_test": float(test_df[test_df.failure_label == 1]["k_nominal"].max()),
    }
    return engine, run_df, probe_df, test_df, pdeltas, summary


def k_gap_sweep(cfg: HarnessConfig, n_pairs: int = 6) -> pd.DataFrame:
    rows = []
    for gap in [0.00, 0.10, 0.20, 0.35]:
        c2 = HarnessConfig(**asdict(cfg))
        c2.n_calibration_pairs = max(18, n_pairs // 2)
        c2.n_test_pairs = n_pairs
        center = 0.76
        c2.high_k_mean = center + gap / 2
        c2.low_k_mean = center - gap / 2
        c2.high_k_sd = 0.09
        c2.low_k_sd = 0.09
        c2.seed = cfg.seed + int(gap * 10000) + 400
        _, _, _, test_df, pdeltas, summary = run_main(c2)
        rows.append({
            "k_gap_mean": gap,
            "auc_adm_z": summary["test_auc_adm_z"],
            "auc_passive_mean_z": summary["test_auc_passive_mean_z"],
            "mean_delta_adm_z": summary["paired_delta_adm_z_mean"],
            "mean_delta_passive": summary["paired_delta_passive_mean_distance_mean"],
            "n": summary["test_n"],
        })
    return pd.DataFrame(rows)


def window_sweep(cfg: HarnessConfig, n_pairs: int = 6) -> pd.DataFrame:
    rows = []
    combos = [(3, 2.5), (6, 1.75), (10, 1.25), (14, 1.0)]
    for relax_steps, damping in combos:
        c2 = HarnessConfig(**asdict(cfg))
        c2.n_calibration_pairs = max(18, n_pairs // 2)
        c2.n_test_pairs = n_pairs
        c2.relax_steps = relax_steps
        c2.damping = damping
        c2.seed = cfg.seed + relax_steps * 100 + int(damping * 1000)
        _, _, _, test_df, pdeltas, summary = run_main(c2)
        rows.append({
            "relax_steps": relax_steps,
            "damping": damping,
            "effective_window": relax_steps / damping,
            "auc_adm_z": summary["test_auc_adm_z"],
            "auc_passive_mean_z": summary["test_auc_passive_mean_z"],
            "mean_delta_adm_z": summary["paired_delta_adm_z_mean"],
            "n": summary["test_n"],
        })
    return pd.DataFrame(rows)


def perturbation_family_summary(probe_df: pd.DataFrame, run_df: pd.DataFrame) -> pd.DataFrame:
    # Uses per-probe post distance standardized by high-k calibration probe distribution per family.
    cal = probe_df[(probe_df["split"] == "calibration") & (probe_df["failure_label"] == 0)]
    rows = []
    test = probe_df[probe_df["split"] == "test"].copy()
    for fam, g in test.groupby("family"):
        mu = cal[cal.family == fam]["post_dist"].mean()
        sd = cal[cal.family == fam]["post_dist"].std(ddof=1) + 1e-12
        score = (g["post_dist"] - mu) / sd
        rows.append({
            "family": fam,
            "n": int(len(g)),
            "auc_probe_family_post_z": safe_auc(g["failure_label"], score),
            "mean_post_z_low_minus_high": float(score[g["failure_label"].to_numpy() == 1].mean() - score[g["failure_label"].to_numpy() == 0].mean()),
        })
    return pd.DataFrame(rows)


def make_plots(out_dir: Path, test_df: pd.DataFrame, pdeltas: pd.DataFrame, gap_df: pd.DataFrame, window_df: pd.DataFrame):
    if not HAVE_MPL:
        return
    # Distribution
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.hist(test_df[test_df.failure_label == 0]["adm_z"], bins=24, alpha=0.65, label="high-k admissible")
    ax.hist(test_df[test_df.failure_label == 1]["adm_z"], bins=24, alpha=0.65, label="low-k test")
    ax.axvline(0, linestyle="--")
    ax.set_title("V724 stress test: held-out restoration deficit")
    ax.set_xlabel("adm_z: post-probe restoration deficit")
    ax.set_ylabel("count")
    ax.legend()
    fig.savefig(out_dir / "adm_z_distribution.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # ROC
    fig, ax = plt.subplots(figsize=(10, 8))
    y = test_df["failure_label"].to_numpy()
    for score, label in [("adm_z", "adm_z"), ("passive_mean_z", "passive mean"), ("probe_start_z", "probe start"), ("curvature_like_z", "curvature-like")]:
        if len(np.unique(test_df[score])) < 2:
            continue
        fpr, tpr, _ = roc_curve(y, test_df[score].to_numpy())
        ax.plot(fpr, tpr, label=f"{label} AUC={safe_auc(y, test_df[score]):.3f}")
    ax.plot([0, 1], [0, 1], "--", label="chance")
    ax.set_title("V724 specificity under stress: active restoration vs passive burden")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend(loc="lower right")
    fig.savefig(out_dir / "roc_specificity_comparison.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # paired deltas
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.hist(pdeltas["delta_adm_z"], bins=24, alpha=0.7, label="Δadm_z")
    ax.hist(pdeltas["delta_passive_mean_distance"], bins=24, alpha=0.7, label="Δpassive_mean")
    ax.axvline(0, linestyle="--")
    ax.set_title("V724 paired contrast under stress")
    ax.set_xlabel("low-k minus high-k")
    ax.set_ylabel("paired count")
    ax.legend()
    fig.savefig(out_dir / "paired_delta_adm_z_vs_passive.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # k gap
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(gap_df["k_gap_mean"], gap_df["auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(gap_df["k_gap_mean"], gap_df["auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--")
    ax.set_title("V724 k-gap stress sweep under passive equivalence")
    ax.set_xlabel("mean k gap")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "k_gap_sweep.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # window
    fig, ax = plt.subplots(figsize=(12, 7))
    w = window_df.sort_values("effective_window")
    ax.plot(w["effective_window"], w["auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(w["effective_window"], w["auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--")
    ax.set_title("V724 observation-window stress sweep")
    ax.set_xlabel("effective window ≈ relax_steps / damping")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "window_sweep.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def write_report(out_dir: Path, cfg: HarnessConfig, summary: Dict, gap_df: pd.DataFrame, window_df: pd.DataFrame, fam_df: pd.DataFrame):
    report = f"""# V724 Stress-Test Recoverability Audit

## Posture

This is an observation-only synthetic assay. It reports measured behavior in the run. It does not claim a universal law, physical theorem, biological law, GR result, or real-world generalization.

## Why V724 exists

V723 held passive burden equivalent and observed that active post-perturbation restoration deficit separated high-restoration and low-restoration branches while passive metrics remained near chance. V724 asks whether that observation survives a harder assay.

## Added stressors

- overlapping high/low restorative-capacity distributions,
- nonlinear restoration saturation,
- reserve fatigue across repeated probes,
- stochastic restoration stalls,
- perturbation-family variation,
- shorter and aliased observation windows.

## Preserved specificity control

For every counterfactual pair, the passive baseline is generated once and shared. Passive mean distance, passive peak distance, probe-start burden, curvature-like energy, and defect-weighted burden are therefore passive-equivalent by construction. Only active relaxation sees the sampled capacity and stress-response terms.

## Main summary

```json
{json.dumps(summary, indent=2)}
```

## K-gap stress sweep

{gap_df.to_markdown(index=False)}

## Observation-window stress sweep

{window_df.to_markdown(index=False)}

## Perturbation-family summary

{fam_df.to_markdown(index=False)}

## Reading guide

- `adm_z` is the held-out restoration deficit standardized from high-k calibration runs.
- Higher `adm_z` means worse post-probe restoration relative to the admissible calibration norm.
- Passive AUC near 0.5 means passive burden did not separate the labels in that assay.
- If `adm_z` remains above passive controls under stress, the observation from V723 is more robust.
- If `adm_z` collapses toward chance under stress, the result identifies a boundary condition rather than a failure.

## Output files

- `summary.json`
- `summary_metrics.csv`
- `audit_log.csv`
- `probe_log.csv`
- `paired_counterfactual_deltas.csv`
- `k_gap_sweep.csv`
- `window_sweep.csv`
- `perturbation_family_summary.csv`
- `adm_z_distribution.png`
- `roc_specificity_comparison.png`
- `paired_delta_adm_z_vs_passive.png`
- `k_gap_sweep.png`
- `window_sweep.png`
"""
    (out_dir / "V724_OBSERVATION_REPORT.md").write_text(report)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output_dir", default="v724_stress_test_outputs")
    ap.add_argument("--seed", type=int, default=724)
    ap.add_argument("--n_test_pairs", type=int, default=48)
    ap.add_argument("--n_calibration_pairs", type=int, default=24)
    ap.add_argument("--no_png", action="store_true")
    ap.add_argument("--zip", action="store_true", default=True)
    args, _unknown = ap.parse_known_args()
    return args


def main():
    if not HAVE_SKLEARN:
        raise RuntimeError("scikit-learn is required for ROC/AUC metrics.")
    args = parse_args()
    cfg = HarnessConfig(seed=args.seed, n_test_pairs=args.n_test_pairs,
                        n_calibration_pairs=args.n_calibration_pairs,
                        output_dir=args.output_dir, make_png=not args.no_png)
    out_dir = Path(cfg.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[V724] Running main stress-test audit...")
    engine, run_df, probe_df, test_df, pdeltas, summary = run_main(cfg)
    print("[V724] Running k-gap stress sweep...")
    gap_df = k_gap_sweep(cfg)
    print("[V724] Running observation-window stress sweep...")
    window_df = window_sweep(cfg)
    fam_df = perturbation_family_summary(probe_df, run_df)

    run_df.to_csv(out_dir / "audit_log.csv", index=False)
    probe_df.to_csv(out_dir / "probe_log.csv", index=False)
    test_df.to_csv(out_dir / "heldout_test_log.csv", index=False)
    pdeltas.to_csv(out_dir / "paired_counterfactual_deltas.csv", index=False)
    gap_df.to_csv(out_dir / "k_gap_sweep.csv", index=False)
    window_df.to_csv(out_dir / "window_sweep.csv", index=False)
    fam_df.to_csv(out_dir / "perturbation_family_summary.csv", index=False)
    pd.DataFrame([summary]).to_csv(out_dir / "summary_metrics.csv", index=False)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    config_json = asdict(cfg)
    config_json["probe_times"] = list(cfg.probe_times)
    (out_dir / "config.json").write_text(json.dumps(config_json, indent=2))

    print("[V724] Generating plots...")
    make_plots(out_dir, test_df, pdeltas, gap_df, window_df)
    write_report(out_dir, cfg, summary, gap_df, window_df, fam_df)

    zip_path = out_dir.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(Path(__file__), arcname=Path(__file__).name)
        for p in sorted(out_dir.iterdir()):
            z.write(p, arcname=p.name)

    print("\n=== V724 SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nOutputs written to:", out_dir)
    print("ZIP written to:", zip_path)


if __name__ == "__main__":
    main()
