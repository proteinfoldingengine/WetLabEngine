#!/usr/bin/env python3
"""
V1150 blind replication scaffold.

Rules:
- Do not load prior scored CSV outputs.
- Rebuild generator and scoring from the written specification.
- Freeze pass/fail criteria before executing.
- Keep claims model-native.
"""

from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd

OUT = Path("v1151_independent_rebuild_outputs")
OUT.mkdir(exist_ok=True)

SEED = 1151
rng = np.random.default_rng(SEED)

RESOLUTIONS = [32, 64, 128, 256, 512]
DENSITIES = ["uniform", "strong_warp", "sparse_patch"]
FAMILIES = ["base", "multiscale", "curved"]
KINDS = [
    "native",
    "label_transported_shift_C",
    "raw_shifted_C",
    "time_shuffle_C",
    "matched_cost_C",
    "source_event_shuffled_C",
    "random_envelope_C",
]
N_PER = 3
T = 6
EPS = 1e-12

PASS_FAIL = {
    "valid_recall_min": 0.95,
    "invalid_rate_max": 0.0,
    "time_shuffle_certified_max": 0,
    "matched_cost_certified_max": 0,
    "source_event_shuffled_certified_max": 0,
    "raw_shifted_cert_rate_max": 0.05,
    "certification_instability_max": 0,
}

def z(v: np.ndarray) -> np.ndarray:
    return (v - v.mean()) / (v.std() + EPS)

def warped_grid(N: int, density: str) -> np.ndarray:
    u = np.linspace(0, 1, N, endpoint=False)
    if density == "uniform":
        w = u
    elif density == "strong_warp":
        w = u + 0.14*np.sin(2*np.pi*u)/(2*np.pi) + 0.035*np.sin(6*np.pi*u)/(2*np.pi)
    elif density == "sparse_patch":
        w = u + 0.12*np.tanh(7*(u-0.55))/7
    else:
        raise ValueError(density)
    w = (w - w.min()) / (w.max() - w.min() + EPS)
    return 2*np.pi*w

