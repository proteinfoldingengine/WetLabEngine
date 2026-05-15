#!/usr/bin/env python3
"""
faithful_recoverability_flow.py

A deliberately non-cinematic, equation-faithful visualization harness for the
retained-geometry / conformal recoverability-flow model.

It visualizes only computed quantities:

    Omega(x,y,t)
    dOmega/dt = Source - Repair - mu_defect + optional physical diffusion
    mu_defect
    C_t - C_floor
    weak-form residual
    V(t)

No artistic geometry. No fake geodesics. No smoothing except explicit operators
used in the model.

Claim boundary:
This is a synthetic weak-form adaptive-branch simulation and diagnostic viewer.
It is NOT proof of GR, physical spacetime, or universality.
"""

from pathlib import Path
import json
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

OUT = Path("faithful_recoverability_outputs")
OUT.mkdir(exist_ok=True)

EPS = 1e-9
rng = np.random.default_rng(541)


# ============================================================
# Basic numerical operators
# ============================================================
def laplacian(A, dx):
    P = np.pad(A, 1, mode="edge")
    return (
        P[:-2, 1:-1] + P[2:, 1:-1] +
        P[1:-1, :-2] + P[1:-1, 2:] -
        4.0 * P[1:-1, 1:-1]
    ) / (dx * dx)


def grad_norm(A, dx):
    gy, gx = np.gradient(A, dx, dx)
    return np.sqrt(gx * gx + gy * gy)


def gaussian(X, Y, cx, cy, w, amp):
    return amp * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2.0 * w * w))


def norm01(A):
    A = np.asarray(A, dtype=float)
    return (A - np.nanmin(A)) / (np.nanmax(A) - np.nanmin(A) + EPS)


def weighted_harmonic(etas, weights):
    etas = np.clip(etas, 1e-6, 1.0)
    weights = np.clip(weights, 0.0, None)
    return weights.sum(axis=0) / (np.sum(weights / etas, axis=0) + EPS)


# ============================================================
# Scientific state initialization
# ============================================================
def initialize_state(n=96):
    """
    Builds a synthetic branch-space field.

    Every variable is an observable/proxy used by the retained-geometry model:
    M, R, L, B, eta_convert, C, C_floor, retained stress T, repair field,
    defect measure mu_defect, and Omega.

    This is still synthetic, but the visualization is equation-faithful.
    """
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)
    dx = 1.0 / (n - 1)

    # Retained stress field: explicitly generated source load.
    T = (
        gaussian(X, Y, 0.28, 0.35, 0.075, 1.00) +
        gaussian(X, Y, 0.70, 0.58, 0.095, 0.90) +
        gaussian(X, Y, 0.47, 0.82, 0.055, 0.65)
    )
    T = norm01(T)

    # Lineage seam and pinch/bottleneck fields.
    seam_center = 0.55 + 0.08 * np.sin(8.0 * Y)
    lineage_weakness = np.exp(-((X - seam_center) ** 2) / (2.0 * 0.014 ** 2))
    pinch = (
        np.exp(-((Y - 0.52) ** 2) / (2.0 * 0.055 ** 2)) *
        np.exp(-((X - 0.62) ** 2) / (2.0 * 0.16 ** 2))
    )
    lineage_weakness = np.clip(norm01(lineage_weakness), 0, 1)
    pinch = np.clip(norm01(pinch), 0, 1)

    # Candidate recoverability channels.
    conductance = np.clip(1.0 - 0.55 * pinch - 0.35 * lineage_weakness, 0.05, 1.0)
    lineage = np.clip(1.0 - 0.75 * lineage_weakness, 0.04, 1.0)
    topology = np.clip(0.35 + 0.65 * conductance * (1.0 - 0.65 * pinch), 0.04, 1.0)
    repair_convert = np.clip(0.25 + 0.55 * conductance + 0.20 * lineage, 0.04, 1.0)
    defect_contain = np.clip(1.0 - 0.70 * pinch * lineage_weakness, 0.04, 1.0)

    etas = np.stack([conductance, lineage, topology, repair_convert, defect_contain], axis=0)

    # Necessity weights: here based on local stress exposure and channel weakness.
    # This is a synthetic intervention proxy, not a learned truth.
    weakness = 1.0 - etas
    raw_w = (0.20 + T[None, :, :]) * (0.20 + weakness)
    weights = raw_w / (raw_w.sum(axis=0, keepdims=True) + EPS)

    eta_channel = weighted_harmonic(etas, weights)

    # Minimal repair cost proxy: de-overlapped repair burden, not naive sum.
    # This is intentionally conservative: overlap is compressed instead of double-counted.
    C_repair_min = (
        0.70 * pinch * lineage_weakness +
        0.35 * T * pinch +
        0.25 * T * lineage_weakness
    )
    C_repair_min = np.clip(C_repair_min, 0, 3.0)

    eta_convert = eta_channel * np.exp(-C_repair_min)

    # Reserve terms.
    M = np.clip(0.45 + 0.35 * conductance - 0.25 * T, 0.05, 1.2)
    R = np.clip(0.35 + 0.25 * topology + 0.35 * repair_convert - 0.15 * pinch, 0.05, 1.2)
    L = np.clip(0.25 + 0.70 * lineage - 0.10 * T, 0.05, 1.2)
    B = np.clip(0.30 + 0.50 * topology + 0.30 * conductance - 0.25 * pinch, 0.03, 1.5)

    lambda0 = 0.65
    C = M * R * L + lambda0 * eta_convert * B

    C_floor = np.clip(
        0.10 + 0.25 * T + 0.20 * pinch + 0.20 * lineage_weakness - 0.10 * repair_convert,
        0.05,
        0.80,
    )
    reserve_surplus = C - C_floor

    # Weak-form source.
    Source = T / (np.maximum(reserve_surplus, 0.02) + EPS)

    # Repair field.
    Repair = np.clip(0.20 * M + 0.30 * R + 0.30 * L + 0.20 * repair_convert, 0.0, 1.25)

    # Defect measure proxy: localized where stress/reserve loading crosses weak lineage/pinch.
    mu_defect = np.clip(Source * pinch * lineage_weakness, 0.0, None)

    # Initial Omega from the current loading state.
    Omega = np.clip(1.0 + 0.20 * Source + 0.20 * lineage_weakness + 0.15 * pinch - 0.15 * Repair, 0.15, 5.0)

    return {
        "X": X,
        "Y": Y,
        "dx": dx,
        "T": T,
        "lineage_weakness": lineage_weakness,
        "pinch": pinch,
        "etas": etas,
        "weights": weights,
        "eta_channel": eta_channel,
        "C_repair_min": C_repair_min,
        "eta_convert": eta_convert,
        "M": M,
        "R": R,
        "L": L,
        "B": B,
        "lambda0": lambda0,
        "C": C,
        "C_floor": C_floor,
        "reserve_surplus": reserve_surplus,
        "Source": Source,
        "Repair": Repair,
        "mu_defect": mu_defect,
        "Omega": Omega,
    }


