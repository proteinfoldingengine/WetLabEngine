# ============================================================
# Direct Heat ADM Spatial Curvature Action Test
# GEM Bridge / ADM Spatial Curvature Term / R^(3)
#
# Purpose:
#   Use the actual dx-normalized direct heat estimator:
#
#       Rhat_heat = (-6 B_i) / dx
#
#   and assemble the ADM spatial curvature action term:
#
#       I_R = ∫ N sqrt(h) R^(3) d^3x
#
#   Discrete:
#
#       I_R_hat = Σ_i N_i sqrt(h_i) Rhat_i dx^3
#
# Important:
#   This is NOT full ADM closure.
#   It tests only the spatial curvature term, not K_ij K^ij - K^2,
#   not lapse/shift derivation, and not action variation.
#
# Recommended: T4 GPU.
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

# Start here. If fast, run [16] separately.
N_LIST = [8, 10, 12, 14]

AMP = 0.15

TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8], dtype=np.float64)

# Relative error target for spatial curvature action term
PASS_ACTION_REL_ERR = 0.15
PASS_DENSITY_CORR = 0.95
PASS_LOCAL_CORR = 0.75


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
# Geometry
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

    sqrt_h = np.exp(3 * phi)
    dV = sqrt_h * dx**3
    rho = R * dV

    return phi, R, sqrt_h, dV, rho, dx, X, Y, Z


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
# Metrics and lapse
# ----------------------------

