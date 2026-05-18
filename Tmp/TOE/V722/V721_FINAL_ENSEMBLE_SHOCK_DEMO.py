# ================================================
# V721 FINAL ENSEMBLE SHOCK DEMO + INVERSE PROBLEM
# 3-panel animation + relaxation window shading + CSV audit log
# Run in Google Colab → auto-downloads MP4, GIF, and CSV
# ================================================

!apt-get update -qq > /dev/null 2>&1
!apt-get install -y ffmpeg > /dev/null 2>&1

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from google.colab import files
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# ====================== PARAMETERS ======================
n_steps = 380
dt = 0.085
target = np.zeros(2)
damping = 1.0
drive_noise = 0.014
probe_noise = 0.009
perturb_mag = 0.23
probe_start = 110
n_probes = 12
probe_times = np.linspace(probe_start, n_steps-50, n_probes, dtype=int)
relax_steps = 16                     # ← this is the key V721 window

high_k = 1.00
low_k = 0.35
n_ensemble = 8

# ====================== SIMULATION ======================
def simulate_2d(k, seed_offset=0):
    rng = np.random.default_rng(721 + seed_offset)
    x = rng.normal(0, 0.035, size=2)
    traj = []
    for t in range(n_steps):
        x += rng.normal(0, drive_noise, size=2)
        if t in probe_times:
            impulse = np.array([perturb_mag * rng.choice([-1., 1.]),
                               perturb_mag * 0.45 * rng.choice([-1., 1.])])
            x += impulse
            for _ in range(relax_steps):
                dx = -(k / damping) * x + rng.normal(0, probe_noise, size=2)
                x += dx * dt
        else:
            dx = -(k / damping) * x + rng.normal(0, probe_noise, size=2)
            x += dx * dt
        traj.append(x.copy())
    return np.array(traj)

print("Simulating ensembles...")
high_ensemble = np.stack([simulate_2d(high_k, i) for i in range(n_ensemble)])
low_ensemble  = np.stack([simulate_2d(low_k, i + n_ensemble) for i in range(n_ensemble)])
print("Simulation complete.")

# ====================== V721 INVERSE: adm_z ======================
def extract_post_restoration_dists(traj_ensemble, probe_times, relax_steps=16):
    n_ens, n_steps, dim = traj_ensemble.shape
    post_dists = np.zeros((n_ens, len(probe_times)))
    for i, t in enumerate(probe_times):
        post_idx = min(t + relax_steps, n_steps - 1)
        dist = np.linalg.norm(traj_ensemble[:, post_idx, :], axis=1)
        post_dists[:, i] = dist
    return post_dists

high_post = extract_post_restoration_dists(high_ensemble, probe_times, relax_steps)
low_post  = extract_post_restoration_dists(low_ensemble, probe_times, relax_steps)

high_mean_post = high_post.mean(axis=1)
low_mean_post  = low_post.mean(axis=1)

adm_mean = high_mean_post.mean()
adm_std  = high_mean_post.std(ddof=1) + 1e-12

high_adm_z = (high_mean_post - adm_mean) / adm_std
low_adm_z  = (low_mean_post - adm_mean) / adm_std

print("\n=== V721 INVERSE PROBLEM RESULTS ===")
print(f"High-k (admissible) adm_z: {high_adm_z.mean():.2f} ± {high_adm_z.std():.2f}")
print(f"Low-k  (failing)    adm_z: {low_adm_z.mean():.2f} ± {low_adm_z.std():.2f}")
print(f"Separation: {low_adm_z.mean() - high_adm_z.mean():.1f} sigma")

# ====================== EXPORT AUDIT LOG ======================
audit_data = []
for i, t in enumerate(probe_times):
    audit_data.append({
        "probe_index": i,
        "probe_time": int(t),
        "high_adm_z_mean": high_adm_z.mean(),
        "low_adm_z_mean": low_adm_z.mean(),
        "high_mean_post_dist": high_mean_post.mean(),
        "low_mean_post_dist": low_mean_post.mean()
    })

audit_df = pd.DataFrame(audit_data)
audit_df.to_csv("v721_audit_log.csv", index=False)
print("✅ Exported v721_audit_log.csv")
files.download("v721_audit_log.csv")

# ====================== 3-PANEL ANIMATION ======================
fig = plt.figure(figsize=(18, 10))
fig.suptitle('V721 Ensemble Shock Demo — Passive Illusion → Dynamical Response Reveal\n'
             'Shaded relaxation windows show the exact V721 observation interval',
             fontsize=16, fontweight='bold', y=0.98)

ax_time_high = fig.add_subplot(2, 2, 1)
ax_time_low  = fig.add_subplot(2, 2, 3, sharex=ax_time_high)
ax_phase_high = fig.add_subplot(2, 2, 2)
ax_phase_low  = fig.add_subplot(2, 2, 4)

# Flow fields
x_grid, y_grid = np.meshgrid(np.linspace(-0.45, 0.45, 22), np.linspace(-0.45, 0.45, 22))
def plot_flow(ax, k_val, color):
    u = -k_val * x_grid
    v = -k_val * y_grid
    ax.quiver(x_grid, y_grid, u, v, alpha=0.18, color=color, scale=9)

