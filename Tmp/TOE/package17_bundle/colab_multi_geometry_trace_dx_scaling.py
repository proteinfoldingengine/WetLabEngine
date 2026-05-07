# ============================================================
# COLAB: Multi-Geometry Trace dx-Scaling Campaign
#
# Purpose:
#   Falsify / validate whether the global heat-trace zero-mode law:
#
#       int R dV ≈ -C0 dx^2 [B(a)-B(0)]
#
#   survives beyond the original single conformal mode:
#
#       phi = a cos(x) cos(y) cos(z)
#
# Tests multiple conformal geometries:
#   1. xyz_product:         cos x cos y cos z
#   2. high_x_product:     cos 2x cos y cos z
#   3. additive_mixed:     cos x + 0.5 cos 2y + 0.25 cos 3z
#   4. two_mode_product:   cos x cos y cos z + 0.35 cos 2x cos 2y cos z
#   5. anisotropic_packet: cos x + 0.35 cos(x+y) + 0.20 cos(2z)
#
# For each geometry:
#   - compute flat B(0) per N
#   - compute delta_B = B(a)-B(0)
#   - compute C_delta = int R dV / delta_B
#   - fit |C_delta| = c dx^q
#   - evaluate prediction error
#
# Recommended:
#   Runtime -> T4 GPU
#
# If full run is slow, set QUICK_MODE=True.
# ============================================================

import time
import json
import numpy as np
import pandas as pd

try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False

USE_GPU_IF_AVAILABLE = True
if TORCH_AVAILABLE and USE_GPU_IF_AVAILABLE and torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print("Torch available:", TORCH_AVAILABLE)
print("Device:", DEVICE)
if DEVICE == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))

QUICK_MODE = True

if QUICK_MODE:
    N_LIST = [8, 10, 12, 14]
    AMP_LIST = [0.08, 0.15, 0.22]
else:
    N_LIST = [8, 10, 12, 14, 16]
    AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25]

GEOMETRY_NAMES = [
    "xyz_product",
    "high_x_product",
    "additive_mixed",
    "two_mode_product",
    "anisotropic_packet",
]

TRACE_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
SAVE_PREFIX = "multi_geometry_trace_dx_scaling_campaign"


# ============================================================
# Geometry definitions with analytic derivatives
# ============================================================

def field_components(name, X, Y, Z):
    # Returns f, fx, fy, fz, lap_f for phi=a*f.
    if name == "xyz_product":
        f = np.cos(X)*np.cos(Y)*np.cos(Z)
        fx = -np.sin(X)*np.cos(Y)*np.cos(Z)
        fy = -np.cos(X)*np.sin(Y)*np.cos(Z)
        fz = -np.cos(X)*np.cos(Y)*np.sin(Z)
        lap = -3*f
        return f, fx, fy, fz, lap

    if name == "high_x_product":
        f = np.cos(2*X)*np.cos(Y)*np.cos(Z)
        fx = -2*np.sin(2*X)*np.cos(Y)*np.cos(Z)
        fy = -np.cos(2*X)*np.sin(Y)*np.cos(Z)
        fz = -np.cos(2*X)*np.cos(Y)*np.sin(Z)
        lap = -(4+1+1)*f
        return f, fx, fy, fz, lap

    if name == "additive_mixed":
        f = np.cos(X) + 0.5*np.cos(2*Y) + 0.25*np.cos(3*Z)
        fx = -np.sin(X)
        fy = -1.0*np.sin(2*Y)
        fz = -0.75*np.sin(3*Z)
        lap = -np.cos(X) - 2.0*np.cos(2*Y) - 2.25*np.cos(3*Z)
        return f, fx, fy, fz, lap

    if name == "two_mode_product":
        f1 = np.cos(X)*np.cos(Y)*np.cos(Z)
        f2 = np.cos(2*X)*np.cos(2*Y)*np.cos(Z)
        f = f1 + 0.35*f2

        fx = -np.sin(X)*np.cos(Y)*np.cos(Z) + 0.35*(-2*np.sin(2*X)*np.cos(2*Y)*np.cos(Z))
        fy = -np.cos(X)*np.sin(Y)*np.cos(Z) + 0.35*(-2*np.cos(2*X)*np.sin(2*Y)*np.cos(Z))
        fz = -np.cos(X)*np.cos(Y)*np.sin(Z) + 0.35*(-np.cos(2*X)*np.cos(2*Y)*np.sin(Z))

        lap = -3*f1 + 0.35*(-(4+4+1)*f2)
        return f, fx, fy, fz, lap

    if name == "anisotropic_packet":
        # cos(x+y): derivatives in x,y and lap=-2 cos(x+y)
        f = np.cos(X) + 0.35*np.cos(X+Y) + 0.20*np.cos(2*Z)
        fx = -np.sin(X) - 0.35*np.sin(X+Y)
        fy = -0.35*np.sin(X+Y)
        fz = -0.40*np.sin(2*Z)
        lap = -np.cos(X) - 0.70*np.cos(X+Y) - 0.80*np.cos(2*Z)
        return f, fx, fy, fz, lap

    raise ValueError(f"Unknown geometry: {name}")


