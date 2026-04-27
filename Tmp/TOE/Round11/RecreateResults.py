import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

# =========================
# CONFIG
# =========================
ROOT = Path(".")
OUT = ROOT / "round11_independent_verification"
OUT.mkdir(exist_ok=True)

GALAXIES = {
    "DDO154": {
        "folder": "things_ddo154",
        "refined_vs_sparc": "ddo154_refined_vs_sparc.csv",
        "gas_compare": "ddo154_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ddo154_bridge_external_gasproxy_pilot.csv",
            "ddo154_bridge_external_gas_disk_proxy_results.csv",
            "ddo154_bridge_external_gas_disk_proxy_results_smooth.csv",
        ],
        "recon_expected": None,
    },
    "NGC2403": {
        "folder": "things_ngc2403",
        "refined_vs_sparc": "ngc2403_refined_vs_sparc.csv",
        "gas_compare": "ngc2403_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ngc2403_bridge_external_gasproxy_pilot.csv",
            "ngc2403_bridge_external_gas_disk_proxy_pilot.csv",
            "ngc2403_bridge_external_gas_disk_proxy_pilot_smoothed.csv",
            "ngc2403_bridge_external_gas_disk_proxy_pilot_disknorm.csv",
        ],
        "recon_expected": None,
    },
    "NGC3198": {
        "folder": "things_ngc3198",
        "refined_vs_sparc": "ngc3198_refined_vs_sparc.csv",
        "gas_compare": "ngc3198_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ngc3198_bridge_external_gasproxy_pilot.csv",
        ],
        "recon_expected": None,
    },
    "NGC6946": {
        "folder": "things_ngc6946",
        "refined_vs_sparc": "ngc6946_refined_vs_sparc.csv",
        "gas_compare": "ngc6946_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ngc6946_bridge_external_gasproxy_pilot.csv",
            "ngc6946_bridge_external_gas_disk_proxy_pilot.csv",
            "ngc6946_bridge_external_gas_disk_proxy_pilot_smoothed.csv",
            "ngc6946_bridge_external_gas_disk_proxy_pilot_disknorm.csv",
        ],
        "extra_diag": [
            "ngc6946_nearfull_overcorrection_region_summary.csv",
            "ngc6946_disk_proxy_vs_sparc_region_summary.csv",
            "ngc6946_bridge_residual_budget_region_summary.csv",
        ],
        "recon_expected": None,
    },
    "NGC5055": {
        "folder": "things_ngc5055",
        "refined_vs_sparc": "ngc5055_refined_vs_sparc.csv",
        "gas_compare": "ngc5055_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ngc5055_bridge_external_gasproxy_pilot.csv",
        ],
        "extra_diag": [
            "ngc5055_gasside_residual_budget_region_summary.csv",
            "ngc5055_gas_proxy_vs_sparc_region_summary.csv",
            "ngc5055_residual_aware_ablation_region_summary.csv",
        ],
        "recon_expected": None,
    },
    "NGC2841": {
        "folder": "things_ngc2841",
        "refined_vs_sparc": "ngc2841_refined_vs_sparc.csv",
        "gas_compare": "ngc2841_external_cumgas_vs_sparc.csv",
        "gas_pilot": [
            "ngc2841_bridge_external_gasproxy_pilot.csv",
        ],
        "recon_expected": None,
    },
}

# Frozen Bridge parameters used in this audit
BRIDGE_PARAMS = dict(
    beta=1.1,
    L=3.5,
    gamma_curv=1.0,
    eta_signed=0.35,
    zeta_disk=0.5,
    gate_frac=0.85,
    gate_width_frac=0.15,
    alpha_s=0.08,
    alpha_f=0.35,
    eps=1e-9,
)

# =========================
# HELPERS
# =========================
def rmse(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    m = np.isfinite(a) & np.isfinite(b)
    if not np.any(m):
        return np.nan
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2)))

