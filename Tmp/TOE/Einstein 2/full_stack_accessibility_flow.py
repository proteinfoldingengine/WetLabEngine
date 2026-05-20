#!/usr/bin/env python3
"""
V831 Full Stack — Accessibility-Flow / ADM-like Visualization Engine

This is a cleaned full-stack visualization artifact.

Guardrails:
- ordered_slice is NOT physical time
- ADM-like means diagnostic analogy, not actual ADM/GR proof
- curvature proxy is a conformal/accessibility diagnostic, not spacetime curvature
- phase winding is computed from theta, not from J = -grad(logA)
- no quantum-spin claim

Outputs:
- v831_full_stack_accessibility_flow.mp4
- v831_full_stack_accessibility_flow.png
- v831_full_stack_diagnostics.csv
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ALPHA = 0.127348327184804
ETA = 0.35
EPS = 1e-8
N_GRID = 110
BOUND = 6.0
TOTAL_FRAMES = 90
FPS = 20

OUTPUT_MP4 = "v831_full_stack_accessibility_flow.mp4"
OUTPUT_PNG = "v831_full_stack_accessibility_flow.png"
OUTPUT_CSV = "v831_full_stack_diagnostics.csv"
SAVE_MP4 = True


def laplacian(F: np.ndarray, dx: float) -> np.ndarray:
    return (
        np.roll(F, 1, axis=1)
        + np.roll(F, -1, axis=1)
        + np.roll(F, 1, axis=0)
        + np.roll(F, -1, axis=0)
        - 4.0 * F
    ) / (dx * dx)


def gradient(F: np.ndarray, dx: float) -> tuple[np.ndarray, np.ndarray]:
    gy, gx = np.gradient(F, dx, edge_order=2)
    return gx, gy


def sample_nearest(F: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    n = F.shape[0]
    ix = np.clip(((xs + BOUND) / (2 * BOUND) * (n - 1)).astype(int), 0, n - 1)
    iy = np.clip(((ys + BOUND) / (2 * BOUND) * (n - 1)).astype(int), 0, n - 1)
    return F[iy, ix]


def winding_from_phase(theta_vals: np.ndarray) -> float:
    unwrapped = np.unwrap(theta_vals)
    return float((unwrapped[-1] - unwrapped[0]) / (2 * np.pi))


def compute_fields(slice_phase: float, apply_gauge_chaos: bool = True) -> dict:
    x = np.linspace(-BOUND, BOUND, N_GRID)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x, indexing="xy")
    R = np.sqrt(X * X + Y * Y)

    # Ordered-slice moving defects. This is not physical time.
    vA_x = 1.8 * np.cos(1.2 * slice_phase)
    vA_y = 1.8 * np.sin(1.2 * slice_phase)
    vB_x = -2.2 * np.cos(-0.8 * slice_phase)
    vB_y = 1.2 * np.sin(-0.8 * slice_phase)

    mu = 2.5 * np.exp(-((X - vA_x) ** 2 + (Y - vA_y) ** 2) / 1.5)
    mu += 3.0 * np.exp(-((X - vB_x) ** 2 + (Y - vB_y) ** 2) / 1.0)

    repair = np.cos(R * 1.4 - slice_phase * 2.5) * np.exp(-R / (BOUND * 0.8))
    C = ETA * repair - 0.25 * mu
    A_base = np.exp(C - mu + ETA * repair)

    if apply_gauge_chaos:
        Lambda = 0.9 * np.sin(1.8 * X + slice_phase) * np.cos(1.8 * Y - 1.3 * slice_phase)
        A_observed = A_base * np.exp(Lambda)
    else:
        Lambda = np.zeros_like(X)
        A_observed = A_base.copy()

    log_base = np.log(A_base + EPS)
    log_obs = np.log(A_observed + EPS)

    theta_A = np.arctan2(Y - vA_y, X - vA_x)
    theta_B = np.arctan2(Y - vB_y, X - vB_x)
    theta_raw = theta_A - theta_B
    theta_mod = np.mod(theta_raw, 2 * np.pi)

    lap_obs = laplacian(log_obs, dx)
    lap_lambda = laplacian(Lambda, dx)

    H_raw = 2 * ALPHA * lap_obs
    H_like = H_raw - 2 * ALPHA * lap_lambda
    H_structural = 2 * ALPHA * laplacian(log_base, dx)
    gauge_residual = H_like - H_structural

    gx, gy = gradient(log_obs, dx)
    Jx, Jy = -gx, -gy

    curvature_weight = np.abs(lap_obs)
    Mx = Jx * curvature_weight
    My = Jy * curvature_weight
    M_mag = np.sqrt(Mx * Mx + My * My)

    # Phase-winding diagnostic loop around defect A.
    loop_radius = 1.0
    phi = np.linspace(0, 2 * np.pi, 160, endpoint=True)
    loop_x = vA_x + loop_radius * np.cos(phi)
    loop_y = vA_y + loop_radius * np.sin(phi)

    theta_loop = sample_nearest(theta_raw, loop_x, loop_y)
    phase_winding = winding_from_phase(theta_loop)

    # Accessibility-flow circulation diagnostic, not quantum spin.
    dl_x = -loop_radius * np.sin(phi) * (phi[1] - phi[0])
    dl_y = loop_radius * np.cos(phi) * (phi[1] - phi[0])
    Jx_loop = sample_nearest(Jx, loop_x, loop_y)
    Jy_loop = sample_nearest(Jy, loop_x, loop_y)
    flow_circulation = float(np.sum(Jx_loop * dl_x + Jy_loop * dl_y))

    weak_energy = float(np.mean(H_like ** 2))
    flow_energy = float(np.mean(M_mag ** 2))
    gauge_residual_rms = float(np.sqrt(np.mean(gauge_residual ** 2)))

    sl = (slice(3, -3), slice(3, -3))
    return dict(
        X=X[sl],
        Y=Y[sl],
        A_observed=A_observed[sl],
        theta=theta_mod[sl],
        H_like=H_like[sl],
        M_mag=M_mag[sl],
        Mx=Mx[sl],
        My=My[sl],
        loop_x=loop_x,
        loop_y=loop_y,
        vA_x=vA_x,
        vA_y=vA_y,
        phase_winding=phase_winding,
        flow_circulation=flow_circulation,
        weak_energy=weak_energy,
        flow_energy=flow_energy,
        gauge_residual_rms=gauge_residual_rms,
    )


def main():
    diagnostics = []

    fig = plt.figure(figsize=(16, 10), dpi=100)
    fig.suptitle(
        "V831 Full Stack — Accessibility-Flow Geometry Across Ordered Slices\n"
        "Gauge-corrected curvature proxy, ADM-like flow, and phase-winding diagnostics",
        fontsize=13,
        fontweight="bold",
        y=0.97,
    )

    ax0 = plt.subplot2grid((2, 6), (0, 0), colspan=2)
    ax1 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
    ax2 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
    ax3 = plt.subplot2grid((2, 6), (1, 0), colspan=3)
    ax4 = plt.subplot2grid((2, 6), (1, 3), colspan=3)
    axs = [ax0, ax1, ax2, ax3, ax4]

    f0 = compute_fields(0.0)
    X, Y = f0["X"], f0["Y"]

    im0 = ax0.pcolormesh(X, Y, f0["A_observed"], cmap="viridis", shading="auto", vmin=0, vmax=3.5)
    ax0.set_title("1. Observed Accessibility Density A′\nA′ = A exp(Λ)", fontsize=10)
    fig.colorbar(im0, ax=ax0, fraction=0.046, pad=0.04)

    im1 = ax1.pcolormesh(X, Y, f0["theta"], cmap="twilight", shading="auto", vmin=0, vmax=2*np.pi)
    ax1.set_title("2. Phase Field θ\nPhase-winding structure", fontsize=10)
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    im2 = ax2.pcolormesh(X, Y, f0["H_like"], cmap="coolwarm", shading="auto", vmin=-1.5, vmax=1.5)
    ax2.set_title("3. Gauge-corrected Curvature Proxy H_like\nConformal/accessibility diagnostic", fontsize=10)
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    im3 = ax3.pcolormesh(X, Y, f0["M_mag"], cmap="inferno", shading="auto", vmin=0, vmax=3.5)
    ax3.set_title("4. ADM-like Accessibility Flow |M_i|\nM_i = J_i |ΔlogA′|", fontsize=10)
    fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    skip = 6
    q = ax3.quiver(
        X[::skip, ::skip], Y[::skip, ::skip],
        f0["Mx"][::skip, ::skip], f0["My"][::skip, ::skip],
        color="white", alpha=0.75, scale=22
    )

    ax4.set_facecolor("#0f0f1f")
    loop_line, = ax4.plot(f0["loop_x"], f0["loop_y"], color="#00ffcc", lw=2.5, label="phase diagnostic loop")
    defect_dot, = ax4.plot([f0["vA_x"]], [f0["vA_y"]], "ro", markersize=8, label="defect core A")
    diag_text = ax4.text(
        -4.75, 4.40, "",
        color="#00ffcc", fontsize=10, fontweight="bold",
        bbox=dict(facecolor="black", alpha=0.65, edgecolor="#00ffcc")
    )
    ax4.set_title("5. Loop Diagnostics\nPhase winding + flow circulation", fontsize=10)
    ax4.legend(loc="lower right", facecolor="black", labelcolor="white")

    for ax in axs:
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect("equal")
        ax.grid(True, linestyle=":", alpha=0.2, color="gray")

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.3)

    def update(frame_idx):
        slice_phase = (frame_idx / TOTAL_FRAMES) * 2 * np.pi
        f = compute_fields(slice_phase)

        im0.set_array(f["A_observed"].ravel())
        im1.set_array(f["theta"].ravel())
        im2.set_array(f["H_like"].ravel())
        im3.set_array(f["M_mag"].ravel())
        q.set_UVC(f["Mx"][::skip, ::skip].ravel(), f["My"][::skip, ::skip].ravel())

        loop_line.set_data(f["loop_x"], f["loop_y"])
        defect_dot.set_data([f["vA_x"]], [f["vA_y"]])

        diag_text.set_text(
            "ordered slice: {:03d}\n"
            "phase winding: {:+.3f}\n"
            "flow circulation: {:+.3f}\n"
            "gauge residual RMS: {:.3e}\n"
            "weak energy: {:.3f}\n"
            "flow energy: {:.3f}".format(
                frame_idx,
                f["phase_winding"],
                f["flow_circulation"],
                f["gauge_residual_rms"],
                f["weak_energy"],
                f["flow_energy"],
            )
        )

        diagnostics.append(dict(
            ordered_slice=frame_idx,
            slice_phase=slice_phase,
            phase_winding=f["phase_winding"],
            flow_circulation=f["flow_circulation"],
            gauge_residual_rms=f["gauge_residual_rms"],
            weak_energy=f["weak_energy"],
            flow_energy=f["flow_energy"],
        ))

        return im0, im1, im2, im3, q, loop_line, defect_dot, diag_text

    ani = animation.FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=50, blit=True)

    update(TOTAL_FRAMES - 1)
    plt.savefig(OUTPUT_PNG, dpi=180, bbox_inches="tight")

    if SAVE_MP4:
        try:
            ani.save(OUTPUT_MP4, writer="ffmpeg", fps=FPS, extra_args=["-vcodec", "libx264", "-pix_fmt", "yuv420p"])
            print("[+] MP4 exported:", OUTPUT_MP4)
        except Exception as e:
            print("[!] MP4 export failed:", e)

    df = pd.DataFrame(diagnostics)
    df = df.drop_duplicates(subset=["ordered_slice"], keep="last").sort_values("ordered_slice")
    df.to_csv(OUTPUT_CSV, index=False)
    print("[+] PNG exported:", OUTPUT_PNG)
    print("[+] diagnostics exported:", OUTPUT_CSV)


if __name__ == "__main__":
    print("[*] Building full-stack accessibility-flow visualization.")
    print("[*] Guardrail: ordered slices only; no physical-time interpretation.")
    main()
    print("[+] Complete.")
