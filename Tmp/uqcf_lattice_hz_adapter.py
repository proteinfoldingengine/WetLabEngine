
"""
uqcf_lattice_hz_adapter.py

Minimal, explicit lattice-to-H(z) bridge for BAO blind tests.

Purpose
-------
This file does NOT claim a closed first-principles derivation of H(z).
It provides a transparent, fixed-parameter effective bridge that can be
audited and swapped out later if a deeper derivation is found.

Design principles
-----------------
- Keep low-regime lattice parameters fixed:
    D_f = 2.4959
    gamma = 0.5041
    beta = -0.997
- Make the bridge explicit and minimal.
- Separate shape from scale:
    * shape is mainly controlled by gamma, beta
    * scale is set by H0 and rd
- Avoid hidden retuning inside the code.

Bridge family implemented here
------------------------------
H(z)^2 / H0^2 = Omega_m (1+z)^3 + Omega_k (1+z)^2 + Omega_X * f_X(z)

with a lattice-inspired effective term

f_X(z) = (1+z)^(-gamma) * (1 + eta * beta * ln(1+z))

where eta is a declared bridge coefficient.

Interpretation:
- gamma controls fractal/coherence dilution
- beta controls weak running from cumulative loop/entropy effects
- eta controls how strongly the running enters the background sector

This is an EFFECTIVE mapping, not yet a proven microscopic derivation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import numpy as np


@dataclass
class LatticeBridgeParams:
    # Fixed low-regime lattice parameters
    D_f: float = 2.4959
    gamma: float = 0.5041
    beta: float = -0.997

    # Background / scale parameters (must be declared up front)
    H0: float = 70.0
    Omega_m: float = 0.30
    Omega_k: float = 0.0
    rd_Mpc: float = 147.05

    # Effective bridge parameter for running contribution
    eta: float = 0.25

    # If True, Omega_X is set by closure 1 - Omega_m - Omega_k
    enforce_closure: bool = True
    Omega_X: float = 0.70

    def finalized(self) -> "LatticeBridgeParams":
        p = LatticeBridgeParams(**asdict(self))
        if p.enforce_closure:
            p.Omega_X = 1.0 - p.Omega_m - p.Omega_k
        return p


def f_X(z: np.ndarray, p: LatticeBridgeParams) -> np.ndarray:
    """
    Lattice-inspired effective background contribution.
    """
    z = np.asarray(z, dtype=float)
    return np.power(1.0 + z, -p.gamma) * (1.0 + p.eta * p.beta * np.log1p(z))


def E2_of_z(z: np.ndarray, p: LatticeBridgeParams) -> np.ndarray:
    """
    E(z)^2 = H(z)^2 / H0^2
    """
    p = p.finalized()
    z = np.asarray(z, dtype=float)
    matter = p.Omega_m * np.power(1.0 + z, 3.0)
    curvature = p.Omega_k * np.power(1.0 + z, 2.0)
    lattice_x = p.Omega_X * f_X(z, p)
    return matter + curvature + lattice_x


def H_of_z(z: np.ndarray, p: LatticeBridgeParams) -> np.ndarray:
    e2 = E2_of_z(z, p)
    if np.any(e2 <= 0):
        raise ValueError("E(z)^2 became non-positive for the chosen parameters.")
    return p.finalized().H0 * np.sqrt(e2)


def describe_bridge(p: LatticeBridgeParams) -> dict:
    p = p.finalized()
    return {
        "status": "effective_bridge_not_first_principles_proof",
        "fixed_lattice_params": {
            "D_f": p.D_f,
            "gamma": p.gamma,
            "beta": p.beta,
        },
        "background_params": {
            "H0": p.H0,
            "Omega_m": p.Omega_m,
            "Omega_k": p.Omega_k,
            "Omega_X": p.Omega_X,
            "rd_Mpc": p.rd_Mpc,
        },
        "bridge_parameter": {
            "eta": p.eta
        },
        "equations": {
            "f_X(z)": "(1+z)^(-gamma) * (1 + eta * beta * ln(1+z))",
            "E2(z)": "Omega_m (1+z)^3 + Omega_k (1+z)^2 + Omega_X f_X(z)",
            "H(z)": "H0 * sqrt(E2(z))"
        }
    }


if __name__ == "__main__":
    p = LatticeBridgeParams()
    z = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    out = {
        "bridge": describe_bridge(p),
        "z": z.tolist(),
        "H_of_z": H_of_z(z, p).tolist(),
        "E2_of_z": E2_of_z(z, p).tolist()
    }
    print(json.dumps(out, indent=2))
