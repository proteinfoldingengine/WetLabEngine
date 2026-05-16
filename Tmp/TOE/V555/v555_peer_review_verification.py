"""
V555 Peer Review Verification Script
====================================

Purpose
-------
This is the peer-review version of the V549/V553/V554 verification stack.

It does not generate a report first.
It generates evidence.

It runs two audits:

1. Full-stack selective-fragility audit
   - admissible transformations should survive with wobble
   - principle-breaking attacks should fail
   - checks geometry, weak form, mu_defect, B_t liquidity, repair burden, C accounting, V accounting

2. Hardened defect-localization audit
   - specifically tests the prior weak point: scrambled/nonlocal defects
   - checks support overlap, centroid drift, defect weak contribution, and mass error

Interpretation boundary
-----------------------
This is synthetic adversarial evidence for a theorem-shaped model.
It is not a completed mathematical proof and not a physical-law claim.

Run
---
pip install numpy pandas matplotlib scikit-learn
python v555_peer_review_verification.py

Outputs
-------
v555_peer_review_outputs/
    v555_full_stack_results.csv
    v555_full_stack_aggregate.csv
    v555_defect_results.csv
    v555_defect_aggregate.csv
    v555_summary.json
    RESULTS.md
    plots
"""

from pathlib import Path
import json, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score

OUT = Path("v555_peer_review_outputs")
OUT.mkdir(exist_ok=True)
EPS = 1e-9


# ==========================================================
# Shared helpers
# ==========================================================
def norm(A):
    return (A - A.min()) / (A.max() - A.min() + EPS)

def smooth(A):
    P = np.pad(A, 1, mode="edge")
    return (
        P[1:-1, 1:-1] + P[:-2, 1:-1] + P[2:, 1:-1] +
        P[1:-1, :-2] + P[1:-1, 2:]
    ) / 5.0

def lap(A, dx):
    P = np.pad(A, 1, mode="edge")
    return (
        P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] +
        P[1:-1, 2:] - 4 * P[1:-1, 1:-1]
    ) / (dx * dx)

def gauss(X, Y, cx, cy, w, a):
    return a * np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * w * w))

def centroid(A, X, Y, dx):
    m = float(np.sum(A) * dx * dx)
    if m <= EPS:
        return 0.0, 0.0, 0.0
    return float(np.sum(X * A) * dx * dx / m), float(np.sum(Y * A) * dx * dx / m), m

def support_iou(A, B, q=0.90):
    ma = A > np.quantile(A, q)
    mb = B > np.quantile(B, q)
    union = np.logical_or(ma, mb).sum()
    if union == 0:
        return 1.0
    return float(np.logical_and(ma, mb).sum() / union)

def weak_residual(true_d, pred_d, X, Y, dx):
    phis = [
        np.ones_like(X),
        np.sin(np.pi * X),
        np.sin(np.pi * Y),
        np.exp(-((X - 0.55)**2 + (Y - 0.50)**2) / (2 * 0.18**2)),
    ]
    vals = []
    for phi in phis:
        truth = float(np.sum(phi * true_d) * dx * dx)
        pred = float(np.sum(phi * pred_d) * dx * dx)
        vals.append(abs(pred - truth) / (abs(truth) + EPS))
    return float(np.mean(vals))

def weighted_harmonic(etas, weights):
    etas = np.clip(etas, 1e-6, 1.0)
    return weights.sum(axis=-1) / (np.sum(weights / etas, axis=-1) + EPS)


