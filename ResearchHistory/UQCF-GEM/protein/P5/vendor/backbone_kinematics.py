from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch

from residue_identity import ResidueId


def _safe_normalize(v: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    return v / torch.clamp(torch.linalg.norm(v, dim=-1, keepdim=True), min=eps)


def bond_angle(a: torch.Tensor, b: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
    u = _safe_normalize(a - b)
    v = _safe_normalize(c - b)
    cosine = torch.clamp((u * v).sum(dim=-1), -1.0, 1.0)
    return torch.acos(cosine)


def dihedral(
    a: torch.Tensor,
    b: torch.Tensor,
    c: torch.Tensor,
    d: torch.Tensor,
) -> torch.Tensor:
    """Return an inverse-consistent signed torsion for `_place_atom`."""

    b1 = b - a
    b2 = c - b
    b3 = d - c

    n1 = _safe_normalize(torch.cross(b1, b2, dim=-1))
    n2 = _safe_normalize(torch.cross(b2, b3, dim=-1))
    b2n = _safe_normalize(b2)

    x = (n1 * n2).sum(dim=-1)
    y = (torch.cross(n1, b2n, dim=-1) * n2).sum(dim=-1)
    return torch.atan2(-y, x)


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


@dataclass(frozen=True, slots=True)
class ChainBackboneGeometry:
    start_index: int
    stop_index: int
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


def _validate_inputs(
    n_coords: torch.Tensor,
    ca_coords: torch.Tensor,
    c_coords: torch.Tensor,
    residue_ids: Iterable[ResidueId],
) -> list[ResidueId]:
    residue_ids = list(residue_ids)

    if n_coords.ndim != 2 or n_coords.shape[-1] != 3:
        raise ValueError("n_coords must have shape [N, 3].")
    if ca_coords.shape != n_coords.shape or c_coords.shape != n_coords.shape:
        raise ValueError("N, CA, and C coordinate tensors must have identical [N, 3] shape.")
    if len(residue_ids) != n_coords.shape[0]:
        raise ValueError(
            "Residue identity count must match the number of backbone coordinate rows."
        )
    if not residue_ids:
        raise ValueError("At least one residue is required for backbone geometry extraction.")

    return residue_ids


def _extract_segment(
    n_coords: torch.Tensor,
    ca_coords: torch.Tensor,
    c_coords: torch.Tensor,
    start_index: int,
    stop_index: int,
) -> ChainBackboneGeometry:
    n = n_coords[start_index:stop_index].detach().clone()
    ca = ca_coords[start_index:stop_index].detach().clone()
    c = c_coords[start_index:stop_index].detach().clone()

    count = stop_index - start_index

    n_ca_lengths = torch.linalg.norm(n - ca, dim=-1)
    ca_c_lengths = torch.linalg.norm(ca - c, dim=-1)
    n_ca_c_angles = bond_angle(n, ca, c)

    phi = torch.zeros(count, dtype=n.dtype, device=n.device)

    if count > 1:
        c_n_lengths = torch.linalg.norm(c[:-1] - n[1:], dim=-1)
        ca_c_n_angles = bond_angle(ca[:-1], c[:-1], n[1:])
        c_n_ca_angles = bond_angle(c[:-1], n[1:], ca[1:])
        psi = dihedral(n[:-1], ca[:-1], c[:-1], n[1:])
        omega = dihedral(ca[:-1], c[:-1], n[1:], ca[1:])
        phi[1:] = dihedral(c[:-1], n[1:], ca[1:], c[1:])
    else:
        c_n_lengths = n.new_empty((0,))
        ca_c_n_angles = n.new_empty((0,))
        c_n_ca_angles = n.new_empty((0,))
        psi = n.new_empty((0,))
        omega = n.new_empty((0,))

    return ChainBackboneGeometry(
        start_index=start_index,
        stop_index=stop_index,
        anchor_n=n[0],
        anchor_ca=ca[0],
        anchor_c=c[0],
        n_ca_lengths=n_ca_lengths,
        ca_c_lengths=ca_c_lengths,
        c_n_lengths=c_n_lengths,
        n_ca_c_angles=n_ca_c_angles,
        ca_c_n_angles=ca_c_n_angles,
        c_n_ca_angles=c_n_ca_angles,
        phi=phi,
        psi=psi,
        omega=omega,
    )


def extract_chain_backbone_geometry(
    n_coords: torch.Tensor,
    ca_coords: torch.Tensor,
    c_coords: torch.Tensor,
    residue_ids: list[ResidueId],
) -> list[ChainBackboneGeometry]:
    """Extract fixed covalent geometry for each contiguous PDB chain segment."""

    residue_ids = _validate_inputs(n_coords, ca_coords, c_coords, residue_ids)

    segments: list[tuple[int, int]] = []
    start = 0
    for index in range(1, len(residue_ids)):
        if residue_ids[index].chain_id != residue_ids[index - 1].chain_id:
            segments.append((start, index))
            start = index
    segments.append((start, len(residue_ids)))

    return [
        _extract_segment(n_coords, ca_coords, c_coords, start_index, stop_index)
        for start_index, stop_index in segments
    ]


def reconstruct_chain_backbone(
    geometry: ChainBackboneGeometry,
    phi: torch.Tensor,
    psi: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Reconstruct one chain from fixed source geometry and supplied phi/psi torsions."""

    count = geometry.stop_index - geometry.start_index
    if phi.shape != (count,):
        raise ValueError(f"phi must have shape [{count}].")
    if psi.shape != (max(0, count - 1),):
        raise ValueError(f"psi must have shape [{max(0, count - 1)}].")

    n_atoms = [geometry.anchor_n]
    ca_atoms = [geometry.anchor_ca]
    c_atoms = [geometry.anchor_c]

    for index in range(count - 1):
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
