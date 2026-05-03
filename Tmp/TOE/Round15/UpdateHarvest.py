from pathlib import Path
import pandas as pd

HARVEST = Path("/content/Round15/challenge15_harvest/challenge15_data_harvest_template.csv")
df = pd.read_csv(HARVEST)

mask = df["system_name"] == "Abell 1689"

df.loc[mask, "gas_source_paper"] = "Tchernin et al. 2015"
df.loc[mask, "gas_product_type"] = "radial_xray_profile_family"
df.loc[mask, "gas_units"] = "R[kpc] with emissivity/temperature profile"
df.loc[mask, "gas_geometry_notes"] = (
    "Primary gas source locked. Page 4 shows emissivity vs R[kpc]; "
    "page 5 shows temperature profile vs R[kpc]; page 7 confirms "
    "emissivity, density, and temperature profile family."
)

df.loc[mask, "mass_source_paper"] = "Halkola et al. 2006"
df.loc[mask, "mass_product_type"] = "radial_total_mass_profile"
df.loc[mask, "mass_units"] = "projected mass / shear radial profile"
df.loc[mask, "mass_geometry_notes"] = (
    "Primary mass source locked. Page 16 shows radial profile of total mass; "
    "page 17 shows tangential shear profile; page 18 provides parameter support."
)

df.loc[mask, "profile_radius_col"] = "R_kpc_manual_extract"
df.loc[mask, "profile_gas_col"] = "gas_profile_manual_extract"
df.loc[mask, "profile_mass_col"] = "mass_profile_manual_extract"

df.loc[mask, "distance_or_scale_info"] = "shared radial scale in kpc required after digitization"
df.loc[mask, "coordinate_frame"] = "radial_profile_space"
df.loc[mask, "registration_needed"] = "manual digitization and radius alignment required"

df.loc[mask, "status"] = "mapped_candidate"
df.loc[mask, "notes_working"] = (
    "Primary gas and mass profile PDFs locked with page-level anchors. "
    "Next step: digitize profile curves/tables into local CSV on shared radial scale."
)

df.to_csv(HARVEST, index=False)

print(df[df["system_name"] == "Abell 1689"][[
    "system_name", "status", "gas_source_paper", "mass_source_paper",
    "profile_radius_col", "profile_gas_col", "profile_mass_col",
    "notes_working"
]].to_string(index=False))
print("\nUpdated:", HARVEST)

from pathlib import Path
import pandas as pd

HARVEST = Path("/content/Round15/challenge15_harvest/challenge15_data_harvest_template.csv")
df = pd.read_csv(HARVEST)

string_cols = [
    "gas_source_paper", "gas_source_url", "gas_product_type", "gas_file_local",
    "gas_units", "gas_geometry_notes",
    "mass_source_paper", "mass_source_url", "mass_product_type", "mass_file_local",
    "mass_units", "mass_geometry_notes",
    "profile_radius_col", "profile_gas_col", "profile_mass_col",
    "map_x_col", "map_y_col", "map_gas_col", "map_mass_col",
    "distance_or_scale_info", "coordinate_frame", "registration_needed",
    "priority_rank", "status", "notes_working", "next_action"
]

for c in string_cols:
    if c in df.columns:
        df[c] = df[c].fillna("").astype(str)

df.to_csv(HARVEST, index=False)

print("Normalized string columns in:", HARVEST)
print(df[df["system_name"] == "Abell 1689"][[
    "system_name", "status", "profile_radius_col", "profile_gas_col",
    "profile_mass_col", "distance_or_scale_info", "coordinate_frame",
    "registration_needed"
]].to_string(index=False))

from pathlib import Path
import pandas as pd

OUTDIR = Path("/content/Round15/challenge15_sources/abell1689")
OUTDIR.mkdir(parents=True, exist_ok=True)

gas = pd.DataFrame({
    "R_kpc_manual_extract": [],
    "gas_profile_manual_extract": [],
    "gas_profile_kind": [],   # emissivity, temperature, density
    "source_pdf": [],
    "source_page": [],
    "notes": []
})

mass = pd.DataFrame({
    "R_kpc_manual_extract": [],
    "mass_profile_manual_extract": [],
    "mass_profile_kind": [],  # projected_mass, tangential_shear
    "source_pdf": [],
    "source_page": [],
    "notes": []
})

gas_path = OUTDIR / "abell1689_gas_profile_manual.csv"
mass_path = OUTDIR / "abell1689_mass_profile_manual.csv"

gas.to_csv(gas_path, index=False)
mass.to_csv(mass_path, index=False)

print("Saved:")
print(gas_path)
print(mass_path)
print("\nGas template columns:", list(gas.columns))
print("Mass template columns:", list(mass.columns))
