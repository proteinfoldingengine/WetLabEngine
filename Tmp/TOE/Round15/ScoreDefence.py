from pathlib import Path
import pandas as pd
import numpy as np

GAS = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
MASS = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")
OUTDIR = Path("/content/Round15/challenge15_scoreable")
OUTDIR.mkdir(parents=True, exist_ok=True)

gas = pd.read_csv(GAS)
mass = pd.read_csv(MASS)

# Keep only the first scoreable pair
gas_t = (
    gas[gas["gas_profile_kind"] == "temperature"]
    .dropna(subset=["R_kpc_manual_extract", "gas_profile_manual_extract"])
    .copy()
)
mass_pm = (
    mass[mass["mass_profile_kind"] == "projected_mass"]
    .dropna(subset=["R_kpc_manual_extract", "mass_profile_manual_extract"])
    .copy()
)

gas_t = gas_t.sort_values("R_kpc_manual_extract")
mass_pm = mass_pm.sort_values("R_kpc_manual_extract")

print("Gas temperature points:")
print(gas_t.to_string(index=False))
print("\nMass projected-mass points:")
print(mass_pm.to_string(index=False))

# Shared radius range
rmin = max(gas_t["R_kpc_manual_extract"].min(), mass_pm["R_kpc_manual_extract"].min())
rmax = min(gas_t["R_kpc_manual_extract"].max(), mass_pm["R_kpc_manual_extract"].max())

if rmax <= rmin:
    raise ValueError(f"No overlapping radial range. gas=[{gas_t['R_kpc_manual_extract'].min()}, {gas_t['R_kpc_manual_extract'].max()}], "
                     f"mass=[{mass_pm['R_kpc_manual_extract'].min()}, {mass_pm['R_kpc_manual_extract'].max()}]")

# Conservative shared grid for prototype
shared_r = np.array(sorted(set(
    [r for r in gas_t["R_kpc_manual_extract"].tolist() if rmin <= r <= rmax] +
    [r for r in mass_pm["R_kpc_manual_extract"].tolist() if rmin <= r <= rmax]
)))

# If too sparse, create small linear grid
if len(shared_r) < 4:
    shared_r = np.linspace(rmin, rmax, 5)

# Interpolate onto shared grid
gas_interp = np.interp(shared_r, gas_t["R_kpc_manual_extract"], gas_t["gas_profile_manual_extract"])
mass_interp = np.interp(shared_r, mass_pm["R_kpc_manual_extract"], mass_pm["mass_profile_manual_extract"])

scoreable = pd.DataFrame({
    "system_name": "Abell 1689",
    "R_kpc": shared_r,
    "temperature_keV_proxy": gas_interp,
    "projected_mass_proxy": mass_interp
})

# Simple normalized columns for first-pass scoring
scoreable["temperature_norm"] = scoreable["temperature_keV_proxy"] / scoreable["temperature_keV_proxy"].max()
scoreable["projected_mass_norm"] = scoreable["projected_mass_proxy"] / scoreable["projected_mass_proxy"].max()
scoreable["abs_norm_gap"] = (scoreable["temperature_norm"] - scoreable["projected_mass_norm"]).abs()

out_csv = OUTDIR / "abell1689_scoreable_profile.csv"
scoreable.to_csv(out_csv, index=False)

summary = {
    "system_name": "Abell 1689",
    "n_shared_points": int(len(scoreable)),
    "shared_r_min_kpc": float(scoreable["R_kpc"].min()),
    "shared_r_max_kpc": float(scoreable["R_kpc"].max()),
    "mean_abs_norm_gap": float(scoreable["abs_norm_gap"].mean()),
    "max_abs_norm_gap": float(scoreable["abs_norm_gap"].max()),
    "prototype_status": "first_scoreable_tier1_profile"
}

print("\nSaved:", out_csv)
print("\nScoreable profile:")
print(scoreable.to_string(index=False))
print("\nSummary:")
print(summary)

from pathlib import Path
import pandas as pd
import json

CSV = Path("/content/Round15/challenge15_scoreable/abell1689_scoreable_profile.csv")
OUTDIR = Path("/content/Round15/challenge15_scoreable")
OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

# Simple first-pass Tier 1 score:
# lower normalized gap = better profile agreement
mean_gap = float(df["abs_norm_gap"].mean())
max_gap = float(df["abs_norm_gap"].max())

if mean_gap < 0.10:
    verdict = "positive_signal"
elif mean_gap < 0.25:
    verdict = "neutral"
else:
    verdict = "destructive_failure"

result = {
    "challenge": 15,
    "system_name": "Abell 1689",
    "tier": "tier_1_relaxed",
    "primary_metric": "mean_abs_norm_gap",
    "mean_abs_norm_gap": mean_gap,
    "max_abs_norm_gap": max_gap,
    "verdict": verdict,
    "catastrophic_failure": verdict == "destructive_failure"
}

out_json = OUTDIR / "abell1689_first_score.json"
with open(out_json, "w") as f:
    json.dump(result, f, indent=2)

print("Saved:", out_json)
print(json.dumps(result, indent=2))

from pathlib import Path
import json

OUT = Path("/content/Round15/challenge15_scoreable/abell1689_score_interpretation.json")

interpretation = {
    "system_name": "Abell 1689",
    "challenge": 15,
    "prototype_stage": "first_score_attempt",
    "scientific_interpretation": "invalid_for_claim",
    "reason": [
        "sparse manual extraction",
        "placeholder-level proxy values",
        "insufficient radial sampling",
        "proxy-vs-proxy comparison rather than full frozen scaffold evaluation"
    ],
    "action": "densify temperature and projected_mass curves before any pass/fail judgment"
}

OUT.write_text(json.dumps(interpretation, indent=2))
print(f"Saved: {OUT}")
print(json.dumps(interpretation, indent=2))
