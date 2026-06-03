#!/usr/bin/env python3
"""
V1215 — Clean-Room Supported-Bridge Replication Harness

Replicates the narrow V1214 supported claim:

    path-certified admissibility
    -> closure pressure
    -> retained source-flow coherence
    -> B-like closure propagation

This script intentionally does NOT attempt to prove:
    - physical GR
    - Einstein equations
    - full ADM-like H/M recovery

Required replication targets:
    1. Closure-necessity result
    2. Anti-tautology result using held-out closure metrics
"""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("v1215_clean_room_supported_bridge_outputs")
OUT.mkdir(exist_ok=True)

SEED = 1215
EPS = 1e-12
N = 256
T = 9
N_CASES = 36
BETA = 3.0

MODES = [
    "legitimate_admissible",
    "raw_shift",
    "source_shuffle",
    "retained_order_shuffle",
    "valid_prefix_invalid_suffix",
    "geometry_matched_counterfeit",
    "provenance_valid_source_flow_shuffled",
]
VALID = {"legitimate_admissible"}

REGIMES = {
    "no_closure_pressure": 0.0,
    "closure_pressure": 1.5,
}

BASE_WEIGHTS = {
    "source_inconsistency": 1.0,
    "retained_order_inconsistency": 1.0,
    "repair_cost": 0.05,
    "accessibility_loss": 0.05,
}


def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / (x.std() + EPS)


def corr(a, b):
    if np.std(a) < EPS or np.std(b) < EPS:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def cosine(a, b):
    a = np.ravel(a)
    b = np.ravel(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + EPS))


def grad(f, x):
    return np.gradient(f, x)


def lap(f, x):
    return np.gradient(np.gradient(f, x), x)


def base_history(seed):
    r = np.random.default_rng(seed)
    x = np.linspace(0, 1, N)
    source0 = z(np.sin(2 * np.pi * x + r.uniform(-0.2, 0.2)) + 0.35 * np.cos(5 * np.pi * x) + 0.05 * r.normal(size=N))
    hist = []
    for t in range(T):
        tau = t / (T - 1)
        source = z(source0 + 0.15 * tau * np.sin(2 * np.pi * (x + 0.1 * tau)) + 0.02 * r.normal(size=N))
        flow = z(-grad(np.log(np.exp(-0.25 * source) + EPS), x) + 0.15 * np.sin(3 * np.pi * x + tau))
        accessibility = np.exp(0.45 * source - 0.25 * np.abs(flow))
        response = z(0.55 * source + 0.25 * flow + 0.20 * np.sin(2 * np.pi * x + tau))
        hist.append(dict(x=x, source=source, flow=flow, accessibility=accessibility, response=response))
    return hist


