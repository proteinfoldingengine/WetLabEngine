# ============================================================
# COLAB: Frozen dx2/long Modal Library Validation Campaign
#
# Result from previous calibration:
#
#   raw/long had the lowest scalar stability score, but it carries
#   an unphysical q ≈ 7.63 caused by raw graph-time scaling.
#
#   dx2/long is the correct next freeze candidate:
#      - no dropped rows
#      - stable sign consistency = 1.0
#      - lower I_rel_error_mean ≈ 0.137
#      - physically interpretable q ≈ 1.06
#      - smooth flat trace behavior
#
# Goal:
#   Freeze the heat operator as:
#
#       L = graph_laplacian / dx^2
#       heat window = long = [0.25, 0.40, 0.65, 1.00, 1.60]
#
#   Then re-run the broad 23-geometry modal library using only this
#   operator/window and test:
#
#      1. per-geometry C, q stability
#      2. amplitude law stability
#      3. modal descriptor prediction of C
#      4. leave-one-geometry-out generalization
#      5. whether dx2/long removes the prior sign-flip pathology
#
# Send back:
#   FROZEN DX2 LONG SUMMARY
#   GEOMETRY_FITS
#   DESCRIPTOR_MODEL_RANKINGS
#   LEAVE_ONE_GEOMETRY_OUT
# ============================================================

import os, json, math, time
import numpy as np
import pandas as pd

try:
    import torch
except Exception:
    torch = None

try:
    import scipy.sparse as sp
except Exception:
    sp = None

print("Torch available:", torch is not None)
if torch is not None:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", DEVICE)
    if DEVICE == "cuda":
        print("GPU:", torch.cuda.get_device_name(0))
else:
    DEVICE = "cpu"

print("Scipy sparse available:", sp is not None)

# ----------------------------
# Frozen operator/window
# ----------------------------
OPERATOR_KIND = "dx2"
WINDOW_NAME = "long"
TAUS = np.array([0.25, 0.40, 0.65, 1.00, 1.60], dtype=np.float64)

DOMAIN_L = 2*np.pi
OUT_PREFIX = "frozen_dx2_long_modal_validation"

QUICK_MODE = True
if QUICK_MODE:
    N_LIST = [8, 10, 12, 14]
    AMP_LIST = [0.06, 0.08, 0.12, 0.15, 0.22]
else:
    N_LIST = [8, 10, 12, 14, 16]
    AMP_LIST = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.18, 0.22]

print("Frozen operator:", OPERATOR_KIND)
print("Frozen window:", WINDOW_NAME, TAUS.tolist())
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)


# ============================================================
# Geometry library
# ============================================================

def normalize_modes(modes):
    # Normalize modal coefficients so E0 = mean f^2 ≈ 1.
    # For cosine modes on torus, E[f^2] = 0.5 * sum a_i^2 for distinct modes.
    s2 = sum(m["a"]**2 for m in modes)
    scale = math.sqrt(2.0 / (s2 + 1e-15))
    out = []
    for m in modes:
        mm = dict(m)
        mm["a"] = mm["a"] * scale
        out.append(mm)
    return out

