# ============================================================
# COLAB: Modal Library Trace Normalization Campaign
#
# Purpose:
#   The 5-geometry test showed:
#
#       q survives near 2
#       C is geometry-dependent
#       one descriptor such as k_eff is not enough
#
#   This campaign expands the geometry library using Fourier fields
#   and tests whether a modal descriptor vector predicts C(f).
#
#   The target is:
#
#       int R dV ≈ - C(f) * dx^q * DeltaTraceSlope
#
#   where q should remain near 2 and C(f) should be predictable
#   from spectral/modal descriptors.
#
# Notes:
#   - Self-contained.
#   - Uses torch if available.
#   - Designed for Colab T4.
#   - QUICK_MODE keeps runtime reasonable.
#
# Outputs:
#   modal_library_trace_rows.csv
#   modal_library_geometry_fits.csv
#   modal_library_descriptor_models.csv
#   modal_library_summary.json
# ============================================================

import os, json, math, time, random
import numpy as np
import pandas as pd

try:
    import torch
except Exception:
    torch = None

print("Torch available:", torch is not None)
if torch is not None:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", DEVICE)
    if DEVICE == "cuda":
        print("GPU:", torch.cuda.get_device_name(0))
else:
    DEVICE = "cpu"

# ----------------------------
# Controls
# ----------------------------
QUICK_MODE = True

if QUICK_MODE:
    N_LIST = [8, 10, 12]
    AMP_LIST = [0.08, 0.15, 0.22]
    N_RANDOM_GEOMS = 18
else:
    N_LIST = [8, 10, 12, 14]
    AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25]
    N_RANDOM_GEOMS = 40

TIME_MULTIPLIERS = [0.8, 1.2, 1.8, 2.6, 3.5]
SEED = 1234
DOMAIN_L = 2*np.pi
OUT_PREFIX = "modal_library"

np.random.seed(SEED)
random.seed(SEED)


# ============================================================
# Fourier geometry definition
# ============================================================

# Field:
#   f(x,y,z) = sum_j a_j cos(k_j dot x + phase_j)
#
# For each mode:
#   k = (kx, ky, kz), phase, coefficient a.
#
# phi = amp * f
#
# Scalar curvature for conformal 3-metric g=e^{2phi} delta:
#
#   R = exp(-2phi) * (-4 Delta phi - 2 |grad phi|^2)
#
# dV = exp(3phi) dx^3
#
# This is the direct analytic curvature target.
# The heat side uses a simple conformal weighted graph Laplacian.
# The absolute C may depend on operator choice, but the campaign tests
# whether q and modal normalization persist inside a fixed operator.
# ============================================================

def make_named_geometries():
    geoms = []

    def add(name, modes):
        geoms.append({"name": name, "modes": modes})

    # Existing family approximations
    add("xyz_product_like", [
        {"k": (1,1,1), "a": 1.0, "phase": 0.0},
        {"k": (1,1,-1), "a": 1.0, "phase": 0.0},
        {"k": (1,-1,1), "a": 1.0, "phase": 0.0},
        {"k": (-1,1,1), "a": 1.0, "phase": 0.0},
    ])

    add("high_x_like", [
        {"k": (2,1,1), "a": 1.0, "phase": 0.0},
        {"k": (2,1,-1), "a": 1.0, "phase": 0.0},
        {"k": (2,-1,1), "a": 1.0, "phase": 0.0},
        {"k": (-2,1,1), "a": 1.0, "phase": 0.0},
    ])

    add("additive_mixed_like", [
        {"k": (1,0,0), "a": 1.0, "phase": 0.0},
        {"k": (0,2,0), "a": 0.5, "phase": 0.0},
        {"k": (0,0,3), "a": 0.25, "phase": 0.0},
    ])

    add("two_mode_like", [
        {"k": (1,1,1), "a": 1.0, "phase": 0.0},
        {"k": (2,2,1), "a": 0.35, "phase": 0.0},
    ])

    add("anisotropic_packet_like", [
        {"k": (1,0,0), "a": 1.0, "phase": 0.0},
        {"k": (1,1,0), "a": 0.35, "phase": 0.0},
        {"k": (0,0,2), "a": 0.20, "phase": 0.0},
    ])

    return geoms


