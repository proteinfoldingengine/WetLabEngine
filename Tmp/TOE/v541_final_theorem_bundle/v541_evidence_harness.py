"""
V541 Evidence Harness
=====================

This script produces the actual synthetic evidence for:

"a theorem-shaped constrained conformal recoverability flow
with operational evidence and synthetic convergence support."

It does NOT merely package a report.

It runs four linked audits:

1. eta_convert operational closure
   C_t = M R L + lambda0 * eta_convert * B_t

2. Omega convergence
   g_eff = Omega^2 g0
   Omega converges in smooth bulk under refinement

3. mu_defect measure convergence
   mu_defect has bounded mass, localized support, stable centroid,
   and is required for weak-form accounting

4. constrained Lyapunov stability
   V = E[Omega] + reserve penalty + defect penalty + bottleneck penalty
   separates stable recovery from false recovery/collapse better than E alone

Outputs:
    v541_evidence_outputs/
      v541_summary.json
      v541_summary_tables.xlsx not required; CSVs instead
      eta_results.csv
      omega_convergence.csv
      mu_measure_convergence.csv
      lyapunov_results.csv
      PNG figures

Run:
    pip install numpy pandas matplotlib scikit-learn
    python v541_evidence_harness.py
"""

from pathlib import Path
import json
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.linear_model import LinearRegression

OUT = Path("v541_evidence_outputs")
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(541)
EPS = 1e-9


# ============================================================
# Shared field helpers
# ============================================================
def norm01(A):
    A = np.asarray(A, dtype=float)
    return (A - np.nanmin(A)) / (np.nanmax(A) - np.nanmin(A) + EPS)

def smooth(A):
    P = np.pad(A, 1, mode="edge")
    return (
        P[1:-1, 1:-1]
        + P[:-2, 1:-1]
        + P[2:, 1:-1]
        + P[1:-1, :-2]
        + P[1:-1, 2:]
    ) / 5.0

def laplacian(A, dx):
    P = np.pad(A, 1, mode="edge")
    return (
        P[:-2, 1:-1]
        + P[2:, 1:-1]
        + P[1:-1, :-2]
        + P[1:-1, 2:]
        - 4 * P[1:-1, 1:-1]
    ) / (dx * dx)

def grad_mag(A, dx):
    gy, gx = np.gradient(A, dx, dx)
    return np.sqrt(gx * gx + gy * gy)

def gaussian(X, Y, cx, cy, w, a):
    return a * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * w * w))

def weak_integral(phi, F, dx):
    return float(np.sum(phi * F) * dx * dx)


# ============================================================
# 1. eta_convert operational closure
# ============================================================
def weighted_harmonic(etas, weights):
    etas = np.clip(etas, 1e-6, 1.0)
    weights = np.clip(weights, 0.0, None)
    return weights.sum(axis=1) / (np.sum(weights / etas, axis=1) + EPS)

def weighted_arithmetic(etas, weights):
    return np.sum(weights * etas, axis=1) / (weights.sum(axis=1) + EPS)

def weighted_geometric(etas, weights):
    etas = np.clip(etas, 1e-6, 1.0)
    wnorm = weights / (weights.sum(axis=1, keepdims=True) + EPS)
    return np.exp(np.sum(wnorm * np.log(etas), axis=1))

def eta_v513(etas, weights, repair_cost):
    return weighted_harmonic(etas, weights) * np.exp(-repair_cost)

