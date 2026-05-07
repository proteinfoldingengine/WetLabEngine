# ============================================================
# COLAB: Trace dx-Scaling Full + Held-Out Campaign
#
# Purpose:
#   Validate the quick result:
#      C_delta(dx) ≈ -c dx^q
#
# Adds:
#   - larger N set
#   - larger amplitude set
#   - train/test split by amplitude and grid
#   - held-out prediction error
#
# Recommended:
#   Runtime -> T4 GPU
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

# Start with these. If N=18 is too slow, remove it.
N_LIST = [8, 10, 12, 14, 16, 18]
AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25]

TRACE_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
SAVE_PREFIX = "trace_dx_scaling_full_heldout_campaign"


def idx(i,j,k,N):
    return ((i%N)*N+(j%N))*N+(k%N)


def build_conformal_geometry(N, amp):
    Lbox=2*np.pi
    dx=Lbox/N
    x=np.arange(N, dtype=np.float64)*dx
    X,Y,Z=np.meshgrid(x,x,x,indexing="ij")
    f=np.cos(X)*np.cos(Y)*np.cos(Z)
    phi=amp*f

    lap_phi=-3*amp*f
    phix=-amp*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy=-amp*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz=-amp*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2=phix*phix+phiy*phiy+phiz*phiz

    R=np.exp(-2*phi)*(-4*lap_phi-2*grad2)
    sqrt_h=np.exp(3*phi)
    dV=sqrt_h*dx**3

    return {
        "N":N,
        "nodes":N**3,
        "amp":amp,
        "dx":dx,
        "phi":phi,
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
        ev=torch.linalg.eigvalsh(L)
        ev=torch.clamp(ev,min=0)
        out=ev.detach().cpu().numpy()
        del L, ev
        torch.cuda.empty_cache()
        return out
    ev=np.linalg.eigvalsh(L_np)
    return np.maximum(ev,0)


def trace_slope(evals, dx):
    times=TRACE_TIME_MULTIPLIERS*dx*dx
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


def fit_power_law(train_df):
    x=np.log(train_df["dx"].values)
    y=np.log(train_df["abs_C_delta"].values)
    A=np.vstack([np.ones_like(x),x]).T
    coef=np.linalg.lstsq(A,y,rcond=None)[0]
    logc,q=coef
    return float(np.exp(logc)), float(q)


def apply_model(df, c, q):
    out=df.copy()
    out["C_delta_pred"]=-c*(out["dx"]**q)
    out["I_pred"]=out["C_delta_pred"]*out["delta_trace_slope"]
    out["I_rel_error"]=np.abs(out["I_pred"]-out["delta_int_RdV"])/(np.abs(out["delta_int_RdV"])+1e-12)
    out["C_scaled"]=out["C_delta_required"]/(out["dx"]**q)
    return out


print()
print("Running trace dx-scaling full held-out campaign...")
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

# Split 1: train on N<=14, test on N>=16
train_N=df[df["N"]<=14]
test_N=df[df["N"]>=16]
cN,qN=fit_power_law(train_N)
train_N_pred=apply_model(train_N,cN,qN)
test_N_pred=apply_model(test_N,cN,qN) if len(test_N)>0 else pd.DataFrame()

# Split 2: train on middle amplitudes, test on edge amplitudes
train_amp=df[df["amp"].isin([0.08,0.10,0.12,0.15,0.18,0.20,0.22])]
test_amp=df[df["amp"].isin([0.05,0.25])]
cA,qA=fit_power_law(train_amp)
train_amp_pred=apply_model(train_amp,cA,qA)
test_amp_pred=apply_model(test_amp,cA,qA)

# All data fit
cAll,qAll=fit_power_law(df)
all_pred=apply_model(df,cAll,qAll)

def summarize_pred(name,pred):
    if len(pred)==0:
        return {f"{name}_n":0}
    return {
        f"{name}_n":int(len(pred)),
        f"{name}_I_rel_error_mean":float(pred["I_rel_error"].mean()),
        f"{name}_I_rel_error_max":float(pred["I_rel_error"].max()),
        f"{name}_C_scaled_cv":float(pred["C_scaled"].std()/(abs(pred["C_scaled"].mean())+1e-12)),
    }

summary={
    "device":DEVICE,
    "n_rows":int(len(df)),
    "N_completed":sorted(df["N"].unique().tolist()),
    "amp_completed":sorted(df["amp"].unique().tolist()),

    "all_fit_c":cAll,
    "all_fit_q":qAll,
    **summarize_pred("all_fit",all_pred),

    "train_N_fit_c":cN,
    "train_N_fit_q":qN,
    **summarize_pred("train_N",train_N_pred),
    **summarize_pred("heldout_N",test_N_pred),

    "train_amp_fit_c":cA,
    "train_amp_fit_q":qA,
    **summarize_pred("train_amp",train_amp_pred),
    **summarize_pred("heldout_amp",test_amp_pred),
}

summary["classification"]=(
    "TRACE_DX_SCALING_FULL_HELDOUT_PROMISING"
    if summary.get("heldout_amp_I_rel_error_max", 999)<0.03
    and (summary.get("heldout_N_I_rel_error_max", 0)<0.05 if summary.get("heldout_N_n",0)>0 else True)
    else "TRACE_DX_SCALING_FULL_HELDOUT_MIXED"
)

df.to_csv(f"{SAVE_PREFIX}_rows.csv",index=False)
all_pred.to_csv(f"{SAVE_PREFIX}_all_pred_rows.csv",index=False)
train_N_pred.to_csv(f"{SAVE_PREFIX}_train_N_pred_rows.csv",index=False)
test_N_pred.to_csv(f"{SAVE_PREFIX}_heldout_N_pred_rows.csv",index=False)
train_amp_pred.to_csv(f"{SAVE_PREFIX}_train_amp_pred_rows.csv",index=False)
test_amp_pred.to_csv(f"{SAVE_PREFIX}_heldout_amp_pred_rows.csv",index=False)

with open(f"{SAVE_PREFIX}_summary.json","w") as f:
    json.dump(summary,f,indent=2)

print()
print("================ TRACE DX SCALING FULL HELDOUT SUMMARY ================")
print(json.dumps(summary,indent=2))
print()
print("ALL_PRED_ROWS:")
print(all_pred.to_csv(index=False))
print()
print("HELDOUT_N_ROWS:")
print(test_N_pred.to_csv(index=False) if len(test_N_pred)>0 else "No N heldout rows.")
print()
print("HELDOUT_AMP_ROWS:")
print(test_amp_pred.to_csv(index=False))
print()
print("Saved files with prefix:", SAVE_PREFIX)
