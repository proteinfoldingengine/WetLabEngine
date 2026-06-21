#!/usr/bin/env python3
"""
mouse_in_the_maze.py
================================================================================
An agent ("mouse") embedded in the Phase 50.2j pruning network, living by its
rules. The network is a modular graph that prunes itself to a natural stop under
a length-weighted stress (long-range "bridge" edges are stressed hardest and die
first). The mouse is a READ-ONLY rider: it can only step along currently-surviving
edges, greedily touring one waypoint per module. It does not affect the physics;
the physics acts on it.

What you watch: the mouse traverses the network WHILE the network dies around it.
Early life is globally connected (long-range roads open); the roads prune away
over time (long-range first); late life is a set of disconnected islands. The
mouse gets as far as the closing window allows, then is stranded where it stands.

Honest notes on what this is and isn't:
- The conservation, pruning, and long-range-dies-first behavior are real, emergent
  properties of the engine (verified across seeds/rates in prior analysis).
- The 3D torus layout is for viewing only; the dynamics live on the graph topology,
  not on the xyz coordinates.
- This is a minimal information-dynamics toy. It exhibits the *structural silhouette*
  of scale-ordered relaxation (which RG flow, cosmological horizon decoupling, and
  order-melting all share) because it instantiates that shared skeleton — not because
  it is any specific physical theory.

Run:
    pip install numpy matplotlib
    python mouse_in_the_maze.py
Produces mouse_in_the_maze.mp4 (needs ffmpeg) — or set SAVE_GIF=True for a GIF.
"""

import collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import animation

EPS = 1e-12
SAVE_GIF = False  # True -> .gif (no ffmpeg needed); False -> .mp4