# ==========================================================
# Full-stack selective fragility audit
# ==========================================================
def make_full_field(rng, n=88, noise=0.018):
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)
    dx = 1 / (n - 1)

    T0 = norm(
        gauss(X, Y, 0.28, 0.35, 0.08, 1.1) +
        gauss(X, Y, 0.68, 0.55, 0.10, 0.9) +
        gauss(X, Y, 0.45, 0.80, 0.06, 0.7)
    )

    seam = 0.55 + 0.08 * np.sin(8 * Y)
    Lambda0 = np.clip(0.10 + 0.90 * norm(np.exp(-((X - seam)**2) / (2 * 0.012**2))), 0, 1)
    Pi0 = np.clip(
        0.15 + 0.85 * norm(
            np.exp(-((Y - 0.50)**2) / (2 * 0.055**2)) *
            np.exp(-((X - 0.62)**2) / (2 * 0.18**2))
        ),
        0, 1
    )

    T = norm(T0 + noise * rng.normal(size=T0.shape))
    Lambda = np.clip(Lambda0 + 0.45 * noise * rng.normal(size=T0.shape), 0, 1)
    Pi = np.clip(Pi0 + 0.45 * noise * rng.normal(size=T0.shape), 0, 1)

    conductance = np.clip(1 - 0.65 * Pi - 0.35 * Lambda, 0.08, 1)
    lineage = np.clip(1 - 0.70 * Lambda, 0.05, 1)
    repair = np.clip(0.55 + 0.30 * conductance + 0.15 * lineage - 0.18 * Pi, 0.05, 1.25)
    margin = np.clip(0.62 + 0.22 * conductance - 0.20 * T - 0.14 * Pi, 0.05, 1.25)
    topology = np.clip(0.35 + 0.65 * conductance * (1 - Pi), 0.05, 1.2)
    containment = np.clip(1 - 0.75 * Pi * Lambda, 0.05, 1)

    repair_cost = (
        0.45 * T * (1 - repair) +
        0.35 * T * (1 - containment) +
        0.20 * (1 - lineage) * (1 - conductance)
    )

    etas = np.stack([conductance, lineage, topology, repair, containment], axis=-1)
    weakness = 1 - np.clip(etas, 0, 1)
    raw_w = (0.2 + weakness) * (0.4 + T[..., None])
    weights = raw_w / (raw_w.sum(axis=-1, keepdims=True) + EPS)

    eta_channel = weighted_harmonic(etas, weights)
    eta_convert = np.clip(eta_channel * np.exp(-repair_cost), 0.001, 1)

    B_nominal = np.clip(0.45 + 0.30 * conductance + 0.22 * lineage - 0.20 * Pi, 0.03, 1.25)
    B_recoverable = B_nominal * conductance * lineage * topology * containment * repair

    C = margin * repair * lineage + 0.62 * eta_convert * B_recoverable
    C_floor = np.clip(
        0.18 + 0.22 * T + 0.20 * Pi + 0.18 * Lambda +
        0.10 * np.abs(T - smooth(T)) - 0.12 * repair - 0.10 * lineage,
        0.05, 0.80
    )
    C_surplus = np.clip(C - C_floor, 0.02, None)

    return dict(
        X=X, Y=Y, dx=dx,
        T=T, Lambda=Lambda, Pi=Pi,
        conductance=conductance, lineage=lineage, repair=repair,
        margin=margin, topology=topology, containment=containment,
        repair_cost=repair_cost, eta_convert=eta_convert,
        B_recoverable=B_recoverable, B_audit_true=B_recoverable.copy(),
        C=C, C_floor=C_floor, C_surplus=C_surplus,
    )

