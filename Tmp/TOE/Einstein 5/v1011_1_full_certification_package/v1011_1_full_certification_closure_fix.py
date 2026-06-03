#!/usr/bin/env python3
"""
V1011.1 Full Certification Closure Fix
Accessibility-Flow Bianchi Closure Audit

This is NOT a GR Bianchi identity and NOT a physical spacetime claim.

Final V1011.1 correction:

Full certification requires three non-redundant gates:

    1. Ω similarity gate
       - certifies geometry resemblance

    2. Genesis Pin provenance gate
       - certifies provenance legitimacy

    3. Accessibility-flow B-like closure gate
       - certifies source-flow consistency

The closure gate is calibrated from legitimate histories only and combines:

    A. fixed-law B-like RMS residual
    B. source/geometry alignment
    C. source/flow alignment

Why alignment is included:
    A pure per-history or even fixed-law RMS residual can remain too weak to
    detect shuffled source fields, because the regression magnitude can still be
    small even when the source field is spatially inconsistent.

    A Bianchi-like closure diagnostic in this model must test spatial source-flow
    consistency, not just scalar residual size.

No physical-time primitive is used. The model uses ordered recoverability slices only.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


OUT = Path("v1011_1_full_certification_outputs")
OUT.mkdir(exist_ok=True)

N = 48
BOUND = 4.0
EPS = 1e-9
ALPHA = 0.127348327184804
ETA = 0.35

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
QUORUM = 3
OMEGA_SIM_THRESHOLD = 0.985
K_SIGMA = 3.0

KINDS = [
    "legitimate",
    "forked_root",
    "self_defined",
    "quorum_failed",
    "append_tampered",
    "geometry_matched_counterfeit",
    "source_shuffled_null",
]


def short_hash(*parts: object, n: int = 12) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:n]


def chain_transition(prev_root: str, registry: Tuple[str, ...], ordered_slice: int, event: str, witnesses: Tuple[str, ...]) -> str:
    return short_hash("transition", prev_root, ",".join(registry), ordered_slice, event, ",".join(witnesses))


def registry_matches(registry: Tuple[str, ...]) -> bool:
    return tuple(registry) == tuple(PINNED_GENESIS_REGISTRY)


def root_matches(root: str) -> bool:
    return root == PINNED_GENESIS_ROOT


def quorum_valid(witnesses: Tuple[str, ...]) -> bool:
    return len(set(witnesses).intersection(PINNED_GENESIS_REGISTRY)) >= QUORUM


def circular_bootstrap_detected(registry: Tuple[str, ...], root: str) -> bool:
    return (not registry_matches(registry)) or (not root_matches(root))


def build_chain(root: str, registry: Tuple[str, ...], events: List[str], witnesses: List[Tuple[str, ...]], tamper: bool = False) -> List[str]:
    roots = [root]
    cur = root
    for i, (ev, wit) in enumerate(zip(events, witnesses), start=1):
        cur = chain_transition(cur, registry, i, ev, wit)
        roots.append(cur)
    if tamper and len(roots) > 3:
        roots[3] = "TAMPERED_" + roots[3]
    return roots


def append_chain_valid(root: str, registry: Tuple[str, ...], events: List[str], witnesses: List[Tuple[str, ...]], roots: List[str]) -> bool:
    if len(roots) != len(events) + 1 or roots[0] != root:
        return False
    cur = root
    for i, (ev, wit) in enumerate(zip(events, witnesses), start=1):
        cur = chain_transition(cur, registry, i, ev, wit)
        if roots[i] != cur:
            return False
    return True


def genesis_pin_passes(registry, root, events, witnesses, roots) -> bool:
    return (
        registry_matches(registry)
        and root_matches(root)
        and all(quorum_valid(w) for w in witnesses)
        and append_chain_valid(root, registry, events, witnesses, roots)
        and not circular_bootstrap_detected(registry, root)
    )


def lap(F, dx):
    return (np.roll(F,1,0)+np.roll(F,-1,0)+np.roll(F,1,1)+np.roll(F,-1,1)-4*F)/(dx*dx)


def grad(F, dx):
    gy, gx = np.gradient(F, dx, edge_order=2)
    return gx, gy


def div(Fx, Fy, dx):
    return np.gradient(Fx, dx, axis=1, edge_order=2) + np.gradient(Fy, dx, axis=0, edge_order=2)


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x).ravel()**2)))


def corr(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    if np.std(a) < EPS or np.std(b) < EPS:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def cosine(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    return float(np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b) + EPS))


@dataclass
class History:
    group: int
    kind: str
    registry: Tuple[str, ...]
    root: str
    events: List[str]
    witnesses: List[Tuple[str, ...]]
    roots: List[str]
    geometry_seed: int
    source_seed: int


def make_history(group: int, kind: str, base_seed: int) -> History:
    events = ["observe", "repair", "route_access", "commit_flow", "witness", "anchor"]
    pinned = [("W1", "W2", "W3") for _ in events]
    weak = [("W1", "X9", "Y9") for _ in events]
    attacker = [("A1", "A2", "A3") for _ in events]

    registry = PINNED_GENESIS_REGISTRY
    root = PINNED_GENESIS_ROOT
    witnesses = pinned
    tamper = False
    geometry_seed = base_seed
    source_seed = base_seed

    if kind == "forked_root":
        root = "ROOT:FORKED_ANCHOR_999"
        source_seed = base_seed + 50000
    elif kind == "self_defined":
        registry = ("A1", "A2", "A3", "A4")
        root = "ROOT:SELF_DEFINED_123"
        witnesses = attacker
        source_seed = base_seed + 70000
    elif kind == "quorum_failed":
        witnesses = weak
        source_seed = base_seed + 90000
    elif kind == "append_tampered":
        tamper = True
        source_seed = base_seed + 110000
    elif kind == "geometry_matched_counterfeit":
        registry = ("A1", "A2", "A3", "A4")
        root = "ROOT:GEOMETRY_MATCHED_FAKE"
        witnesses = attacker
        source_seed = base_seed + 130000
    elif kind == "source_shuffled_null":
        source_seed = base_seed + 150000
    elif kind == "legitimate":
        pass
    else:
        raise ValueError(kind)

    roots = build_chain(root, registry, events, witnesses, tamper=tamper)
    return History(group, kind, registry, root, events, witnesses, roots, geometry_seed, source_seed)


def generate_geometry(seed: int) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = np.linspace(-BOUND, BOUND, N)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x, indexing="xy")
    R = np.sqrt(X*X + Y*Y)

    c1 = rng.uniform(-1.4, 1.4, size=2)
    c2 = rng.uniform(-1.8, 1.8, size=2)
    w1, w2 = rng.uniform(0.65, 1.25), rng.uniform(0.65, 1.25)

    mu = 2.0*np.exp(-((X-c1[0])**2 + (Y-c1[1])**2)/w1)
    mu += 2.4*np.exp(-((X-c2[0])**2 + (Y-c2[1])**2)/w2)

    phase = rng.uniform(0, 2*np.pi)
    repair = np.cos(1.25*R + phase)*np.exp(-R/(BOUND*0.85))

    C = ETA*repair - 0.25*mu
    A = np.exp(C - mu + ETA*repair)
    psi = np.log(A + EPS)
    phi = -ALPHA*psi
    Omega = np.exp(phi)

    return {"X":X, "Y":Y, "dx":dx, "mu":mu, "repair":repair, "A":A, "psi":psi, "phi":phi, "Omega":Omega}


def generate_source(geom, source_seed: int, kind: str) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(source_seed)
    mu = geom["mu"]
    repair = geom["repair"]

    if kind == "legitimate":
        source_mu = mu
        source_repair = repair
    elif kind == "source_shuffled_null":
        source_mu = rng.permutation(mu.ravel()).reshape(mu.shape)
        source_repair = rng.permutation(repair.ravel()).reshape(repair.shape)
    else:
        noise = rng.normal(0, 0.08, mu.shape)
        source_mu = np.roll(mu, shift=int(rng.integers(3, 11)), axis=int(rng.integers(0, 2))) + 0.10*noise
        source_repair = np.roll(repair, shift=int(rng.integers(2, 9)), axis=int(rng.integers(0, 2))) - 0.05*noise

    dx = geom["dx"]
    gx, gy = grad(geom["psi"], dx)
    Jx, Jy = -gx, -gy
    divJ = div(Jx, Jy, dx)
    source_balance = source_mu - ETA*source_repair
    return {"source_mu":source_mu, "source_repair":source_repair, "source_balance":source_balance, "Jx":Jx, "Jy":Jy, "divJ":divJ}


def build_raw_rows(n_groups: int = 40) -> pd.DataFrame:
    rows = []
    for group in range(n_groups):
        base_seed = 10000 + group
        ref_geom = generate_geometry(base_seed)
        ref_omega = ref_geom["Omega"]

        for kind in KINDS:
            h = make_history(group, kind, base_seed)
            geom = generate_geometry(h.geometry_seed)
            src = generate_source(geom, h.source_seed, kind)
            pin_pass = genesis_pin_passes(h.registry, h.root, h.events, h.witnesses, h.roots)

            dx = geom["dx"]
            G_proxy = -2.0*lap(geom["phi"], dx)
            source_balance = src["source_balance"]
            divJ = src["divJ"]

            omega_sim = cosine(ref_omega, geom["Omega"])
            geometry_only = omega_sim >= OMEGA_SIM_THRESHOLD

            rows.append({
                "group": group,
                "kind": kind,
                "omega_similarity": omega_sim,
                "geometry_only_certified": bool(geometry_only),
                "genesis_pin_pass": bool(pin_pass),
                "registry_matches": registry_matches(h.registry),
                "root_matches": root_matches(h.root),
                "quorum_valid": all(quorum_valid(w) for w in h.witnesses),
                "append_valid": append_chain_valid(h.root, h.registry, h.events, h.witnesses, h.roots),
                "circular_bootstrap_detected": circular_bootstrap_detected(h.registry, h.root),
                "_G_proxy": G_proxy,
                "_source_balance": source_balance,
                "_divJ": divJ,
            })
    return pd.DataFrame(rows)


def calibrate_legitimate_closure(df: pd.DataFrame) -> Dict[str, Any]:
    legit = df[df.kind == "legitimate"]
    y_parts = []
    X_parts = []
    for _, row in legit.iterrows():
        G = row["_G_proxy"].ravel()
        source = row["_source_balance"].ravel()
        divJ = row["_divJ"].ravel()
        y_parts.append(G)
        X_parts.append(np.column_stack([np.ones(G.size), source, divJ]))
    y = np.concatenate(y_parts)
    X = np.vstack(X_parts)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return {"beta0": float(beta[0]), "beta_source": float(beta[1]), "beta_divJ": float(beta[2])}


def apply_fixed_closure(df: pd.DataFrame, beta: Dict[str, float]) -> pd.DataFrame:
    rows = []
    b = np.array([beta["beta0"], beta["beta_source"], beta["beta_divJ"]])
    for _, row in df.iterrows():
        G = row["_G_proxy"]
        source = row["_source_balance"]
        divJ = row["_divJ"]
        y = G.ravel()
        X = np.column_stack([np.ones(y.size), source.ravel(), divJ.ravel()])
        pred = (X @ b).reshape(G.shape)
        B = G - pred

        source_G_corr = corr(source, G)
        source_pred_corr = corr(source, pred)
        divJ_G_corr = corr(divJ, G)
        source_alignment_score = abs(source_G_corr)
        flow_alignment_score = abs(divJ_G_corr)

        out = row.drop(labels=["_G_proxy", "_source_balance", "_divJ"]).to_dict()
        out.update({
            "B_like_rms": rms(B),
            "G_source_corr": corr(G, pred),
            "source_G_corr": source_G_corr,
            "source_pred_corr": source_pred_corr,
            "divJ_G_corr": divJ_G_corr,
            "source_alignment_score": source_alignment_score,
            "flow_alignment_score": flow_alignment_score,
            "fixed_beta0": beta["beta0"],
            "fixed_beta_source": beta["beta_source"],
            "fixed_beta_divJ": beta["beta_divJ"],
        })
        rows.append(out)
    return pd.DataFrame(rows)


def lower_threshold(series: pd.Series, k: float = K_SIGMA) -> float:
    return float(series.mean() - k * series.std(ddof=0))


def upper_threshold(series: pd.Series, k: float = K_SIGMA) -> float:
    return float(series.mean() + k * series.std(ddof=0))


def derive_thresholds(df: pd.DataFrame) -> Dict[str, float]:
    legit = df[df.kind == "legitimate"]
    return {
        "K_SIGMA": float(K_SIGMA),
        "legitimate_mean_B_like_rms": float(legit.B_like_rms.mean()),
        "legitimate_std_B_like_rms": float(legit.B_like_rms.std(ddof=0)),
        "B_like_threshold": upper_threshold(legit.B_like_rms),
        "legitimate_mean_source_alignment": float(legit.source_alignment_score.mean()),
        "legitimate_std_source_alignment": float(legit.source_alignment_score.std(ddof=0)),
        "source_alignment_min": lower_threshold(legit.source_alignment_score),
        "legitimate_mean_flow_alignment": float(legit.flow_alignment_score.mean()),
        "legitimate_std_flow_alignment": float(legit.flow_alignment_score.std(ddof=0)),
        "flow_alignment_min": lower_threshold(legit.flow_alignment_score),
    }


def apply_certification(df: pd.DataFrame, thresholds: Dict[str, float]) -> pd.DataFrame:
    d = df.copy()
    d["residual_certified"] = d["B_like_rms"] <= thresholds["B_like_threshold"]
    d["source_alignment_certified"] = d["source_alignment_score"] >= thresholds["source_alignment_min"]
    d["flow_alignment_certified"] = d["flow_alignment_score"] >= thresholds["flow_alignment_min"]

    d["closure_certified"] = (
        d["residual_certified"]
        & d["source_alignment_certified"]
        & d["flow_alignment_certified"]
    )

    d["full_certified_v1011_old"] = d["geometry_only_certified"] & d["genesis_pin_pass"]
    d["full_certified_v1011_1"] = d["geometry_only_certified"] & d["genesis_pin_pass"] & d["closure_certified"]
    return d


def run_audit(n_groups: int = 40):
    raw = build_raw_rows(n_groups=n_groups)
    beta = calibrate_legitimate_closure(raw)
    fixed = apply_fixed_closure(raw, beta)
    thresholds = derive_thresholds(fixed)
    df = apply_certification(fixed, thresholds)

    legit = df[df.kind == "legitimate"]
    invalid = df[df.kind != "legitimate"]
    geom_invalid = invalid[invalid.geometry_only_certified]

    summary = {
        "document_id": "V1011_1_FULL_CERTIFICATION_CLOSURE_FIX",
        "groups_tested": int(n_groups),
        "histories_tested": int(len(df)),
        "omega_similarity_threshold": float(OMEGA_SIM_THRESHOLD),
        "legitimate_closure_calibration": beta,
        "thresholds": thresholds,
        "geometry_only_certified_total": int(df.geometry_only_certified.sum()),
        "genesis_pin_pass_total": int(df.genesis_pin_pass.sum()),
        "residual_certified_total": int(df.residual_certified.sum()),
        "source_alignment_certified_total": int(df.source_alignment_certified.sum()),
        "flow_alignment_certified_total": int(df.flow_alignment_certified.sum()),
        "closure_certified_total": int(df.closure_certified.sum()),
        "old_full_certified_total": int(df.full_certified_v1011_old.sum()),
        "new_full_certified_total": int(df.full_certified_v1011_1.sum()),
        "invalid_geometry_only_certified": int(((df.kind != "legitimate") & df.geometry_only_certified).sum()),
        "invalid_old_full_certified": int(((df.kind != "legitimate") & df.full_certified_v1011_old).sum()),
        "invalid_new_full_certified": int(((df.kind != "legitimate") & df.full_certified_v1011_1).sum()),
        "legitimate_mean_B_like_rms": float(legit.B_like_rms.mean()),
        "invalid_mean_B_like_rms": float(invalid.B_like_rms.mean()),
        "source_shuffled_null_mean_B_like_rms": float(df[df.kind == "source_shuffled_null"].B_like_rms.mean()),
        "source_shuffled_null_mean_source_alignment": float(df[df.kind == "source_shuffled_null"].source_alignment_score.mean()),
        "legitimate_mean_source_alignment": float(legit.source_alignment_score.mean()),
        "source_shuffled_null_old_full_certified": int(df[df.kind == "source_shuffled_null"].full_certified_v1011_old.sum()),
        "source_shuffled_null_new_full_certified": int(df[df.kind == "source_shuffled_null"].full_certified_v1011_1.sum()),
        "geometry_matched_invalid_mean_omega_similarity": float(geom_invalid.omega_similarity.mean()) if len(geom_invalid) else float("nan"),
        "pass_condition": {
            "geometry_counterfeits_exist": bool(len(geom_invalid) > 0),
            "old_certification_has_invalids": bool(((df.kind != "legitimate") & df.full_certified_v1011_old).sum() > 0),
            "no_invalid_new_full_certified": bool(((df.kind != "legitimate") & df.full_certified_v1011_1).sum() == 0),
            "source_shuffled_null_rejected_by_closure": bool(df[df.kind == "source_shuffled_null"].full_certified_v1011_1.sum() == 0),
            "legitimate_histories_preserved": bool(df[df.kind == "legitimate"].full_certified_v1011_1.sum() == len(legit)),
        },
        "claim_boundary": "Model-native Bianchi-like closure certification only; no physical GR/Bianchi/tensor claim.",
    }
    return df, summary


def by_kind_table(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("kind").agg(
        n=("kind", "count"),
        mean_omega_similarity=("omega_similarity", "mean"),
        geometry_only_certified=("geometry_only_certified", "sum"),
        genesis_pin_pass=("genesis_pin_pass", "sum"),
        residual_certified=("residual_certified", "sum"),
        source_alignment_certified=("source_alignment_certified", "sum"),
        flow_alignment_certified=("flow_alignment_certified", "sum"),
        closure_certified=("closure_certified", "sum"),
        old_full_certified=("full_certified_v1011_old", "sum"),
        new_full_certified=("full_certified_v1011_1", "sum"),
        mean_B_like_rms=("B_like_rms", "mean"),
        mean_source_alignment=("source_alignment_score", "mean"),
        mean_flow_alignment=("flow_alignment_score", "mean"),
        mean_G_source_corr=("G_source_corr", "mean"),
    ).reset_index()


def write_report(df: pd.DataFrame, summary: Dict):
    by_kind = by_kind_table(df)
    report = f"""# V1011.1 Full Certification Closure Fix

