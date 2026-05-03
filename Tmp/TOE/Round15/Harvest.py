from pathlib import Path
import pandas as pd

HARVEST = Path("/content/Round15/challenge15_harvest/challenge15_data_harvest_template.csv")
df = pd.read_csv(HARVEST)

mask = df["system_name"] == "Abell 1689"

df.loc[mask, "gas_source_paper"] = "Xue & Wu 2002; Tchernin et al. 2015; CHEX-MATE 2025"
df.loc[mask, "gas_source_url"] = "local_downloaded_pdfs"
df.loc[mask, "gas_product_type"] = "xray_gas_profile_or_recoverable_profile"
df.loc[mask, "gas_file_local"] = "/content/Round15/challenge15_sources/abell1689/"
df.loc[mask, "gas_units"] = "to_be_extracted"
df.loc[mask, "gas_geometry_notes"] = "Downloaded candidate X-ray / multiprobe sources for Abell 1689."

df.loc[mask, "mass_source_paper"] = "Halkola et al. 2006; Coe et al. 2010"
df.loc[mask, "mass_source_url"] = "local_downloaded_pdfs"
df.loc[mask, "mass_product_type"] = "radial_lensing_mass_profile_or_recoverable_profile"
df.loc[mask, "mass_file_local"] = "/content/Round15/challenge15_sources/abell1689/"
df.loc[mask, "mass_units"] = "to_be_extracted"
df.loc[mask, "mass_geometry_notes"] = "Downloaded candidate strong+weak lensing mass-profile sources for Abell 1689."

df.loc[mask, "status"] = "downloaded"
df.loc[mask, "notes_working"] = "Abell 1689 source papers downloaded locally; next step is profile extraction / mapping."

df.to_csv(HARVEST, index=False)
print(df[df["system_name"] == "Abell 1689"].to_string(index=False))