def compute_full(F, hidden=None):
    hidden = hidden or {}
    T = hidden.get("T", F["T"])
    C_surplus = hidden.get("C_surplus", F["C_surplus"])
    Lambda = hidden.get("Lambda", F["Lambda"])
    Pi = hidden.get("Pi", F["Pi"])
    B = hidden.get("B_recoverable", F["B_recoverable"])
    B_audit = hidden.get("B_audit_true", F.get("B_audit_true", F["B_recoverable"]))
    repair_cost = hidden.get("repair_cost", F["repair_cost"])

    Source = smooth(T / (C_surplus + EPS))
    Repair = np.clip(0.28 * F["lineage"] + 0.25 * F["repair"] + 0.22 * F["conductance"], 0, 1.2)
    mu = Source * Lambda * Pi
    Omega = np.clip(1 + 0.30 * Source + 0.22 * Lambda + 0.20 * Pi - 0.22 * Repair, 0.2, 4)
    dOmega = Source - Repair - 0.45 * mu
    K = norm(np.clip(-lap(np.log(np.clip(Omega, 1e-8, None)), F["dx"]) / (Omega**2 + EPS), -1000, 1000))

    score = norm(mu)
    label = (score > np.quantile(score, 0.90)).astype(int)

    gy, gx = np.gradient(Omega, F["dx"], F["dx"])
    E = float(0.5 * np.mean(gx * gx + gy * gy) + np.mean((Source - Repair)**2))

    Cmean = float(np.mean(F["margin"] * F["repair"] * F["lineage"] + 0.62 * F["eta_convert"] * B))
    Caud = float(np.mean(F["margin"] * F["repair"] * F["lineage"] + 0.62 * F["eta_convert"] * B_audit))
    Cfloor = float(np.mean(F["C_floor"]))
    mu_mass = float(np.mean(mu))
    bottleneck = float(np.mean((1 - F["conductance"]) * score))
    repair_mean = float(np.mean(repair_cost))
    Bmean = float(np.mean(B))
    Baudit_mean = float(np.mean(B_audit))

    Bpen = abs(Bmean - Baudit_mean) / (Baudit_mean + EPS)
    V = E + 6 * max(0, Cfloor - Cmean)**2 + 2.5 * mu_mass + 2.0 * bottleneck + repair_mean + 1.5 * Bpen

    cx, cy, _ = centroid(mu, F["X"], F["Y"], F["dx"])

    return dict(
        mu=mu, Omega=Omega, dOmega=dOmega, K=K, score=score, label=label,
        V=V, mu_mass=mu_mass, Cmean=Cmean, Caud=Caud,
        Bmean=Bmean, Baudit_mean=Baudit_mean,
        repair_mean=repair_mean, cx=cx, cy=cy
    )

