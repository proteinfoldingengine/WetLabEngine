# ============================================================
# COLAB: Heat Normalization Delta-Trace Campaign
#
# Fixes from quick campaign:
#   1. Trace zero-mode uses background-subtracted slope:
#        Delta_B = B_trace(amp) - B_trace(0)
#
#   2. Local p test reports:
#        raw scale required by geometry
#        scale stability across N/amp
#      Note: p cannot be identified if each case gets an independent scale.
#
# Recommended:
#   Runtime -> T4 GPU
#   Start QUICK_MODE=True
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
    N_LIST = [8, 10, 12]
    AMP_LIST = [0.08, 0.15, 0.22]
else:
    N_LIST = [8, 10, 12, 14, 16]
    AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25]

P_LIST = [0.0, 0.5, 1.0, 1.5, 2.0]
SIGN_LIST = [6.0, -6.0]

LOCAL_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8], dtype=np.float64)
TRACE_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
SAVE_PREFIX = "heat_delta_trace_campaign"


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
        "N": N,
        "nodes": N**3,
        "amp": amp,
        "dx": dx,
        "phi": phi,
        "R": R,
        "sqrt_h": sqrt_h,
        "dV": dV,
        "int_RdV": float(np.sum(R*dV)),
        "volume": float(np.sum(dV)),
    }


def idx(i,j,k,N):
    return ((i%N)*N+(j%N))*N+(k%N)


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
    L=(np.diag(deg)-W)/(dx*dx)
    return L


def eig_system(L_np):
    if DEVICE == "cuda":
        L=torch.tensor(L_np, dtype=torch.float64, device="cuda")
        evals,evecs=torch.linalg.eigh(L)
        evals=torch.clamp(evals,min=0)
        evals_np=evals.detach().cpu().numpy()
        evecs_np=evecs.detach().cpu().numpy()
        del L, evals, evecs
        torch.cuda.empty_cache()
        return evals_np, evecs_np

    evals,evecs=np.linalg.eigh(L_np)
    return np.maximum(evals,0), evecs


def corr(a,b):
    a=np.asarray(a).ravel()
    b=np.asarray(b).ravel()
    a=a-a.mean()
    b=b-b.mean()
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))


def fit_centered_scale(x,y):
    x=(x-x.mean()).ravel()
    y=(y-y.mean()).ravel()
    return float(np.dot(x,y)/(np.dot(x,x)+1e-12))


def rel_l2(a,b):
    return float(np.linalg.norm((np.asarray(a)-np.asarray(b)).ravel())/(np.linalg.norm(np.asarray(b).ravel())+1e-12))


def local_heat_slope_field(evals,evecs,dx,N):
    times=LOCAL_TIME_MULTIPLIERS*dx*dx
    V2=evecs*evecs
    Ys=[]
    for t in times:
        diag=V2@np.exp(-float(t)*evals)
        Ys.append(diag*((4*np.pi*t)**1.5))
    Y=np.array(Ys)
    slopes=np.empty(N**3,dtype=np.float64)
    for i in range(N**3):
        m,_=np.polyfit(times,Y[:,i],1)
        slopes[i]=m
    return slopes.reshape(N,N,N)


def trace_slope(evals,dx):
    times=TRACE_TIME_MULTIPLIERS*dx*dx
    H=[]
    for t in times:
        tr=np.sum(np.exp(-float(t)*evals))
        H.append(tr*((4*np.pi*t)**1.5))
    H=np.array(H)
    m,b=np.polyfit(times,H,1)
    return float(m), float(b), float(H.mean()), float(H.std())


def compute_case(N, amp, need_local=True):
    t0=time.time()
    geom=build_conformal_geometry(N, amp)
    L=build_dense_laplacian(geom["phi"], geom["dx"])
    evals,evecs=eig_system(L)
    tr_m,tr_b,tr_mean,tr_std=trace_slope(evals, geom["dx"])

    out={
        "N":N,
        "nodes":N**3,
        "amp":amp,
        "dx":geom["dx"],
        "int_RdV":geom["int_RdV"],
        "volume":geom["volume"],
        "trace_slope":tr_m,
        "trace_intercept":tr_b,
        "trace_H_mean":tr_mean,
        "trace_H_std":tr_std,
        "total_seconds":round(time.time()-t0,3),
    }

    if need_local:
        B=local_heat_slope_field(evals,evecs,geom["dx"],N)
        local_rows=[]
        for sign in SIGN_LIST:
            for p in P_LIST:
                Rhat=sign*B/(geom["dx"]**p)
                s=fit_centered_scale(Rhat,geom["R"])
                Rscaled=s*(Rhat-Rhat.mean())
                target=geom["R"]-geom["R"].mean()
                local_rows.append({
                    "N":N,
                    "nodes":N**3,
                    "amp":amp,
                    "dx":geom["dx"],
                    "sign":sign,
                    "p":p,
                    "corr_raw":corr(Rhat,geom["R"]),
                    "required_scale":s,
                    "relL2_centered_scaled":rel_l2(Rscaled,target),
                })
        return out, local_rows

    return out, []


