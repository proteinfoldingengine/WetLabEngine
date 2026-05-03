from pathlib import Path
import pandas as pd

gas_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
mass_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")

gas_seed = pd.DataFrame([
    {
        "R_kpc_manual_extract": 120,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "emissivity",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 4,
        "notes": "starter row; replace with approximate digitized value from page 4"
    },
    {
        "R_kpc_manual_extract": 300,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "emissivity",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 4,
        "notes": "starter row; replace with approximate digitized value from page 4"
    },
    {
        "R_kpc_manual_extract": 800,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "emissivity",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 4,
        "notes": "starter row; replace with approximate digitized value from page 4"
    },
    {
        "R_kpc_manual_extract": 120,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "temperature",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 5,
        "notes": "starter row; replace with approximate digitized value from page 5"
    },
    {
        "R_kpc_manual_extract": 300,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "temperature",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 5,
        "notes": "starter row; replace with approximate digitized value from page 5"
    },
    {
        "R_kpc_manual_extract": 800,
        "gas_profile_manual_extract": "",
        "gas_profile_kind": "temperature",
        "source_pdf": "abell1689_projected_potential_xray_2015.pdf",
        "source_page": 5,
        "notes": "starter row; replace with approximate digitized value from page 5"
    },
])

mass_seed = pd.DataFrame([
    {
        "R_kpc_manual_extract": 50,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "projected_mass",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 16,
        "notes": "starter row; replace with approximate digitized value from page 16"
    },
    {
        "R_kpc_manual_extract": 150,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "projected_mass",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 16,
        "notes": "starter row; replace with approximate digitized value from page 16"
    },
    {
        "R_kpc_manual_extract": 300,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "projected_mass",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 16,
        "notes": "starter row; replace with approximate digitized value from page 16"
    },
    {
        "R_kpc_manual_extract": 100,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "tangential_shear",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 17,
        "notes": "starter row; replace with approximate digitized value from page 17"
    },
    {
        "R_kpc_manual_extract": 300,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "tangential_shear",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 17,
        "notes": "starter row; replace with approximate digitized value from page 17"
    },
    {
        "R_kpc_manual_extract": 700,
        "mass_profile_manual_extract": "",
        "mass_profile_kind": "tangential_shear",
        "source_pdf": "abell1689_strong_weak_lensing_halkola_2006.pdf",
        "source_page": 17,
        "notes": "starter row; replace with approximate digitized value from page 17"
    },
])

gas_seed.to_csv(gas_path, index=False)
mass_seed.to_csv(mass_path, index=False)

print("Gas seed:")
print(gas_seed.to_string(index=False))
print("\nMass seed:")
print(mass_seed.to_string(index=False))

from pathlib import Path
import pandas as pd

gas = pd.read_csv("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
mass = pd.read_csv("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")

print("Gas non-empty values:", gas["gas_profile_manual_extract"].replace("", pd.NA).notna().sum())
print("Mass non-empty values:", mass["mass_profile_manual_extract"].replace("", pd.NA).notna().sum())

print("\nGas preview:")
print(gas.to_string(index=False))

print("\nMass preview:")
print(mass.to_string(index=False))

from pathlib import Path
import fitz  # PyMuPDF

jobs = [
    {
        "pdf": "/content/Round15/challenge15_sources/abell1689/abell1689_projected_potential_xray_2015.pdf",
        "pages": [4, 5],
        "prefix": "a1689_gas"
    },
    {
        "pdf": "/content/Round15/challenge15_sources/abell1689/abell1689_strong_weak_lensing_halkola_2006.pdf",
        "pages": [16, 17],
        "prefix": "a1689_mass"
    }
]

outdir = Path("/content/Round15/challenge15_sources/abell1689/page_images")
outdir.mkdir(parents=True, exist_ok=True)

for job in jobs:
    doc = fitz.open(job["pdf"])
    for p in job["pages"]:
        page = doc[p - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), alpha=False)
        out = outdir / f"{job['prefix']}_page_{p}.png"
        pix.save(str(out))
        print("Saved:", out)

import pandas as pd
from pathlib import Path

gas_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_gas_profile_manual.csv")
mass_path = Path("/content/Round15/challenge15_sources/abell1689/abell1689_mass_profile_manual.csv")

gas = pd.read_csv(gas_path)
mass = pd.read_csv(mass_path)

# Replace these with your approximate reads from the PNGs
gas.loc[(gas["gas_profile_kind"] == "emissivity") & (gas["R_kpc_manual_extract"] == 120), "gas_profile_manual_extract"] = 3e-12
gas.loc[(gas["gas_profile_kind"] == "emissivity") & (gas["R_kpc_manual_extract"] == 300), "gas_profile_manual_extract"] = 6e-13
gas.loc[(gas["gas_profile_kind"] == "emissivity") & (gas["R_kpc_manual_extract"] == 800), "gas_profile_manual_extract"] = 8e-15

gas.loc[(gas["gas_profile_kind"] == "temperature") & (gas["R_kpc_manual_extract"] == 120), "gas_profile_manual_extract"] = 9.5
gas.loc[(gas["gas_profile_kind"] == "temperature") & (gas["R_kpc_manual_extract"] == 300), "gas_profile_manual_extract"] = 8.8
gas.loc[(gas["gas_profile_kind"] == "temperature") & (gas["R_kpc_manual_extract"] == 800), "gas_profile_manual_extract"] = 10.0

mass.loc[(mass["mass_profile_kind"] == "projected_mass") & (mass["R_kpc_manual_extract"] == 50), "mass_profile_manual_extract"] = 1.5e14
mass.loc[(mass["mass_profile_kind"] == "projected_mass") & (mass["R_kpc_manual_extract"] == 150), "mass_profile_manual_extract"] = 4.5e14
mass.loc[(mass["mass_profile_kind"] == "projected_mass") & (mass["R_kpc_manual_extract"] == 300), "mass_profile_manual_extract"] = 8.0e14

mass.loc[(mass["mass_profile_kind"] == "tangential_shear") & (mass["R_kpc_manual_extract"] == 100), "mass_profile_manual_extract"] = 0.22
mass.loc[(mass["mass_profile_kind"] == "tangential_shear") & (mass["R_kpc_manual_extract"] == 300), "mass_profile_manual_extract"] = 0.12
mass.loc[(mass["mass_profile_kind"] == "tangential_shear") & (mass["R_kpc_manual_extract"] == 700), "mass_profile_manual_extract"] = 0.05

gas.to_csv(gas_path, index=False)
mass.to_csv(mass_path, index=False)

print("Updated gas:")
print(gas.to_string(index=False))
print("\nUpdated mass:")
print(mass.to_string(index=False))