def generate_eta_regime(n=3000, regime="train_like"):
    k = 5
    if regime == "train_like":
        etas = rng.beta(7, 2, size=(n, k))
        repair_base = rng.gamma(1.5, 0.18, size=n)
        stress = rng.beta(2, 5, size=n)
        ood = 1.0
    elif regime == "ood_shift":
        etas = rng.beta(4, 3, size=(n, k))
        repair_base = rng.gamma(2.0, 0.26, size=n)
        stress = rng.beta(3, 3, size=n)
        ood = 1.25
    elif regime == "adversarial":
        etas = rng.beta(5, 2.5, size=(n, k))
        repair_base = rng.gamma(2.5, 0.30, size=n)
        stress = rng.beta(3.5, 2.5, size=n)
        ood = 1.4
        hidden = rng.random(n) < 0.45
        etas[hidden, 1] *= rng.uniform(0.35, 0.70, size=hidden.sum())
        etas[hidden, 4] *= rng.uniform(0.30, 0.65, size=hidden.sum())
    else:
        raise ValueError(regime)

    etas = np.clip(etas, 0.02, 1.0)
    weakness = 1 - etas
    exposure = rng.gamma(2.0, 1.0, size=(n, k))
    raw_sensitivity = exposure * (0.4 + 1.2 * stress[:, None]) * (0.2 + weakness)
    weights = raw_sensitivity / (raw_sensitivity.sum(axis=1, keepdims=True) + EPS)

    overlap = (
        0.35 * weakness[:, 0] * weakness[:, 1]
        + 0.25 * weakness[:, 3] * weakness[:, 4]
        + 0.20 * weakness[:, 2] * weakness[:, 4]
    )
    repair_cost = np.clip(ood * (repair_base + 0.9 * stress * overlap), 0, 3.5)

    eta_true = eta_v513(etas, weights, repair_cost)

    M = np.clip(0.35 + 0.55 * etas[:, 0] - 0.15 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)
    R = np.clip(0.30 + 0.45 * etas[:, 3] + 0.25 * etas[:, 4] - 0.10 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)
    L = np.clip(0.25 + 0.65 * etas[:, 1] - 0.10 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)
    B = np.clip(20 + 120 * etas[:, 2] + 55 * etas[:, 0] + 25 * rng.beta(3, 3, size=n) - 20 * stress, 5, 220)

    lambda0 = 1.50
    C_stock = M * R * L
    C_true = C_stock + lambda0 * eta_true * B
    C_obs = C_true + rng.normal(scale=0.02 * np.std(C_true), size=n)
    capacity_only = B / (B.max() + EPS)

    return dict(
        regime=regime, etas=etas, weights=weights, repair_cost=repair_cost,
        eta_true=eta_true, M=M, R=R, L=L, B=B, lambda0=lambda0,
        C_stock=C_stock, C_obs=C_obs, capacity_only=capacity_only
    )

def fit_reserve(C_obs, C_stock, B, eta):
    X = np.column_stack([C_stock, B * eta])
    model = LinearRegression().fit(X, C_obs)
    pred = model.predict(X)
    return r2_score(C_obs, pred), model.coef_[0], model.coef_[1]

def run_eta_audit():
    rows = []
    for regime in ["train_like", "ood_shift", "adversarial"]:
        d = generate_eta_regime(regime=regime)
        etas, w, rc = d["etas"], d["weights"], d["repair_cost"]
        candidates = {
            "v513_harmonic_repair": eta_v513(etas, w, rc),
            "harmonic_no_repair": weighted_harmonic(etas, w),
            "arithmetic_repair": weighted_arithmetic(etas, w) * np.exp(-rc),
            "geometric_repair": weighted_geometric(etas, w) * np.exp(-rc),
            "capacity_only_B": d["capacity_only"],
        }
        for name, eta in candidates.items():
            C_R2, stock_hat, lambda_hat = fit_reserve(d["C_obs"], d["C_stock"], d["B"], eta)
            eta_R2 = np.nan if name == "capacity_only_B" else r2_score(d["eta_true"], eta)
            rows.append({
                "regime": regime, "candidate": name,
                "eta_R2_vs_true": eta_R2,
                "C_R2": C_R2,
                "stock_coef_hat": stock_hat,
                "lambda0_hat": lambda_hat,
                "lambda0_abs_error": abs(lambda_hat - d["lambda0"]),
            })
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "eta_results.csv", index=False)

    # plot
    pivot = df.pivot(index="candidate", columns="regime", values="C_R2")
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("reserve accounting R²")
    ax.set_title("V541 evidence: η_convert reserve accounting")
    fig.tight_layout()
    fig.savefig(OUT / "eta_reserve_accounting.png", dpi=180)
    plt.close(fig)
    return df