# ----------------------------------------------------------------------------
# Graph + layout (modular network; the maze the mouse lives in)
# ----------------------------------------------------------------------------
def build_candidate_graph(modules=8, module_size=10):
    N = modules * module_size
    edges, lengths = [], []
    for m in range(modules):
        b = m * module_size
        for s in [1, 2, 3, 4, 5]:
            for u in range(module_size):
                edges.append((b + u, b + ((u + s) % module_size))); lengths.append(float(s))
    for m in range(modules):  # short bridges to next module
        nm = (m + 1) % modules
        for off in [0, module_size // 3, 2 * module_size // 3]:
            edges.append((m * module_size + off, nm * module_size + off)); lengths.append(float(module_size))
    for m in range(modules):  # long bridges across the ring
        jm = (m + 3) % modules
        for off in [module_size // 4, module_size // 2]:
            edges.append((m * module_size + off, jm * module_size + off)); lengths.append(float(3 * module_size))
    e = np.array(edges); L = np.array(lengths, float)
    sv = np.array(sorted(np.unique(L)))
    sid = np.array([np.where(sv == x)[0][0] for x in L])
    return e[:, 0], e[:, 1], sid, L, sv, N


def build_3d_positions(modules=8, module_size=10):
    N = modules * module_size
    xyz = np.zeros((N, 3)); R, r = 5.0, 1.0
    for m in range(modules):
        phi = 2 * np.pi * m / modules
        center = np.array([R * np.cos(phi), R * np.sin(phi), 0.0])
        radial = np.array([np.cos(phi), np.sin(phi), 0.0])
        tangential = np.array([-np.sin(phi), np.cos(phi), 0.0])
        zaxis = np.array([0.0, 0.0, 1.0])
        for u in range(module_size):
            psi = 2 * np.pi * u / module_size
            xyz[m * module_size + u] = center + r * (np.cos(psi) * tangential + np.sin(psi) * zaxis) + 0.15 * radial
    return xyz


def bfs(goal, ii, jj, alive):
    adj = collections.defaultdict(list)
    for a, b, al in zip(ii, jj, alive):
        if al:
            adj[a].append(b); adj[b].append(a)
    dist = {goal: 0}; q = collections.deque([goal])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; q.append(y)
    return dist


# ----------------------------------------------------------------------------
# Run: the engine prunes; the mouse tours one waypoint per module.
# ----------------------------------------------------------------------------
def run(seed=7, step_every=30, modules=8, module_size=10, max_updates=12000):
    rng = np.random.default_rng(seed)
    ii, jj, sid, L, sv, N = build_candidate_graph(modules, module_size)
    pos = build_3d_positions(modules, module_size)
    w0 = 1 / np.sqrt(L); w = w0.copy(); X0 = float(w.sum())
    theta = .010 * rng.normal(size=N); omega = .010 * rng.normal(size=N)
    delays = np.maximum(2, np.round(2 + .33 * L).astype(int)); maxd = int(delays.max()) + 1
    sup = np.zeros((maxd, len(ii)))
    K0, gd, sg, eg, rg = 1.35, .018, .11, .21, .62
    supg, repe, rr, minw = .017, .58, .015, 1e-8

    waypoints = [m * module_size + (m * 3) % module_size for m in range(modules)]
    wp_idx = 1; mouse = waypoints[0]; trail = [mouse]; visited = [waypoints[0]]
    reached_all = stranded = False; stranded_at = None
    frames = []

    for k in range(max_updates):
        u = k / max(1, max_updates - 1); expn = 1 + 12 * (u ** 1.18); ep = np.log(expn)
        act = w > minw
        dm = np.zeros(N); np.add.at(dm, ii[act], w[act]); np.add.at(dm, jj[act], w[act])
        d = theta[jj] - theta[ii]; coup = w * np.sin(d); force = np.zeros(N)
        np.add.at(force, ii, coup); np.add.at(force, jj, -coup)
        omega += .035 * ((K0 / (expn ** 1.05)) * force - gd * omega); theta += .035 * omega
        d = theta[jj] - theta[ii]; phase = 1 - np.cos(d)
        endp = dm[ii] + dm[jj] + EPS; med = np.median(endp[act]) if np.any(act) else EPS
        red = np.clip((med + EPS) / endp, .2, 8.); se = ep * (L / L.max()) ** 1.05
        stress = (sg * phase + eg * se * (1 + rg * np.log1p(red))) * act
        ns = np.zeros(N); nc = np.zeros(N)
        np.add.at(ns, ii[act], stress[act]); np.add.at(ns, jj[act], stress[act])
        np.add.at(nc, ii[act], 1.); np.add.at(nc, jj[act], 1.)
        mean = np.zeros(N); m = nc > 0; mean[m] = ns[m] / nc[m]
        em = .5 * (mean[ii] + mean[jj]); high = np.maximum(stress - em, 0) * act; low = np.maximum(em - stress, 0) * act
        rem = np.minimum(w, rr * w * high / (em + EPS))
        pool = np.zeros(N); np.add.at(pool, ii, .5 * rem); np.add.at(pool, jj, .5 * rem)
        lows = np.zeros(N); np.add.at(lows, ii, low); np.add.at(lows, jj, low)
        add = low * (.5 * pool[ii] / (lows[ii] + EPS) + .5 * pool[jj] / (lows[jj] + EPS))
        rt, at = rem.sum(), add.sum(); add = add * (rt / at) if (at > EPS and rt > EPS) else add * 0
        wre = np.maximum(w - rem + add, 0); a2 = wre > minw; demand = stress * wre * a2
        slot = k % maxd; dl = sup[slot].copy(); sup[slot] = 0
        repair = np.minimum(demand, dl); defect = np.maximum(demand - repair, 0)
        dw = np.minimum(wre, defect); w = np.maximum(wre - dw, 0)
        a3 = w > minw; dm2 = np.zeros(N); dc2 = np.zeros(N)
        np.add.at(dm2, ii[a3], w[a3]); np.add.at(dm2, jj[a3], w[a3]); np.add.at(dc2, ii[a3], 1.); np.add.at(dc2, jj[a3], 1.)
        sh = np.zeros(N); m = dc2 > 0; sh[m] = repe * supg * dm2[m] / dc2[m]; news = (sh[ii] + sh[jj]) * a3
        for dd in np.unique(delays):
            idx = delays == dd; sup[(k + int(dd)) % maxd, idx] += news[idx]

        alive = w > 1e-4
        if k % step_every == 0 and not reached_all and not stranded:
            target = waypoints[wp_idx]; dist = bfs(target, ii, jj, alive)
            if mouse == target:
                visited.append(target); wp_idx += 1
                if wp_idx >= len(waypoints): reached_all = True
            elif target not in dist:
                stranded = True; stranded_at = k
            else:
                nbrs = set(jj[(ii == mouse) & alive]).union(set(ii[(jj == mouse) & alive]))
                bd = dist.get(mouse, 1e9); best = mouse
                for nb in nbrs:
                    if dist.get(nb, 1e9) < bd: bd = dist.get(nb, 1e9); best = nb
                if best != mouse: mouse = best; trail.append(mouse)
        if k % step_every == 0:
            frames.append(dict(k=k, w=w.copy(), alive=alive.copy(), mouse=mouse,
                               reached=reached_all, stranded=stranded, trail=list(trail),
                               target=waypoints[min(wp_idx, len(waypoints) - 1)],
                               nvisited=len(visited), alive_frac=float(alive.mean())))
        if w.sum() / X0 < 1e-5 and float(np.mean(w > 1e-4)) < 1e-4: break
        if stranded and frames[-1]['alive_frac'] < 0.06: break

    return dict(frames=frames, pos=pos, ii=ii, jj=jj, L=L, module_size=module_size,
                waypoints=waypoints, reached=reached_all, stranded=stranded)


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------
def render(R, out="mouse_in_the_maze"):
    pos, ii, jj, L, ms = R['pos'], R['ii'], R['jj'], R['L'], R['module_size']
    frames, wps = R['frames'], R['waypoints']; bridge = L >= ms
    fig = plt.figure(figsize=(11, 8.5)); ax = fig.add_subplot(111, projection='3d')
    xlim = (pos[:, 0].min() - 1, pos[:, 0].max() + 1)
    ylim = (pos[:, 1].min() - 1, pos[:, 1].max() + 1)
    zlim = (pos[:, 2].min() - 1.5, pos[:, 2].max() + 1.5)

    def mouse_glyph(p):
        x, y, z = p
        ax.scatter([x], [y], [z], s=320, c='#9a9a9a', edgecolors='k', linewidths=0.7, depthshade=False, zorder=20)
        ax.scatter([x - 0.28], [y + 0.28], [z + 0.25], s=90, c='#bbb', edgecolors='k', linewidths=0.4, depthshade=False, zorder=21)
        ax.scatter([x + 0.28], [y + 0.28], [z + 0.25], s=90, c='#bbb', edgecolors='k', linewidths=0.4, depthshade=False, zorder=21)
        ax.scatter([x], [y - 0.1], [z + 0.05], s=28, c='#e0208a', edgecolors='none', depthshade=False, zorder=22)

    def draw(fi):
        fr = frames[fi]; ax.cla()
        ax.set_xlim(xlim); ax.set_ylim(ylim); ax.set_zlim(zlim)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([]); ax.view_init(elev=22, azim=35)
        al = fr['alive']
        for idx in np.where(al)[0]:
            a, b = ii[idx], jj[idx]
            col = (0.9, 0.45, 0.1, 0.6) if bridge[idx] else (0.5, 0.5, 0.5, 0.15)
            lw = 1.3 if bridge[idx] else 0.6
            ax.plot([pos[a, 0], pos[b, 0]], [pos[a, 1], pos[b, 1]], [pos[a, 2], pos[b, 2]], color=col, lw=lw, zorder=3 if bridge[idx] else 2)
        nm = np.zeros(len(pos)); np.add.at(nm, ii[al], fr['w'][al]); np.add.at(nm, jj[al], fr['w'][al])
        ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], s=6 + 20 * (nm / (nm.max() + 1e-9)), c='#3a6ea5', alpha=0.45, depthshade=False, zorder=4)
        for wp in wps:
            ax.scatter([pos[wp, 0]], [pos[wp, 1]], [pos[wp, 2]], s=120, marker='o', facecolors='none', edgecolors='#2a9d4a', linewidths=1.5, zorder=8)
        tgt = fr['target']
        ax.scatter([pos[tgt, 0]], [pos[tgt, 1]], [pos[tgt, 2]], s=320, marker='*', c='#f5c518', edgecolors='k', linewidths=0.8, depthshade=False, zorder=9)
        tr = fr['trail']
        if len(tr) > 1:
            tp = pos[tr]; ax.plot(tp[:, 0], tp[:, 1], tp[:, 2], color='#e0208a', lw=1.8, alpha=0.65, zorder=7)
        mouse_glyph(pos[fr['mouse']])
        nb = int(al[bridge].sum())
        if fr['reached']: status = "toured the whole world!"
        elif fr['stranded']: status = "STRANDED — roads closed"
        else: status = f"touring... {fr['nvisited']}/{len(wps)} modules reached"
        ax.set_title(f"mouse in a dying maze   tick {fr['k']}   roads {nb}/{int(bridge.sum())}   "
                     f"alive {100*fr['alive_frac']:.0f}%   {status}", fontsize=11)

    anim = animation.FuncAnimation(fig, draw, frames=len(frames), interval=110)
    if SAVE_GIF:
        anim.save(out + ".gif", writer=animation.PillowWriter(fps=9))
        print("saved", out + ".gif")
    else:
        from matplotlib.animation import FFMpegWriter
        anim.save(out + ".mp4", writer=FFMpegWriter(fps=9, bitrate=2600))
        print("saved", out + ".mp4")
    plt.close(fig)


if __name__ == "__main__":
    R = run(seed=7, step_every=30)
    n = sum(1 for w in R['waypoints'])
    visited = R['frames'][-1]['nvisited']
    print(f"toured {visited}/{n} modules | reached_all={R['reached']} | stranded={R['stranded']}")
    render(R)
