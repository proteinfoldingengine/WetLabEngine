# ============================================================
# COLAB: Trace dx-Scaling Campaign
#
# Purpose:
#   Continue from delta-trace result.
#
# Test:
#   C_delta(N,a) = I_R(a) / [B_trace(N,a)-B_trace(N,0)]
#
# Fit:
#   |C_delta| = c * dx^q
#
# Then predict:
#   I_R_hat = -c * dx^q * Delta_B
#
# Recommended:
#   Run with T4 GPU if available.
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
    N_LIST = [8, 10, 12, 14, 16, 18]
    AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25]

TRACE_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
SAVE_PREFIX = "trace_dx_scaling_campaign"


def idx(i,j,k,N):
    return ((i%N)*N+(j%N))*N+(k%N)


def build_conformal_geometry(N, amp):
    Lbox = 2*np.pi
    dx = Lbox/N
    x = np.arange(N, dtype=np.float64)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    f = np.cos(X)*np.cos(Y)*np.cos(Z)
    phi = amp*f

    lap_phi = -3*amp*f
    phix = -amp*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy = -amp*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz = -amp*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2 = phix*phix + phiy*phiy + phiz*phiz

    R = np.exp(-2*phi)*(-4*lap_phi - 2*grad2)
    sqrt_h = np.exp(3*phi)
    dV = sqrt_h*dx**3

    return {
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
    }


def build_dense_laplacian(phi, dx):
    N=phi.shape[0]
    n=N**3
    W=np.zeros((n,n), dtype=np.float64)
    nbrs=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a=idx(i,j,k,N)
                for di,dj,dk in nbrs:
                    ni=(i+di)%N
                    nj=(j+dj)%N
                    nk=(k+dk)%N
                    phimid=0.5*(phi[i,j,k]+phi[ni,nj,nk])
                    ell=np.exp(phimid)*dx
                    w=np.exp(-(ell*ell)/(4*dx*dx))
                    W[a,idx(ni,nj,nk,N)] = w

    W=0.5*(W+W.T)
    deg=W.sum(axis=1)
    return (np.diag(deg)-W)/(dx*dx)


def eigvals_only(L_np):
    if DEVICE == "cuda":
        L=torch.tensor(L_np, dtype=torch.float64, device="cuda")
        evals=torch.linalg.eigvalsh(L)
        evals=torch.clamp(evals,min=0)
        out=evals.detach().cpu().numpy()
        del L, evals
        torch.cuda.empty_cache()
        return out
    evals=np.linalg.eigvalsh(L_np)
    return np.maximum(evals,0)


def trace_slope(evals, dx):
    times = TRACE_TIME_MULTIPLIERS*dx*dx
    H=[]
    for t in times:
        tr=np.sum(np.exp(-float(t)*evals))
        H.append(tr*((4*np.pi*t)**1.5))
    H=np.array(H)
    m,b=np.polyfit(times,H,1)
    return float(m), float(b), float(H.mean()), float(H.std())


def compute_case(N, amp):
    t0=time.time()
    geom=build_conformal_geometry(N, amp)
    L=build_dense_laplacian(geom["phi"], geom["dx"])
    ev=eigvals_only(L)
    m,b,hm,hs=trace_slope(ev, geom["dx"])
    return {
        "N":N,
        "nodes":N**3,
        "amp":amp,
        "dx":geom["dx"],
        "int_RdV":geom["int_RdV"],
        "volume":geom["volume"],
        "trace_slope":m,
        "trace_intercept":b,
        "trace_H_mean":hm,
        "trace_H_std":hs,
        "seconds":round(time.time()-t0,3),
    }


print()
print("Running trace dx-scaling campaign...")
print("QUICK_MODE:", QUICK_MODE)
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("DEVICE:", DEVICE)
print()

flat={}
for N in N_LIST:
    print(f"--- Flat N={N} ---")
    flat[N]=compute_case(N,0.0)
    print(json.dumps(flat[N],indent=2))

rows=[]
for N in N_LIST:
    B0=flat[N]["trace_slope"]
    I0=flat[N]["int_RdV"]
    for amp in AMP_LIST:
        print(f"--- N={N}, amp={amp} ---")
        r=compute_case(N,amp)
        dB=r["trace_slope"]-B0
        dI=r["int_RdV"]-I0
        r.update({
            "flat_trace_slope":B0,
            "delta_trace_slope":dB,
            "delta_int_RdV":dI,
            "C_delta_required":float(dI/(dB+1e-12)),
            "abs_C_delta":float(abs(dI/(dB+1e-12))),
        })
        rows.append(r)
        print(json.dumps(r,indent=2))

df=pd.DataFrame(rows)

# Fit log |C| = log c + q log dx.
x=np.log(df["dx"].values)
y=np.log(df["abs_C_delta"].values)
A=np.vstack([np.ones_like(x),x]).T
coef=np.linalg.lstsq(A,y,rcond=None)[0]
logc,q=coef
c=float(np.exp(logc))
q=float(q)

# Sign is negative from observed C_delta.
df["C_delta_pred"] = -c*(df["dx"]**q)
df["I_pred"] = df["C_delta_pred"]*df["delta_trace_slope"]
df["I_rel_error"] = np.abs(df["I_pred"]-df["delta_int_RdV"])/(np.abs(df["delta_int_RdV"])+1e-12)
df["C_scaled"] = df["C_delta_required"]/(df["dx"]**q)

summary={
    "device":DEVICE,
    "quick_mode":QUICK_MODE,
    "n_rows":len(df),
    "N_completed":sorted(df["N"].unique().tolist()),
    "amp_completed":sorted(df["amp"].unique().tolist()),
    "fit_c":c,
    "fit_q":q,
    "C_scaled_mean":float(df["C_scaled"].mean()),
    "C_scaled_std":float(df["C_scaled"].std()),
    "C_scaled_cv":float(df["C_scaled"].std()/(abs(df["C_scaled"].mean())+1e-12)),
    "I_prediction_rel_error_mean":float(df["I_rel_error"].mean()),
    "I_prediction_rel_error_max":float(df["I_rel_error"].max()),
    "classification":(
        "TRACE_DX_SCALING_PROMISING"
        if df["I_rel_error"].max()<0.08 and (df["C_scaled"].std()/(abs(df["C_scaled"].mean())+1e-12))<0.10
        else "TRACE_DX_SCALING_MIXED"
    )
}

df.to_csv(f"{SAVE_PREFIX}_rows.csv", index=False)
with open(f"{SAVE_PREFIX}_summary.json","w") as f:
    json.dump(summary,f,indent=2)

print()
print("================ TRACE DX SCALING SUMMARY ================")
print(json.dumps(summary, indent=2))
print()
print("TRACE_DX_ROWS:")
print(df.to_csv(index=False))
print()
print("Saved files:")
print(f"{SAVE_PREFIX}_rows.csv")
print(f"{SAVE_PREFIX}_summary.json")
