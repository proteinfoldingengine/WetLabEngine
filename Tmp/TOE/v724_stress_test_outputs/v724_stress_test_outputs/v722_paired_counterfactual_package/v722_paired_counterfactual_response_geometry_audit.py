#!/usr/bin/env python3
# ==============================================================================
# V722 PAIRED COUNTERFACTUAL RESPONSE-GEOMETRY AUDIT
# Retained Atlas / Recoverability Law-Discovery Harness
#
# Peer-review posture:
# This is an exploratory first-principles synthetic systems harness. It tests an
# observed recoverability regularity under stricter causal controls. It is not a
# proof of GR, quantum collapse, or a universal physical law.
#
# Core improvement over V721:
#   Same world. Same target. Same initial condition. Same passive noise.
#   Same probe masks. Same perturbation amplitude. Same relaxation noise.
#   Only restorative capacity k changes.
#
# Frozen operational observable:
#   adm_z = (post-perturbation restoration distance - admissible calibration mean)
#           / admissible calibration std
#
# Primary scientific question:
#   Does active restoration deficit reveal recoverability better than passive
#   burden alone when all non-k sources of variation are paired?
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
    from sklearn.metrics import roc_auc_score, f1_score
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import StandardScaler
    HAVE_SKLEARN = True
except Exception:
    HAVE_SKLEARN = False


@dataclass
class HarnessConfig:
    seed: int = 722
    n_grid: int = 64
    n_steps: int = 260
    probe_times: Tuple[int, ...] = (75, 110, 145, 180, 215)
    relax_steps: int = 18
    high_k: float = 1.0
    low_k: float = 0.35
    n_calibration_pairs: int = 36
    n_test_pairs: int = 48
    perturb_amp: float = 1.20
    field_noise: float = 0.007
    relax_noise: float = 0.0055
    evolve_dt: float = 0.055
    relax_dt: float = 0.085
    diffusion_coupling: float = 0.035
    target_restore_background: float = 0.035
    damping: float = 1.0
    bootstrap_n: int = 500
    make_png: bool = True
    output_dir: str = "v722_paired_counterfactual_outputs"


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

    def simulate_with_streams(
        self,
        k: float,
        run_id: str,
        pair_id: str,
        initial_noise: np.ndarray,
        field_noises: np.ndarray,
        relax_noises_by_probe: List[np.ndarray],
        perturbations_by_probe: List[Tuple[str, np.ndarray]],
        damping: Optional[float] = None,
        return_traj: bool = False,
    ):
        cfg = self.cfg
        damping = cfg.damping if damping is None else damping
        Omega = np.clip(self.target + initial_noise, 0.25, 5.0)
        traj = [Omega.copy()] if return_traj else None
        probe_log = []
        passive_distances = []
        curvature_energy = []
        defect_energy = []
        probe_index = 0
        probe_set = set(cfg.probe_times)

        for t in range(cfg.n_steps):
            dOmega = 0.040 * (self.Source - self.Repair - self.mu_defect)
            dOmega += cfg.diffusion_coupling * laplacian(Omega)
            dOmega += -cfg.target_restore_background * (k / damping) * (Omega - self.target)
            Omega += cfg.evolve_dt * dOmega + field_noises[t]
            Omega = np.clip(Omega, 0.25, 5.0)

            if t in probe_set:
                pre = Omega.copy()
                family, mask_signed = perturbations_by_probe[probe_index]
                Omega = np.clip(Omega + cfg.perturb_amp * mask_signed, 0.25, 5.0)
                start_dist = mean_abs_to_target(Omega, self.target)
                shock_magnitude = float(np.mean(np.abs(cfg.perturb_amp * mask_signed)))

                for r in range(cfg.relax_steps):
                    flow = -(k / damping) * (Omega - self.target)
                    smooth = 0.045 * laplacian(Omega)
                    Omega += cfg.relax_dt * flow + smooth + relax_noises_by_probe[probe_index][r]
                    Omega = np.clip(Omega, 0.25, 5.0)

                post_dist = mean_abs_to_target(Omega, self.target)
                probe_log.append({
                    "pair_id": pair_id,
                    "run_id": run_id,
                    "probe_time": int(t),
                    "probe_index": int(probe_index),
                    "perturbation_family": family,
                    "k": float(k),
                    "damping": float(damping),
                    "start_dist": start_dist,
                    "post_dist": post_dist,
                    "raw_restoration_gain": start_dist - post_dist,
                    "shock_magnitude": shock_magnitude,
                    "pre_target_distance": mean_abs_to_target(pre, self.target),
                })
                probe_index += 1

            passive_distances.append(mean_abs_to_target(Omega, self.target))
            curvature_energy.append(float(np.mean(np.abs(curvature_like(Omega)))))
            defect_energy.append(float(np.mean(np.abs(Omega - self.target) * self.mu_defect)))
            if return_traj:
                traj.append(Omega.copy())

        meta = {
            "pair_id": pair_id,
            "run_id": run_id,
            "k": float(k),
            "damping": float(damping),
            "passive_mean_distance": float(np.mean(passive_distances)),
            "passive_peak_distance": float(np.max(passive_distances)),
            "mean_curvature_like_energy": float(np.mean(curvature_energy)),
            "mean_defect_weighted_error": float(np.mean(defect_energy)),
        }
        return (np.asarray(traj) if return_traj else None), pd.DataFrame(probe_log), meta


