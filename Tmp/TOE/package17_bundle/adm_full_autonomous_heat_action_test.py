# ============================================================
# ADM Full Autonomous Heat Action Test
# GEM Bridge / Autonomous Heat Spatial R^(3) + Graph Kinetic Proxy
#
# Purpose:
#   Upgrade the full ADM geometric proxy by replacing the degree-based
#   spatial curvature term with the stronger autonomous heat reconstruction:
#
#       R_heat_auto = local dx-normalized heat diagonal + heat-trace zero mode
#
#   Then combine with graph kinetic proxy:
#
#       K_proxy = -6 phidot_hat^2
#
#   Target:
#
#       I_ADM = ∫ N sqrt(h) [R^(3) + K_ij K^ij - K^2] d^3x
#
# Scope:
#   Diagnostic only. The spatial heat zero mode is calibrated from amplitude
#   references. The kinetic proxy still uses fitted phidot scale.
#
# Recommended:
#   CPU works for N<=14. T4 also works.
# ============================================================

import time
import json
import numpy as np

try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False


USE_GPU_IF_AVAILABLE = True

N_LIST = [8, 10, 12, 14]
TEST_AMP = 0.15
OMEGA = 0.30
T0 = 0.7
DT = 1e-3

CALIBRATION_AMPS = [0.05, 0.08, 0.10, 0.12, 0.18, 0.20, 0.25]

TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
LOCAL_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8], dtype=np.float64)

PASS_ADM_ACTION_REL_ERR = 0.10
PASS_DENSITY_CORR = 0.95
PASS_LOCAL_ADM_CORR = 0.95


if TORCH_AVAILABLE and USE_GPU_IF_AVAILABLE and torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print("Torch available:", TORCH_AVAILABLE)
print("Device:", DEVICE)
if DEVICE == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


def conformal_fields(N, amp=0.15, omega=0.30, t=0.7):
    Lbox = 2*np.pi
    dx = Lbox/N
    x = np.arange(N, dtype=np.float64)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    f = np.cos(X)*np.cos(Y)*np.cos(Z)

    phi = amp*np.cos(omega*t)*f
    phidot = -amp*omega*np.sin(omega*t)*f

    lap_phi = -3*amp*np.cos(omega*t)*f
    phix = -amp*np.cos(omega*t)*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy = -amp*np.cos(omega*t)*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz = -amp*np.cos(omega*t)*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2 = phix*phix + phiy*phiy + phiz*phiz

    R3 = np.exp(-2*phi)*(-4*lap_phi - 2*grad2)
    sqrt_h = np.exp(3*phi)
    dV = sqrt_h*dx**3
    rho = R3*dV

    kinetic = -6*phidot*phidot
    ADM = R3 + kinetic

    return {
        "N": N,
        "nodes": N**3,
        "dx": dx,
        "X": X, "Y": Y, "Z": Z,
        "phi": phi,
        "phidot": phidot,
        "R3": R3,
        "sqrt_h": sqrt_h,
        "dV": dV,
        "rho": rho,
        "kinetic": kinetic,
        "ADM": ADM,
        "volume": float(np.sum(dV)),
        "int_RdV": float(np.sum(rho)),
    }


def phi_only(N, amp=0.15, omega=0.30, t=0.7):
    Lbox = 2*np.pi
    dx = Lbox/N
    x = np.arange(N, dtype=np.float64)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    phi = amp*np.cos(omega*t)*np.cos(X)*np.cos(Y)*np.cos(Z)
    return phi, dx


def build_laplacian_from_phi(phi, dx):
    N = phi.shape[0]
    n = N**3
    W = np.zeros((n,n), dtype=np.float64)

    def idx(i,j,k):
        return ((i % N)*N + (j % N))*N + (k % N)

    nbrs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i,j,k)
                for di,dj,dk in nbrs:
                    ni=(i+di)%N
                    nj=(j+dj)%N
                    nk=(k+dk)%N
                    phimid=0.5*(phi[i,j,k]+phi[ni,nj,nk])
                    ell=np.exp(phimid)*dx
                    w=np.exp(-(ell*ell)/(4*dx*dx))
                    W[a,idx(ni,nj,nk)] = w

    W = 0.5*(W+W.T)
    deg = W.sum(axis=1)
    L = (np.diag(deg)-W)/(dx*dx)
    return L, deg.reshape(N,N,N)


def eig_system(L_np, device="cpu"):
    if device == "cuda":
        L = torch.tensor(L_np, dtype=torch.float64, device=device)
        evals, evecs = torch.linalg.eigh(L)
        evals = torch.clamp(evals, min=0.0)
        evals_np = evals.detach().cpu().numpy()
        evecs_np = evecs.detach().cpu().numpy()
        del L, evals, evecs
        torch.cuda.empty_cache()
        return evals_np, evecs_np
    evals, evecs = np.linalg.eigh(L_np)
    evals = np.maximum(evals, 0.0)
    return evals, evecs


