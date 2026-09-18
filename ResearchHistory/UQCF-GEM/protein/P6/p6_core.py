from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import torch

torch.set_default_dtype(torch.float64)

ROOT = Path(__file__).resolve().parent

TARGET_NAMES = ("1VII", "1L2Y", "1UAO")
MODES = ("physical_real_sequence", "physical_shuffled_sequence", "generic_collapse")
SEEDS = tuple(range(6))
STEPS = 300
LEARNING_RATE = 0.02
CONTACT_MIN_SEQ_SEPARATION = 4
NATIVE_CONTACT_CUTOFF_A = 8.0
RG_RATIO_GATE = (0.75, 1.25)

# Target-independent canonical backbone geometry, frozen before measurement.
N_CA_A = 1.46
CA_C_A = 1.52
C_N_A = 1.33
N_CA_C_RAD = math.radians(110.8914)
CA_C_N_RAD = math.radians(116.642992978)
C_N_CA_RAD = math.radians(121.38221582)
OMEGA_RAD = math.pi

# Common local/steric scaffold.
STERIC_CUTOFF_A = 3.6
STERIC_K = 2.0
RAMA_K = 0.20
RAMA_CENTERS = (
    (-math.pi / 3.0, -math.pi / 4.0),
    (-3.0 * math.pi / 4.0, 3.0 * math.pi / 4.0),
)

# DSSP-like backbone hydrogen-bond electrostatic term.
HBOND_COEFF = 27.888
HBOND_O_A = 1.231
HBOND_H_A = 1.0
HBOND_MIN_SEP = 3
HBOND_DISTANCE_FLOOR_A = 1.5
HBOND_FAVORABLE_CAP = -3.0

# Eisenberg normalized consensus hydrophobicity scale.
HYDROPATHY = {
    "A": 0.62, "R": -2.53, "N": -0.78, "D": -0.90, "C": 0.29,
    "Q": -0.85, "E": -0.74, "G": 0.48, "H": -0.40, "I": 1.38,
    "L": 1.06, "K": -1.50, "M": 0.64, "F": 1.19, "P": 0.12,
    "S": -0.18, "T": -0.05, "W": 0.81, "Y": 0.26, "V": 1.08,
}
HYDRO_MAX = 1.38
HYDRO_K = 0.593
CONTACT_MIDPOINT_A = 8.0
CONTACT_WIDTH_A = 0.5

# Screened Debye-Huckel electrostatics.
PH = 7.0
IONIC_STRENGTH_M = 0.15
WATER_RELATIVE_DIELECTRIC = 80.0
COULOMB_KCAL_A_PER_MOL_E2 = 332.06371
DEBYE_NUMERATOR_A_SQRT_M = 3.04
HISTIDINE_PKA = 6.0

AA3_TO_1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}

SHUFFLED_SEQUENCES = {
    "1VII": "LRSFKMAKELKSKMTAFLEKAFGWGDPFLQQLNDVN",
    "1L2Y": "NKPPLIGSQRDSWPSPLGGY",
    "1UAO": "TGYWEPGTGD",
}

TARGET_PATHS = {
    "1VII": ROOT.parent / "P5" / "inputs" / "1VII.pdb",
    "1L2Y": ROOT / "inputs" / "1L2Y.chainA_model1_NCAC.pdb",
    "1UAO": ROOT / "inputs" / "1UAO.chainA_model1_NCAC.pdb",
}
EXPECTED_LENGTHS = {"1VII": 36, "1L2Y": 20, "1UAO": 10}


@dataclass(frozen=True)
class CanonicalGeometry:
    anchor_n: torch.Tensor
    anchor_ca: torch.Tensor
    anchor_c: torch.Tensor
    n_ca_lengths: torch.Tensor
    ca_c_lengths: torch.Tensor
    c_n_lengths: torch.Tensor
    n_ca_c_angles: torch.Tensor
    ca_c_n_angles: torch.Tensor
    c_n_ca_angles: torch.Tensor
    phi: torch.Tensor
    psi: torch.Tensor
    omega: torch.Tensor


