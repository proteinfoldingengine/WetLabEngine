from pathlib import Path
import pandas as pd

gas_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
mass_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")

temp_r = [120, 180, 240, 300, 380, 460, 540, 620, 700, 800]
pmass_r = [50, 80, 110, 140, 170, 200, 240, 280, 320, 380]

gas = pd.DataFrame({
    "R_kpc_manual_extract": temp_r,
    "gas_profile_manual_extract": [None] * len(temp_r),
    "gas_profile_kind": ["temperature"] * len(temp_r),
    "source_pdf": ["abell1689_projected_potential_xray_2015.pdf"] * len(temp_r),
    "source_page": [5] * len(temp_r),
    "notes": ["densified target row from page 5"] * len(temp_r),
})

mass = pd.DataFrame({
    "R_kpc_manual_extract": pmass_r,
    "mass_profile_manual_extract": [None] * len(pmass_r),
    "mass_profile_kind": ["projected_mass"] * len(pmass_r),
    "source_pdf": ["abell1689_strong_weak_lensing_halkola_2006.pdf"] * len(pmass_r),
    "source_page": [16] * len(pmass_r),
    "notes": ["densified target row from page 16"] * len(pmass_r),
})

gas.to_csv(gas_path, index=False)
mass.to_csv(mass_path, index=False)

print("Saved densified templates:")
print(gas_path)
print(mass_path)
print("\nGas template:")
print(gas.to_string(index=False))
print("\nMass template:")
print(mass.to_string(index=False))

import pandas as pd
from pathlib import Path

gas_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
mass_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")

gas = pd.read_csv(gas_path)
mass = pd.read_csv(mass_path)

# TEMPORARY prototype fill from approximate visual trend only
# Replace later with better manual read-offs from the figures.

gas_values = {
    120: 9.7,
    180: 9.4,
    240: 9.1,
    300: 8.8,
    380: 8.6,
    460: 8.4,
    540: 8.7,
    620: 9.0,
    700: 9.4,
    800: 9.8,
}

mass_values = {
    50: 1.5e14,
    80: 2.2e14,
    110: 3.0e14,
    140: 3.9e14,
    170: 4.8e14,
    200: 5.7e14,
    240: 6.8e14,
    280: 7.7e14,
    320: 8.5e14,
    380: 9.3e14,
}

for r, v in gas_values.items():
    gas.loc[gas["R_kpc_manual_extract"] == r, "gas_profile_manual_extract"] = v
    gas.loc[gas["R_kpc_manual_extract"] == r, "notes"] = "temporary prototype fill; replace with better manual read-off"

for r, v in mass_values.items():
    mass.loc[mass["R_kpc_manual_extract"] == r, "mass_profile_manual_extract"] = v
    mass.loc[mass["R_kpc_manual_extract"] == r, "notes"] = "temporary prototype fill; replace with better manual read-off"

gas.to_csv(gas_path, index=False)
mass.to_csv(mass_path, index=False)

print("Updated gas:")
print(gas.to_string(index=False))
print("\nUpdated mass:")
print(mass.to_string(index=False))

from pathlib import Path
import pandas as pd
import numpy as np
import json

GAS = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
MASS = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")
OUTDIR = Path("/content/Round15/challenge15_scoreable")
OUTDIR.mkdir(parents=True, exist_ok=True)

gas = pd.read_csv(GAS)
mass = pd.read_csv(MASS)

gas = gas[gas["gas_profile_kind"] == "temperature"].dropna(subset=["R_kpc_manual_extract", "gas_profile_manual_extract"]).copy()
mass = mass[mass["mass_profile_kind"] == "projected_mass"].dropna(subset=["R_kpc_manual_extract", "mass_profile_manual_extract"]).copy()

gas = gas.sort_values("R_kpc_manual_extract")
mass = mass.sort_values("R_kpc_manual_extract")

print("Filled gas points:", len(gas))
print("Filled mass points:", len(mass))

