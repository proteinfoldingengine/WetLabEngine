from __future__ import annotations

import random
import numpy as np
import torch

CONTROL_MODES = (
    "baseline",
    "angle_only",
    "dihedral_only",
    "soft_contact_only",
    "static_combo",
    "fixed_gate",
    "v9",
)

# Frozen from the recovered 1VII fixed-gate ablation packet. These are
# historical constants, not values fit or tuned on the prospective P1 run.
FIXED_GATE_SIGMA = 0.1955639719963073
FIXED_GATE_CLOSURE = 0.0393431633710861


def seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def pairwise_dists(X: torch.Tensor) -> torch.Tensor:
    return torch.cdist(X, X)


def bond_vectors(X: torch.Tensor) -> torch.Tensor:
    return X[1:] - X[:-1]


def angles_from_coords(X: torch.Tensor) -> torch.Tensor:
    v1 = X[1:-1] - X[:-2]
    v2 = X[2:] - X[1:-1]
    n1 = v1 / (v1.norm(dim=1, keepdim=True) + 1e-8)
    n2 = v2 / (v2.norm(dim=1, keepdim=True) + 1e-8)
    cosang = (n1 * n2).sum(1).clamp(-1 + 1e-7, 1 - 1e-7)
    return torch.acos(cosang)


def dihedrals_from_coords(X: torch.Tensor) -> torch.Tensor:
    b0 = X[1:-2] - X[:-3]
    b1 = X[2:-1] - X[1:-2]
    b2 = X[3:] - X[2:-1]
    b1n = b1 / (b1.norm(dim=1, keepdim=True) + 1e-8)
    v = b0 - (b0 * b1n).sum(1, keepdim=True) * b1n
    w = b2 - (b2 * b1n).sum(1, keepdim=True) * b1n
    y = (torch.cross(b1n, v, dim=1) * w).sum(1)
    x = (v * w).sum(1)
    return torch.atan2(y, x)


def random_chain(n: int, bond_len: float = 3.8, seed: int = 0) -> torch.Tensor:
    rng = np.random.RandomState(seed)
    pts = [np.zeros(3)]
    prev = np.array([1.0, 0.0, 0.0])
    for _ in range(1, n):
        d = rng.normal(size=3)
        d = d / np.linalg.norm(d)
        prev = 0.4 * prev + 0.6 * d
        prev = prev / np.linalg.norm(prev)
        pts.append(pts[-1] + bond_len * prev)
    return torch.tensor(np.array(pts), dtype=torch.float32)


class FoldContext:
    def __init__(self, target: torch.Tensor, name: str) -> None:
        self.target = target
        self.name = name
        self.N = target.shape[0]
        self.pairs = torch.tensor(
            [(i, j) for i in range(self.N) for j in range(i + 3, self.N)],
            dtype=torch.long,
        )
        self.pi = self.pairs[:, 0]
        self.pj = self.pairs[:, 1]


def baseline_energy(X: torch.Tensor, ctx: FoldContext) -> torch.Tensor:
    D = pairwise_dists(X)
    bond = ((bond_vectors(X).norm(dim=1) - 3.8) ** 2).mean()
    mask = torch.ones_like(D, dtype=torch.bool)
    for k in range(-2, 3):
        if k >= 0:
            idx = torch.arange(ctx.N - k)
            mask[idx, idx + k] = False
            mask[idx + k, idx] = False
    rep = torch.relu(3.5 - D[mask]).pow(2).mean()
    rg = torch.mean(torch.sum((X - X.mean(0)) ** 2, dim=1))
    return 10.0 * bond + 0.5 * rep + 0.02 * rg