print()
print("Running heat normalization delta-trace campaign...")
print("QUICK_MODE:", QUICK_MODE)
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("DEVICE:", DEVICE)
print()

flat_by_N={}
for N in N_LIST:
    print(f"--- Running flat reference N={N}, amp=0 ---")
    flat, _ = compute_case(N, 0.0, need_local=False)
    flat_by_N[N]=flat
    print(json.dumps(flat, indent=2))

all_trace=[]
all_local=[]

for N in N_LIST:
    B0=flat_by_N[N]["trace_slope"]
    I0=flat_by_N[N]["int_RdV"]

    for amp in AMP_LIST:
        print(f"--- Running N={N}, amp={amp} ({N**3} nodes) ---")
        case, local_rows=compute_case(N, amp, need_local=True)
        delta_B=case["trace_slope"]-B0
        delta_I=case["int_RdV"]-I0

        case.update({
            "flat_trace_slope":B0,
            "flat_int_RdV":I0,
            "delta_trace_slope":delta_B,
            "delta_int_RdV":delta_I,
            "C_delta_required":float(delta_I/(delta_B+1e-12)),
        })
        all_trace.append(case)
        all_local.extend(local_rows)
        print(json.dumps(case, indent=2))

local_df=pd.DataFrame(all_local)
trace_df=pd.DataFrame(all_trace)

local_summary=(
    local_df.groupby(["sign","p"])
    .agg(
        corr_mean=("corr_raw","mean"),
        corr_min=("corr_raw","min"),
        scale_mean=("required_scale","mean"),
        scale_std=("required_scale","std"),
        relL2_mean=("relL2_centered_scaled","mean"),
        relL2_max=("relL2_centered_scaled","max"),
    )
    .reset_index()
)
local_summary["scale_cv"]=local_summary["scale_std"]/(local_summary["scale_mean"].abs()+1e-12)
local_summary=local_summary.sort_values(by=["corr_mean","scale_cv","relL2_mean"], ascending=[False,True,True])

trace_summary={
    "C_delta_required_mean":float(trace_df["C_delta_required"].mean()),
    "C_delta_required_std":float(trace_df["C_delta_required"].std()),
    "C_delta_required_cv":float(trace_df["C_delta_required"].std()/(abs(trace_df["C_delta_required"].mean())+1e-12)),
    "C_delta_required_min":float(trace_df["C_delta_required"].min()),
    "C_delta_required_max":float(trace_df["C_delta_required"].max()),
}

summary={
    "device":DEVICE,
    "quick_mode":QUICK_MODE,
    "n_geometries":len(trace_df),
    "N_completed":sorted(trace_df["N"].unique().tolist()),
    "amp_completed":sorted(trace_df["amp"].unique().tolist()),
    "best_local_candidate":local_summary.iloc[0].to_dict(),
    "trace_delta_summary":trace_summary,
    "classification":(
        "HEAT_DELTA_TRACE_TARGET_PROMISING"
        if local_summary.iloc[0]["corr_min"]>0.90 and trace_summary["C_delta_required_cv"]<0.25
        else "HEAT_DELTA_TRACE_TARGET_MIXED"
    )
}

local_df.to_csv(f"{SAVE_PREFIX}_local_rows.csv", index=False)
local_summary.to_csv(f"{SAVE_PREFIX}_local_summary.csv", index=False)
trace_df.to_csv(f"{SAVE_PREFIX}_trace_rows.csv", index=False)

with open(f"{SAVE_PREFIX}_summary.json","w") as f:
    json.dump(summary,f,indent=2)

print()
print("================ HEAT DELTA TRACE CAMPAIGN SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("LOCAL_CANDIDATE_SUMMARY:")
print(local_summary.to_csv(index=False))

print()
print("TRACE_DELTA_SUMMARY:")
print(json.dumps(trace_summary, indent=2))

print()
print("TRACE_DELTA_ROWS:")
print(trace_df.to_csv(index=False))

print()
print("Saved files:")
print(f"{SAVE_PREFIX}_local_rows.csv")
print(f"{SAVE_PREFIX}_local_summary.csv")
print(f"{SAVE_PREFIX}_trace_rows.csv")
print(f"{SAVE_PREFIX}_summary.json")
