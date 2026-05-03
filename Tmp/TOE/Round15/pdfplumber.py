!pip install -q pdfplumber
from pathlib import Path
import re
import pandas as pd
import pdfplumber

SRC = Path("/content/Round15/challenge15_sources/abell1689")
OUT = Path("/content/Round15/challenge15_sources/abell1689_extraction")
OUT.mkdir(parents=True, exist_ok=True)

pdfs = sorted(SRC.glob("*.pdf"))
rows = []

keywords = [
    "table", "profile", "radial", "radius", "mass profile", "surface density",
    "convergence", "shear", "x-ray", "electron density", "temperature",
    "entropy", "pressure", "projected mass", "weak lensing", "strong lensing"
]

for pdf in pdfs:
    try:
        with pdfplumber.open(pdf) as doc:
            n_pages = len(doc.pages)
            for i, page in enumerate(doc.pages):
                text = page.extract_text() or ""
                text_l = text.lower()
                hits = [k for k in keywords if k in text_l]
                if hits:
                    snippet = re.sub(r"\s+", " ", text)[:500]
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
out_csv = OUT / "abell1689_pdf_keyword_scan.csv"
df.to_csv(out_csv, index=False)

print("Saved:", out_csv)
print(df.head(50).to_string(index=False))

from pathlib import Path
import pdfplumber
import pandas as pd

PDF = Path("/content/Round15/challenge15_sources/abell1689/abell1689_strong_weak_lensing_halkola_2006.pdf")  # change as needed
PAGES = [1,2,3,4,5,6,7,8,9,10]  # adjust after keyword scan

rows = []
with pdfplumber.open(PDF) as doc:
    for pno in PAGES:
        if pno <= len(doc.pages):
            page = doc.pages[pno - 1]
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                if table:
                    temp = pd.DataFrame(table)
                    temp["source_page"] = pno
                    temp["table_index"] = t_idx
                    rows.append(temp)

if rows:
    out = pd.concat(rows, ignore_index=True)
    out_path = Path("/content/Round15/challenge15_sources/abell1689_extraction/extracted_tables_preview.csv")
    out.to_csv(out_path, index=False)
    print("Saved:", out_path)
    print(out.head(40).to_string(index=False))
else:
    print("No tables extracted. Use text/snippet review to identify figure/table pages first.")