def make_counterfactual_streams(engine: RetainedAtlasEngine, cfg: HarnessConfig, seed: int):
    rng = np.random.default_rng(seed)
    shape = engine.target.shape
    initial_noise = rng.normal(0, 0.015, shape)
    field_noises = rng.normal(0, cfg.field_noise, (cfg.n_steps, *shape))
    perturbations = []
    relax_noises = []
    for i, _t in enumerate(cfg.probe_times):
        family = PERTURBATION_FAMILIES[i % len(PERTURBATION_FAMILIES)]
        perturbations.append((family, engine.make_perturbation(rng, family)))
        relax_noises.append(rng.normal(0, cfg.relax_noise, (cfg.relax_steps, *shape)))
    return initial_noise, field_noises, relax_noises, perturbations


def compute_run_level(probe_df: pd.DataFrame, meta_rows: List[Dict]) -> pd.DataFrame:
    probe_agg = probe_df.groupby(["pair_id", "run_id"]).agg(
        restoration_measure=("post_dist", "mean"),
        probe_start_mean=("start_dist", "mean"),
        probe_post_mean=("post_dist", "mean"),
        probe_gain_mean=("raw_restoration_gain", "mean"),
        probe_gain_std=("raw_restoration_gain", "std"),
        shock_magnitude_mean=("shock_magnitude", "mean"),
    ).reset_index()
    return pd.DataFrame(meta_rows).merge(probe_agg, on=["pair_id", "run_id"], how="left")


