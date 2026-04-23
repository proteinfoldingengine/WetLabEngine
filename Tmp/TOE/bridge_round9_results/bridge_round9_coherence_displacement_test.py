
"""
bridge_round9_coherence_displacement_test.py

Purpose
-------
Next iteration inspired by earlier nonlocal/coherence-displacement mechanics.

This script does NOT claim a derived law.
It constructs a new family of Bridge-derived observables meant to be closer to
"displacement / filament / nonlocal transport" ideas than the older simple means:
    - coherence_displacement_index
    - filament_persistence_index
    - transport_asymmetry_index
    - outer_memory_buildup_index

Then it tests whether these derived observables help predict:
    - Bridge delta_v correlation
    - Bridge sign-match fraction
    - Bridge RMSE improvement
    - Bridge onset radius
    - residual class

Required prior files
--------------------
From round 5:
- bridge_round5_results/round5_bridge_vs_mond_merged.csv

From round 4:
- bridge_round4_results/round4_full_comparison.csv

Outputs
-------
bridge_round9_results/round9_derived_observables.csv
bridge_round9_results/round9_regression_summary.csv
bridge_round9_results/round9_classification_summary.csv
bridge_round9_results/round9_feature_correlation_table.csv
bridge_round9_results/round9_r2.png
bridge_round9_results/round9_macro_f1.png

Usage
-----
!python bridge_round9_coherence_displacement_test.py
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, f1_score, balanced_accuracy_score

ROOT = Path(".")
IN5 = ROOT / "bridge_round5_results"
IN4 = ROOT / "bridge_round4_results"
OUT = ROOT / "bridge_round9_results"
OUT.mkdir(parents=True, exist_ok=True)

MERGED = IN5 / "round5_bridge_vs_mond_merged.csv"
FULL4 = IN4 / "round4_full_comparison.csv"


def assign_residual_class(df: pd.DataFrame) -> pd.Series:
    sign_match = df["delta_v_sign_match_fraction_bridge"]
    corr = df["delta_v_corrcoef_vs_obs_bridge"]
    outer = df["mean_outer_delta_v_bridge"]
    outer_med = np.nanmedian(outer)

    labels = []
    for s, c, o in zip(sign_match, corr, outer):
        if (s >= 0.80) and (c >= 0.75):
            labels.append("strong_positive")
        elif (s <= 0.40) and (o >= outer_med):
            labels.append("overboosted")
        else:
            labels.append("mixed")
    return pd.Series(labels, index=df.index, name="residual_class")


def build_derived_observables(merged: pd.DataFrame) -> pd.DataFrame:
    df = merged.copy()

    # 1) Coherence displacement index:
    #    small-support / large-selectivity type quantity
    df["coherence_displacement_index"] = (
        df["mean_outer_delta_v_bridge"] / (df["mean_outer_delta_v_mond"] + 1e-9)
    ) * (df["mean_lambda_bridge"] + 1e-9)

    # 2) Filament persistence index:
    #    retain nonlocal memory while tracking morphology-conditioned structure
    df["filament_persistence_index"] = (
        df["mean_retained_weight_bridge"] * df["mean_component_weight_bridge"]
    ) / (df["concentration_proxy_bridge"] + 1e-9)

    # 3) Transport asymmetry index:
    #    stronger when Bridge support is more selective than MOND but still shape-coherent
    df["transport_asymmetry_index"] = (
        (df["delta_v_corrcoef_vs_obs_bridge"] + 1.0)
        * (df["mean_outer_delta_v_mond"] - df["mean_outer_delta_v_bridge"])
        / (np.abs(df["mean_outer_delta_v_mond"]) + 1e-9)
    )

    # 4) Outer memory buildup index:
    #    low-acceleration-style support modulated by retained state rather than one universal boost
    df["outer_memory_buildup_index"] = (
        df["mean_lambda_bridge"] * df["mean_retained_weight_bridge"] * df["mean_outer_delta_v_bridge"]
    )

    # 5) Coherence selectivity index:
    #    how much shape is recovered per unit outer support
    df["coherence_selectivity_index"] = (
        df["delta_v_corrcoef_vs_obs_bridge"] / (df["mean_outer_delta_v_bridge"] + 1e-9)
    )

    return df


def eval_regression(df: pd.DataFrame, target: str, features: list[str], label: str):
    X = df[features]
    y = df[target]

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=1.0)),
    ])
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(model, X, y, cv=cv)
    return {
        "target": target,
        "feature_set": label,
        "mean_r2": float(r2_score(y, y_pred)),
        "mean_mae": float(mean_absolute_error(y, y_pred)),
    }


def eval_classification(df: pd.DataFrame, target: str, features: list[str], label: str):
    X = df[features]
    y = df[target]

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000, class_weight="balanced")),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(model, X, y, cv=cv)

    return {
        "feature_set": label,
        "macro_f1": float(f1_score(y, y_pred, average="macro")),
        "balanced_accuracy": float(balanced_accuracy_score(y, y_pred)),
    }


def main():
    merged = pd.read_csv(MERGED)
    derived = build_derived_observables(merged)
    derived["residual_class"] = assign_residual_class(derived)
    derived.to_csv(OUT / "round9_derived_observables.csv", index=False)

    morphology = [
        "mean_disk_frac_bridge",
        "mean_bulge_frac_bridge",
        "concentration_proxy_bridge",
    ]

    bridge_internal = [
        "mean_component_weight_bridge",
        "mean_lambda_bridge",
        "mean_retained_weight_bridge",
        "mean_corr_field_bridge",
    ]

    derived_feats = [
        "coherence_displacement_index",
        "filament_persistence_index",
        "transport_asymmetry_index",
        "outer_memory_buildup_index",
        "coherence_selectivity_index",
    ]

    combined_old = morphology + bridge_internal
    combined_new = morphology + bridge_internal + derived_feats

    targets = [
        "delta_v_corrcoef_vs_obs_bridge",
        "delta_v_sign_match_fraction_bridge",
        "rmse_improvement_bridge",
        "onset_radius_kpc_bridge",
    ]

    reg_rows = []
    for target in targets:
        for label, feats in [
            ("morphology_only", morphology),
            ("bridge_internal_only", bridge_internal),
            ("derived_only", derived_feats),
            ("combined_old", combined_old),
            ("combined_new", combined_new),
        ]:
            reg_rows.append(eval_regression(derived, target, feats, label))

    reg = pd.DataFrame(reg_rows).sort_values(["target", "mean_r2"], ascending=[True, False])
    reg.to_csv(OUT / "round9_regression_summary.csv", index=False)

    cls_rows = []
    for label, feats in [
        ("morphology_only", morphology),
        ("bridge_internal_only", bridge_internal),
        ("derived_only", derived_feats),
        ("combined_old", combined_old),
        ("combined_new", combined_new),
    ]:
        cls_rows.append(eval_classification(derived, "residual_class", feats, label))

    cls = pd.DataFrame(cls_rows).sort_values("macro_f1", ascending=False)
    cls.to_csv(OUT / "round9_classification_summary.csv", index=False)

    # feature correlations
    corr_rows = []
    targets_for_corr = [
        "delta_v_corrcoef_vs_obs_bridge",
        "delta_v_sign_match_fraction_bridge",
        "rmse_improvement_bridge",
        "onset_radius_kpc_bridge",
        "mean_outer_delta_v_bridge",
    ]
    features_for_corr = morphology + bridge_internal + derived_feats
    for feat in features_for_corr:
        for targ in targets_for_corr:
            x = derived[feat].to_numpy()
            y = derived[targ].to_numpy()
            mask = np.isfinite(x) & np.isfinite(y)
            corr = np.nan
            if np.sum(mask) > 3 and np.std(x[mask]) > 0 and np.std(y[mask]) > 0:
                corr = float(np.corrcoef(x[mask], y[mask])[0,1])
            corr_rows.append({"feature": feat, "target": targ, "corrcoef": corr})
    corr_df = pd.DataFrame(corr_rows).sort_values("corrcoef", ascending=False)
    corr_df.to_csv(OUT / "round9_feature_correlation_table.csv", index=False)

    # plots
    target_order = targets
    feat_order = ["morphology_only", "bridge_internal_only", "derived_only", "combined_old", "combined_new"]
    x = np.arange(len(target_order))
    w = 0.15

    plt.figure(figsize=(11, 6))
    for i, feat in enumerate(feat_order):
        sub = reg[reg["feature_set"] == feat].set_index("target").loc[target_order]
        plt.bar(x + (i - 2) * w, sub["mean_r2"].to_numpy(), width=w, label=feat)
    plt.xticks(x, target_order, rotation=20, ha="right")
    plt.ylabel("Cross-validated R²")
    plt.title("Round 9: do derived displacement observables improve prediction?")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "round9_r2.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.5))
    plt.bar(cls["feature_set"], cls["macro_f1"])
    plt.ylabel("Macro F1")
    plt.title("Round 9 residual-class prediction")
    plt.tight_layout()
    plt.savefig(OUT / "round9_macro_f1.png", dpi=180)
    plt.close()

    print("Regression summary:")
    print(reg.to_string(index=False))
    print("\nClassification summary:")
    print(cls.to_string(index=False))
    print("\nTop feature correlations:")
    print(corr_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
