
from __future__ import annotations
import numpy as np
import pandas as pd

def sample_disk(n_particles, disk_scale, disk_radius, central_mass, G, seed):
    rng = np.random.default_rng(seed)
    u = rng.random(n_particles)
    r = -disk_scale * np.log(1 - 0.98 * u)
    r = np.clip(r, 0.15, disk_radius)
    theta = rng.uniform(0, 2*np.pi, size=n_particles)
    pos = np.stack([r*np.cos(theta), r*np.sin(theta)], axis=1)
    order = np.argsort(r)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(n_particles)
    M_enc = central_mass + (6.0 / n_particles) * (ranks + 1)
    v_circ = np.sqrt(G * M_enc / np.maximum(r, 0.2))
    v_circ *= rng.normal(1.0, 0.03, size=n_particles)
    vel = np.stack([-v_circ*np.sin(theta), v_circ*np.cos(theta)], axis=1)
    return pos, vel

def enclosed_mass(pos, particle_mass, central_mass, extra_weight=None):
    r = np.linalg.norm(pos, axis=1)
    order = np.argsort(r)
    if extra_weight is None:
        masses = np.full(len(r), particle_mass)
    else:
        masses = particle_mass * (1.0 + extra_weight[order])
    M_enc_sorted = central_mass + np.cumsum(masses)
    M_enc = np.empty_like(r)
    M_enc[order] = M_enc_sorted
    return r, M_enc

def radial_acc_from_mass(pos, M_enc, G, softening, power=2.0):
    r = np.linalg.norm(pos, axis=1)
    r2 = r**2 + softening**2
    r_safe = np.sqrt(r2)
    denom = np.power(r_safe, power)
    a_mag = -G * M_enc / denom
    return (a_mag / r_safe)[:, None] * pos

def baseline_acc(pos, G, softening, particle_mass, central_mass):
    r, M = enclosed_mass(pos, particle_mass, central_mass)
    a = radial_acc_from_mass(pos, M, G, softening, power=2.0)
    return a, r, M

def bridge_acc(pos, a_newton, a_prev, m_s, m_f, alpha_s, alpha_f, beta, eps, particle_mass, central_mass, G, softening):
    phi = np.linalg.norm(a_newton - a_prev, axis=1)
    m_s = (1-alpha_s)*m_s + alpha_s*phi
    m_f = (1-alpha_f)*m_f + alpha_f*phi
    lam = m_s / (m_s + m_f + eps)
    retained_weight = m_f / (m_s + m_f + eps)
    _, M_bary = enclosed_mass(pos, particle_mass, central_mass)
    a_bary = radial_acc_from_mass(pos, M_bary, G, softening, power=2.0)
    _, M_ret = enclosed_mass(pos, particle_mass, central_mass, extra_weight=beta*retained_weight)
    a_ret = radial_acc_from_mass(pos, M_ret - central_mass, G, softening, power=1.0)
    a_bridge = lam[:,None] * a_bary + (1-lam)[:,None] * a_ret
    return a_bridge, m_s, m_f, lam, retained_weight

def radial_curve(pos, vel, n_bins=18):
    r = np.linalg.norm(pos, axis=1)
    phi = np.arctan2(pos[:,1], pos[:,0])
    v_tan = -vel[:,0]*np.sin(phi) + vel[:,1]*np.cos(phi)
    bins = np.linspace(max(0.2, r.min()), r.max(), n_bins+1)
    centers = 0.5*(bins[:-1]+bins[1:])
    vals = np.full(n_bins, np.nan)
    for i in range(n_bins):
        m = (r >= bins[i]) & (r < bins[i+1])
        if np.any(m):
            vals[i] = np.nanmean(v_tan[m])
    return centers, vals

def run(beta, seed):
    n_particles=300; n_steps=300; dt=0.01; G=1.0; softening=0.08; disk_radius=6.0; disk_scale=2.0; central_mass=6.0; particle_mass=6.0/n_particles
    alpha_s=0.03; alpha_f=0.25; eps=1e-8
    pos0, vel0 = sample_disk(n_particles, disk_scale, disk_radius, central_mass, G, seed)
    pos_n, vel_n = pos0.copy(), vel0.copy()
    acc_n, _, _ = baseline_acc(pos_n, G, softening, particle_mass, central_mass)
    pos_b, vel_b = pos0.copy(), vel0.copy()
    a_prev, _, _ = baseline_acc(pos_b, G, softening, particle_mass, central_mass)
    m_s = np.zeros(n_particles); m_f = np.zeros(n_particles)
    acc_b, m_s, m_f, lam, retained_weight = bridge_acc(pos_b, a_prev, a_prev, m_s, m_f, alpha_s, alpha_f, beta, eps, particle_mass, central_mass, G, softening)
    for _ in range(n_steps):
        vel_half = vel_n + 0.5*dt*acc_n
        pos_n = pos_n + dt*vel_half
        acc_n, _, _ = baseline_acc(pos_n, G, softening, particle_mass, central_mass)
        vel_n = vel_half + 0.5*dt*acc_n

        vel_half_b = vel_b + 0.5*dt*acc_b
        pos_b = pos_b + dt*vel_half_b
        a_newton, _, _ = baseline_acc(pos_b, G, softening, particle_mass, central_mass)
        acc_b, m_s, m_f, lam, retained_weight = bridge_acc(pos_b, a_newton, a_prev, m_s, m_f, alpha_s, alpha_f, beta, eps, particle_mass, central_mass, G, softening)
        a_prev = a_newton.copy()
        vel_b = vel_half_b + 0.5*dt*acc_b

    r_n, v_n = radial_curve(pos_n, vel_n)
    r_b, v_b = radial_curve(pos_b, vel_b)
    finite = np.isfinite(v_n) & np.isfinite(v_b)
    outer = finite & (r_n > np.nanmedian(r_n[finite]))
    return {
        "beta_bridge": beta,
        "seed": seed,
        "outer_ratio": float(np.nanmean(v_b[outer])/(np.nanmean(v_n[outer])+eps)),
        "flatness_cv_outer": float(np.nanstd(v_b[outer]) / (np.nanmean(v_b[outer]) + eps)),
        "roughness": float(np.nanstd(np.diff(v_b[finite]))) if np.sum(finite) > 3 else np.nan,
        "final_lambda": float(np.mean(lam)),
        "final_retained_weight": float(np.mean(retained_weight)),
    }

rows = []
for beta in [3.2, 3.4]:
    for seed in [11, 22, 33, 44, 55]:
        rows.append(run(beta, seed))
df = pd.DataFrame(rows)
summary = df.groupby("beta_bridge").agg(
    outer_ratio_mean=("outer_ratio","mean"),
    outer_ratio_std=("outer_ratio","std"),
    flatness_mean=("flatness_cv_outer","mean"),
    flatness_std=("flatness_cv_outer","std"),
    roughness_mean=("roughness","mean"),
    roughness_std=("roughness","std"),
    lambda_mean=("final_lambda","mean"),
).reset_index()
df.to_csv("/mnt/data/bridge_dark_sector_proxy_v4_seed_sweep.csv", index=False)
summary.to_csv("/mnt/data/bridge_dark_sector_proxy_v4_seed_sweep_summary.csv", index=False)
print("Per-run:")
print(df.to_string(index=False))
print("\nSummary:")
print(summary.to_string(index=False))