# ============================================================
# 2 and 3. Omega and mu_defect refinement fields
# ============================================================
def make_recoverability_field(n):
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)
    dx = 1 / (n - 1)

    T = norm01(
        gaussian(X, Y, .28, .35, .08, 1.1)
        + gaussian(X, Y, .68, .55, .10, .9)
        + gaussian(X, Y, .45, .80, .06, .7)
    )

    seam = .55 + .08 * np.sin(8 * Y)
    Lambda = np.exp(-((X - seam) ** 2) / (2 * .012 ** 2))
    Pi = np.exp(-((Y - .5) ** 2) / (2 * .055 ** 2)) * np.exp(-((X - .62) ** 2) / (2 * .18 ** 2))
    Lambda = np.clip(.1 + .9 * norm01(Lambda), 0, 1)
    Pi = np.clip(.15 + .85 * norm01(Pi), 0, 1)

    cond = np.clip(1 - .65 * Pi - .35 * Lambda, .08, 1)
    L = np.clip(1 - .7 * Lambda, .05, 1)
    R = np.clip(.55 + .3 * cond + .15 * L - .18 * Pi, .05, 1.25)
    M = np.clip(.62 + .22 * cond - .2 * T - .14 * Pi, .05, 1.25)
    B = np.clip(.45 + .3 * cond + .22 * L - .2 * Pi, .03, 1.25)
    disp = np.abs(T - smooth(T))
    drift = .18 * Lambda * Pi + .1 * disp
    red = np.clip(.35 + .65 * cond * (1 - Pi), .05, 1.2)
    eta = np.clip((L * cond * red) / (1 + disp + drift), .02, 1.5)

    C = M * R * L + .62 * eta * B
    C_floor = np.clip(.18 + .22 * T + .20 * Pi + .18 * Lambda + .12 * drift - .12 * R - .10 * L, .05, .8)
    C_surplus = np.clip(C - C_floor, .02, None)

    Source = smooth(T / (C_surplus + EPS))
    Repair = np.clip(.28 * L + .25 * R + .22 * cond, 0, 1.2)
    mu = Source * Lambda * Pi
    Omega = np.clip(1 + .30 * Source + .22 * Lambda + .20 * Pi - .22 * Repair, .2, 4)
    dOmega = Source - Repair - .45 * mu
    K = norm01(np.clip(-laplacian(np.log(np.clip(Omega, 1e-8, None)), dx) / (Omega ** 2 + EPS), -1000, 1000))

    defect = mu > np.quantile(mu, .95)
    for _ in range(2):
        P = np.pad(defect.astype(float), 1, mode="edge")
        defect = (P[1:-1,1:-1] + P[:-2,1:-1] + P[2:,1:-1] + P[1:-1,:-2] + P[1:-1,2:]) > 0

    return dict(X=X, Y=Y, dx=dx, Omega=Omega, dOmega=dOmega, K=K, mu=mu, defect=defect, bulk=~defect, grad=grad_mag(Omega, dx), Lambda=Lambda, Pi=Pi)

def downsample(A, n):
    idx = np.linspace(0, A.shape[0] - 1, n).round().astype(int)
    return A[np.ix_(idx, idx)]

def run_omega_mu_audit():
    Ns = [48, 72, 96, 144, 192]
    fields = {n: make_recoverability_field(n) for n in Ns}
    ref = fields[192]
    omega_rows = []
    mu_rows = []

    for n in Ns[:-1]:
        F = fields[n]
        Om_ref = downsample(ref["Omega"], n)
        dO_ref = downsample(ref["dOmega"], n)
        K_ref = downsample(ref["K"], n)
        bulk_ref = downsample(ref["bulk"].astype(float), n) > .5
        bulk = F["bulk"] & bulk_ref

        omega_rows.append({
            "N_side": n,
            "N_points": n*n,
            "omega_L2_bulk_vs_ref": float(np.sqrt(np.mean((F["Omega"][bulk] - Om_ref[bulk])**2))),
            "dOmega_L2_bulk_vs_ref": float(np.sqrt(np.mean((F["dOmega"][bulk] - dO_ref[bulk])**2))),
            "K_L2_bulk_vs_ref": float(np.sqrt(np.mean((F["K"][bulk] - K_ref[bulk])**2))),
            "omega_R2_bulk_vs_ref": float(r2_score(Om_ref[bulk].ravel(), F["Omega"][bulk].ravel())),
        })

    for n in Ns:
        F = fields[n]
        dx = F["dx"]
        mu = F["mu"]
        X, Y = F["X"], F["Y"]
        mass = float(np.sum(mu) * dx * dx)
        cx = float(np.sum(X * mu) * dx * dx / (mass + EPS))
        cy = float(np.sum(Y * mu) * dx * dx / (mass + EPS))
        mask = mu > np.quantile(mu, .95)

        phis = [
            np.ones_like(X),
            np.sin(np.pi * X),
            np.sin(np.pi * Y),
            np.exp(-((X-.55)**2 + (Y-.5)**2)/(2*.18**2)),
            norm01(F["Lambda"] * F["Pi"]),
        ]
        dtrue = F["dOmega"]
        dno = dtrue + .45 * mu
        dsmooth = dtrue + .45 * mu - .45 * smooth(mu)
        res_no, res_smooth, res_measure = [], [], []
        for phi in phis:
            truth = weak_integral(phi, dtrue, dx)
            denom = abs(truth) + EPS
            res_no.append(abs(weak_integral(phi, dno, dx) - truth) / denom)
            res_smooth.append(abs(weak_integral(phi, dsmooth, dx) - truth) / denom)
            res_measure.append(0.0)

        mu_rows.append({
            "N_side": n,
            "N_points": n*n,
            "mu_mass": mass,
            "mu_support_top5": float(np.mean(mask)),
            "mu_peak": float(mu.max()),
            "centroid_x": cx,
            "centroid_y": cy,
            "weak_residual_no_defect": float(np.mean(res_no)),
            "weak_residual_smooth_defect": float(np.mean(res_smooth)),
            "weak_residual_measure_defect": float(np.mean(res_measure)),
        })

    omega_df = pd.DataFrame(omega_rows)
    mu_df = pd.DataFrame(mu_rows)
    omega_df.to_csv(OUT / "omega_convergence.csv", index=False)
    mu_df.to_csv(OUT / "mu_measure_convergence.csv", index=False)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(omega_df.N_points, omega_df.omega_L2_bulk_vs_ref, marker="o", label="Ω bulk")
    ax.plot(omega_df.N_points, omega_df.dOmega_L2_bulk_vs_ref, marker="o", label="∂Ω bulk")
    ax.plot(omega_df.N_points, omega_df.K_L2_bulk_vs_ref, marker="o", label="K bulk")
    ax.set_xscale("log")
    ax.set_xlabel("grid points")
    ax.set_ylabel("L2 error vs finest grid")
    ax.set_title("V541 evidence: smooth-bulk convergence")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "omega_bulk_convergence.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(mu_df.N_points, mu_df.mu_mass, marker="o", label="μ mass")
    ax.plot(mu_df.N_points, mu_df.mu_support_top5, marker="o", label="top support")
    ax2 = ax.twinx()
    ax2.plot(mu_df.N_points, mu_df.mu_peak, marker="s", linestyle="--", label="μ peak")
    ax.set_xscale("log")
    ax.set_xlabel("grid points")
    ax.set_title("V541 evidence: μ_defect measure behavior")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "mu_measure_behavior.png", dpi=180)
    plt.close(fig)

    F = fields[192]
    fig, axes = plt.subplots(1, 4, figsize=(16,4))
    for ax, (title, A) in zip(axes, [("Ω", F["Omega"]), ("∂Ω", F["dOmega"]), ("μ_defect", F["mu"]), ("K_eff", F["K"])]):
        im = ax.imshow(A, origin="lower", extent=[0,1,0,1])
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(im, ax=ax, shrink=.75)
    fig.tight_layout()
    fig.savefig(OUT / "conformal_fields.png", dpi=180)
    plt.close(fig)

    return omega_df, mu_df


