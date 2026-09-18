from __future__ import annotations

import itertools
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT / "vendor"
if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

import backbone_kinematics as bk  # noqa: E402
from residue_identity import ResidueId  # noqa: E402

torch.set_default_dtype(torch.float64)

MODES = (
    "baseline",
    "rama",
    "variance",
    "entropy",
    "rama_entropy",
    "entropy_historical_0p02",
)
PRIMARY_MODES = MODES[:5]
SEEDS = tuple(range(8))
STEPS = 120
LEARNING_RATE = 0.03
GRADIENT_MATCH_RATIO = 0.5
HISTORICAL_ENTROPY_K = 0.02
HISTORICAL_TPO_MIN_VAL = -3.14159
HISTORICAL_TPO_MAX_VAL = 3.14159
HISTORICAL_TPO_EPS = 1e-8

CONTACT_K = 0.05
CONTACT_CUTOFF_A = 8.0
CONTACT_MIN_SEQ_SEPARATION = 3
STERIC_K = 2.0
STERIC_CUTOFF_A = 3.6

PH = 7.0
IONIC_STRENGTH_M = 0.15
ELECTROSTATIC_SCALE = 1.0
COULOMB_KCAL_A_PER_MOL_E2 = 332.06371
WATER_RELATIVE_DIELECTRIC = 80.0
HISTIDINE_PKA = 6.0
DEBYE_NUMERATOR_A_SQRT_M = 3.04

TARGETS = {
    "1VII": {"path": ROOT / "inputs" / "1VII.pdb", "chain": "A", "expected_n": 36},
    "1CRN": {"path": ROOT / "inputs" / "1CRN.pdb", "chain": "A", "expected_n": 46},
}

AA3_TO_1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}


@dataclass(frozen=True)
class Target:
    name: str
    sequence: str
    residue_ids: tuple[ResidueId, ...]
    native_n: torch.Tensor
    native_ca: torch.Tensor
    native_c: torch.Tensor
    geometry: bk.ChainBackboneGeometry
    native_contacts: tuple[tuple[int, int], ...]


def _first_model_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    has_model = any(line.startswith("MODEL") for line in lines)
    if not has_model:
        return lines
    out: list[str] = []
    active = False
    for line in lines:
        if line.startswith("MODEL"):
            if active:
                break
            active = True
            continue
        if active and line.startswith("ENDMDL"):
            break
        if active:
            out.append(line)
    return out


def load_target(name: str) -> Target:
    cfg = TARGETS[name]
    chain = cfg["chain"]
    rows: dict[tuple[str, int, str], dict[str, object]] = {}
    order: list[tuple[str, int, str]] = []
    for line in _first_model_lines(Path(cfg["path"])):
        if not line.startswith("ATOM"):
            continue
        if len(line) < 54 or line[21:22] != chain:
            continue
        altloc = line[16:17]
        if altloc not in (" ", "A"):
            continue
        atom = line[12:16].strip()
        if atom not in ("N", "CA", "C"):
            continue
        resname = line[17:20].strip().upper()
        if resname not in AA3_TO_1:
            continue
        key = (chain, int(line[22:26]), line[26:27].strip())
        if key not in rows:
            rows[key] = {"resname": resname}
            order.append(key)
        row = rows[key]
        if row["resname"] != resname:
            raise ValueError(f"inconsistent residue identity for {key}")
        row.setdefault(
            atom,
            (
                float(line[30:38]),
                float(line[38:46]),
                float(line[46:54]),
            ),
        )

    complete = [key for key in order if all(atom in rows[key] for atom in ("N", "CA", "C"))]
    if len(complete) != int(cfg["expected_n"]):
        raise ValueError(f"{name}: expected {cfg['expected_n']} complete residues, got {len(complete)}")

    residue_ids = tuple(ResidueId(*key) for key in complete)
    sequence = "".join(AA3_TO_1[str(rows[key]["resname"])] for key in complete)
    n = torch.tensor([rows[key]["N"] for key in complete], dtype=torch.float64)
    ca = torch.tensor([rows[key]["CA"] for key in complete], dtype=torch.float64)
    c = torch.tensor([rows[key]["C"] for key in complete], dtype=torch.float64)
    geometries = bk.extract_chain_backbone_geometry(n, ca, c, list(residue_ids))
    if len(geometries) != 1:
        raise ValueError(f"{name}: expected one chain segment, got {len(geometries)}")
    contacts = native_contact_pairs(ca)
    return Target(name, sequence, residue_ids, n, ca, c, geometries[0], contacts)