def heat_trace_features(evals, dx):
    times = TIME_MULTIPLIERS*dx*dx
    traces = np.array([np.sum(np.exp(-float(t)*evals)) for t in times])
    H = traces*((4*np.pi*times)**1.5)

    m,b = np.polyfit(times,H,1)
    a2,b2,c2 = np.polyfit(times,H,2)

    return {
        "trace_slope_6m_linear": float(6*m),
        "trace_intercept_linear": float(b),
        "trace_quad_slope_6b": float(6*b2),
        "trace_quad_intercept": float(c2),
        "trace_H_mean": float(np.mean(H)),
    }


def local_heat_Rhat(evals, evecs, dx, N):
    times = LOCAL_TIME_MULTIPLIERS*dx*dx
    V2 = evecs*evecs

    diags=[]
    for t in times:
        weights = np.exp(-float(t)*evals)
        diags.append(V2 @ weights)

    diags=np.array(diags)
    Y = diags*((4*np.pi*times)[:,None]**1.5)

    slopes=np.empty(Y.shape[1], dtype=np.float64)
    for i in range(Y.shape[1]):
        m,_=np.polyfit(times,Y[:,i],1)
        slopes[i]=m

    return ((-6.0*slopes)/dx).reshape(N,N,N)


def corr(a,b):
    a=np.asarray(a).ravel()
    b=np.asarray(b).ravel()
    a=a-np.mean(a)
    b=b-np.mean(b)
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))


def fit_linear(x,y):
    x=np.asarray(x,dtype=np.float64)
    y=np.asarray(y,dtype=np.float64)
    A=np.vstack([np.ones_like(x),x]).T
    coef=np.linalg.lstsq(A,y,rcond=None)[0]
    pred=A@coef
    rel=float(np.linalg.norm(pred-y)/(np.linalg.norm(y)+1e-12))
    r2=float(1-np.sum((y-pred)**2)/(np.sum((y-y.mean())**2)+1e-12))
    return coef, rel, r2


def fit_centered_scale(x,y):
    x=(x-np.mean(x)).ravel()
    y=(y-np.mean(y)).ravel()
    return float(np.dot(x,y)/(np.dot(x,x)+1e-12))


def degree_field(phi, dx):
    _, deg = build_laplacian_from_phi(phi, dx)
    return deg


def kinetic_proxy_from_degree_time(N, amp, omega, t, dt, dx, phidot_true):
    phi_p,_ = phi_only(N, amp, omega, t+dt)
    phi_m,_ = phi_only(N, amp, omega, t-dt)
    deg_p = degree_field(phi_p, dx)
    deg_m = degree_field(phi_m, dx)
    degdot = (deg_p-deg_m)/(2*dt)

    s = fit_centered_scale(degdot, phidot_true)
    phidot_hat = s*(degdot-np.mean(degdot)) + np.mean(phidot_true)
    K_hat = -6*phidot_hat*phidot_hat

    return {
        "degdot": degdot,
        "phidot_hat": phidot_hat,
        "K_hat": K_hat,
        "scale_phidot": s,
        "phidot_corr": corr(phidot_hat, phidot_true),
    }


def lapse_field(kind,X,Y,Z):
    if kind == "unit":
        return np.ones_like(X)
    if kind == "smooth_positive":
        return 1.0 + 0.10*np.cos(X) + 0.05*np.sin(Y+Z)
    if kind == "curvature_coupled":
        return 1.0 + 0.10*np.cos(X)*np.cos(Y)*np.cos(Z)
    if kind == "mixed_wave":
        return 1.0 + 0.06*np.cos(2*X+Y) + 0.04*np.sin(Z-X)
    raise ValueError(kind)


def integrate_lapse(field, geom, lapse_kind):
    lapse = lapse_field(lapse_kind, geom["X"], geom["Y"], geom["Z"])
    return float(np.sum(lapse*geom["sqrt_h"]*field)*geom["dx"]**3)


def compute_heat_trace_row(N, amp):
    geom = conformal_fields(N, amp, OMEGA, T0)
    L, deg = build_laplacian_from_phi(geom["phi"], geom["dx"])
    evals, evecs = eig_system(L, DEVICE)
    feats = heat_trace_features(evals, geom["dx"])
    return {
        "N": N,
        "amp": amp,
        "int_RdV": geom["int_RdV"],
        "volume": geom["volume"],
        **feats,
    }