def random_geometry(idx):
    # A controlled random Fourier mixture.
    candidate_modes = []
    for kx in range(0, 4):
        for ky in range(0, 4):
            for kz in range(0, 4):
                if kx == ky == kz == 0:
                    continue
                k2 = kx*kx + ky*ky + kz*kz
                if 1 <= k2 <= 14:
                    candidate_modes.append((kx,ky,kz))

    n_modes = random.choice([2,3,4,5,6])
    modes = random.sample(candidate_modes, n_modes)

    out = []
    for k in modes:
        k2 = sum(v*v for v in k)
        # Decay high modes, but not too aggressively.
        a = random.uniform(0.25, 1.0) / (k2 ** random.uniform(0.15, 0.45))
        phase = random.uniform(0, 2*np.pi)
        out.append({"k": k, "a": a, "phase": phase})

    return {"name": f"rand_fourier_{idx:02d}", "modes": out}


GEOMS = make_named_geometries() + [random_geometry(i) for i in range(N_RANDOM_GEOMS)]
print("Number of geometries:", len(GEOMS))


def normalize_modes(modes, target_rms=1.0, grid_N=48):
    # Normalize f RMS to target_rms so amplitude is comparable across geometries.
    x = np.linspace(0, DOMAIN_L, grid_N, endpoint=False)
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    f = np.zeros_like(X)
    for m in modes:
        kx,ky,kz = m["k"]
        f += m["a"] * np.cos(kx*X + ky*Y + kz*Z + m["phase"])
    rms = float(np.sqrt(np.mean(f*f)))
    if rms < 1e-12:
        return modes
    scale = target_rms / rms
    new_modes = []
    for m in modes:
        mm = dict(m)
        mm["a"] = float(mm["a"] * scale)
        new_modes.append(mm)
    return new_modes


for g in GEOMS:
    g["modes"] = normalize_modes(g["modes"], target_rms=1.0)


# ============================================================
# Grid and field functions
# ============================================================

def grid_np(N):
    dx = DOMAIN_L/N
    x = np.arange(N)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    return X,Y,Z,dx


def eval_field_derivatives(modes, N):
    X,Y,Z,dx = grid_np(N)
    f = np.zeros((N,N,N), dtype=np.float64)
    fx = np.zeros_like(f); fy = np.zeros_like(f); fz = np.zeros_like(f)
    lap = np.zeros_like(f)

    for m in modes:
        kx,ky,kz = m["k"]
        a = m["a"]; ph = m["phase"]
        theta = kx*X + ky*Y + kz*Z + ph
        c = np.cos(theta)
        s = np.sin(theta)
        k2 = kx*kx + ky*ky + kz*kz

        f += a*c
        fx += -a*kx*s
        fy += -a*ky*s
        fz += -a*kz*s
        lap += -a*k2*c

    return f,fx,fy,fz,lap,dx


def curvature_integral(modes, N, amp):
    f,fx,fy,fz,lap,dx = eval_field_derivatives(modes, N)
    phi = amp*f
    grad2_phi = (amp*fx)**2 + (amp*fy)**2 + (amp*fz)**2
    lap_phi = amp*lap

    R = np.exp(-2*phi) * (-4*lap_phi - 2*grad2_phi)
    dV = np.exp(3*phi) * (dx**3)
    I = float(np.sum(R*dV))
    volume = float(np.sum(dV))
    return {
        "int_RdV": I,
        "volume": volume,
        "R_min": float(np.min(R)),
        "R_max": float(np.max(R)),
        "R_mean": float(np.mean(R)),
        "R_std": float(np.std(R)),
        "dx": float(dx),
        "phi_flat": phi.reshape(-1),
    }