def wrap_angle(x: torch.Tensor) -> torch.Tensor:
    return torch.atan2(torch.sin(x), torch.cos(x))


def common_torsions(phi: torch.Tensor, psi: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    if phi.numel() < 3 or psi.numel() < 2:
        raise ValueError("at least three residues are required")
    return phi[1:-1], psi[1:]


def ramachandran_energy(phi: torch.Tensor, psi: torch.Tensor) -> torch.Tensor:
    p, q = common_torsions(phi, psi)
    angles = torch.stack([p, q], dim=1)
    centers = angles.new_tensor([
        [-math.pi / 3.0, -math.pi / 4.0],
        [-3.0 * math.pi / 4.0, 3.0 * math.pi / 4.0],
    ])
    delta = wrap_angle(angles[:, None, :] - centers[None, :, :])
    d2 = (delta * delta).sum(dim=-1)
    return d2.min(dim=1).values.mean()


def _soft_histogram_2d(
    phi: torch.Tensor,
    psi: torch.Tensor,
    *,
    bins: int = 18,
    min_val: float = HISTORICAL_TPO_MIN_VAL,
    max_val: float = HISTORICAL_TPO_MAX_VAL,
) -> torch.Tensor:
    width = (max_val - min_val) / bins
    centers = torch.linspace(
        min_val + width / 2.0,
        max_val - width / 2.0,
        bins,
        dtype=phi.dtype,
        device=phi.device,
    )
    phi_r = phi.unsqueeze(1).unsqueeze(2)
    psi_r = psi.unsqueeze(1).unsqueeze(2)
    c_phi = centers.unsqueeze(0).unsqueeze(2)
    c_psi = centers.unsqueeze(0).unsqueeze(1)
    w_phi = torch.relu(width - torch.abs(phi_r - c_phi))
    w_psi = torch.relu(width - torch.abs(psi_r - c_psi))
    return (w_phi * w_psi).sum(dim=0) / (width * width)


def tpo_entropy_energy(phi: torch.Tensor, psi: torch.Tensor) -> torch.Tensor:
    p, q = common_torsions(phi, psi)
    hist = _soft_histogram_2d(p, q)
    probs = hist / (hist.sum() + HISTORICAL_TPO_EPS)
    positive = probs[probs > 0]
    return -(positive * torch.log(positive)).sum()


def circular_variance_energy(phi: torch.Tensor, psi: torch.Tensor) -> torch.Tensor:
    p, q = common_torsions(phi, psi)
    def cv(x: torch.Tensor) -> torch.Tensor:
        c = torch.cos(x).mean()
        s = torch.sin(x).mean()
        return 1.0 - torch.sqrt(c * c + s * s + 1e-12)
    return cv(p) + cv(q)


def _charge_table() -> dict[str, float]:
    h = 1.0 / (1.0 + 10.0 ** (PH - HISTIDINE_PKA))
    table = {aa: 0.0 for aa in "CSTNQYWFMAGPLIV"}
    table.update({"D": -1.0, "E": -1.0, "K": 1.0, "R": 1.0, "H": h})
    return table


def charges_for_sequence(sequence: str, *, device: torch.device) -> torch.Tensor:
    table = _charge_table()
    try:
        vals = [table[aa] for aa in sequence]
    except KeyError as exc:
        raise ValueError(f"unsupported residue {exc.args[0]!r}") from exc
    return torch.tensor(vals, dtype=torch.float64, device=device)


def base_energy(ca: torch.Tensor, sequence: str) -> tuple[torch.Tensor, dict[str, float]]:
    n = ca.shape[0]
    dist = torch.cdist(ca, ca)
    idx = torch.arange(n, device=ca.device)
    sep = torch.abs(idx[:, None] - idx[None, :])
    upper = torch.triu(torch.ones((n, n), dtype=torch.bool, device=ca.device), diagonal=1)

    steric_mask = upper & (sep >= 2)
    steric_r = dist[steric_mask]
    steric = STERIC_K * torch.mean(torch.relu(STERIC_CUTOFF_A - steric_r) ** 2)

    contact_mask = upper & (sep >= CONTACT_MIN_SEQ_SEPARATION) & (dist < CONTACT_CUTOFF_A)
    contact_r = dist[contact_mask]
    if contact_r.numel():
        contacts = 0.5 * CONTACT_K * torch.sum(contact_r * contact_r)
    else:
        contacts = ca.new_tensor(0.0)

    q = charges_for_sequence(sequence, device=ca.device)
    charged = torch.nonzero(q != 0.0, as_tuple=False).flatten()
    electro = ca.new_tensor(0.0)
    electro_pairs = 0
    if charged.numel() >= 2:
        lam = DEBYE_NUMERATOR_A_SQRT_M / math.sqrt(IONIC_STRENGTH_M)
        pref = ELECTROSTATIC_SCALE * COULOMB_KCAL_A_PER_MOL_E2 / WATER_RELATIVE_DIELECTRIC
        terms = []
        for ai in range(charged.numel()):
            i = int(charged[ai])
            for aj in range(ai + 1, charged.numel()):
                j = int(charged[aj])
                r = torch.clamp(dist[i, j], min=1e-6)
                terms.append(pref * q[i] * q[j] * torch.exp(-r / lam) / r)
                electro_pairs += 1
        electro = torch.stack(terms).sum()

    total = steric + contacts + electro
    return total, {
        "steric": float(steric.detach()),
        "contacts": float(contacts.detach()),
        "electrostatics": float(electro.detach()),
        "contact_count": int(contact_r.numel()),
        "electrostatic_pair_count": int(electro_pairs),
    }


def _gradient_norm(energy: torch.Tensor, params: Iterable[torch.Tensor], *, retain_graph: bool = True) -> float:
    grads = torch.autograd.grad(energy, tuple(params), retain_graph=retain_graph, allow_unused=False)
    value = torch.sqrt(sum((g * g).sum() for g in grads))
    return float(value.detach())


def regularizer_scales(
    target: Target,
    phi_free_init: torch.Tensor,
    psi_init: torch.Tensor,
) -> dict[str, float]:
    pf = phi_free_init.detach().clone().requires_grad_(True)
    ps = psi_init.detach().clone().requires_grad_(True)
    phi = torch.cat([target.geometry.phi[:1], pf])
    _, ca, _ = bk.reconstruct_chain_backbone(target.geometry, phi, ps)
    base, _ = base_energy(ca, target.sequence)
    rama = ramachandran_energy(phi, ps)
    variance = circular_variance_energy(phi, ps)
    entropy = tpo_entropy_energy(phi, ps)

    gb = _gradient_norm(base, (pf, ps), retain_graph=True)
    target_norm = 0.5 * gb if gb >= 1e-8 else 1.0

    def scale(raw: torch.Tensor) -> float:
        g = _gradient_norm(raw, (pf, ps), retain_graph=True)
        if not math.isfinite(g) or g < 1e-12:
            raise FloatingPointError(f"regularizer initial gradient is invalid: {g}")
        return target_norm / g

    sr = scale(rama)
    sv = scale(variance)
    se = scale(entropy)
    combo = 0.5 * sr * rama + 0.5 * se * entropy
    gc = _gradient_norm(combo, (pf, ps), retain_graph=False)
    if not math.isfinite(gc) or gc < 1e-12:
        raise FloatingPointError(f"combined regularizer gradient is invalid: {gc}")
    sc = target_norm / gc
    return {
        "base_gradient_norm": gb,
        "target_regularizer_gradient_norm": target_norm,
        "rama_scale": sr,
        "variance_scale": sv,
        "entropy_scale": se,
        "combo_outer_scale": sc,
    }


def objective(
    target: Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    mode: str,
    scales: dict[str, float],
) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor, torch.Tensor], dict[str, float]]:
    phi = torch.cat([target.geometry.phi[:1], phi_free])
    n, ca, c = bk.reconstruct_chain_backbone(target.geometry, phi, psi)
    base, components = base_energy(ca, target.sequence)
    rama = ramachandran_energy(phi, psi)
    variance = circular_variance_energy(phi, psi)
    entropy = tpo_entropy_energy(phi, psi)

    added = phi.new_tensor(0.0)
    if mode == "rama":
        added = scales["rama_scale"] * rama
    elif mode == "variance":
        added = scales["variance_scale"] * variance
    elif mode == "entropy":
        added = scales["entropy_scale"] * entropy
    elif mode == "rama_entropy":
        inner = 0.5 * scales["rama_scale"] * rama + 0.5 * scales["entropy_scale"] * entropy
        added = scales["combo_outer_scale"] * inner
    elif mode == "entropy_historical_0p02":
        added = HISTORICAL_ENTROPY_K * entropy
    elif mode != "baseline":
        raise ValueError(f"unknown mode {mode!r}")

    total = base + added
    components.update(
        {
            "rama_raw": float(rama.detach()),
            "variance_raw": float(variance.detach()),
            "entropy_raw": float(entropy.detach()),
            "regularizer_added": float(added.detach()),
            "total": float(total.detach()),
        }
    )
    return total, (n, ca, c), components