def reconstruct_heat_spatial(N):
    # Calibrate heat-trace zero-mode map excluding TEST_AMP.
    calib = [compute_heat_trace_row(N, a) for a in CALIBRATION_AMPS]
    x = np.array([r["trace_slope_6m_linear"] for r in calib], dtype=np.float64)
    y = np.array([r["int_RdV"] for r in calib], dtype=np.float64)
    coef, z_rel, z_r2 = fit_linear(x,y)

    # Test geometry eigensystem.
    geom = conformal_fields(N, TEST_AMP, OMEGA, T0)
    L, deg = build_laplacian_from_phi(geom["phi"], geom["dx"])
    evals, evecs = eig_system(L, DEVICE)
    feats = heat_trace_features(evals, geom["dx"])

    I_R_trace = float(coef[0] + coef[1]*feats["trace_slope_6m_linear"])

    Rhat_raw = local_heat_Rhat(evals, evecs, geom["dx"], N)
    sR = fit_centered_scale(Rhat_raw, geom["R3"])
    R_centered = sR*(Rhat_raw-np.mean(Rhat_raw))

    weighted_centered = float(np.sum(geom["sqrt_h"]*R_centered)*geom["dx"]**3)
    volume = geom["volume"]
    c = (I_R_trace - weighted_centered)/(volume+1e-12)

    R_heat_auto = R_centered + c

    return geom, {
        "R_heat_auto": R_heat_auto,
        "R_centered": R_centered,
        "I_R_trace": I_R_trace,
        "I_R_true": geom["int_RdV"],
        "I_R_trace_rel_error": abs(I_R_trace-geom["int_RdV"])/(abs(geom["int_RdV"])+1e-12),
        "R_local_corr": corr(R_centered, geom["R3"]-np.mean(geom["R3"])),
        "R_heat_auto_corr": corr(R_heat_auto, geom["R3"]),
        "R_local_rel_L2": float(np.linalg.norm((R_centered-(geom["R3"]-np.mean(geom["R3"]))).ravel())/(np.linalg.norm((geom["R3"]-np.mean(geom["R3"])).ravel())+1e-12)),
        "R_scale": sR,
        "zero_calib_R2": z_r2,
        "zero_calib_rel_error": z_rel,
        "weighted_centered_integral": weighted_centered,
        "offset_c": c,
    }


def run_one_N(N):
    t0=time.time()
    geom, spatial = reconstruct_heat_spatial(N)
    kin = kinetic_proxy_from_degree_time(N, TEST_AMP, OMEGA, T0, DT, geom["dx"], geom["phidot"])

    ADM_hat = spatial["R_heat_auto"] + kin["K_hat"]

    rows={}
    for kind in ["unit","smooth_positive","curvature_coupled","mixed_wave"]:
        I_R_true = integrate_lapse(geom["R3"], geom, kind)
        I_R_hat = integrate_lapse(spatial["R_heat_auto"], geom, kind)
        I_K_true = integrate_lapse(geom["kinetic"], geom, kind)
        I_K_hat = integrate_lapse(kin["K_hat"], geom, kind)
        I_ADM_true = integrate_lapse(geom["ADM"], geom, kind)
        I_ADM_hat = integrate_lapse(ADM_hat, geom, kind)

        rows[kind]={
            "I_R_true": I_R_true,
            "I_R_hat": I_R_hat,
            "I_R_rel_error": abs(I_R_hat-I_R_true)/(abs(I_R_true)+1e-12),
            "I_K_true": I_K_true,
            "I_K_hat": I_K_hat,
            "I_K_rel_error": abs(I_K_hat-I_K_true)/(abs(I_K_true)+1e-12),
            "I_ADM_true": I_ADM_true,
            "I_ADM_hat": I_ADM_hat,
            "I_ADM_rel_error": abs(I_ADM_hat-I_ADM_true)/(abs(I_ADM_true)+1e-12),
            "ADM_density_corr": corr(lapse_field(kind,geom["X"],geom["Y"],geom["Z"])*geom["sqrt_h"]*ADM_hat,
                                    lapse_field(kind,geom["X"],geom["Y"],geom["Z"])*geom["sqrt_h"]*geom["ADM"]),
        }

    return {
        "N": N,
        "nodes": N**3,
        "spatial": spatial,
        "kinetic": {
            "phidot_corr": kin["phidot_corr"],
            "K_corr": corr(kin["K_hat"], geom["kinetic"]),
            "K_rel_L2": float(np.linalg.norm((kin["K_hat"]-geom["kinetic"]).ravel())/(np.linalg.norm(geom["kinetic"].ravel())+1e-12)),
            "scale_phidot": kin["scale_phidot"],
        },
        "ADM_local_corr": corr(ADM_hat, geom["ADM"]),
        "ADM_local_rel_L2": float(np.linalg.norm((ADM_hat-geom["ADM"]).ravel())/(np.linalg.norm(geom["ADM"].ravel())+1e-12)),
        "actions": rows,
        "total_seconds": round(time.time()-t0,3),
    }


