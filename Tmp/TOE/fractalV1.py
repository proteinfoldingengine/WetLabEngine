import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

# === Parameters tuned to your theorem (3D version) ===
LAMBDA = 0.78
INNOVATION_SCALE = 0.25
MAX_DEPTH = 7
NUM_BRANCHES_PER_SPLIT = 3

class Branch3D:
    def __init__(self, start, direction, length, depth):
        self.start = np.array(start, dtype=float)
        self.dir = np.array(direction, dtype=float)
        self.dir /= np.linalg.norm(self.dir) + 1e-8
        self.length = length
        self.depth = depth
        self.end = self.start + self.dir * self.length
        self.children = []

def grow_branch3d(b):
    if b.depth >= MAX_DEPTH:
        return
    goal_dir = np.array([0., 0., 1.])  # upward growth
    r = goal_dir - b.dir * 0.3
    r /= np.linalg.norm(r) + 1e-8
    for _ in range(NUM_BRANCHES_PER_SPLIT):
        delta = LAMBDA * r
        # 3D orthogonal innovation
        perp = np.random.randn(3)
        perp -= np.dot(perp, b.dir) * b.dir
        perp /= np.linalg.norm(perp) + 1e-8
        delta += INNOVATION_SCALE * perp
        new_dir = delta
        new_dir /= np.linalg.norm(new_dir) + 1e-8
        new_length = b.length * (0.68 + 0.08 * np.random.randn())
        child = Branch3D(b.end, new_dir, new_length, b.depth + 1)
        b.children.append(child)
        grow_branch3d(child)

# Build the tree
np.random.seed(42)
root = Branch3D([0, 0, 0], [0, 0, 1], 10.0, 0)
grow_branch3d(root)

# === 3D Animation that saves GIF ===
fig = plt.figure(figsize=(12, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    ax.clear()
    ax.set_xlim(-22, 22)
    ax.set_ylim(-22, 22)
    ax.set_zlim(0, 38)
    ax.set_facecolor('black')
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z (growth)', color='white')
    
    current_max_d = min(MAX_DEPTH, frame // 3 + 1)
    
    def rec_draw(b):
        if b.depth > current_max_d:
            return
        xs, ys, zs = [b.start[0], b.end[0]], [b.start[1], b.end[1]], [b.start[2], b.end[2]]
        # Glow layers
        for i in range(6):
            a = 0.32 / (i + 1)
            w = 11 / (b.depth + 1) * (1.4 - i * 0.2)
            ax.plot(xs, ys, zs, color=(1.0, 0.5, 0.1), lw=w, alpha=a)
        # Core
        ax.plot(xs, ys, zs, color='orange', lw=3.8 / (b.depth + 1), alpha=0.95)
        for child in b.children:
            rec_draw(child)
    
    rec_draw(root)
    
    # Smooth 3D camera rotation
    ax.view_init(elev=28, azim=frame * 2.5)
    
    ax.set_title(f"Restricted Bridge Theorem + Fractal Corollary (3D)\n"
                 f"r + (λr + ξ) • Frame {frame} • Depth {current_max_d}", 
                 color='white', fontsize=13)
    
ani = FuncAnimation(fig, animate, frames=72, interval=80, repeat=True)

print("Saving gorgeous 3D growing fractal GIF... (15–30 seconds)")
ani.save('restricted_bridge_fractal_3d_growth.gif', writer=PillowWriter(fps=12), dpi=140)
print("✅ Done! Open 'restricted_bridge_fractal_3d_growth.gif' — watch your theorem come alive in full 3D with spinning camera 🚀")
