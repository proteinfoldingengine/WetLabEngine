import numpy as np
import time
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional

@dataclass
class UQCFGEMConfig:
    Df_base: float = 2.7387
    entropy_scale: float = 0.12
    coherence_scale: float = 3.00
    gamma0: float = 0.2613
    knn_k: int = 12                    # Balanced for 10K cities
    random_seed: int = 42
    w_distance: float = 0.15           # Small distance component for practicality
    w_entropy: float = 0.10
    w_coherence: float = 0.75          # Dominant objective

class UQCFGEMBackboneSolver:
    """
    UQCF-GEM Coherence-First Fractal Backbone Solver (10K-city ready)
    Primary objective: maximize directional coherence under fractal scaling.
    """

    def __init__(self, config: Optional[UQCFGEMConfig] = None):
        self.cfg = config or UQCFGEMConfig()
        self.rng = np.random.default_rng(self.cfg.random_seed)

    def solve(self, coords: np.ndarray) -> Tuple[np.ndarray, float, float]:
        coords = np.asarray(coords, dtype=np.float64)
        n = len(coords)

        knn_idx, knn_dist = self._build_knn(coords, self.cfg.knn_k)
        local_density = self._local_density(knn_dist)
        local_df = self._local_fractal_dimension(local_density)

        start = int(self.rng.integers(0, n))
        tour = [start]
        visited = {start}
        current = start
        prev_dir = None

        while len(visited) < n:
            candidates = [int(j) for j in knn_idx[current] if int(j) not in visited]
            if not candidates:
                candidates = [j for j in range(n) if j not in visited]

            best_j = None
            best_cost = float("inf")
            for j in candidates:
                cost = self._edge_cost(coords, current, j, prev_dir, local_density, local_df)
                if cost < best_cost:
                    best_cost = cost
                    best_j = j

            step_vec = coords[best_j] - coords[current]
            prev_dir = step_vec / (np.linalg.norm(step_vec) + 1e-12)

            tour.append(best_j)
            visited.add(best_j)
            current = best_j

        tour = np.array(tour, dtype=int)
        length = self._tour_length(coords, tour)
        coherence = self._coherence_flow_score(coords, tour)
        return tour, length, coherence

    def run_ensemble(self, coords: np.ndarray, num_starts: int = 20) -> List[Dict]:
        results = []
        for seed in range(num_starts):
            self.cfg.random_seed = seed
            self.rng = np.random.default_rng(seed)
            t0 = time.time()
            tour, length, coh = self.solve(coords)
            dt = time.time() - t0
            results.append({"seed": seed, "length": length, "coherence": coh, "runtime_s": dt, "tour": tour.copy()})
        return results

    @staticmethod
    def summarize_ensemble(results: List[Dict]) -> Dict:
        lengths = np.array([r["length"] for r in results])
        coherences = np.array([r["coherence"] for r in results])
        best_idx = int(np.argmax(coherences))
        return {
            "best_coherence": float(coherences[best_idx]),
            "best_length": float(lengths[best_idx]),
            "mean_coherence": float(coherences.mean()),
            "mean_length": float(lengths.mean()),
            "best_tour": results[best_idx]["tour"],
        }

    # === Helper methods (optimized for large n) ===
    def _build_knn(self, coords: np.ndarray, k: int):
        dmat = np.linalg.norm(coords[:, None] - coords[None, :], axis=2)
        kk = min(k + 1, len(coords))
        idx = np.argsort(dmat, axis=1)[:, 1:kk]
        dist = np.take_along_axis(dmat, idx, axis=1)
        return idx, dist

    def _local_density(self, knn_dist: np.ndarray):
        rho = 1.0 / (np.mean(knn_dist, axis=1) + 1e-12)
        rho /= (rho.max() + 1e-12)
        return rho

    def _local_fractal_dimension(self, rho: np.ndarray):
        df = self.cfg.Df_base + 0.15 * (rho - rho.mean())
        return np.clip(df, 2.0, 3.0)

    def _edge_cost(self, coords, i, j, prev_dir, rho, df):
        d = np.linalg.norm(coords[j] - coords[i])
        entropy_term = 1.0 / ((d + 1e-9) ** max(df[i] / 2.0, 1e-9))

        if prev_dir is None:
            coherence_term = 0.0
        else:
            step = coords[j] - coords[i]
            step = step / (np.linalg.norm(step) + 1e-12)
            alignment = float(np.dot(prev_dir, step))
            coherence_term = self.cfg.coherence_scale * (1.0 - alignment)

        return (self.cfg.w_distance * d +
                self.cfg.w_entropy * self.cfg.entropy_scale * entropy_term +
                self.cfg.w_coherence * coherence_term)

    def _tour_length(self, coords, tour):
        rolled = np.roll(tour, -1)
        return float(np.sum(np.linalg.norm(coords[tour] - coords[rolled], axis=1)))

    def _coherence_flow_score(self, coords, tour):
        pts = coords[tour]
        edges = pts[1:] - pts[:-1]
        norms = np.linalg.norm(edges, axis=1, keepdims=True) + 1e-12
        edges = edges / norms
        if len(edges) < 2:
            return 0.0
        return float(np.mean(np.sum(edges[:-1] * edges[1:], axis=1)))


# =========================
# 10K City Run
# =========================
if __name__ == "__main__":
    print("UQCF-GEM 10,000-city Coherence-First Backbone Solver\n")

    np.random.seed(42)
    n_cities = 10000
    coords = np.random.uniform(0, 100, (n_cities, 3))   # 3D capable

    solver = UQCFGEMBackboneSolver()

    t0 = time.time()
    ensemble = solver.run_ensemble(coords, num_starts=10)   # 10 starts is practical
    summary = solver.summarize_ensemble(ensemble)
    total_time = time.time() - t0

    print(f"10,000 cities completed in {total_time:.1f} seconds")
    print(f"Best coherence flow score : {summary['best_coherence']:.4f}")
    print(f"Best Euclidean length     : {summary['best_length']:.1f}")
    print(f"Mean coherence             : {summary['mean_coherence']:.4f}")
    print(f"Mean length                : {summary['mean_length']:.1f}")
    print("\nThe best backbone is stored in summary['best_tour']")
    print("This demonstrates coherence-first propagation at 10K scale.")
