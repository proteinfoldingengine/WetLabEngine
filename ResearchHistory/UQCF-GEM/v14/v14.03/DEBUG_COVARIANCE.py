#!/usr/bin/env python3
import json
import numpy as np

import source_ray_audit as sra

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
    maxima = {"tangent": 0.0, "hidden": 0.0, "hidden_unit": 0.0, "boundary": 0.0, "dual": 0.0}
    where = {k: None for k in maxima}
    for si, P in enumerate(sources[name]):
        base = sra.source_contact(v1402, cfg, P, certify_base_formula=True)
        for ui, ctx in enumerate(contexts[name]):
            U = ctx["U"]
            cfg2 = {**cfg, "X0": ctx["X0"], "modes": ctx["modes"]}
            P2 = sra._herm(U @ P @ U.conj().T)
            c2 = sra.source_contact(v1402, cfg2, P2, certify_base_formula=False)
            expected = {
                "tangent": U @ base["dotX"] @ U.conj().T,
                "hidden": U @ base["hidden"]["V"] @ U.conj().T,
                "hidden_unit": U @ base["hidden"]["unit_matrix"] @ U.conj().T,
                "boundary": U @ base["boundary"]["Xstar"] @ U.conj().T,
                "dual": U @ base["dual_rep"] @ U.conj().T,
            }
            actual = {
                "tangent": c2["dotX"],
                "hidden": c2["hidden"]["V"],
                "hidden_unit": c2["hidden"]["unit_matrix"],
                "boundary": c2["boundary"]["Xstar"],
                "dual": c2["dual_rep"],
            }
            for key in maxima:
                err = sra._rel_matrix_error(actual[key], expected[key])
                if err > maxima[key]:
                    maxima[key] = float(err)
                    where[key] = {"source_index": si, "unitary_index": ui}
    out[name] = {"maxima": maxima, "where": where}

print("V14_03_COVARIANCE_LAYER_DEBUG")
print(json.dumps(out, indent=2, sort_keys=True))
