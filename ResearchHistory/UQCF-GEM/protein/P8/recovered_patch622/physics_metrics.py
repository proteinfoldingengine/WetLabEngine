# physics_metrics.py
# Patch ID: 624.1 (Restored Metric Functions)

import torch
import torch.nn.functional as F
import numpy as np
from scipy.spatial.distance import pdist, squareform
from collections import deque
import math

eps = 1e-6

# --- QIC DAG Coherence Metrics ---

def estimate_betti1_entropy(betti1_delta: float) -> float:
    """Estimates the persistence entropy of Betti-1 loops as a proxy."""
    return 1.0 / (betti1_delta + eps)

def compute_qic_dag_coherence(metrics: dict) -> float:
    """Computes the QIC DAG Coherence score."""
    gamma_bar = metrics.get('gamma_bar', 0.0)
    phi_rms = metrics.get('phi_rms', 9.9)
    d2S_dt2 = metrics.get('d2S_dt2', 0.0)
    betti1_entropy = metrics.get('betti1_entropy', 0.0)
    
    gamma_score = 1 - math.exp(-0.5 * (gamma_bar - 1))
    phi_score = math.exp(-1.5 * max(0, phi_rms - 0.5))
    entropy_funnel_score = 1 if d2S_dt2 < 0 else 0.5
    betti_entropy_score = 1 - math.exp(-0.1 * betti1_entropy)
    
    weights = {'gamma': 0.4, 'phi': 0.3, 'entropy': 0.15, 'betti': 0.15}
    
    qic_score = (weights['gamma'] * gamma_score +
                 weights['phi'] * phi_score +
                 weights['entropy'] * entropy_funnel_score +
                 weights['betti'] * betti_entropy_score)
    
    return qic_score

# --- Core Physical Observables ---

def compute_rg(X: torch.Tensor) -> torch.Tensor:
    """Computes the Radius of Gyration."""
    centroid = X.mean(dim=0)
    return torch.sqrt(torch.mean(((X - centroid)**2).sum(dim=1)) + eps)

def compute_entropy(X: torch.Tensor) -> torch.Tensor:
    """Computes a conformational entropy proxy based on pairwise distances."""
    if X.shape[0] < 2: return torch.tensor(0.0, device=X.device)
    D = torch.cdist(X, X)
    D_filtered = D[D > eps]
    if D_filtered.numel() == 0: return torch.tensor(0.0, device=X.device)
    P = F.softmax(-D_filtered, dim=0)
    return -(P * (P + eps).log()).sum()