def dense_graph_laplacian_from_phi(phi_flat, N):
    # Simple symmetric conformal conductance graph on periodic 3D grid.
    # Conductance choice is fixed across all geometries.
    # W_ij = exp(phi_i + phi_j)
    # L = D - W
    n = N**3
    phi = phi_flat.reshape(N,N,N)
    L = np.zeros((n,n), dtype=np.float64)

    def idx(i,j,k):
        return (i*N + j)*N + k

    dirs = [(1,0,0),(0,1,0),(0,0,1)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i,j,k)
                phia = phi[i,j,k]
                for di,dj,dk in dirs:
                    ii = (i+di) % N
                    jj = (j+dj) % N
                    kk = (k+dk) % N
                    b = idx(ii,jj,kk)
                    w = math.exp(phia + phi[ii,jj,kk])
                    L[a,a] += w
                    L[b,b] += w
                    L[a,b] -= w
                    L[b,a] -= w
    return L


def heat_trace_slope(phi_flat, N, dx):
    L = dense_graph_laplacian_from_phi(phi_flat, N)

    if torch is not None and DEVICE == "cuda":
        with torch.no_grad():
            T = torch.tensor(L, dtype=torch.float64, device="cuda")
            eig = torch.linalg.eigvalsh(T).detach().cpu().numpy()
    else:
        eig = np.linalg.eigvalsh(L)

    eig = np.maximum(eig, 0.0)
    times = np.array(TIME_MULTIPLIERS, dtype=np.float64) * (dx**2)
    traces = np.array([np.sum(np.exp(-t*eig)) for t in times], dtype=np.float64)

    # Linear slope over short heat-time window.
    A = np.vstack([np.ones_like(times), times]).T
    beta = np.linalg.lstsq(A, traces, rcond=None)[0]
    intercept, slope = float(beta[0]), float(beta[1])

    return {
        "trace_slope": slope,
        "trace_intercept": intercept,
        "trace_H_mean": float(np.mean(traces)),
        "trace_H_std": float(np.std(traces)),
        "eig_min": float(np.min(eig)),
        "eig_max": float(np.max(eig)),
    }


# ============================================================
# Modal descriptors
# ============================================================

def descriptors(modes, N_desc=96):
    f,fx,fy,fz,lap,dx = eval_field_derivatives(modes, N_desc)
    g2 = fx*fx + fy*fy + fz*fz
    E0 = float(np.mean(f*f))
    E1 = float(np.mean(g2))
    E2 = float(np.mean(lap*lap))
    E4 = float(np.mean(f**4))
    E6 = float(np.mean(f**6))
    ipr4 = float(E4/(E0*E0 + 1e-15))
    ipr6 = float(E6/(E0**3 + 1e-15))
    k_eff2 = float(E2/(E1+1e-15))
    k_eff = float(np.sqrt(k_eff2))
    gx,gy,gz = float(np.mean(fx*fx)), float(np.mean(fy*fy)), float(np.mean(fz*fz))
    grad = np.array([gx,gy,gz])
    anis = float(np.std(grad)/(np.mean(grad)+1e-15))

    # modal coefficient descriptors
    weights = []
    k2s = []
    for m in modes:
        k2 = sum(v*v for v in m["k"])
        weights.append(m["a"]**2)
        k2s.append(k2)
    weights = np.array(weights, dtype=float)
    weights = weights/(weights.sum()+1e-15)
    k2s = np.array(k2s, dtype=float)

    k2_mean = float(np.sum(weights*k2s))
    k2_var = float(np.sum(weights*(k2s-k2_mean)**2))
    entropy = float(-np.sum(weights*np.log(weights+1e-15)))
    n_eff = float(np.exp(entropy))

    return {
        "E0": E0,
        "E1": E1,
        "E2": E2,
        "k_eff": k_eff,
        "k_eff2": k_eff2,
        "ipr4": ipr4,
        "ipr6": ipr6,
        "grad_anisotropy": anis,
        "grad_x": gx,
        "grad_y": gy,
        "grad_z": gz,
        "modal_k2_mean": k2_mean,
        "modal_k2_var": k2_var,
        "modal_entropy": entropy,
        "modal_n_eff": n_eff,
        "n_modes": len(modes),
    }