def kabsch_rmsd(x: torch.Tensor, y: torch.Tensor) -> float:
    x = x.detach().to(dtype=torch.float64)
    y = y.detach().to(dtype=torch.float64)
    xc = x - x.mean(dim=0)
    yc = y - y.mean(dim=0)
    h = xc.T @ yc
    u, _, vh = torch.linalg.svd(h)
    d = torch.sign(torch.det(u @ vh))
    if float(d) == 0.0:
        d = x.new_tensor(1.0)
    diag = torch.eye(3, dtype=x.dtype, device=x.device)
    diag[-1, -1] = d
    r = u @ diag @ vh
    aligned = xc @ r
    return float(torch.sqrt(torch.mean(torch.sum((aligned - yc) ** 2, dim=1))))


def native_contact_pairs(ca: torch.Tensor) -> tuple[tuple[int, int], ...]:
    n = ca.shape[0]
    d = torch.cdist(ca, ca)
    pairs = []
    for i in range(n):
        for j in range(i + CONTACT_MIN_SEQ_SEPARATION, n):
            if float(d[i, j]) < CONTACT_CUTOFF_A:
                pairs.append((i, j))
    return tuple(pairs)


def contact_recovery(ca: torch.Tensor, pairs: tuple[tuple[int, int], ...]) -> float:
    if not pairs:
        return float("nan")
    d = torch.cdist(ca, ca)
    return sum(float(d[i, j]) < CONTACT_CUTOFF_A for i, j in pairs) / len(pairs)


