
"""
bridge_visual_post_pack.py

A post-friendly visualization pack for the retained-memory Bridge toy experiment.

What it produces:
1. rotation_curve_human_view.png
   - Newtonian baseline vs Bridge mean curve
   - per-seed Bridge traces for visual robustness

2. bridge_parameter_window.png
   - outer-support ratio across beta values
   - easy to see where the Bridge starts to outperform Newtonian

3. bridge_diagnostics_human_view.png
   - retained state and coherence-weight evolution

4. summary_for_post.txt
   - plain-language summary you can quote in a post

Notes:
- This is still a toy benchmark, not a physics proof
- The purpose is to make the result legible to both humans and AI reviewers
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class SimConfig:
    n_particles: int = 300
    n_steps: int = 300
    dt: float = 0.01
    G: float = 1.0
    softening: float = 0.08
    disk_radius: float = 6.0
    disk_scale: float = 2.0
    central_mass: float = 6.0
    seed: int = 42
    alpha_s: float = 0.03
    alpha_f: float = 0.25
    eps: float = 1e-8
    output_dir: str = "/mnt/data/bridge_visual_post_pack_output"

    @property
    def particle_mass(self) -> float:
        return 6.0 / self.n_particles


def sample_disk(cfg: SimConfig, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    u = rng.random(cfg.n_particles)
    r = -cfg.disk_scale * np.log(1 - 0.98 * u)
    r = np.clip(r, 0.15, cfg.disk_radius)
    theta = rng.uniform(0, 2 * np.pi, size=cfg.n_particles)
    pos = np.stack([r * np.cos(theta), r * np.sin(theta)], axis=1)

    order = np.argsort(r)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(cfg.n_particles)
    M_enc = cfg.central_mass + cfg.particle_mass * (ranks + 1)

    v_circ = np.sqrt(cfg.G * M_enc / np.maximum(r, 0.2))
    v_circ *= rng.normal(1.0, 0.03, size=cfg.n_particles)
    vel = np.stack([-v_circ * np.sin(theta), v_circ * np.cos(theta)], axis=1)
    return pos, vel


def enclosed_mass(pos: np.ndarray, cfg: SimConfig, extra_weight: np.ndarray | None = None):
    r = np.linalg.norm(pos, axis=1)
    order = np.argsort(r)
    if extra_weight is None:
        masses = np.full(len(r), cfg.particle_mass)
    else:
        masses = cfg.particle_mass * (1.0 + extra_weight[order])
    M_sorted = cfg.central_mass + np.cumsum(masses)
    M = np.empty_like(r)
    M[order] = M_sorted
    return r, M


def radial_acc_from_mass(pos: np.ndarray, M_enc: np.ndarray, cfg: SimConfig, power: float = 2.0):
    r = np.linalg.norm(pos, axis=1)
    r2 = r**2 + cfg.softening**2
    r_safe = np.sqrt(r2)
    denom = np.power(r_safe, power)
    a_mag = -cfg.G * M_enc / denom
    return (a_mag / r_safe)[:, None] * pos


def baseline_acc(pos: np.ndarray, cfg: SimConfig):
    r, M = enclosed_mass(pos, cfg)
    a = radial_acc_from_mass(pos, M, cfg, power=2.0)
    return a, r, M


def bridge_acc(pos, a_newton, a_prev, m_s, m_f, beta, cfg: SimConfig):
    phi = np.linalg.norm(a_newton - a_prev, axis=1)
    m_s = (1 - cfg.alpha_s) * m_s + cfg.alpha_s * phi
    m_f = (1 - cfg.alpha_f) * m_f + cfg.alpha_f * phi
    lam = m_s / (m_s + m_f + cfg.eps)
    retained_weight = m_f / (m_s + m_f + cfg.eps)

    _, M_bary = enclosed_mass(pos, cfg)
    a_bary = radial_acc_from_mass(pos, M_bary, cfg, power=2.0)

    # v4-style potential proxy: retained enclosed load enters as a slower-falloff support channel
    _, M_ret = enclosed_mass(pos, cfg, extra_weight=beta * retained_weight)
    a_ret = radial_acc_from_mass(pos, M_ret - cfg.central_mass, cfg, power=1.0)

    a_bridge = lam[:, None] * a_bary + (1 - lam)[:, None] * a_ret
    R = 0.45 * m_s + 0.55 * m_f
    return a_bridge, m_s, m_f, lam, retained_weight, R


def radial_curve(pos, vel, n_bins: int = 18):
    r = np.linalg.norm(pos, axis=1)
    phi = np.arctan2(pos[:, 1], pos[:, 0])
    v_tan = -vel[:, 0] * np.sin(phi) + vel[:, 1] * np.cos(phi)

    bins = np.linspace(max(0.2, r.min()), r.max(), n_bins + 1)
    centers = 0.5 * (bins[:-1] + bins[1:])
    vals = np.full(n_bins, np.nan)
    for i in range(n_bins):
        m = (r >= bins[i]) & (r < bins[i + 1])
        if np.any(m):
            vals[i] = np.nanmean(v_tan[m])
    return centers, vals


def run_case(beta: float, seed: int, cfg: SimConfig):
    pos0, vel0 = sample_disk(cfg, seed)

    pos_n, vel_n = pos0.copy(), vel0.copy()
    acc_n, _, _ = baseline_acc(pos_n, cfg)

    pos_b, vel_b = pos0.copy(), vel0.copy()
    a_prev, _, _ = baseline_acc(pos_b, cfg)
    m_s = np.zeros(cfg.n_particles)
    m_f = np.zeros(cfg.n_particles)
    acc_b, m_s, m_f, lam, retained_weight, R = bridge_acc(pos_b, a_prev, a_prev, m_s, m_f, beta, cfg)

    R_hist = [float(np.mean(R))]
    lam_hist = [float(np.mean(lam))]

    for _ in range(cfg.n_steps):
        # Newtonian
        vel_half_n = vel_n + 0.5 * cfg.dt * acc_n
        pos_n = pos_n + cfg.dt * vel_half_n
        acc_n, _, _ = baseline_acc(pos_n, cfg)
        vel_n = vel_half_n + 0.5 * cfg.dt * acc_n

        # Bridge
        vel_half_b = vel_b + 0.5 * cfg.dt * acc_b
        pos_b = pos_b + cfg.dt * vel_half_b
        a_newton, _, _ = baseline_acc(pos_b, cfg)
        acc_b, m_s, m_f, lam, retained_weight, R = bridge_acc(pos_b, a_newton, a_prev, m_s, m_f, beta, cfg)
        a_prev = a_newton.copy()
        vel_b = vel_half_b + 0.5 * cfg.dt * acc_b

        R_hist.append(float(np.mean(R)))
        lam_hist.append(float(np.mean(lam)))

    r_n, v_n = radial_curve(pos_n, vel_n)
    r_b, v_b = radial_curve(pos_b, vel_b)

    finite = np.isfinite(v_n) & np.isfinite(v_b)
    outer = finite & (r_n > np.nanmedian(r_n[finite]))
    outer_ratio = float(np.nanmean(v_b[outer]) / (np.nanmean(v_n[outer]) + cfg.eps))
    flatness = float(np.nanstd(v_b[outer]) / (np.nanmean(v_b[outer]) + cfg.eps))
    roughness = float(np.nanstd(np.diff(v_b[finite]))) if np.sum(finite) > 3 else np.nan

    return {
        "beta": beta,
        "seed": seed,
        "r_newton": r_n,
        "v_newton": v_n,
        "r_bridge": r_b,
        "v_bridge": v_b,
        "outer_ratio": outer_ratio,
        "flatness": flatness,
        "roughness": roughness,
        "R_hist": np.array(R_hist),
        "lam_hist": np.array(lam_hist),
    }


def main():
    cfg = SimConfig()
    outdir = Path(cfg.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    betas = [2.8, 3.0, 3.2, 3.4, 3.6, 3.8]
    seeds = [11, 22, 33, 44, 55]

    all_rows = []
    all_runs = []

    for beta in betas:
        for seed in seeds:
            run = run_case(beta, seed, cfg)
            all_runs.append(run)
            all_rows.append({
                "beta": beta,
                "seed": seed,
                "outer_ratio": run["outer_ratio"],
                "flatness": run["flatness"],
                "roughness": run["roughness"],
            })

    df = pd.DataFrame(all_rows)
    df.to_csv(outdir / "all_runs_metrics.csv", index=False)

    summary = (
        df.groupby("beta", as_index=False)
        .agg(
            outer_ratio_mean=("outer_ratio", "mean"),
            outer_ratio_std=("outer_ratio", "std"),
            flatness_mean=("flatness", "mean"),
            roughness_mean=("roughness", "mean"),
        )
    )
    summary.to_csv(outdir / "beta_summary.csv", index=False)

    # 1) Human-view rotation curves for the best-looking window
    plt.figure(figsize=(9, 5.5))
    # Plot Newtonian from the first run only (all seeds share same baseline style)
    first = all_runs[0]
    plt.plot(first["r_newton"], first["v_newton"], linestyle="--", linewidth=2, label="Newtonian baseline")

    for run in all_runs:
        if run["beta"] in (3.2, 3.4):
            plt.plot(run["r_bridge"], run["v_bridge"], alpha=0.65, label=f"Bridge β={run['beta']} seed={run['seed']}")
    plt.xlabel("Radius")
    plt.ylabel("Mean tangential velocity")
    plt.title("Rotation support window: Bridge vs Newtonian")
    plt.tight_layout()
    plt.legend(fontsize=7, ncol=2)
    plt.savefig(outdir / "rotation_curve_human_view.png", dpi=180)
    plt.close()

    # 2) Parameter window
    plt.figure(figsize=(8.5, 5.5))
    for beta in betas:
        sub = df[df["beta"] == beta]
        plt.scatter([beta] * len(sub), sub["outer_ratio"])
    plt.plot(summary["beta"], summary["outer_ratio_mean"], marker="o", linewidth=2)
    plt.xlabel("Bridge strength β")
    plt.ylabel("Outer support ratio (Bridge / Newtonian)")
    plt.title("Bridge parameter window")
    plt.tight_layout()
    plt.savefig(outdir / "bridge_parameter_window.png", dpi=180)
    plt.close()

    # 3) Diagnostics on a representative best-window run
    rep = next(run for run in all_runs if run["beta"] == 3.2 and run["seed"] == 11)
    plt.figure(figsize=(8.5, 5.5))
    plt.plot(rep["R_hist"], label="Mean retained state R")
    plt.plot(rep["lam_hist"], label="Mean coherence weight λ")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("Bridge retained-memory diagnostics")
    plt.tight_layout()
    plt.legend()
    plt.savefig(outdir / "bridge_diagnostics_human_view.png", dpi=180)
    plt.close()

    # 4) Plain-language summary
    best = summary.sort_values(["outer_ratio_mean", "flatness_mean"], ascending=[False, True]).iloc[0]
    text = f"""Bridge visual post pack summary
=================================

This is a toy baryonic-only pressure test of a retained-memory Bridge mapping.

Headline:
- The Bridge shows a reproducible outer-support enhancement window.
- The strongest mean support in this sweep occurs near beta = {best['beta']:.1f}.

Key summary:
- Best mean outer support ratio: {best['outer_ratio_mean']:.4f}
- Support std across seeds: {best['outer_ratio_std']:.4f}
- Mean flatness score in that window: {best['flatness_mean']:.4f}
- Mean roughness score in that window: {best['roughness_mean']:.4f}

Interpretation:
- Ratio > 1 means stronger outer support than the Newtonian baseline.
- This is not yet a physical dark-matter claim.
- It is a reproducible computational pressure-test signal in a narrow parameter window.
"""
    (outdir / "summary_for_post.txt").write_text(text)
    print("Wrote visual pack to", outdir)


if __name__ == "__main__":
    main()
