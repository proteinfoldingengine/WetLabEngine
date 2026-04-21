import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# ====================== PARAMETERS (tweak these!) ======================
LAMBDA = 0.78
XI_SCALE = 0.42
MAX_DEPTH = 7
NUM_CHILDREN = 3
INITIAL_LENGTH = 1.2
LENGTH_SCALE = 0.73
TRUNK_STRAIGHTNESS = 0.85
SEED = 42
# =====================================================================

np.random.seed(SEED)

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-8 else np.array([0., 0., 1.])

def generate_orthogonal_xi(direction):
    direction = normalize(direction)
    rand_vec = np.random.randn(3)
    proj = np.dot(rand_vec, direction) * direction
    xi = rand_vec - proj
    xi = normalize(xi)
    scale = XI_SCALE * np.random.uniform(0.75, 1.25)
    return xi * scale

def grow_tree(start, direction, length, depth, depth_lists):
    if depth > MAX_DEPTH:
        return
    end = start + length * direction
    depth_lists[depth].append((start.copy(), end.copy()))
    r = direction.copy()
    for _ in range(NUM_CHILDREN):
        xi = generate_orthogonal_xi(r)
        new_dir = LAMBDA * r + xi
        if depth < 3:
            new_dir = normalize(new_dir * TRUNK_STRAIGHTNESS + r * (1 - TRUNK_STRAIGHTNESS))
        else:
            new_dir = normalize(new_dir)
        new_length = length * LENGTH_SCALE * np.random.uniform(0.9, 1.1)
        grow_tree(end, new_dir, new_length, depth + 1, depth_lists)

# ====================== GENERATE TREE BY DEPTH ======================
depth_lists = [[] for _ in range(MAX_DEPTH + 1)]
grow_tree(np.zeros(3), np.array([0., 0., 1.]), INITIAL_LENGTH, 0, depth_lists)

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

def animate(frame):
    ax.cla()                     # clear for clean redraw
    ax.set_facecolor('black')
    ax.axis('off')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_zlim(0, 7.5)
    
    # Growth: reveal one depth every ~15 frames
    current_depth = min(frame // 15, MAX_DEPTH)
    
    # Draw every level up to current_depth
    for d in range(current_depth + 1):
        for start, end in depth_lists[d]:
            color = cmap(norm(d))
            linewidth = max(6.0 - d * 0.7, 1.0)
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                    color=color, linewidth=linewidth, alpha=0.92)
    
    # Slow rotation while growing
    ax.view_init(elev=28, azim=frame * 0.8)
    
    # Live title showing the math + current build progress
    title = f'Restricted Bridge Theorem + Fractal Corollary\n'
    title += f'Building step-by-step: δ = λr + ξ   (λ={LAMBDA})\n'
    title += f'Depth {current_depth}/{MAX_DEPTH}   (ξ orthogonal & retained residual)'
    ax.set_title(title, color='white', fontsize=13, pad=30)
    
    return ax,

# Total frames: growth + extra rotation at the end
total_frames = 15 * (MAX_DEPTH + 1) + 90
ani = FuncAnimation(fig, animate, frames=total_frames, interval=40, blit=False, repeat=True)

# ====================== SAVE THE GIF ======================
gif_path = 'fractal_tree_growth_step_by_step.gif'
ani.save(gif_path, writer='pillow', fps=25)
print(f"✅ Growth animation saved: {gif_path} — ready to download and watch!")

plt.close(fig)
