# ============================================================
# Zero-Mode Heat Trace Colab Test
# GEM Bridge / ADM Spatial Zero-Mode Recovery
#
# Purpose:
#   Test whether the missing ADM spatial curvature zero mode:
#
#       ∫ sqrt(h) R^(3) d^3x
#
#   can be recovered from global heat-trace observables:
#
#       Tr(exp(-tL)) * (4*pi*t)^(3/2)
#
#   For a smooth 3D manifold:
#
#       Tr(e^{-tP}) ~ (4πt)^(-3/2) [ Vol + (t/6) ∫R dV + O(t^2) ]
#
#   Therefore:
#
#       H(t) = Tr(e^{-tL}) * (4πt)^(3/2)
#       H(t) ≈ A + B t
#       6B should track ∫R dV up to graph normalization.
#
# What this is:
#   A diagnostic zero-mode recovery test.
#
# What this is NOT:
#   Not full ADM closure.
#   Not an Einstein equation derivation.
#   Not a theorem-level heat-kernel convergence proof.
#
# Recommended:
#   Run on T4 GPU.
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

# Start here. If fast, try [16] separately.
N_LIST = [8, 10, 12, 14]

# Amplitudes vary the curvature zero mode.
AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25]

# Heat trace window.
TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)

# Early pass criteria for heat-trace zero-mode signal.
PASS_R2 = 0.98
PASS_REL_ERR = 0.12


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
    """
    Periodic 3D conformal metric:

        h_ij = exp(2 phi) delta_ij
        phi = a cos x cos y cos z

    Spatial scalar curvature:

        R^(3) = exp(-2phi) [ -4 Δphi - 2 |grad phi|^2 ]

    Volume element:

        sqrt(h) d^3x = exp(3phi) dx^3
    """
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

    return phi, R, sqrt_h, dV, rho, dx


def build_dense_laplacian_3d_np(phi, dx):
    """
    Metric-weighted periodic 6-neighbor graph.

    Edge length:
        ell_ij = exp(phi_mid) dx

    Weight:
        w_ij = exp(-ell_ij^2 / (4 dx^2))

    L = (D - W) / dx^2
    """
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
# Heat trace
# ----------------------------

def eigvals_cpu(L_np):
    evals = np.linalg.eigvalsh(L_np)
    evals = np.maximum(evals, 0.0)
    return evals


def eigvals_torch(L_np, device="cuda"):
    L = torch.tensor(L_np, dtype=torch.float64, device=device)
    evals = torch.linalg.eigvalsh(L)
    evals = torch.clamp(evals, min=0.0)
    out = evals.detach().cpu().numpy()

    del L, evals
    if device == "cuda":
        torch.cuda.empty_cache()

    return out


def heat_trace_features(evals, dx, time_multipliers):
    """
    Compute:

        H(t) = Tr(e^{-tL}) * (4*pi*t)^(3/2)

    Fit:

        H(t) ≈ A + B t

    Return:
        trace_slope_6m = 6B
    """
    times = time_multipliers * dx * dx

    traces = np.array([
        np.sum(np.exp(-float(t) * evals))
        for t in times
    ], dtype=np.float64)

    H = traces * ((4 * np.pi * times) ** 1.5)

    m, b = np.polyfit(times, H, 1)

    # Add a quadratic fit too, to see if O(t^2) matters.
    quad = np.polyfit(times, H, 2)
    a2, b2, c2 = quad

    return {
        "trace_slope_6m_linear": float(6 * m),
        "trace_intercept_linear": float(b),
        "trace_quad_a": float(a2),
        "trace_quad_slope_6b": float(6 * b2),
        "trace_quad_intercept": float(c2),
        "trace_H_mean": float(np.mean(H)),
        "trace_H_std": float(np.std(H)),
        "trace_raw_t0": float(traces[0]),
        "trace_raw_tlast": float(traces[-1]),
        "times": times.tolist(),
        "H_values": H.tolist(),
        "trace_values": traces.tolist(),
    }


# ----------------------------
# Fit helpers
# ----------------------------