def native_torsion_rmse(target: Target, phi: torch.Tensor, psi: torch.Tensor) -> float:
    pn, qn = common_torsions(target.geometry.phi, target.geometry.psi)
    p, q = common_torsions(phi, psi)
    dp = wrap_angle(p - pn)
    dq = wrap_angle(q - qn)
    return float(torch.sqrt(torch.mean(torch.cat([dp * dp, dq * dq]))))


def radius_of_gyration(ca: torch.Tensor) -> float:
    center = ca.mean(dim=0)
    return float(torch.sqrt(torch.mean(torch.sum((ca - center) ** 2, dim=1))))


def covalent_drift(
    target: Target,
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
) -> tuple[float, float]:
    rid = list(target.residue_ids)
    g = bk.extract_chain_backbone_geometry(n, ca, c, rid)[0]
    ref = target.geometry
    length_fields = ("n_ca_lengths", "ca_c_lengths", "c_n_lengths")
    angle_fields = ("n_ca_c_angles", "ca_c_n_angles", "c_n_ca_angles")
    max_len = max(float(torch.max(torch.abs(getattr(g, f) - getattr(ref, f)))) for f in length_fields)
    max_ang = max(float(torch.max(torch.abs(getattr(g, f) - getattr(ref, f)))) for f in angle_fields)
    return max_len, max_ang