def transform_history(hist, mode, seed):
    r = np.random.default_rng(seed)
    h = [{k: np.array(v, copy=True) for k, v in s.items()} for s in hist]

    if mode == "legitimate_admissible":
        pass
    elif mode == "raw_shift":
        for s in h:
            s["response"] = z(np.roll(s["response"], N // 8))
            s["accessibility"] = np.roll(s["accessibility"], N // 8)
    elif mode == "source_shuffle":
        for s in h:
            s["source"] = z(r.permutation(s["source"]))
            s["flow"] = z(r.permutation(s["flow"]))
    elif mode == "retained_order_shuffle":
        h = list(reversed(h))
    elif mode == "valid_prefix_invalid_suffix":
        for s in h[T // 2:]:
            s["source"] = z(np.roll(s["source"], N // 5))
            s["flow"] = z(np.roll(s["flow"], N // 7))
    elif mode == "geometry_matched_counterfeit":
        for s in h:
            s["response"] = z(s["response"] + 0.01 * r.normal(size=N))
            s["source"] = z(np.roll(s["source"], N // 4))
            s["flow"] = z(-0.5 * s["flow"] + 0.25 * np.sin(7 * np.pi * s["x"]))
    elif mode == "provenance_valid_source_flow_shuffled":
        for s in h:
            s["source"] = z(np.roll(s["source"], N // 3))
            s["flow"] = z(np.roll(s["flow"], N // 6))
    else:
        raise ValueError(mode)

    for s in h:
        s["accessibility"] = np.exp(0.45 * s["source"] - 0.25 * np.abs(s["flow"]))
    return h


def training_linear_closure(s):
    y = z(s["response"])
    X = np.c_[np.ones(N), z(s["source"]), z(s["flow"])]
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(np.sqrt(np.mean((y - X @ beta) ** 2)))


def nonlinear_closure(s):
    y = z(s["response"])
    src = z(s["source"])
    fl = z(s["flow"])
    X = np.c_[np.ones(N), src, fl, src * fl, src**2, fl**2]
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(np.sqrt(np.mean((y - X @ beta) ** 2)))


def spectral_closure(s, k=12):
    y = z(s["response"])
    src = z(s["source"])
    fl = z(s["flow"])
    fy = np.fft.rfft(y)[:k]
    fs = np.fft.rfft(src)[:k]
    ff = np.fft.rfft(fl)[:k]
    X = np.c_[np.ones(k), fs.real, fs.imag, ff.real, ff.imag]
    beta_r = np.linalg.lstsq(X, fy.real, rcond=None)[0]
    beta_i = np.linalg.lstsq(X, fy.imag, rcond=None)[0]
    pred = X @ beta_r + 1j * (X @ beta_i)
    return float(np.sqrt(np.mean(np.abs(fy - pred) ** 2)))


def derivative_closure(s):
    x = s["x"]
    dy = z(grad(s["response"], x))
    ds = z(grad(s["source"], x))
    df = z(grad(s["flow"], x))
    X = np.c_[np.ones(N), ds, df]
    beta = np.linalg.lstsq(X, dy, rcond=None)[0]
    return float(np.sqrt(np.mean((dy - X @ beta) ** 2)))


def lagged_closure(s):
    y = z(s["response"])
    src = z(s["source"])
    fl = z(s["flow"])
    X = np.c_[np.ones(N), src, fl, np.roll(src, 1), np.roll(src, -1), np.roll(fl, 1), np.roll(fl, -1)]
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(np.sqrt(np.mean((y - X @ beta) ** 2)))


def mutual_proxy_closure(s):
    y = z(s["response"])
    src = z(s["source"])
    fl = z(s["flow"])
    score = abs(corr(y, src)) + abs(corr(y, fl)) + abs(corr(grad(y, s["x"]), fl))
    return float(3.0 - score)


def closure_vector(s):
    return {
        "training_linear_closure": training_linear_closure(s),
        "heldout_nonlinear_closure": nonlinear_closure(s),
        "heldout_spectral_closure": spectral_closure(s),
        "heldout_derivative_closure": derivative_closure(s),
        "heldout_lagged_closure": lagged_closure(s),
        "heldout_mutual_proxy_closure": mutual_proxy_closure(s),
    }


def path_signature(hist):
    sig = []
    for t in range(1, len(hist)):
        a = hist[t - 1]
        b = hist[t]
        ds = z(b["source"] - a["source"])
        df = z(b["flow"] - a["flow"])
        da = z(np.log(b["accessibility"] + EPS) - np.log(a["accessibility"] + EPS))
        dr = z(b["response"] - a["response"])
        sig += [
            cosine(ds, df),
            cosine(ds, da),
            cosine(df, da),
            cosine(da, dr),
            np.linalg.norm(ds) / np.sqrt(N),
            np.linalg.norm(df) / np.sqrt(N),
            np.linalg.norm(da) / np.sqrt(N),
        ]
    return np.array(sig)


def calibrate():
    sigs = []
    Bs = []
    for i in range(80):
        h = base_history(500000 + i)
        sigs.append(path_signature(h))
        Bs.append(np.mean([training_linear_closure(s) for s in h]))
    return np.array(sigs).mean(axis=0), float(np.mean(Bs))


def terms(hist, center, B_mean):
    Bs = []
    repairs = []
    access = []
    orders = []
    for t, s in enumerate(hist):
        Bs.append(training_linear_closure(s))
        repairs.append(float(np.mean(np.abs(lap(s["response"], s["x"])))))
        access.append(float(np.mean(1 / (s["accessibility"] + EPS))))
        if t > 0:
            orders.append(float(np.linalg.norm(s["source"] - hist[t - 1]["source"]) / np.sqrt(N)))
    sig = path_signature(hist)
    return {
        "source_inconsistency": float(np.linalg.norm(sig - center) / (np.linalg.norm(center) + EPS)),
        "retained_order_inconsistency": float(np.std(orders) if orders else 0),
        "closure_imbalance": float(np.mean(Bs) / (B_mean + EPS)),
        "repair_cost": float(np.mean(repairs)),
        "accessibility_loss": float(np.mean(access)),
    }


def downstream(A, S, F, R, x):
    s = dict(x=x, source=z(S), flow=z(F), response=z(R), accessibility=np.maximum(A, EPS))
    vals = closure_vector(s)
    vals.update({
        "source_flow_alignment": float(corr(s["source"], s["response"]) + corr(s["flow"], grad(s["response"], x))),
        "flow_coherence": float(abs(corr(-grad(np.log(s["accessibility"] + EPS), x), s["flow"]))),
    })
    return vals


def run():
    center, B_mean = calibrate()
    rows = []
    weights_rows = []

    for case in range(N_CASES):
        base = base_history(600000 + case)
        candidates = []
        for mi, mode in enumerate(MODES):
            h = transform_history(base, mode, 700000 + 100 * case + mi)
            candidates.append({"mode": mode, "history": h, **terms(h, center, B_mean)})

        for regime, closure_weight in REGIMES.items():
            weights = BASE_WEIGHTS.copy()
            weights["closure_imbalance"] = closure_weight
            U = np.array([sum(weights[k] * c[k] for k in weights) for c in candidates])
            w = np.exp(-BETA * (U - U.min()))
            w = w / (w.sum() + EPS)

            x = base[-1]["x"]
            A = sum(float(w[i]) * candidates[i]["history"][-1]["accessibility"] for i in range(len(candidates)))
            S = sum(float(w[i]) * candidates[i]["history"][-1]["source"] for i in range(len(candidates)))
            F = sum(float(w[i]) * candidates[i]["history"][-1]["flow"] for i in range(len(candidates)))
            R = sum(float(w[i]) * candidates[i]["history"][-1]["response"] for i in range(len(candidates)))

            winner = candidates[int(np.argmax(w))]["mode"]
            valid_weight = float(sum(w[i] for i, c in enumerate(candidates) if c["mode"] in VALID))
            diag = downstream(A, S, F, R, x)

            rows.append({
                "case": case,
                "regime": regime,
                "closure_weight": closure_weight,
                "valid_weight": valid_weight,
                "winner": winner,
                "valid_winner": winner in VALID,
                **diag,
            })

            for i, c in enumerate(candidates):
                weights_rows.append({
                    "case": case,
                    "regime": regime,
                    "mode": c["mode"],
                    "expected_valid": c["mode"] in VALID,
                    "weight": float(w[i]),
                    "U": float(U[i]),
                })

    df = pd.DataFrame(rows)
    weights_df = pd.DataFrame(weights_rows)

    summary_by_regime = df.groupby("regime").agg(
        mean_valid_weight=("valid_weight", "mean"),
        valid_winner_rate=("valid_winner", "mean"),
        mean_training_linear_closure=("training_linear_closure", "mean"),
        mean_heldout_nonlinear_closure=("heldout_nonlinear_closure", "mean"),
        mean_heldout_spectral_closure=("heldout_spectral_closure", "mean"),
        mean_heldout_derivative_closure=("heldout_derivative_closure", "mean"),
        mean_heldout_lagged_closure=("heldout_lagged_closure", "mean"),
        mean_heldout_mutual_proxy_closure=("heldout_mutual_proxy_closure", "mean"),
        mean_source_flow_alignment=("source_flow_alignment", "mean"),
        mean_flow_coherence=("flow_coherence", "mean"),
    ).reset_index()

    no = summary_by_regime[summary_by_regime.regime == "no_closure_pressure"].iloc[0]
    cl = summary_by_regime[summary_by_regime.regime == "closure_pressure"].iloc[0]
    deltas = {
        "delta_valid_weight": float(cl.mean_valid_weight - no.mean_valid_weight),
        "delta_valid_winner_rate": float(cl.valid_winner_rate - no.valid_winner_rate),
        "delta_training_linear_closure": float(cl.mean_training_linear_closure - no.mean_training_linear_closure),
        "delta_heldout_nonlinear_closure": float(cl.mean_heldout_nonlinear_closure - no.mean_heldout_nonlinear_closure),
        "delta_heldout_spectral_closure": float(cl.mean_heldout_spectral_closure - no.mean_heldout_spectral_closure),
        "delta_heldout_derivative_closure": float(cl.mean_heldout_derivative_closure - no.mean_heldout_derivative_closure),
        "delta_heldout_lagged_closure": float(cl.mean_heldout_lagged_closure - no.mean_heldout_lagged_closure),
        "delta_heldout_mutual_proxy_closure": float(cl.mean_heldout_mutual_proxy_closure - no.mean_heldout_mutual_proxy_closure),
        "delta_source_flow_alignment": float(cl.mean_source_flow_alignment - no.mean_source_flow_alignment),
        "delta_flow_coherence": float(cl.mean_flow_coherence - no.mean_flow_coherence),
    }

    heldout_keys = [k for k in deltas if k.startswith("delta_heldout")]
    heldout_improved = {k: deltas[k] < 0 for k in heldout_keys}
    pass_result = (
        deltas["delta_valid_weight"] > 0
        and deltas["delta_valid_winner_rate"] > 0
        and all(heldout_improved.values())
        and deltas["delta_source_flow_alignment"] > 0
        and deltas["delta_flow_coherence"] > 0
    )

    summary = {
        "document_id": "V1215_CLEAN_ROOM_SUPPORTED_BRIDGE_REPLICATION",
        "status": "completed",
        "verdict": "PASS" if pass_result else "WEAK_PASS_OR_FAIL",
        "supported_claim": "closure pressure improves source-flow/B-like closure propagation inside this synthetic replication harness",
        "deltas_closure_pressure_vs_no_closure": deltas,
        "heldout_metric_improved": heldout_improved,
        "heldout_improved_count": int(sum(heldout_improved.values())),
    }

    df.to_csv(OUT / "v1215_case_diagnostics.csv", index=False)
    weights_df.to_csv(OUT / "v1215_candidate_weights.csv", index=False)
    summary_by_regime.to_csv(OUT / "v1215_summary_by_regime.csv", index=False)
    (OUT / "v1215_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