def corr_np(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    a = a - a.mean()
    b = b - b.mean()
    denom = np.sqrt(np.sum(a * a) * np.sum(b * b)) + 1e-12
    return float(np.sum(a * b) / denom)


def lapse_field(kind, X, Y, Z):
    if kind == "unit":
        return np.ones_like(X)
    if kind == "smooth_positive":
        return 1.0 + 0.10 * np.cos(X) + 0.05 * np.sin(Y + Z)
    if kind == "curvature_coupled":
        return 1.0 + 0.10 * np.cos(X) * np.cos(Y) * np.cos(Z)
    if kind == "mixed_wave":
        return 1.0 + 0.06*np.cos(2*X + Y) + 0.04*np.sin(Z - X)
    raise ValueError(kind)


def fit_centered_scale(Rhat, R):
    x = (Rhat - Rhat.mean()).ravel()
    y = (R - R.mean()).ravel()
    return float(np.dot(x, y) / (np.dot(x, x) + 1e-12))


def local_metrics(Rhat, R, rho):
    Rhat0 = Rhat - Rhat.mean()
    R0 = R - R.mean()
    rho0 = rho - rho.mean()

    s = fit_centered_scale(Rhat, R)
    pred = s * Rhat0

    rel_l2 = float(np.linalg.norm(pred - R0.ravel()) / (np.linalg.norm(R0.ravel()) + 1e-12))

    return {
        "local_scale_s": s,
        "local_corr_R": corr_np(Rhat0, R0),
        "local_corr_RdV": corr_np(Rhat0, rho0),
        "local_relative_L2": rel_l2,
        "local_std_Rhat": float(np.std(Rhat0)),
        "local_std_R": float(np.std(R0)),
    }


def action_metrics(Rhat, R, sqrt_h, dx, X, Y, Z):
    """
    We evaluate two versions:

    1. centered_scale_plus_analytic_mean:
       Rhat_action = s*(Rhat - mean(Rhat)) + mean(R)
       This tests action assembly assuming the zero mode is supplied.

    2. raw_scaled_no_mean_restore:
       Rhat_action = s*(Rhat - mean(Rhat))
       This exposes the zero-mode problem.

    The first is the fair spatial-density assembly test.
    The second tells us whether autonomous zero-mode recovery exists.
    """
    s = fit_centered_scale(Rhat, R)
    Rhat_centered_scaled = s * (Rhat - Rhat.mean())
    Rhat_mean_restored = Rhat_centered_scaled + R.mean()

    out = {}

    for lapse_kind in ["unit", "smooth_positive", "curvature_coupled", "mixed_wave"]:
        Nfield = lapse_field(lapse_kind, X, Y, Z)

        true_density = Nfield * sqrt_h * R
        pred_density_mean_restored = Nfield * sqrt_h * Rhat_mean_restored
        pred_density_no_mean = Nfield * sqrt_h * Rhat_centered_scaled

        S_true = float(np.sum(true_density) * dx**3)
        S_hat_mean = float(np.sum(pred_density_mean_restored) * dx**3)
        S_hat_no_mean = float(np.sum(pred_density_no_mean) * dx**3)

        rel_mean = float(abs(S_hat_mean - S_true) / (abs(S_true) + 1e-12))
        rel_no_mean = float(abs(S_hat_no_mean - S_true) / (abs(S_true) + 1e-12))

        out[lapse_kind] = {
            "S_true": S_true,
            "S_hat_mean_restored": S_hat_mean,
            "S_hat_no_mean_restore": S_hat_no_mean,
            "rel_error_mean_restored": rel_mean,
            "rel_error_no_mean_restore": rel_no_mean,
            "density_corr_mean_restored": corr_np(pred_density_mean_restored, true_density),
            "density_corr_no_mean_restore": corr_np(pred_density_no_mean, true_density),
            "mean_lapse": float(np.mean(Nfield)),
            "min_lapse": float(np.min(Nfield)),
            "max_lapse": float(np.max(Nfield)),
        }

    return out


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


def estimate_Rhat_dxnorm(diags, times, N, dx):
    """
    3D heat expansion:
        Y_i(t)=K(t,i,i)*(4*pi*t)^(3/2)
        Y_i≈A_i+B_i t

    dx-normalized estimator:
        Rhat = (-6 B_i)/dx
    """
    Y = diags * ((4 * np.pi * times)[:, None] ** 1.5)

    slopes = np.empty(Y.shape[1], dtype=np.float64)

    for i in range(Y.shape[1]):
        m, b = np.polyfit(times, Y[:, i], 1)
        slopes[i] = m

    Rhat = ((-6.0 * slopes) / dx).reshape(N, N, N)
    return Rhat


# ----------------------------
# One run
# ----------------------------

def run_one_N(N, amp=0.15, device="cpu"):
    t0 = time.time()

    phi, R, sqrt_h, dV, rho, dx, X, Y, Z = build_conformal_grid_3d_np(N, amp=amp)

    geom_info = {
        "int_R_dV": float(np.sum(rho)),
        "mean_R": float(np.mean(R)),
        "R_min": float(np.min(R)),
        "R_max": float(np.max(R)),
        "positive_R_fraction": float(np.mean(R > 0)),
        "negative_R_fraction": float(np.mean(R < 0)),
    }

    t_geom = time.time()

    L_np, deg = build_dense_laplacian_3d_np(phi, dx)

    t_build = time.time()

    if device == "cuda":
        diags, times = direct_heat_diagonal_torch(L_np, dx, TIME_MULTIPLIERS, device="cuda")
    else:
        diags, times = direct_heat_diagonal_cpu(L_np, dx, TIME_MULTIPLIERS)

    t_heat = time.time()

    Rhat = estimate_Rhat_dxnorm(diags, times, N, dx)

    lm = local_metrics(Rhat, R, rho)
    am = action_metrics(Rhat, R, sqrt_h, dx, X, Y, Z)

    t_done = time.time()

    return {
        "N": N,
        "nodes": N**3,
        "dx": float(dx),
        "geometry_seconds": round(t_geom - t0, 3),
        "build_seconds": round(t_build - t_geom, 3),
        "heat_seconds": round(t_heat - t_build, 3),
        "total_seconds": round(t_done - t0, 3),
        **geom_info,
        **lm,
        "action": am,
    }


# ----------------------------
# Main campaign
# ----------------------------

all_results = []

print("\nRunning direct heat ADM spatial curvature action test...")
print("N_LIST:", N_LIST)
print("AMP:", AMP)
print("TIME_MULTIPLIERS:", TIME_MULTIPLIERS.tolist())
print()

for N in N_LIST:
    print(f"--- Running N={N} ({N**3} nodes) ---")
    try:
        result = run_one_N(N, amp=AMP, device=DEVICE)
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
# Summary
# ----------------------------

print("\n================ DIRECT HEAT ADM ACTION SUMMARY ================")

if len(all_results) > 0:
    local_corr_ok = all(r["local_corr_R"] > PASS_LOCAL_CORR for r in all_results)

    mean_restored_errors = []
    no_mean_errors = []
    density_corrs_mean = []
    density_corrs_no_mean = []

    for r in all_results:
        for lapse_kind, vals in r["action"].items():
            mean_restored_errors.append(vals["rel_error_mean_restored"])
            no_mean_errors.append(vals["rel_error_no_mean_restore"])
            density_corrs_mean.append(vals["density_corr_mean_restored"])
            density_corrs_no_mean.append(vals["density_corr_no_mean_restore"])

    mean_restored_action_ok = all(e < PASS_ACTION_REL_ERR for e in mean_restored_errors)
    density_corr_mean_ok = all(c > PASS_DENSITY_CORR for c in density_corrs_mean)

    no_mean_action_ok = all(e < PASS_ACTION_REL_ERR for e in no_mean_errors)
    density_corr_no_mean_ok = all(c > PASS_DENSITY_CORR for c in density_corrs_no_mean)

    summary = {
        "n_completed": len(all_results),
        "N_completed": [r["N"] for r in all_results],
        "local_corr_ok": local_corr_ok,
        "mean_restored_action_rel_error_max": float(max(mean_restored_errors)),
        "mean_restored_action_ok_all": mean_restored_action_ok,
        "mean_restored_density_corr_min": float(min(density_corrs_mean)),
        "mean_restored_density_corr_ok_all": density_corr_mean_ok,
        "no_mean_action_rel_error_max": float(max(no_mean_errors)),
        "no_mean_action_ok_all": no_mean_action_ok,
        "no_mean_density_corr_min": float(min(density_corrs_no_mean)),
        "no_mean_density_corr_ok_all": density_corr_no_mean_ok,
        "classification": (
            "DIRECT_HEAT_ADM_SPATIAL_ACTION_PROMISING"
            if local_corr_ok and mean_restored_action_ok and density_corr_mean_ok
            else "DIRECT_HEAT_ADM_SPATIAL_ACTION_WEAK"
        ),
        "zero_mode_status": (
            "ZERO_MODE_NOT_AUTONOMOUSLY_RECOVERED"
            if not no_mean_action_ok
            else "ZERO_MODE_ACTION_OK"
        ),
    }

    print(json.dumps(summary, indent=2))

    print("\nCSV_ROWS:")
    print(
        "N,nodes,dx,lapse_kind,S_true,S_hat_mean_restored,S_hat_no_mean_restore,"
        "rel_error_mean_restored,rel_error_no_mean_restore,"
        "density_corr_mean_restored,density_corr_no_mean_restore,"
        "local_corr_R,local_corr_RdV,local_relative_L2,local_scale_s,"
        "mean_lapse,min_lapse,max_lapse,total_seconds"
    )

    for r in all_results:
        for lapse_kind, vals in r["action"].items():
            print(
                f"{r['N']},{r['nodes']},{r['dx']},{lapse_kind},"
                f"{vals['S_true']},{vals['S_hat_mean_restored']},{vals['S_hat_no_mean_restore']},"
                f"{vals['rel_error_mean_restored']},{vals['rel_error_no_mean_restore']},"
                f"{vals['density_corr_mean_restored']},{vals['density_corr_no_mean_restore']},"
                f"{r['local_corr_R']},{r['local_corr_RdV']},{r['local_relative_L2']},{r['local_scale_s']},"
                f"{vals['mean_lapse']},{vals['min_lapse']},{vals['max_lapse']},{r['total_seconds']}"
            )

else:
    print("No completed results.")