def idx(i,j,k,N):
    return ((i%N)*N+(j%N))*N+(k%N)


def build_conformal_geometry(N, amp, geom_name):
    Lbox = 2*np.pi
    dx = Lbox/N
    x = np.arange(N, dtype=np.float64)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")

    f, fx, fy, fz, lap_f = field_components(geom_name, X, Y, Z)

    phi = amp*f
    grad2 = (amp*fx)**2 + (amp*fy)**2 + (amp*fz)**2
    lap_phi = amp*lap_f

    # 3D conformal scalar curvature:
    # R = e^{-2phi}(-4 lap phi - 2 |grad phi|^2)
    R = np.exp(-2*phi)*(-4*lap_phi - 2*grad2)

    sqrt_h = np.exp(3*phi)
    dV = sqrt_h*dx**3

    return {
        "geometry": geom_name,
        "N":N,
        "nodes":N**3,
        "amp":amp,
        "dx":dx,
        "phi":phi,
        "R":R,
        "sqrt_h":sqrt_h,
        "dV":dV,
        "int_RdV":float(np.sum(R*dV)),
        "volume":float(np.sum(dV)),
        "R_min":float(np.min(R)),
        "R_max":float(np.max(R)),
        "R_std":float(np.std(R)),
    }


def build_dense_laplacian(phi, dx):
    N = phi.shape[0]
    n = N**3
    W = np.zeros((n,n), dtype=np.float64)
    nbrs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i,j,k,N)
                for di,dj,dk in nbrs:
                    ni=(i+di)%N
                    nj=(j+dj)%N
                    nk=(k+dk)%N
                    phimid = 0.5*(phi[i,j,k] + phi[ni,nj,nk])
                    ell = np.exp(phimid)*dx
                    w = np.exp(-(ell*ell)/(4*dx*dx))
                    W[a,idx(ni,nj,nk,N)] = w

    W = 0.5*(W+W.T)
    deg = W.sum(axis=1)
    return (np.diag(deg)-W)/(dx*dx)


def eigvals_only(L_np):
    if DEVICE == "cuda":
        L = torch.tensor(L_np, dtype=torch.float64, device="cuda")
        ev = torch.linalg.eigvalsh(L)
        ev = torch.clamp(ev, min=0)
        out = ev.detach().cpu().numpy()
        del L, ev
        torch.cuda.empty_cache()
        return out
    ev = np.linalg.eigvalsh(L_np)
    return np.maximum(ev, 0)


def trace_slope(evals, dx):
    times = TRACE_TIME_MULTIPLIERS*dx*dx
    H = []
    for t in times:
        tr = np.sum(np.exp(-float(t)*evals))
        H.append(tr*((4*np.pi*t)**1.5))
    H = np.array(H)
    m,b = np.polyfit(times,H,1)
    return float(m), float(b), float(H.mean()), float(H.std())


def compute_case(N, amp, geom_name):
    t0=time.time()
    geom = build_conformal_geometry(N, amp, geom_name)
    L = build_dense_laplacian(geom["phi"], geom["dx"])
    ev = eigvals_only(L)
    m,b,hm,hs = trace_slope(ev, geom["dx"])
    return {
        "geometry":geom_name,
        "N":N,
        "nodes":N**3,
        "amp":amp,
        "dx":geom["dx"],
        "int_RdV":geom["int_RdV"],
        "volume":geom["volume"],
        "R_min":geom["R_min"],
        "R_max":geom["R_max"],
        "R_std":geom["R_std"],
        "trace_slope":m,
        "trace_intercept":b,
        "trace_H_mean":hm,
        "trace_H_std":hs,
        "seconds":round(time.time()-t0,3),
    }


def fit_power_law(df):
    x = np.log(df["dx"].values)
    y = np.log(df["abs_C_delta"].values)
    A = np.vstack([np.ones_like(x), x]).T
    coef = np.linalg.lstsq(A,y,rcond=None)[0]
    logc,q = coef
    return float(np.exp(logc)), float(q)


def apply_model(df, c, q):
    out = df.copy()
    out["C_delta_pred"] = -c*(out["dx"]**q)
    out["I_pred"] = out["C_delta_pred"]*out["delta_trace_slope"]
    out["I_rel_error"] = np.abs(out["I_pred"]-out["delta_int_RdV"])/(np.abs(out["delta_int_RdV"])+1e-12)
    out["C_scaled"] = out["C_delta_required"]/(out["dx"]**q)
    return out


print()
print("Running multi-geometry trace dx-scaling campaign...")
print("QUICK_MODE:", QUICK_MODE)
print("GEOMETRIES:", GEOMETRY_NAMES)
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("DEVICE:", DEVICE)
print()

