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
