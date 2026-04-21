import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# ====================== 4 VARIATIONS (tweak here if you want!) ======================
PRESETS = [
    {"name": "Classic",          "LAMBDA": 0.78, "XI_SCALE": 0.42, "XI_VARIANCE": 0.25},
    {"name": "Biological",       "LAMBDA": 0.72, "XI_SCALE": 0.48, "XI_VARIANCE": 0.35},
    {"name": "Clean Canopy",     "LAMBDA": 0.82, "XI_SCALE": 0.35, "XI_VARIANCE": 0.15},
    {"name": "Explosive Chaos",  "LAMBDA": 0.68, "XI_SCALE": 0.55, "XI_VARIANCE": 0.30},
]

MAX_DEPTH = 7
NUM_CHILDREN = 3
INITIAL_LENGTH = 1.2
LENGTH_SCALE = 0.73
TRUNK_STRAIGHTNESS = 0.85
SEED = 42
# ===================================================================================

np.random.seed(SEED)

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-8 else np.array([0., 0., 1.])

def generate_orthogonal_xi(direction, xi_scale, xi_variance):
    direction = normalize(direction)
    rand_vec = np.random.randn(3)
    proj = np.dot(rand_vec, direction) * direction
    xi = rand_vec - proj
    xi = normalize(xi)
    scale = xi_scale * np.random.uniform(1 - xi_variance, 1 + xi_variance)
    return xi * scale

def grow_tree(start, direction, length, depth, depth_lists, lam, xi_scale, xi_var):
    if depth > MAX_DEPTH:
        return
    end = start + length * direction
    depth_lists[depth].append((start.copy(), end.copy()))
    r = direction.copy()
    for _ in range(NUM_CHILDREN):
        xi = generate_orthogonal_xi(r, xi_scale, xi_var)
        new_dir = lam * r + xi
        if depth < 3:
            new_dir = normalize(new_dir * TRUNK_STRAIGHTNESS + r * (1 - TRUNK_STRAIGHTNESS))
        else:
            new_dir = normalize(new_dir)
        new_length = length * LENGTH_SCALE * np.random.uniform(0.9, 1.1)
        grow_tree(end, new_dir, new_length, depth + 1, depth_lists, lam, xi_scale, xi_var)

# ====================== PRE-GENERATE ALL 4 TREES ======================
print("Generating 4 fractal variations...")
depth_lists_per_preset = []
for preset in PRESETS:
    depth_lists = [[] for _ in range(MAX_DEPTH + 1)]
    grow_tree(np.zeros(3), np.array([0., 0., 1.]), INITIAL_LENGTH, 0,
              depth_lists, preset["LAMBDA"], preset["XI_SCALE"], preset["XI_VARIANCE"])
    depth_lists_per_preset.append(depth_lists)
    print(f"   ✓ {preset['name']} complete")
print("All trees ready!\n")

# ====================== ANIMATION SETUP ======================
fig = plt.figure(figsize=(12, 12), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

cmap = plt.cm.plasma
norm = mcolors.Normalize(vmin=0, vmax=MAX_DEPTH)

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_zlim(0, 7.5)

FRAMES_PER_BUILD = 15 * (MAX_DEPTH + 1)   # ~120 frames per example
PAUSE_FRAMES = 30                         # hold on finished tree for a moment

def animate(frame):
    ax.cla()
    ax.set_facecolor('black')
    ax.axis('off')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_zlim(0, 7.5)
    
    # Which preset are we on?
    cycle_length = FRAMES_PER_BUILD + PAUSE_FRAMES
    preset_idx = (frame // cycle_length) % len(PRESETS)
    local_frame = frame % cycle_length
    current_depth = min(local_frame // 15, MAX_DEPTH)
    
    preset = PRESETS[preset_idx]
    depth_lists = depth_lists_per_preset[preset_idx]
    
    # Draw current depth for this preset
    for d in range(current_depth + 1):
        for start, end in depth_lists[d]:
            color = cmap(norm(d))
            linewidth = max(6.0 - d * 0.7, 1.0)
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                    color=color, linewidth=linewidth, alpha=0.92)
    
    # Slow rotation
    ax.view_init(elev=28, azim=frame * 0.8)
    
    # Live title
    title = f'Restricted Bridge Theorem + Fractal Corollary\n'
    title += f'Example {preset_idx+1}/4: {preset["name"]}\n'
    title += f'δ = λr + ξ   (λ={preset["LAMBDA"]}, ξ-scale={preset["XI_SCALE"]}, ξ-var={preset["XI_VARIANCE"]})\n'
    title += f'Depth {current_depth}/{MAX_DEPTH}   (ξ orthogonal & retained residual)'
    ax.set_title(title, color='white', fontsize=13, pad=25)
    
    return ax,

# Total frames: full cycle of all 4 + extra rotation at end before loop
total_frames = len(PRESETS) * (FRAMES_PER_BUILD + PAUSE_FRAMES) + 60

ani = FuncAnimation(fig, animate, frames=total_frames, interval=40, blit=False, repeat=True)

# ====================== SAVE THE GIF ======================
gif_path = 'fractal_tree_4_examples_loop.gif'
ani.save(gif_path, writer='pillow', fps=25)
print(f"\n🎉 SUCCESS! Looping 4-example animation saved as:\n   {gif_path}\n")
print("Open it in any browser — it will automatically cycle through all four variations forever!")

plt.close(fig)
