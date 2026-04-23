
"""
bridge_round6_post_pack.py

Builds a compact "Bridge is not just another fit law" pack from round 5 outputs.

Inputs expected in current working directory:
- bridge_round5_results/round5_bridge_vs_mond_merged.csv
- bridge_round5_results/round5_quartile_diagnostics.csv
- bridge_round5_results/round5_bridge_internal_correlations.csv
- bridge_round5_results/round5_aggregate.csv

Outputs:
- round6_summary_tables.txt
- round6_key_quartiles.csv
- round6_key_correlations.csv
- round6_bridge_vs_mond_quartiles.png
- round6_bridge_internal_predictors.png
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root = Path(".")
in_dir = root / "bridge_round5_results"
out_dir = root / "bridge_round6_post_pack"
out_dir.mkdir(parents=True, exist_ok=True)

quart = pd.read_csv(in_dir / "round5_quartile_diagnostics.csv")
corrs = pd.read_csv(in_dir / "round5_bridge_internal_correlations.csv")
agg = pd.read_csv(in_dir / "round5_aggregate.csv")
merged = pd.read_csv(in_dir / "round5_bridge_vs_mond_merged.csv")

# Focus on the cleanest morphology axis from the preview
key_axis = "concentration_proxy_bridge"
key_quart = quart[quart["axis"] == key_axis].copy()
key_quart.to_csv(out_dir / "round6_key_quartiles.csv", index=False)

# Focus on strongest positive correlations
wanted_targets = [
    "delta_v_sign_match_fraction_bridge",
    "delta_v_corrcoef_vs_obs_bridge",
    "onset_radius_kpc_bridge",
    "mean_outer_delta_v_bridge",
]
key_corrs = corrs[corrs["target"].isin(wanted_targets)].sort_values("corrcoef", ascending=False).head(20).copy()
key_corrs.to_csv(out_dir / "round6_key_correlations.csv", index=False)

# Text summary
bridge_row = agg[agg["model"] == "bridge"].iloc[0]
mond_row = agg[agg["model"] == "mond_standard"].iloc[0]
bary_row = agg[agg["model"] == "baryonic"].iloc[0]

lines = []
lines.append("ROUND 6 POST PACK SUMMARY")
lines.append("=" * 28)
lines.append("")
lines.append("Top-level benchmark")
lines.append(f"- Bridge mean RMSE improvement vs baryonic: {bridge_row['mean_rmse_improvement']:.3f}")
lines.append(f"- Bridge mean Δv correlation: {bridge_row['mean_delta_v_corr']:.3f}")
lines.append(f"- Bridge mean sign match: {bridge_row['mean_sign_match']:.3f}")
lines.append(f"- Bridge mean outer Δv: {bridge_row['mean_outer_delta_v']:.3f}")
lines.append("")
lines.append(f"- MOND-standard mean RMSE improvement vs baryonic: {mond_row['mean_rmse_improvement']:.3f}")
lines.append(f"- MOND-standard mean Δv correlation: {mond_row['mean_delta_v_corr']:.3f}")
lines.append(f"- MOND-standard mean sign match: {mond_row['mean_sign_match']:.3f}")
lines.append(f"- MOND-standard mean outer Δv: {mond_row['mean_outer_delta_v']:.3f}")
lines.append("")
lines.append("What makes Bridge structurally different")
lines.append("- Bridge outer support is much smaller than MOND's on average.")
lines.append("- Bridge response varies across morphology/concentration quartiles.")
lines.append("- Bridge internal variables correlate with sign-match and residual-shape quality.")
lines.append("")
lines.append("Concentration quartiles (Bridge vs MOND)")
for _, row in key_quart.iterrows():
    lines.append(
        f"- {row['quartile']}: "
        f"Bridge RMSE+ {row['bridge_mean_rmse_improvement']:.2f}, "
        f"MOND RMSE+ {row['mond_mean_rmse_improvement']:.2f}; "
        f"Bridge corr {row['bridge_mean_delta_v_corr']:.3f}, "
        f"MOND corr {row['mond_mean_delta_v_corr']:.3f}; "
        f"Bridge/MOND outer-support ratio {row['mean_outer_support_ratio_bridge_to_mond']:.3f}"
    )
lines.append("")
lines.append("Strongest Bridge internal predictors")
for _, row in key_corrs.head(8).iterrows():
    lines.append(f"- {row['source']} -> {row['target']}: r = {row['corrcoef']:.3f}")

(out_dir / "round6_summary_tables.txt").write_text("\n".join(lines))

# Plot 1: quartiles
x = np.arange(len(key_quart))
w = 0.36
plt.figure(figsize=(9, 5.5))
plt.bar(x - w/2, key_quart["bridge_mean_rmse_improvement"], width=w, label="Bridge RMSE improvement")
plt.bar(x + w/2, key_quart["mond_mean_rmse_improvement"], width=w, label="MOND RMSE improvement")
plt.xticks(x, key_quart["quartile"])
plt.xlabel("Concentration quartile")
plt.ylabel("Mean RMSE improvement vs baryonic [km/s]")
plt.title("Bridge vs MOND by concentration quartile")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "round6_bridge_vs_mond_quartiles.png", dpi=180)
plt.close()

# Plot 2: bridge internal predictors
plot_corrs = key_corrs.head(10).iloc[::-1]
labels = [f"{s} → {t}" for s, t in zip(plot_corrs["source"], plot_corrs["target"])]
vals = plot_corrs["corrcoef"].to_numpy()

plt.figure(figsize=(10, 6))
plt.barh(range(len(vals)), vals)
plt.yticks(range(len(vals)), labels, fontsize=8)
plt.xlabel("Correlation coefficient")
plt.title("Bridge internal predictors of structural fit behavior")
plt.tight_layout()
plt.savefig(out_dir / "round6_bridge_internal_predictors.png", dpi=180)
plt.close()

print("Created round6 post pack in", out_dir)
print((out_dir / "round6_summary_tables.txt").read_text())