@dataclass(frozen=True)
class Target:
    name: str
    sequence: str
    native_ca: torch.Tensor


def _safe_normalize(v: torch.Tensor, eps: float = 1e-12) -> torch.Tensor:
    return v / torch.clamp(torch.linalg.norm(v, dim=-1, keepdim=True), min=eps)


def bond_angle(a: torch.Tensor, b: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
    u = _safe_normalize(a - b)
    v = _safe_normalize(c - b)
    return torch.acos(torch.clamp((u * v).sum(dim=-1), -1.0, 1.0))


def _place_atom(
    a: torch.Tensor,
    b: torch.Tensor,
    c: torch.Tensor,
    bond_length: torch.Tensor,
    bond_angle_value: torch.Tensor,
    dihedral_value: torch.Tensor,
) -> torch.Tensor:
    bc = _safe_normalize(c - b)
    ba = b - a
    normal = _safe_normalize(torch.cross(ba, bc, dim=-1))
    binormal = torch.cross(normal, bc, dim=-1)
    local = (
        -torch.cos(bond_angle_value) * bc
        + torch.sin(bond_angle_value)
        * (
            torch.cos(dihedral_value) * binormal
            + torch.sin(dihedral_value) * normal
        )
    )
    return c + bond_length * local


def canonical_geometry(n_residues: int) -> CanonicalGeometry:
    if n_residues < 2:
        raise ValueError("P6 requires at least two residues")
    dtype = torch.float64
    n0 = torch.tensor([0.0, 0.0, 0.0], dtype=dtype)
    ca0 = torch.tensor([N_CA_A, 0.0, 0.0], dtype=dtype)
    direction = torch.tensor(
        [-math.cos(N_CA_C_RAD), math.sin(N_CA_C_RAD), 0.0],
        dtype=dtype,
    )
    c0 = ca0 + CA_C_A * direction
    return CanonicalGeometry(
        anchor_n=n0,
        anchor_ca=ca0,
        anchor_c=c0,
        n_ca_lengths=torch.full((n_residues,), N_CA_A, dtype=dtype),
        ca_c_lengths=torch.full((n_residues,), CA_C_A, dtype=dtype),
        c_n_lengths=torch.full((n_residues - 1,), C_N_A, dtype=dtype),
        n_ca_c_angles=torch.full((n_residues,), N_CA_C_RAD, dtype=dtype),
        ca_c_n_angles=torch.full((n_residues - 1,), CA_C_N_RAD, dtype=dtype),
        c_n_ca_angles=torch.full((n_residues - 1,), C_N_CA_RAD, dtype=dtype),
        phi=torch.zeros((n_residues,), dtype=dtype),
        psi=torch.zeros((n_residues - 1,), dtype=dtype),
        omega=torch.full((n_residues - 1,), OMEGA_RAD, dtype=dtype),
    )


def reconstruct_backbone(
    geometry: CanonicalGeometry,
    phi: torch.Tensor,
    psi: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    n_residues = geometry.n_ca_lengths.numel()
    if phi.shape != (n_residues,):
        raise ValueError(f"phi must have shape [{n_residues}]")
    if psi.shape != (n_residues - 1,):
        raise ValueError(f"psi must have shape [{n_residues - 1}]")

    n_atoms = [geometry.anchor_n]
    ca_atoms = [geometry.anchor_ca]
    c_atoms = [geometry.anchor_c]

    for index in range(n_residues - 1):
        n_next = _place_atom(
            n_atoms[-1],
            ca_atoms[-1],
            c_atoms[-1],
            geometry.c_n_lengths[index],
            geometry.ca_c_n_angles[index],
            psi[index],
        )
        ca_next = _place_atom(
            ca_atoms[-1],
            c_atoms[-1],
            n_next,
            geometry.n_ca_lengths[index + 1],
            geometry.c_n_ca_angles[index],
            geometry.omega[index],
        )
        c_next = _place_atom(
            c_atoms[-1],
            n_next,
            ca_next,
            geometry.ca_c_lengths[index + 1],
            geometry.n_ca_c_angles[index + 1],
            phi[index + 1],
        )
        n_atoms.append(n_next)
        ca_atoms.append(ca_next)
        c_atoms.append(c_next)

    return torch.stack(n_atoms), torch.stack(ca_atoms), torch.stack(c_atoms)


def covalent_drift(
    geometry: CanonicalGeometry,
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
) -> tuple[float, float]:
    length_errors = [
        torch.max(
            torch.abs(
                torch.linalg.norm(n - ca, dim=-1) - geometry.n_ca_lengths
            )
        ),
        torch.max(
            torch.abs(
                torch.linalg.norm(ca - c, dim=-1) - geometry.ca_c_lengths
            )
        ),
        torch.max(
            torch.abs(
                torch.linalg.norm(c[:-1] - n[1:], dim=-1)
                - geometry.c_n_lengths
            )
        ),
    ]
    angle_errors = [
        torch.max(
            torch.abs(
                bond_angle(n, ca, c) - geometry.n_ca_c_angles
            )
        ),
        torch.max(
            torch.abs(
                bond_angle(ca[:-1], c[:-1], n[1:])
                - geometry.ca_c_n_angles
            )
        ),
        torch.max(
            torch.abs(
                bond_angle(c[:-1], n[1:], ca[1:])
                - geometry.c_n_ca_angles
            )
        ),
    ]
    return (
        float(torch.max(torch.stack(length_errors))),
        float(torch.max(torch.stack(angle_errors))),
    )


def _first_model_records(path: Path) -> list[str]:
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
    if name not in TARGET_NAMES:
        raise KeyError(name)

    rows: dict[tuple[str, int, str], dict[str, object]] = {}
    order: list[tuple[str, int, str]] = []

    for line in _first_model_records(TARGET_PATHS[name]):
        if (
            not line.startswith("ATOM")
            or len(line) < 54
            or line[21:22] != "A"
        ):
            continue
        if line[16:17] not in (" ", "A"):
            continue
        atom = line[12:16].strip()
        if atom not in ("N", "CA", "C"):
            continue
        resname = line[17:20].strip().upper()
        if resname not in AA3_TO_1:
            continue

        key = (line[21:22], int(line[22:26]), line[26:27].strip())
        if key not in rows:
            rows[key] = {"resname": resname}
            order.append(key)

        rows[key].setdefault(
            atom,
            (
                float(line[30:38]),
                float(line[38:46]),
                float(line[46:54]),
            ),
        )

    complete = [
        key
        for key in order
        if all(atom in rows[key] for atom in ("N", "CA", "C"))
    ]
    if len(complete) != EXPECTED_LENGTHS[name]:
        raise ValueError(
            f"{name}: expected {EXPECTED_LENGTHS[name]} complete residues, "
            f"got {len(complete)}"
        )

    sequence = "".join(
        AA3_TO_1[str(rows[key]["resname"])] for key in complete
    )
    native_ca = torch.tensor(
        [rows[key]["CA"] for key in complete],
        dtype=torch.float64,
    )
    return Target(name=name, sequence=sequence, native_ca=native_ca)


def shuffled_sequence(name: str) -> str:
    return SHUFFLED_SEQUENCES[name]


def wrap_angle(x: torch.Tensor) -> torch.Tensor:
    return torch.atan2(torch.sin(x), torch.cos(x))


def initial_torsions(
    n_residues: int,
    seed: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    if n_residues < 2:
        raise ValueError(n_residues)

    generator = torch.Generator(device="cpu")
    generator.manual_seed(
        2_026_091_800
        + 10_007 * int(seed)
        + 101 * int(n_residues)
    )
    phi_free = (
        -math.pi
        + 2.0
        * math.pi
        * torch.rand(
            n_residues - 1,
            generator=generator,
            dtype=torch.float64,
        )
    )
    psi = (
        -math.pi
        + 2.0
        * math.pi
        * torch.rand(
            n_residues - 1,
            generator=generator,
            dtype=torch.float64,
        )
    )
    return phi_free, psi


def _rama_energy(
    phi: torch.Tensor,
    psi: torch.Tensor,
) -> torch.Tensor:
    if phi.numel() < 3:
        return phi.new_tensor(0.0)

    p = phi[1:-1]
    q = psi[1:]
    angles = torch.stack([p, q], dim=1)
    centers = angles.new_tensor(RAMA_CENTERS)
    delta = wrap_angle(
        angles[:, None, :] - centers[None, :, :]
    )
    d2 = (delta * delta).sum(dim=-1)
    return RAMA_K * d2.min(dim=1).values.mean()


def _steric_energy(ca: torch.Tensor) -> torch.Tensor:
    n_residues = ca.shape[0]
    if n_residues < 3:
        return ca.new_tensor(0.0)

    distances = torch.cdist(ca, ca)
    indices = torch.arange(n_residues, device=ca.device)
    separation = torch.abs(
        indices[:, None] - indices[None, :]
    )
    mask = (
        torch.triu(
            torch.ones(
                (n_residues, n_residues),
                dtype=torch.bool,
                device=ca.device,
            ),
            diagonal=1,
        )
        & (separation >= 2)
    )
    r = distances[mask]
    if r.numel() == 0:
        return ca.new_tensor(0.0)
    return STERIC_K * torch.mean(
        torch.relu(STERIC_CUTOFF_A - r) ** 2
    )


def _contact_switch(r: torch.Tensor) -> torch.Tensor:
    return torch.sigmoid(
        (CONTACT_MIDPOINT_A - r) / CONTACT_WIDTH_A
    )


def _hydropathy_energy(
    ca: torch.Tensor,
    sequence: str,
) -> torch.Tensor:
    distances = torch.cdist(ca, ca)
    terms = []

    for i in range(len(sequence)):
        hi = max(HYDROPATHY[sequence[i]], 0.0) / HYDRO_MAX
        if hi == 0.0:
            continue
        for j in range(i + 3, len(sequence)):
            hj = max(HYDROPATHY[sequence[j]], 0.0) / HYDRO_MAX
            if hj == 0.0:
                continue
            terms.append(
                -HYDRO_K
                * hi
                * hj
                * _contact_switch(distances[i, j])
            )

    return (
        torch.stack(terms).sum()
        if terms
        else ca.new_tensor(0.0)
    )


def _charges(
    sequence: str,
    *,
    device: torch.device,
) -> torch.Tensor:
    q = torch.zeros(
        len(sequence),
        dtype=torch.float64,
        device=device,
    )

    for index, aa in enumerate(sequence):
        if aa in ("D", "E"):
            q[index] -= 1.0
        elif aa in ("K", "R"):
            q[index] += 1.0
        elif aa == "H":
            q[index] += 1.0 / (
                1.0 + 10.0 ** (PH - HISTIDINE_PKA)
            )

    q[0] += 1.0
    q[-1] -= 1.0
    return q


def _electrostatic_energy(
    ca: torch.Tensor,
    sequence: str,
) -> torch.Tensor:
    q = _charges(sequence, device=ca.device)
    distances = torch.cdist(ca, ca)
    screening_length = (
        DEBYE_NUMERATOR_A_SQRT_M
        / math.sqrt(IONIC_STRENGTH_M)
    )
    prefactor = (
        COULOMB_KCAL_A_PER_MOL_E2
        / WATER_RELATIVE_DIELECTRIC
    )

    terms = []
    for i in range(len(sequence)):
        if float(q[i]) == 0.0:
            continue
        for j in range(i + 2, len(sequence)):
            if float(q[j]) == 0.0:
                continue
            r = torch.clamp(
                distances[i, j],
                min=1e-6,
            )
            terms.append(
                prefactor
                * q[i]
                * q[j]
                * torch.exp(-r / screening_length)
                / r
            )

    return (
        torch.stack(terms).sum()
        if terms
        else ca.new_tensor(0.0)
    )


def _virtual_oxygen(
    ca_i: torch.Tensor,
    c_i: torch.Tensor,
    n_next: torch.Tensor,
) -> torch.Tensor:
    u1 = _safe_normalize(ca_i - c_i)
    u2 = _safe_normalize(n_next - c_i)
    direction = -_safe_normalize(u1 + u2)
    return c_i + HBOND_O_A * direction


def _virtual_hydrogen(
    c_prev: torch.Tensor,
    n_i: torch.Tensor,
    ca_i: torch.Tensor,
) -> torch.Tensor:
    u1 = _safe_normalize(c_prev - n_i)
    u2 = _safe_normalize(ca_i - n_i)
    direction = -_safe_normalize(u1 + u2)
    return n_i + HBOND_H_A * direction


def _hbond_energy(
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
    sequence: str,
) -> torch.Tensor:
    residue_count = len(sequence)
    oxygens = [
        _virtual_oxygen(
            ca[index],
            c[index],
            n[index + 1],
        )
        for index in range(residue_count - 1)
    ]
    hydrogens = {
        index: _virtual_hydrogen(
            c[index - 1],
            n[index],
            ca[index],
        )
        for index in range(1, residue_count)
        if sequence[index] != "P"
    }

    terms = []
    for donor_index, hydrogen in hydrogens.items():
        for acceptor_index, oxygen in enumerate(oxygens):
            if (
                abs(donor_index - acceptor_index)
                < HBOND_MIN_SEP
            ):
                continue

            r_on = torch.clamp(
                torch.linalg.norm(
                    oxygen - n[donor_index]
                ),
                min=HBOND_DISTANCE_FLOOR_A,
            )
            r_ch = torch.clamp(
                torch.linalg.norm(
                    c[acceptor_index] - hydrogen
                ),
                min=HBOND_DISTANCE_FLOOR_A,
            )
            r_oh = torch.clamp(
                torch.linalg.norm(
                    oxygen - hydrogen
                ),
                min=HBOND_DISTANCE_FLOOR_A,
            )
            r_cn = torch.clamp(
                torch.linalg.norm(
                    c[acceptor_index]
                    - n[donor_index]
                ),
                min=HBOND_DISTANCE_FLOOR_A,
            )

            energy = HBOND_COEFF * (
                1.0 / r_on
                + 1.0 / r_ch
                - 1.0 / r_oh
                - 1.0 / r_cn
            )
            favorable = torch.minimum(
                energy,
                energy.new_tensor(0.0),
            )
            terms.append(
                torch.maximum(
                    favorable,
                    energy.new_tensor(
                        HBOND_FAVORABLE_CAP
                    ),
                )
            )

    return (
        torch.stack(terms).sum()
        if terms
        else ca.new_tensor(0.0)
    )


def _generic_contact_raw(
    ca: torch.Tensor,
) -> torch.Tensor:
    distances = torch.cdist(ca, ca)
    terms = [
        _contact_switch(distances[i, j])
        for i in range(ca.shape[0])
        for j in range(i + 3, ca.shape[0])
    ]
    return (
        -torch.stack(terms).sum()
        if terms
        else ca.new_tensor(0.0)
    )


def _physical_nonlocal(
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
    sequence: str,
) -> tuple[
    torch.Tensor,
    dict[str, torch.Tensor],
]:
    hydropathy = _hydropathy_energy(ca, sequence)
    electrostatics = _electrostatic_energy(
        ca,
        sequence,
    )
    hbond = _hbond_energy(
        n,
        ca,
        c,
        sequence,
    )
    return (
        hydropathy + electrostatics + hbond,
        {
            "hydropathy": hydropathy,
            "electrostatics": electrostatics,
            "hbond": hbond,
        },
    )


def _gradient_norm(
    energy: torch.Tensor,
    params: Iterable[torch.Tensor],
    *,
    retain_graph: bool = True,
) -> float:
    gradients = torch.autograd.grad(
        energy,
        tuple(params),
        retain_graph=retain_graph,
        allow_unused=False,
    )
    value = torch.sqrt(
        sum(
            (gradient * gradient).sum()
            for gradient in gradients
        )
    )
    return float(value.detach())


def generic_collapse_scale(
    sequence: str,
    phi_free_init: torch.Tensor,
    psi_init: torch.Tensor,
) -> float:
    phi_free = (
        phi_free_init.detach()
        .clone()
        .requires_grad_(True)
    )
    psi = (
        psi_init.detach()
        .clone()
        .requires_grad_(True)
    )

    geometry = canonical_geometry(len(sequence))
    phi = torch.cat(
        [geometry.phi[:1], phi_free]
    )
    n, ca, c = reconstruct_backbone(
        geometry,
        phi,
        psi,
    )

    physical, _ = _physical_nonlocal(
        n,
        ca,
        c,
        sequence,
    )
    generic = _generic_contact_raw(ca)

    physical_gradient = _gradient_norm(
        physical,
        (phi_free, psi),
        retain_graph=True,
    )
    generic_gradient = _gradient_norm(
        generic,
        (phi_free, psi),
        retain_graph=False,
    )

    if (
        not math.isfinite(physical_gradient)
        or not math.isfinite(generic_gradient)
        or generic_gradient < 1e-12
    ):
        raise FloatingPointError(
            (physical_gradient, generic_gradient)
        )

    return physical_gradient / generic_gradient


def initial_nonlocal_gradient_norm(
    sequence: str,
    phi_free_init: torch.Tensor,
    psi_init: torch.Tensor,
    mode: str,
    *,
    generic_scale: float,
) -> float:
    phi_free = (
        phi_free_init.detach()
        .clone()
        .requires_grad_(True)
    )
    psi = (
        psi_init.detach()
        .clone()
        .requires_grad_(True)
    )

    geometry = canonical_geometry(len(sequence))
    phi = torch.cat(
        [geometry.phi[:1], phi_free]
    )
    n, ca, c = reconstruct_backbone(
        geometry,
        phi,
        psi,
    )

    if mode == "physical_real_sequence":
        energy, _ = _physical_nonlocal(
            n,
            ca,
            c,
            sequence,
        )
    elif mode == "generic_collapse":
        energy = (
            generic_scale
            * _generic_contact_raw(ca)
        )
    else:
        raise ValueError(mode)

    return _gradient_norm(
        energy,
        (phi_free, psi),
        retain_graph=False,
    )


def objective(
    target: Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    mode: str,
    *,
    generic_scale: float,
) -> tuple[
    torch.Tensor,
    tuple[
        torch.Tensor,
        torch.Tensor,
        torch.Tensor,
    ],
    dict[str, float],
]:
    if mode not in MODES:
        raise ValueError(mode)

    geometry = canonical_geometry(
        len(target.sequence)
    )
    phi = torch.cat(
        [geometry.phi[:1], phi_free]
    )
    n, ca, c = reconstruct_backbone(
        geometry,
        phi,
        psi,
    )

    steric = _steric_energy(ca)
    rama = _rama_energy(phi, psi)

    hydropathy = ca.new_tensor(0.0)
    electrostatics = ca.new_tensor(0.0)
    hbond = ca.new_tensor(0.0)
    generic = ca.new_tensor(0.0)

    if mode == "physical_real_sequence":
        nonlocal_energy, components = (
            _physical_nonlocal(
                n,
                ca,
                c,
                target.sequence,
            )
        )
        hydropathy = components["hydropathy"]
        electrostatics = components[
            "electrostatics"
        ]
        hbond = components["hbond"]
    elif mode == "physical_shuffled_sequence":
        sequence = shuffled_sequence(
            target.name
        )
        nonlocal_energy, components = (
            _physical_nonlocal(
                n,
                ca,
                c,
                sequence,
            )
        )
        hydropathy = components["hydropathy"]
        electrostatics = components[
            "electrostatics"
        ]
        hbond = components["hbond"]
    else:
        generic = (
            generic_scale
            * _generic_contact_raw(ca)
        )
        nonlocal_energy = generic

    total = (
        steric
        + rama
        + nonlocal_energy
    )

    components_out = {
        "steric": float(steric.detach()),
        "rama": float(rama.detach()),
        "hydropathy": float(
            hydropathy.detach()
        ),
        "electrostatics": float(
            electrostatics.detach()
        ),
        "hbond": float(hbond.detach()),
        "generic_collapse": float(
            generic.detach()
        ),
        "total": float(total.detach()),
    }

    return (
        total,
        (n, ca, c),
        components_out,
    )


def topk_native_contact_precision(
    model_ca: torch.Tensor,
    native_ca: torch.Tensor,
) -> tuple[float, int]:
    if (
        model_ca.shape != native_ca.shape
        or model_ca.ndim != 2
        or model_ca.shape[1] != 3
    ):
        raise ValueError(
            "coordinate shapes must match [N,3]"
        )

    n_residues = model_ca.shape[0]
    pairs = [
        (i, j)
        for i in range(n_residues)
        for j in range(
            i + CONTACT_MIN_SEQ_SEPARATION,
            n_residues,
        )
    ]
    if not pairs:
        raise ValueError(
            "not enough residues for "
            "long-range contact precision"
        )

    k = min(
        max(1, n_residues // 2),
        len(pairs),
    )
    model_distances = torch.cdist(
        model_ca,
        model_ca,
    )
    native_distances = torch.cdist(
        native_ca,
        native_ca,
    )

    ranked = sorted(
        pairs,
        key=lambda pair: float(
            model_distances[
                pair[0],
                pair[1],
            ].detach()
        ),
    )[:k]

    hits = sum(
        float(
            native_distances[i, j]
            < NATIVE_CONTACT_CUTOFF_A
        )
        for i, j in ranked
    )

    return hits / k, k


def radius_of_gyration(
    ca: torch.Tensor,
) -> float:
    centered = ca - ca.mean(dim=0)
    return float(
        torch.sqrt(
            torch.mean(
                torch.sum(
                    centered * centered,
                    dim=1,
                )
            )
        ).detach()
    )


def kabsch_rmsd(
    x: torch.Tensor,
    y: torch.Tensor,
) -> float:
    x = x.detach().to(dtype=torch.float64)
    y = y.detach().to(dtype=torch.float64)
    xc = x - x.mean(dim=0)
    yc = y - y.mean(dim=0)
    covariance = xc.T @ yc
    u, _, vh = torch.linalg.svd(covariance)
    determinant = torch.sign(
        torch.det(u @ vh)
    )
    if float(determinant) == 0.0:
        determinant = x.new_tensor(1.0)
    diagonal = torch.eye(
        3,
        dtype=x.dtype,
        device=x.device,
    )
    diagonal[-1, -1] = determinant
    rotation = u @ diagonal @ vh
    aligned = xc @ rotation
    return float(
        torch.sqrt(
            torch.mean(
                torch.sum(
                    (aligned - yc) ** 2,
                    dim=1,
                )
            )
        )
    )


def exact_sign_flip_p(
    differences: Iterable[float],
) -> float:
    values = [float(value) for value in differences]
    if not values:
        raise ValueError("empty differences")

    observed = abs(
        sum(values) / len(values)
    )
    total = 1 << len(values)
    extreme = 0

    for bits in range(total):
        signed_sum = 0.0
        for index, value in enumerate(values):
            signed_sum += (
                value
                if ((bits >> index) & 1)
                else -value
            )
        statistic = abs(
            signed_sum / len(values)
        )
        if statistic + 1e-15 >= observed:
            extreme += 1

    return extreme / total


def holm_two(
    p1: float,
    p2: float,
) -> tuple[float, float]:
    values = [
        (float(p1), 0),
        (float(p2), 1),
    ]
    values.sort()
    adjusted = [0.0, 0.0]

    first = min(
        1.0,
        2.0 * values[0][0],
    )
    second = min(
        1.0,
        max(first, values[1][0]),
    )

    adjusted[values[0][1]] = first
    adjusted[values[1][1]] = second
    return adjusted[0], adjusted[1]