def mae(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    m = np.isfinite(a) & np.isfinite(b)
    if not np.any(m):
        return np.nan
    return float(np.mean(np.abs(a[m] - b[m])))

def corr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    m = np.isfinite(a) & np.isfinite(b)
    if np.sum(m) < 2:
        return np.nan
    return float(np.corrcoef(a[m], b[m])[0, 1])

def smooth_transfer(x, r, L, eps=1e-9):
    dr = np.abs(r[:, None] - r[None, :])
    K = np.exp(-dr / max(L, eps))
    K /= np.sum(K, axis=1, keepdims=True) + eps
    return K @ x

def compute_bridge(vobs, vgas, vdisk, vbul, r, params):
    beta = params["beta"]
    L = params["L"]
    gamma_curv = params["gamma_curv"]
    eta_signed = params["eta_signed"]
    zeta_disk = params["zeta_disk"]
    gate_frac = params["gate_frac"]
    gate_width_frac = params["gate_width_frac"]
    alpha_s = params["alpha_s"]
    alpha_f = params["alpha_f"]
    eps = params["eps"]

    vbar2 = np.sign(vgas) * (vgas ** 2) + vdisk ** 2 + vbul ** 2
    vbar2 = np.maximum(vbar2, 0.0)
    vbar = np.sqrt(vbar2)
    gbar = vbar2 / np.maximum(r, eps)

    disk_frac = (np.sign(vgas) * (vgas ** 2) + vdisk ** 2) / np.maximum(vbar2, eps)
    bulge_frac = (vbul ** 2) / np.maximum(vbar2, eps)
    component_weight = np.clip(disk_frac - 0.5 * bulge_frac, 0.0, 1.0)

    logg = np.log(np.maximum(gbar, eps))
    grad = np.zeros_like(gbar)
    grad[1:] = np.diff(logg) / np.maximum(np.diff(r), eps)

    curv = np.zeros_like(gbar)
    if len(r) > 2:
        dr = np.diff(r)
        d1 = np.diff(logg) / np.maximum(dr, eps)
        d2 = np.diff(d1) / np.maximum((dr[1:] + dr[:-1]) / 2.0, eps)
        curv[2:] = d2

    r_norm = r / (np.nanmedian(r) + eps)
    radial_shape = np.abs(grad) * (r_norm / (1 + r_norm)) + gamma_curv * np.abs(curv) * (r_norm**2 / (1 + r_norm**2))
    if np.any(np.abs(curv) > 0):
        cscale = np.nanmedian(np.abs(curv[np.abs(curv) > 0]))
    else:
        cscale = 1.0

    signed_shape = np.sign(curv) * np.minimum(np.abs(curv) / (cscale + eps), 3.0)

    drive_abs = radial_shape * (1 + zeta_disk * component_weight)
    m_s = np.zeros_like(gbar)
    m_f = np.zeros_like(gbar)
    for i in range(len(r)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - alpha_s) * ps + alpha_s * drive_abs[i]
        m_f[i] = (1 - alpha_f) * pf + alpha_f * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    a0 = np.nanmedian(gbar)
    rw_nonlocal = smooth_transfer(rw, r, L=L, eps=eps)
    if np.any(radial_shape > 0):
        shape_scale = np.nanmedian(radial_shape[radial_shape > 0])
    else:
        shape_scale = 1.0
    pos_shape = smooth_transfer(radial_shape / (shape_scale + eps), r, L=L, eps=eps)
    signed_shape_s = smooth_transfer(signed_shape, r, L=L, eps=eps)

    r0 = np.nanmedian(r)
    outer_gate = 1.0 / (1.0 + np.exp(-(r - gate_frac * r0) / (gate_width_frac * r0 + eps)))
    low_acc = a0 / (gbar + a0 + eps)

    corr_raw = beta * (1 - lam) * rw_nonlocal * low_acc * outer_gate * (
        (1 + zeta_disk * component_weight) * pos_shape + eta_signed * signed_shape_s
    )
    corr_term = np.tanh(corr_raw)

    gbridge = np.maximum(gbar * (1.0 + corr_term), 0.0)
    vbridge = np.sqrt(np.maximum(gbridge * r, 0.0))

    return {
        "vbar": vbar,
        "vbridge": vbridge,
        "corr_term": corr_term,
        "outer_gate": outer_gate,
        "component_weight": component_weight,
    }

def load_first_existing(folder, filenames):
    for fn in filenames:
        p = folder / fn
        if p.exists():
            return p
    return None

# =========================
# AUDIT
# =========================
summary_rows = []
notes = []

for galaxy, cfg in GALAXIES.items():
    folder = ROOT / cfg["folder"]
    row = {
        "galaxy": galaxy,
        "folder_exists": folder.exists(),
        "reconstruction_verified": False,
        "gas_shape_verified": False,
        "bridge_recomputed": False,
        "diagnostic_present": False,
        "status": "missing",
        "recon_rmse": np.nan,
        "recon_mae": np.nan,
        "recon_corr": np.nan,
        "gas_corr_cumulative": np.nan,
        "gas_corr_proxy": np.nan,
        "pilot_file_used": "",
        "rmse_baryonic_recomputed": np.nan,
        "rmse_bridge_recomputed": np.nan,
        "improvement_recomputed": np.nan,
        "comment": "",
    }

    if not folder.exists():
        row["comment"] = "folder missing"
        summary_rows.append(row)
        continue

    # Reconstruction check
    recon_path = folder / cfg["refined_vs_sparc"]
    if recon_path.exists():
        recon = pd.read_csv(recon_path)
        if {"vref_kms", "recon_kms"}.issubset(recon.columns):
            row["recon_rmse"] = rmse(recon["vref_kms"], recon["recon_kms"])
            row["recon_mae"] = mae(recon["vref_kms"], recon["recon_kms"])
            row["recon_corr"] = corr(recon["vref_kms"], recon["recon_kms"])
            row["reconstruction_verified"] = True

    # Gas compare check
    gas_compare_path = folder / cfg["gas_compare"]
    if gas_compare_path.exists():
        gc = pd.read_csv(gas_compare_path)
        if {"vgas2_norm", "things_cum_gas_norm"}.issubset(gc.columns):
            row["gas_corr_cumulative"] = corr(gc["vgas2_norm"], gc["things_cum_gas_norm"])
        if {"vgas2_norm", "things_gas_support_proxy_norm"}.issubset(gc.columns):
            row["gas_corr_proxy"] = corr(gc["vgas2_norm"], gc["things_gas_support_proxy_norm"])
        row["gas_shape_verified"] = True

    # Pilot recomputation
    pilot_path = load_first_existing(folder, cfg["gas_pilot"])
    if pilot_path is not None:
        row["pilot_file_used"] = pilot_path.name
        pilot = pd.read_csv(pilot_path)

        # pick available columns
        vobs_col = "Vobs" if "Vobs" in pilot.columns else None
        vgas_col = "Vgas" if "Vgas" in pilot.columns else None
        vdisk_col = "Vdisk" if "Vdisk" in pilot.columns else None
        vbul_col = "Vbul" if "Vbul" in pilot.columns else None
        r_col = "Rad" if "Rad" in pilot.columns else ("r_kpc" if "r_kpc" in pilot.columns else None)

        if all(c is not None for c in [vobs_col, vgas_col, vdisk_col, vbul_col, r_col]):
            sub = pilot[[r_col, vobs_col, vgas_col, vdisk_col, vbul_col]].copy()
            sub.columns = ["Rad", "Vobs", "Vgas", "Vdisk", "Vbul"]
            sub = sub.replace([np.inf, -np.inf], np.nan).dropna()
            if len(sub) >= 5:
                bridge = compute_bridge(
                    vobs=sub["Vobs"].to_numpy(float),
                    vgas=sub["Vgas"].to_numpy(float),
                    vdisk=sub["Vdisk"].to_numpy(float),
                    vbul=sub["Vbul"].to_numpy(float),
                    r=sub["Rad"].to_numpy(float),
                    params=BRIDGE_PARAMS,
                )
                row["rmse_baryonic_recomputed"] = rmse(sub["Vobs"], bridge["vbar"])
                row["rmse_bridge_recomputed"] = rmse(sub["Vobs"], bridge["vbridge"])
                row["improvement_recomputed"] = row["rmse_baryonic_recomputed"] - row["rmse_bridge_recomputed"]
                row["bridge_recomputed"] = True

                detail = sub.copy()
                detail["Vbar_recomputed"] = bridge["vbar"]
                detail["Vbridge_recomputed"] = bridge["vbridge"]
                detail["corr_term"] = bridge["corr_term"]
                detail["outer_gate"] = bridge["outer_gate"]
                detail["component_weight"] = bridge["component_weight"]
                detail.to_csv(OUT / f"{galaxy.lower()}_recomputed_detail.csv", index=False)

    # Diagnostics presence
    diag_present = False
    for fn in cfg.get("extra_diag", []):
        if (folder / fn).exists():
            diag_present = True
            break
    row["diagnostic_present"] = diag_present

    # status
    if row["reconstruction_verified"] and row["bridge_recomputed"]:
        row["status"] = "verified_core"
    elif row["reconstruction_verified"] or row["bridge_recomputed"]:
        row["status"] = "partial"
    else:
        row["status"] = "incomplete"

    if galaxy == "NGC6946":
        row["comment"] = "Check disk-amplitude caveat separately if disknorm file exists."
    elif galaxy == "NGC5055":
        row["comment"] = "Check residual-aware ablation separately if ablation files exist."
    else:
        row["comment"] = ""

    summary_rows.append(row)

summary = pd.DataFrame(summary_rows)
summary.to_csv(OUT / "round11_independent_verification_summary.csv", index=False)

# =========================
# OPTIONAL SPECIAL CHECKS
# =========================
special_rows = []

# NGC6946 disk-normalized near-full
p = ROOT / "things_ngc6946" / "ngc6946_bridge_external_gas_disk_proxy_pilot_disknorm.csv"
if p.exists():
    df = pd.read_csv(p)
    need = {"Rad", "Vobs", "Vgas", "Vdisk", "Vbul"}
    if need.issubset(df.columns):
        sub = df[list(need)].dropna().copy()
        bridge = compute_bridge(
            vobs=sub["Vobs"].to_numpy(float),
            vgas=sub["Vgas"].to_numpy(float),
            vdisk=sub["Vdisk"].to_numpy(float),
            vbul=sub["Vbul"].to_numpy(float),
            r=sub["Rad"].to_numpy(float),
            params=BRIDGE_PARAMS,
        )
        rb = rmse(sub["Vobs"], bridge["vbar"])
        rg = rmse(sub["Vobs"], bridge["vbridge"])
        special_rows.append({
            "galaxy": "NGC6946",
            "special_case": "disk_normalized_near_full",
            "rmse_baryonic": rb,
            "rmse_bridge": rg,
            "improvement": rb - rg,
        })

# NGC5055 residual-aware ablation if present
p = ROOT / "things_ngc5055" / "ngc5055_residual_aware_ablation_by_radius.csv"
if p.exists():
    df = pd.read_csv(p)
    if {"Vobs", "Vbar", "Vbridge_frozen", "Vbridge_resid"}.issubset(df.columns):
        special_rows.append({
            "galaxy": "NGC5055",
            "special_case": "residual_aware_ablation",
            "rmse_baryonic": rmse(df["Vobs"], df["Vbar"]),
            "rmse_bridge": rmse(df["Vobs"], df["Vbridge_resid"]),
            "improvement": rmse(df["Vobs"], df["Vbar"]) - rmse(df["Vobs"], df["Vbridge_resid"]),
        })
        special_rows.append({
            "galaxy": "NGC5055",
            "special_case": "frozen_reference_from_ablation_file",
            "rmse_baryonic": rmse(df["Vobs"], df["Vbar"]),
            "rmse_bridge": rmse(df["Vobs"], df["Vbridge_frozen"]),
            "improvement": rmse(df["Vobs"], df["Vbar"]) - rmse(df["Vobs"], df["Vbridge_frozen"]),
        })

special = pd.DataFrame(special_rows)
special.to_csv(OUT / "round11_special_case_checks.csv", index=False)

# =========================
# MARKDOWN REPORT
# =========================
lines = []
lines.append("# Round 11 Independent Verification Audit")
lines.append("")
lines.append("This audit recomputes core Round 11 metrics from local galaxy folders when available.")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append(summary.to_markdown(index=False))
lines.append("")

if len(special):
    lines.append("## Special-case checks")
    lines.append("")
    lines.append(special.to_markdown(index=False))
    lines.append("")

lines.append("## Notes")
lines.append("")
lines.append("- `verified_core` means reconstruction and at least one Bridge pilot were recomputed from local files.")
lines.append("- This audit only verifies what is present locally.")
lines.append("- Diagnostic ablations are reported separately from frozen raw results.")
lines.append("- If some galaxies are missing files, rerun after copying their working folders into the same root directory.")

report_path = OUT / "ROUND11_INDEPENDENT_VERIFICATION.md"
report_path.write_text("\n".join(lines), encoding="utf-8")

print("Saved:")
print(OUT / "round11_independent_verification_summary.csv")
print(OUT / "round11_special_case_checks.csv")
print(report_path)

print("\nSummary preview:")
print(summary.to_string(index=False))

if len(special):
    print("\nSpecial-case preview:")
    print(special.to_string(index=False))
