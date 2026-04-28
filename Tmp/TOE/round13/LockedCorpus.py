from pathlib import Path
import pandas as pd
import numpy as np

LOCK_PATH = Path("/content/round12_test_set_locked_strict.csv")
IN_DIR = Path("/content/unseen_galaxy_csvs_strict")
OUT_PATH = Path("/content/round13_locked_corpus.csv")

locked = pd.read_csv(LOCK_PATH)

rows = []

for _, r in locked.iterrows():
    galaxy = r["galaxy"]
    source = r["source"]
    fn = r["csv_filename"]

    df = pd.read_csv(IN_DIR / fn).copy()
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Rad", "Vobs", "sd_proxy"]).copy()
    df = df.sort_values("Rad").reset_index(drop=True)

    if len(df) < 3:
        continue

    # Build a gas-only baryonic proxy layer from public WALLABY data
    # We only have HI-like profile support here, so:
    # - Vgas := cumulative/support-derived proxy
    # - Vdisk := 0 for now
    # - Vbul := 0 for now
    # - Mgas_total := simple profile integral proxy
    # - stellar masses remain 0 in this pilot corpus

    rad = df["Rad"].to_numpy(float)
    vobs = df["Vobs"].to_numpy(float)
    sd = np.maximum(df["sd_proxy"].to_numpy(float), 0.0)

    cum_sd = np.cumsum(sd)
    cum_sd_norm = cum_sd / cum_sd.max() if cum_sd.max() > 0 else np.zeros_like(cum_sd)

    vmax2 = np.nanmax(vobs**2)
    vgas = np.sqrt(np.maximum(cum_sd_norm * vmax2, 0.0))

    # crude gas-mass proxy from radial integral of profile
    # this is only for the locked WALLABY gas-side pilot, not final baryonic mass
    if len(rad) > 1:
        dr = np.diff(rad, prepend=rad[0])
        dr[0] = np.nanmedian(np.diff(rad)) if len(rad) > 1 else 1.0
    else:
        dr = np.array([1.0])

    mgas_proxy = float(np.nansum(sd * np.maximum(rad, 0.0) * np.maximum(dr, 0.0)))
    mstar_disk_proxy = 0.0
    mstar_bul_proxy = 0.0

    out = pd.DataFrame({
        "galaxy": galaxy,
        "source": source,
        "Rad": rad,
        "Vobs": vobs,
        "Vgas": vgas,
        "Vdisk": np.zeros_like(rad),
        "Vbul": np.zeros_like(rad),
        "Mgas_total": mgas_proxy,
        "Mstar_disk_total": mstar_disk_proxy,
        "Mstar_bul_total": mstar_bul_proxy,
        "notes": "round13a_wallaby_gas_side_locked_corpus"
    })

    rows.append(out)

if not rows:
    raise RuntimeError("No usable galaxies found to build round13_locked_corpus.csv")

corpus = pd.concat(rows, ignore_index=True)
corpus.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("\nColumns:")
print(list(corpus.columns))
print("\nGalaxy counts:")
print(corpus.groupby("galaxy").size().to_string())
print("\nPreview:")
print(corpus.head(20).to_string(index=False))