# ============================================================
# Campaign
# ============================================================

print()
print("Running modal library trace normalization campaign...")
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("QUICK_MODE:", QUICK_MODE)

rows = []
flat_cache = {}

for gi, geom in enumerate(GEOMS):
    gname = geom["name"]
    modes = geom["modes"]
    print()
    print("="*80)
    print(f"GEOMETRY {gi+1}/{len(GEOMS)}: {gname}")
    print("modes:", modes)

    dsc = descriptors(modes)

    for N in N_LIST:
        # Flat reference for this N: phi=0
        if N not in flat_cache:
            curv0 = curvature_integral([], N, 0.0)
            zero_phi = np.zeros(N**3, dtype=np.float64)
            h0 = heat_trace_slope(zero_phi, N, curv0["dx"])
            flat_cache[N] = h0
            print(f"  flat N={N}: slope={h0['trace_slope']:.6g}")

        flat = flat_cache[N]

        for amp in AMP_LIST:
            t0 = time.time()
            curv = curvature_integral(modes, N, amp)
            heat = heat_trace_slope(curv["phi_flat"], N, curv["dx"])

            delta_slope = heat["trace_slope"] - flat["trace_slope"]
            I = curv["int_RdV"]
            C_req = I / (delta_slope + 1e-15)

            row = {
                "geometry": gname,
                "N": N,
                "nodes": N**3,
                "amp": amp,
                "dx": curv["dx"],
                "int_RdV": I,
                "volume": curv["volume"],
                "R_min": curv["R_min"],
                "R_max": curv["R_max"],
                "R_mean": curv["R_mean"],
                "R_std": curv["R_std"],
                "trace_slope": heat["trace_slope"],
                "flat_trace_slope": flat["trace_slope"],
                "delta_trace_slope": delta_slope,
                "C_delta_required": C_req,
                "abs_C_delta": abs(C_req),
                "seconds": round(time.time()-t0, 3),
            }
            row.update(dsc)
            rows.append(row)
            print(json.dumps({
                "geometry": gname,
                "N": N,
                "amp": amp,
                "int_RdV": I,
                "delta_trace_slope": delta_slope,
                "C_delta_required": C_req,
                "seconds": row["seconds"],
            }, indent=2))

raw = pd.DataFrame(rows)
raw.to_csv(f"{OUT_PREFIX}_trace_rows.csv", index=False)


# ============================================================
# Per-geometry q/C fits
# ============================================================

def fit_cq(gdf):
    x = np.log(gdf["dx"].values)
    y = np.log(np.abs(gdf["C_delta_required"].values))
    A = np.vstack([np.ones_like(x), x]).T
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    c = float(np.exp(beta[0]))
    q = float(beta[1])

    pred_C = -c*(gdf["dx"].values**q) * np.sign(np.median(gdf["C_delta_required"].values))
    # Since most C_req may be negative/positive depending sign convention,
    # predict I directly using fitted C_req sign.
    signed_c = float(np.median(gdf["C_delta_required"].values / (gdf["dx"].values**q)))
    pred_I = signed_c*(gdf["dx"].values**q)*gdf["delta_trace_slope"].values
    err = np.abs(pred_I-gdf["int_RdV"].values)/(np.abs(gdf["int_RdV"].values)+1e-12)

    return {
        "geometry": gdf["geometry"].iloc[0],
        "fit_c_abs": c,
        "fit_q": q,
        "fit_signed_c": signed_c,
        "fit_I_rel_error_mean": float(np.mean(err)),
        "fit_I_rel_error_max": float(np.max(err)),
        "n_rows": int(len(gdf)),
    }