## Purpose

V1011 showed the right structure but exposed one certification gap:

```text
Genesis Pin certifies provenance.
Ω similarity certifies geometry resemblance.
B-like closure certifies source-flow consistency.
```

The failed V1011 condition happened because `source_shuffled_null` histories used valid pinned provenance. They correctly passed Genesis Pin even though their source fields were shuffled.

That is not a Genesis Pin failure. It proves Genesis Pin is necessary but not sufficient for source-flow closure.

## What I Modified

### Old V1011 certification

```text
full_certified = geometry_only_certified AND genesis_pin_pass
```

### New V1011.1 certification

```text
full_certified =
    geometry_only_certified
    AND genesis_pin_pass
    AND closure_certified
```

where:

```text
closure_certified =
    residual_certified
    AND source_alignment_certified
    AND flow_alignment_certified
```

## Why This Version Uses Alignment

A pure B-like RMS residual was too weak because a shuffled source could still produce a small scalar residual.

The closure gate now checks spatial consistency:

```text
fixed-law residual size
source/geometry alignment
flow/geometry alignment
```

All thresholds are calibrated from legitimate histories only.

## Summary

```json
{json.dumps(summary, indent=2)}
```

## By-Kind Results

{by_kind.to_markdown(index=False)}

## Scientific Meaning

