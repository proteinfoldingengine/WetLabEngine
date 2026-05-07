# ============================================================
# COLAB: Heat Operator Stability + Window Calibration Campaign
#
# Why this exists:
#   The modal-library run was not a clean theorem test.
#   It exposed operator/window instability:
#
#     - flat trace slopes jumped from about -25.6 to -155.9 to -600.5
#     - several N=12 delta_trace_slope values crossed zero
#     - C and q became meaningless when denominator nearly vanished
#
#   So the next step is NOT more geometries.
#   The next step is to freeze a numerically stable heat operator.
#
# Goal:
#   Compare graph operator normalizations and heat-time windows.
#   Keep only operator/window combinations where:
#
#     1. flat slope scales smoothly with dx
#     2. delta_trace_slope has stable sign across N and amp
#     3. no small-denominator rows
#     4. per-geometry q is stable
#     5. I prediction error is low
#
# Outputs:
#   heat_operator_stability_rows.csv
#   heat_operator_stability_operator_summary.csv
#   heat_operator_stability_summary.json
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
    import scipy.sparse.linalg as spla
except Exception:
    sp = None
    spla = None

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
# Controls
# ----------------------------
QUICK_MODE = True

if QUICK_MODE:
    N_LIST = [8, 10, 12, 14]
    AMP_LIST = [0.08, 0.15, 0.22]
else:
    N_LIST = [8, 10, 12, 14, 16]
    AMP_LIST = [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25]

DOMAIN_L = 2*np.pi
OUT_PREFIX = "heat_operator_stability"

# Windows are dimensionless multipliers.
# The actual heat time is tau * dx^2 for raw graph operators,
# and tau for operators already divided by dx^2.
WINDOWS = {
    "short": [0.05, 0.08, 0.12, 0.18, 0.25],
    "medium": [0.10, 0.16, 0.25, 0.40, 0.65],
    "long": [0.25, 0.40, 0.65, 1.00, 1.60],
}

# Operator normalizations to compare.
# raw:        L_graph
# dx2:        L_graph / dx^2
# volume_dx:  L_graph / dx^2 with heat trace weighted by cell volume
# degree_norm normalized graph Laplacian
OPERATOR_KINDS = ["raw", "dx2", "degree_norm", "volume_dx"]


# ============================================================
# Geometries: use stable known families, not huge random library
# ============================================================

GEOMS = [
    {
        "name": "xyz_product_like",
        "modes": [
            {"k": (1,1,1),  "a": 0.7071067811865476, "phase": 0.0},
            {"k": (1,1,-1), "a": 0.7071067811865476, "phase": 0.0},
            {"k": (1,-1,1), "a": 0.7071067811865476, "phase": 0.0},
            {"k": (-1,1,1), "a": 0.7071067811865476, "phase": 0.0},
        ],
    },
    {
        "name": "high_x_like",
        "modes": [
            {"k": (2,1,1),  "a": 0.7071067811865476, "phase": 0.0},
            {"k": (2,1,-1), "a": 0.7071067811865476, "phase": 0.0},
            {"k": (2,-1,1), "a": 0.7071067811865476, "phase": 0.0},
            {"k": (-2,1,1), "a": 0.7071067811865476, "phase": 0.0},
        ],
    },
    {
        "name": "additive_mixed_like",
        "modes": [
            {"k": (1,0,0), "a": 1.2344267996967353, "phase": 0.0},
            {"k": (0,2,0), "a": 0.6172133998483676, "phase": 0.0},
            {"k": (0,0,3), "a": 0.3086066999241838, "phase": 0.0},
        ],
    },
    {
        "name": "two_mode_like",
        "modes": [
            {"k": (1,1,1), "a": 1.3348172885319998, "phase": 0.0},
            {"k": (2,2,1), "a": 0.46718605098619986, "phase": 0.0},
        ],
    },
    {
        "name": "anisotropic_packet_like",
        "modes": [
            {"k": (1,0,0), "a": 1.3116516715679063, "phase": 0.0},
            {"k": (1,1,0), "a": 0.4590780850487672, "phase": 0.0},
            {"k": (0,0,2), "a": 0.26233033431358127, "phase": 0.0},
        ],
    },
]


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