rmin = max(gas["R_kpc_manual_extract"].min(), mass["R_kpc_manual_extract"].min())
rmax = min(gas["R_kpc_manual_extract"].max(), mass["R_kpc_manual_extract"].max())

if rmax <= rmin:
    raise ValueError("No overlapping radial range.")

shared_r = np.linspace(rmin, rmax, 12)

gas_interp = np.interp(shared_r, gas["R_kpc_manual_extract"], gas["gas_profile_manual_extract"])
mass_interp = np.interp(shared_r, mass["R_kpc_manual_extract"], mass["mass_profile_manual_extract"])

scoreable = pd.DataFrame({
    "system_name": "Abell 1689",
    "R_kpc": shared_r,
    "temperature_keV_proxy": gas_interp,
    "projected_mass_proxy": mass_interp
})

scoreable["temperature_norm"] = scoreable["temperature_keV_proxy"] / scoreable["temperature_keV_proxy"].max()
scoreable["projected_mass_norm"] = scoreable["projected_mass_proxy"] / scoreable["projected_mass_proxy"].max()
scoreable["abs_norm_gap"] = (scoreable["temperature_norm"] - scoreable["projected_mass_norm"]).abs()

scoreable_path = OUTDIR / "abell1689_scoreable_profile_densified.csv"
scoreable.to_csv(scoreable_path, index=False)

mean_gap = float(scoreable["abs_norm_gap"].mean())
max_gap = float(scoreable["abs_norm_gap"].max())

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
    "prototype_stage": "densified_first_pass",
    "primary_metric": "mean_abs_norm_gap",
    "mean_abs_norm_gap": mean_gap,
    "max_abs_norm_gap": max_gap,
    "n_gas_points": int(len(gas)),
    "n_mass_points": int(len(mass)),
    "shared_r_min_kpc": float(rmin),
    "shared_r_max_kpc": float(rmax),
    "verdict": verdict,
    "catastrophic_failure": verdict == "destructive_failure",
    "interpretation_guardrail": "temporary prototype values only; not valid for final scientific claim"
}

result_path = OUTDIR / "abell1689_densified_score.json"
with open(result_path, "w") as f:
    json.dump(result, f, indent=2)

print("Saved:")
print(scoreable_path)
print(result_path)
print("\nScoreable profile:")
print(scoreable.to_string(index=False))
print("\nResult:")
print(json.dumps(result, indent=2))

from pathlib import Path
import pandas as pd
import json

HARVEST = Path("/content/Round15/challenge15_harvest/challenge15_data_harvest_template.csv")
RESULT = Path("/content/Round15/challenge15_scoreable/abell1689_densified_score.json")

df = pd.read_csv(HARVEST)
result = json.loads(RESULT.read_text())

mask = df["system_name"] == "Abell 1689"

df.loc[mask, "notes_working"] = (
    f"Densified prototype scored: verdict={result['verdict']}, "
    f"mean_abs_norm_gap={result['mean_abs_norm_gap']:.4f}, "
    f"n_gas_points={result['n_gas_points']}, n_mass_points={result['n_mass_points']}. "
    "Temporary prototype values only."
)

df.loc[mask, "status"] = "ready_to_score"

df.to_csv(HARVEST, index=False)

print(df[df["system_name"] == "Abell 1689"][["system_name", "status", "notes_working"]].to_string(index=False))

from pathlib import Path
import json

OUT = Path("/content/Round15/challenge15_scoreable/abell1689_prototype_classification.json")

payload = {
    "system_name": "Abell 1689",
    "challenge": 15,
    "prototype_status": "weak_negative_not_claimable",
    "reason": [
        "temporary prototype values",
        "manual extraction still approximate",
        "first Tier 1 mapping only",
        "insufficient basis for frozen-scaffold judgment"
    ],
    "recommended_next_step": "start Abell 1835 while later refining A1689 extraction once"
}

OUT.write_text(json.dumps(payload, indent=2))
print(f"Saved: {OUT}")
print(json.dumps(payload, indent=2))
