from pathlib import Path
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List

# =========================================
# ROUND 13 CONFIG
# =========================================

@dataclass
class Round13Config:
    corpus_csv: str = "/content/round13_locked_corpus.csv"
    output_dir: str = "/content/round13_results"
    catastrophic_rmse_threshold: float = -10.0

    # V_flat extraction
    vflat_outer_frac_start: float = 0.70   # use outer 30% of valid radii
    min_outer_points: int = 3

    # BTFR fitting
    btfr_log_base: float = 10.0

    # RAR safeguards
    eps: float = 1e-12

CFG = Round13Config()
Path(CFG.output_dir).mkdir(parents=True, exist_ok=True)

# =========================================
# REQUIRED INPUT CONTRACT
# =========================================
# Expected locked corpus columns (one row per radial point):
#
# galaxy
# source
# Rad
# Vobs
# Vgas
# Vdisk
# Vbul
# Mgas_total        (can repeat per row within galaxy)
# Mstar_disk_total  (can repeat per row within galaxy)
# Mstar_bul_total   (can repeat per row within galaxy)
#
# Optional:
# quality_flag
# survey
# notes

REQUIRED_COLS = [
    "galaxy", "Rad", "Vobs", "Vgas", "Vdisk", "Vbul",
    "Mgas_total", "Mstar_disk_total", "Mstar_bul_total"
]

# =========================================
# HELPERS
# =========================================

def rmse(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2))) if np.any(m) else np.nan

def signed_baryonic_velocity(vgas, vdisk, vbul):
    vbar2 = np.sign(vgas) * (vgas ** 2) + vdisk ** 2 + vbul ** 2
    vbar2 = np.maximum(vbar2, 0.0)
    return np.sqrt(vbar2)

def extract_vflat(rad, vel, outer_frac_start=0.70, min_outer_points=3):
    rad = np.asarray(rad, float)
    vel = np.asarray(vel, float)
    m = np.isfinite(rad) & np.isfinite(vel)
    rad = rad[m]
    vel = vel[m]
    if len(rad) == 0:
        return np.nan

    order = np.argsort(rad)
    rad = rad[order]
    vel = vel[order]

    start_idx = int(np.floor(outer_frac_start * len(rad)))
    start_idx = min(start_idx, max(len(rad) - min_outer_points, 0))
    outer = vel[start_idx:]

    if len(outer) < min_outer_points:
        outer = vel[-min_outer_points:] if len(vel) >= min_outer_points else vel

    return float(np.nanmedian(outer)) if len(outer) else np.nan

def total_baryonic_mass(df_gal):
    mgas = float(df_gal["Mgas_total"].dropna().iloc[0]) if df_gal["Mgas_total"].notna().any() else np.nan
    mdisk = float(df_gal["Mstar_disk_total"].dropna().iloc[0]) if df_gal["Mstar_disk_total"].notna().any() else np.nan
    mbul = float(df_gal["Mstar_bul_total"].dropna().iloc[0]) if df_gal["Mstar_bul_total"].notna().any() else np.nan
    parts = [x for x in [mgas, mdisk, mbul] if np.isfinite(x)]
    return float(np.sum(parts)) if parts else np.nan

def compute_accelerations(rad, vel, eps=1e-12):
    rad = np.asarray(rad, float)
    vel = np.asarray(vel, float)
    return (vel ** 2) / np.maximum(rad, eps)

def safe_log10(x):
    x = np.asarray(x, float)
    out = np.full_like(x, np.nan, dtype=float)
    m = x > 0
    out[m] = np.log10(x[m])
    return out

# =========================================
# PLACEHOLDER MODEL HOOK
# =========================================
# Replace this with your frozen Round 13 Bridge model.
# For now it uses the baryonic baseline as a placeholder.