def compute_pseudo_dihedrals(X: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Computes pseudo-dihedral angles (phi and psi) from C-alpha coordinates."""
    if X.shape[0] < 4:
        return torch.tensor([], device=X.device), torch.tensor([], device=X.device)
    v1, v2, v3 = X[1:-2] - X[0:-3], X[2:-1] - X[1:-2], X[3:] - X[2:-1]
    n1, n2 = torch.cross(v1, v2, dim=1), torch.cross(v2, v3, dim=1)
    cos_angle = (n1 * n2).sum(dim=1) / (torch.norm(n1, dim=1) * torch.norm(n2, dim=1) + eps)
    angle_rad = torch.acos(torch.clamp(cos_angle, -1.0 + eps, 1.0 - eps))
    sign = torch.sign((n1 * v3).sum(dim=1))
    # For C-alpha only models, phi and psi are degenerate
    return angle_rad * sign, angle_rad * sign

def compute_betti1_count(X: torch.Tensor, N_residues: int) -> int:
    """Computes a proxy for the first Betti number (B1), representing the number of loops."""
    with torch.no_grad():
        if N_residues < 3: return 0
        dist_matrix = torch.pdist(X).cpu().numpy()
        contact_map = squareform(dist_matrix) < 8.0
        np.fill_diagonal(contact_map, 0); np.fill_diagonal(contact_map[1:], 0); np.fill_diagonal(contact_map[:, 1:], 0)
        total_contacts = np.sum(contact_map) / 2
        return max(0, int(total_contacts - (N_residues - 1)))

def compute_rmsd(X1: torch.Tensor, X2: torch.Tensor) -> tuple[float, torch.Tensor]:
    """Computes RMSD after Kabsch alignment."""
    with torch.no_grad():
        X1_c, X2_c = X1 - X1.mean(dim=0), X2 - X2.mean(dim=0)
        H = X1_c.T @ X2_c
        U, _, Vt = torch.linalg.svd(H)
        d = torch.sign(torch.det(Vt.T @ U.T))
        diag = torch.eye(3, device=X1.device); diag[-1, -1] = d
        R = Vt.T @ diag @ U.T
        X1_aligned = X1_c @ R
        rmsd_val = torch.sqrt(torch.mean(torch.sum((X1_aligned - X2_c)**2, dim=1))).item()
        return rmsd_val, X1_aligned

def compute_contact_map(X: torch.Tensor, threshold: float) -> torch.Tensor:
    """Generates a binary contact map."""
    contact_map = torch.cdist(X, X) < threshold
    contact_map.fill_diagonal_(0)
    return contact_map.int()
    
def compute_phi_entropy(phi_tensor: torch.Tensor) -> float:
    """Computes the entropy of the phi angle distribution."""
    if phi_tensor.numel() < 2: return 0.0
    hist = torch.histc(phi_tensor, bins=20, min=-math.pi, max=math.pi)
    probs = hist / hist.sum()
    return -torch.sum(probs * torch.log(probs + eps)).item()

def compute_torsion_coherence_score(phi_tensor: torch.Tensor) -> float:
    """Computes a score based on the negative standard deviation of torsion angles."""
    if phi_tensor.numel() < 2: return 0.0
    return -phi_tensor.std().item()

def compute_curvature(coords: torch.Tensor) -> torch.Tensor:
    """Computes the discrete curvature along the backbone."""
    if coords.shape[0] < 3: return torch.tensor([], device=coords.device)
    v1 = coords[1:-1] - coords[:-2]
    v2 = coords[2:] - coords[1:-1]
    v1_norm = F.normalize(v1, p=2, dim=1)
    v2_norm = F.normalize(v2, p=2, dim=1)
    # Cosine of the angle between vectors is their dot product
    cos_theta = torch.sum(v1_norm * v2_norm, dim=1)
    # Clamp to avoid numerical errors with acos
    return torch.acos(torch.clamp(cos_theta, -1.0 + eps, 1.0 - eps))

# --- ✅ RESTORED METRIC FUNCTIONS ---
def compute_min_inter_residue_distance(X: torch.Tensor) -> float:
    """Computes the minimum distance between any two non-adjacent residues."""
    with torch.no_grad():
        if X.shape[0] < 3: return 0.0
        dist_matrix = torch.cdist(X, X)
        mask = torch.ones_like(dist_matrix, dtype=torch.bool)
        mask.fill_diagonal_(False); mask.diagonal(offset=1).fill_(False); mask.diagonal(offset=-1).fill_(False)
        return torch.min(dist_matrix[mask]).item() if mask.any() else 0.0

def compute_contact_percentage(X: torch.Tensor, threshold: float) -> float:
    """Calculates the percentage of non-local residues within a given contact threshold."""
    with torch.no_grad():
        n = X.shape[0]
        if n < 3: return 0.0
        dist_matrix = torch.cdist(X, X)
        mask = torch.ones_like(dist_matrix, dtype=torch.bool)
        mask.fill_diagonal_(False); mask.diagonal(offset=1).fill_(False); mask.diagonal(offset=-1).fill_(False)
        contact_count = torch.sum(dist_matrix[mask] < threshold).item()
        total_possible_pairs = (n * (n - 1) / 2) - (n - 1)
        return (contact_count / total_possible_pairs) * 100.0 if total_possible_pairs > 0 else 0.0

def compute_betti1_lifetime_heuristic(betti_history: deque, lifetime_threshold: int) -> int:
    """Calculates a heuristic for Betti1 lifetime."""
    if not list(betti_history): return 0
    window_size = min(len(betti_history), lifetime_threshold)
    window = list(betti_history)[-window_size:]
    return sum(1 for count in window if count > 0)