def fit_linear_predictor(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    A = np.vstack([np.ones_like(x), x]).T
    coef = np.linalg.lstsq(A, y, rcond=None)[0]
    pred = A @ coef

    rel = float(np.linalg.norm(pred - y) / (np.linalg.norm(y) + 1e-12))
    r2 = float(1 - np.sum((y - pred)**2) / (np.sum((y - y.mean())**2) + 1e-12))

    return {
        "intercept": float(coef[0]),
        "slope": float(coef[1]),
        "relative_error": rel,
        "R2": r2,
        "predicted": pred.tolist(),
    }


def summarize_for_N(rows_for_N):
    """
    Fit multiple predictors against integrated curvature.
    """
    y_int = np.array([r["int_RdV"] for r in rows_for_N], dtype=np.float64)
    y_mean = np.array([r["mean_R_volume"] for r in rows_for_N], dtype=np.float64)

    predictors = [
        "trace_slope_6m_linear",
        "trace_quad_slope_6b",
        "trace_intercept_linear",
        "trace_quad_intercept",
        "trace_H_mean",
        "mean_degree",
        "var_degree",
        "mean_degree_deficit",
    ]

    fits = []

    for p in predictors:
        x = np.array([r[p] for r in rows_for_N], dtype=np.float64)

        f_int = fit_linear_predictor(x, y_int)
        fits.append({
            "predictor": p,
            "target": "int_RdV",
            **{k: v for k, v in f_int.items() if k != "predicted"},
        })

        f_mean = fit_linear_predictor(x, y_mean)
        fits.append({
            "predictor": p,
            "target": "mean_R_volume",
            **{k: v for k, v in f_mean.items() if k != "predicted"},
        })

    heat_fit = [f for f in fits if f["predictor"] == "trace_slope_6m_linear" and f["target"] == "int_RdV"][0]
    best_int = max([f for f in fits if f["target"] == "int_RdV"], key=lambda z: z["R2"])
    best_mean = max([f for f in fits if f["target"] == "mean_R_volume"], key=lambda z: z["R2"])

    return {
        "N": int(rows_for_N[0]["N"]),
        "n_amp": len(rows_for_N),
        "heat_trace_linear_slope_R2_int_RdV": heat_fit["R2"],
        "heat_trace_linear_slope_relative_error_int_RdV": heat_fit["relative_error"],
        "best_int_predictor": best_int["predictor"],
        "best_int_R2": best_int["R2"],
        "best_int_relative_error": best_int["relative_error"],
        "best_mean_predictor": best_mean["predictor"],
        "best_mean_R2": best_mean["R2"],
        "best_mean_relative_error": best_mean["relative_error"],
        "classification": (
            "ZERO_MODE_HEAT_TRACE_PROMISING"
            if heat_fit["R2"] > PASS_R2 and heat_fit["relative_error"] < PASS_REL_ERR
            else "ZERO_MODE_HEAT_TRACE_WEAK"
        ),
        "fits": fits,
    }


# ----------------------------
# One run
# ----------------------------

def run_one_geometry(N, amp, device="cpu"):
    t0 = time.time()

    phi, R, sqrt_h, dV, rho, dx = build_conformal_grid_3d_np(N, amp=amp)

    geom_time = time.time()

    L_np, deg = build_dense_laplacian_3d_np(phi, dx)

    build_time = time.time()

    if device == "cuda":
        evals = eigvals_torch(L_np, device=device)
    else:
        evals = eigvals_cpu(L_np)

    eig_time = time.time()

    feats = heat_trace_features(evals, dx, TIME_MULTIPLIERS)

    done_time = time.time()

    row = {
        "N": N,
        "nodes": N**3,
        "amp": amp,
        "dx": float(dx),
        "volume": float(np.sum(dV)),
        "int_RdV": float(np.sum(rho)),
        "mean_R_volume": float(np.sum(rho) / np.sum(dV)),
        "mean_R_arithmetic": float(np.mean(R)),
        "mean_degree": float(np.mean(deg)),
        "var_degree": float(np.var(deg)),
        "mean_degree_deficit": float(np.mean(6.0 - deg)),
        "eig_min": float(np.min(evals)),
        "eig_max": float(np.max(evals)),
        "geometry_seconds": round(geom_time - t0, 3),
        "build_seconds": round(build_time - geom_time, 3),
        "eig_seconds": round(eig_time - build_time, 3),
        "total_seconds": round(done_time - t0, 3),
        **feats,
    }

    return row


# ----------------------------
# Campaign
# ----------------------------

all_rows = []
summaries = []

print("\nRunning zero-mode heat trace Colab test...")
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("TIME_MULTIPLIERS:", TIME_MULTIPLIERS.tolist())
print()

for N in N_LIST:
    print(f"\n=== N={N} ({N**3} nodes) ===")
    rows_N = []

    for amp in AMP_LIST:
        print(f"--- amp={amp} ---")
        try:
            row = run_one_geometry(N, amp, device=DEVICE)
            rows_N.append(row)
            all_rows.append(row)

            compact = {
                "N": row["N"],
                "amp": row["amp"],
                "nodes": row["nodes"],
                "int_RdV": row["int_RdV"],
                "mean_R_volume": row["mean_R_volume"],
                "trace_slope_6m_linear": row["trace_slope_6m_linear"],
                "trace_quad_slope_6b": row["trace_quad_slope_6b"],
                "trace_intercept_linear": row["trace_intercept_linear"],
                "mean_degree": row["mean_degree"],
                "var_degree": row["var_degree"],
                "eig_seconds": row["eig_seconds"],
                "total_seconds": row["total_seconds"],
            }

            print(json.dumps(compact, indent=2))

        except RuntimeError as e:
            print(f"RuntimeError at N={N}, amp={amp}: {e}")
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            break

        except Exception as e:
            print(f"FAILED at N={N}, amp={amp}: {type(e).__name__}: {e}")
            break

    if len(rows_N) >= 4:
        summary_N = summarize_for_N(rows_N)
        summaries.append(summary_N)

        printable = {k: v for k, v in summary_N.items() if k != "fits"}
        print("\nN_SUMMARY:")
        print(json.dumps(printable, indent=2))


# ----------------------------
# Final summary
# ----------------------------

print("\n================ ZERO-MODE HEAT TRACE CAMPAIGN SUMMARY ================")

if len(summaries) > 0:
    classification_all = all(s["classification"] == "ZERO_MODE_HEAT_TRACE_PROMISING" for s in summaries)

    final = {
        "device": DEVICE,
        "n_geometries_completed": len(all_rows),
        "N_completed": [s["N"] for s in summaries],
        "all_N_promising": classification_all,
        "min_heat_trace_linear_slope_R2_int_RdV": float(min(s["heat_trace_linear_slope_R2_int_RdV"] for s in summaries)),
        "max_heat_trace_linear_slope_relative_error_int_RdV": float(max(s["heat_trace_linear_slope_relative_error_int_RdV"] for s in summaries)),
        "classification": (
            "ZERO_MODE_HEAT_TRACE_COLAB_PROMISING"
            if classification_all
            else "ZERO_MODE_HEAT_TRACE_COLAB_MIXED"
        ),
    }

    print(json.dumps(final, indent=2))

    print("\nN_SUMMARY_ROWS:")
    print(
        "N,n_amp,heat_trace_linear_slope_R2_int_RdV,"
        "heat_trace_linear_slope_relative_error_int_RdV,"
        "best_int_predictor,best_int_R2,best_int_relative_error,"
        "best_mean_predictor,best_mean_R2,best_mean_relative_error,classification"
    )

    for s in summaries:
        print(
            f"{s['N']},{s['n_amp']},"
            f"{s['heat_trace_linear_slope_R2_int_RdV']},"
            f"{s['heat_trace_linear_slope_relative_error_int_RdV']},"
            f"{s['best_int_predictor']},{s['best_int_R2']},{s['best_int_relative_error']},"
            f"{s['best_mean_predictor']},{s['best_mean_R2']},{s['best_mean_relative_error']},"
            f"{s['classification']}"
        )

    print("\nGEOMETRY_ROWS:")
    print(
        "N,nodes,amp,dx,volume,int_RdV,mean_R_volume,mean_R_arithmetic,"
        "mean_degree,var_degree,mean_degree_deficit,"
        "trace_slope_6m_linear,trace_quad_slope_6b,"
        "trace_intercept_linear,trace_quad_intercept,trace_H_mean,trace_H_std,"
        "eig_min,eig_max,geometry_seconds,build_seconds,eig_seconds,total_seconds"
    )

    for r in all_rows:
        print(
            f"{r['N']},{r['nodes']},{r['amp']},{r['dx']},"
            f"{r['volume']},{r['int_RdV']},{r['mean_R_volume']},{r['mean_R_arithmetic']},"
            f"{r['mean_degree']},{r['var_degree']},{r['mean_degree_deficit']},"
            f"{r['trace_slope_6m_linear']},{r['trace_quad_slope_6b']},"
            f"{r['trace_intercept_linear']},{r['trace_quad_intercept']},"
            f"{r['trace_H_mean']},{r['trace_H_std']},"
            f"{r['eig_min']},{r['eig_max']},"
            f"{r['geometry_seconds']},{r['build_seconds']},{r['eig_seconds']},{r['total_seconds']}"
        )

else:
    print("No N summaries completed.")