base_geoms = [
    {
        "name": "xyz_product_like",
        "modes": [
            {"k": (1,1,1),  "a": 1.0, "phase": 0.0},
            {"k": (1,1,-1), "a": 1.0, "phase": 0.0},
            {"k": (1,-1,1), "a": 1.0, "phase": 0.0},
            {"k": (-1,1,1), "a": 1.0, "phase": 0.0},
        ],
    },
    {
        "name": "high_x_like",
        "modes": [
            {"k": (2,1,1),  "a": 1.0, "phase": 0.0},
            {"k": (2,1,-1), "a": 1.0, "phase": 0.0},
            {"k": (2,-1,1), "a": 1.0, "phase": 0.0},
            {"k": (-2,1,1), "a": 1.0, "phase": 0.0},
        ],
    },
    {
        "name": "additive_mixed_like",
        "modes": [
            {"k": (1,0,0), "a": 1.0, "phase": 0.0},
            {"k": (0,2,0), "a": 0.5, "phase": 0.0},
            {"k": (0,0,3), "a": 0.25, "phase": 0.0},
        ],
    },
    {
        "name": "two_mode_like",
        "modes": [
            {"k": (1,1,1), "a": 1.0, "phase": 0.0},
            {"k": (2,2,1), "a": 0.35, "phase": 0.0},
        ],
    },
    {
        "name": "anisotropic_packet_like",
        "modes": [
            {"k": (1,0,0), "a": 1.0, "phase": 0.0},
            {"k": (1,1,0), "a": 0.35, "phase": 0.0},
            {"k": (0,0,2), "a": 0.2, "phase": 0.0},
        ],
    },
]

# Deterministic random modal library.
rng = np.random.default_rng(20260506)
allowed_k = []
for kx in range(0,4):
    for ky in range(0,4):
        for kz in range(0,4):
            if (kx,ky,kz) == (0,0,0):
                continue
            if kx*kx + ky*ky + kz*kz <= 14:
                allowed_k.append((kx,ky,kz))

rand_geoms = []
for gi in range(18):
    n_modes = int(rng.integers(2, 7))
    ks_idx = rng.choice(len(allowed_k), size=n_modes, replace=False)
    modes = []
    for idx in ks_idx:
        k = allowed_k[int(idx)]
        a = float(np.exp(rng.normal(0.0, 0.55)))
        phase = float(rng.uniform(0, 2*np.pi))
        modes.append({"k": k, "a": a, "phase": phase})
    rand_geoms.append({"name": f"rand_fourier_{gi:02d}", "modes": modes})

GEOMS = []
for g in base_geoms + rand_geoms:
    GEOMS.append({"name": g["name"], "modes": normalize_modes(g["modes"])})

print("Number of geometries:", len(GEOMS))


# ============================================================
# Field, curvature, descriptors
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
    return {
        "int_RdV": float(np.sum(R*dV)),
        "volume": float(np.sum(dV)),
        "dx": float(dx),
        "phi_flat": phi.reshape(-1),
        "R_std": float(np.std(R)),
        "R_min": float(np.min(R)),
        "R_max": float(np.max(R)),
    }

def modal_descriptors(modes):
    # For normalized cosines:
    # E0 = 0.5 sum a^2
    # E1 = 0.5 sum a^2 |k|^2
    # E2 = 0.5 sum a^2 |k|^4
    weights = []
    k2s = []
    gx = gy = gz = 0.0
    for m in modes:
        kx,ky,kz = m["k"]
        a = m["a"]
        w = 0.5*a*a
        k2 = kx*kx + ky*ky + kz*kz
        weights.append(w)
        k2s.append(k2)
        gx += w*kx*kx
        gy += w*ky*ky
        gz += w*kz*kz

    weights = np.array(weights, dtype=np.float64)
    k2s = np.array(k2s, dtype=np.float64)
    E0 = float(np.sum(weights))
    E1 = float(np.sum(weights*k2s))
    E2 = float(np.sum(weights*k2s*k2s))
    k_eff2 = E2/(E1 + 1e-15)
    k_eff = math.sqrt(max(k_eff2, 0.0))

    p = weights/(np.sum(weights)+1e-15)
    modal_entropy = float(-np.sum(p*np.log(p+1e-15)))
    modal_n_eff = float(np.exp(modal_entropy))
    modal_k2_mean = float(np.sum(p*k2s))
    modal_k2_var = float(np.sum(p*(k2s-modal_k2_mean)**2))

    grad_vec = np.array([gx,gy,gz], dtype=np.float64)
    grad_anisotropy = float(np.std(grad_vec)/(np.mean(grad_vec)+1e-15))

    return {
        "E0": E0,
        "E1": E1,
        "E2": E2,
        "k_eff": k_eff,
        "k_eff2": k_eff2,
        "grad_x_energy": float(gx),
        "grad_y_energy": float(gy),
        "grad_z_energy": float(gz),
        "grad_anisotropy": grad_anisotropy,
        "modal_k2_mean": modal_k2_mean,
        "modal_k2_var": modal_k2_var,
        "modal_entropy": modal_entropy,
        "modal_n_eff": modal_n_eff,
        "n_modes": int(len(modes)),
    }


