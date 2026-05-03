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
