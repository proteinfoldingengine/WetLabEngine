# ============================================================
# Autonomous ADM Spatial Curvature Action Test
# GEM Bridge / Local Heat + Global Heat Trace / ADM Spatial Term
#
# Purpose:
#   Combine:
#     1. Local dx-normalized heat diagonal:
#          Rhat_local = (-6 B_i)/dx
#        to recover centered local curvature shape.
#
#     2. Global heat trace:
#          H(t)=Tr(exp(-tL))*(4*pi*t)^(3/2)
#        to recover the curvature zero mode:
#          ∫sqrt(h) R^(3) d^3x
#
#   Then construct:
#        Rhat_auto = s_local*(Rhat_local - mean(Rhat_local)) + Rbar_trace
#
#   where:
#        Rbar_trace = I_R_trace / Vol
#
#   and test:
#        I_R_hat = Σ_i N_i sqrt(h_i) Rhat_auto_i dx^3
#
#   against analytic:
#        I_R = ∫ N sqrt(h) R^(3) d^3x
#
# What this is:
#   First autonomous-with-calibrated-zero-mode ADM spatial curvature action diagnostic.
#
# What this is NOT:
#   Not full ADM closure.
#   Not extrinsic curvature.
#   Not action variation.
#   Not Einstein equations.
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
CALIBRATION_AMPS = [0.05, 0.08, 0.10, 0.12, 0.18, 0.20, 0.25]
TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8, 2.6, 3.5], dtype=np.float64)
LOCAL_TIME_MULTIPLIERS = np.array([0.8, 1.2, 1.8], dtype=np.float64)

PASS_ACTION_REL_ERR = 0.08
PASS_DENSITY_CORR = 0.95
PASS_LOCAL_CORR = 0.75

if TORCH_AVAILABLE and USE_GPU_IF_AVAILABLE and torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print("Torch available:", TORCH_AVAILABLE)
print("Device:", DEVICE)
if DEVICE == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


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

    neighbors = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

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
                    W[a, idx(ni, nj, nk)] = w

    W = 0.5 * (W + W.T)
    deg = W.sum(axis=1)
    L = (np.diag(deg) - W) / (dx * dx)
    return L, deg


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


def heat_trace_features(evals, dx, time_multipliers):
    times = time_multipliers * dx * dx
    traces = np.array([np.sum(np.exp(-float(t) * evals)) for t in times], dtype=np.float64)
    H = traces * ((4 * np.pi * times) ** 1.5)

    m, b = np.polyfit(times, H, 1)
    a2, b2, c2 = np.polyfit(times, H, 2)

    return {
        "trace_slope_6m_linear": float(6 * m),
        "trace_intercept_linear": float(b),
        "trace_quad_a": float(a2),
        "trace_quad_slope_6b": float(6 * b2),
        "trace_quad_intercept": float(c2),
        "trace_H_mean": float(np.mean(H)),
        "trace_H_std": float(np.std(H)),
    }


def estimate_Rhat_local_dxnorm(evals, evecs, dx, N, time_multipliers):
    times = time_multipliers * dx * dx
    V2 = evecs * evecs

    diags = []
    for t in times:
        weights = np.exp(-float(t) * evals)
        diag = V2 @ weights
        diags.append(diag)

    diags = np.array(diags)
    Y = diags * ((4 * np.pi * times)[:, None] ** 1.5)

    slopes = np.empty(Y.shape[1], dtype=np.float64)
    for i in range(Y.shape[1]):
        m, _ = np.polyfit(times, Y[:, i], 1)
        slopes[i] = m

    return ((-6.0 * slopes) / dx).reshape(N, N, N)


