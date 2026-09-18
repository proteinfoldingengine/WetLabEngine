from __future__ import annotations

import math
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
P6_DIR = ROOT.parent / "P6"
if str(P6_DIR) not in sys.path:
    sys.path.insert(0, str(P6_DIR))

import p6_core as p6  # exact certified P6 core vendored on the P8 branch

torch.set_default_dtype(torch.float64)

TARGET_NAME = "1VII"
SEEDS = tuple(range(42, 50))
MODES = (
    "dynamic_622",
    "compaction_only",
    "force_gate_only",
    "all_lockin_from_start",
)
STEPS = 2000
TORSION_LEARNING_RATE = 0.001
GAMMA_LEARNING_RATE = 0.1

BETTI_THRESHOLD = 8
DAG_LIFETIME = 100
FORCE_LIFETIME = 50
BETTI_HISTORY_MAXLEN = 120

EPS = 1e-6

# Exact coordinate-relevant constants recovered from the Patch-622/623 bundle.
RECOVERED_CONSTANTS = {
    "k_contact_spring_base": 1.5,
    "k_df_funnel": 6000.0,
    "k_gamma_surge": 2.0,
    "k_phi_torque_base": 1.0,
    "k_lj_repulsion_base": 1.25,
    "k_hydro_base": 0.75,
    "k_electrostatic_base": 1.0,
    "k_rama": 0.05,
    "contact_dist": 8.0,
    "DEBYE_LENGTH": 5.0,
    "gamma_base": 1.0,
    "gamma_target": 3.0,
}
HYDROPHOBIC_RESIDUES = frozenset({"A", "V", "I", "L", "M", "F", "W", "Y", "C"})
RESIDUE_CHARGES = {"D": -1.0, "E": -1.0, "K": 1.0, "R": 1.0, "H": 1.0}

Target = p6.Target


@dataclass
class ControllerState:
    phase: str = "Compaction"
    betti_history: deque[int] = field(
        default_factory=lambda: deque(maxlen=BETTI_HISTORY_MAXLEN)
    )
    transition_step: int | None = None
    last_betti_lifetime: int = 0
    contact_active: bool = False


def load_target() -> Target:
    return p6.load_target(TARGET_NAME)


