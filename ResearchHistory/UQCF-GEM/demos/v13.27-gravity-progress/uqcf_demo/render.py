from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def _norm01(x):
    x = np.asarray(x, dtype=float)
    lo, hi = float(np.min(x)), float(np.max(x))
    if hi - lo < 1e-15:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def safefmt(x):
    return f"{float(x):+.2f}"


def _draw(fig, data, frame_index):
    fig.clf()
    rec = data["records"][frame_index]
    graph = data["graph"]
    positions = np.asarray(graph["positions"], dtype=float)
    edges = [tuple(e) for e in graph["edges"]]

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    corr = np.asarray(rec["edge_correlation"])
    corr_n = _norm01(corr)
    for k, (i, j) in enumerate(edges):
        p, q = positions[i], positions[j]
        ax1.plot([p[0], q[0]], [p[1], q[1]], linewidth=0.8 + 3.0 * corr_n[k], alpha=0.65)
    src = np.asarray(rec["node_source"])
    sizes = 90 + 650 * _norm01(np.abs(src))
    ax1.scatter(positions[:, 0], positions[:, 1], s=sizes, zorder=3)
    for i, (x, y) in enumerate(positions):
        ax1.text(x, y, str(i), ha="center", va="center", fontsize=8)
    ax1.set_title("Pre-time quantum relations")
    ax1.set_aspect("equal")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.text(0.02, 0.02, "abstract embedding — not physical space", transform=ax1.transAxes, fontsize=8)

    z = np.asarray(rec["node_geometry_score"], dtype=float)
    zplot = 0.15 + 1.8 * _norm01(z)
    nm_n = _norm01(np.asarray(rec["edge_nonmetricity"]))
    for k, (i, j) in enumerate(edges):
        ax2.plot(
            [positions[i, 0], positions[j, 0]],
            [positions[i, 1], positions[j, 1]],
            [zplot[i], zplot[j]],
            linewidth=1.0 + 2.0 * nm_n[k],
            alpha=0.7,
        )
    ax2.scatter(positions[:, 0], positions[:, 1], zplot, s=80 + 280 * _norm01(z))
    for i in range(len(positions)):
        ax2.text(positions[i, 0], positions[i, 1], zplot[i], str(i), fontsize=7)
    ax2.set_title("Retained metric-affine geometry")
    ax2.set_xlabel("abstract x")
    ax2.set_ylabel("abstract y")
    ax2.set_zlabel("retained geometry score")
    ax2.text2D(
        0.02,
        0.02,
        f"mean loop angle={rec['mean_cycle_angle']:.3f} rad\nfinite holonomy proxy, not spacetime curvature",
        transform=ax2.transAxes,
        fontsize=8,
    )

    cur = np.asarray(rec["edge_current"], dtype=float)
    maxcur = max(float(np.max(np.abs(cur))), 1e-12)
    for k, (i, j) in enumerate(edges):
        val = cur[k]
        a, b = (i, j) if val >= 0 else (j, i)
        p, q = positions[a], positions[b]
        ax3.annotate(
            "",
            xy=q,
            xytext=p,
            arrowprops=dict(arrowstyle="->", lw=0.8 + 3.0 * abs(val) / maxcur, alpha=0.7),
        )
    ax3.scatter(positions[:, 0], positions[:, 1], s=80 + 500 * _norm01(np.abs(src)))
    for i, (x, y) in enumerate(positions):
        ax3.text(x, y, f"{i}\n{safefmt(src[i])}", ha="center", va="center", fontsize=7)
    ax3.set_title("Source/current + projective coupling")
    ax3.set_aspect("equal")
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.text(
        0.02,
        0.02,
        f"||BJ-s||={rec['balance_residual']:.2e}\n[Σ] ray stable: Δdir={rec['projective_direction_change']:.2e}\n|Σ| not derived → RGCL missing",
        transform=ax3.transAxes,
        fontsize=8,
    )

    xs = np.array([r["lambda_source"] for r in data["records"][: frame_index + 1]])
    qmar = np.array([r["qmar_jet_norm"] for r in data["records"][: frame_index + 1]])
    dew = np.array([r["dewitt_diagnostic"] for r in data["records"][: frame_index + 1]])
    ax4.plot(xs, _norm01(qmar), label="QMAR jet (normalized)")
    ax4.plot(xs, dew / max(np.max(np.abs(dew)), 1e-12), label="DeWitt diagnostic (scaled)")
    ax4.axhline(0.0, linewidth=0.8)
    ax4.set_title("ADM-like diagnostics + claim ledger")
    ax4.set_xlabel("source-family parameter λ")
    ax4.set_ylabel("normalized diagnostic")
    ax4.legend(loc="upper left", fontsize=7)
    ledger = data["claim_ledger"]
    status_lines = []
    for status in ("DERIVED", "CONDITIONAL", "CONTROLLED_CORRESPONDENCE", "MISSING_LAW"):
        names = [x["name"] for x in ledger if x["status"] == status]
        if names:
            status_lines.append(f"{status}: {len(names)}")
    status_lines.append("Physical Einstein closure: OPEN")
    ax4.text(0.98, 0.02, "\n".join(status_lines), transform=ax4.transAxes, ha="right", va="bottom", fontsize=8)

    lam = rec["lambda_source"]
    fig.suptitle(
        f"UQCF-GEM v13.27 — full-stack gravity-progress simulation | source-family λ={lam:+.3f} (not physical time)",
        fontsize=14,
    )
    fig.text(
        0.5,
        0.01,
        "Derived finite quantum/metric-affine structure → conditional ADM-like diagnostics → RGCL coupling magnitude + physical Einstein closure remain open",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    return (ax1, ax2, ax3, ax4)


def render_frame(data, frame_index=-1, figsize=(19.2, 10.8), dpi=100):
    if frame_index < 0:
        frame_index = len(data["records"]) - 1
    fig = plt.figure(figsize=figsize, dpi=dpi)
    _draw(fig, data, int(frame_index))
    return fig


def save_final_frame(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig = render_frame(data, -1)
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


def save_animation(data, output_dir, fps=8, make_gif=True, make_mp4=True):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)

    def update(k):
        _draw(fig, data, k)
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(data["records"]), interval=1000 / fps, blit=False)
    outputs = {}
    if make_gif:
        gif = output_dir / "gravity_progress.gif"
        ani.save(gif, writer=animation.PillowWriter(fps=fps), dpi=100)
        outputs["gif"] = str(gif)
    if make_mp4 and animation.writers.is_available("ffmpeg"):
        mp4 = output_dir / "gravity_progress.mp4"
        ani.save(mp4, writer=animation.FFMpegWriter(fps=fps, bitrate=4000), dpi=100)
        outputs["mp4"] = str(mp4)
    plt.close(fig)
    return outputs