fits = pd.DataFrame([fit_cq(g) for _,g in raw.groupby("geometry")])
desc_df = raw.groupby("geometry").first().reset_index()[[
    "geometry","E0","E1","E2","k_eff","k_eff2","ipr4","ipr6","grad_anisotropy",
    "modal_k2_mean","modal_k2_var","modal_entropy","modal_n_eff","n_modes"
]]
fitdesc = fits.merge(desc_df, on="geometry", how="left")
fitdesc.to_csv(f"{OUT_PREFIX}_geometry_fits.csv", index=False)


# ============================================================
# Descriptor models for log C
# ============================================================

from itertools import combinations

work = fitdesc.copy()
for col in ["fit_c_abs","E0","E1","E2","k_eff","k_eff2","ipr4","ipr6","modal_k2_mean","modal_k2_var","modal_n_eff","n_modes"]:
    work["log_"+col] = np.log(work[col].values + 1e-15)

work["logC"] = np.log(work["fit_c_abs"].values + 1e-15)

candidate_features = [
    "log_E0","log_E1","log_E2","log_k_eff","log_ipr4","log_ipr6",
    "grad_anisotropy","log_modal_k2_mean","log_modal_k2_var",
    "modal_entropy","log_modal_n_eff","log_n_modes"
]

feature_sets = []
feature_sets.append(("constant", []))
for f in candidate_features:
    feature_sets.append((f, [f]))
for r in [2,3]:
    for comb in combinations(candidate_features, r):
        feature_sets.append(("+".join(comb), list(comb)))


def ridge_fit(X, y, alpha=1e-3):
    # No penalty on intercept.
    P = np.eye(X.shape[1])
    P[0,0] = 0.0
    return np.linalg.solve(X.T@X + alpha*P, X.T@y)


def make_X(df, feats):
    if not feats:
        return np.ones((len(df),1))
    return np.column_stack([np.ones(len(df))] + [df[f].values for f in feats])


model_rows = []
logo_rows = []
geoms = work["geometry"].tolist()

for model_name, feats in feature_sets:
    errs = []
    logerrs = []

    for holdout in geoms:
        train = work[work.geometry != holdout]
        test = work[work.geometry == holdout]
        Xtr = make_X(train, feats)
        ytr = train["logC"].values
        beta = ridge_fit(Xtr, ytr, alpha=1e-2)

        Xte = make_X(test, feats)
        pred_logC = float((Xte@beta)[0])
        pred_C = float(np.exp(pred_logC))
        true_C = float(test["fit_c_abs"].iloc[0])
        rel = abs(pred_C-true_C)/(true_C+1e-15)
        loge = abs(pred_logC - float(test["logC"].iloc[0]))
        errs.append(rel); logerrs.append(loge)
        logo_rows.append({
            "model": model_name,
            "holdout_geometry": holdout,
            "true_C": true_C,
            "pred_C": pred_C,
            "rel_C_error": rel,
            "abs_log_error": loge,
            "features": "+".join(feats) if feats else "constant",
        })

    model_rows.append({
        "model": model_name,
        "features": "+".join(feats) if feats else "constant",
        "n_features": len(feats),
        "logo_rel_C_error_mean": float(np.mean(errs)),
        "logo_rel_C_error_median": float(np.median(errs)),
        "logo_rel_C_error_max": float(np.max(errs)),
        "logo_abs_log_error_mean": float(np.mean(logerrs)),
        "logo_abs_log_error_max": float(np.max(logerrs)),
    })

models = pd.DataFrame(model_rows).sort_values(
    ["logo_rel_C_error_mean", "n_features"],
    ascending=[True, True]
)
logo = pd.DataFrame(logo_rows)
models.to_csv(f"{OUT_PREFIX}_descriptor_models.csv", index=False)
logo.to_csv(f"{OUT_PREFIX}_leave_one_geometry_out.csv", index=False)

best = models.iloc[0].to_dict()
best_feats = [] if best["features"] == "constant" else best["features"].split("+")