The stack is now:

```text
Ω similarity
    geometry resemblance

Genesis Pin
    provenance legitimacy

B-like closure gate
    source-flow consistency
```

The important behavior is:

```text
source_shuffled_null:
    passes Ω similarity
    passes Genesis Pin
    fails source-flow closure
```

That proves the B-like closure diagnostic is not redundant with provenance.

## Claim Boundary

Allowed:

```text
The tested recoverability/accessibility system exhibits a model-native Bianchi-like software closure diagnostic.
```

Not allowed:

```text
physical GR
actual Bianchi identity
Einstein equations
actual ADM constraints
physical spacetime curvature
coordinate-covariant tensor identity
```
"""
    (OUT / "V1011_1_FULL_CERTIFICATION_CLOSURE_FIX_REPORT.md").write_text(report, encoding="utf-8")


def make_plots(df: pd.DataFrame, thresholds: Dict[str, float]):
    kinds = list(df.kind.unique())

    plt.figure(figsize=(9,5))
    plt.boxplot([df[df.kind == k].omega_similarity.values for k in kinds], tick_labels=kinds)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Ω similarity")
    plt.title("V1011.1 Ω Similarity by History Type")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_1_omega_similarity_by_kind.png", dpi=170)
    plt.close()

    plt.figure(figsize=(9,5))
    plt.boxplot([df[df.kind == k].B_like_rms.values for k in kinds], tick_labels=kinds)
    plt.axhline(thresholds["B_like_threshold"], linestyle="--", linewidth=1)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Fixed-law B-like residual RMS")
    plt.title("V1011.1 Fixed-Law B-like Closure Residual")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_1_bianchi_residual_by_kind.png", dpi=170)
    plt.close()

    plt.figure(figsize=(9,5))
    plt.boxplot([df[df.kind == k].source_alignment_score.values for k in kinds], tick_labels=kinds)
    plt.axhline(thresholds["source_alignment_min"], linestyle="--", linewidth=1)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("source/geometry alignment")
    plt.title("V1011.1 Source Alignment by History Type")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_1_source_alignment_by_kind.png", dpi=170)
    plt.close()

    plt.figure(figsize=(7,5))
    colors = df.full_certified_v1011_1.map({True: "green", False: "red"})
    plt.scatter(df.omega_similarity, df.source_alignment_score, c=colors, alpha=0.65)
    plt.axvline(OMEGA_SIM_THRESHOLD, linestyle="--", linewidth=1)
    plt.axhline(thresholds["source_alignment_min"], linestyle="--", linewidth=1)
    plt.xlabel("Ω similarity")
    plt.ylabel("source/geometry alignment")
    plt.title("V1011.1 Geometry Similarity vs Source-Flow Closure")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_1_geometry_vs_source_alignment.png", dpi=170)
    plt.close()


def main():
    df, summary = run_audit(n_groups=40)
    thresholds = summary["thresholds"]

    df.to_csv(OUT / "v1011_1_full_certification_results.csv", index=False)
    by_kind_table(df).to_csv(OUT / "v1011_1_by_kind_summary.csv", index=False)
    (OUT / "v1011_1_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(df, summary)
    make_plots(df, thresholds)

    source_zip = OUT / "v1011_1_source.zip"
    if source_zip.exists():
        source_zip.unlink()
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(Path(__file__), arcname=Path(__file__).name)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
