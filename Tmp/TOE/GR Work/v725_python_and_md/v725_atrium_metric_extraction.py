#!/usr/bin/env python3
# ==============================================================================
# V725 ATRIUM METRIC EXTRACTION
# Retained-Atlas Response Geometry
#
# Purpose:
#   Extract a first operational Atrium Metric scalar from passive-equivalent
#   perturbation-response assays.
#
# Scientific posture:
#   This is not a GR metric tensor.
#   This is an operational response-geometry scalar derived from:
#       - admissible-normalized restoration deficit (adm_z)
#       - local contraction
#       - curvature-like relief
#       - metric strain / response path inefficiency
#
# Core question:
#   When passive burden is held equivalent, does a response-geometry metric
#   still track hidden restorative capacity k?
#
# Output:
#   v725_run_level_atrium_metric.csv
#   v725_paired_metric_deltas.csv
#   v725_k_gap_ablation.csv
#   v725_summary.json
#   V725_ATRIUM_METRIC_EXTRACTION.md
#   atrium_metric_distribution.png
#   v725_k_gap_ablation.png
# ==============================================================================

from pathlib import Path
import json
import zipfile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score


# ==============================================================================
# CONFIG
# ==============================================================================

OUT = Path("v725_atrium_metric_extraction_outputs")
OUT.mkdir(exist_ok=True)

SEED = 725
rng = np.random.default_rng(SEED)

N = 32
T = 90
PROBE_TIMES = np.array([28, 45, 62, 78])
RELAX_STEPS = 10

PERTURB_AMP = 1.1
HIGH_K = 1.0
LOW_K = 0.35

SHOCK_KINDS = ["gaussian", "ring", "stripe", "multi"]


# ==============================================================================
# FIELD SETUP
# ==============================================================================

x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)

burden = (
    np.exp(-((X - 0.35) ** 2 + (Y - 0.42) ** 2) / 0.07)
    + 0.8 * np.exp(-((X - 0.72) ** 2 + (Y - 0.62) ** 2) / 0.08)
)

pinch = np.exp(-((X - 0.58) ** 2 + (Y - 0.50) ** 2) / 0.035)

M = np.clip(0.65 - 0.28 * burden, 0.15, 1.2)
R = np.clip(0.65 - 0.25 * pinch, 0.12, 1.2)
L = np.clip(0.58 - 0.16 * burden - 0.20 * pinch, 0.12, 1.2)

C = M * R * L
C_floor = np.clip(0.15 + 0.25 * burden + 0.18 * pinch, 0.08, 0.85)

target = np.clip(1.0 + 0.75 * (C - C_floor), 0.25, 4.5)

Source = burden / (np.maximum(C - C_floor, 0.02) + 1e-8)
Repair = 0.30 * M + 0.30 * R + 0.25 * L
Defect = 0.45 * burden * (1 - L)


# ==============================================================================
# OPERATORS
# ==============================================================================

def lap(A: np.ndarray) -> np.ndarray:
    return (
        np.roll(A, 1, 0)
        + np.roll(A, -1, 0)
        + np.roll(A, 1, 1)
        + np.roll(A, -1, 1)
        - 4 * A
    )


def curvature_energy(A: np.ndarray) -> float:
    """
    Curvature-like second-variation diagnostic.
    Not a GR curvature tensor.
    """
    return float(np.mean(np.abs(lap(A))))


def dist_to_target(A: np.ndarray) -> float:
    return float(np.mean(np.abs(A - target)))


def shock(local_rng: np.random.Generator, kind: str) -> np.ndarray:
    """
    Perturbation masks. Same mask and noise stream are used for high-k and low-k
    branches within each paired counterfactual.
    """
    if kind == "gaussian":
        cx = 0.5 + 0.18 * local_rng.normal()
        cy = 0.5 + 0.18 * local_rng.normal()
        m = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.035)

    elif kind == "ring":
        r = np.sqrt((X - 0.5) ** 2 + (Y - 0.5) ** 2)
        m = np.exp(-((r - 0.18) ** 2) / 0.004)

    elif kind == "stripe":
        m = np.exp(-((X - (0.5 + 0.1 * local_rng.normal())) ** 2) / 0.008)

    elif kind == "multi":
        m = np.zeros_like(X)
        for _ in range(2):
            cx = local_rng.uniform(0.25, 0.75)
            cy = local_rng.uniform(0.25, 0.75)
            m += np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.018)
        m /= max(m.max(), 1e-12)

    else:
        raise ValueError(kind)

    return local_rng.choice([-1, 1]) * m


# ==============================================================================
# PAIRED COUNTERFACTUAL ASSAY
# ==============================================================================

