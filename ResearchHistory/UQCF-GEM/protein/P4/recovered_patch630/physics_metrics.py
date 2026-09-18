# physics_metrics.py
# Patch 630: Full Backbone Angular Physics

import torch
import torch.nn.functional as F
import numpy as np
from scipy.spatial.distance import pdist, squareform
import math

eps = 1e-6

# --- ✅ Patch 630: True Dihedral Angle Calculation ---
def compute_dihedral(p0: torch.Tensor, p1: torch.Tensor, p2: torch.Tensor, p3: torch.Tensor) -> torch.Tensor:
    """
    Computes the dihedral angle between four points in radians using the Praxeolitic formula.
    This implementation is numerically stable and differentiable.
    """
    b0 = -1.0 * (p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2
    
    # Normalize b1 to prevent numerical instability
    b1_norm = torch.norm(b1, dim=-1, keepdim=True)
    b1 = b1 / (b1_norm + eps)

    # Vector rejections: find vectors v and w perpendicular to b1
    v = b0 - torch.sum(b0 * b1, dim=-1, keepdim=True) * b1
    w = b2 - torch.sum(b2 * b1, dim=-1, keepdim=True) * b1

    # Angle between v and w is the dihedral angle
    x = torch.sum(v * w, dim=-1)
    y = torch.sum(torch.cross(b1, v, dim=-1) * w, dim=-1)
    
    return torch.atan2(y, x)

def compute_true_phi_psi(N_coords: torch.Tensor, CA_coords: torch.Tensor, C_coords: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Computes true φ and ψ torsion angles using full backbone atom positions.
    This breaks the degeneracy of the C-alpha-only model.
    """
    if CA_coords.shape[0] < 3:
        return torch.tensor([], device=CA_coords.device), torch.tensor([], device=CA_coords.device)
        
    # Phi (φ) angle: C(i-1) - N(i) - CA(i) - C(i)
    phi = compute_dihedral(C_coords[:-2], N_coords[1:-1], CA_coords[1:-1], C_coords[1:-1])
    
    # Psi (ψ) angle: N(i) - CA(i) - C(i) - N(i+1)
    psi = compute_dihedral(N_coords[1:-1], CA_coords[1:-1], C_coords[1:-1], N_coords[2:])
    
    return phi, psi

# --- (Other metric functions remain the same, but use CA_coords for global properties) ---
def compute_rg(X: torch.Tensor) -> torch.Tensor:
    centroid = X.mean(dim=0)
    return torch.sqrt(torch.mean(((X - centroid)**2).sum(dim=1)) + eps)

def compute_entropy(X: torch.Tensor) -> torch.Tensor:
    if X.shape[0] < 2: return torch.tensor(0.0, device=X.device)
    D = torch.cdist(X, X)
    D_filtered = D[D > eps]
    if D_filtered.numel() == 0: return torch.tensor(0.0, device=X.device)
    P = F.softmax(-D_filtered, dim=0)
    return -(P * (P + eps).log()).sum()

def compute_betti1_count(X: torch.Tensor, N_residues: int) -> int:
    with torch.no_grad():
        if N_residues < 3: return 0
        dist_matrix = torch.pdist(X).cpu().numpy()
        contact_map = squareform(dist_matrix) < 8.0
        np.fill_diagonal(contact_map, 0); np.fill_diagonal(contact_map[1:], 0); np.fill_diagonal(contact_map[:, 1:], 0)
        total_contacts = np.sum(contact_map) / 2
        return max(0, int(total_contacts - (N_residues - 1)))

def compute_rmsd(X1: torch.Tensor, X2: torch.Tensor) -> tuple[float, torch.Tensor]:
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