def compute_bridge_prediction(df_gal: pd.DataFrame) -> pd.DataFrame:
    out = df_gal.copy()
    out["Vbar"] = signed_baryonic_velocity(
        out["Vgas"].to_numpy(float),
        out["Vdisk"].to_numpy(float),
        out["Vbul"].to_numpy(float),
    )
    # TODO: replace with frozen Bridge model prediction
    out["Vbridge"] = out["Vbar"]
    return out

# =========================================
# PER-GALAXY SCORING
# =========================================

def score_one_galaxy(df_gal: pd.DataFrame) -> Dict:
    df_gal = df_gal.copy()
    df_gal = df_gal.replace([np.inf, -np.inf], np.nan)
    df_gal = df_gal.dropna(subset=["Rad", "Vobs", "Vgas", "Vdisk", "Vbul"]).copy()
    df_gal = df_gal.sort_values("Rad").reset_index(drop=True)

    if len(df_gal) < 3:
        return {
            "galaxy": df_gal["galaxy"].iloc[0] if len(df_gal) else None,
            "n_points": len(df_gal),
            "rmse_baryonic": np.nan,
            "rmse_bridge": np.nan,
            "improvement": np.nan,
            "vflat_obs": np.nan,
            "vflat_bridge": np.nan,
            "m_baryon": np.nan,
            "catastrophic_failure": False,
            "usable": False,
        }

    out = compute_bridge_prediction(df_gal)

    rmse_bary = rmse(out["Vobs"], out["Vbar"])
    rmse_bridge = rmse(out["Vobs"], out["Vbridge"])
    improvement = rmse_bary - rmse_bridge

    vflat_obs = extract_vflat(out["Rad"], out["Vobs"], CFG.vflat_outer_frac_start, CFG.min_outer_points)
    vflat_bridge = extract_vflat(out["Rad"], out["Vbridge"], CFG.vflat_outer_frac_start, CFG.min_outer_points)
    m_baryon = total_baryonic_mass(out)

    g_obs = compute_accelerations(out["Rad"], out["Vobs"], CFG.eps)
    g_bar = compute_accelerations(out["Rad"], out["Vbar"], CFG.eps)
    g_bridge = compute_accelerations(out["Rad"], out["Vbridge"], CFG.eps)

    # Save radial detail
    radial = out.copy()
    radial["g_obs"] = g_obs
    radial["g_bar"] = g_bar
    radial["g_bridge"] = g_bridge
    safe_name = str(out["galaxy"].iloc[0]).lower().replace(" ", "_").replace("/", "_")
    radial.to_csv(Path(CFG.output_dir) / f"{safe_name}_radial_detail.csv", index=False)

    return {
        "galaxy": out["galaxy"].iloc[0],
        "n_points": len(out),
        "rmse_baryonic": rmse_bary,
        "rmse_bridge": rmse_bridge,
        "improvement": improvement,
        "vflat_obs": vflat_obs,
        "vflat_bridge": vflat_bridge,
        "m_baryon": m_baryon,
        "log10_vflat_obs": float(safe_log10(np.array([vflat_obs]))[0]) if np.isfinite(vflat_obs) else np.nan,
        "log10_vflat_bridge": float(safe_log10(np.array([vflat_bridge]))[0]) if np.isfinite(vflat_bridge) else np.nan,
        "log10_m_baryon": float(safe_log10(np.array([m_baryon]))[0]) if np.isfinite(m_baryon) else np.nan,
        "catastrophic_failure": bool(improvement < CFG.catastrophic_rmse_threshold),
        "usable": True,
    }

# =========================================
# BTFR FIT
# =========================================

