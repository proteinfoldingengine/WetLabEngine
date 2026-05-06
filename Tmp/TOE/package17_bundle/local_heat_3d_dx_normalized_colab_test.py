# ============================================================
# 3D dx-Normalized Direct Heat-Diagonal Curvature Test
# GEM Bridge / Local Heat Curvature Recovery / R^(3)
#
# Purpose:
#   Retest the 3D direct heat result using:
#
#       Rhat_norm = (-6 B_i) / dx
#
#   Previous result:
#       shape/sign recovery passed strongly,
#       but fitted scale s_N grew with refinement.
#
#   Scale diagnostic suggested:
#       s_N ~ dx^-1.327
#       s_N * dx much more stable than raw s_N
#
# Run on T4 GPU if available.
# ============================================================

import time
import json
import numpy as np

try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False


# ----------------------------
# Config
# ----------------------------

USE_GPU_IF_AVAILABLE = True

# Start here. If fast, add 16 or run [16] separately.
N_LIST = [8, 10, 12, 14]

AMP = 0.15

TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8], dtype=np.float64)

SIGN_THRESHOLD = 0.10

PASS_CORR = 0.75
PASS_SIGN = 0.70
PASS_REL_L2 = 0.70
PASS_SCALE_CV = 0.15   # tighter than prior 0.25 because dx normalization should improve this


# ----------------------------
# Device
# ----------------------------

if TORCH_AVAILABLE and USE_GPU_IF_AVAILABLE and torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print("Torch available:", TORCH_AVAILABLE)
print("Device:", DEVICE)
if DEVICE == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


# ----------------------------
# 3D geometry
# ----------------------------

def build_conformal_grid_3d_np(N, amp=0.15):
    Lbox = 2 * np.pi
    dx = Lbox / N

    x = np.arange(N, dtype=np.float64) * dx
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")

    phi = amp * np.cos(X) * np.cos(Y) * np.cos(Z)

    lap_phi = -3 * amp * np.cos(X) * np.cos(Y) * np.cos(Z)

    phix = -amp * np.sin(X) * np.cos(Y) * np.cos(Z)
    phiy = -amp * np.cos(X) * np.sin(Y) * np.cos(Z)
    phiz = -amp * np.cos(X) * np.cos(Y) * np.sin(Z)

    grad2 = phix * phix + phiy * phiy + phiz * phiz

    R = np.exp(-2 * phi) * (-4 * lap_phi - 2 * grad2)

    dV = np.exp(3 * phi) * dx**3
    rho = R * dV

    return phi, R, dV, rho, dx


def build_dense_laplacian_3d_np(phi, dx):
    N = phi.shape[0]
    n = N**3

    W = np.zeros((n, n), dtype=np.float64)

    def idx(i, j, k):
        return ((i % N) * N + (j % N)) * N + (k % N)

    neighbors = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i, j, k)

                for di, dj, dk in neighbors:
                    ni = (i + di) % N
                    nj = (j + dj) % N
                    nk = (k + dk) % N

                    phimid = 0.5 * (phi[i, j, k] + phi[ni, nj, nk])
                    ell = np.exp(phimid) * dx
                    w = np.exp(-(ell * ell) / (4 * dx * dx))

                    b = idx(ni, nj, nk)
                    W[a, b] = w

    W = 0.5 * (W + W.T)
    deg = W.sum(axis=1)

    L = (np.diag(deg) - W) / (dx * dx)

    return L, deg


# ----------------------------
# Metrics
# ----------------------------