# Fit best on all and predict row-level
Xall = make_X(work, best_feats)
beta = ridge_fit(Xall, work["logC"].values, alpha=1e-2)
work["pred_logC"] = make_X(work, best_feats) @ beta
work["pred_C_abs"] = np.exp(work["pred_logC"])
work["pred_C_rel_error"] = np.abs(work["pred_C_abs"]-work["fit_c_abs"])/(work["fit_c_abs"]+1e-15)
work.to_csv(f"{OUT_PREFIX}_best_descriptor_by_geometry.csv", index=False)

rowpred = raw.merge(work[["geometry","fit_q","fit_signed_c","fit_c_abs","pred_C_abs"]], on="geometry", how="left")
# Keep sign from per-geometry median sign, magnitude from descriptor model.
sign_by_geom = raw.groupby("geometry")["C_delta_required"].median().apply(np.sign).to_dict()
rowpred["pred_signed_C_descriptor"] = rowpred.apply(
    lambda r: sign_by_geom[r["geometry"]] * r["pred_C_abs"], axis=1
)
rowpred["I_pred_descriptor"] = rowpred["pred_signed_C_descriptor"]*(rowpred["dx"]**rowpred["fit_q"])*rowpred["delta_trace_slope"]
rowpred["I_rel_error_descriptor"] = np.abs(rowpred["I_pred_descriptor"]-rowpred["int_RdV"])/(np.abs(rowpred["int_RdV"])+1e-12)
rowpred.to_csv(f"{OUT_PREFIX}_row_predictions.csv", index=False)


summary = {
    "device": DEVICE,
    "quick_mode": QUICK_MODE,
    "n_geometries": int(len(GEOMS)),
    "n_rows": int(len(raw)),
    "N_completed": N_LIST,
    "amp_completed": AMP_LIST,
    "q_mean": float(fits["fit_q"].mean()),
    "q_std": float(fits["fit_q"].std()),
    "q_min": float(fits["fit_q"].min()),
    "q_max": float(fits["fit_q"].max()),
    "per_geometry_I_rel_error_mean": float(fits["fit_I_rel_error_mean"].mean()),
    "per_geometry_I_rel_error_max": float(fits["fit_I_rel_error_max"].max()),
    "best_descriptor_model": best["model"],
    "best_descriptor_features": best["features"],
    "best_logo_rel_C_error_mean": float(best["logo_rel_C_error_mean"]),
    "best_logo_rel_C_error_median": float(best["logo_rel_C_error_median"]),
    "best_logo_rel_C_error_max": float(best["logo_rel_C_error_max"]),
    "row_descriptor_I_rel_error_mean": float(rowpred["I_rel_error_descriptor"].mean()),
    "row_descriptor_I_rel_error_max": float(rowpred["I_rel_error_descriptor"].max()),
    "classification": (
        "MODAL_DESCRIPTOR_NORMALIZATION_PROMISING"
        if float(best["logo_rel_C_error_mean"]) < 0.25 and float(fits["fit_q"].std()) < 0.35
        else "MODAL_DESCRIPTOR_NORMALIZATION_MIXED"
    )
}

with open(f"{OUT_PREFIX}_summary.json","w") as f:
    json.dump(summary, f, indent=2)

print()
print("================ MODAL LIBRARY TRACE NORMALIZATION SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("GEOMETRY_FITS:")
print(fitdesc.to_csv(index=False))

print()
print("TOP_DESCRIPTOR_MODELS:")
print(models.head(25).to_csv(index=False))

print()
print("BEST_DESCRIPTOR_BY_GEOMETRY:")
print(work.to_csv(index=False))

print()
print("Saved files:")
for name in [
    f"{OUT_PREFIX}_trace_rows.csv",
    f"{OUT_PREFIX}_geometry_fits.csv",
    f"{OUT_PREFIX}_descriptor_models.csv",
    f"{OUT_PREFIX}_leave_one_geometry_out.csv",
    f"{OUT_PREFIX}_best_descriptor_by_geometry.csv",
    f"{OUT_PREFIX}_row_predictions.csv",
    f"{OUT_PREFIX}_summary.json",
]:
    print(name)