def base_fields(N: int, family: str, idx: int, density: str, transport_labels: bool = False):
    x = warped_grid(N, density)
    ph0 = 0.031*idx + 0.19
    shift = max(1, N//7)
    masks = []
    for k in range(4):
        center = (k+0.5)/4*2*np.pi
        dist = np.angle(np.exp(1j*(x-center)))
        m = np.exp(-(dist**2)/(2*(0.23*np.pi)**2))
        if transport_labels:
            m = np.roll(m, shift)
        masks.append(m/(m.max()+EPS))
    base = []
    for t in range(T):
        ph = ph0 + 0.11*t
        C = 1.32 + 0.19*np.cos(x-0.35*ph) + 0.12*np.sin(7*x+0.04*t)
        if transport_labels:
            C = np.roll(C, shift)
        base.append((C, masks, x, ph))
    return base

def build_C(base, kind: str, event_id=None, amp: float = 0.0, raw_shift: bool = False):
    N = len(base[0][0])
    shift = max(1, N//7)
    Cs = []
    for t, (C, masks, x, ph) in enumerate(base):
        C = C.copy()
        local = 0.0
        if event_id is not None:
            profile = 1/(1+np.exp(-(t-1.8)))
            local = amp*(0.6+0.4*profile)

        if kind in ["native", "label_transported_shift_C", "time_shuffle_C", "raw_shifted_C"]:
            if event_id is not None:
                C += 0.42*local*np.roll(masks[event_id], -1)
            if raw_shift:
                C = np.roll(C, shift)
        elif kind == "matched_cost_C":
            C = 1.32 + 0.19*np.cos(x-0.35*ph+0.55*np.sin(2*x)) + 0.12*np.sin(7*x+0.04*t+0.35)
        elif kind == "source_event_shuffled_C":
            wrong = (event_id+2)%4 if event_id is not None else 2
            C = 1.32 + 0.19*np.cos(x-0.35*ph) + 0.12*np.sin(7*x+0.04*t)
            if event_id is not None:
                C += 0.42*local*np.roll(masks[wrong], -1)
        elif kind == "random_envelope_C":
            C = 1.32 + 0.17*rng.normal(size=N)
        else:
            raise ValueError(kind)
        Cs.append(C)

    if kind == "time_shuffle_C":
        perm = [2,0,4,1,5,3]
        Cs = [Cs[p] for p in perm]
    return Cs

def response_path(base, kind: str, raw_shift: bool = False):
    C0 = build_C(base, kind, None, 0.0, raw_shift=raw_shift)
    path = []
    solti = []
    for t in range(T):
        masks = base[t][1]
        vec = []
        margins = []
        for event_id in range(4):
            C1 = build_C(base, kind, event_id, 0.035, raw_shift=raw_shift)
            dC = z(C1[t] - C0[t])
            channels = []
            for k in range(4):
                expected = z(np.roll(masks[k], -1))
                channels.append(float(np.dot(dC, expected)/(np.linalg.norm(dC)*np.linalg.norm(expected)+EPS)))
            ch = channels[event_id]
            wrong = max([channels[k] for k in range(4) if k != event_id])
            vec.append(ch)
            margins.append(ch - wrong)
        path.append(vec)
        solti.append(np.mean(margins))
    return np.array(path), float(np.mean(solti))

def path_signature(P: np.ndarray) -> np.ndarray:
    P = (P - P.mean(axis=0, keepdims=True))/(P.std(axis=0, keepdims=True)+EPS)
    d = np.diff(P, axis=0)
    first = d.sum(axis=0)
    areas = []
    for i in range(4):
        for j in range(i+1,4):
            areas.append(0.5*np.sum(P[:-1,i]*d[:,j] - P[:-1,j]*d[:,i]))
    adj = z(np.sum(np.abs(d), axis=1))
    return z(np.concatenate([first, np.array(areas), adj]))

def temporal_adjacency_score(P: np.ndarray, R: np.ndarray) -> float:
    P = (P - P.mean(axis=0))/(P.std(axis=0)+EPS)
    R = (R - R.mean(axis=0))/(R.std(axis=0)+EPS)
    step = np.mean(np.sum(P*R,axis=1)/(np.linalg.norm(P,axis=1)*np.linalg.norm(R,axis=1)+EPS))
    dP = np.diff(P,axis=0); dR = np.diff(R,axis=0)
    trans = np.mean(np.sum(dP*dR,axis=1)/(np.linalg.norm(dP,axis=1)*np.linalg.norm(dR,axis=1)+EPS))
    return float(0.5*step + 0.5*trans)

def canonicalize(P: np.ndarray, R: np.ndarray):
    bestP = P
    best = -1e9
    rot = 0
    for r in range(4):
        Pr = np.roll(P, r, axis=1)
        sc = np.sum(Pr*R)
        if sc > best:
            best = sc
            bestP = Pr
            rot = r
    return bestP, rot

def score_case(N: int, family: str, idx: int, density: str, kind: str):
    if kind == "label_transported_shift_C":
        ref_base = base_fields(N, family, idx, density, transport_labels=True)
        P, solti = response_path(ref_base, kind, raw_shift=False)
        R, _ = response_path(ref_base, "native", raw_shift=False)
    elif kind == "raw_shifted_C":
        ref_base = base_fields(N, family, idx, density, transport_labels=False)
        P, solti = response_path(ref_base, kind, raw_shift=True)
        R, _ = response_path(ref_base, "native", raw_shift=False)
    else:
        ref_base = base_fields(N, family, idx, density, transport_labels=False)
        P, solti = response_path(ref_base, kind, raw_shift=False)
        R, _ = response_path(ref_base, "native", raw_shift=False)

    Pc, rot = canonicalize(P, R)
    sig = path_signature(Pc)
    rsig = path_signature(R)
    sigsim = float(np.dot(sig, rsig)/(np.linalg.norm(sig)*np.linalg.norm(rsig)+EPS))
    adj = temporal_adjacency_score(Pc, R)
    scrsi = 0.55*sigsim + 0.45*adj
    joint = solti*max(0, scrsi)
    return solti, sigsim, adj, scrsi, joint, rot

def main():
    rows = []
    for N in RESOLUTIONS:
        for density in DENSITIES:
            for family in FAMILIES:
                for idx in range(N_PER):
                    for kind in KINDS:
                        solti, sigsim, adj, scrsi, joint, rot = score_case(N, family, idx, density, kind)
                        rows.append({
                            "N": N, "density": density, "family": family, "idx": idx, "kind": kind,
                            "valid_equiv": kind in ["native", "label_transported_shift_C"],
                            "solti_score": solti, "sig_similarity": sigsim,
                            "temporal_adjacency": adj, "scrsi_score": scrsi,
                            "joint_score": joint, "canonical_rotation": rot,
                        })
    df = pd.DataFrame(rows)

    scored = []
    for keys, g in df.groupby(["N","density","family"]):
        inv = g[~g.valid_equiv]
        val = g[g.valid_equiv]
        inv_max = float(inv.joint_score.max())
        val_med = float(val.joint_score.median())
        scale = max(abs(val_med-inv_max), 1e-9)
        gg = g.copy()
        gg["dimless_margin"] = (gg.joint_score - inv_max)/scale
        gg["certified"] = gg.dimless_margin > 1e-6
        scored.append(gg)
    out = pd.concat(scored, ignore_index=True)

    valid = out[out.valid_equiv]
    invalid = out[~out.valid_equiv]
    summary = {
        "valid_recall": float(valid.certified.mean()),
        "invalid_rate": float(invalid.certified.mean()),
        "invalid_certified": int(invalid.certified.sum()),
        "native_rate": float(out[out.kind=="native"].certified.mean()),
        "label_transported_shift_rate": float(out[out.kind=="label_transported_shift_C"].certified.mean()),
        "raw_shifted_rate": float(out[out.kind=="raw_shifted_C"].certified.mean()),
        "time_shuffle_certified": int(out[out.kind=="time_shuffle_C"].certified.sum()),
        "matched_cost_certified": int(out[out.kind=="matched_cost_C"].certified.sum()),
        "source_event_shuffled_certified": int(out[out.kind=="source_event_shuffled_C"].certified.sum()),
        "pass_fail": PASS_FAIL,
    }

    summary["passed"] = (
        summary["valid_recall"] >= PASS_FAIL["valid_recall_min"] and
        summary["invalid_rate"] <= PASS_FAIL["invalid_rate_max"] and
        summary["time_shuffle_certified"] <= PASS_FAIL["time_shuffle_certified_max"] and
        summary["matched_cost_certified"] <= PASS_FAIL["matched_cost_certified_max"] and
        summary["source_event_shuffled_certified"] <= PASS_FAIL["source_event_shuffled_certified_max"] and
        summary["raw_shifted_rate"] < PASS_FAIL["raw_shifted_cert_rate_max"]
    )

    out.to_csv(OUT/"all_results.csv", index=False)
    out.groupby(["N","valid_equiv"]).certified.mean().reset_index().to_csv(OUT/"scale_sweep_by_N.csv", index=False)
    out.groupby(["kind"]).certified.mean().reset_index().to_csv(OUT/"by_kind.csv", index=False)
    (OUT/"summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
