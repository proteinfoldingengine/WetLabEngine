%%bash
mkdir -p /content/Round15/challenge15_sources/abell1835
cd /content/Round15/challenge15_sources/abell1835

# Gas / X-ray / hydrostatic candidates
wget -O abell1835_chandra_schmidt_2001.pdf https://arxiv.org/pdf/astro-ph/0107438
wget -O abell1835_chandra_allen_2002.pdf https://arxiv.org/pdf/astro-ph/0205007
wget -O abell1835_xray_mass_2006.pdf https://arxiv.org/pdf/astro-ph/0510182

# Lensing / total-mass candidates
wget -O abell1835_wl_cfht_2006.pdf https://arxiv.org/pdf/astro-ph/0509252
wget -O abell1835_cluster_lensing_2008.pdf https://arxiv.org/pdf/0802.2160

ls -lh

from pathlib import Path
import pandas as pd

HARVEST = Path("/content/Round15/challenge15_harvest/challenge15_data_harvest_template.csv")
df = pd.read_csv(HARVEST)

mask = df["system_name"] == "Abell 1835"

df.loc[mask, "gas_source_paper"] = "Schmidt et al. 2001; Allen et al. 2002; X-ray mass candidate 2006"
df.loc[mask, "gas_source_url"] = "local_downloaded_pdfs"
df.loc[mask, "gas_product_type"] = "xray_gas_profile_or_hydrostatic_profile_candidate"
df.loc[mask, "gas_file_local"] = "/content/Round15/challenge15_sources/abell1835/"
df.loc[mask, "gas_units"] = "to_be_extracted"
df.loc[mask, "gas_geometry_notes"] = "Downloaded Abell 1835 X-ray / hydrostatic candidate sources."

df.loc[mask, "mass_source_paper"] = "CFHT weak lensing 2006; cluster lensing candidate 2008"
df.loc[mask, "mass_source_url"] = "local_downloaded_pdfs"
df.loc[mask, "mass_product_type"] = "lensing_mass_profile_candidate"
df.loc[mask, "mass_file_local"] = "/content/Round15/challenge15_sources/abell1835/"
df.loc[mask, "mass_units"] = "to_be_extracted"
df.loc[mask, "mass_geometry_notes"] = "Downloaded Abell 1835 lensing candidate sources."

df.loc[mask, "status"] = "downloaded"
df.loc[mask, "notes_working"] = "Abell 1835 source papers downloaded locally; next step is keyword/page scan and source locking."

df.to_csv(HARVEST, index=False)

print(df[df["system_name"] == "Abell 1835"][[
    "system_name", "status", "gas_source_paper", "mass_source_paper", "notes_working"
]].to_string(index=False))
print("\nUpdated:", HARVEST)

from pathlib import Path
import re
import pandas as pd
import pdfplumber

SRC = Path("/content/Round15/challenge15_sources/abell1835")
OUT = Path("/content/Round15/challenge15_sources/abell1835_extraction")
OUT.mkdir(parents=True, exist_ok=True)

pdfs = sorted(SRC.glob("*.pdf"))
rows = []

keywords = [
    "table", "profile", "radial", "radius", "mass profile", "surface density",
    "convergence", "shear", "x-ray", "electron density", "temperature",
    "entropy", "pressure", "projected mass", "weak lensing", "strong lensing",
    "hydrostatic"
]

for pdf in pdfs:
    try:
        with pdfplumber.open(pdf) as doc:
            for i, page in enumerate(doc.pages):
                text = page.extract_text() or ""
                text_l = text.lower()
                hits = [k for k in keywords if k in text_l]
                if hits:
                    snippet = re.sub(r"\s+", " ", text)[:700]
                    rows.append({
                        "file": pdf.name,
                        "page": i + 1,
                        "keyword_hits": ", ".join(hits),
                        "snippet": snippet
                    })
    except Exception as e:
        rows.append({
            "file": pdf.name,
            "page": None,
            "keyword_hits": "ERROR",
            "snippet": str(e)
        })

df = pd.DataFrame(rows).sort_values(["file", "page"], na_position="last")
out_csv = OUT / "abell1835_pdf_keyword_scan.csv"
df.to_csv(out_csv, index=False)

print("Saved:", out_csv)
print(df.head(120).to_string(index=False))

from pathlib import Path
import pandas as pd

OUTDIR = Path("/content/Round15/challenge15_sources/abell1835")
OUTDIR.mkdir(parents=True, exist_ok=True)

gas = pd.DataFrame({
    "R_kpc_manual_extract": [],
    "gas_profile_manual_extract": [],
    "gas_profile_kind": [],
    "source_pdf": [],
    "source_page": [],
    "notes": []
})

mass = pd.DataFrame({
    "R_kpc_manual_extract": [],
    "mass_profile_manual_extract": [],
    "mass_profile_kind": [],
    "source_pdf": [],
    "source_page": [],
    "notes": []
})

gas_path = OUTDIR / "abell1835_gas_profile_manual.csv"
mass_path = OUTDIR / "abell1835_mass_profile_manual.csv"

gas.to_csv(gas_path, index=False)
mass.to_csv(mass_path, index=False)

print("Saved:")
print(gas_path)
print(mass_path)