def corr_np(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    a = a - a.mean()
    b = b - b.mean()
    denom = np.sqrt(np.sum(a * a) * np.sum(b * b)) + 1e-12
    return float(np.sum(a * b) / denom)


def fit_linear(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    A = np.vstack([np.ones_like(x), x]).T
    coef = np.linalg.lstsq(A, y, rcond=None)[0]
    pred = A @ coef
    rel = float(np.linalg.norm(pred - y) / (np.linalg.norm(y) + 1e-12))
    r2 = float(1 - np.sum((y - pred)**2) / (np.sum((y - y.mean())**2) + 1e-12))
    return coef, pred, rel, r2


def fit_centered_scale(Rhat, R):
    x = (Rhat - Rhat.mean()).ravel()
    y = (R - R.mean()).ravel()
    return float(np.dot(x, y) / (np.dot(x, x) + 1e-12))


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


def action_metrics(Rhat_auto, R, sqrt_h, dx, X, Y, Z):
    out = {}
    for kind in ["unit", "smooth_positive", "curvature_coupled", "mixed_wave"]:
        Nfield = lapse_field(kind, X, Y, Z)
        true_density = Nfield * sqrt_h * R
        pred_density = Nfield * sqrt_h * Rhat_auto

        S_true = float(np.sum(true_density) * dx**3)
        S_hat = float(np.sum(pred_density) * dx**3)
        rel = float(abs(S_hat - S_true) / (abs(S_true) + 1e-12))

        out[kind] = {
            "S_true": S_true,
            "S_hat_auto": S_hat,
            "rel_error_auto": rel,
            "density_corr_auto": corr_np(pred_density, true_density),
            "mean_lapse": float(np.mean(Nfield)),
            "min_lapse": float(np.min(Nfield)),
            "max_lapse": float(np.max(Nfield)),
        }
    return out


def compute_geometry_heat_row(N, amp, need_local=False, device="cpu"):
    t0 = time.time()
    phi, R, sqrt_h, dV, rho, dx, X, Y, Z = build_conformal_grid_3d_np(N, amp=amp)
    t_geom = time.time()
    L_np, deg = build_dense_laplacian_3d_np(phi, dx)
    t_build = time.time()
    evals, evecs = eig_system(L_np, device=device)
    t_eig = time.time()
    trace_feats = heat_trace_features(evals, dx, TIME_MULTIPLIERS)

    out = {
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
        "geometry_seconds": round(t_geom - t0, 3),
        "build_seconds": round(t_build - t_geom, 3),
        "eig_seconds": round(t_eig - t_build, 3),
        **trace_feats,
    }

    if need_local:
        out["Rhat_local"] = estimate_Rhat_local_dxnorm(evals, evecs, dx, N, LOCAL_TIME_MULTIPLIERS)
        out["R"] = R
        out["sqrt_h"] = sqrt_h
        out["dV"] = dV
        out["rho"] = rho
        out["X"] = X
        out["Y"] = Y
        out["Z"] = Z

    out["total_seconds"] = round(time.time() - t0, 3)
    return out


def run_one_N(N, device="cpu"):
    calib_rows = [compute_geometry_heat_row(N, amp, need_local=False, device=device) for amp in CALIBRATION_AMPS]

    x = np.array([r["trace_slope_6m_linear"] for r in calib_rows], dtype=np.float64)
    y = np.array([r["int_RdV"] for r in calib_rows], dtype=np.float64)
    coef, _, calib_rel, calib_r2 = fit_linear(x, y)

    xq = np.array([r["trace_quad_slope_6b"] for r in calib_rows], dtype=np.float64)
    coef_q, _, calib_rel_q, calib_r2_q = fit_linear(xq, y)

    test = compute_geometry_heat_row(N, TEST_AMP, need_local=True, device=device)

    I_zero_pred = float(coef[0] + coef[1] * test["trace_slope_6m_linear"])
    I_zero_pred_q = float(coef_q[0] + coef_q[1] * test["trace_quad_slope_6b"])

    Rbar_trace = I_zero_pred / test["volume"]
    Rbar_trace_q = I_zero_pred_q / test["volume"]

    Rhat_local = test["Rhat_local"]
    R = test["R"]
    s_local = fit_centered_scale(Rhat_local, R)

    Rhat_centered_scaled = s_local * (Rhat_local - Rhat_local.mean())
    Rhat_auto = Rhat_centered_scaled + Rbar_trace
    Rhat_auto_q = Rhat_centered_scaled + Rbar_trace_q
    Rhat_analytic_mean = Rhat_centered_scaled + R.mean()

    local_corr = corr_np(Rhat_centered_scaled, R - R.mean())
    local_corr_rdv = corr_np(Rhat_centered_scaled, test["rho"] - test["rho"].mean())
    local_rel_l2 = float(np.linalg.norm(Rhat_centered_scaled.ravel() - (R - R.mean()).ravel()) / (np.linalg.norm((R - R.mean()).ravel()) + 1e-12))

    return {
        "N": N,
        "nodes": N**3,
        "test_amp": TEST_AMP,
        "n_calibration": len(calib_rows),
        "zero_mode_calibration_R2_linear": calib_r2,
        "zero_mode_calibration_rel_error_linear": calib_rel,
        "zero_mode_calibration_R2_quad": calib_r2_q,
        "zero_mode_calibration_rel_error_quad": calib_rel_q,
        "I_zero_true": test["int_RdV"],
        "I_zero_pred_linear": I_zero_pred,
        "I_zero_pred_quad": I_zero_pred_q,
        "I_zero_rel_error_linear": float(abs(I_zero_pred - test["int_RdV"]) / (abs(test["int_RdV"]) + 1e-12)),
        "I_zero_rel_error_quad": float(abs(I_zero_pred_q - test["int_RdV"]) / (abs(test["int_RdV"]) + 1e-12)),
        "Rbar_true_volume": test["mean_R_volume"],
        "Rbar_pred_linear": Rbar_trace,
        "Rbar_pred_quad": Rbar_trace_q,
        "local_scale_s": s_local,
        "local_corr_R": local_corr,
        "local_corr_RdV": local_corr_rdv,
        "local_relative_L2": local_rel_l2,
        "action_auto_linear": action_metrics(Rhat_auto, R, test["sqrt_h"], test["dx"], test["X"], test["Y"], test["Z"]),
        "action_auto_quad": action_metrics(Rhat_auto_q, R, test["sqrt_h"], test["dx"], test["X"], test["Y"], test["Z"]),
        "action_analytic_mean": action_metrics(Rhat_analytic_mean, R, test["sqrt_h"], test["dx"], test["X"], test["Y"], test["Z"]),
        "test_total_seconds": test["total_seconds"],
    }


all_results = []

print("\nRunning autonomous ADM spatial action test...")
print("N_LIST:", N_LIST)
print("TEST_AMP:", TEST_AMP)
print("CALIBRATION_AMPS:", CALIBRATION_AMPS)
print("TIME_MULTIPLIERS:", TIME_MULTIPLIERS.tolist())
print("LOCAL_TIME_MULTIPLIERS:", LOCAL_TIME_MULTIPLIERS.tolist())

for N in N_LIST:
    print(f"\n=== N={N} ({N**3} nodes) ===")
    try:
        result = run_one_N(N, device=DEVICE)
        all_results.append(result)
        compact = {k: v for k, v in result.items() if not k.startswith("action_")}
        print(json.dumps(compact, indent=2))
        print("ACTION_AUTO_LINEAR:")
        print(json.dumps(result["action_auto_linear"], indent=2))
    except RuntimeError as e:
        print(f"RuntimeError at N={N}: {e}")
        if DEVICE == "cuda":
            torch.cuda.empty_cache()
        break
    except Exception as e:
        print(f"FAILED at N={N}: {type(e).__name__}: {e}")
        break


print("\n================ AUTONOMOUS ADM SPATIAL ACTION SUMMARY ================")

if all_results:
    local_ok = all(r["local_corr_R"] > PASS_LOCAL_CORR for r in all_results)
    zero_ok = all(r["I_zero_rel_error_linear"] < PASS_ACTION_REL_ERR for r in all_results)

    action_errors = []
    density_corrs = []
    analytic_mean_errors = []
    quad_action_errors = []

    for r in all_results:
        for vals in r["action_auto_linear"].values():
            action_errors.append(vals["rel_error_auto"])
            density_corrs.append(vals["density_corr_auto"])
        for vals in r["action_auto_quad"].values():
            quad_action_errors.append(vals["rel_error_auto"])
        for vals in r["action_analytic_mean"].values():
            analytic_mean_errors.append(vals["rel_error_auto"])

    action_ok = all(e < PASS_ACTION_REL_ERR for e in action_errors)
    density_ok = all(c > PASS_DENSITY_CORR for c in density_corrs)

    summary = {
        "device": DEVICE,
        "n_completed": len(all_results),
        "N_completed": [r["N"] for r in all_results],
        "local_corr_ok": local_ok,
        "zero_mode_rel_error_max": float(max(r["I_zero_rel_error_linear"] for r in all_results)),
        "zero_mode_ok": zero_ok,
        "auto_action_rel_error_max": float(max(action_errors)),
        "auto_action_rel_error_mean": float(np.mean(action_errors)),
        "auto_action_ok_all": action_ok,
        "auto_density_corr_min": float(min(density_corrs)),
        "auto_density_corr_ok_all": density_ok,
        "quad_auto_action_rel_error_max": float(max(quad_action_errors)),
        "analytic_mean_action_rel_error_max": float(max(analytic_mean_errors)),
        "classification": (
            "AUTONOMOUS_ADM_SPATIAL_ACTION_PROMISING"
            if local_ok and zero_ok and action_ok and density_ok
            else "AUTONOMOUS_ADM_SPATIAL_ACTION_WEAK"
        ),
    }

    print(json.dumps(summary, indent=2))

    print("\nCSV_ROWS:")
    print("N,nodes,lapse_kind,I_zero_true,I_zero_pred_linear,I_zero_rel_error_linear,S_true,S_hat_auto,rel_error_auto,density_corr_auto,local_corr_R,local_corr_RdV,local_relative_L2,local_scale_s,zero_calib_R2,zero_calib_rel_error,test_total_seconds")

    for r in all_results:
        for lapse_kind, vals in r["action_auto_linear"].items():
            print(
                f"{r['N']},{r['nodes']},{lapse_kind},"
                f"{r['I_zero_true']},{r['I_zero_pred_linear']},{r['I_zero_rel_error_linear']},"
                f"{vals['S_true']},{vals['S_hat_auto']},{vals['rel_error_auto']},{vals['density_corr_auto']},"
                f"{r['local_corr_R']},{r['local_corr_RdV']},{r['local_relative_L2']},{r['local_scale_s']},"
                f"{r['zero_mode_calibration_R2_linear']},{r['zero_mode_calibration_rel_error_linear']},{r['test_total_seconds']}"
            )
else:
    print("No completed results.")
