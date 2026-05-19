import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from google.colab import files

class AtriumSimulation:
    def __init__(self, grid_resolution=150, spatial_bound=10.0):
        """
        Initializes the synthetic assay base manifold (g0 = 1).
        """
        self.res = grid_resolution
        self.bound = spatial_bound

        # Base Manifold Coordinates
        x = np.linspace(-self.bound, self.bound, self.res)
        y = np.linspace(-self.bound, self.bound, self.res)
        self.X, self.Y = np.meshgrid(x, y)
        self.R = np.sqrt(self.X**2 + self.Y**2)

        # Frozen system parameters
        self.eta_convert = 0.35  # Frozen conversion efficiency
        self.g0 = np.ones_like(self.X) # Unwarped baseline metric

        # Initialize defect origin nodes (randomized but deterministic for the run)
        np.random.seed(42)
        self.num_defects = 4
        self.defect_nodes = np.random.uniform(-self.bound/2, self.bound/2, (self.num_defects, 2))
        self.defect_phases = np.random.uniform(0, 2*np.pi, self.num_defects)

    def mu_defect(self, t):
        """
        Calculates the dynamic defect measure.
        Defects swirl and pulse, challenging Lyapunov stability.
        """
        defect_field = np.zeros_like(self.X)
        for i in range(self.num_defects):
            cx, cy = self.defect_nodes[i]

            # Add orbital swirl to the defects over time
            angle = t * 0.4 + self.defect_phases[i]
            rx = cx * np.cos(angle) - cy * np.sin(angle)
            ry = cx * np.sin(angle) + cy * np.cos(angle)

            # Localized turbulent nodes
            distance_sq = (self.X - rx)**2 + (self.Y - ry)**2
            pulse = 1.0 + 0.3 * np.sin(2.0 * t + self.defect_phases[i])
            defect_field += pulse * np.exp(-distance_sq / 2.5)

        return defect_field

    def repair_waves(self, t):
        """
        Propagates retained-coherence operator waves attempting to enforce stability.
        """
        # Radial phase correction sweeping from the center
        radial_wave = np.cos(self.R * 1.5 - t * 3.0) * np.exp(-self.R / (self.bound * 0.8))
        # High-frequency interference grid
        grid_wave = np.sin(self.X * 1.2 - t) * np.cos(self.Y * 1.2 - t * 1.5) * 0.5

        return radial_wave + grid_wave

    def conformal_factor(self, t):
        """
        Derives bounded Omega(x,t) from repair attempts and defect density.
        """
        R_field = self.repair_waves(t)
        D_field = self.mu_defect(t)

        # Omega = 1.0 + (efficiency * repair) - (defect impact)
        omega_raw = 1.0 + (self.eta_convert * R_field) - (0.6 * D_field)

        # Enforce bounded response geometry (soft clip to prevent numerical blowup)
        # Analogous to the bounded omega rule in the V745 protocol
        omega_bounded = 0.1 + 2.0 * (1.0 / (1.0 + np.exp(-omega_raw)) - 0.5)

        return omega_bounded

    def effective_metric(self, t):
        """
        The Atrium Metric: g_eff(x,t) = Omega(x,t)^2 * g0
        """
        omega = self.conformal_factor(t)
        return (omega**2) * self.g0

# --- Colab Rendering Pipeline ---

# Using a slightly lower resolution so the video encoding is faster,
# but you can crank this up to 150+ if you want ultra-high fidelity.
sim = AtriumSimulation(grid_resolution=120)

fig = plt.figure(figsize=(10, 8), dpi=100)
fig.patch.set_facecolor('black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# Initial plot styling
t_init = 0.0
Z_init = sim.effective_metric(t_init)

ax.set_zlim(0, 2.5)
ax.set_title("Emergent Topology: $g_{\mathrm{eff}}(x,t) = \Omega(x,t)^2 g_0(x)$", color='w', pad=20)
ax.set_xlabel("x", color='w')
ax.set_ylabel("y", color='w')
ax.set_zlabel("Metric Warp Density", color='w')

def update(frame):
    ax.clear()

    # Re-apply styling because ax.clear() wipes it
    ax.set_facecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(color='w', linestyle=':', linewidth=0.5, alpha=0.3)
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.tick_params(colors='w')
    ax.set_zlim(0, 2.5)
    ax.set_title(f"Emergent Topology: $g_{{\mathrm{{eff}}}}(x,t) = \Omega(x,t)^2 g_0(x)$ | t = {frame/10:.1f}", color='w')

    # Calculate physics for current time step
    t = frame / 10.0
    Z = sim.effective_metric(t)

    # Map the defect locations to the colormap to see where the rules are fighting
    D = sim.mu_defect(t)
    norm = mcolors.Normalize(vmin=-0.5, vmax=1.5)

    # Render warped manifold
    surf = ax.plot_surface(sim.X, sim.Y, Z, facecolors=plt.cm.magma(norm(D)),
                           shade=True, antialiased=True, alpha=0.9)

    # Rotate camera slowly to see the structure from multiple angles
    ax.view_init(elev=35, azim=frame * 1.5)
    return surf,

# Compile the animation (60 frames for a smooth, rotating sequence)
print("Compiling Atrium Metric tensor projection... this will take a moment.")
anim = animation.FuncAnimation(fig, update, frames=60, interval=80, blit=False)

# Prevent static plot from rendering alongside the video output
plt.close(fig)

# Set up the FFmpeg writer to encode the video
print("Encoding Atrium flow to MP4... please hold.")
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='V745_Engine'), bitrate=1800)

# Save the file to the Colab environment
filename = 'atrium_metric_flow.mp4'
anim.save(filename, writer=writer)
print(f"Saved successfully as {filename}. Downloading now...")

# Trigger an automatic download to your local machine
files.download(filename)
