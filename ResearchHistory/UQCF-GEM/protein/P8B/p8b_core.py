from __future__ import annotations

import math
import sys
from collections import deque
from dataclasses import replace
from pathlib import Path

import torch

torch.set_default_dtype(torch.float64)

ROOT = Path(__file__).resolve().parent
P6_DIR = ROOT.parent / "P6"
if str(P6_DIR) not in sys.path:
    sys.path.insert(0, str(P6_DIR))
import p6_core as p6

TARGET_NAMES = ("1VII", "1L2Y", "1UAO")
SEEDS = tuple(range(6))
MODES = (
    "recovered_state_gate",
    "fixed_step99_lockin",
    "static_lockin",
    "compaction_only",
)
STEPS = 2000
LEARNING_RATE = 0.02

BETTI_PROXY_THRESHOLD = 8
DAG_QUALIFYING_COUNT = 100
FORCE_QUALIFYING_COUNT = 50
BETTI_HISTORY_MAXLEN = 120
FIXED_LOCKIN_FIRST_STEP = 99

K_CONTACT = 1.5
K_DF_FUNNEL = 6000.0
K_PHI_TORQUE = 1.0
K_LJ = 1.25
K_HYDRO = 0.75
K_ELECTROSTATIC = 1.0
K_RAMA = 0.05
CONTACT_DIST_A = 8.0
DEBYE_LENGTH_A = 5.0
EPS = 1e-6
LJ_SIGMA_A = 3.8

HYDROPHOBIC_RESIDUES = frozenset("AVILMFWYC")
RESIDUE_CHARGES = {"D": -1.0, "E": -1.0, "K": 1.0, "R": 1.0, "H": 1.0}

COMPACTION_COORDINATE_FORCES = (
    "lennard_jones_repulsion",
    "angular_torque_locking",
    "ramachandran_potential",
    "fractal_compaction_funnel",
    "hydrophobic_collapse",
)
LOCKIN_ADDITIONAL_COORDINATE_FORCES = (
    "screened_electrostatics",
    "contact_springs",
)
ALL_COORDINATE_FORCES = (
    *COMPACTION_COORDINATE_FORCES,
    *LOCKIN_ADDITIONAL_COORDINATE_FORCES,
)


def load_target(name: str):
    return p6.load_target(name)


def initial_torsions(n_residues: int, seed: int):
    return p6.initial_torsions(n_residues, seed)


def initial_torsions_for_mode(target, seed: int, mode: str):
    if mode not in MODES:
        raise ValueError(mode)
    return p6.initial_torsions(len(target.sequence), seed)


def wrap_angle(x: torch.Tensor) -> torch.Tensor:
    return p6.wrap_angle(x)


def reconstruct(target, phi_free: torch.Tensor, psi: torch.Tensor):
    geometry = p6.canonical_geometry(len(target.sequence))
    phi = torch.cat([geometry.phi[:1], phi_free])
    n, ca, c = p6.reconstruct_backbone(geometry, phi, psi)
    return geometry, phi, n, ca, c