rows=[]
flat_cache={}

for geom_name in GEOMETRY_NAMES:
    print()
    print("="*80)
    print("GEOMETRY:", geom_name)
    print("="*80)

    for N in N_LIST:
        print(f"--- Flat reference geometry={geom_name}, N={N} ---")
        flat = compute_case(N, 0.0, geom_name)
        flat_cache[(geom_name,N)] = flat
        print(json.dumps(flat, indent=2))

    for N in N_LIST:
        B0 = flat_cache[(geom_name,N)]["trace_slope"]
        I0 = flat_cache[(geom_name,N)]["int_RdV"]

        for amp in AMP_LIST:
            print(f"--- geometry={geom_name}, N={N}, amp={amp} ---")
            r = compute_case(N, amp, geom_name)
            dB = r["trace_slope"] - B0
            dI = r["int_RdV"] - I0
            r.update({
                "flat_trace_slope":B0,
                "delta_trace_slope":dB,
                "delta_int_RdV":dI,
                "C_delta_required":float(dI/(dB+1e-12)),
                "abs_C_delta":float(abs(dI/(dB+1e-12))),
            })
            rows.append(r)
            print(json.dumps(r, indent=2))


df = pd.DataFrame(rows)

geom_summaries = []
pred_rows = []

for geom_name, gdf in df.groupby("geometry"):
    c,q = fit_power_law(gdf)
    pdf = apply_model(gdf,c,q)
    pred_rows.append(pdf)
    geom_summaries.append({
        "geometry":geom_name,
        "n_rows":int(len(gdf)),
        "fit_c":c,
        "fit_q":q,
        "I_rel_error_mean":float(pdf["I_rel_error"].mean()),
        "I_rel_error_max":float(pdf["I_rel_error"].max()),
        "C_scaled_mean":float(pdf["C_scaled"].mean()),
        "C_scaled_cv":float(pdf["C_scaled"].std()/(abs(pdf["C_scaled"].mean())+1e-12)),
    })

pred_df = pd.concat(pred_rows, ignore_index=True)
geom_summary_df = pd.DataFrame(geom_summaries)

# One universal fit across all geometries:
c_all, q_all = fit_power_law(df)
universal_pred = apply_model(df, c_all, q_all)

summary = {
    "device":DEVICE,
    "quick_mode":QUICK_MODE,
    "n_rows":int(len(df)),
    "geometries":GEOMETRY_NAMES,
    "N_completed":sorted(df["N"].unique().tolist()),
    "amp_completed":sorted(df["amp"].unique().tolist()),
    "universal_fit_c":c_all,
    "universal_fit_q":q_all,
    "universal_I_rel_error_mean":float(universal_pred["I_rel_error"].mean()),
    "universal_I_rel_error_max":float(universal_pred["I_rel_error"].max()),
    "universal_C_scaled_cv":float(universal_pred["C_scaled"].std()/(abs(universal_pred["C_scaled"].mean())+1e-12)),
    "per_geometry_q_mean":float(geom_summary_df["fit_q"].mean()),
    "per_geometry_q_std":float(geom_summary_df["fit_q"].std()),
    "per_geometry_c_mean":float(geom_summary_df["fit_c"].mean()),
    "per_geometry_c_std":float(geom_summary_df["fit_c"].std()),
    "classification":(
        "MULTI_GEOMETRY_TRACE_DX_SCALING_PROMISING"
        if geom_summary_df["fit_q"].between(1.7,2.3).all()
        and geom_summary_df["I_rel_error_max"].max() < 0.08
        else "MULTI_GEOMETRY_TRACE_DX_SCALING_MIXED"
    )
}

df.to_csv(f"{SAVE_PREFIX}_raw_rows.csv", index=False)
pred_df.to_csv(f"{SAVE_PREFIX}_per_geometry_pred_rows.csv", index=False)
universal_pred.to_csv(f"{SAVE_PREFIX}_universal_pred_rows.csv", index=False)
geom_summary_df.to_csv(f"{SAVE_PREFIX}_geometry_summary.csv", index=False)

with open(f"{SAVE_PREFIX}_summary.json","w") as f:
    json.dump(summary,f,indent=2)

print()
print("================ MULTI-GEOMETRY TRACE DX SCALING SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("GEOMETRY_SUMMARY:")
print(geom_summary_df.to_csv(index=False))

print()
print("UNIVERSAL_PRED_ROWS:")
print(universal_pred.to_csv(index=False))

print()
print("Saved files:")
print(f"{SAVE_PREFIX}_raw_rows.csv")
print(f"{SAVE_PREFIX}_per_geometry_pred_rows.csv")
print(f"{SAVE_PREFIX}_universal_pred_rows.csv")
print(f"{SAVE_PREFIX}_geometry_summary.csv")
print(f"{SAVE_PREFIX}_summary.json")
