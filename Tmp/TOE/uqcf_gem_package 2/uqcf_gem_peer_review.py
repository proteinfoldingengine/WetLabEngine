import numpy as np
import time
from dataclasses import dataclass
from typing import Tuple, Optional, List, Dict

@dataclass
class UQCFGEMConfig:
    Df_base: float = 2.7387
    entropy_scale: float = 0.12
    coherence_scale: float = 3.00
    gamma0: float = 0.2613
    knn_k: int = 8
    random_seed: int = 42
    w_distance: float = 0.0
    w_entropy: float = 0.10
    w_coherence: float = 0.90

class UQCFGEMBackboneSolver:

    def __init__(self, config: Optional[UQCFGEMConfig] = None):
        self.cfg = config or UQCFGEMConfig()
        self.rng = np.random.default_rng(self.cfg.random_seed)

    def solve(self, coords: np.ndarray) -> Tuple[np.ndarray, float, float]:
        coords = np.asarray(coords, dtype=np.float64)
        n = len(coords)

        knn_idx, knn_dist = self._build_knn(coords, self.cfg.knn_k)
        rho = self._local_density(knn_dist)
        df = self._local_fractal_dimension(rho)

        start = int(self.rng.integers(0, n))
        tour = [start]
        visited = {start}
        current = start
        prev_dir = None

        while len(visited) < n:
            candidates = [j for j in knn_idx[current] if j not in visited]
            if not candidates:
                candidates = [j for j in range(n) if j not in visited]

            best_j = min(candidates, key=lambda j: self._edge_cost(coords, current, j, prev_dir, rho, df))

            step = coords[best_j] - coords[current]
            prev_dir = step / (np.linalg.norm(step) + 1e-12)

            tour.append(best_j)
            visited.add(best_j)
            current = best_j

        tour = np.array(tour)
        length = self._tour_length(coords, tour)
        coh = self._coherence(coords, tour)

        return tour, length, coh

    def run_ensemble(self, coords, num_starts=20):
        results = []
        for seed in range(num_starts):
            self.rng = np.random.default_rng(seed)
            t0 = time.time()
            _, length, coh = self.solve(coords)
            results.append((length, coh, time.time() - t0))
        return results

    def _build_knn(self, coords, k):
        d = np.linalg.norm(coords[:,None]-coords[None,:], axis=2)
        idx = np.argsort(d, axis=1)[:,1:k+1]
        dist = np.take_along_axis(d, idx, axis=1)
        return idx, dist

    def _local_density(self, d):
        rho = 1.0/(np.mean(d,axis=1)+1e-12)
        return rho/np.max(rho)

    def _local_fractal_dimension(self, rho):
        df = self.cfg.Df_base + 0.15*(rho-np.mean(rho))
        return np.clip(df,2.0,3.0)

    def _edge_cost(self, coords,i,j,prev_dir,rho,df):
        d = np.linalg.norm(coords[j]-coords[i])
        entropy = 1/((d+1e-9)**(df[i]/2))

        if prev_dir is None:
            coh = 0
        else:
            step = coords[j]-coords[i]
            step /= np.linalg.norm(step)+1e-12
            coh = self.cfg.coherence_scale*(1-np.dot(prev_dir,step))

        return self.cfg.w_entropy*entropy + self.cfg.w_coherence*coh

    def _tour_length(self, coords, tour):
        return float(np.sum(np.linalg.norm(coords[tour]-coords[np.roll(tour,-1)],axis=1)))

    def _coherence(self, coords, tour):
        pts = coords[tour]
        edges = pts[1:]-pts[:-1]
        edges /= np.linalg.norm(edges,axis=1,keepdims=True)+1e-12
        return float(np.mean(np.sum(edges[:-1]*edges[1:],axis=1)))

if __name__ == "__main__":
    np.random.seed(42)
    solver = UQCFGEMBackboneSolver()

    for n in [50,200]:
        coords = np.random.uniform(0,100,(n,3))
        res = solver.run_ensemble(coords,20)
        best = max(res, key=lambda x: x[1])
        print(f"n={n} best coherence={best[1]:.4f}, length={best[0]:.1f}")
