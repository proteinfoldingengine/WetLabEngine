#!/usr/bin/env python3
# ==============================================================================
# V723 PASSIVE-EQUIVALENT RECOVERABILITY AUDIT
# Retained Atlas / Response-Transfer Law-Discovery Harness
#
# Scientific purpose:
#   V722 established a real counterfactual k signal, but passive burden metrics
#   also separated perfectly. V723 makes the test harder: passive burden is held
#   equivalent by construction, and restorative capacity k is expressed only in
#   the active probe relaxation assay.
#
# Core question:
#   Can active post-perturbation restoration deficit identify hidden recoverability
#   when passive burden metrics are unable to separate high-k from low-k systems?
#
# Core design:
#   1. Generate one shared passive baseline trajectory per pair, independent of k.
#   2. At probe times, branch from the same pre-probe state into high-k and low-k
#      counterfactual relaxation assays.
#   3. Use identical perturbation masks and identical relaxation noise in each pair.
#   4. Record identical passive_mean, passive_peak, and probe_start burden for the
#      high-k and low-k members of every pair.
#   5. Test whether adm_z separates while passive metrics collapse toward chance.
#
# Peer-review posture:
#   Exploratory first-principles synthetic systems harness. This is not a proof of
#   GR, quantum collapse, or a universal physical law. It is a stricter assay for
#   a candidate operational law of recoverability.
# ==============================================================================

from __future__ import annotations

import argparse
import json
import math
import warnings
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

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
    seed: int = 723
    n_grid: int = 48
    n_steps: int = 260
    probe_times: Tuple[int, ...] = (75, 110, 145, 180, 215)
    relax_steps: int = 18
    high_k: float = 1.0
    low_k: float = 0.35
    n_calibration_pairs: int = 24
    n_test_pairs: int = 36
    perturb_amp: float = 1.20
    field_noise: float = 0.007
    relax_noise: float = 0.0055
    evolve_dt: float = 0.055
    relax_dt: float = 0.085
    diffusion_coupling: float = 0.035
    passive_background_restore: float = 0.012
    damping: float = 1.0
    bootstrap_n: int = 300
    make_png: bool = True
    output_dir: str = "v723_passive_equivalent_outputs"


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

    return {
        "X": X, "Y": Y, "T": T, "lineage_weak": lineage_weak, "pinch": pinch,
        "M": M, "R": R, "L": L, "C": C, "C_floor": C_floor,
        "Omega_target": Omega_target,
    }


def laplacian(A: np.ndarray) -> np.ndarray:
    return (np.roll(A, 1, axis=0) + np.roll(A, -1, axis=0)
            + np.roll(A, 1, axis=1) + np.roll(A, -1, axis=1) - 4 * A)


def curvature_like(A: np.ndarray) -> np.ndarray:
    """Operational second-variation diagnostic, not a GR curvature tensor."""
    return laplacian(A)


def mean_abs_to_target(A: np.ndarray, target: np.ndarray) -> float:
    return float(np.mean(np.abs(A - target)))


def l2_to_target(A: np.ndarray, target: np.ndarray) -> float:
    return float(np.sqrt(np.mean((A - target) ** 2)))


def safe_auc(y: Iterable[int], score: Iterable[float]) -> float:
    y = np.asarray(list(y))
    score = np.asarray(list(score))
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, score))


