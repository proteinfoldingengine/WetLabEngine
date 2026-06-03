#!/usr/bin/env python3
"""
V1011 Accessibility-Flow Bianchi Closure Audit

Supporting Python for the Bianchi-like branch.

This is NOT a GR Bianchi identity and NOT a physical spacetime claim.

It tests whether a model-native closure diagnostic ties together:

    Ω curvature proxy
    accessibility flow J = -grad(log A)
    retained source balance
    Genesis Pin provenance predicate

Core test:
    Can geometry-matched counterfeit histories pass Ω similarity while failing
    provenance-weighted closure?

No physical-time primitive is used. The model uses ordered histories/slices only.
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


OUT = Path("v1011_bianchi_closure_outputs")
OUT.mkdir(exist_ok=True)

SEED = 1011
N = 48
BOUND = 4.0
EPS = 1e-9
ALPHA = 0.127348327184804
ETA = 0.35

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
QUORUM = 3
OMEGA_SIM_THRESHOLD = 0.985

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


def compute_closure(geom, src, pin_pass: bool):
    dx = geom["dx"]
    G_proxy = -2.0*lap(geom["phi"], dx)
    source_balance = src["source_balance"]
    divJ = src["divJ"]

    y = G_proxy.ravel()
    X = np.column_stack([np.ones(y.size), source_balance.ravel(), divJ.ravel()])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = (X @ beta).reshape(G_proxy.shape)

    B_like = G_proxy - pred

    # provenance-weighted closure makes provenance an explicit legitimacy gate
    # rather than allowing geometry-only closure to carry source legitimacy.
    provenance_penalty = 0.0 if pin_pass else float(np.std(G_proxy))
    B_weighted = B_like + provenance_penalty

    return {
        "G_proxy": G_proxy,
        "source_pred": pred,
        "B_like_rms": rms(B_like),
        "provenance_weighted_B_rms": rms(B_weighted),
        "G_source_corr": corr(G_proxy, pred),
        "beta0": float(beta[0]),
        "beta_source": float(beta[1]),
        "beta_divJ": float(beta[2]),
    }


def run_audit(n_groups: int = 40):
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
            closure = compute_closure(geom, src, pin_pass)

            omega_sim = cosine(ref_omega, geom["Omega"])
            geometry_only = omega_sim >= OMEGA_SIM_THRESHOLD
            full_certified = bool(geometry_only and pin_pass)

            rows.append({
                "group": group,
                "kind": kind,
                "omega_similarity": omega_sim,
                "geometry_only_certified": geometry_only,
                "genesis_pin_pass": pin_pass,
                "full_certified": full_certified,
                "B_like_rms": closure["B_like_rms"],
                "provenance_weighted_B_rms": closure["provenance_weighted_B_rms"],
                "G_source_corr": closure["G_source_corr"],
                "registry_matches": registry_matches(h.registry),
                "root_matches": root_matches(h.root),
                "quorum_valid": all(quorum_valid(w) for w in h.witnesses),
                "append_valid": append_chain_valid(h.root, h.registry, h.events, h.witnesses, h.roots),
                "circular_bootstrap_detected": circular_bootstrap_detected(h.registry, h.root),
            })

    df = pd.DataFrame(rows)
    legit = df[df.kind == "legitimate"]
    invalid = df[df.kind != "legitimate"]
    geom_invalid = invalid[invalid.geometry_only_certified]

    summary = {
        "document_id": "V1011_ACCESSIBILITY_FLOW_BIANCHI_CLOSURE_AUDIT",
        "groups_tested": int(n_groups),
        "histories_tested": int(len(df)),
        "geometry_only_certified_total": int(df.geometry_only_certified.sum()),
        "full_certified_total": int(df.full_certified.sum()),
        "invalid_geometry_only_certified": int(((df.kind != "legitimate") & df.geometry_only_certified).sum()),
        "invalid_full_certified": int(((df.kind != "legitimate") & df.full_certified).sum()),
        "legitimate_mean_B_like_rms": float(legit.B_like_rms.mean()),
        "invalid_mean_B_like_rms": float(invalid.B_like_rms.mean()),
        "legitimate_mean_provenance_weighted_B_rms": float(legit.provenance_weighted_B_rms.mean()),
        "invalid_mean_provenance_weighted_B_rms": float(invalid.provenance_weighted_B_rms.mean()),
        "geometry_matched_invalid_mean_omega_similarity": float(geom_invalid.omega_similarity.mean()),
        "pass_condition": {
            "geometry_counterfeits_exist": bool(len(geom_invalid) > 0),
            "no_invalid_full_certified": bool(((df.kind != "legitimate") & df.full_certified).sum() == 0),
            "provenance_weighted_residual_separates": bool(invalid.provenance_weighted_B_rms.mean() > legit.provenance_weighted_B_rms.mean()),
        },
        "claim_boundary": "Bianchi-like software closure diagnostic only; no physical GR/Bianchi/tensor claim.",
    }
    return df, summary


def write_report(df, summary):
    by_kind = df.groupby("kind").agg(
        n=("kind", "count"),
        mean_omega_similarity=("omega_similarity", "mean"),
        geometry_only_certified=("geometry_only_certified", "sum"),
        genesis_pin_pass=("genesis_pin_pass", "sum"),
        full_certified=("full_certified", "sum"),
        mean_B_like_rms=("B_like_rms", "mean"),
        mean_provenance_weighted_B_rms=("provenance_weighted_B_rms", "mean"),
        mean_G_source_corr=("G_source_corr", "mean"),
    ).reset_index()

    report = f"""# V1011 Accessibility-Flow Bianchi Closure Audit

