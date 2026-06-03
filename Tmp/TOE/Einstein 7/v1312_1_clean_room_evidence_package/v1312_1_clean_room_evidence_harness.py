#!/usr/bin/env python3
"""
V1312.1 — Consolidated Clean-Room Evidence Harness

Purpose:
    Provide the missing computational evidence for the V1312 external adversarial review.

Frozen claim under review:
    Inside the tested synthetic transport simulations, identity + closure is a scaled,
    adversarially tested minimal sufficient stack for rejecting identity-matched
    counterfeits while preserving B-like closure and ADM_M-like propagation.

This script is intentionally synthetic. It does NOT claim:
    - physical GR
    - Einstein equations
    - physical spacetime curvature
    - full ADM derivation
    - universality beyond tested simulations
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd

OUT = Path("v1312_1_clean_room_evidence_outputs")
OUT.mkdir(exist_ok=True)

EPS = 1e-12
BETA = 3.0
VALID = "legitimate_transport"

BASE_WEIGHTS = {
    "source_path": 1.0,
    "repair": 0.05,
    "access_loss": 0.05,
}

BASE_MODES = [
    "legitimate_transport",
    "identity_matched_response_scramble",
    "identity_matched_nonlinear_response",
    "identity_matched_spectral_response",
    "identity_matched_lagged_response",
    "identity_matched_flow_phase_warp",
    "identity_matched_current_flip",
    "identity_matched_local_spike",
    "source_shuffle",
    "time_reverse",
]

REGIMES = {
    "identity_only": {"identity": 3.0},
    "closure_only": {"closure": 1.5},
    "momentum_only": {"momentum": 3.0},
    "identity_plus_closure": {"identity": 3.0, "closure": 1.5},
    "identity_plus_momentum": {"identity": 3.0, "momentum": 3.0},
    "closure_plus_momentum": {"closure": 1.5, "momentum": 3.0},
    "identity_closure_momentum": {"identity": 3.0, "closure": 1.5, "momentum": 3.0},
}


def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / (x.std() + EPS)


def corr(a, b):
    if np.std(a) < EPS or np.std(b) < EPS:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def grad(f, x):
    return np.gradient(f, x)


def lap_fast(f):
    return np.roll(f, 1) + np.roll(f, -1) - 2 * f


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x) ** 2)))


def cosine(a, b):
    a = np.ravel(a)
    b = np.ravel(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + EPS))


def base_history(seed: int, N: int, T: int):
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, N)
    rho = np.exp(0.55 * z(np.sin(2 * np.pi * x + rng.uniform(-0.1, 0.1)) + 0.25 * np.cos(5 * np.pi * x)))
    hist = []

    for t in range(T):
        tau = t / (T - 1)
        psi = np.log(rho + EPS)
        J = -0.12 * grad(psi, x) + 0.03 * np.sin(2 * np.pi * x + tau)
        source = z(np.log(rho + EPS))
        flow = z(J)
        response = z(0.55 * source + 0.35 * flow + 0.15 * np.sin(3 * np.pi * x + tau))
        hist.append(dict(x=x, rho=rho.copy(), source=source, flow=flow, J=J, response=response))

        if t < T - 1:
            rho = np.maximum(rho - 0.12 * grad(J, x) + 0.01 * rng.normal(size=N), EPS)
            rho = rho / np.mean(rho)

    return hist


def transform_history(hist, mode: str, seed: int, N: int, T: int):
    rng = np.random.default_rng(seed)
    h = [{k: np.array(v, copy=True) for k, v in s.items()} for s in hist]

    if mode == "legitimate_transport":
        pass

    elif mode == "identity_matched_response_scramble":
        # preserves rho/J/source identity and momentum, breaks response closure
        for s in h:
            s["response"] = z(np.roll(s["response"], N // 4) + 0.25 * rng.normal(size=N))

    elif mode == "identity_matched_nonlinear_response":
        for s in h:
            s["response"] = z(np.tanh(1.8 * s["response"]) + 0.35 * np.sin(9 * np.pi * s["x"]))

    elif mode == "identity_matched_spectral_response":
        for s in h:
            s["response"] = z(s["response"] + 0.45 * np.sin(13 * np.pi * s["x"]) + 0.25 * np.cos(17 * np.pi * s["x"]))

    elif mode == "identity_matched_lagged_response":
        for s in h:
            s["response"] = z(np.roll(s["response"], N // 6) + 0.15 * np.roll(s["source"], -N // 7))

    elif mode == "identity_matched_flow_phase_warp":
        for s in h:
            warp = 0.18 * np.sin(9 * np.pi * s["x"] + 0.3)
            s["flow"] = z(s["flow"] + warp)
            s["J"] = z(s["J"] + warp)

    elif mode == "identity_matched_current_flip":
        for s in h:
            mask = (s["x"] > 0.35) & (s["x"] < 0.58)
            s["J"][mask] *= -1
            s["flow"] = z(s["J"])

    elif mode == "identity_matched_local_spike":
        for s in h:
            spike = np.exp(-120 * (s["x"] - 0.52) ** 2)
            s["source"] = z(s["source"] + 0.10 * spike)
            s["rho"] = np.exp(s["source"])
            s["rho"] /= np.mean(s["rho"])
            s["flow"] = z(s["flow"] - 0.08 * spike)
            s["J"] = s["flow"]

    elif mode == "source_shuffle":
        for s in h:
            s["source"] = z(rng.permutation(s["source"]))
            s["rho"] = np.exp(s["source"])
            s["rho"] /= np.mean(s["rho"])

    elif mode == "time_reverse":
        h = list(reversed(h))

    else:
        raise ValueError(mode)

    return h


def closure_residual_slice(s, N):
    y = z(s["response"])
    X = np.c_[np.ones(N), z(s["source"]), z(s["flow"])]
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return rms(y - X @ beta)


def momentum_residual(hist, N, T):
    vals = []
    for t in range(T - 1):
        vals.append(rms(z(hist[t + 1]["rho"] - hist[t]["rho"]) + z(grad(hist[t]["J"], hist[t]["x"]))))
    return float(np.mean(vals))


def identity_residual(hist, ref, T):
    return float(np.mean([1 - cosine(hist[t][k], ref[t][k]) for t in range(T) for k in ["rho", "J", "source"]]))


def source_path_residual(hist, T):
    return float(np.std([rms(z(hist[t + 1]["source"] - hist[t]["source"])) for t in range(T - 1)]))


def raw_diag(hist, ref, N, T):
    return {
        "closure": float(np.mean([closure_residual_slice(s, N) for s in hist])),
        "momentum": momentum_residual(hist, N, T),
        "identity": max(identity_residual(hist, ref, T), 1e-12),
        "source_path": source_path_residual(hist, T),
        "repair": float(np.mean([np.mean(np.abs(lap_fast(s["response"]))) for s in hist])),
        "access_loss": float(np.mean([np.mean(1 / (s["rho"] + EPS)) for s in hist])),
    }


def retained_path(cands, w, ref, N, T):
    ret = []
    for t in range(T):
        x = ref[t]["x"]
        rho = sum(float(w[i]) * cands[i]["history"][t]["rho"] for i in range(len(cands)))
        source = sum(float(w[i]) * cands[i]["history"][t]["source"] for i in range(len(cands)))
        flow = sum(float(w[i]) * cands[i]["history"][t]["flow"] for i in range(len(cands)))
        J = sum(float(w[i]) * cands[i]["history"][t]["J"] for i in range(len(cands)))
        response = sum(float(w[i]) * cands[i]["history"][t]["response"] for i in range(len(cands)))
        ret.append(dict(x=x, rho=np.maximum(rho, EPS), source=z(source), flow=z(flow), J=J, response=z(response)))
    return ret


def downstream(ret, ref, N, T):
    final = ret[-1]
    x = final["x"]
    J_native = -grad(np.log(final["rho"] + EPS), x)
    cont = float(np.mean([rms(z(ret[t + 1]["rho"] - ret[t]["rho"]) + z(grad(ret[t]["J"], ret[t]["x"]))) for t in range(T - 1)]))
    return {
        "B_like_residual": closure_residual_slice(final, N),
        "ADM_M_residual": rms(z(J_native) - z(final["flow"])),
        "continuity_residual": cont,
        "identity_residual": identity_residual(ret, ref, T),
        "flow_coherence": float(abs(corr(J_native, final["flow"]))),
    }


def run_suite(NS=(96, 128, 160), TS=(6, 8, 10), n_cases=8):
    case_rows = []
    candidate_rows = []

    for N in NS:
        for T in TS:
            raws = []
            for i in range(5):
                ref = base_history(6900000 + N * 10 + T * 100 + i, N, T)
                raws.append(raw_diag(ref, ref, N, T))
            scales = {k: max(float(np.mean([r[k] for r in raws])), 1e-6) for k in raws[0]}

            for case in range(n_cases):
                ref = base_history(7000000 + N * 13 + T * 17 + case, N, T)
                cands = []

                for mi, mode in enumerate(BASE_MODES):
                    h = transform_history(ref, mode, 7100000 + 100 * case + mi, N, T)
                    raw = raw_diag(h, ref, N, T)
                    terms = {k: raw[k] / (scales[k] + EPS) for k in raw}
                    cands.append({"mode": mode, "history": h, "raw": raw, "terms": terms})
                    candidate_rows.append({"N": N, "T": T, "case": case, "mode": mode, "is_valid": mode == VALID, **terms})

                for regime, extra in REGIMES.items():
                    weights_def = BASE_WEIGHTS.copy()
                    weights_def.update(extra)
                    U = np.array([sum(weights_def[k] * c["terms"][k] for k in weights_def) for c in cands])
                    w = np.exp(-BETA * (U - U.min()))
                    w = w / (w.sum() + EPS)

                    winner = cands[int(np.argmax(w))]["mode"]
                    ret = retained_path(cands, w, ref, N, T)
                    dd = downstream(ret, ref, N, T)

                    valid_weight = float(sum(w[i] for i, c in enumerate(cands) if c["mode"] == VALID))
                    id_counterfeit_weight = float(sum(w[i] for i, c in enumerate(cands) if c["mode"].startswith("identity_matched")))

                    pass_counterfeit = id_counterfeit_weight < 0.05 and valid_weight > 0.95
                    pass_adm = dd["ADM_M_residual"] < 0.02 and dd["flow_coherence"] > 0.98
                    pass_closure = dd["B_like_residual"] < 0.30

                    case_rows.append({
                        "N": N,
                        "T": T,
                        "case": case,
                        "regime": regime,
                        "winner": winner,
                        "valid_winner": winner == VALID,
                        "valid_weight": valid_weight,
                        "identity_counterfeit_weight": id_counterfeit_weight,
                        "pass_counterfeit": pass_counterfeit,
                        "pass_adm": pass_adm,
                        "pass_closure": pass_closure,
                        "pass_all": pass_counterfeit and pass_adm and pass_closure,
                        **dd,
                    })

    df = pd.DataFrame(case_rows)
    cand = pd.DataFrame(candidate_rows)

    summary_by_regime = df.groupby("regime").agg(
        valid_winner_rate=("valid_winner", "mean"),
        mean_valid_weight=("valid_weight", "mean"),
        mean_identity_counterfeit_weight=("identity_counterfeit_weight", "mean"),
        counterfeit_pass_rate=("pass_counterfeit", "mean"),
        adm_pass_rate=("pass_adm", "mean"),
        closure_pass_rate=("pass_closure", "mean"),
        all_pass_rate=("pass_all", "mean"),
        mean_B_like_residual=("B_like_residual", "mean"),
        mean_ADM_M_residual=("ADM_M_residual", "mean"),
        mean_flow_coherence=("flow_coherence", "mean"),
    ).reset_index()

    by_scale = df.groupby(["regime", "N", "T"]).agg(
        all_pass_rate=("pass_all", "mean"),
        mean_valid_weight=("valid_weight", "mean"),
        mean_identity_counterfeit_weight=("identity_counterfeit_weight", "mean"),
        mean_B_like_residual=("B_like_residual", "mean"),
        mean_ADM_M_residual=("ADM_M_residual", "mean"),
    ).reset_index()

    candidate_summary = cand.groupby("mode").agg(
        mean_identity=("identity", "mean"),
        mean_closure=("closure", "mean"),
        mean_momentum=("momentum", "mean"),
    ).reset_index()

    min_row = summary_by_regime[summary_by_regime.regime == "identity_plus_closure"].iloc[0]
    summary = {
        "document_id": "V1312_1_CLEAN_ROOM_EVIDENCE_HARNESS",
        "status": "completed",
        "claim_under_test": "identity + closure minimal sufficiency inside synthetic transport simulations",
        "identity_plus_closure": {
            "valid_winner_rate": float(min_row.valid_winner_rate),
            "mean_valid_weight": float(min_row.mean_valid_weight),
            "mean_identity_counterfeit_weight": float(min_row.mean_identity_counterfeit_weight),
            "counterfeit_pass_rate": float(min_row.counterfeit_pass_rate),
            "adm_pass_rate": float(min_row.adm_pass_rate),
            "closure_pass_rate": float(min_row.closure_pass_rate),
            "all_pass_rate": float(min_row.all_pass_rate),
            "mean_B_like_residual": float(min_row.mean_B_like_residual),
            "mean_ADM_M_residual": float(min_row.mean_ADM_M_residual),
            "mean_flow_coherence": float(min_row.mean_flow_coherence),
        },
        "review_attack_points_supported_by_outputs": [
            "identity leakage: compare identity_only vs identity_plus_closure",
            "closure tautology: compare closure_only, identity_only, and identity_plus_closure",
            "counterfeit diversity: inspect candidate_summary and candidate_terms",
            "ADM_M dependence: compare ADM_M pass in identity_only, identity_plus_momentum, identity_plus_closure",
            "scaling: inspect by_scale",
            "minimality: inspect summary_by_regime"
        ],
        "not_claimed": [
            "physical GR",
            "Einstein equations",
            "full ADM derivation",
            "physical spacetime curvature",
            "universal law beyond tested simulations"
        ],
    }

    df.to_csv(OUT / "v1312_1_case_diagnostics.csv", index=False)
    cand.to_csv(OUT / "v1312_1_candidate_terms.csv", index=False)
    summary_by_regime.to_csv(OUT / "v1312_1_summary_by_regime.csv", index=False)
    by_scale.to_csv(OUT / "v1312_1_by_scale.csv", index=False)
    candidate_summary.to_csv(OUT / "v1312_1_candidate_summary.csv", index=False)
    (OUT / "v1312_1_summary.json").write_text(json.dumps(summary, indent=2))

    report = f"""# V1312.1 — Clean-Room Evidence Harness Report

## Status

Completed.

## Claim Under Test

```text
identity + closure is a scaled, adversarially tested minimal sufficient stack
inside synthetic transport simulations.
```

## Summary by Regime

{summary_by_regime.to_markdown(index=False)}

## Candidate Summary

{candidate_summary.to_markdown(index=False)}

## Scale Summary

{by_scale.to_markdown(index=False)}

## Auditor Use

Use these outputs to attack:

```text
identity leakage
closure tautology
counterfeit diversity
ADM_M diagnostic dependence
scaling limits
minimality
```

## Boundary

This does not claim physical GR, Einstein equations, full ADM derivation, or physical spacetime curvature.
"""
    (OUT / "V1312_1_CLEAN_ROOM_EVIDENCE_HARNESS_REPORT.md").write_text(report)

    return summary


if __name__ == "__main__":
    summary = run_suite()
    print(json.dumps(summary, indent=2))
