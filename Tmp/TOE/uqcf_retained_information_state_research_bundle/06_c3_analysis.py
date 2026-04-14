from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


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


@dataclass
class ModelResult:
    name: str
    roc_auc: float
    pr_auc: float
    log_loss_value: float


def make_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]
    )


def evaluate_model(
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
    group_col: str = "run_id",
) -> ModelResult:
    usable = df.dropna(subset=[target_col]).copy()
    X = usable[feature_cols]
    y = usable[target_col].astype(int).to_numpy()
    groups = usable[group_col].astype(str).to_numpy()

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y[train_idx]
    y_test = y[test_idx]

    pipe = make_pipeline()
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]

    return ModelResult(
        name="+".join(feature_cols),
        roc_auc=float(roc_auc_score(y_test, proba)),
        pr_auc=float(average_precision_score(y_test, proba)),
        log_loss_value=float(log_loss(y_test, proba)),
    )


def matched_pair_analysis(
    df: pd.DataFrame,
    target_col: str,
    g_threshold: float = 0.35,
    r_threshold: float = 1.5,
) -> pd.DataFrame:
    use_cols = ["run_id", target_col] + G_FEATURES + R_FEATURES
    work = df.dropna(subset=[target_col]).copy()[use_cols]

    g = work[G_FEATURES].to_numpy(dtype=float)
    r = work[R_FEATURES].to_numpy(dtype=float)

    # simple z-score standardization for matching only
    g = (g - np.nanmean(g, axis=0)) / (np.nanstd(g, axis=0) + 1e-8)
    r = (r - np.nanmean(r, axis=0)) / (np.nanstd(r, axis=0) + 1e-8)

    pair_rows = []
    n = len(work)

    # sample anchors for efficiency
    anchor_idx = np.arange(0, n, max(1, n // 300))
    for i in anchor_idx:
        gdist = np.sqrt(np.mean((g - g[i]) ** 2, axis=1))
        rdist = np.sqrt(np.mean((r - r[i]) ** 2, axis=1))

        mask = (gdist <= g_threshold) & (rdist >= r_threshold)
        mask[i] = False
        if not np.any(mask):
            continue

        # choose strongest retained-state separation among close geometry points
        candidates = np.where(mask)[0]
        j = candidates[np.argmax(rdist[candidates])]

        pair_rows.append(
            {
                "idx_a": int(i),
                "idx_b": int(j),
                "g_distance": float(gdist[j]),
                "r_distance": float(rdist[j]),
                "target_a": int(work.iloc[i][target_col]),
                "target_b": int(work.iloc[j][target_col]),
                "different_future_outcome": int(work.iloc[i][target_col] != work.iloc[j][target_col]),
            }
        )

    return pd.DataFrame(pair_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to telemetry CSV")
    parser.add_argument("--target", default="fail_within_32", help="Binary target column")
    parser.add_argument("--outdir", default="c3_retained_state_results", help="Output directory")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)

    result_g = evaluate_model(df, G_FEATURES, args.target)
    result_gr = evaluate_model(df, G_FEATURES + R_FEATURES, args.target)

    summary = pd.DataFrame(
        [
            {
                "model": "G_only",
                "roc_auc": result_g.roc_auc,
                "pr_auc": result_g.pr_auc,
                "log_loss": result_g.log_loss_value,
            },
            {
                "model": "G_plus_R",
                "roc_auc": result_gr.roc_auc,
                "pr_auc": result_gr.pr_auc,
                "log_loss": result_gr.log_loss_value,
            },
        ]
    )
    summary.to_csv(outdir / "predictor_comparison.csv", index=False)

    pairs = matched_pair_analysis(df, args.target)
    if len(pairs) > 0:
        pairs.to_csv(outdir / "matched_pair_analysis.csv", index=False)

        pair_summary = pd.DataFrame(
            [
                {
                    "n_pairs": int(len(pairs)),
                    "mean_g_distance": float(pairs["g_distance"].mean()),
                    "mean_r_distance": float(pairs["r_distance"].mean()),
                    "future_outcome_disagreement_rate": float(pairs["different_future_outcome"].mean()),
                }
            ]
        )
        pair_summary.to_csv(outdir / "matched_pair_summary.csv", index=False)

    print(summary.to_string(index=False))
    if len(pairs) > 0:
        print()
        print(pair_summary.to_string(index=False))


if __name__ == "__main__":
    main()