# ============================================================
# Heat operator
# ============================================================

def build_sparse_graph_laplacian(phi_flat, N, dx):
    phi = phi_flat.reshape(N,N,N)
    n = N**3
    rows = []
    cols = []
    vals = []
    deg = np.zeros(n, dtype=np.float64)

    def idx(i,j,k):
        return (i*N + j)*N + k

    edge_i = []
    edge_j = []
    edge_w = []
    dirs = [(1,0,0),(0,1,0),(0,0,1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i,j,k)
                for di,dj,dk in dirs:
                    ii = (i+di) % N
                    jj = (j+dj) % N
                    kk = (k+dk) % N
                    b = idx(ii,jj,kk)
                    w = math.exp(phi[i,j,k] + phi[ii,jj,kk])
                    edge_i.append(a); edge_j.append(b); edge_w.append(w)
                    edge_i.append(b); edge_j.append(a); edge_w.append(w)
                    deg[a] += w
                    deg[b] += w

    for a in range(n):
        rows.append(a); cols.append(a); vals.append(deg[a])
    for a,b,w in zip(edge_i, edge_j, edge_w):
        rows.append(a); cols.append(b); vals.append(-w)

    L = sp.csr_matrix((vals,(rows,cols)), shape=(n,n))
    return L/(dx*dx)

def eigvals_operator(phi_flat, N, dx):
    L = build_sparse_graph_laplacian(phi_flat, N, dx)
    A = L.toarray()
    if torch is not None and DEVICE == "cuda" and A.shape[0] <= 3000:
        with torch.no_grad():
            T = torch.tensor(A, dtype=torch.float64, device="cuda")
            eig = torch.linalg.eigvalsh(T).detach().cpu().numpy()
    else:
        eig = np.linalg.eigvalsh(A)
    return np.maximum(eig, 0.0)

def heat_trace_slope(eig):
    traces = np.array([np.sum(np.exp(-t*eig)) for t in TAUS], dtype=np.float64)
    A = np.vstack([np.ones_like(TAUS), TAUS]).T
    beta = np.linalg.lstsq(A, traces, rcond=None)[0]
    return {
        "trace_intercept": float(beta[0]),
        "trace_slope": float(beta[1]),
        "trace_mean": float(np.mean(traces)),
        "trace_std": float(np.std(traces)),
    }


# ============================================================
# Run
# ============================================================

rows = []
flat_slope_by_N = {}

print()
print("Computing flat references...")
for N in N_LIST:
    dx = DOMAIN_L/N
    zero_phi = np.zeros(N**3, dtype=np.float64)
    eig0 = eigvals_operator(zero_phi, N, dx)
    h0 = heat_trace_slope(eig0)
    flat_slope_by_N[N] = h0["trace_slope"]
    print(f"flat N={N}, dx={dx:.4f}, slope={h0['trace_slope']:.6g}")

print()
print("Running frozen dx2/long modal validation...")
for gi, geom in enumerate(GEOMS, start=1):
    print()
    print("="*80)
    print(f"GEOMETRY {gi}/{len(GEOMS)}: {geom['name']}")
    print("modes:", geom["modes"])
    desc = modal_descriptors(geom["modes"])

    for N in N_LIST:
        for amp in AMP_LIST:
            t0 = time.time()
            curv = curvature_integral(geom["modes"], N, amp)
            eig = eigvals_operator(curv["phi_flat"], N, curv["dx"])
            h = heat_trace_slope(eig)
            delta = h["trace_slope"] - flat_slope_by_N[N]
            C_req = curv["int_RdV"]/(delta + 1e-15)

            row = {
                "geometry": geom["name"],
                "N": N,
                "nodes": N**3,
                "amp": amp,
                "dx": curv["dx"],
                "int_RdV": curv["int_RdV"],
                "volume": curv["volume"],
                "R_std": curv["R_std"],
                "R_min": curv["R_min"],
                "R_max": curv["R_max"],
                "trace_slope": h["trace_slope"],
                "flat_trace_slope": flat_slope_by_N[N],
                "delta_trace_slope": delta,
                "C_delta_required": C_req,
                "abs_C_delta": abs(C_req),
                "seconds": round(time.time()-t0, 3),
                **desc,
            }
            rows.append(row)

            print(json.dumps({
                "geometry": geom["name"],
                "N": N,
                "amp": amp,
                "I": curv["int_RdV"],
                "delta": delta,
                "C_req": C_req,
                "seconds": row["seconds"],
            }, indent=2))

raw = pd.DataFrame(rows)
raw.to_csv(f"{OUT_PREFIX}_rows.csv", index=False)


# ============================================================
# Fits and diagnostics
# ============================================================

def fit_per_geometry(g):
    x = np.log(g["dx"].values)
    y = np.log(np.abs(g["C_delta_required"].values) + 1e-30)
    A = np.vstack([np.ones_like(x), x]).T
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    c_abs = float(np.exp(beta[0]))
    q = float(beta[1])
    signed_c = float(np.median(g["C_delta_required"].values/(g["dx"].values**q)))

    pred_I = signed_c*(g["dx"].values**q)*g["delta_trace_slope"].values
    err = np.abs(pred_I - g["int_RdV"].values)/(np.abs(g["int_RdV"].values)+1e-12)

    signs = np.sign(g["delta_trace_slope"].values)
    nonzero = signs[signs != 0]
    sign_consistency = float(np.max([np.mean(nonzero > 0), np.mean(nonzero < 0)])) if len(nonzero) else 0.0

    # amplitude law: I ≈ A * amp^p by N, then average p
    amp_ps = []
    delta_ps = []
    for N, gn in g.groupby("N"):
        lx = np.log(gn["amp"].values)
        lyI = np.log(np.abs(gn["int_RdV"].values)+1e-30)
        lyd = np.log(np.abs(gn["delta_trace_slope"].values)+1e-30)
        AA = np.vstack([np.ones_like(lx), lx]).T
        amp_ps.append(float(np.linalg.lstsq(AA, lyI, rcond=None)[0][1]))
        delta_ps.append(float(np.linalg.lstsq(AA, lyd, rcond=None)[0][1]))

    first = g.iloc[0]
    out = {
        "geometry": first["geometry"],
        "fit_c_abs": c_abs,
        "fit_q": q,
        "fit_signed_c": signed_c,
        "I_rel_error_mean": float(np.mean(err)),
        "I_rel_error_max": float(np.max(err)),
        "delta_sign_consistency": sign_consistency,
        "delta_min_abs": float(np.min(np.abs(g["delta_trace_slope"].values))),
        "delta_median_abs": float(np.median(np.abs(g["delta_trace_slope"].values))),
        "amp_power_I_mean": float(np.mean(amp_ps)),
        "amp_power_I_std": float(np.std(amp_ps)),
        "amp_power_delta_mean": float(np.mean(delta_ps)),
        "amp_power_delta_std": float(np.std(delta_ps)),
        "n_rows": int(len(g)),
    }

    for col in ["E0","E1","E2","k_eff","k_eff2","grad_x_energy","grad_y_energy","grad_z_energy",
                "grad_anisotropy","modal_k2_mean","modal_k2_var","modal_entropy","modal_n_eff","n_modes"]:
        out[col] = float(first[col])

    return out

geom_fits = pd.DataFrame([fit_per_geometry(g) for _, g in raw.groupby("geometry")])
geom_fits.to_csv(f"{OUT_PREFIX}_geometry_fits.csv", index=False)

# Descriptor models for log C.
eps = 1e-15
fit_df = geom_fits.copy()
for col in ["fit_c_abs","E0","E1","E2","k_eff","k_eff2","modal_k2_mean","modal_k2_var","modal_n_eff","n_modes"]:
    fit_df["log_"+col] = np.log(fit_df[col].astype(float)+eps)
fit_df["logC"] = np.log(fit_df["fit_c_abs"]+eps)

candidate_models = [
    ("constant", []),
    ("log_E1", ["log_E1"]),
    ("log_E2", ["log_E2"]),
    ("log_k_eff", ["log_k_eff"]),
    ("log_k_eff2", ["log_k_eff2"]),
    ("log_modal_k2_mean", ["log_modal_k2_mean"]),
    ("log_E1+log_modal_k2_var", ["log_E1","log_modal_k2_var"]),
    ("log_E1+log_modal_n_eff", ["log_E1","log_modal_n_eff"]),
    ("log_E1+grad_anisotropy", ["log_E1","grad_anisotropy"]),
    ("log_k_eff+grad_anisotropy", ["log_k_eff","grad_anisotropy"]),
    ("log_E1+log_k_eff+grad_anisotropy", ["log_E1","log_k_eff","grad_anisotropy"]),
]

logo_rows = []
best_by_model = []

for model_name, features in candidate_models:
    preds = []
    true = []
    geoms = []

    for holdout in fit_df["geometry"]:
        train = fit_df[fit_df["geometry"] != holdout]
        test = fit_df[fit_df["geometry"] == holdout]

        if features:
            X = train[features].values.astype(float)
            Xt = test[features].values.astype(float)
            X = np.column_stack([np.ones(len(X)), X])
            Xt = np.column_stack([np.ones(len(Xt)), Xt])
        else:
            X = np.ones((len(train),1))
            Xt = np.ones((len(test),1))

        y = train["logC"].values.astype(float)
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        pred_log = float((Xt@beta)[0])
        true_log = float(test["logC"].iloc[0])
        pred_c = float(np.exp(pred_log))
        true_c = float(test["fit_c_abs"].iloc[0])

        geoms.append(holdout)
        preds.append(pred_c)
        true.append(true_c)

        logo_rows.append({
            "model": model_name,
            "features": "+".join(features) if features else "constant",
            "holdout_geometry": holdout,
            "true_c": true_c,
            "pred_c": pred_c,
            "rel_c_error": abs(pred_c-true_c)/(abs(true_c)+eps),
            "abs_log_error": abs(pred_log-true_log),
        })

    tmp = pd.DataFrame([r for r in logo_rows if r["model"] == model_name])
    best_by_model.append({
        "model": model_name,
        "features": "+".join(features) if features else "constant",
        "n_features": len(features),
        "logo_rel_C_error_mean": float(tmp["rel_c_error"].mean()),
        "logo_rel_C_error_median": float(tmp["rel_c_error"].median()),
        "logo_rel_C_error_max": float(tmp["rel_c_error"].max()),
        "logo_abs_log_error_mean": float(tmp["abs_log_error"].mean()),
        "logo_abs_log_error_max": float(tmp["abs_log_error"].max()),
    })

model_rankings = pd.DataFrame(best_by_model).sort_values(["logo_abs_log_error_mean","logo_rel_C_error_median"])
logo = pd.DataFrame(logo_rows)
model_rankings.to_csv(f"{OUT_PREFIX}_descriptor_model_rankings.csv", index=False)
logo.to_csv(f"{OUT_PREFIX}_leave_one_geometry_out.csv", index=False)

# Attach best descriptor prediction.
best_model = model_rankings.iloc[0]["model"]
best_features = []
for name, feats in candidate_models:
    if name == best_model:
        best_features = feats
        break

if best_features:
    X = fit_df[best_features].values.astype(float)
    X = np.column_stack([np.ones(len(X)), X])
else:
    X = np.ones((len(fit_df),1))
y = fit_df["logC"].values.astype(float)
beta = np.linalg.lstsq(X, y, rcond=None)[0]
pred_log = X@beta
fit_df["pred_logC_best_in_sample"] = pred_log
fit_df["pred_C_best_in_sample"] = np.exp(pred_log)
fit_df["pred_C_best_rel_error_in_sample"] = np.abs(fit_df["pred_C_best_in_sample"]-fit_df["fit_c_abs"])/(fit_df["fit_c_abs"]+eps)
fit_df.to_csv(f"{OUT_PREFIX}_best_descriptor_by_geometry.csv", index=False)

summary = {
    "device": DEVICE,
    "quick_mode": QUICK_MODE,
    "operator_kind": OPERATOR_KIND,
    "window": WINDOW_NAME,
    "n_geometries": int(len(GEOMS)),
    "n_rows": int(len(raw)),
    "N_completed": N_LIST,
    "amp_completed": AMP_LIST,
    "q_mean": float(geom_fits["fit_q"].mean()),
    "q_std": float(geom_fits["fit_q"].std()),
    "q_min": float(geom_fits["fit_q"].min()),
    "q_max": float(geom_fits["fit_q"].max()),
    "I_rel_error_mean": float(geom_fits["I_rel_error_mean"].mean()),
    "I_rel_error_max": float(geom_fits["I_rel_error_max"].max()),
    "delta_sign_consistency_mean": float(geom_fits["delta_sign_consistency"].mean()),
    "amp_power_I_mean": float(geom_fits["amp_power_I_mean"].mean()),
    "amp_power_I_std": float(geom_fits["amp_power_I_mean"].std()),
    "amp_power_delta_mean": float(geom_fits["amp_power_delta_mean"].mean()),
    "amp_power_delta_std": float(geom_fits["amp_power_delta_mean"].std()),
    "best_descriptor_model": str(model_rankings.iloc[0]["model"]),
    "best_descriptor_features": str(model_rankings.iloc[0]["features"]),
    "best_logo_rel_C_error_mean": float(model_rankings.iloc[0]["logo_rel_C_error_mean"]),
    "best_logo_rel_C_error_median": float(model_rankings.iloc[0]["logo_rel_C_error_median"]),
    "best_logo_rel_C_error_max": float(model_rankings.iloc[0]["logo_rel_C_error_max"]),
    "classification": (
        "FROZEN_DX2_LONG_VALIDATED"
        if geom_fits["delta_sign_consistency"].mean() > 0.98
        and geom_fits["I_rel_error_mean"].mean() < 0.25
        and geom_fits["fit_q"].std() < 0.6
        else "FROZEN_DX2_LONG_MIXED"
    )
}

with open(f"{OUT_PREFIX}_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print()
print("================ FROZEN DX2 LONG SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("GEOMETRY_FITS:")
print(geom_fits.to_csv(index=False))

print()
print("DESCRIPTOR_MODEL_RANKINGS:")
print(model_rankings.to_csv(index=False))

print()
print("LEAVE_ONE_GEOMETRY_OUT:")
print(logo.to_csv(index=False))

print()
print("Saved files:")
for name in [
    f"{OUT_PREFIX}_rows.csv",
    f"{OUT_PREFIX}_geometry_fits.csv",
    f"{OUT_PREFIX}_descriptor_model_rankings.csv",
    f"{OUT_PREFIX}_leave_one_geometry_out.csv",
    f"{OUT_PREFIX}_best_descriptor_by_geometry.csv",
    f"{OUT_PREFIX}_summary.json",
]:
    print(name)