def add_calibration_z(run_df: pd.DataFrame, calibration_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    adm = calibration_df[calibration_df["admissible_flag"] == True].copy()
    out = run_df.copy()
    cal = {
        "adm_mean_restoration": float(adm["restoration_measure"].mean()),
        "adm_std_restoration": float(adm["restoration_measure"].std(ddof=1) + 1e-12),
        "n_calibration_admissible": int(len(adm)),
    }
    out["adm_z"] = (out["restoration_measure"] - cal["adm_mean_restoration"]) / cal["adm_std_restoration"]

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
    all_probes = []
    meta_rows = []

    for i in range(n_pairs):
        pair_id = f"{split_name}_pair_{i:04d}"
        streams = make_counterfactual_streams(engine, cfg, cfg.seed + seed_offset + i)
        for condition, k, admissible_flag, default_failure in [
            ("admissible_high_k", cfg.high_k, True, 0),
            ("low_capacity", k_low, False, int(k_low < cfg.high_k)),
        ]:
            run_id = f"{pair_id}_{condition}"
            _, probes, meta = engine.simulate_with_streams(
                k=k,
                run_id=run_id,
                pair_id=pair_id,
                initial_noise=streams[0],
                field_noises=streams[1],
                relax_noises_by_probe=streams[2],
                perturbations_by_probe=streams[3],
                damping=damping,
                return_traj=False,
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
            all_probes.append(probes)
            meta_rows.append(meta)

    probe_df = pd.concat(all_probes, ignore_index=True)
    run_df = compute_run_level(probe_df, meta_rows)
    return run_df, probe_df


def paired_delta_table(run_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = [
        "restoration_measure", "adm_z", "passive_mean_distance", "passive_peak_distance",
        "probe_start_mean", "mean_curvature_like_energy", "mean_defect_weighted_error",
    ]
    for pair_id, g in run_df.groupby("pair_id"):
        if set(g["condition"]) >= {"admissible_high_k", "low_capacity"}:
            high = g[g["condition"] == "admissible_high_k"].iloc[0]
            low = g[g["condition"] == "low_capacity"].iloc[0]
            row = {"pair_id": pair_id, "split": high["split"], "k_gap": float(high["k"] - low["k"])}
            for m in metrics:
                row[f"delta_{m}"] = float(low[m] - high[m])
            rows.append(row)
    return pd.DataFrame(rows)


def passive_matched_subset(run_df: pd.DataFrame, q: float = 0.35) -> pd.DataFrame:
    if not HAVE_SKLEARN:
        return run_df.copy()
    adm = run_df[run_df["failure_label"] == 0].copy().reset_index(drop=True)
    low = run_df[run_df["failure_label"] == 1].copy().reset_index(drop=True)
    if len(adm) == 0 or len(low) == 0:
        return run_df.copy()
    feats = ["passive_mean_distance", "probe_start_mean"]
    scaler = StandardScaler()
    A = scaler.fit_transform(adm[feats])
    L = scaler.transform(low[feats])
    nn = NearestNeighbors(n_neighbors=1).fit(A)
    dist, idx = nn.kneighbors(L)
    dist = dist[:, 0]
    idx = idx[:, 0]
    keep = dist <= np.quantile(dist, q)
    matched = pd.concat([adm.iloc[idx[keep]].copy(), low.loc[keep].copy()], ignore_index=True)
    matched["match_distance"] = np.r_[dist[keep], dist[keep]]
    return matched


def evaluate_scores(run_df: pd.DataFrame) -> Dict[str, float]:
    y = run_df["failure_label"].to_numpy()
    out: Dict[str, float] = {
        "n": int(len(run_df)),
        "n_positive": int(y.sum()),
        "n_negative": int((y == 0).sum()),
    }
    for score in ["adm_z", "passive_mean_z", "passive_peak_z", "probe_start_z", "curvature_like_z", "defect_weighted_z"]:
        out[f"auc_{score}"] = safe_auc(y, run_df[score].to_numpy())
    for threshold in [0.75, 1.00, 1.50, 2.00]:
        pred = (run_df["adm_z"].to_numpy() > threshold).astype(int)
        out[f"f1_adm_z_gt_{threshold}"] = safe_f1(y, pred)
        out[f"flag_rate_adm_z_gt_{threshold}"] = float(pred.mean())
    return out


def bootstrap_ci(values: np.ndarray, stat_fn, n_boot: int, seed: int) -> Tuple[float, float, float]:
    values = np.asarray(values)
    rng = np.random.default_rng(seed)
    observed = float(stat_fn(values))
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(values), len(values))
        try:
            val = float(stat_fn(values[idx]))
            if np.isfinite(val):
                boots.append(val)
        except Exception:
            pass
    if len(boots) < 10:
        return observed, float("nan"), float("nan")
    lo, hi = np.quantile(boots, [0.025, 0.975])
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


def run_main_audit(engine: RetainedAtlasEngine, cfg: HarnessConfig):
    cal_raw, cal_probe = run_pairs(engine, cfg, cfg.n_calibration_pairs, seed_offset=0, split_name="calibration")
    # Calibration rows are z-scored against high-k calibration rows only.
    cal_scored, cal = add_calibration_z(cal_raw, cal_raw)

    test_raw, test_probe = run_pairs(engine, cfg, cfg.n_test_pairs, seed_offset=10000, split_name="test")
    test_scored, _ = add_calibration_z(test_raw, cal_raw)
    matched = passive_matched_subset(test_scored, q=0.35)
    paired = paired_delta_table(test_scored)

    eval_full = evaluate_scores(test_scored)
    eval_matched = evaluate_scores(matched)

    paired_admz = paired["delta_adm_z"].to_numpy()
    delta_admz_mean, delta_admz_lo, delta_admz_hi = bootstrap_ci(
        paired_admz, np.mean, cfg.bootstrap_n, cfg.seed + 44
    )
    auc_admz, auc_admz_lo, auc_admz_hi = bootstrap_auc_ci(test_scored, "adm_z", cfg.bootstrap_n, cfg.seed + 45)
    auc_passive, auc_passive_lo, auc_passive_hi = bootstrap_auc_ci(test_scored, "passive_mean_z", cfg.bootstrap_n, cfg.seed + 46)

    summary = {
        "version": "V722_PairedCounterfactualResponseGeometryAudit",
        "seed": cfg.seed,
        "high_k": cfg.high_k,
        "low_k": cfg.low_k,
        "k_gap": cfg.high_k - cfg.low_k,
        "damping": cfg.damping,
        "n_calibration_pairs": cfg.n_calibration_pairs,
        "n_test_pairs": cfg.n_test_pairs,
        **cal,
        **{f"full_{k}": v for k, v in eval_full.items()},
        **{f"matched_{k}": v for k, v in eval_matched.items()},
        "paired_delta_adm_z_mean": delta_admz_mean,
        "paired_delta_adm_z_ci95_low": delta_admz_lo,
        "paired_delta_adm_z_ci95_high": delta_admz_hi,
        "auc_adm_z_ci95_low": auc_admz_lo,
        "auc_adm_z_ci95_high": auc_admz_hi,
        "auc_passive_mean_z_ci95_low": auc_passive_lo,
        "auc_passive_mean_z_ci95_high": auc_passive_hi,
    }
    probes = pd.concat([cal_probe, test_probe], ignore_index=True)
    scored = pd.concat([cal_scored, test_scored], ignore_index=True)
    return scored, probes, matched, paired, summary


def k_gap_ablation(engine: RetainedAtlasEngine, cfg: HarnessConfig, n_pairs: int = 24) -> pd.DataFrame:
    rows = []
    # Use one calibration set for this ablation family.
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
            "f1_adm_z_gt_0.75": ev["f1_adm_z_gt_0.75"],
            "mean_delta_adm_z_low_minus_high": float(paired["delta_adm_z"].mean()),
            "mean_delta_restoration_low_minus_high": float(paired["delta_restoration_measure"].mean()),
        })
    return pd.DataFrame(rows)