all_results=[]
print("\nRunning ADM full autonomous heat action test...")
print("N_LIST:", N_LIST)
print("TEST_AMP:", TEST_AMP)
print("CALIBRATION_AMPS:", CALIBRATION_AMPS)
print("DEVICE:", DEVICE)

for N in N_LIST:
    print(f"\n=== N={N} ({N**3} nodes) ===")
    try:
        r=run_one_N(N)
        all_results.append(r)
        compact={
            "N": r["N"],
            "nodes": r["nodes"],
            "I_R_trace_rel_error": r["spatial"]["I_R_trace_rel_error"],
            "R_heat_auto_corr": r["spatial"]["R_heat_auto_corr"],
            "K_corr": r["kinetic"]["K_corr"],
            "ADM_local_corr": r["ADM_local_corr"],
            "ADM_local_rel_L2": r["ADM_local_rel_L2"],
            "total_seconds": r["total_seconds"],
        }
        print(json.dumps(compact, indent=2))
        print("ACTIONS:")
        print(json.dumps(r["actions"], indent=2))
    except Exception as e:
        print(f"FAILED at N={N}: {type(e).__name__}: {e}")
        break


print("\n================ ADM FULL AUTONOMOUS HEAT ACTION SUMMARY ================")
if all_results:
    adm_errors=[]
    density_corrs=[]
    R_errors=[]
    K_errors=[]
    for r in all_results:
        for vals in r["actions"].values():
            adm_errors.append(vals["I_ADM_rel_error"])
            density_corrs.append(vals["ADM_density_corr"])
            R_errors.append(vals["I_R_rel_error"])
            K_errors.append(vals["I_K_rel_error"])

    summary={
        "device": DEVICE,
        "n_completed": len(all_results),
        "N_completed": [r["N"] for r in all_results],
        "R_action_rel_error_max": float(max(R_errors)),
        "K_action_rel_error_max": float(max(K_errors)),
        "ADM_action_rel_error_max": float(max(adm_errors)),
        "ADM_action_rel_error_mean": float(np.mean(adm_errors)),
        "ADM_density_corr_min": float(min(density_corrs)),
        "R_heat_auto_corr_min": float(min(r["spatial"]["R_heat_auto_corr"] for r in all_results)),
        "K_corr_min": float(min(r["kinetic"]["K_corr"] for r in all_results)),
        "ADM_local_corr_min": float(min(r["ADM_local_corr"] for r in all_results)),
        "ADM_action_ok_all": all(e < PASS_ADM_ACTION_REL_ERR for e in adm_errors),
        "ADM_density_corr_ok_all": all(c > PASS_DENSITY_CORR for c in density_corrs),
        "ADM_local_corr_ok_all": all(r["ADM_local_corr"] > PASS_LOCAL_ADM_CORR for r in all_results),
        "classification": (
            "ADM_FULL_AUTONOMOUS_HEAT_ACTION_PROMISING"
            if all(e < PASS_ADM_ACTION_REL_ERR for e in adm_errors)
            and all(c > PASS_DENSITY_CORR for c in density_corrs)
            and all(r["ADM_local_corr"] > PASS_LOCAL_ADM_CORR for r in all_results)
            else "ADM_FULL_AUTONOMOUS_HEAT_ACTION_WEAK"
        )
    }
    print(json.dumps(summary, indent=2))

    print("\nCSV_ROWS:")
    print("N,nodes,lapse_kind,I_R_true,I_R_hat,I_R_rel_error,I_K_true,I_K_hat,I_K_rel_error,I_ADM_true,I_ADM_hat,I_ADM_rel_error,ADM_density_corr,R_heat_auto_corr,K_corr,ADM_local_corr,I_R_trace_rel_error,total_seconds")
    for r in all_results:
        for kind, vals in r["actions"].items():
            print(
                f"{r['N']},{r['nodes']},{kind},"
                f"{vals['I_R_true']},{vals['I_R_hat']},{vals['I_R_rel_error']},"
                f"{vals['I_K_true']},{vals['I_K_hat']},{vals['I_K_rel_error']},"
                f"{vals['I_ADM_true']},{vals['I_ADM_hat']},{vals['I_ADM_rel_error']},"
                f"{vals['ADM_density_corr']},"
                f"{r['spatial']['R_heat_auto_corr']},{r['kinetic']['K_corr']},{r['ADM_local_corr']},"
                f"{r['spatial']['I_R_trace_rel_error']},{r['total_seconds']}"
            )
else:
    print("No completed results.")