def make_full_scenario(F, name, sev, rng):
    obs = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in F.items()}

    if name == "clean":
        obs["T"] = norm(obs["T"] + 0.008 * rng.normal(size=obs["T"].shape))

    elif name == "coordinate_relabel":
        warp = 1 + 0.12 * sev * np.sin(2 * np.pi * F["X"]) * np.sin(2 * np.pi * F["Y"])
        obs["T"] = norm(obs["T"] * warp + 0.018 * rng.normal(size=F["T"].shape))
        obs["C_surplus"] = np.clip(obs["C_surplus"] * warp * (1 + 0.012 * rng.normal(size=F["T"].shape)), 0.02, None)

    elif name == "omega_rescale_equiv":
        scale = 1 + 0.25 * sev
        obs["T"] = obs["T"] * scale + 0.014 * rng.normal(size=F["T"].shape)
        obs["C_surplus"] = np.clip(obs["C_surplus"] * scale * (1 + 0.010 * rng.normal(size=F["T"].shape)), 0.02, None)

    elif name == "topology_preserving_smooth":
        obs["conductance"] = np.clip(
            0.74 * obs["conductance"] + 0.26 * smooth(obs["conductance"]) +
            0.010 * rng.normal(size=F["T"].shape),
            0.08, 1
        )

    elif name == "destroy_source_reserve":
        flat = obs["T"].ravel().copy()
        rng.shuffle(flat)
        obs["T"] = flat.reshape(obs["T"].shape)

    elif name == "scramble_defects":
        n = F["T"].shape[0]
        sh = max(1, int(sev * n * 0.70))
        obs["Lambda"] = np.roll(obs["Lambda"], sh, axis=1)
        obs["Pi"] = np.roll(obs["Pi"], sh // 2, axis=0)
        obs["Lambda"] = np.clip(0.55 * obs["Lambda"] + 0.45 * norm(rng.random(obs["Lambda"].shape)), 0, 1)
        obs["Pi"] = np.clip(0.55 * obs["Pi"] + 0.45 * norm(rng.random(obs["Pi"].shape)), 0, 1)

    elif name == "fake_B_liquidity":
        obs["B_recoverable"] = F["B_recoverable"] * (1 + 5.0 * sev * smooth(F["T"]) + 1.0 * sev)

    elif name == "hidden_repair_burden":
        obs["repair_cost"] = np.clip(F["repair_cost"] * (1 - 2.0 * sev * F["T"]) - 0.16 * sev, 0, None)

    elif name == "coordinated_fake_recovery":
        obs["B_recoverable"] = F["B_recoverable"] * (1 + 3.0 * sev)
        obs["repair_cost"] = np.clip(F["repair_cost"] * (1 - 1.6 * sev * F["T"]) - 0.12 * sev, 0, None)
        obs["C_surplus"] = np.clip(F["C_surplus"] * (1 + 1.4 * sev), 0.02, None)
        n = F["T"].shape[0]
        sh = max(1, int(sev * n * 0.40))
        obs["Lambda"] = np.roll(obs["Lambda"], sh, axis=1)
        obs["Pi"] = np.roll(obs["Pi"], sh // 2, axis=0)

    else:
        raise ValueError(name)

    return obs

def eval_full_once(name, sev, seed):
    rng = np.random.default_rng(seed)
    F = make_full_field(rng)
    obs = make_full_scenario(F, name, sev, rng)
    pred = compute_full(obs)
    truth = compute_full(F)

    geom = (
        1 - float(np.mean((norm(truth["dOmega"]) - norm(pred["dOmega"]))**2)) +
        1 - float(np.mean((truth["K"] - pred["K"])**2))
    ) / 2

    try:
        defect_auc = roc_auc_score(truth["label"].ravel(), pred["score"].ravel())
    except Exception:
        defect_auc = 0.5

    wr = weak_residual(truth["dOmega"], pred["dOmega"], F["X"], F["Y"], F["dx"])
    muerr = abs(pred["mu_mass"] - truth["mu_mass"]) / (abs(truth["mu_mass"]) + EPS)
    Berr = abs(pred["Bmean"] - truth["Bmean"]) / (abs(truth["Bmean"]) + EPS)
    brancherr = abs(pred["Bmean"] - pred["Baudit_mean"]) / (abs(pred["Baudit_mean"]) + EPS)
    rerr = abs(pred["repair_mean"] - truth["repair_mean"]) / (abs(truth["repair_mean"]) + EPS)
    Verr = abs(pred["V"] - truth["V"]) / (abs(truth["V"]) + EPS)
    Cerr = abs(pred["Cmean"] - truth["Cmean"]) / (abs(truth["Cmean"]) + EPS)
    Caerr = abs(pred["Cmean"] - truth["Caud"]) / (abs(truth["Caud"]) + EPS)
    centroid_drift = float(np.sqrt((pred["cx"] - truth["cx"])**2 + (pred["cy"] - truth["cy"])**2))
    support_err = 1 - support_iou(pred["mu"], truth["mu"], q=0.90)

    validity = (
        (geom + defect_auc) / 2
        - 0.25 * min(wr, 5)
        - 0.75 * min(muerr, 3)
        - 1.45 * min(Berr, 3)
        - 1.35 * min(brancherr, 3)
        - 1.75 * min(rerr, 3)
        - 0.75 * min(Verr, 3)
        - 0.80 * min(Cerr, 3)
        - 0.80 * min(Caerr, 3)
        - 2.50 * min(centroid_drift, 1)
        - 1.70 * min(support_err, 1)
    )

    return dict(
        scenario=name, severity=sev,
        geometry_consistency=geom, defect_AUC=float(defect_auc),
        weak_residual=wr, mu_error=muerr,
        B_liquidity_error=Berr, branch_audit_error=brancherr,
        repair_burden_error=rerr, V_error=Verr,
        C_error=Cerr, audited_C_error=Caerr,
        defect_centroid_drift=centroid_drift,
        defect_support_overlap_error=support_err,
        validity_score=float(validity),
    )


# ==========================================================
# Defect-only hardening audit
# ==========================================================
def make_defect_field(seed, n=80):
    r = np.random.default_rng(seed)
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)
    dx = 1 / (n - 1)
    T = norm(gauss(X, Y, 0.30, 0.35, 0.08, 1.0) + gauss(X, Y, 0.68, 0.55, 0.10, 0.9) + 0.01 * r.normal(size=(n, n)))
    seam = 0.55 + 0.08 * np.sin(8 * Y)
    Lambda = norm(np.exp(-((X - seam)**2) / (2 * 0.012**2)) + 0.003 * r.normal(size=(n, n)))
    Pi = norm(np.exp(-((Y - 0.50)**2) / (2 * 0.055**2)) * np.exp(-((X - 0.62)**2) / (2 * 0.18**2)) + 0.003 * r.normal(size=(n, n)))
    Source = smooth(T / (0.25 + 0.50 * (1 - Lambda * Pi) + EPS))
    mu = Source * Lambda * Pi
    return X, Y, dx, T, Lambda, Pi, mu

def perturb_defect(Lambda, Pi, name, sev, seed):
    r = np.random.default_rng(seed)
    if name == "clean":
        return np.clip(Lambda + 0.004 * r.normal(size=Lambda.shape), 0, 1), np.clip(Pi + 0.004 * r.normal(size=Pi.shape), 0, 1)
    if name == "admissible_smooth":
        return np.clip(0.90 * Lambda + 0.10 * smooth(Lambda) + 0.004 * r.normal(size=Lambda.shape), 0, 1), np.clip(0.90 * Pi + 0.10 * smooth(Pi) + 0.004 * r.normal(size=Pi.shape), 0, 1)
    if name == "small_jitter":
        sh = max(1, int(sev * 2))
        return np.roll(Lambda, sh, axis=1), np.roll(Pi, sh // 2, axis=0)
    if name == "scramble_defects":
        n = Lambda.shape[0]
        sh = max(1, int(sev * n * 0.75))
        L = np.roll(Lambda, sh, axis=1)
        P = np.roll(Pi, sh // 2, axis=0)
        return np.clip(0.45 * L + 0.55 * norm(r.random(Lambda.shape)), 0, 1), np.clip(0.45 * P + 0.55 * norm(r.random(Pi.shape)), 0, 1)
    if name == "nonlocal_defect_noise":
        noise = norm(r.random(Lambda.shape))
        return np.clip(0.25 * Lambda + 0.75 * noise, 0, 1), np.clip(0.25 * Pi + 0.75 * np.roll(noise, 17, axis=0), 0, 1)
    raise ValueError(name)

def defect_weak_error(true_mu, pred_mu, X, Y, dx):
    phi_support = (true_mu > np.quantile(true_mu, 0.90)).astype(float)
    phis = [np.ones_like(X), np.sin(np.pi * X), np.sin(np.pi * Y), phi_support]
    vals = []
    for phi in phis:
        t = float(np.sum(phi * true_mu) * dx * dx)
        p = float(np.sum(phi * pred_mu) * dx * dx)
        vals.append(abs(p - t) / (abs(t) + EPS))
    return float(np.mean(vals))

def support_distance(A, B, X, Y, q=0.90):
    ma = A > np.quantile(A, q)
    mb = B > np.quantile(B, q)
    if ma.sum() == 0 or mb.sum() == 0:
        return 1.0
    bx, by = float(X[mb].mean()), float(Y[mb].mean())
    return float(np.sqrt((X[ma] - bx)**2 + (Y[ma] - by)**2).mean())

def eval_defect_once(name, sev, seed):
    X, Y, dx, T, Lambda, Pi, true_mu = make_defect_field(seed)
    Lp, Pp = perturb_defect(Lambda, Pi, name, sev, seed + 777)
    pred_mu = smooth(T / (0.25 + 0.50 * (1 - Lp * Pp) + EPS)) * Lp * Pp

    true_score = norm(true_mu)
    pred_score = norm(pred_mu)
    true_label = (true_score > np.quantile(true_score, 0.90)).astype(int)

    try:
        auc = roc_auc_score(true_label.ravel(), pred_score.ravel())
    except Exception:
        auc = 0.5

    tcx, tcy, tm = centroid(true_mu, X, Y, dx)
    pcx, pcy, pm = centroid(pred_mu, X, Y, dx)

    overlap = support_iou(pred_mu, true_mu, q=0.90)
    cdrift = float(np.sqrt((pcx - tcx)**2 + (pcy - tcy)**2))
    sdist = support_distance(pred_mu, true_mu, X, Y, q=0.90)
    masserr = abs(pm - tm) / (tm + EPS)
    werr = defect_weak_error(true_mu, pred_mu, X, Y, dx)

    validity = (
        auc
        - 2.0 * (1 - overlap)
        - 3.0 * cdrift
        - 1.5 * sdist
        - 0.8 * min(masserr, 3)
        - 0.5 * min(werr, 5)
    )

    return dict(
        scenario=name, severity=sev,
        defect_AUC=float(auc), support_IoU=float(overlap),
        support_overlap_error=float(1 - overlap),
        centroid_drift=cdrift, support_distance=sdist,
        mass_error=masserr, weak_measure_error=werr,
        defect_validity=float(validity),
    )


# ==========================================================
# Main
# ==========================================================
def main():
    # Full-stack audit
    admissible = ["clean", "coordinate_relabel", "omega_rescale_equiv", "topology_preserving_smooth"]
    breaking = ["destroy_source_reserve", "scramble_defects", "fake_B_liquidity", "hidden_repair_burden", "coordinated_fake_recovery"]

    full_rows = []
    for seed_idx in range(8):
        for name in admissible + breaking:
            severities = [0.0] if name == "clean" else [0.25, 0.50, 0.75]
            for sev in severities:
                row = eval_full_once(name, sev, seed=2000 + seed_idx * 100 + int(sev * 100) + (abs(hash(name)) % 50))
                row["class"] = "admissible" if name in admissible else "principle_breaking"
                row["seed_idx"] = seed_idx
                full_rows.append(row)

    full_df = pd.DataFrame(full_rows)
    full_agg = full_df.groupby(["class", "scenario"]).mean(numeric_only=True).reset_index()
    full_auc = roc_auc_score((full_df["class"] == "admissible").astype(int), full_df["validity_score"])

    # Defect hardening audit
    defect_scenarios = ["clean", "admissible_smooth", "small_jitter", "scramble_defects", "nonlocal_defect_noise"]
    defect_rows = []
    for seed_idx in range(10):
        for name in defect_scenarios:
            severities = [0.0] if name == "clean" else ([0.15, 0.25, 0.35] if name == "small_jitter" else [0.25, 0.50, 0.75])
            for sev in severities:
                row = eval_defect_once(name, sev, seed=900 + seed_idx)
                row["class"] = "admissible" if name in ["clean", "admissible_smooth", "small_jitter"] else "principle_breaking"
                row["seed_idx"] = seed_idx
                defect_rows.append(row)

    defect_df = pd.DataFrame(defect_rows)
    defect_agg = defect_df.groupby(["class", "scenario"]).mean(numeric_only=True).reset_index()
    defect_auc = roc_auc_score((defect_df["class"] == "admissible").astype(int), defect_df["defect_validity"])

    full_weak_spots = full_agg[(full_agg["class"] == "principle_breaking") & (full_agg["validity_score"] > 0.30)][["scenario", "validity_score"]].to_dict("records")
    defect_weak_spots = defect_agg[(defect_agg["class"] == "principle_breaking") & (defect_agg["defect_validity"] > 0.30)][["scenario", "defect_validity"]].to_dict("records")

    summary = {
        "full_stack_selective_fragility_AUC": float(full_auc),
        "full_stack_mean_admissible_validity": float(full_agg[full_agg["class"] == "admissible"]["validity_score"].mean()),
        "full_stack_mean_breaking_validity": float(full_agg[full_agg["class"] == "principle_breaking"]["validity_score"].mean()),
        "full_stack_weak_spots_above_0_30": full_weak_spots,
        "defect_localization_AUC": float(defect_auc),
        "defect_mean_admissible_validity": float(defect_agg[defect_agg["class"] == "admissible"]["defect_validity"].mean()),
        "defect_mean_breaking_validity": float(defect_agg[defect_agg["class"] == "principle_breaking"]["defect_validity"].mean()),
        "defect_weak_spots_above_0_30": defect_weak_spots,
        "interpretation": "V555 combines the resolved full-stack selective-fragility audit with a stricter defect-localization hardening audit.",
    }

    full_df.to_csv(OUT / "v555_full_stack_results.csv", index=False)
    full_agg.to_csv(OUT / "v555_full_stack_aggregate.csv", index=False)
    defect_df.to_csv(OUT / "v555_defect_results.csv", index=False)
    defect_agg.to_csv(OUT / "v555_defect_aggregate.csv", index=False)

    with open(OUT / "v555_summary.json", "w") as f:
        json.dump({
            "summary": summary,
            "full_stack_aggregate": full_agg.to_dict("records"),
            "defect_aggregate": defect_agg.to_dict("records"),
        }, f, indent=2)

    # Plots
    order = full_agg.sort_values("validity_score", ascending=False)
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = ["#2ca02c" if c == "admissible" else "#d62728" for c in order["class"]]
    ax.bar(range(len(order)), order["validity_score"], color=colors)
    ax.axhline(0.30, linestyle="--", linewidth=1)
    ax.axhline(0.00, linestyle=":", linewidth=1)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order["scenario"], rotation=35, ha="right")
    ax.set_title(f"V555 full-stack selective fragility, AUC={full_auc:.3f}")
    ax.set_ylabel("validity score")
    fig.tight_layout()
    fig.savefig(OUT / "v555_full_stack_validity.png", dpi=180)
    plt.close(fig)

    order2 = defect_agg.sort_values("defect_validity", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#2ca02c" if c == "admissible" else "#d62728" for c in order2["class"]]
    ax.bar(range(len(order2)), order2["defect_validity"], color=colors)
    ax.axhline(0.30, linestyle="--", linewidth=1)
    ax.axhline(0.00, linestyle=":", linewidth=1)
    ax.set_xticks(range(len(order2)))
    ax.set_xticklabels(order2["scenario"], rotation=30, ha="right")
    ax.set_title(f"V555 defect-localization hardening, AUC={defect_auc:.3f}")
    ax.set_ylabel("defect validity")
    fig.tight_layout()
    fig.savefig(OUT / "v555_defect_validity.png", dpi=180)
    plt.close(fig)

    md = "# V555 Peer Review Verification Results\n\n"
    md += "## Summary\n\n"
    md += pd.DataFrame([summary]).to_markdown(index=False)
    md += "\n\n## Full-stack aggregate\n\n"
    md += full_agg.to_markdown(index=False)
    md += "\n\n## Defect-localization aggregate\n\n"
    md += defect_agg.to_markdown(index=False)
    (OUT / "RESULTS.md").write_text(md)

    zip_path = Path("v555_peer_review_outputs.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            z.write(p, arcname=p.relative_to(OUT))

    print("=== V555 PEER REVIEW SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {v}")

    print("\nFull-stack aggregate:")
    print(full_agg.to_string(index=False))

    print("\nDefect aggregate:")
    print(defect_agg.to_string(index=False))

    print("\nOutputs:", OUT.resolve())
    print("Zip:", zip_path.resolve())


if __name__ == "__main__":
    main()