def safe_f1(y: Iterable[int], pred: Iterable[int]) -> float:
    y = np.asarray(list(y))
    pred = np.asarray(list(pred))
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(f1_score(y, pred))


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
        X = self.state["X"]
        Y = self.state["Y"]
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
            stripe_coord = np.cos(theta) * (X - cx) + np.sin(theta) * (Y - cy)
            mask = np.exp(-(stripe_coord ** 2) / 0.010)
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

    def make_pair_streams(self, seed: int):
        rng = np.random.default_rng(seed)
        shape = self.target.shape
        initial_noise = rng.normal(0, 0.015, shape)
        field_noises = rng.normal(0, self.cfg.field_noise, (self.cfg.n_steps, *shape))
        perturbations = []
        relax_noises = []
        for i, _t in enumerate(self.cfg.probe_times):
            family = PERTURBATION_FAMILIES[i % len(PERTURBATION_FAMILIES)]
            perturbations.append((family, self.make_perturbation(rng, family)))
            relax_noises.append(rng.normal(0, self.cfg.relax_noise, (self.cfg.relax_steps, *shape)))
        return initial_noise, field_noises, relax_noises, perturbations

    def passive_baseline_states(self, initial_noise: np.ndarray, field_noises: np.ndarray):
        """Generate one passive baseline trajectory independent of k.

        This is the V723 specificity control. Passive burden is a property of the
        shared assay substrate, not of the high-k or low-k branch. k only acts in
        active relaxation windows.
        """
        cfg = self.cfg
        Omega = np.clip(self.target + initial_noise, 0.25, 5.0)
        probe_set = set(cfg.probe_times)
        pre_probe_states = {}
        passive_distances = []
        passive_l2 = []
        curvature_energy = []
        defect_energy = []

        for t in range(cfg.n_steps):
            # Passive retained-atlas evolution. No high/low k branch here.
            dOmega = 0.040 * (self.Source - self.Repair - self.mu_defect)
            dOmega += cfg.diffusion_coupling * laplacian(Omega)
            dOmega += -cfg.passive_background_restore * (Omega - self.target)
            Omega += cfg.evolve_dt * dOmega + field_noises[t]
            Omega = np.clip(Omega, 0.25, 5.0)

            if t in probe_set:
                pre_probe_states[t] = Omega.copy()

            passive_distances.append(mean_abs_to_target(Omega, self.target))
            passive_l2.append(l2_to_target(Omega, self.target))
            curvature_energy.append(float(np.mean(np.abs(curvature_like(Omega)))))
            defect_energy.append(float(np.mean(np.abs(Omega - self.target) * self.mu_defect)))

        meta = {
            "passive_mean_distance": float(np.mean(passive_distances)),
            "passive_peak_distance": float(np.max(passive_distances)),
            "passive_mean_l2_distance": float(np.mean(passive_l2)),
            "passive_peak_l2_distance": float(np.max(passive_l2)),
            "mean_curvature_like_energy": float(np.mean(curvature_energy)),
            "mean_defect_weighted_error": float(np.mean(defect_energy)),
        }
        return pre_probe_states, meta

    def relaxation_assay(
        self,
        k: float,
        pair_id: str,
        run_id: str,
        passive_meta: Dict[str, float],
        pre_probe_states: Dict[int, np.ndarray],
        relax_noises_by_probe: List[np.ndarray],
        perturbations_by_probe: List[Tuple[str, np.ndarray]],
        damping: Optional[float] = None,
    ) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """Branch from identical pre-probe states and measure restoration capacity."""
        cfg = self.cfg
        damping = cfg.damping if damping is None else damping
        probe_log = []
        probe_start_values = []
        probe_post_values = []
        probe_gain_values = []
        probe_l2_post_values = []

        for probe_index, t in enumerate(cfg.probe_times):
            pre = pre_probe_states[t].copy()
            family, mask_signed = perturbations_by_probe[probe_index]
            shocked = np.clip(pre + cfg.perturb_amp * mask_signed, 0.25, 5.0)
            start_dist = mean_abs_to_target(shocked, self.target)
            start_l2 = l2_to_target(shocked, self.target)
            shock_magnitude = float(np.mean(np.abs(cfg.perturb_amp * mask_signed)))

            Omega = shocked.copy()
            for r in range(cfg.relax_steps):
                flow = -(k / damping) * (Omega - self.target)
                smooth = 0.045 * laplacian(Omega)
                Omega += cfg.relax_dt * flow + smooth + relax_noises_by_probe[probe_index][r]
                Omega = np.clip(Omega, 0.25, 5.0)

            post_dist = mean_abs_to_target(Omega, self.target)
            post_l2 = l2_to_target(Omega, self.target)
            gain = start_dist - post_dist

            probe_start_values.append(start_dist)
            probe_post_values.append(post_dist)
            probe_gain_values.append(gain)
            probe_l2_post_values.append(post_l2)

            probe_log.append({
                "pair_id": pair_id,
                "run_id": run_id,
                "probe_time": int(t),
                "probe_index": int(probe_index),
                "perturbation_family": family,
                "k": float(k),
                "damping": float(damping),
                "pre_target_distance": mean_abs_to_target(pre, self.target),
                "start_dist": start_dist,
                "start_l2": start_l2,
                "post_dist": post_dist,
                "post_l2": post_l2,
                "raw_restoration_gain": gain,
                "shock_magnitude": shock_magnitude,
            })

        meta = {
            "pair_id": pair_id,
            "run_id": run_id,
            "k": float(k),
            "damping": float(damping),
            **passive_meta,
            "restoration_measure": float(np.mean(probe_post_values)),
            "restoration_measure_l2": float(np.mean(probe_l2_post_values)),
            "probe_start_mean": float(np.mean(probe_start_values)),
            "probe_post_mean": float(np.mean(probe_post_values)),
            "probe_gain_mean": float(np.mean(probe_gain_values)),
            "probe_gain_std": float(np.std(probe_gain_values, ddof=1)),
            "shock_magnitude_mean": float(np.mean([p["shock_magnitude"] for p in probe_log])),
        }
        return pd.DataFrame(probe_log), meta