def paired_assay(pair_id: int, k_low: float = LOW_K, kind: str = "gaussian", seed: int = 0):
    """
    Passive-equivalent paired counterfactual.

    A shared passive baseline is evolved independent of k.
    At each probe time, high-k and low-k branches start from the same pre-probe
    state and receive:
        same perturbation mask
        same perturbation amplitude
        same relaxation noise
        same target field
        same relaxation window

    Only k differs.
    """
    local_rng = np.random.default_rng(seed)

    O = target + local_rng.normal(0, 0.015, target.shape)

    high_rows = []
    low_rows = []
    passive_dists = []

    for t in range(T):
        # Shared passive baseline evolution, independent of high/low k labels.
        dO = 0.035 * (Source - Repair - Defect) + 0.035 * lap(O)
        O = np.clip(O + 0.05 * dO + local_rng.normal(0, 0.006, O.shape), 0.25, 5.0)
        passive_dists.append(dist_to_target(O))

        if t in PROBE_TIMES:
            pre = O.copy()
            sh = PERTURB_AMP * shock(local_rng, kind)
            noises = [local_rng.normal(0, 0.005, target.shape) for _ in range(RELAX_STEPS)]

            for k, store in [(HIGH_K, high_rows), (k_low, low_rows)]:
                B = np.clip(pre + sh, 0.25, 5.0)

                start_dist = dist_to_target(B)
                start_curv = curvature_energy(B)

                d_list = [start_dist]
                c_list = [start_curv]

                for n in noises:
                    B = np.clip(B + 0.085 * (-k * (B - target)) + 0.042 * lap(B) + n, 0.25, 5.0)
                    d_list.append(dist_to_target(B))
                    c_list.append(curvature_energy(B))

                post_dist = d_list[-1]

                contraction = (start_dist - post_dist) / (start_dist + 1e-12)
                path_len = float(np.sum(np.abs(np.diff(d_list))))
                curv_relief = (c_list[0] - c_list[-1]) / (c_list[0] + 1e-12)
                metric_strain = path_len / (abs(start_dist - post_dist) + 1e-9)

                store.append(
                    {
                        "pair_id": pair_id,
                        "k": k,
                        "kind": kind,
                        "start_dist": start_dist,
                        "post_dist": post_dist,
                        "contraction": contraction,
                        "path_len": path_len,
                        "curv_relief": curv_relief,
                        "metric_strain": metric_strain,
                        "passive_mean": float(np.mean(passive_dists)),
                        "passive_curv": curvature_energy(pre),
                    }
                )

    return pd.DataFrame(high_rows), pd.DataFrame(low_rows)


def summarize_branch(df: pd.DataFrame, label: str, kind: str, adm_mean: float, adm_std: float) -> pd.DataFrame:
    g = (
        df.groupby("pair_id")
        .agg(
            restoration_measure=("post_dist", "mean"),
            contraction=("contraction", "mean"),
            curv_relief=("curv_relief", "mean"),
            metric_strain=("metric_strain", "mean"),
            passive_mean=("passive_mean", "mean"),
            passive_curv=("passive_curv", "mean"),
            path_len=("path_len", "mean"),
        )
        .reset_index()
    )

    g["label"] = label
    g["failure"] = 1 if label == "low" else 0
    g["kind"] = kind

    # Frozen restoration deficit
    g["adm_z"] = (g["restoration_measure"] - adm_mean) / adm_std

    # Candidate Atrium scalar:
    # high when residual is high, contraction is low, curvature relief is low, path strain is high.
    g["atrium_metric"] = (
        g["adm_z"]
        + 2.0 * (1.0 - g["contraction"])
        + 1.0 * (1.0 - g["curv_relief"])
        + 0.15 * np.log1p(g["metric_strain"])
    )

    return g


# ==============================================================================
# CALIBRATION
# ==============================================================================

def build_calibration(n_pairs: int = 14):
    rows = []
    for i in range(n_pairs):
        kind = SHOCK_KINDS[i % len(SHOCK_KINDS)]
        hi, _ = paired_assay(i, LOW_K, kind, 1000 + i)
        g = hi.groupby("pair_id").agg(restoration_measure=("post_dist", "mean")).reset_index()
        rows.append(g)

    cal = pd.concat(rows, ignore_index=True)
    adm_mean = cal["restoration_measure"].mean()
    adm_std = cal["restoration_measure"].std(ddof=1) + 1e-12
    return adm_mean, adm_std, cal


# ==============================================================================
# MAIN RUN
# ==============================================================================