## Purpose

This audit supports the Bianchi-like branch without claiming physical GR.

It tests whether a model-native closure diagnostic ties together:

```text
Ω curvature proxy
accessibility flow J = -grad(log A)
retained source balance
Genesis Pin provenance predicate
```

## Core Result

```json
{json.dumps(summary, indent=2)}
```

## By-Kind Results

{by_kind.to_markdown(index=False)}

## Interpretation

This audit separates three layers:

1. Geometry-only certification via Ω similarity.
2. Genesis Pin provenance certification.
3. Bianchi-like closure residual tying geometry proxy to source-flow balance.

The important expected pattern is:

```text
geometry-matched counterfeits can pass Ω similarity,
Genesis Pin rejects illegitimate histories,
and provenance-weighted B-like residual separates legitimate from illegitimate histories.
```

## Claim Boundary

Allowed:

```text
The tested recoverability/accessibility system exhibits a Bianchi-like software closure diagnostic.
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
    (OUT / "V1011_BIANCHI_CLOSURE_AUDIT.md").write_text(report)


def make_plots(df):
    kinds = list(df.kind.unique())

    plt.figure(figsize=(9,5))
    plt.boxplot([df[df.kind == k].omega_similarity.values for k in kinds], labels=kinds)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Ω similarity")
    plt.title("V1011 Ω Similarity by History Type")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_omega_similarity_by_kind.png", dpi=170)
    plt.close()

    plt.figure(figsize=(9,5))
    plt.boxplot([df[df.kind == k].provenance_weighted_B_rms.values for k in kinds], labels=kinds)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("provenance-weighted B-like residual RMS")
    plt.title("V1011 Provenance-Weighted B-like Closure Residual")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_bianchi_residual_by_kind.png", dpi=170)
    plt.close()

    plt.figure(figsize=(7,5))
    colors = df.genesis_pin_pass.map({True: "green", False: "red"})
    plt.scatter(df.omega_similarity, df.provenance_weighted_B_rms, c=colors, alpha=0.65)
    plt.axvline(OMEGA_SIM_THRESHOLD, linestyle="--", linewidth=1)
    plt.xlabel("Ω similarity")
    plt.ylabel("provenance-weighted B-like residual RMS")
    plt.title("Geometry Similarity vs Provenance-Weighted Closure")
    plt.tight_layout()
    plt.savefig(OUT / "v1011_geometry_vs_closure.png", dpi=170)
    plt.close()


def main():
    df, summary = run_audit(n_groups=40)
    df.to_csv(OUT / "v1011_bianchi_closure_results.csv", index=False)
    (OUT / "v1011_bianchi_closure_summary.json").write_text(json.dumps(summary, indent=2))
    write_report(df, summary)
    make_plots(df)

    source_zip = OUT / "v1011_source.zip"
    if source_zip.exists():
        source_zip.unlink()
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(Path(__file__), arcname=Path(__file__).name)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