def corr_np(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    a = a - a.mean()
    b = b - b.mean()
    denom = np.sqrt(np.sum(a * a) * np.sum(b * b)) + 1e-12
    return float(np.sum(a * b) / denom)


def analyze_result_3d(Rhat, R, rho, threshold=0.10):
    Rhat0 = Rhat - Rhat.mean()
    R0 = R - R.mean()
    rho0 = rho - rho.mean()

    x = Rhat0.ravel()
    y = R0.ravel()

    s = float(np.dot(x, y) / (np.dot(x, x) + 1e-12))
    pred = s * x

    rel_l2 = float(np.linalg.norm(pred - y) / (np.linalg.norm(y) + 1e-12))

    max_abs_R = np.max(np.abs(y)) + 1e-12
    mask = np.abs(y) >= threshold * max_abs_R

    sign_match = float(np.mean(np.sign(pred[mask]) == np.sign(y[mask])))
    retained = float(np.mean(mask))

    return {
        "best_scale_s": s,
        "relative_L2_error": rel_l2,
        "corr_raw_Rhat_R": corr_np(Rhat0, R0),
        "corr_scaled_R": corr_np(pred, y),
        "corr_raw_Rhat_RdV": corr_np(Rhat0, rho0),
        "thresholded_sign_match": sign_match,
        "retained_fraction": retained,
        "std_Rhat": float(np.std(Rhat0)),
        "std_R": float(np.std(R0)),
    }


# ----------------------------
# Direct heat diagonal
# ----------------------------

def direct_heat_diagonal_cpu(L_np, dx, time_multipliers):
    evals, evecs = np.linalg.eigh(L_np)
    evals = np.maximum(evals, 0.0)

    V2 = evecs * evecs
    times = time_multipliers * dx * dx

    diags = []
    for t in times:
        weights = np.exp(-t * evals)
        diag = V2 @ weights
        diags.append(diag)

    return np.array(diags), times


def direct_heat_diagonal_torch(L_np, dx, time_multipliers, device="cuda"):
    L = torch.tensor(L_np, dtype=torch.float64, device=device)

    evals, evecs = torch.linalg.eigh(L)
    evals = torch.clamp(evals, min=0.0)

    V2 = evecs * evecs
    times_np = time_multipliers * dx * dx

    diags = []
    for t in times_np:
        weights = torch.exp(float(-t) * evals)
        diag = V2 @ weights
        diags.append(diag.detach().cpu().numpy())

    del L, evals, evecs, V2
    if device == "cuda":
        torch.cuda.empty_cache()

    return np.array(diags), times_np


def estimate_local_Rhat_3d_dx_normalized(diags, times, N, dx):
    """
    3D local heat expansion:
        Y_i(t) = K(t,i,i) * (4*pi*t)^(3/2)
        Y_i(t) ≈ A_i + B_i t

    Raw sign-corrected:
        Rhat_raw = -6 B_i

    dx-normalized:
        Rhat_norm = (-6 B_i) / dx
    """
    Y = diags * ((4 * np.pi * times)[:, None] ** 1.5)

    n_times, n_nodes = Y.shape
    slopes = np.empty(n_nodes, dtype=np.float64)

    for i in range(n_nodes):
        m, b = np.polyfit(times, Y[:, i], 1)
        slopes[i] = m

    Rhat_raw = (-6.0 * slopes).reshape(N, N, N)
    Rhat_norm = Rhat_raw / dx

    return Rhat_raw, Rhat_norm


# ----------------------------
# Conductance proxy
# ----------------------------

def conductance_proxy_check(phi, R, rho, dx):
    L_np, deg = build_dense_laplacian_3d_np(phi, dx)

    deg_field = deg.reshape(phi.shape)
    proxy = -(deg_field - deg_field.mean())

    R0 = R - R.mean()
    rho0 = rho - rho.mean()

    x = proxy.ravel()
    y = R0.ravel()

    s = float(np.dot(x, y) / (np.dot(x, x) + 1e-12))
    pred = s * x
    rel_l2 = float(np.linalg.norm(pred - y) / (np.linalg.norm(y) + 1e-12))

    return {
        "conductance_corr_R": corr_np(proxy, R0),
        "conductance_corr_RdV": corr_np(proxy, rho0),
        "conductance_best_scale_s": s,
        "conductance_relative_L2_error": rel_l2,
    }, L_np


# ----------------------------
# Main run
# ----------------------------

def run_one_N_3d_dx_normalized(N, amp=0.15, device="cpu"):
    t0 = time.time()

    phi, R, dV, rho, dx = build_conformal_grid_3d_np(N, amp=amp)

    ref_info = {
        "int_R_dV": float(np.sum(rho)),
        "R_min": float(np.min(R)),
        "R_max": float(np.max(R)),
        "positive_R_fraction": float(np.mean(R > 0)),
        "negative_R_fraction": float(np.mean(R < 0)),
    }

    t_geom = time.time()

    conductance_metrics, L_np = conductance_proxy_check(phi, R, rho, dx)

    t_build = time.time()

    if device == "cuda":
        diags, times = direct_heat_diagonal_torch(L_np, dx, TIME_MULTIPLIERS, device="cuda")
    else:
        diags, times = direct_heat_diagonal_cpu(L_np, dx, TIME_MULTIPLIERS)

    t_heat = time.time()

    Rhat_raw, Rhat_norm = estimate_local_Rhat_3d_dx_normalized(diags, times, N, dx)

    raw_metrics = analyze_result_3d(Rhat_raw, R, rho, threshold=SIGN_THRESHOLD)
    norm_metrics = analyze_result_3d(Rhat_norm, R, rho, threshold=SIGN_THRESHOLD)

    t_done = time.time()

    # Prefix keys for clarity
    raw_metrics = {f"raw_{k}": v for k, v in raw_metrics.items()}
    norm_metrics = {f"dxnorm_{k}": v for k, v in norm_metrics.items()}

    out = {
        "N": N,
        "nodes": N**3,
        "dx": float(dx),
        "geometry_seconds": round(t_geom - t0, 3),
        "build_seconds": round(t_build - t_geom, 3),
        "heat_seconds": round(t_heat - t_build, 3),
        "total_seconds": round(t_done - t0, 3),
        **ref_info,
        **conductance_metrics,
        **raw_metrics,
        **norm_metrics,
    }

    return out


all_results = []

print("\nRunning 3D dx-normalized direct heat-diagonal curvature test...")
print("N_LIST:", N_LIST)
print("AMP:", AMP)
print("TIME_MULTIPLIERS:", TIME_MULTIPLIERS.tolist())
print("SIGN_THRESHOLD:", SIGN_THRESHOLD)
print()

for N in N_LIST:
    print(f"--- Running N={N} ({N**3} nodes) ---")
    try:
        result = run_one_N_3d_dx_normalized(N, amp=AMP, device=DEVICE)
        all_results.append(result)
        print(json.dumps(result, indent=2))

    except RuntimeError as e:
        print(f"RuntimeError at N={N}: {e}")
        if DEVICE == "cuda":
            print("Clearing CUDA cache and continuing...")
            torch.cuda.empty_cache()
        break

    except Exception as e:
        print(f"FAILED at N={N}: {type(e).__name__}: {e}")
        break


# ----------------------------
# Campaign summary
# ----------------------------

print("\n================ 3D DX-NORMALIZED CAMPAIGN SUMMARY ================")

if len(all_results) > 0:
    raw_scales = np.array([r["raw_best_scale_s"] for r in all_results], dtype=np.float64)
    dxnorm_scales = np.array([r["dxnorm_best_scale_s"] for r in all_results], dtype=np.float64)

    raw_scale_cv = float(np.std(raw_scales) / (abs(np.mean(raw_scales)) + 1e-12))
    dxnorm_scale_cv = float(np.std(dxnorm_scales) / (abs(np.mean(dxnorm_scales)) + 1e-12))

    corr_ok_all = all(r["dxnorm_corr_scaled_R"] > PASS_CORR for r in all_results)
    sign_ok_all = all(r["dxnorm_thresholded_sign_match"] > PASS_SIGN for r in all_results)
    retained_ok_all = all(r["dxnorm_retained_fraction"] > 0.35 for r in all_results)
    final_error_ok = all_results[-1]["dxnorm_relative_L2_error"] < PASS_REL_L2
    scale_ok = dxnorm_scale_cv < PASS_SCALE_CV

    conductance_corr_ok_all = all(r["conductance_corr_R"] > PASS_CORR for r in all_results)

    scale_improved = dxnorm_scale_cv < raw_scale_cv

    summary = {
        "n_completed": len(all_results),
        "N_completed": [r["N"] for r in all_results],
        "raw_scale_cv_across_grids": raw_scale_cv,
        "dxnorm_scale_cv_across_grids": dxnorm_scale_cv,
        "scale_improved_by_dx_normalization": scale_improved,
        "corr_ok_all": corr_ok_all,
        "thresholded_sign_ok_all": sign_ok_all,
        "retained_ok_all": retained_ok_all,
        "final_error_lt_0p70": final_error_ok,
        "dxnorm_scale_cv_lt_0p15": scale_ok,
        "conductance_corr_ok_all": conductance_corr_ok_all,
        "classification": (
            "DX_NORMALIZED_3D_HEAT_PROMISING"
            if corr_ok_all and sign_ok_all and retained_ok_all and final_error_ok and scale_ok and scale_improved
            else "DX_NORMALIZED_3D_HEAT_WEAK"
        ),
    }

    print(json.dumps(summary, indent=2))

    print("\nCSV_ROWS:")
    print(
        "N,nodes,dx,int_R_dV,"
        "raw_scale,dxnorm_scale,raw_rel_L2,dxnorm_rel_L2,"
        "raw_corr_R,dxnorm_corr_R,raw_corr_RdV,dxnorm_corr_RdV,"
        "raw_sign_match,dxnorm_sign_match,retained_fraction,"
        "conductance_corr_R,conductance_corr_RdV,"
        "geometry_seconds,build_seconds,heat_seconds,total_seconds"
    )

    for r in all_results:
        print(
            f"{r['N']},{r['nodes']},{r['dx']},{r['int_R_dV']},"
            f"{r['raw_best_scale_s']},{r['dxnorm_best_scale_s']},"
            f"{r['raw_relative_L2_error']},{r['dxnorm_relative_L2_error']},"
            f"{r['raw_corr_scaled_R']},{r['dxnorm_corr_scaled_R']},"
            f"{r['raw_corr_raw_Rhat_RdV']},{r['dxnorm_corr_raw_Rhat_RdV']},"
            f"{r['raw_thresholded_sign_match']},{r['dxnorm_thresholded_sign_match']},"
            f"{r['dxnorm_retained_fraction']},"
            f"{r['conductance_corr_R']},{r['conductance_corr_RdV']},"
            f"{r['geometry_seconds']},{r['build_seconds']},{r['heat_seconds']},{r['total_seconds']}"
        )

else:
    print("No completed results.")