def initial_torsions(n_residues: int, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
    return p6.initial_torsions(n_residues, seed)


def wrap_angle(x: torch.Tensor) -> torch.Tensor:
    return p6.wrap_angle(x)


def reconstruct(
    phi_free: torch.Tensor,
    psi: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    n_residues = int(phi_free.numel()) + 1
    geometry = p6.canonical_geometry(n_residues)
    phi = torch.cat([geometry.phi[:1], phi_free])
    return p6.reconstruct_backbone(geometry, phi, psi)


def covalent_drift(
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
) -> tuple[float, float]:
    geometry = p6.canonical_geometry(int(ca.shape[0]))
    return p6.covalent_drift(geometry, n, ca, c)


def compute_pseudo_dihedrals(
    ca: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    # Exact recovered formula from physics_metrics.py, expressed without SciPy.
    if ca.shape[0] < 4:
        empty = torch.tensor([], device=ca.device, dtype=ca.dtype)
        return empty, empty
    v1 = ca[1:-2] - ca[0:-3]
    v2 = ca[2:-1] - ca[1:-2]
    v3 = ca[3:] - ca[2:-1]
    n1 = torch.cross(v1, v2, dim=1)
    n2 = torch.cross(v2, v3, dim=1)
    cos_angle = (n1 * n2).sum(dim=1) / (
        torch.norm(n1, dim=1) * torch.norm(n2, dim=1) + EPS
    )
    angle_rad = torch.acos(torch.clamp(cos_angle, -1.0 + EPS, 1.0 - EPS))
    sign = torch.sign((n1 * v3).sum(dim=1))
    pseudo = angle_rad * sign
    return pseudo, pseudo


def compute_betti1_count(ca: torch.Tensor) -> int:
    # Semantically identical to the recovered squareform(pdist) implementation:
    # contacts are d < 8 A, diagonal and +/-1 sequence neighbors are excluded.
    n_residues = int(ca.shape[0])
    if n_residues < 3:
        return 0
    with torch.no_grad():
        d = torch.cdist(ca, ca)
        contact_map = d < 8.0
        contact_map.fill_diagonal_(False)
        idx = torch.arange(n_residues - 1, device=ca.device)
        contact_map[idx, idx + 1] = False
        contact_map[idx + 1, idx] = False
        total_contacts = float(contact_map.sum().item()) / 2.0
        return max(0, int(total_contacts - (n_residues - 1)))


def _betti_lifetime(state: ControllerState) -> int:
    # Recovered lifetime semantics count qualifying retained entries; they are
    # not required to be consecutive.
    return sum(1 for value in state.betti_history if value >= BETTI_THRESHOLD)


def update_controller(
    state: ControllerState,
    mode: str,
    betti1_count: int,
    step: int,
) -> tuple[str, bool]:
    if mode not in MODES:
        raise ValueError(mode)

    # Historical runner order: append current Betti value before both DAG and
    # force-gate lifetime queries.
    state.betti_history.append(int(betti1_count))
    lifetime = _betti_lifetime(state)
    state.last_betti_lifetime = lifetime

    if mode == "compaction_only":
        state.phase = "Compaction"
        state.contact_active = False
        return state.phase, state.contact_active

    if mode == "all_lockin_from_start":
        state.phase = "LockIn"
        state.contact_active = True
        return state.phase, state.contact_active

    if mode == "force_gate_only":
        state.phase = "LockIn"
        state.contact_active = (
            betti1_count >= BETTI_THRESHOLD and lifetime >= FORCE_LIFETIME
        )
        return state.phase, state.contact_active

    # dynamic_622: exact two-level recovered logic.
    if state.phase == "Compaction":
        transition = (
            betti1_count >= BETTI_THRESHOLD and lifetime >= DAG_LIFETIME
        )
        if transition:
            state.phase = "LockIn"
            state.transition_step = int(step)

    state.contact_active = (
        state.phase == "LockIn"
        and betti1_count >= BETTI_THRESHOLD
        and lifetime >= FORCE_LIFETIME
    )
    return state.phase, state.contact_active


def residue_charges(sequence: str, *, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
    return torch.tensor(
        [RESIDUE_CHARGES.get(residue, 0.0) for residue in sequence],
        device=device,
        dtype=dtype,
    )


def lennard_jones_repulsion(ca: torch.Tensor) -> torch.Tensor:
    k = RECOVERED_CONSTANTS["k_lj_repulsion_base"]
    dist_matrix = torch.cdist(ca, ca)
    sigma = 3.8
    inv_dist_6 = (sigma / (dist_matrix + EPS)) ** 6
    repulsion = inv_dist_6 ** 2
    mask = torch.triu(torch.ones_like(repulsion), diagonal=1).bool()
    return k * torch.mean(repulsion[mask])


def hydrophobic_collapse(ca: torch.Tensor, sequence: str) -> torch.Tensor:
    k = RECOVERED_CONSTANTS["k_hydro_base"]
    indices = [
        index
        for index, residue in enumerate(sequence)
        if residue in HYDROPHOBIC_RESIDUES
    ]
    if len(indices) < 2:
        return ca.new_tensor(0.0)
    hydrophobic_coords = ca[indices]
    centroid = hydrophobic_coords.mean(dim=0)
    return k * torch.mean(
        torch.sum((hydrophobic_coords - centroid) ** 2, dim=1)
    )


def ramachandran_potential(
    pseudo_phi: torch.Tensor,
    pseudo_psi: torch.Tensor,
) -> torch.Tensor:
    if pseudo_phi.numel() == 0:
        return pseudo_phi.new_tensor(0.0)
    k = RECOVERED_CONSTANTS["k_rama"]
    # The recovered source defaults both centers to zero.
    return k * (
        torch.mean(pseudo_phi ** 2) + torch.mean(pseudo_psi ** 2)
    )


def angular_torque_locking(
    pseudo_phi: torch.Tensor,
    pseudo_psi: torch.Tensor,
) -> torch.Tensor:
    if pseudo_phi.numel() == 0:
        return pseudo_phi.new_tensor(0.0)
    k = RECOVERED_CONSTANTS["k_phi_torque_base"]
    return k * (
        torch.mean(pseudo_phi ** 2) + torch.mean(pseudo_psi ** 2)
    )


def fractal_compaction_funnel(ca: torch.Tensor) -> torch.Tensor:
    k = RECOVERED_CONSTANTS["k_df_funnel"]
    rg = torch.sqrt(
        torch.mean(torch.sum((ca - ca.mean(dim=0)) ** 2, dim=1))
    )
    return k * rg


def screened_electrostatics(ca: torch.Tensor, sequence: str) -> torch.Tensor:
    k = RECOVERED_CONSTANTS["k_electrostatic_base"]
    charges = residue_charges(sequence, device=ca.device, dtype=ca.dtype)
    dist_matrix = torch.cdist(ca, ca)
    charge_matrix = charges.unsqueeze(1) * charges
    debye_length = RECOVERED_CONSTANTS["DEBYE_LENGTH"]
    screening = torch.exp(-dist_matrix / debye_length)
    energy = (charge_matrix * screening) / (dist_matrix + EPS)
    mask = torch.ones_like(energy, dtype=torch.bool)
    mask.fill_diagonal_(False)
    for i in range(ca.shape[0] - 1):
        mask[i, i + 1] = False
        mask[i + 1, i] = False
    return k * torch.sum(energy[mask]) / 2.0


def contact_springs(ca: torch.Tensor) -> torch.Tensor:
    k = RECOVERED_CONSTANTS["k_contact_spring_base"]
    contact_dist = RECOVERED_CONSTANTS["contact_dist"]
    dist_matrix = torch.cdist(ca, ca)
    pairs = (dist_matrix < contact_dist).nonzero(as_tuple=False)
    pairs = pairs[pairs[:, 0] < pairs[:, 1]]
    pairs = pairs[pairs[:, 1] > pairs[:, 0] + 3]
    if pairs.numel() == 0:
        return ca.new_tensor(0.0)
    i, j = pairs[:, 0], pairs[:, 1]
    dist_seeded = dist_matrix[i, j]
    return k * torch.mean(dist_seeded ** 2)


def coordinate_objective(
    sequence: str,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    state: ControllerState,
    mode: str,
    step: int,
) -> tuple[torch.Tensor, dict[str, object]]:
    n, ca, c = reconstruct(phi_free, psi)
    pseudo_phi, pseudo_psi = compute_pseudo_dihedrals(ca)
    betti1_count = compute_betti1_count(ca)
    phase, contact_active = update_controller(
        state=state,
        mode=mode,
        betti1_count=betti1_count,
        step=step,
    )

    components = {
        "lennard_jones_repulsion": lennard_jones_repulsion(ca),
        "hydrophobic_collapse": hydrophobic_collapse(ca, sequence),
        "ramachandran_potential": ramachandran_potential(
            pseudo_phi, pseudo_psi
        ),
        "angular_torque_locking": angular_torque_locking(
            pseudo_phi, pseudo_psi
        ),
        "fractal_compaction_funnel": fractal_compaction_funnel(ca),
    }

    if contact_active:
        components["contact_springs"] = contact_springs(ca)
        components["screened_electrostatics"] = screened_electrostatics(
            ca, sequence
        )
    else:
        components["contact_springs"] = ca.new_tensor(0.0)
        components["screened_electrostatics"] = ca.new_tensor(0.0)

    total = sum(components.values(), ca.new_tensor(0.0))
    diagnostics: dict[str, object] = {
        "phase": phase,
        "betti1_count": betti1_count,
        "betti1_lifetime": state.last_betti_lifetime,
        "contact_springs_active": bool(contact_active),
        "transition_step": state.transition_step,
        "pseudo_phi_rms": (
            float(pseudo_phi.std().detach()) if pseudo_phi.numel() > 1 else 0.0
        ),
        "rg_A": float(
            torch.sqrt(
                torch.mean(torch.sum((ca - ca.mean(dim=0)) ** 2, dim=1))
            ).detach()
        ),
    }
    for name, value in components.items():
        diagnostics[f"{name}_loss"] = float(value.detach())
    diagnostics["total_loss"] = float(total.detach())
    return total, diagnostics