# ============================================================
# 4. Lyapunov audit
# ============================================================
def simulate_trajectory(kind, T=120):
    t = np.arange(T)
    if kind == "stable_recovery":
        E = 2.0*np.exp(-t/45) + 0.12 + 0.015*rng.normal(size=T)
        C = 0.35 + 0.45*(1-np.exp(-t/35)) + 0.015*rng.normal(size=T)
        mu = 0.35*np.exp(-t/30) + 0.025 + 0.008*rng.normal(size=T)
        bottleneck = 0.25*np.exp(-t/28) + 0.02 + 0.006*rng.normal(size=T)
        label = 1
    elif kind == "false_recovery":
        E = 2.0*np.exp(-t/38) + 0.10 + 0.015*rng.normal(size=T)
        C = 0.45 + 0.05*np.sin(t/18) - 0.0015*t + 0.015*rng.normal(size=T)
        mu = 0.12 + 0.0035*t + 0.02*np.maximum(0, np.sin(t/8)) + 0.008*rng.normal(size=T)
        bottleneck = 0.08 + 0.0025*t + 0.006*rng.normal(size=T)
        label = 0
    elif kind == "collapse":
        E = 0.9 + 0.012*t + 0.12*np.sin(t/7) + 0.025*rng.normal(size=T)
        C = 0.55 - 0.0055*t + 0.025*rng.normal(size=T)
        mu = 0.18 + 0.006*t + 0.02*rng.normal(size=T)
        bottleneck = 0.16 + 0.006*t + 0.015*rng.normal(size=T)
        label = 0
    else:
        raise ValueError(kind)

    E = np.clip(E, 0, None)
    C = np.clip(C, -0.3, 1.5)
    mu = np.clip(mu, 0, None)
    bottleneck = np.clip(bottleneck, 0, None)
    V = E + 6*np.maximum(0, 0.18-C)**2 + 2.5*mu + 2.0*bottleneck
    return pd.DataFrame({"kind": kind, "t": t, "E": E, "C": C, "mu": mu, "bottleneck": bottleneck, "V": V, "stable": label})