def fit_btfr(df_summary: pd.DataFrame, v_col: str) -> Dict:
    sub = df_summary[["log10_m_baryon", v_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "slope": np.nan, "intercept": np.nan, "scatter_rmse": np.nan}

    # Fit log10(Vflat) = a * log10(Mb) + b
    x = sub["log10_m_baryon"].to_numpy(float)
    y = sub[v_col].to_numpy(float)
    a, b = np.polyfit(x, y, 1)
    yhat = a * x + b
    scatter = float(np.sqrt(np.mean((y - yhat) ** 2)))

    return {"n": len(sub), "slope": float(a), "intercept": float(b), "scatter_rmse": scatter}

# =========================================
# RAR PREP
# =========================================

def build_rar_points(corpus: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for galaxy, g in corpus.groupby("galaxy", sort=True):
        out = compute_bridge_prediction(g)
        out = out.replace([np.inf, -np.inf], np.nan).dropna(subset=["Rad", "Vobs", "Vbar", "Vbridge"]).copy()
        if len(out) == 0:
            continue

        g_obs = compute_accelerations(out["Rad"], out["Vobs"], CFG.eps)
        g_bar = compute_accelerations(out["Rad"], out["Vbar"], CFG.eps)
        g_bridge = compute_accelerations(out["Rad"], out["Vbridge"], CFG.eps)

        tmp = pd.DataFrame({
            "galaxy": galaxy,
            "Rad": out["Rad"].to_numpy(float),
            "g_obs": g_obs,
            "g_bar": g_bar,
            "g_bridge": g_bridge,
            "log10_g_obs": safe_log10(g_obs),
            "log10_g_bar": safe_log10(g_bar),
            "log10_g_bridge": safe_log10(g_bridge),
        })
        rows.append(tmp)

    if not rows:
        return pd.DataFrame()

    rar = pd.concat(rows, ignore_index=True)
    rar.to_csv(Path(CFG.output_dir) / "round13_rar_points.csv", index=False)
    return rar

def rar_scatter(rar: pd.DataFrame, pred_col: str = "log10_g_bridge") -> Dict:
    sub = rar[["log10_g_obs", pred_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "scatter_rmse": np.nan}

    scatter = float(np.sqrt(np.mean((sub["log10_g_obs"] - sub[pred_col]) ** 2)))
    return {"n": len(sub), "scatter_rmse": scatter}

# =========================================
# MAIN
# =========================================

def run_round13():
    corpus = pd.read_csv(CFG.corpus_csv)
    missing = [c for c in REQUIRED_COLS if c not in corpus.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    summaries = []
    for galaxy, g in corpus.groupby("galaxy", sort=True):
        summaries.append(score_one_galaxy(g))

    summary = pd.DataFrame(summaries)
    summary.to_csv(Path(CFG.output_dir) / "round13_per_galaxy_summary.csv", index=False)

    valid = summary["usable"] == True
    positive_rate = float((summary.loc[valid, "improvement"] > 0).mean()) if valid.any() else np.nan
    mean_improvement = float(summary.loc[valid, "improvement"].mean()) if valid.any() else np.nan
    catastrophic_failures = int(summary.loc[valid, "catastrophic_failure"].sum()) if valid.any() else 0

    btfr_obs = fit_btfr(summary.loc[valid].copy(), "log10_vflat_obs")
    btfr_bridge = fit_btfr(summary.loc[valid].copy(), "log10_vflat_bridge")

    rar = build_rar_points(corpus)
    rar_bar = rar_scatter(rar, "log10_g_bar") if len(rar) else {"n": 0, "scatter_rmse": np.nan}
    rar_bridge = rar_scatter(rar, "log10_g_bridge") if len(rar) else {"n": 0, "scatter_rmse": np.nan}

    aggregate = {
        "n_galaxies_total": int(len(summary)),
        "n_galaxies_usable": int(valid.sum()),
        "positive_improvement_rate": positive_rate,
        "mean_rmse_improvement": mean_improvement,
        "catastrophic_failures": catastrophic_failures,
        "btfr_obs": btfr_obs,
        "btfr_bridge": btfr_bridge,
        "rar_baryonic": rar_bar,
        "rar_bridge": rar_bridge,
    }

    pd.Series({"aggregate_json": str(aggregate)}).to_csv(
        Path(CFG.output_dir) / "round13_aggregate_summary.csv", index=False
    )

    print(summary.to_string(index=False))
    print("\nAggregate:")
    print(aggregate)

if __name__ == "__main__":
    run_round13()