# ============================================================
# Diagnostics
# ============================================================
def weak_residual(Omega_prev, Omega_next, dt, Source, Repair, mu_defect, dx, diffusion_coeff):
    """
    Strong residual of the exact update law used here:

        dOmega/dt = Source - Repair - mu_defect + diffusion_coeff * Laplacian(Omega)

    The residual should be small when computed against the same numerical update.
    """
    lhs = (Omega_next - Omega_prev) / dt
    rhs = Source - Repair - mu_defect + diffusion_coeff * laplacian(Omega_prev, dx)
    return lhs - rhs


def weak_form_test_residual(residual, dx):
    """
    Weak-form residual using a small fixed family of test functions phi.

    Returns max absolute integral residual over test functions.
    """
    n = residual.shape[0]
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)

    phis = [
        np.ones_like(X),
        X,
        Y,
        np.sin(np.pi * X),
        np.sin(np.pi * Y),
        np.sin(np.pi * X) * np.sin(np.pi * Y),
    ]

    vals = [abs(float(np.sum(phi * residual) * dx * dx)) for phi in phis]
    return max(vals), vals


def lyapunov_value(Omega, C, C_floor, mu_defect, pinch, dx):
    """
    Constrained Lyapunov candidate:

        V = E[Omega]
            + reserve floor penalty
            + defect mass penalty
            + bottleneck penalty
    """
    grad = grad_norm(Omega, dx)
    E = 0.5 * float(np.sum(grad * grad) * dx * dx)

    reserve_penalty = float(np.sum(np.maximum(0.0, C_floor - C) ** 2) * dx * dx)
    defect_mass = float(np.sum(mu_defect) * dx * dx)
    bottleneck = float(np.sum(pinch * np.maximum(0.0, C_floor - C + 0.1)) * dx * dx)

    V = E + 8.0 * reserve_penalty + 2.0 * defect_mass + 2.0 * bottleneck
    return V, E, reserve_penalty, defect_mass, bottleneck


def curvature_like(Omega, dx):
    """
    2D conformal curvature-like diagnostic for g_eff = Omega^2 g0.
    For flat baseline, Gaussian curvature form is proportional to:

        K ~ -Delta(log Omega) / Omega^2

    This is a diagnostic only.
    """
    logO = np.log(np.clip(Omega, 1e-8, None))
    K = -laplacian(logO, dx) / (Omega * Omega + EPS)
    return np.clip(K, np.quantile(K, 0.01), np.quantile(K, 0.99))