def damping_window_sweep(engine: RetainedAtlasEngine, cfg: HarnessConfig, n_pairs: int = 18) -> pd.DataFrame:
    rows = []
    cal_raw, _ = run_pairs(engine, cfg, n_pairs, seed_offset=400000, split_name="damping_calibration")
    for damping in [0.50, 0.75, 1.00, 1.50, 2.00, 3.00]:
        raw, _ = run_pairs(
            engine, cfg, n_pairs, seed_offset=int(500000 + 10000 * damping),
            split_name=f"damping_{damping:.2f}", damping=damping
        )
        scored, _ = add_calibration_z(raw, cal_raw)
        matched = passive_matched_subset(scored, q=0.35)
        ev = evaluate_scores(scored)
        mev = evaluate_scores(matched)
        paired = paired_delta_table(scored)
        rows.append({
            "damping": damping,
            "effective_window_relax_steps_over_damping": cfg.relax_steps / damping,
            "full_auc_adm_z": ev["auc_adm_z"],
            "full_auc_passive_mean_z": ev["auc_passive_mean_z"],
            "matched_auc_adm_z": mev["auc_adm_z"],
            "matched_auc_passive_mean_z": mev["auc_passive_mean_z"],
            "matched_n": mev["n"],
            "mean_delta_adm_z_low_minus_high": float(paired["delta_adm_z"].mean()),
        })
    return pd.DataFrame(rows)