def initial_torsions(target: Target, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
    gen = torch.Generator(device="cpu")
    target_offset = 100_003 if target.name == "1CRN" else 0
    gen.manual_seed(2_026_091_700 + target_offset + 10_007 * int(seed))
    n = target.native_ca.shape[0]
    phi_free = -math.pi + 2.0 * math.pi * torch.rand(n - 1, generator=gen, dtype=torch.float64)
    psi = -math.pi + 2.0 * math.pi * torch.rand(n - 1, generator=gen, dtype=torch.float64)
    return phi_free, psi


def run_one(target_name: str, seed: int, mode: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    if mode not in MODES:
        raise ValueError(mode)
    torch.use_deterministic_algorithms(True)
    target = load_target(target_name)
    phi0, psi0 = initial_torsions(target, seed)
    scales = regularizer_scales(target, phi0, psi0)

    phi_free = torch.nn.Parameter(phi0.clone())
    psi = torch.nn.Parameter(psi0.clone())
    optimizer = torch.optim.Adam([phi_free, psi], lr=LEARNING_RATE)

    traces: list[dict[str, object]] = []
    best_rmsd = float("inf")
    best_contact = -float("inf")
    start_rmsd = None
    failed = False

    for step in range(STEPS + 1):
        total, (n, ca, c), components = objective(target, phi_free, psi, mode, scales)
        if not torch.isfinite(total) or not torch.isfinite(ca).all():
            failed = True
            raise FloatingPointError(f"nonfinite state {target_name} seed={seed} mode={mode} step={step}")

        rmsd = kabsch_rmsd(ca, target.native_ca)
        recovery = contact_recovery(ca, target.native_contacts)
        if start_rmsd is None:
            start_rmsd = rmsd
        best_rmsd = min(best_rmsd, rmsd)
        if math.isfinite(recovery):
            best_contact = max(best_contact, recovery)

        if step == 0 or step == STEPS or step % 10 == 0:
            traces.append(
                {
                    "target": target_name,
                    "seed": seed,
                    "mode": mode,
                    "step": step,
                    "rmsd_A": rmsd,
                    "contact_recovery": recovery,
                    "rg_A": radius_of_gyration(ca),
                    **components,
                }
            )

        if step == STEPS:
            break

        optimizer.zero_grad(set_to_none=True)
        total.backward()
        if phi_free.grad is None or psi.grad is None:
            raise FloatingPointError("missing torsion gradient")
        if not torch.isfinite(phi_free.grad).all() or not torch.isfinite(psi.grad).all():
            raise FloatingPointError("nonfinite torsion gradient")
        optimizer.step()
        with torch.no_grad():
            phi_free.copy_(wrap_angle(phi_free))
            psi.copy_(wrap_angle(psi))

    final_total, (fn, fca, fc), _ = objective(target, phi_free, psi, mode, scales)
    final_phi = torch.cat([target.geometry.phi[:1], phi_free.detach()])
    final_psi = psi.detach().clone()
    max_len, max_ang = covalent_drift(target, fn.detach(), fca.detach(), fc.detach())

    row = {
        "target": target_name,
        "seed": int(seed),
        "mode": mode,
        "n_residues": int(target.native_ca.shape[0]),
        "start_rmsd_A": float(start_rmsd),
        "best_ca_rmsd_A": float(best_rmsd),
        "final_ca_rmsd_A": kabsch_rmsd(fca, target.native_ca),
        "best_contact_recovery": float(best_contact),
        "final_contact_recovery": contact_recovery(fca, target.native_contacts),
        "final_native_torsion_rmse_rad": native_torsion_rmse(target, final_phi, final_psi),
        "final_rg_A": radius_of_gyration(fca),
        "final_energy": float(final_total.detach()),
        "max_bond_length_drift_A": max_len,
        "max_bond_angle_drift_rad": max_ang,
        "failed": failed,
        **scales,
    }
    return row, traces


def exact_sign_flip_p(diffs: Iterable[float]) -> float:
    d = np.asarray(list(diffs), dtype=np.float64)
    if d.ndim != 1 or d.size == 0:
        raise ValueError("paired differences required")
    obs = abs(float(d.mean()))
    extreme = 0
    total = 1 << d.size
    for bits in range(total):
        signs = np.ones(d.size, dtype=np.float64)
        for i in range(d.size):
            if bits & (1 << i):
                signs[i] = -1.0
        stat = abs(float((signs * d).mean()))
        if stat >= obs - 1e-15:
            extreme += 1
    return extreme / total


def holm_two(p_a: float, p_b: float) -> tuple[float, float]:
    vals = [float(p_a), float(p_b)]
    order = sorted(range(2), key=lambda i: vals[i])
    adjusted = [0.0, 0.0]
    first = min(1.0, 2.0 * vals[order[0]])
    second = min(1.0, max(first, vals[order[1]]))
    adjusted[order[0]] = first
    adjusted[order[1]] = second
    return adjusted[0], adjusted[1]