def run_pairs(
    engine: RetainedAtlasEngine,
    cfg: HarnessConfig,
    n_pairs: int,
    seed_offset: int,
    split_name: str,
    k_low: Optional[float] = None,
    damping: Optional[float] = None,
    shuffled_null_labels: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    k_low = cfg.low_k if k_low is None else k_low
    damping = cfg.damping if damping is None else damping
    meta_rows = []
    probes = []

    for i in range(n_pairs):
        pair_id = f"{split_name}_pair_{i:04d}"
        streams = engine.make_pair_streams(cfg.seed + seed_offset + i)
        initial_noise, field_noises, relax_noises, perturbations = streams
        pre_states, passive_meta = engine.passive_baseline_states(initial_noise, field_noises)

        for condition, k, admissible_flag, default_failure in [
            ("admissible_high_k", cfg.high_k, True, 0),
            ("low_capacity", k_low, False, int(k_low < cfg.high_k)),
        ]:
            run_id = f"{pair_id}_{condition}"
            probe_df, meta = engine.relaxation_assay(
                k=k,
                pair_id=pair_id,
                run_id=run_id,
                passive_meta=passive_meta,
                pre_probe_states=pre_states,
                relax_noises_by_probe=relax_noises,
                perturbations_by_probe=perturbations,
                damping=damping,
            )
            if shuffled_null_labels:
                failure_label = int(np.random.default_rng(cfg.seed + seed_offset + 900000 + i).integers(0, 2))
            else:
                failure_label = default_failure
            meta.update({
                "split": split_name,
                "condition": condition,
                "admissible_flag": admissible_flag,
                "failure_label": failure_label,
                "physical_failure_condition": int(k < cfg.high_k),
                "shuffled_null_label": bool(shuffled_null_labels),
            })
            meta_rows.append(meta)
            probe_df["split"] = split_name
            probe_df["condition"] = condition
            probe_df["failure_label"] = failure_label
            probes.append(probe_df)

    return pd.DataFrame(meta_rows), pd.concat(probes, ignore_index=True)


def add_calibration_z(run_df: pd.DataFrame, calibration_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    adm = calibration_df[calibration_df["admissible_flag"] == True].copy()
    out = run_df.copy()
    cal = {
        "adm_mean_restoration": float(adm["restoration_measure"].mean()),
        "adm_std_restoration": float(adm["restoration_measure"].std(ddof=1) + 1e-12),
        "n_calibration_admissible": int(len(adm)),
    }
    out["adm_z"] = (out["restoration_measure"] - cal["adm_mean_restoration"]) / cal["adm_std_restoration"]
    out["adm_z_l2"] = (out["restoration_measure_l2"] - float(adm["restoration_measure_l2"].mean())) / (float(adm["restoration_measure_l2"].std(ddof=1)) + 1e-12)

    for src, dst in [
        ("passive_mean_distance", "passive_mean_z"),
        ("passive_peak_distance", "passive_peak_z"),
        ("probe_start_mean", "probe_start_z"),
        ("mean_curvature_like_energy", "curvature_like_z"),
        ("mean_defect_weighted_error", "defect_weighted_z"),
    ]:
        mu = float(adm[src].mean())
        sd = float(adm[src].std(ddof=1) + 1e-12)
        out[dst] = (out[src] - mu) / sd
        cal[f"{src}_mean"] = mu
        cal[f"{src}_std"] = sd
    return out, cal


def evaluate_scores(run_df: pd.DataFrame) -> Dict[str, float]:
    y = run_df["failure_label"].to_numpy()
    out: Dict[str, float] = {
        "n": int(len(run_df)),
        "n_positive": int(y.sum()),
        "n_negative": int((y == 0).sum()),
    }
    for score in ["adm_z", "adm_z_l2", "passive_mean_z", "passive_peak_z", "probe_start_z", "curvature_like_z", "defect_weighted_z"]:
        out[f"auc_{score}"] = safe_auc(y, run_df[score].to_numpy())
    for threshold in [0.75, 1.00, 1.50, 2.00]:
        pred = (run_df["adm_z"].to_numpy() > threshold).astype(int)
        out[f"f1_adm_z_gt_{threshold}"] = safe_f1(y, pred)
        out[f"flag_rate_adm_z_gt_{threshold}"] = float(pred.mean())
    return out


def paired_delta_table(run_df: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "restoration_measure", "adm_z", "adm_z_l2", "passive_mean_distance", "passive_peak_distance",
        "probe_start_mean", "mean_curvature_like_energy", "mean_defect_weighted_error", "probe_gain_mean",
    ]
    rows = []
    for pair_id, g in run_df.groupby("pair_id"):
        if set(g["condition"]) >= {"admissible_high_k", "low_capacity"}:
            high = g[g["condition"] == "admissible_high_k"].iloc[0]
            low = g[g["condition"] == "low_capacity"].iloc[0]
            row = {"pair_id": pair_id, "split": high["split"], "k_gap": float(high["k"] - low["k"])}
            for m in metrics:
                row[f"delta_{m}"] = float(low[m] - high[m])
            rows.append(row)
    return pd.DataFrame(rows)


def passive_equivalence_audit(paired_df: pd.DataFrame) -> Dict[str, float]:
    if paired_df.empty:
        return {}
    out = {}
    for col in ["delta_passive_mean_distance", "delta_passive_peak_distance", "delta_probe_start_mean", "delta_mean_curvature_like_energy", "delta_mean_defect_weighted_error"]:
        vals = paired_df[col].to_numpy()
        out[f"{col}_mean_abs"] = float(np.mean(np.abs(vals)))
        out[f"{col}_max_abs"] = float(np.max(np.abs(vals)))
    return out


def bootstrap_ci(values: np.ndarray, stat_fn, n_boot: int, seed: int) -> Tuple[float, float, float]:
    values = np.asarray(values)
    rng = np.random.default_rng(seed)
    observed = float(stat_fn(values))
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(values), len(values))
        try:
            v = float(stat_fn(values[idx]))
            if np.isfinite(v):
                vals.append(v)
        except Exception:
            pass
    if len(vals) < 10:
        return observed, float("nan"), float("nan")
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return observed, float(lo), float(hi)


def bootstrap_auc_ci(run_df: pd.DataFrame, score_col: str, n_boot: int, seed: int) -> Tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    y = run_df["failure_label"].to_numpy()
    score = run_df[score_col].to_numpy()
    observed = safe_auc(y, score)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(run_df), len(run_df))
        if len(np.unique(y[idx])) < 2:
            continue
        vals.append(safe_auc(y[idx], score[idx]))
    if len(vals) < 10:
        return observed, float("nan"), float("nan")
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return observed, float(lo), float(hi)