def bridge_observables(X: torch.Tensor, ctx: FoldContext) -> dict[str, torch.Tensor]:
    D = pairwise_dists(X)
    b = bond_vectors(X)
    bn = b / (b.norm(dim=1, keepdim=True) + 1e-8)
    dots = (bn[:-1] * bn[1:]).sum(1)
    angles = angles_from_coords(X)
    diheds = dihedrals_from_coords(X)

    angle_var = ((angles - angles.mean()) ** 2).mean() if len(angles) > 1 else torch.tensor(0.0)
    if len(diheds) > 1:
        dd_local = torch.atan2(
            torch.sin(diheds[1:] - diheds[:-1]),
            torch.cos(diheds[1:] - diheds[:-1]),
        )
        dihed_smooth = (dd_local ** 2).mean()
    else:
        dd_local = torch.empty(0)
        dihed_smooth = torch.tensor(0.0)

    dir_pen = (1.0 - dots).mean()
    R_micro = torch.exp(-(0.60 * dir_pen + 0.20 * angle_var + 0.26 * dihed_smooth))

    c_mask = torch.triu(torch.ones_like(D, dtype=torch.bool), diagonal=3)
    soft_contacts = torch.sigmoid((7.4 - D[c_mask]) * 2.2).mean()
    local_density = ((D < 8.0).float().sum(dim=1) - 1.0)
    density_var = ((local_density - local_density.mean()) ** 2).mean() / (local_density.mean() + 1e-6)
    rg = torch.mean(torch.sum((X - X.mean(0)) ** 2, dim=1))
    compactness = torch.exp(-0.12 * rg)
    C_meso = torch.sigmoid(1.8 * (soft_contacts - 0.40) - 0.42 * density_var + 0.8 * compactness)

    pi, pj = ctx.pi, ctx.pj
    pair_d = D[pi, pj]
    c_soft = torch.sigmoid((7.1 - pair_d) * 2.2)
    ti = bn[pi]
    tj = bn[pj - 1]
    opp = (1.0 - (ti * tj).sum(dim=1)) / 2.0
    ai_idx = torch.clamp(pi, 0, len(angles) - 1)
    aj_idx = torch.clamp(pj - 2, 0, len(angles) - 1)
    bend_local = torch.sigmoid(1.6 * (((angles[ai_idx] + angles[aj_idx]) / 2.0) - 0.58))
    seqsep = (pj - pi).float() / float(ctx.N)
    seq_weight = torch.sigmoid(4.5 * (seqsep - 0.28))
    loop_compat = (c_soft * opp * bend_local * seq_weight).mean()

    sigma_bridge = torch.sigmoid(6.0 * ((0.36 * R_micro + 0.24 * C_meso + 0.40 * loop_compat) - 0.45))
    closure_ready = sigma_bridge * (0.32 * R_micro + 0.20 * C_meso + 0.48 * loop_compat)
    false_closure = soft_contacts * (1.0 - sigma_bridge) + 0.35 * soft_contacts * (1.0 - loop_compat)

    density_i = local_density[pi]
    density_j = local_density[pj]
    crowd_soft = torch.sigmoid(0.7 * (((density_i + density_j) / 2.0) - 6.5))
    compat_pair = c_soft * (0.45 * opp + 0.35 * bend_local + 0.20 * seq_weight) * (1.0 - 0.25 * crowd_soft)
    compat_field = compat_pair.mean()

    if len(dd_local) > 0:
        left_idx = torch.clamp(pi - 1, 0, len(dd_local) - 1)
        right_idx = torch.clamp(pj - 2, 0, len(dd_local) - 1)
        local_dihed_consistency = torch.exp(-0.8 * (dd_local[left_idx] ** 2 + dd_local[right_idx] ** 2))
        dihedral_preserve = (compat_pair * local_dihed_consistency).mean()
    else:
        dihedral_preserve = torch.tensor(0.0)

    productive_contact = (c_soft * (opp * seq_weight) * bend_local * (1.0 - 0.20 * crowd_soft)).mean()

    return {
        "compat_field": compat_field,
        "dihedral_preserve": dihedral_preserve,
        "productive_contact": productive_contact,
        "sigma_bridge": sigma_bridge,
        "closure_ready": closure_ready,
        "false_closure": false_closure,
        "dir_pen": dir_pen,
        "angle_var": angle_var,
        "dihed_smooth": dihed_smooth,
        "soft_contacts": soft_contacts,
        "density_var": density_var,
        "rg": rg,
        "loop_compat": loop_compat,
    }


def v9_energy_from_observables(
    obs: dict[str, torch.Tensor],
    gate_sigma: float | torch.Tensor | None = None,
    gate_closure: float | torch.Tensor | None = None,
) -> torch.Tensor:
    s = obs["sigma_bridge"] if gate_sigma is None else torch.as_tensor(gate_sigma, dtype=obs["E0"].dtype)
    c = obs["closure_ready"] if gate_closure is None else torch.as_tensor(gate_closure, dtype=obs["E0"].dtype)
    false_closure = obs["soft_contacts"] * (1.0 - s) + 0.35 * obs["soft_contacts"] * (1.0 - obs["loop_compat"])
    return (
        obs["E0"]
        + s * (0.29 * obs["dir_pen"] + 0.09 * obs["angle_var"] + 0.18 * obs["dihed_smooth"])
        - 0.70 * s * obs["loop_compat"]
        - 2.6 * c * obs["compat_field"]
        - 0.8 * c * obs["dihedral_preserve"]
        - 1.7 * c * obs["productive_contact"]
        - 0.8 * c * obs["soft_contacts"]
        - 0.0065 * c * torch.exp(-0.10 * obs["rg"])
        + 0.78 * false_closure
        + 0.024 * (1.0 - s) * obs["density_var"]
    )


def energy_for_mode(X: torch.Tensor, ctx: FoldContext, mode: str):
    if mode not in CONTROL_MODES:
        raise ValueError(f"Unknown mode: {mode}")
    E0 = baseline_energy(X, ctx)
    obs = bridge_observables(X, ctx)
    obs["E0"] = E0
    if mode == "baseline":
        return E0, obs
    if mode == "angle_only":
        return E0 + 0.09 * obs["angle_var"], obs
    if mode == "dihedral_only":
        return E0 + 0.18 * obs["dihed_smooth"], obs
    if mode == "soft_contact_only":
        return E0 - 0.8 * obs["soft_contacts"], obs
    if mode == "static_combo":
        # Same v9 ingredients and coefficients, but no live sigma/closure
        # compression: both dynamic gates are held fully open.
        return v9_energy_from_observables(obs, gate_sigma=1.0, gate_closure=1.0), obs
    if mode == "fixed_gate":
        # Same v9 ingredients with historically frozen gate values. This
        # preserves information content while removing state-dependent gating.
        return v9_energy_from_observables(
            obs,
            gate_sigma=FIXED_GATE_SIGMA,
            gate_closure=FIXED_GATE_CLOSURE,
        ), obs
    return v9_energy_from_observables(obs), obs
