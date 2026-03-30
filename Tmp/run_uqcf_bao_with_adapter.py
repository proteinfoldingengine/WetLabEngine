
"""
run_uqcf_bao_with_adapter.py

Runs the DESI DR2 BAO blind-test module using the explicit effective lattice H(z) bridge.
"""

from __future__ import annotations

import json
from uqcf_lattice_hz_adapter import LatticeBridgeParams, H_of_z
from desi_bao_blind_test import evaluate_bao_model, chi2_bao


def main():
    p = LatticeBridgeParams(
        D_f=2.4959,
        gamma=0.5041,
        beta=-0.997,
        H0=70.0,
        Omega_m=0.30,
        Omega_k=0.0,
        rd_Mpc=147.05,
        eta=0.25,
        enforce_closure=True,
    )

    df = evaluate_bao_model(rd_Mpc=p.rd_Mpc, H_of_z=lambda z: H_of_z(z, p))
    stats = chi2_bao(rd_Mpc=p.rd_Mpc, H_of_z=lambda z: H_of_z(z, p))

    out = {
        "note": "This is an effective-bridge BAO run, not a closed first-principles proof.",
        "params": p.__dict__,
        "table": df.to_dict(orient="records"),
        "stats": stats
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
