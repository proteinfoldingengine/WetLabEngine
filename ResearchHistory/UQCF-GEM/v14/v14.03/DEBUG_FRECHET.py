#!/usr/bin/env python3
import json
import numpy as np
from scipy.linalg import expm_frechet

import source_ray_audit as sra


def stable_tangent(X0, P):
    X0 = sra._herm(np.asarray(X0, dtype=complex))
    P = sra._herm(np.asarray(P, dtype=complex))
    p, U = np.linalg.eigh(X0)
    A = sra._herm(U @ np.diag(np.log(p)) @ U.conj().T)
    raw = expm_frechet(A, P, compute_expm=False)
    mean = float(np.real(np.trace(X0 @ P)))
    return sra._herm(raw - X0 * mean)

v1402 = sra.load_v1402()
configs = {name: sra.build_configuration(v1402, name) for name in ("V_A", "V_B")}
rng = np.random.default_rng(sra.SEED)
sources = {name: sra.sample_sources(configs[name]["X0"], sra.PRIMARY_SAMPLES, rng) for name in ("V_A", "V_B")}
contexts = {
    "V_A": sra._gauge_contexts(configs["V_A"], 14031),
    "V_B": sra._gauge_contexts(configs["V_B"], 14032),
}

out = {}
for name in ("V_A", "V_B"):
    cfg = configs[name]
    max_old_cov = 0.0
    max_new_cov = 0.0
    max_base_old_new = 0.0
    max_new_fd = 0.0
    for P in sources[name]:
        old = sra.pgrl_tangent(cfg["X0"], P)
        new = stable_tangent(cfg["X0"], P)
        max_base_old_new = max(max_base_old_new, sra._rel_matrix_error(old, new))
        fd = (sra.pgrl_state(cfg["X0"], P, sra.FD_EPS) - sra.pgrl_state(cfg["X0"], P, -sra.FD_EPS))/(2*sra.FD_EPS)
        max_new_fd = max(max_new_fd, sra._rel_matrix_error(new, sra._herm(fd)))
        for ctx in contexts[name]:
            U = ctx["U"]
            P2 = sra._herm(U @ P @ U.conj().T)
            old2 = sra.pgrl_tangent(ctx["X0"], P2)
            new2 = stable_tangent(ctx["X0"], P2)
            max_old_cov = max(max_old_cov, sra._rel_matrix_error(old2, U @ old @ U.conj().T))
            max_new_cov = max(max_new_cov, sra._rel_matrix_error(new2, U @ new @ U.conj().T))
    out[name] = {
        "max_old_covariance_error": max_old_cov,
        "max_stable_frechet_covariance_error": max_new_cov,
        "max_base_old_vs_stable_error": max_base_old_new,
        "max_stable_frechet_fd_error": max_new_fd,
    }

print("V14_03_FRECHET_HYPOTHESIS_TEST")
print(json.dumps(out, indent=2, sort_keys=True))