def historical_betti1_proxy(coords: torch.Tensor) -> int:
    n_residues = int(coords.shape[0])
    if n_residues < 3:
        return 0
    with torch.no_grad():
        distances = torch.cdist(coords, coords)
        contact = distances < CONTACT_DIST_A
        contact.fill_diagonal_(False)
        if n_residues > 1:
            idx = torch.arange(n_residues - 1, device=coords.device)
            contact[idx, idx + 1] = False
            contact[idx + 1, idx] = False
        total_contacts = int(torch.sum(contact).item() // 2)
        return max(0, int(total_contacts - (n_residues - 1)))


class HistoricalBettiHistory:
    def __init__(self):
        self.values: deque[int] = deque(maxlen=BETTI_HISTORY_MAXLEN)

    def append(self, value: int) -> None:
        self.values.append(int(value))

    def qualifying_count(self, threshold: int = BETTI_PROXY_THRESHOLD) -> int:
        return sum(1 for value in self.values if value >= threshold)


class RecoveredController:
    def __init__(self):
        self.phase = "Compaction"
        self.history = HistoricalBettiHistory()
        self.transition_step: int | None = None

    def observe(self, proxy: int, step: int | None = None) -> dict[str, object]:
        proxy = int(proxy)
        self.history.append(proxy)
        qualifying = self.history.qualifying_count()
        transitioned = False
        if (
            self.phase == "Compaction"
            and proxy >= BETTI_PROXY_THRESHOLD
            and qualifying >= DAG_QUALIFYING_COUNT
        ):
            self.phase = "LockIn"
            self.transition_step = step
            transitioned = True

        lockin_force_active = (
            self.phase == "LockIn"
            and proxy >= BETTI_PROXY_THRESHOLD
            and qualifying >= FORCE_QUALIFYING_COUNT
        )
        return {
            "proxy": proxy,
            "qualifying_count": qualifying,
            "transitioned": transitioned,
            "phase": self.phase,
            "lockin_force_active": lockin_force_active,
        }


def fixed_schedule_phase(step: int) -> str:
    return "LockIn" if int(step) >= FIXED_LOCKIN_FIRST_STEP else "Compaction"


def force_names_for_step(
    mode: str,
    step: int,
    ca: torch.Tensor,
    controller: RecoveredController | None = None,
) -> tuple[tuple[str, ...], dict[str, object]]:
    if mode not in MODES:
        raise ValueError(mode)
    proxy = historical_betti1_proxy(ca)

    if mode == "recovered_state_gate":
        if controller is None:
            raise ValueError("recovered_state_gate requires controller")
        event = controller.observe(proxy, step=step)
        forces = list(COMPACTION_COORDINATE_FORCES)
        if bool(event["lockin_force_active"]):
            forces.extend(LOCKIN_ADDITIONAL_COORDINATE_FORCES)
        return tuple(forces), event

    if mode == "fixed_step99_lockin":
        phase = fixed_schedule_phase(step)
        forces = (
            ALL_COORDINATE_FORCES
            if phase == "LockIn"
            else COMPACTION_COORDINATE_FORCES
        )
    elif mode == "static_lockin":
        phase = "LockIn"
        forces = ALL_COORDINATE_FORCES
    else:
        phase = "Compaction"
        forces = COMPACTION_COORDINATE_FORCES

    return tuple(forces), {
        "proxy": proxy,
        "qualifying_count": None,
        "transitioned": False,
        "phase": phase,
        "lockin_force_active": all(
            name in forces for name in LOCKIN_ADDITIONAL_COORDINATE_FORCES
        ),
    }


def pseudo_dihedrals(coords: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    if coords.shape[0] < 4:
        empty = coords.new_tensor([])
        return empty, empty
    v1 = coords[1:-2] - coords[0:-3]
    v2 = coords[2:-1] - coords[1:-2]
    v3 = coords[3:] - coords[2:-1]
    n1 = torch.cross(v1, v2, dim=1)
    n2 = torch.cross(v2, v3, dim=1)
    cos_angle = (n1 * n2).sum(dim=1) / (
        torch.linalg.norm(n1, dim=1) * torch.linalg.norm(n2, dim=1) + EPS
    )
    angle = torch.acos(torch.clamp(cos_angle, -1.0 + EPS, 1.0 - EPS))
    sign = torch.sign((n1 * v3).sum(dim=1))
    signed = angle * sign
    return signed, signed


def _lj_repulsion(ca: torch.Tensor) -> torch.Tensor:
    distances = torch.cdist(ca, ca)
    inv6 = (LJ_SIGMA_A / (distances + EPS)) ** 6
    repulsion = inv6 ** 2
    mask = torch.triu(torch.ones_like(repulsion, dtype=torch.bool), diagonal=1)
    return K_LJ * torch.mean(repulsion[mask])


def _hydrophobic_collapse(ca: torch.Tensor, sequence: str) -> torch.Tensor:
    indices = [i for i, aa in enumerate(sequence) if aa in HYDROPHOBIC_RESIDUES]
    if len(indices) < 2:
        return ca.new_tensor(0.0)
    subset = ca[torch.tensor(indices, dtype=torch.long, device=ca.device)]
    centroid = subset.mean(dim=0)
    return K_HYDRO * torch.mean(torch.sum((subset - centroid) ** 2, dim=1))


def _historical_rama(ca: torch.Tensor) -> torch.Tensor:
    phi, psi = pseudo_dihedrals(ca)
    if phi.numel() == 0:
        return ca.new_tensor(0.0)
    # The recovered source defaults both centers to 0.0 because no alternate
    # centers are supplied by the frozen constants/config.
    return K_RAMA * (torch.mean(phi ** 2) + torch.mean(psi ** 2))


def _angular_torque(ca: torch.Tensor) -> torch.Tensor:
    phi, psi = pseudo_dihedrals(ca)
    if phi.numel() == 0:
        return ca.new_tensor(0.0)
    return K_PHI_TORQUE * (torch.mean(phi ** 2) + torch.mean(psi ** 2))


def _fractal_compaction(ca: torch.Tensor) -> torch.Tensor:
    rg = torch.sqrt(torch.mean(torch.sum((ca - ca.mean(dim=0)) ** 2, dim=1)))
    return K_DF_FUNNEL * rg


def _charges(sequence: str, device: torch.device) -> torch.Tensor:
    return torch.tensor(
        [RESIDUE_CHARGES.get(aa, 0.0) for aa in sequence],
        dtype=torch.float64,
        device=device,
    )


def _screened_electrostatics(ca: torch.Tensor, sequence: str) -> torch.Tensor:
    charges = _charges(sequence, ca.device)
    distances = torch.cdist(ca, ca)
    charge_matrix = charges[:, None] * charges[None, :]
    screening = torch.exp(-distances / DEBYE_LENGTH_A)
    energy = (charge_matrix * screening) / (distances + EPS)
    mask = torch.ones_like(energy, dtype=torch.bool)
    mask.fill_diagonal_(False)
    if ca.shape[0] > 1:
        idx = torch.arange(ca.shape[0] - 1, device=ca.device)
        mask[idx, idx + 1] = False
        mask[idx + 1, idx] = False
    return K_ELECTROSTATIC * torch.sum(energy[mask]) / 2.0


def _contact_springs(ca: torch.Tensor) -> torch.Tensor:
    distances = torch.cdist(ca, ca)
    pairs = (distances < CONTACT_DIST_A).nonzero(as_tuple=False)
    pairs = pairs[pairs[:, 0] < pairs[:, 1]]
    pairs = pairs[pairs[:, 1] > pairs[:, 0] + 3]
    if pairs.numel() == 0:
        return ca.new_tensor(0.0)
    d = distances[pairs[:, 0], pairs[:, 1]]
    return K_CONTACT * torch.mean(d ** 2)


def coordinate_objective(
    target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    force_names: tuple[str, ...] | list[str],
):
    geometry, phi, n, ca, c = reconstruct(target, phi_free, psi)
    names = set(force_names)
    terms: dict[str, torch.Tensor] = {}

    if "lennard_jones_repulsion" in names:
        terms["lennard_jones_repulsion"] = _lj_repulsion(ca)
    if "angular_torque_locking" in names:
        terms["angular_torque_locking"] = _angular_torque(ca)
    if "ramachandran_potential" in names:
        terms["ramachandran_potential"] = _historical_rama(ca)
    if "fractal_compaction_funnel" in names:
        terms["fractal_compaction_funnel"] = _fractal_compaction(ca)
    if "hydrophobic_collapse" in names:
        terms["hydrophobic_collapse"] = _hydrophobic_collapse(ca, target.sequence)
    if "screened_electrostatics" in names:
        terms["screened_electrostatics"] = _screened_electrostatics(
            ca, target.sequence
        )
    if "contact_springs" in names:
        terms["contact_springs"] = _contact_springs(ca)

    total = (
        torch.stack(list(terms.values())).sum()
        if terms
        else ca.new_tensor(0.0)
    )
    components = {name: float(value.detach()) for name, value in terms.items()}
    components["total"] = float(total.detach())
    return total, (geometry, phi, n, ca, c), components


def native_firewall_selfcheck() -> bool:
    target = load_target("1VII")
    phi0, psi0 = initial_torsions(len(target.sequence), seed=0)

    def value_grad(t):
        pf = phi0.detach().clone().requires_grad_(True)
        ps = psi0.detach().clone().requires_grad_(True)
        energy, _, _ = coordinate_objective(
            t, pf, ps, COMPACTION_COORDINATE_FORCES
        )
        gp, gs = torch.autograd.grad(energy, (pf, ps))
        return float(energy.detach()), gp.detach(), gs.detach()

    e0, gp0, gs0 = value_grad(target)
    changed = replace(target, native_ca=target.native_ca * 7.0 + 123.456)
    e1, gp1, gs1 = value_grad(changed)

    if abs(e0 - e1) > 1e-12:
        return False
    if not torch.allclose(gp0, gp1, rtol=0.0, atol=1e-12):
        return False
    if not torch.allclose(gs0, gs1, rtol=0.0, atol=1e-12):
        return False

    # Controller state is a function only of modeled C-alpha coordinates.
    pf = phi0.detach().clone()
    ps = psi0.detach().clone()
    _, _, _, ca, _ = reconstruct(target, pf, ps)
    proxy0 = historical_betti1_proxy(ca)
    _, _, _, ca_changed, _ = reconstruct(changed, pf, ps)
    proxy1 = historical_betti1_proxy(ca_changed)
    return proxy0 == proxy1


def covalent_drift(target, phi_free: torch.Tensor, psi: torch.Tensor):
    geometry, _, n, ca, c = reconstruct(target, phi_free, psi)
    return p6.covalent_drift(geometry, n, ca, c)


def topk_native_contact_precision(model_ca: torch.Tensor, native_ca: torch.Tensor):
    return p6.topk_native_contact_precision(model_ca, native_ca)


def radius_of_gyration(ca: torch.Tensor) -> float:
    return p6.radius_of_gyration(ca)


def kabsch_rmsd(model_ca: torch.Tensor, native_ca: torch.Tensor) -> float:
    return p6.kabsch_rmsd(model_ca, native_ca)


def exact_sign_flip_p(differences):
    return p6.exact_sign_flip_p(differences)


def holm_three(p_values):
    vals = [float(p) for p in p_values]
    if len(vals) != 3:
        raise ValueError("holm_three requires exactly 3 p-values")
    order = sorted(range(3), key=lambda i: vals[i])
    adjusted = [0.0, 0.0, 0.0]
    running = 0.0
    for rank, idx in enumerate(order):
        multiplier = 3 - rank
        value = min(1.0, multiplier * vals[idx])
        running = max(running, value)
        adjusted[idx] = running
    return tuple(adjusted)