def build_sparse_graph_laplacian(phi_flat, N, dx, operator_kind):
    phi = phi_flat.reshape(N,N,N)
    n = N**3

    rows = []
    cols = []
    vals = []

    deg = np.zeros(n, dtype=np.float64)

    def idx(i,j,k):
        return (i*N + j)*N + k

    # Build weighted adjacency first.
    edge_i = []
    edge_j = []
    edge_w = []
    dirs = [(1,0,0),(0,1,0),(0,0,1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                a = idx(i,j,k)
                phia = phi[i,j,k]
                for di,dj,dk in dirs:
                    ii = (i+di) % N
                    jj = (j+dj) % N
                    kk = (k+dk) % N
                    b = idx(ii,jj,kk)
                    # midpoint conformal conductance
                    w = math.exp(phi[i,j,k] + phi[ii,jj,kk])
                    edge_i.append(a); edge_j.append(b); edge_w.append(w)
                    edge_i.append(b); edge_j.append(a); edge_w.append(w)
                    deg[a] += w
                    deg[b] += w

    if operator_kind == "degree_norm":
        # L_sym = I - D^{-1/2} W D^{-1/2}
        rows.extend(range(n)); cols.extend(range(n)); vals.extend(np.ones(n))
        for a,b,w in zip(edge_i, edge_j, edge_w):
            vals.append(-w / math.sqrt((deg[a]+1e-15)*(deg[b]+1e-15)))
            rows.append(a); cols.append(b)
        L = sp.csr_matrix((vals,(rows,cols)), shape=(n,n))
        return L

    # Unnormalized graph L = D - W.
    for a in range(n):
        rows.append(a); cols.append(a); vals.append(deg[a])
    for a,b,w in zip(edge_i, edge_j, edge_w):
        rows.append(a); cols.append(b); vals.append(-w)

    L = sp.csr_matrix((vals,(rows,cols)), shape=(n,n))

    if operator_kind in ["dx2", "volume_dx"]:
        L = L / (dx*dx)

    return L


def eigvals_operator(phi_flat, N, dx, operator_kind):
    L = build_sparse_graph_laplacian(phi_flat, N, dx, operator_kind)

    # For these N values, dense eig is still feasible and reproducible.
    A = L.toarray()
    if torch is not None and DEVICE == "cuda" and A.shape[0] <= 3000:
        with torch.no_grad():
            T = torch.tensor(A, dtype=torch.float64, device="cuda")
            eig = torch.linalg.eigvalsh(T).detach().cpu().numpy()
    else:
        eig = np.linalg.eigvalsh(A)

    eig = np.maximum(eig, 0.0)
    return eig


def heat_trace_slope(eig, dx, window_name, operator_kind):
    taus = np.array(WINDOWS[window_name], dtype=np.float64)

    # If operator already has dx^-2, use physical t = tau.
    # If raw graph, use t = tau * dx^2.
    if operator_kind in ["dx2", "volume_dx"]:
        times = taus
    else:
        times = taus * dx*dx

    traces = np.array([np.sum(np.exp(-t*eig)) for t in times], dtype=np.float64)

    # For volume_dx, use cell-volume scaled trace.
    if operator_kind == "volume_dx":
        traces = traces * (dx**3)

    A = np.vstack([np.ones_like(times), times]).T
    beta = np.linalg.lstsq(A, traces, rcond=None)[0]
    intercept, slope = float(beta[0]), float(beta[1])

    return {
        "trace_slope": slope,
        "trace_intercept": intercept,
        "trace_mean": float(np.mean(traces)),
        "trace_std": float(np.std(traces)),
    }


print()
print("Running heat operator stability campaign...")
print("N_LIST:", N_LIST)
print("AMP_LIST:", AMP_LIST)
print("OPERATOR_KINDS:", OPERATOR_KINDS)
print("WINDOWS:", list(WINDOWS.keys()))

rows = []
eig_cache = {}

for operator_kind in OPERATOR_KINDS:
    for window_name in WINDOWS:
        print()
        print("="*80)
        print("OPERATOR:", operator_kind, "WINDOW:", window_name)

        flat_slope_by_N = {}

        for N in N_LIST:
            dx = DOMAIN_L/N
            zero_phi = np.zeros(N**3, dtype=np.float64)
            eig0 = eigvals_operator(zero_phi, N, dx, operator_kind)
            h0 = heat_trace_slope(eig0, dx, window_name, operator_kind)
            flat_slope_by_N[N] = h0["trace_slope"]
            print(f"flat N={N}, dx={dx:.4f}, slope={h0['trace_slope']:.6g}")

        for geom in GEOMS:
            gname = geom["name"]
            modes = geom["modes"]

            for N in N_LIST:
                for amp in AMP_LIST:
                    t0 = time.time()
                    curv = curvature_integral(modes, N, amp)
                    dx = curv["dx"]
                    eig = eigvals_operator(curv["phi_flat"], N, dx, operator_kind)
                    h = heat_trace_slope(eig, dx, window_name, operator_kind)

                    delta = h["trace_slope"] - flat_slope_by_N[N]
                    C_req = curv["int_RdV"] / (delta + 1e-15)

                    row = {
                        "operator_kind": operator_kind,
                        "window": window_name,
                        "geometry": gname,
                        "N": N,
                        "nodes": N**3,
                        "amp": amp,
                        "dx": dx,
                        "int_RdV": curv["int_RdV"],
                        "volume": curv["volume"],
                        "R_std": curv["R_std"],
                        "R_min": curv["R_min"],
                        "R_max": curv["R_max"],
                        "trace_slope": h["trace_slope"],
                        "flat_trace_slope": flat_slope_by_N[N],
                        "delta_trace_slope": delta,
                        "C_delta_required": C_req,
                        "abs_delta_trace_slope": abs(delta),
                        "seconds": round(time.time()-t0, 3),
                    }
                    rows.append(row)

                    print(json.dumps({
                        "op": operator_kind,
                        "window": window_name,
                        "geometry": gname,
                        "N": N,
                        "amp": amp,
                        "I": curv["int_RdV"],
                        "delta": delta,
                        "C_req": C_req,
                    }, indent=2))

raw = pd.DataFrame(rows)
raw.to_csv(f"{OUT_PREFIX}_rows.csv", index=False)


# ============================================================
# Scoring
# ============================================================

def fit_geom(group):
    # Drop tiny denominator rows before fitting.
    g = group.copy()
    med_abs_delta = np.median(np.abs(g["delta_trace_slope"].values))
    floor = max(1e-8, 0.02*med_abs_delta)
    g = g[g["abs_delta_trace_slope"] > floor]

    if len(g) < 5:
        return None

    x = np.log(g["dx"].values)
    y = np.log(np.abs(g["C_delta_required"].values) + 1e-30)
    A = np.vstack([np.ones_like(x), x]).T
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    c_abs = float(np.exp(beta[0]))
    q = float(beta[1])

    signed_c = float(np.median(g["C_delta_required"].values / (g["dx"].values**q)))
    pred_I = signed_c*(g["dx"].values**q)*g["delta_trace_slope"].values
    err = np.abs(pred_I-g["int_RdV"].values)/(np.abs(g["int_RdV"].values)+1e-12)

    signs = np.sign(g["delta_trace_slope"].values)
    nonzero = signs[signs != 0]
    sign_consistency = float(np.max([np.mean(nonzero > 0), np.mean(nonzero < 0)])) if len(nonzero) else 0.0

    return {
        "geometry": group["geometry"].iloc[0],
        "fit_c_abs": c_abs,
        "fit_q": q,
        "fit_signed_c": signed_c,
        "fit_rows": int(len(g)),
        "dropped_rows": int(len(group)-len(g)),
        "I_rel_error_mean": float(np.mean(err)),
        "I_rel_error_max": float(np.max(err)),
        "delta_sign_consistency": sign_consistency,
        "delta_min_abs": float(np.min(np.abs(g["delta_trace_slope"].values))),
        "delta_median_abs": float(np.median(np.abs(g["delta_trace_slope"].values))),
    }


summary_rows = []
geom_fit_rows = []

for (op, win), df in raw.groupby(["operator_kind", "window"]):
    fits = []
    for geom, g in df.groupby("geometry"):
        fg = fit_geom(g)
        if fg is not None:
            fg["operator_kind"] = op
            fg["window"] = win
            fits.append(fg)
            geom_fit_rows.append(fg)

    fdf = pd.DataFrame(fits)
    if len(fdf) == 0:
        continue

    # Flat slope smoothness: fit log|flat_slope| vs log dx.
    flats = df.groupby("N").first().reset_index()[["N","dx","flat_trace_slope"]]
    x = np.log(flats["dx"].values)
    y = np.log(np.abs(flats["flat_trace_slope"].values) + 1e-30)
    A = np.vstack([np.ones_like(x), x]).T
    b = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = A@b
    flat_log_rmse = float(np.sqrt(np.mean((y-yhat)**2)))
    flat_slope_power = float(b[1])

    score = (
        fdf["I_rel_error_mean"].mean()
        + fdf["fit_q"].std()
        + 0.5*(1.0 - fdf["delta_sign_consistency"].mean())
        + flat_log_rmse
    )

    summary_rows.append({
        "operator_kind": op,
        "window": win,
        "n_geometry_fits": int(len(fdf)),
        "q_mean": float(fdf["fit_q"].mean()),
        "q_std": float(fdf["fit_q"].std()),
        "q_min": float(fdf["fit_q"].min()),
        "q_max": float(fdf["fit_q"].max()),
        "I_rel_error_mean": float(fdf["I_rel_error_mean"].mean()),
        "I_rel_error_max": float(fdf["I_rel_error_max"].max()),
        "delta_sign_consistency_mean": float(fdf["delta_sign_consistency"].mean()),
        "dropped_rows_total": int(fdf["dropped_rows"].sum()),
        "flat_slope_power_vs_dx": flat_slope_power,
        "flat_slope_log_rmse": flat_log_rmse,
        "stability_score_lower_better": float(score),
    })

geom_fits = pd.DataFrame(geom_fit_rows)
op_summary = pd.DataFrame(summary_rows).sort_values("stability_score_lower_better")
geom_fits.to_csv(f"{OUT_PREFIX}_geometry_fits.csv", index=False)
op_summary.to_csv(f"{OUT_PREFIX}_operator_summary.csv", index=False)

best = op_summary.iloc[0].to_dict() if len(op_summary) else {}

summary = {
    "device": DEVICE,
    "quick_mode": QUICK_MODE,
    "n_rows": int(len(raw)),
    "n_operator_window_tests": int(len(op_summary)),
    "N_completed": N_LIST,
    "amp_completed": AMP_LIST,
    "best_operator_kind": best.get("operator_kind", None),
    "best_window": best.get("window", None),
    "best_q_mean": best.get("q_mean", None),
    "best_q_std": best.get("q_std", None),
    "best_I_rel_error_mean": best.get("I_rel_error_mean", None),
    "best_I_rel_error_max": best.get("I_rel_error_max", None),
    "best_delta_sign_consistency_mean": best.get("delta_sign_consistency_mean", None),
    "best_flat_slope_power_vs_dx": best.get("flat_slope_power_vs_dx", None),
    "best_flat_slope_log_rmse": best.get("flat_slope_log_rmse", None),
    "classification": (
        "HEAT_OPERATOR_STABILITY_PROMISING"
        if best and best.get("q_std", 999) < 0.5 and best.get("I_rel_error_mean", 999) < 0.25 and best.get("delta_sign_consistency_mean", 0) > 0.9
        else "HEAT_OPERATOR_STABILITY_MIXED"
    )
}

with open(f"{OUT_PREFIX}_summary.json","w") as f:
    json.dump(summary, f, indent=2)

print()
print("================ HEAT OPERATOR STABILITY SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("OPERATOR_SUMMARY:")
print(op_summary.to_csv(index=False))

print()
print("GEOMETRY_FITS:")
print(geom_fits.to_csv(index=False))

print()
print("Saved files:")
for name in [
    f"{OUT_PREFIX}_rows.csv",
    f"{OUT_PREFIX}_geometry_fits.csv",
    f"{OUT_PREFIX}_operator_summary.csv",
    f"{OUT_PREFIX}_summary.json",
]:
    print(name)
