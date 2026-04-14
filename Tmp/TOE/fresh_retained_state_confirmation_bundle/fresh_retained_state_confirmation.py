from __future__ import annotations

from pathlib import Path
import argparse
import json
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def simulate_system(
    n_traj: int = 250,
    T: int = 140,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Fresh retained-state toy system built from scratch.

    Visible/current state:
        x_t  : current observable state
    Retained-information state:
        r_t  : hidden retained state that carries path information

    Dynamics are bounded and mildly nonlinear:
        x_{t+1} = tanh(a*x_t + b*r_t + noise)
        r_{t+1} = tanh(lam*r_t + c*x_t - d*x_t^3 + eta_t)

    The analysis later deliberately hides r_t from the G-only model.
    """
    rng = np.random.default_rng(seed)
    a, b = 0.90, 0.72
    lam, c, d = 0.94, 0.22, 0.16

    rows = []
    for traj in range(n_traj):
        x = rng.normal(0.0, 0.8)
        r = rng.normal(0.0, 0.9)
        prev_x = x
        for t in range(T):
            eps = rng.normal(0.0, 0.04)
            eta = rng.normal(0.0, 0.03)

            x_next = np.tanh(a * x + b * r + eps)
            r_next = np.tanh(lam * r + c * x - d * (x ** 3) + eta)

            # Build a C3++-like visible state G_t from instantaneous quantities only
            current_entropy = 1.0 - abs(x) / 1.5
            current_topk_mass = 0.55 + 0.35 * (1.0 - abs(np.tanh(0.8 * x)))
            current_repetition_ratio = min(1.0, abs(x - prev_x))
            current_local_semantic_displacement = x - prev_x
            h1 = np.tanh(1.2 * x)
            h2 = np.tanh(0.7 * x + 0.25 * prev_x)
            h3 = np.tanh(-0.5 * x + 0.4 * prev_x)

            # Retained state R_t is generated from path/history structure
            mem_tension = r + 0.25 * abs(x)
            mem_drift = 0.8 * r + 0.4 * (x - prev_x)
            mem_entropy = 0.7 * r + 0.3 * current_entropy
            mem_repetition = 0.3 * r + 0.8 * current_repetition_ratio
            mem_recovery = -0.7 * r + 0.35 * (1.0 - current_repetition_ratio)
            mem_pink_noise_deviation = 0.45 * r + 0.2 * np.sin(3.0 * x)

            rows.append(
                {
                    "run_id": f"run_{traj}",
                    "prompt_id": f"prompt_{traj % 25}",
                    "model_id": "fresh_retained_state_model",
                    "token_index": t,
                    "x": x,
                    "r": r,
                    "x_next": x_next,
                    "current_entropy": current_entropy,
                    "current_topk_mass": current_topk_mass,
                    "current_repetition_ratio": current_repetition_ratio,
                    "current_local_semantic_displacement": current_local_semantic_displacement,
                    "current_hidden_state_projection_1": h1,
                    "current_hidden_state_projection_2": h2,
                    "current_hidden_state_projection_3": h3,
                    "mem_tension": mem_tension,
                    "mem_drift": mem_drift,
                    "mem_entropy": mem_entropy,
                    "mem_repetition": mem_repetition,
                    "mem_recovery": mem_recovery,
                    "mem_pink_noise_deviation": mem_pink_noise_deviation,
                }
            )
            prev_x = x
            x, r = x_next, r_next

    df = pd.DataFrame(rows)

    # Future labels over horizon H
    for horizon in [16, 32, 64]:
        fail = []
        for _, g in df.groupby("run_id"):
            xs = g["x"].to_numpy()
            vals = np.zeros(len(xs), dtype=int)
            for i in range(len(xs)):
                j = min(len(xs), i + horizon + 1)
                # failure: future magnitude exceeds threshold often enough
                vals[i] = int(np.max(np.abs(xs[i:j])) > 0.92)
            fail.extend(vals.tolist())
        df[f"fail_within_{horizon}"] = fail

    return df


G_FEATURES = [
    "current_entropy",
    "current_topk_mass",
    "current_repetition_ratio",
    "current_local_semantic_displacement",
    "current_hidden_state_projection_1",
    "current_hidden_state_projection_2",
    "current_hidden_state_projection_3",
]

R_FEATURES = [
    "mem_tension",
    "mem_drift",
    "mem_entropy",
    "mem_repetition",
    "mem_recovery",
    "mem_pink_noise_deviation",
]


def make_clf() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=3000, class_weight="balanced")),
        ]
    )


def eval_prediction(df: pd.DataFrame, target: str, seed: int = 7) -> pd.DataFrame:
    usable = df.dropna(subset=[target]).copy()
    y = usable[target].astype(int).to_numpy()
    groups = usable["run_id"].astype(str).to_numpy()

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)

    rows = []
    for name, features in {
        "G_only": G_FEATURES,
        "G_plus_R": G_FEATURES + R_FEATURES,
    }.items():
        train_idx, test_idx = next(splitter.split(usable[features], y, groups=groups))
        X_train = usable.iloc[train_idx][features]
        X_test = usable.iloc[test_idx][features]
        y_train = y[train_idx]
        y_test = y[test_idx]

        pipe = make_clf()
        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]

        rows.append(
            {
                "model": name,
                "roc_auc": roc_auc_score(y_test, proba),
                "pr_auc": average_precision_score(y_test, proba),
                "log_loss": log_loss(y_test, proba),
            }
        )

    return pd.DataFrame(rows)


def matched_pair_analysis(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = df.dropna(subset=[target]).copy()

    g = work[G_FEATURES].to_numpy(float)
    r = work[R_FEATURES].to_numpy(float)

    g = (g - np.nanmean(g, axis=0)) / (np.nanstd(g, axis=0) + 1e-8)
    r = (r - np.nanmean(r, axis=0)) / (np.nanstd(r, axis=0) + 1e-8)

    far_rows = []
    close_rows = []
    anchor_idx = np.arange(0, len(work), max(1, len(work) // 300))

    for i in anchor_idx:
        gdist = np.sqrt(np.mean((g - g[i]) ** 2, axis=1))
        rdist = np.sqrt(np.mean((r - r[i]) ** 2, axis=1))
        mask_g = gdist <= 0.35
        mask_g[i] = False

        close = np.where(mask_g & (rdist <= 0.50))[0]
        far = np.where(mask_g & (rdist >= 1.50))[0]

        if len(close):
            j = close[np.argmin(gdist[close])]
            close_rows.append(
                {
                    "g_distance": float(gdist[j]),
                    "r_distance": float(rdist[j]),
                    "different_future_outcome": int(work.iloc[i][target] != work.iloc[j][target]),
                }
            )
        if len(far):
            j = far[np.argmax(rdist[far])]
            far_rows.append(
                {
                    "g_distance": float(gdist[j]),
                    "r_distance": float(rdist[j]),
                    "different_future_outcome": int(work.iloc[i][target] != work.iloc[j][target]),
                }
            )

    close_df = pd.DataFrame(close_rows)
    far_df = pd.DataFrame(far_rows)

    summary = pd.DataFrame(
        [
            {
                "n_close_pairs": len(close_df),
                "close_pair_disagreement_rate": close_df["different_future_outcome"].mean() if len(close_df) else np.nan,
                "n_far_pairs": len(far_df),
                "far_pair_disagreement_rate": far_df["different_future_outcome"].mean() if len(far_df) else np.nan,
                "disagreement_gap_far_minus_close": (
                    far_df["different_future_outcome"].mean() - close_df["different_future_outcome"].mean()
                    if len(close_df) and len(far_df)
                    else np.nan
                ),
            }
        ]
    )
    return close_df, far_df, summary


def repeated_split_validation(df: pd.DataFrame, target: str, n_splits: int = 30) -> pd.DataFrame:
    usable = df.dropna(subset=[target]).copy()
    rows = []

    for seed in range(n_splits):
        groups = usable["run_id"].astype(str).to_numpy()
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)

        def score(features):
            y = usable[target].astype(int).to_numpy()
            train_idx, test_idx = next(splitter.split(usable[features], y, groups=groups))
            X_train = usable.iloc[train_idx][features]
            X_test = usable.iloc[test_idx][features]
            y_train = y[train_idx]
            y_test = y[test_idx]
            pipe = make_clf()
            pipe.fit(X_train, y_train)
            p = pipe.predict_proba(X_test)[:, 1]
            return roc_auc_score(y_test, p), average_precision_score(y_test, p), log_loss(y_test, p)

        g_roc, g_pr, g_ll = score(G_FEATURES)
        gr_roc, gr_pr, gr_ll = score(G_FEATURES + R_FEATURES)

        rows.append(
            {
                "seed": seed,
                "roc_auc_lift": gr_roc - g_roc,
                "pr_auc_lift": gr_pr - g_pr,
                "log_loss_improvement": g_ll - gr_ll,
            }
        )

    return pd.DataFrame(rows)


def reconstructibility(df: pd.DataFrame) -> pd.DataFrame:
    usable = df.dropna().copy()
    rows = []
    for col in R_FEATURES:
        model = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("lr", LinearRegression()),
            ]
        )
        model.fit(usable[G_FEATURES], usable[col])
        pred = model.predict(usable[G_FEATURES])
        rows.append(
            {
                "channel": col,
                "linear_R2_from_G": r2_score(usable[col], pred),
                "residual_std": np.std(usable[col] - pred),
                "raw_std": np.std(usable[col]),
            }
        )
    return pd.DataFrame(rows).sort_values("linear_R2_from_G")


def channel_ablation(df: pd.DataFrame, target: str, seed: int = 11) -> pd.DataFrame:
    usable = df.dropna(subset=[target]).copy()
    y = usable[target].astype(int).to_numpy()
    groups = usable["run_id"].astype(str).to_numpy()
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)

    def score(features):
        train_idx, test_idx = next(splitter.split(usable[features], y, groups=groups))
        X_train = usable.iloc[train_idx][features]
        X_test = usable.iloc[test_idx][features]
        y_train = y[train_idx]
        y_test = y[test_idx]
        pipe = make_clf()
        pipe.fit(X_train, y_train)
        p = pipe.predict_proba(X_test)[:, 1]
        return roc_auc_score(y_test, p), average_precision_score(y_test, p), log_loss(y_test, p)

    full_roc, full_pr, full_ll = score(G_FEATURES + R_FEATURES)

    rows = []
    rows.append(
        {
            "model": "G_only",
            "removed_channel": "",
            **dict(zip(["roc_auc", "pr_auc", "log_loss"], score(G_FEATURES))),
            "roc_auc_drop_vs_full": full_roc - score(G_FEATURES)[0],
        }
    )

    rows.append(
        {
            "model": "G_plus_R",
            "removed_channel": "",
            "roc_auc": full_roc,
            "pr_auc": full_pr,
            "log_loss": full_ll,
            "roc_auc_drop_vs_full": 0.0,
        }
    )

    for ch in R_FEATURES:
        feats = G_FEATURES + [x for x in R_FEATURES if x != ch]
        roc, pr, ll = score(feats)
        rows.append(
            {
                "model": "G_plus_R_minus_one",
                "removed_channel": ch,
                "roc_auc": roc,
                "pr_auc": pr,
                "log_loss": ll,
                "roc_auc_drop_vs_full": full_roc - roc,
                "log_loss_increase_vs_full": ll - full_ll,
            }
        )

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="fresh_retained_state_confirmation")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = simulate_system()
    df.to_csv(outdir / "fresh_retained_state_dataset.csv", index=False)

    pred = eval_prediction(df, "fail_within_32")
    pred.to_csv(outdir / "predictor_comparison.csv", index=False)

    close_df, far_df, pair_summary = matched_pair_analysis(df, "fail_within_32")
    close_df.to_csv(outdir / "matched_pairs_close_R.csv", index=False)
    far_df.to_csv(outdir / "matched_pairs_far_R.csv", index=False)
    pair_summary.to_csv(outdir / "matched_pair_summary.csv", index=False)

    repeated = repeated_split_validation(df, "fail_within_32", n_splits=40)
    repeated.to_csv(outdir / "repeated_split_validation.csv", index=False)

    recon = reconstructibility(df)
    recon.to_csv(outdir / "reconstructibility.csv", index=False)

    ablation = channel_ablation(df, "fail_within_32")
    ablation.to_csv(outdir / "channel_ablation.csv", index=False)

    # Plots
    plt.figure(figsize=(7.0, 4.5))
    plt.bar(pred["model"], pred["roc_auc"])
    plt.ylabel("ROC AUC")
    plt.title("Fresh retained-state confirmation: G vs G+R")
    plt.tight_layout()
    plt.savefig(outdir / "predictor_comparison.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.0, 4.5))
    plt.hist(repeated["roc_auc_lift"], bins=14)
    plt.xlabel("ROC AUC lift (G+R minus G-only)")
    plt.ylabel("Count")
    plt.title("Repeated-split retained-state lift")
    plt.tight_layout()
    plt.savefig(outdir / "repeated_split_lift.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.0, 4.6))
    rows = ablation[ablation["model"] == "G_plus_R_minus_one"].sort_values("roc_auc_drop_vs_full", ascending=False)
    plt.bar(rows["removed_channel"], rows["roc_auc_drop_vs_full"])
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("ROC AUC drop vs full")
    plt.title("Fresh channel ablation")
    plt.tight_layout()
    plt.savefig(outdir / "channel_ablation.png", dpi=180)
    plt.close()

    summary = {
        "predictor": pred.to_dict(orient="records"),
        "matched_pair_summary": pair_summary.to_dict(orient="records"),
        "repeated_split": {
            "mean_roc_auc_lift": float(repeated["roc_auc_lift"].mean()),
            "median_roc_auc_lift": float(repeated["roc_auc_lift"].median()),
            "share_positive_roc_auc_lift": float((repeated["roc_auc_lift"] > 0).mean()),
        },
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))

    report = f"""
# Fresh retained-state confirmation

This run rebuilds the retained-information result from scratch using a new bounded nonlinear system.

## Main result
- G_only ROC AUC: {pred[pred['model']=='G_only']['roc_auc'].iloc[0]:.4f}
- G_plus_R ROC AUC: {pred[pred['model']=='G_plus_R']['roc_auc'].iloc[0]:.4f}
- ROC AUC lift: {(pred[pred['model']=='G_plus_R']['roc_auc'].iloc[0] - pred[pred['model']=='G_only']['roc_auc'].iloc[0]):+.4f}

## Matched-pair contrast
- close-R disagreement rate: {pair_summary['close_pair_disagreement_rate'].iloc[0]:.4f}
- far-R disagreement rate: {pair_summary['far_pair_disagreement_rate'].iloc[0]:.4f}
- far-minus-close gap: {pair_summary['disagreement_gap_far_minus_close'].iloc[0]:+.4f}

## Repeated-split validation
- mean ROC AUC lift: {repeated['roc_auc_lift'].mean():.4f}
- median ROC AUC lift: {repeated['roc_auc_lift'].median():.4f}
- share positive lifts: {100*(repeated['roc_auc_lift']>0).mean():.1f}%

## Interpretation
This is not proof of the full TOE.
It is a fresh reconstruction showing that the retained-state theorem shape can be recreated independently:
current visible state can be incomplete, and retained state can add predictive value.
"""
    (outdir / "report.md").write_text(textwrap.dedent(report).strip() + "\n")


if __name__ == "__main__":
    main()