def perturbation_family_summary(probe_df: pd.DataFrame) -> pd.DataFrame:
    # Probe-level paired deltas by family.
    rows = []
    for (pair_id, family, probe_index), g in probe_df.groupby(["pair_id", "perturbation_family", "probe_index"]):
        if set(g["k"].round(8)):
            high = g.loc[g["k"] == g["k"].max()].iloc[0]
            low = g.loc[g["k"] == g["k"].min()].iloc[0]
            rows.append({
                "pair_id": pair_id,
                "perturbation_family": family,
                "probe_index": probe_index,
                "delta_post_dist_low_minus_high": float(low["post_dist"] - high["post_dist"]),
                "delta_gain_low_minus_high": float(low["raw_restoration_gain"] - high["raw_restoration_gain"]),
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
        mean_shock_magnitude=("shock_magnitude", "mean"),
    ).reset_index()


def make_visuals(out_dir: Path, run_df: pd.DataFrame, paired_df: pd.DataFrame, gap_df: pd.DataFrame, damping_df: pd.DataFrame):
    if not HAVE_MPL:
        return
    # Main distributions.
    fig, ax = plt.subplots(figsize=(10, 6))
    test = run_df[run_df["split"] == "test"].copy()
    ax.hist(test.loc[test["condition"] == "admissible_high_k", "adm_z"], bins=20, alpha=0.65, label="High-k admissible")
    ax.hist(test.loc[test["condition"] == "low_capacity", "adm_z"], bins=20, alpha=0.65, label="Low-k capacity")
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_title("Held-out adm_z distribution: paired counterfactual audit")
    ax.set_xlabel("adm_z: restoration deficit vs admissible calibration")
    ax.set_ylabel("count")
    ax.legend()
    fig.savefig(out_dir / "adm_z_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(paired_df["delta_adm_z"], bins=22, alpha=0.8)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_title("Paired causal contrast: low-k adm_z minus high-k adm_z")
    ax.set_xlabel("Δadm_z")
    ax.set_ylabel("paired run count")
    fig.savefig(out_dir / "paired_delta_adm_z.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(gap_df["k_gap"], gap_df["auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(gap_df["k_gap"], gap_df["auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("K-gap ablation: signal should degrade toward null as gap closes")
    ax.set_xlabel("k_high - k_low")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "k_gap_ablation.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(damping_df["effective_window_relax_steps_over_damping"], damping_df["full_auc_adm_z"], marker="o", label="adm_z AUC")
    ax.plot(damping_df["effective_window_relax_steps_over_damping"], damping_df["full_auc_passive_mean_z"], marker="o", label="passive mean AUC")
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("Observation-window sweep")
    ax.set_xlabel("effective window ≈ relax_steps / damping")
    ax.set_ylabel("AUC")
    ax.legend()
    fig.savefig(out_dir / "damping_window_sweep.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_readme(out_dir: Path, cfg: HarnessConfig, summary: Dict, gap_df: pd.DataFrame, damping_df: pd.DataFrame, family_df: pd.DataFrame):
    md = f"""# V722 Paired Counterfactual Response-Geometry Audit

## Purpose

This package is a stricter follow-up to the V713/V721 recoverability audit stack.

The scientific objective is to test whether an active post-perturbation restoration deficit exposes recoverability better than passive burden alone.

The core peer-review improvement is a paired counterfactual design:

```text
Same world.
Same target field.
Same initial condition.
Same passive noise stream.
Same probe masks.
Same perturbation amplitude.
Same relaxation noise.
Only restorative capacity k changes.
```

This makes the causal contrast much cleaner than an unpaired high-k vs low-k comparison.

## Current law-discovery posture

The harness treats the earlier stack as an iterative observation program:

- V395 observed a control skeleton: reserve/reachability product, dynamic floor, and hierarchy.
- V541 expressed the same observed recoverability behavior in field-geometric form.
- V713 froze the measurable restoration-deficit observable.
- V721 introduced active perturbation-response testing and damping/window controls.
- V722 adds paired counterfactual rigor.

This is not a claim that a final universal physical law is proven. It is a controlled synthetic test of a novel candidate operational law of recoverability.

## Core observable

```text
adm_z = (restoration_measure - admissible_calibration_mean) / admissible_calibration_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target field
```

Positive `adm_z` means worse restoration than the admissible baseline.

Calibration is performed using high-k admissible calibration runs only. Held-out test runs are then scored against that frozen calibration.

## Physics / systems interpretation

The synthetic field `Omega(x,t)` represents an effective recoverability state over a retained atlas.

The target field `Omega_target` is constructed from three internal reserve factors:

```text
M = adaptive margin
R = retained future capacity / memory
L = lineage continuity
C = M * R * L
C_floor = local survivability floor
Omega_target = clipped function of C - C_floor
```

The field evolves under:

```text
dOmega/dt = Source - Repair - Defect + diffusion - background restoration
```

with active probes inserted at fixed times. After each probe, the system is allowed a finite relaxation window. The audit asks whether lower restorative capacity `k` leaves a measurable residual restoration deficit even when passive burden is controlled.

The curvature-like term in the code is only a second-variation diagnostic. It is not a GR curvature tensor.

## What V722 fixes

### 1. Paired counterfactuals

For every pair, the high-k and low-k runs share the exact same generated world and disturbance streams.

### 2. Held-out calibration

Admissible calibration runs define the `adm_z` baseline. Separate held-out test pairs are then evaluated.

### 3. Perturbation-family invariance

The audit cycles through five probe families:

- Gaussian bump
- ring perturbation
- stripe perturbation
- multi-site perturbation
- sinusoidal field perturbation

### 4. Null / k-gap ablation

The code sweeps `k_low` toward `k_high`. When `k_low = k_high`, labels are explicitly randomized as a shuffled-label null. A valid signal should degrade toward chance as the gap closes.

### 5. Damping / observation-window sweep

The code sweeps damping and reports an effective observation window:

```text
effective_window ≈ relax_steps / damping
```

This tests whether recoverability observability has a finite-window boundary.

### 6. Bootstrap uncertainty

The main summary includes bootstrap confidence intervals for:

- AUC of `adm_z`
- AUC of passive mean burden
- paired delta `adm_z`

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

## Expected peer-review reading

A strong result has this pattern:

```text
1. Held-out adm_z separates low-k from high-k better than passive burden.
2. Paired delta adm_z is positive with confidence interval above zero.
3. The signal degrades as k_gap approaches zero.
4. The shuffled-label null approaches chance.
5. The signal persists across perturbation families.
6. Damping exposes an observation-window boundary rather than arbitrary failure.
```

A weak result has this pattern:

```text
1. Passive burden metrics match or beat adm_z.
2. Paired delta adm_z overlaps zero.
3. k_gap ablation does not degrade toward null.
4. Perturbation-family results are inconsistent.
5. Damping effects are erratic rather than window-like.
```

## How to run in Colab

Upload `v722_paired_counterfactual_response_geometry_audit.py` and run:

```bash
python v722_paired_counterfactual_response_geometry_audit.py
```

Optional:

```bash
python v722_paired_counterfactual_response_geometry_audit.py --n_test_pairs 80 --bootstrap_n 1000 --zip
```

## Outputs

```text
v722_paired_counterfactual_outputs/
  audit_log.csv
  probe_log.csv
  matched_passive_control_log.csv
  paired_counterfactual_deltas.csv
  summary.json
  summary.csv
  k_gap_ablation.csv
  damping_window_sweep.csv
  perturbation_family_summary.csv
  adm_z_distribution.png
  paired_delta_adm_z.png
  k_gap_ablation.png
  damping_window_sweep.png
  V722_PEER_REVIEW_README.md
  config.json
```

## Claim boundary

The result, if positive, supports this narrower claim:

> In this controlled synthetic retained-atlas system, active post-perturbation restoration deficit is a stronger recoverability observable than passive burden alone, and the signal survives paired counterfactual controls.

It does not by itself prove a universal physical law. It does strengthen the candidate operational law by removing major confounds.
"""
    (out_dir / "V722_PEER_REVIEW_README.md").write_text(md, encoding="utf-8")


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output_dir", default="v722_paired_counterfactual_outputs")
    ap.add_argument("--seed", type=int, default=722)
    ap.add_argument("--n_grid", type=int, default=64)
    ap.add_argument("--n_steps", type=int, default=260)
    ap.add_argument("--n_calibration_pairs", type=int, default=36)
    ap.add_argument("--n_test_pairs", type=int, default=48)
    ap.add_argument("--high_k", type=float, default=1.0)
    ap.add_argument("--low_k", type=float, default=0.35)
    ap.add_argument("--damping", type=float, default=1.0)
    ap.add_argument("--bootstrap_n", type=int, default=500)
    ap.add_argument("--no_png", action="store_true")
    ap.add_argument("--zip", action="store_true")
    args, _unknown = ap.parse_known_args()
    return args


def main():
    if not HAVE_SKLEARN:
        raise RuntimeError("scikit-learn is required for AUC/F1 and matched controls.")
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
    out_dir = Path(cfg.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[V722] Initializing retained-atlas engine...")
    engine = RetainedAtlasEngine(cfg)

    print("[V722] Running paired counterfactual main audit...")
    run_df, probe_df, matched_df, paired_df, summary = run_main_audit(engine, cfg)

    print("[V722] Running k-gap ablation...")
    gap_df = k_gap_ablation(engine, cfg, n_pairs=max(12, min(24, cfg.n_test_pairs // 2)))

    print("[V722] Running damping / observation-window sweep...")
    damping_df = damping_window_sweep(engine, cfg, n_pairs=max(10, min(18, cfg.n_test_pairs // 3)))

    family_df = perturbation_family_summary(probe_df[probe_df["run_id"].str.contains("test_pair", na=False)].copy())

    print("[V722] Writing outputs...")
    run_df.to_csv(out_dir / "audit_log.csv", index=False)
    probe_df.to_csv(out_dir / "probe_log.csv", index=False)
    matched_df.to_csv(out_dir / "matched_passive_control_log.csv", index=False)
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
        print("[V722] Generating visual diagnostics...")
        make_visuals(out_dir, run_df, paired_df, gap_df, damping_df)

    if args.zip:
        zip_path = out_dir.with_suffix(".zip")
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in out_dir.iterdir():
                z.write(p, arcname=p.name)
            z.write(Path(__file__), arcname=Path(__file__).name)
        print("[V722] Created zip:", zip_path)

    print("\n=== V722 SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nOutputs written to:", out_dir)


if __name__ == "__main__":
    main()