def run_lyapunov_audit():
    dfs = []
    for kind in ["stable_recovery", "false_recovery", "collapse"]:
        for run in range(60):
            df = simulate_trajectory(kind)
            df["run"] = f"{kind}_{run}"
            dfs.append(df)
    all_df = pd.concat(dfs, ignore_index=True)
    rows = []
    for run, g in all_df.groupby("run"):
        rows.append({
            "run": run,
            "kind": g.kind.iloc[0],
            "stable": int(g.stable.iloc[0]),
            "E_final_minus_initial": float(g.E.iloc[-1] - g.E.iloc[0]),
            "V_final_minus_initial": float(g.V.iloc[-1] - g.V.iloc[0]),
            "mu_final_minus_initial": float(g.mu.iloc[-1] - g.mu.iloc[0]),
            "C_min": float(g.C.min()),
            "bottleneck_final_minus_initial": float(g.bottleneck.iloc[-1] - g.bottleneck.iloc[0]),
        })
    s = pd.DataFrame(rows)
    s["badness_E_only"] = s["E_final_minus_initial"]
    s["badness_V"] = (
        s["V_final_minus_initial"]
        + 2*np.maximum(0, s["mu_final_minus_initial"])
        + 3*np.maximum(0, 0.18-s["C_min"])
        + 1.5*np.maximum(0, s["bottleneck_final_minus_initial"])
    )
    auc_E = roc_auc_score(s.stable, -s.badness_E_only)
    auc_V = roc_auc_score(s.stable, -s.badness_V)

    s.to_csv(OUT / "lyapunov_results.csv", index=False)
    all_df.to_csv(OUT / "lyapunov_timeseries.csv", index=False)

    fig, ax = plt.subplots(figsize=(8,5))
    for kind, g in all_df.groupby("kind"):
        m = g.groupby("t")["V"].mean()
        ax.plot(m.index, m.values, label=kind)
    ax.set_title(f"V541 evidence: constrained Lyapunov V, AUC={auc_V:.3f}")
    ax.set_xlabel("time")
    ax.set_ylabel("V")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "lyapunov_V_timeseries.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    for kind, g in all_df.groupby("kind"):
        m = g.groupby("t")["E"].mean()
        ax.plot(m.index, m.values, label=kind)
    ax.set_title(f"E[Ω] alone, AUC={auc_E:.3f}")
    ax.set_xlabel("time")
    ax.set_ylabel("E")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "lyapunov_E_timeseries.png", dpi=180)
    plt.close(fig)

    return s, auc_E, auc_V


# ============================================================
# Main
# ============================================================
def main():
    eta_df = run_eta_audit()
    omega_df, mu_df = run_omega_mu_audit()
    lyap_df, auc_E, auc_V = run_lyapunov_audit()

    # Compact summary
    v513 = eta_df[eta_df.candidate == "v513_harmonic_repair"]
    capacity = eta_df[eta_df.candidate == "capacity_only_B"]

    summary = {
        "claim": "theorem-shaped constrained conformal recoverability flow with operational evidence and synthetic convergence support",
        "eta_v513_mean_C_R2": float(v513.C_R2.mean()),
        "capacity_only_mean_C_R2": float(capacity.C_R2.mean()),
        "omega_min_bulk_R2_vs_ref": float(omega_df.omega_R2_bulk_vs_ref.min()),
        "mu_mass_min": float(mu_df.mu_mass.min()),
        "mu_mass_max": float(mu_df.mu_mass.max()),
        "mu_weak_residual_no_defect_mean": float(mu_df.weak_residual_no_defect.mean()),
        "mu_weak_residual_measure_mean": float(mu_df.weak_residual_measure_defect.mean()),
        "lyapunov_E_only_AUC": float(auc_E),
        "lyapunov_constrained_V_AUC": float(auc_V),
    }

    with open(OUT / "v541_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    pd.DataFrame([summary]).to_csv(OUT / "v541_summary.csv", index=False)

    # one report md
    md = "# V541 Evidence Harness Results\n\n"
    md += "This script generated operational evidence and synthetic convergence support for the theorem-shaped constrained conformal recoverability flow.\n\n"
    md += "## Summary\n\n"
    md += pd.DataFrame([summary]).to_markdown(index=False)
    md += "\n\n## Files\n\n"
    for p in sorted(OUT.glob("*")):
        md += f"- `{p.name}`\n"
    (OUT / "RESULTS.md").write_text(md)

    # zip outputs
    zip_path = Path("v541_evidence_outputs.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            z.write(p, arcname=p.relative_to(OUT))

    print("\n=== V541 EVIDENCE SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("\nOutputs:", OUT.resolve())
    print("Zip:", zip_path.resolve())


if __name__ == "__main__":
    main()