def perturbation_family_summary(probe_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (pair_id, family, probe_index), g in probe_df.groupby(["pair_id", "perturbation_family", "probe_index"]):
        if set(g["condition"]) >= {"admissible_high_k", "low_capacity"}:
            high = g[g["condition"] == "admissible_high_k"].iloc[0]
            low = g[g["condition"] == "low_capacity"].iloc[0]
            rows.append({
                "pair_id": pair_id,
                "perturbation_family": family,
                "probe_index": int(probe_index),
                "delta_post_dist_low_minus_high": float(low["post_dist"] - high["post_dist"]),
                "delta_gain_low_minus_high": float(low["raw_restoration_gain"] - high["raw_restoration_gain"]),
                "delta_start_dist_low_minus_high": float(low["start_dist"] - high["start_dist"]),
                "shock_magnitude": float(high["shock_magnitude"]),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.groupby("perturbation_family").agg(
        n=("delta_post_dist_low_minus_high", "size"),
        mean_delta_post_dist=("delta_post_dist_low_minus_high", "mean"),
        median_delta_post_dist=("delta_post_dist_low_minus_high", "median"),
        mean_delta_gain=("delta_gain_low_minus_high", "mean"),
        max_abs_delta_start=("delta_start_dist_low_minus_high", lambda x: float(np.max(np.abs(x)))),
        mean_shock_magnitude=("shock_magnitude", "mean"),
    ).reset_index()


def run_main_audit(engine: RetainedAtlasEngine, cfg: HarnessConfig):
    cal_raw, cal_probe = run_pairs(engine, cfg, cfg.n_calibration_pairs, seed_offset=0, split_name="calibration")
    cal_scored, cal = add_calibration_z(cal_raw, cal_raw)

    test_raw, test_probe = run_pairs(engine, cfg, cfg.n_test_pairs, seed_offset=10000, split_name="test")
    test_scored, _ = add_calibration_z(test_raw, cal_raw)
    paired = paired_delta_table(test_scored)

    eval_full = evaluate_scores(test_scored)
    equiv = passive_equivalence_audit(paired)

    delta_admz_mean, delta_admz_lo, delta_admz_hi = bootstrap_ci(
        paired["delta_adm_z"].to_numpy(), np.mean, cfg.bootstrap_n, cfg.seed + 44
    )
    delta_passive_mean, delta_passive_lo, delta_passive_hi = bootstrap_ci(
        paired["delta_passive_mean_distance"].to_numpy(), np.mean, cfg.bootstrap_n, cfg.seed + 45
    )
    auc_admz, auc_admz_lo, auc_admz_hi = bootstrap_auc_ci(test_scored, "adm_z", cfg.bootstrap_n, cfg.seed + 46)
    auc_passive, auc_passive_lo, auc_passive_hi = bootstrap_auc_ci(test_scored, "passive_mean_z", cfg.bootstrap_n, cfg.seed + 47)

    summary = {
        "version": "V723_PassiveEquivalentRecoverabilityAudit",
        "seed": cfg.seed,
        "high_k": cfg.high_k,
        "low_k": cfg.low_k,
        "k_gap": cfg.high_k - cfg.low_k,
        "damping": cfg.damping,
        "n_calibration_pairs": cfg.n_calibration_pairs,
        "n_test_pairs": cfg.n_test_pairs,
        **cal,
        **{f"full_{k}": v for k, v in eval_full.items()},
        **equiv,
        "paired_delta_adm_z_mean": delta_admz_mean,
        "paired_delta_adm_z_ci95_low": delta_admz_lo,
        "paired_delta_adm_z_ci95_high": delta_admz_hi,
        "paired_delta_passive_mean_distance_mean": delta_passive_mean,
        "paired_delta_passive_mean_distance_ci95_low": delta_passive_lo,
        "paired_delta_passive_mean_distance_ci95_high": delta_passive_hi,
        "auc_adm_z_ci95_low": auc_admz_lo,
        "auc_adm_z_ci95_high": auc_admz_hi,
        "auc_passive_mean_z_ci95_low": auc_passive_lo,
        "auc_passive_mean_z_ci95_high": auc_passive_hi,
        "specificity_gap_auc_adm_minus_passive_mean": float(eval_full["auc_adm_z"] - eval_full["auc_passive_mean_z"]),
    }
    scored = pd.concat([cal_scored, test_scored], ignore_index=True)
    probes = pd.concat([cal_probe, test_probe], ignore_index=True)
    return scored, probes, paired, summary


def k_gap_ablation(engine: RetainedAtlasEngine, cfg: HarnessConfig, n_pairs: int = 24) -> pd.DataFrame:
    rows = []
    cal_raw, _ = run_pairs(engine, cfg, n_pairs, seed_offset=200000, split_name="kgap_calibration")
    for k_low in [0.20, 0.35, 0.50, 0.70, 0.85, 1.00]:
        shuffled = math.isclose(k_low, cfg.high_k)
        raw, _ = run_pairs(
            engine, cfg, n_pairs, seed_offset=int(300000 + 10000 * k_low),
            split_name=f"kgap_{k_low:.2f}", k_low=k_low, shuffled_null_labels=shuffled
        )
        scored, _ = add_calibration_z(raw, cal_raw)
        ev = evaluate_scores(scored)
        paired = paired_delta_table(scored)
        rows.append({
            "k_low": k_low,
            "k_gap": cfg.high_k - k_low,
            "shuffled_label_null": shuffled,
            "auc_adm_z": ev["auc_adm_z"],
            "auc_passive_mean_z": ev["auc_passive_mean_z"],
            "auc_probe_start_z": ev["auc_probe_start_z"],
            "mean_delta_adm_z_low_minus_high": float(paired["delta_adm_z"].mean()),
            "mean_abs_delta_passive_mean": float(np.mean(np.abs(paired["delta_passive_mean_distance"]))),
        })
    return pd.DataFrame(rows)


def damping_window_sweep(engine: RetainedAtlasEngine, cfg: HarnessConfig, n_pairs: int = 20) -> pd.DataFrame:
    rows = []
    cal_raw, _ = run_pairs(engine, cfg, n_pairs, seed_offset=400000, split_name="damping_calibration")
    for damping in [0.50, 0.75, 1.00, 1.50, 2.00, 3.00]:
        raw, _ = run_pairs(
            engine, cfg, n_pairs, seed_offset=int(500000 + 10000 * damping),
            split_name=f"damping_{damping:.2f}", damping=damping
        )
        scored, _ = add_calibration_z(raw, cal_raw)
        ev = evaluate_scores(scored)
        paired = paired_delta_table(scored)
        rows.append({
            "damping": damping,
            "effective_window_relax_steps_over_damping": cfg.relax_steps / damping,
            "auc_adm_z": ev["auc_adm_z"],
            "auc_passive_mean_z": ev["auc_passive_mean_z"],
            "auc_probe_start_z": ev["auc_probe_start_z"],
            "mean_delta_adm_z_low_minus_high": float(paired["delta_adm_z"].mean()),
            "mean_abs_delta_passive_mean": float(np.mean(np.abs(paired["delta_passive_mean_distance"]))),
        })
    return pd.DataFrame(rows)


def make_visuals(out_dir: Path, run_df: pd.DataFrame, paired_df: pd.DataFrame, gap_df: pd.DataFrame, damping_df: pd.DataFrame):
    if not HAVE_MPL:
        return
    test = run_df[run_df["split"] == "test"].copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(test.loc[test["condition"] == "admissible_high_k", "adm_z"], bins=24, alpha=0.65, label="High-k admissible")
    ax.hist(test.loc[test["condition"] == "low_capacity", "adm_z"], bins=24, alpha=0.65, label="Low-k test")
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_title("V723 held-out restoration deficit: passive-equivalent assay")
    ax.set_xlabel("adm_z: post-probe restoration deficit")
    ax.set_ylabel("count")
    ax.legend()
    fig.savefig(out_dir / "adm_z_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(paired_df["delta_adm_z"], bins=24, alpha=0.75, label="Δadm_z")
    ax.hist(paired_df["delta_passive_mean_distance"], bins=24, alpha=0.55, label="Δpassive_mean")
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_title("Paired contrast: restoration changes while passive burden is held equivalent")
    ax.set_xlabel("low-k minus high-k")
    ax.set_ylabel("paired count")
    ax.legend()
    fig.savefig(out_dir / "paired_delta_adm_z_vs_passive.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    if HAVE_SKLEARN:
        fig, ax = plt.subplots(figsize=(8, 7))
        y = test["failure_label"].to_numpy()
        for col, label in [("adm_z", "adm_z"), ("passive_mean_z", "passive mean"), ("probe_start_z", "probe start")]:
            fpr, tpr, _ = roc_curve(y, test[col].to_numpy())
            ax.plot(fpr, tpr, label=f"{label} AUC={safe_auc(y, test[col].to_numpy()):.3f}")
        ax.plot([0, 1], [0, 1], linestyle="--", label="chance")
        ax.set_title("Specificity test: active restoration vs passive burden")
        ax.set_xlabel("False positive rate")
        ax.set_ylabel("True positive rate")
        ax.legend()
        fig.savefig(out_dir / "roc_specificity_comparison.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(gap_df["k_gap"], gap_df["auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(gap_df["k_gap"], gap_df["auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("K-gap ablation under passive equivalence")
    ax.set_xlabel("k_high - k_low")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "k_gap_ablation.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(damping_df["effective_window_relax_steps_over_damping"], damping_df["auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(damping_df["effective_window_relax_steps_over_damping"], damping_df["auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("Observation-window sweep under passive equivalence")
    ax.set_xlabel("effective window ≈ relax_steps / damping")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "damping_window_sweep.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_readme(out_dir: Path, cfg: HarnessConfig, summary: Dict, gap_df: pd.DataFrame, damping_df: pd.DataFrame, family_df: pd.DataFrame):
    md = f"""# V723 Passive-Equivalent Recoverability Audit

## Why V723 exists

V722 confirmed a real counterfactual `k` signal, but the full run was too easy: `adm_z` separated perfectly, and passive burden metrics also separated perfectly. That meant V722 proved that changing restorative capacity changes the whole trajectory, but it did not isolate the restoration-specific law from passive burden.

V723 is the specificity repair.

The scientific goal is now sharper:

> Can active post-perturbation restoration deficit separate recoverability when passive burden is held equivalent?

## Core design

For each pair, V723 creates one shared passive baseline trajectory independent of high/low `k`.

At each probe time, the code branches from the same pre-probe state into two active relaxation assays:

```text
High-k branch: k = {cfg.high_k}
Low-k branch:  k = {cfg.low_k}
```

Both branches receive:

```text
same pre-probe state
same perturbation mask
same perturbation amplitude
same relaxation noise
same relaxation window
same target field
```

Only restorative capacity `k` differs.

This means passive burden metrics are the same within each pair by construction:

```text
passive_mean_distance
passive_peak_distance
probe_start_mean
curvature_like_energy
defect_weighted_error
```

The test is whether post-relaxation restoration distance still differs.

## Core observable

```text
adm_z = (restoration_measure - admissible_calibration_mean) / admissible_calibration_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target field
```

Positive `adm_z` means worse restoration than the admissible high-k calibration baseline.

## Physics / systems interpretation

The synthetic field `Omega(x,t)` is an effective recoverability state over a retained atlas. It is not claimed to be spacetime curvature or a GR tensor.

The passive atlas evolves under source, repair, defect, diffusion, background relaxation, and exogenous noise. This creates a burdened state.

The active probe then asks a different question:

> Given the same burdened state, how much corrective response capacity remains?

That is why V723 separates passive burden from active response-transfer capacity.

## Pass condition

A successful V723 result should show:

```text
passive AUC ≈ 0.50 to 0.65
probe_start AUC ≈ 0.50 to 0.65
adm_z AUC meaningfully higher
paired_delta_adm_z > 0 with CI above zero
k-gap ablation collapses toward null as k_low approaches k_high
passive paired deltas approximately zero
```

## Main summary from this run

```json
{json.dumps(summary, indent=2)}
```

## K-gap ablation

{gap_df.to_markdown(index=False)}

## Damping / observation-window sweep

{damping_df.to_markdown(index=False)}

## Perturbation-family summary

{family_df.to_markdown(index=False) if not family_df.empty else 'No perturbation-family rows generated.'}

## Outputs

```text
{cfg.output_dir}/
  audit_log.csv
  probe_log.csv
  paired_counterfactual_deltas.csv
  summary.json
  summary.csv
  k_gap_ablation.csv
  damping_window_sweep.csv
  perturbation_family_summary.csv
  adm_z_distribution.png
  paired_delta_adm_z_vs_passive.png
  roc_specificity_comparison.png
  k_gap_ablation.png
  damping_window_sweep.png
  V723_PEER_REVIEW_README.md
  config.json
```

## Claim boundary

V723, if positive, supports this narrower and stronger claim:

> In this controlled synthetic retained-atlas assay, active perturbation-response measurement reveals hidden restorative capacity even when passive burden observables are held equivalent.

That is the specificity test V722 did not close.
"""
    (out_dir / "V723_PEER_REVIEW_README.md").write_text(md, encoding="utf-8")


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output_dir", default="v723_passive_equivalent_outputs")
    ap.add_argument("--seed", type=int, default=723)
    ap.add_argument("--n_grid", type=int, default=48)
    ap.add_argument("--n_steps", type=int, default=260)
    ap.add_argument("--n_calibration_pairs", type=int, default=24)
    ap.add_argument("--n_test_pairs", type=int, default=36)
    ap.add_argument("--high_k", type=float, default=1.0)
    ap.add_argument("--low_k", type=float, default=0.35)
    ap.add_argument("--damping", type=float, default=1.0)
    ap.add_argument("--bootstrap_n", type=int, default=300)
    ap.add_argument("--no_png", action="store_true")
    ap.add_argument("--zip", action="store_true")
    args, _unknown = ap.parse_known_args()
    return args


def main():
    if not HAVE_SKLEARN:
        raise RuntimeError("scikit-learn is required for AUC/F1 and ROC diagnostics.")
    args = parse_args()
    cfg = HarnessConfig(
        seed=args.seed,
        n_grid=args.n_grid,
        n_steps=args.n_steps,
        n_calibration_pairs=args.n_calibration_pairs,
        n_test_pairs=args.n_test_pairs,
        high_k=args.high_k,
        low_k=args.low_k,
        damping=args.damping,
        bootstrap_n=args.bootstrap_n,
        make_png=not args.no_png,
        output_dir=args.output_dir,
    )

    # Keep short smoke tests runnable when --n_steps is smaller than the default probe schedule.
    cfg.probe_times = tuple(t for t in cfg.probe_times if t < cfg.n_steps)
    if len(cfg.probe_times) == 0:
        raise ValueError("n_steps must exceed at least one configured probe_time.")

    out_dir = Path(cfg.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[V723] Initializing retained-atlas engine...")
    engine = RetainedAtlasEngine(cfg)

    print("[V723] Running passive-equivalent main audit...")
    run_df, probe_df, paired_df, summary = run_main_audit(engine, cfg)

    print("[V723] Running k-gap ablation...")
    gap_df = k_gap_ablation(engine, cfg, n_pairs=max(8, min(14, cfg.n_test_pairs // 3)))

    print("[V723] Running damping / observation-window sweep...")
    damping_df = damping_window_sweep(engine, cfg, n_pairs=max(8, min(12, cfg.n_test_pairs // 4)))

    family_df = perturbation_family_summary(probe_df[probe_df["split"] == "test"].copy())

    print("[V723] Writing outputs...")
    run_df.to_csv(out_dir / "audit_log.csv", index=False)
    probe_df.to_csv(out_dir / "probe_log.csv", index=False)
    paired_df.to_csv(out_dir / "paired_counterfactual_deltas.csv", index=False)
    pd.DataFrame([summary]).to_csv(out_dir / "summary.csv", index=False)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    gap_df.to_csv(out_dir / "k_gap_ablation.csv", index=False)
    damping_df.to_csv(out_dir / "damping_window_sweep.csv", index=False)
    family_df.to_csv(out_dir / "perturbation_family_summary.csv", index=False)
    config_json = asdict(cfg)
    config_json["probe_times"] = list(cfg.probe_times)
    (out_dir / "config.json").write_text(json.dumps(config_json, indent=2), encoding="utf-8")

    write_readme(out_dir, cfg, summary, gap_df, damping_df, family_df)

    if cfg.make_png:
        print("[V723] Generating visual diagnostics...")
        make_visuals(out_dir, run_df, paired_df, gap_df, damping_df)

    if args.zip:
        zip_path = out_dir.with_suffix(".zip")
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in out_dir.iterdir():
                z.write(p, arcname=p.name)
            z.write(Path(__file__), arcname=Path(__file__).name)
        print("[V723] Created zip:", zip_path)

    print("\n=== V723 SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nOutputs written to:", out_dir)


if __name__ == "__main__":
    main()