plot_flow(ax_phase_high, high_k, 'blue')
plot_flow(ax_phase_low, low_k, 'darkorange')

# Artists
mean_high, = ax_time_high.plot([], [], 'b-', lw=2.5)
std_high = None
mean_low, = ax_time_low.plot([], [], color='darkorange', lw=2.5)
std_low = None

lines_high = [ax_phase_high.plot([], [], 'b-', lw=1.2, alpha=0.6)[0] for _ in range(n_ensemble)]
dots_high  = [ax_phase_high.plot([], [], 'bo', markersize=6)[0] for _ in range(n_ensemble)]
lines_low  = [ax_phase_low.plot([], [], color='darkorange', lw=1.2, alpha=0.6)[0] for _ in range(n_ensemble)]
dots_low   = [ax_phase_low.plot([], [], color='darkorange', markersize=6)[0] for _ in range(n_ensemble)]

ax_time_high.set_ylabel('State x₁ (ensemble)')
ax_time_low.set_xlabel('Time steps')
ax_time_high.set_title('High k — Strong Restorative Flow')
ax_time_low.set_title('Low k — Weak Restorative Flow')
ax_time_high.grid(True, alpha=0.3)
ax_time_low.grid(True, alpha=0.3)

# Relaxation window shading (the V721 tweak)
for t in probe_times:
    ax_time_high.axvspan(t, t + relax_steps, alpha=0.12, color='red')
    ax_time_low.axvspan(t, t + relax_steps, alpha=0.12, color='red')

probes_high = [ax_time_high.axvline(t, color='darkred', alpha=0.7, lw=1.8) for t in probe_times]
probes_low  = [ax_time_low.axvline(t, color='darkred', alpha=0.7, lw=1.8) for t in probe_times]

metrics_text = ax_phase_low.text(0.02, 0.95, '', transform=ax_phase_low.transAxes, 
                                 fontsize=11, va='top',
                                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

def animate(frame):
    global std_high, std_low
    t = np.arange(frame + 1)
    high_x1 = high_ensemble[:, :frame+1, 0]
    low_x1  = low_ensemble[:, :frame+1, 0]
    
    mean_h = high_x1.mean(axis=0)
    std_h_val = high_x1.std(axis=0)
    mean_l = low_x1.mean(axis=0)
    std_l_val = low_x1.std(axis=0)
    
    mean_high.set_data(t, mean_h)
    mean_low.set_data(t, mean_l)
    
    if std_high is not None: std_high.remove()
    std_high = ax_time_high.fill_between(t, mean_h - std_h_val, mean_h + std_h_val, color='blue', alpha=0.25)
    
    if std_low is not None: std_low.remove()
    std_low = ax_time_low.fill_between(t, mean_l - std_l_val, mean_l + std_l_val, color='darkorange', alpha=0.25)
    
    for i, tp in enumerate(probe_times):
        alpha = 1.0 if frame >= tp else 0.0
        probes_high[i].set_alpha(alpha)
        probes_low[i].set_alpha(alpha)
    
    for i in range(n_ensemble):
        lines_high[i].set_data(high_ensemble[i, :frame+1, 0], high_ensemble[i, :frame+1, 1])
        dots_high[i].set_data([high_ensemble[i, frame, 0]], [high_ensemble[i, frame, 1]])
        lines_low[i].set_data(low_ensemble[i, :frame+1, 0], low_ensemble[i, :frame+1, 1])
        dots_low[i].set_data([low_ensemble[i, frame, 0]], [low_ensemble[i, frame, 1]])
    
    dist_high = np.abs(high_ensemble[:, frame, :]).mean()
    dist_low  = np.abs(low_ensemble[:, frame, :]).mean()
    spread_high = high_ensemble[:, frame, :].std(axis=0).mean()
    spread_low  = low_ensemble[:, frame, :].std(axis=0).mean()
    
    metrics_text.set_text(
        f'Frame: {frame}\n\n'
        f'High k |x| mean: {dist_high:.3f}\n'
        f'High k spread:  {spread_high:.3f}\n\n'
        f'Low k |x| mean:  {dist_low:.3f}\n'
        f'Low k spread:   {spread_low:.3f}\n\n'
        f'High k → stable\nLow k → fails'
    )
    
    return [mean_high, mean_low] + lines_high + dots_high + lines_low + dots_low + [metrics_text]

# ====================== RUN ANIMATION ======================
ani = FuncAnimation(fig, animate, frames=n_steps, interval=28, blit=False)

mp4_path = "v721_ensemble_shock_demo.mp4"
gif_path = "v721_ensemble_shock_demo.gif"

print("\nRendering animation (~35–50 seconds)...")
ani.save(mp4_path, writer=FFMpegWriter(fps=28, bitrate=2800, extra_args=['-pix_fmt', 'yuv420p']))
ani.save(gif_path, writer=PillowWriter(fps=22))

print("✅ DONE!")
print(f"   • {mp4_path}")
print(f"   • {gif_path}")
print(f"   • v721_audit_log.csv")
files.download(mp4_path)
files.download(gif_path)