# ============================================================
# Simulation
# ============================================================
def run_simulation(n=96, steps=180, dt=0.012, diffusion_coeff=0.00035):
    S = initialize_state(n)
    Omega = S["Omega"].copy()

    records = []
    frames = []

    V_prev = None

    for t in range(steps):
        Omega_prev = Omega.copy()

        rhs = (
            S["Source"]
            - S["Repair"]
            - S["mu_defect"]
            + diffusion_coeff * laplacian(Omega_prev, S["dx"])
        )

        # Faithful explicit update. No aesthetic smoothing.
        Omega = np.clip(Omega_prev + dt * rhs, 0.05, 8.0)

        residual = weak_residual(
            Omega_prev,
            Omega,
            dt,
            S["Source"],
            S["Repair"],
            S["mu_defect"],
            S["dx"],
            diffusion_coeff,
        )
        weak_max, weak_vals = weak_form_test_residual(residual, S["dx"])

        V, E, reserve_penalty, defect_mass, bottleneck = lyapunov_value(
            Omega, S["C"], S["C_floor"], S["mu_defect"], S["pinch"], S["dx"]
        )

        dV = np.nan if V_prev is None else V - V_prev
        V_prev = V

        rec = {
            "step": t,
            "time": t * dt,
            "Omega_mean": float(np.mean(Omega)),
            "Omega_max": float(np.max(Omega)),
            "Omega_min": float(np.min(Omega)),
            "weak_residual_max_test": float(weak_max),
            "strong_residual_L2": float(np.sqrt(np.mean(residual * residual))),
            "V": float(V),
            "dV": float(dV) if not np.isnan(dV) else np.nan,
            "E_grad": float(E),
            "reserve_penalty": float(reserve_penalty),
            "defect_mass": float(defect_mass),
            "bottleneck_penalty": float(bottleneck),
            "C_min_minus_floor": float(np.min(S["C"] - S["C_floor"])),
            "C_mean_minus_floor": float(np.mean(S["C"] - S["C_floor"])),
            "eta_convert_mean": float(np.mean(S["eta_convert"])),
            "repair_cost_mean": float(np.mean(S["C_repair_min"])),
        }
        records.append(rec)

        if t % 2 == 0:
            frames.append((t, Omega.copy(), residual.copy(), curvature_like(Omega, S["dx"]).copy()))

    df = pd.DataFrame(records)
    df.to_csv(OUT / "faithful_diagnostics.csv", index=False)

    np.savez_compressed(
        OUT / "faithful_fields_final.npz",
        Omega=Omega,
        Source=S["Source"],
        Repair=S["Repair"],
        mu_defect=S["mu_defect"],
        C=S["C"],
        C_floor=S["C_floor"],
        reserve_surplus=S["reserve_surplus"],
        eta_convert=S["eta_convert"],
        C_repair_min=S["C_repair_min"],
        pinch=S["pinch"],
        lineage_weakness=S["lineage_weakness"],
    )

    return S, df, frames


# ============================================================
# Static diagnostic dashboard
# ============================================================
def make_static_dashboard(S, df, frames):
    last_step, Omega, residual, K = frames[-1]

    fig, axes = plt.subplots(3, 3, figsize=(14, 12))

    panels = [
        ("Omega final", Omega),
        ("Source = T/(C-C_floor)", S["Source"]),
        ("Repair", S["Repair"]),
        ("mu_defect", S["mu_defect"]),
        ("C - C_floor", S["C"] - S["C_floor"]),
        ("eta_convert", S["eta_convert"]),
        ("weak residual final", residual),
        ("curvature-like K(Omega)", K),
        ("C_repair_min", S["C_repair_min"]),
    ]

    for ax, (title, A) in zip(axes.ravel(), panels):
        im = ax.imshow(A, origin="lower")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle("Faithful Recoverability Flow Diagnostics — computed fields only", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "faithful_static_dashboard.png", dpi=180)
    plt.close(fig)

    # Time-series diagnostics.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["time"], df["V"], label="V(t)")
    ax.plot(df["time"], df["E_grad"], label="E_grad")
    ax.plot(df["time"], df["reserve_penalty"], label="reserve penalty")
    ax.plot(df["time"], df["defect_mass"], label="defect mass")
    ax.plot(df["time"], df["bottleneck_penalty"], label="bottleneck")
    ax.set_title("Lyapunov components and defect accounting")
    ax.set_xlabel("time")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "faithful_timeseries.png", dpi=180)
    plt.close(fig)