def main():
    adm_mean, adm_std, cal = build_calibration()

    rows = []
    deltas = []

    for i in range(36):
        kind = SHOCK_KINDS[i % len(SHOCK_KINDS)]
        hi, lo = paired_assay(i, LOW_K, kind, 2000 + i)

        high = summarize_branch(hi, "high", kind, adm_mean, adm_std)
        low = summarize_branch(lo, "low", kind, adm_mean, adm_std)

        rows += [high, low]

        deltas.append(
            {
                "pair_id": i,
                "kind": kind,
                "delta_adm_z": float(low["adm_z"].iloc[0] - high["adm_z"].iloc[0]),
                "delta_atrium": float(low["atrium_metric"].iloc[0] - high["atrium_metric"].iloc[0]),
                "delta_passive": float(low["passive_mean"].iloc[0] - high["passive_mean"].iloc[0]),
            }
        )

    df = pd.concat(rows, ignore_index=True)
    delta_df = pd.DataFrame(deltas)

    # K-gap ablation using frozen calibration.
    gap_rows = []
    for k_low in [0.20, 0.35, 0.50, 0.70, 0.85, 1.00]:
        temp = []
        for i in range(16):
            kind = SHOCK_KINDS[i % len(SHOCK_KINDS)]
            hi, lo = paired_assay(i, k_low, kind, 3000 + int(k_low * 100) + i)

            temp += [
                summarize_branch(hi, "high", kind, adm_mean, adm_std),
                summarize_branch(lo, "low", kind, adm_mean, adm_std),
            ]

        gd = pd.concat(temp, ignore_index=True)

        if k_low == 1.00:
            y = np.random.default_rng(99).integers(0, 2, len(gd))
        else:
            y = gd["failure"].values

        gap_rows.append(
            {
                "k_low": k_low,
                "k_gap": HIGH_K - k_low,
                "auc_adm_z": roc_auc_score(y, gd["adm_z"]),
                "auc_atrium_metric": roc_auc_score(y, gd["atrium_metric"]),
                "auc_passive_mean": roc_auc_score(y, gd["passive_mean"]),
                "mean_delta_atrium": float(
                    gd[gd.label == "low"]["atrium_metric"].mean()
                    - gd[gd.label == "high"]["atrium_metric"].mean()
                ),
                "mean_delta_adm_z": float(
                    gd[gd.label == "low"]["adm_z"].mean()
                    - gd[gd.label == "high"]["adm_z"].mean()
                ),
            }
        )

    gap_df = pd.DataFrame(gap_rows)

    y = df["failure"].values
    summary = {
        "version": "V725_AtriumMetricExtraction",
        "adm_mean": float(adm_mean),
        "adm_std": float(adm_std),
        "auc_adm_z": float(roc_auc_score(y, df["adm_z"])),
        "auc_atrium_metric": float(roc_auc_score(y, df["atrium_metric"])),
        "auc_passive_mean": float(roc_auc_score(y, df["passive_mean"])),
        "auc_passive_curv": float(roc_auc_score(y, df["passive_curv"])),
        "paired_delta_atrium_mean": float(delta_df["delta_atrium"].mean()),
        "paired_delta_adm_z_mean": float(delta_df["delta_adm_z"].mean()),
        "paired_delta_passive_abs_max": float(delta_df["delta_passive"].abs().max()),
        "interpretation": (
            "First Atrium scalar extracted from restoration deficit, contraction, "
            "curvature relief, and metric strain. It remains response-specific while "
            "passive burden is fixed."
        ),
    }

    df.to_csv(OUT / "v725_run_level_atrium_metric.csv", index=False)
    delta_df.to_csv(OUT / "v725_paired_metric_deltas.csv", index=False)
    gap_df.to_csv(OUT / "v725_k_gap_ablation.csv", index=False)
    (OUT / "v725_summary.json").write_text(json.dumps(summary, indent=2))

    report = "# V725 Atrium Metric Extraction\n\n"
    report += "## Purpose\n\n"
    report += (
        "Extract a first operational response-geometry scalar from V723-style "
        "passive-equivalent perturbation-response assays.\n\n"
    )
    report += "## Candidate scalar\n\n"
    report += "`A = adm_z + 2(1-contraction) + (1-curvature_relief) + 0.15 log(1+metric_strain)`\n\n"
    report += (
        "This is not a GR metric tensor. It is a first operational scalar proxy "
        "for response-geometry deformation.\n\n"
    )
    report += "## Summary\n\n"
    report += "```json\n" + json.dumps(summary, indent=2) + "\n```\n\n"
    report += "## K-gap ablation\n\n"
    report += gap_df.to_markdown(index=False)
    report += "\n\n## Interpretation\n\n"
    report += (
        "The Atrium scalar tracks hidden restoration capacity while passive burden "
        "is held fixed. The next step is to generalize this scalar into a local "
        "tensor or metric-field candidate and test coordinate/perturbation invariance.\n"
    )

    (OUT / "V725_ATRIUM_METRIC_EXTRACTION.md").write_text(report)

    # Plots
    plt.figure(figsize=(7, 4))
    for label in ["high", "low"]:
        plt.hist(df[df.label == label]["atrium_metric"], bins=16, alpha=0.6, label=label)
    plt.title("V725 Atrium Metric Distribution")
    plt.xlabel("atrium_metric")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "atrium_metric_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(gap_df["k_gap"], gap_df["auc_atrium_metric"], marker="o", label="atrium")
    plt.plot(gap_df["k_gap"], gap_df["auc_adm_z"], marker="o", label="adm_z")
    plt.plot(gap_df["k_gap"], gap_df["auc_passive_mean"], marker="o", label="passive")
    plt.axhline(0.5, linestyle="--", linewidth=1)
    plt.xlabel("k gap")
    plt.ylabel("AUC")
    plt.title("V725 k-gap ablation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "v725_k_gap_ablation.png", dpi=160)
    plt.close()

    zip_path = Path("v725_atrium_metric_extraction.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in OUT.iterdir():
            z.write(p, arcname=p.name)

    print(json.dumps(summary, indent=2))
    print("\nK-gap ablation:")
    print(gap_df.to_string(index=False))
    print("\nZIP:", zip_path)


if __name__ == "__main__":
    main()
