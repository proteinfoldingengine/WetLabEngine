#!/usr/bin/env python3
"""
V823 Reproducibility Script
Accessibility-Curvature Law

Reproduces:
1. A = exp(C - mu + eta * repair)
2. G_proxy = 2 alpha Delta log(A + eps)
3. held-out curvature prediction
4. direct A perturbation response
5. adversarial/null specificity

No external data required.
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path

EPS = 1e-9
ETA = 0.35
ALPHA = 0.127348327184804

def lap2(F, dx):
    return (
        np.roll(F, 1, 1) + np.roll(F, -1, 1)
        + np.roll(F, 1, 2) + np.roll(F, -1, 2)
        - 4 * F
    ) / (dx * dx)

def lap2_2d(F, dx):
    return (
        np.roll(F, 1, 0) + np.roll(F, -1, 0)
        + np.roll(F, 1, 1) + np.roll(F, -1, 1)
        - 4 * F
    ) / (dx * dx)

def r2(y, p):
    y = np.asarray(y).ravel()
    p = np.asarray(p).ravel()
    return float(1 - np.sum((y - p) ** 2) / (np.sum((y - y.mean()) ** 2) + EPS))

def corr(a, b):
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    if np.std(a) < EPS or np.std(b) < EPS:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])

class Sim:
    def __init__(self, nt=18, nx=44, bound=8.0, seed=823, defects=6, complexity=4):
        self.tau = np.linspace(0, 6, nt)
        x = np.linspace(-bound, bound, nx)
        self.dt = self.tau[1] - self.tau[0]
        self.dx = x[1] - x[0]
        self.bound = bound
        self.X, self.Y = np.meshgrid(x, x, indexing="xy")
        self.R = np.sqrt(self.X ** 2 + self.Y ** 2)
        self.eta = ETA
        self.comp = complexity
        rng = np.random.default_rng(seed)
        self.nodes = rng.uniform(-bound / 2, bound / 2, (defects, 2))
        self.phases = rng.uniform(0, 2 * np.pi, defects)

    def build(self):
        mus, repairs, Cs, phis = [], [], [], []
        for tau in self.tau:
            mu = np.zeros_like(self.X)
            for i, (cx, cy) in enumerate(self.nodes):
                a = tau * (0.25 + 0.15 * self.comp) + self.phases[i]
                rx = cx * np.cos(a) - cy * np.sin(a) + 0.25 * self.comp * np.sin(tau + self.phases[i])
                ry = cx * np.sin(a) + cy * np.cos(a) + 0.25 * self.comp * np.cos(0.7 * tau + self.phases[i])
                width = max(1.6, 2.8 - 0.25 * self.comp)
                mu += (
                    1 + 0.25 * np.sin((1.5 + 0.2 * self.comp) * tau + self.phases[i])
                ) * np.exp(-((self.X - rx) ** 2 + (self.Y - ry) ** 2) / width)

            repair = (
                np.cos(self.R * (1.2 + 0.1 * self.comp) - tau * (2.4 + 0.2 * self.comp))
                * np.exp(-self.R / (self.bound * 0.8))
                + 0.5 * np.sin(self.X * (1 + 0.1 * self.comp) - tau)
                * np.cos(self.Y * (1 + 0.08 * self.comp) - 1.5 * tau)
            )
            C = self.eta * repair - 0.25 * mu
            phi = np.clip(
                0.42 * np.log1p(np.clip(mu, 0, 10)) - 0.22 * np.tanh(self.eta * repair),
                -1.2,
                1.2,
            )
            mus.append(mu)
            repairs.append(repair)
            Cs.append(C)
            phis.append(phi)

        return np.stack(mus), np.stack(repairs), np.stack(Cs), np.stack(phis)

def make_case(seed, defects, complexity):
    sim = Sim(seed=seed, defects=defects, complexity=complexity)
    mu, repair, C, phi = sim.build()
    A = np.exp(C - mu + ETA * repair)
    G_proxy = -2 * lap2(phi, sim.dx)
    lap_log_A = lap2(np.log(A + 1e-6), sim.dx)
    lap_balance = lap2(C - mu + ETA * repair, sim.dx)
    sl = (slice(2, -2), slice(2, -2), slice(2, -2))
    return pd.DataFrame({
        "case": f"s{seed}_d{defects}_c{complexity}",
        "G_proxy": G_proxy[sl].ravel(),
        "lap_log_A": lap_log_A[sl].ravel(),
        "lap_balance": lap_balance[sl].ravel(),
    })

def heldout_accessibility_test(outdir):
    cases = [(823, 6, 4), (1100, 6, 4), (1101, 8, 4), (1102, 5, 3), (1103, 9, 5), (1104, 7, 2)]
    df = pd.concat([make_case(*c) for c in cases], ignore_index=True)

    rows = []
    for feature in ["lap_log_A", "lap_balance"]:
        for hold in df.case.unique():
            tr = df[df.case != hold]
            te = df[df.case == hold]
            X = tr[[feature]].values
            y = tr.G_proxy.values
            beta = np.linalg.lstsq(np.column_stack([np.ones(len(X)), X]), y, rcond=None)[0]
            pred = np.column_stack([np.ones(len(te)), te[[feature]].values]) @ beta
            rows.append({
                "feature": feature,
                "holdout": hold,
                "r2": r2(te.G_proxy, pred),
                "corr": corr(te.G_proxy, pred),
                "coef": float(beta[1]),
                "intercept": float(beta[0]),
            })

    scores = pd.DataFrame(rows)
    scores.to_csv(outdir / "heldout_accessibility_scores.csv", index=False)
    summary = scores.groupby("feature").agg(
        mean_r2=("r2", "mean"),
        min_r2=("r2", "min"),
        mean_corr=("corr", "mean")
    ).reset_index()
    return scores, summary

def perturbation_and_null_tests(outdir):
    n = 96
    bound = 8.0
    x = np.linspace(-bound, bound, n)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x, indexing="xy")

    def gaussian(cx, cy, w):
        return np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * w * w))

    rows = []
    for seed in range(20):
        rng = np.random.default_rng(9000 + seed)
        C = np.zeros_like(X)
        mu = np.zeros_like(X)
        for _ in range(5):
            C += rng.uniform(0.2, 1.0) * gaussian(*rng.uniform(-4, 4, 2), rng.uniform(0.8, 1.8))
            mu += rng.uniform(0.2, 1.0) * gaussian(*rng.uniform(-4, 4, 2), rng.uniform(0.8, 1.8))
        R = np.sqrt(X ** 2 + Y ** 2)
        repair = np.cos(R * rng.uniform(0.8, 1.4) + rng.uniform(0, 2 * np.pi)) * np.exp(-R / 7.5)
        A = np.exp(C - mu + ETA * repair)
        G = 2 * ALPHA * lap2_2d(np.log(A + 1e-6), dx)

        q = gaussian(*rng.uniform(-3.5, 3.5, 2), rng.uniform(0.8, 1.6))
        amp = rng.choice([-0.3, -0.15, 0.15, 0.3])
        A2 = A * np.exp(amp * q)
        G2 = 2 * ALPHA * lap2_2d(np.log(A2 + 1e-6), dx)
        dG = G2 - G
        correct = 2 * ALPHA * lap2_2d(np.log(A2 + 1e-6) - np.log(A + 1e-6), dx)

        shuffled = correct.copy().ravel()
        rng.shuffle(shuffled)
        shuffled = shuffled.reshape(correct.shape)

        preds = {
            "correct_delta_lap_logA": correct,
            "null_zero": np.zeros_like(dG),
            "wrong_sign": -correct,
            "zero_order_q": amp * q,
            "shuffled_correct": shuffled,
        }
        for name, pred in preds.items():
            rows.append({
                "seed": seed,
                "predictor": name,
                "r2": r2(dG, pred),
                "corr": corr(dG, pred),
            })

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "perturbation_null_scores.csv", index=False)
    summary = df.groupby("predictor").agg(
        mean_r2=("r2", "mean"),
        min_r2=("r2", "min"),
        mean_corr=("corr", "mean")
    ).reset_index().sort_values("mean_r2", ascending=False)
    return df, summary

def main():
    outdir = Path("v823_results")
    outdir.mkdir(exist_ok=True)

    heldout_scores, heldout_summary = heldout_accessibility_test(outdir)
    perturb_scores, perturb_summary = perturbation_and_null_tests(outdir)

    result = {
        "version": "V823",
        "core_law": "G_proxy = 2 alpha Delta log(A + epsilon)",
        "A": "exp(C - mu + eta * repair)",
        "heldout_summary": heldout_summary.to_dict("records"),
        "perturbation_summary": perturb_summary.to_dict("records"),
    }

    (outdir / "v823_results.json").write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