# ============================================================
# Animation
# ============================================================
def make_animation(S, df, frames):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    titles = [
        "Omega(x,y,t)",
        "mu_defect",
        "C - C_floor",
        "weak residual",
        "curvature-like K",
        "diagnostics",
    ]

    for ax, title in zip(axes.ravel(), titles):
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])

    t0, O0, R0, K0 = frames[0]
    imgs = []
    imgs.append(axes[0, 0].imshow(O0, origin="lower", vmin=0.05, vmax=max(2.5, np.max(O0))))
    imgs.append(axes[0, 1].imshow(S["mu_defect"], origin="lower"))
    imgs.append(axes[0, 2].imshow(S["C"] - S["C_floor"], origin="lower"))
    imgs.append(axes[1, 0].imshow(R0, origin="lower"))
    imgs.append(axes[1, 1].imshow(K0, origin="lower"))

    diag_ax = axes[1, 2]
    diag_ax.axis("on")
    diag_ax.set_xticks([])
    diag_ax.set_yticks([])
    text = diag_ax.text(0.02, 0.96, "", va="top", ha="left", family="monospace", fontsize=10)

    fig.colorbar(imgs[0], ax=axes[0, 0], fraction=0.046, pad=0.04)
    fig.colorbar(imgs[1], ax=axes[0, 1], fraction=0.046, pad=0.04)
    fig.colorbar(imgs[2], ax=axes[0, 2], fraction=0.046, pad=0.04)
    fig.colorbar(imgs[3], ax=axes[1, 0], fraction=0.046, pad=0.04)
    fig.colorbar(imgs[4], ax=axes[1, 1], fraction=0.046, pad=0.04)

    def update(i):
        step, Omega, residual, K = frames[i]
        row = df.iloc[step]

        imgs[0].set_array(Omega)
        imgs[3].set_array(residual)
        imgs[4].set_array(K)

        text.set_text(
            f"step: {int(row.step)}\n"
            f"time: {row.time:.4f}\n\n"
            f"Omega mean: {row.Omega_mean:.4f}\n"
            f"Omega max : {row.Omega_max:.4f}\n\n"
            f"weak max test: {row.weak_residual_max_test:.3e}\n"
            f"strong L2    : {row.strong_residual_L2:.3e}\n\n"
            f"V(t): {row.V:.6f}\n"
            f"dV  : {row.dV:.3e}\n"
            f"defect mass: {row.defect_mass:.6f}\n"
            f"C-floor min: {row.C_min_minus_floor:.6f}\n"
            f"eta mean   : {row.eta_convert_mean:.6f}\n"
            f"repair mean: {row.repair_cost_mean:.6f}\n"
        )
        return imgs + [text]

    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=100, blit=False)

    mp4_path = OUT / "faithful_recoverability_flow.mp4"
    try:
        ani.save(mp4_path, writer="ffmpeg", fps=10, dpi=130, extra_args=["-vcodec", "libx264"])
        print(f"saved MP4: {mp4_path}")
    except Exception as e:
        print(f"MP4 save failed: {e}")
        gif_path = OUT / "faithful_recoverability_flow.gif"
        ani.save(gif_path, writer="pillow", fps=8)
        print(f"saved GIF instead: {gif_path}")

    plt.close(fig)


# ============================================================
# Main
# ============================================================
def main():
    S, df, frames = run_simulation(n=96, steps=180, dt=0.012, diffusion_coeff=0.00035)
    make_static_dashboard(S, df, frames)
    make_animation(S, df, frames)

    metadata = {
        "claim_boundary": "Synthetic weak-form recoverability-flow diagnostic. Not GR, not physical spacetime proof.",
        "equation": "dOmega/dt = Source - Repair - mu_defect + diffusion_coeff * Laplacian(Omega)",
        "reserve_law": "C = M*R*L + lambda0*eta_convert*B",
        "eta_convert": "weighted harmonic channel efficiency * exp(-C_repair_min)",
        "outputs": [
            "faithful_diagnostics.csv",
            "faithful_fields_final.npz",
            "faithful_static_dashboard.png",
            "faithful_timeseries.png",
            "faithful_recoverability_flow.mp4 or .gif",
        ],
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2))

    zip_path = Path("faithful_recoverability_flow_bundle.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(Path(__file__), arcname=Path(__file__).name)
        for p in OUT.iterdir():
            z.write(p, arcname=f"{OUT.name}/{p.name}")

    print(f"wrote bundle: {zip_path.resolve()}")
    print(df.tail().to_string(index=False))


if __name__ == "__main__":
    main()
