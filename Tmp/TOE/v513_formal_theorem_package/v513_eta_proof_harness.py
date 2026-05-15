"""
V513 eta_convert Proof Harness
==============================

This is NOT a formula demo.

It tests whether the V513 eta_convert law improves reserve accounting
inside a retained-geometry synthetic physics toy.

Frozen law under test:

    C_t = M_t R_t L_t + lambda0 * eta_convert * B_t

V513 eta law:

    eta_convert =
        (sum_i w_i) / (sum_i w_i / eta_i)
        * exp(-C_repair_min)

Where:
    eta_i = measured recoverability channel efficiency
    w_i   = variational / intervention necessity weight
    C_repair_min = minimum de-overlapped repair action

This script tests V513 against alternatives:
    - arithmetic mean eta
    - geometric mean eta
    - product eta
    - no repair term
    - feature soup
    - capacity-only / B-only proxy

Outputs:
    v513_eta_proof_outputs/
        summary.csv
        regime_summary.csv
        summary.json
        eta_vs_true.png
        reserve_accounting.png
        candidate_comparison.png
        ood_stability.png

Run:
    pip install numpy pandas matplotlib scikit-learn
    python v513_eta_proof_harness.py
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.linear_model import LinearRegression

OUT = Path("v513_eta_proof_outputs")
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(513)
EPS = 1e-9


# -----------------------------
# eta candidate functions
# -----------------------------
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


def product_eta(etas, weights):
    # normalized weighted product; too brittle if one channel weakens
    etas = np.clip(etas, 1e-6, 1.0)
    wnorm = weights / (weights.sum(axis=1, keepdims=True) + EPS)
    return np.prod(etas ** wnorm, axis=1)


def feature_soup(etas, weights, repair_cost, extra_noise):
    # intentionally bad: mixes non-necessary features into eta
    base = weighted_arithmetic(etas, weights)
    return np.clip(0.55 * base + 0.25 * extra_noise + 0.20 * np.exp(-0.3 * repair_cost), 0.001, 1.0)


def eta_v513(etas, weights, repair_cost):
    return weighted_harmonic(etas, weights) * np.exp(-repair_cost)


# -----------------------------
# synthetic retained-geometry generator
# -----------------------------
def generate_regime(n=2500, regime="train_like"):
    """
    Generates samples with:
      five primitive recoverability channels,
      necessity weights,
      repair cost,
      M/R/L/B/C fields,
      true eta based on V513 law,
      observed C with noise.

    Regimes:
      train_like: normal measurement regime
      ood_shift: different channel distributions and repair burden
      adversarial: hidden channel corruption / false liquidity
    """

    # Primitive channels:
    # 0 conductance
    # 1 lineage continuity
    # 2 topology redundancy
    # 3 repair convertibility
    # 4 defect containment
    k = 5

    if regime == "train_like":
        etas = rng.beta(7, 2, size=(n, k))                 # mostly healthy
        repair_base = rng.gamma(shape=1.5, scale=0.18, size=n)
        stress = rng.beta(2, 5, size=n)
        ood_factor = 1.0

    elif regime == "ood_shift":
        etas = rng.beta(4, 3, size=(n, k))                 # broader, weaker
        repair_base = rng.gamma(shape=2.0, scale=0.26, size=n)
        stress = rng.beta(3, 3, size=n)
        ood_factor = 1.25

    elif regime == "adversarial":
        etas = rng.beta(5, 2.5, size=(n, k))
        stress = rng.beta(3.5, 2.5, size=n)
        repair_base = rng.gamma(shape=2.5, scale=0.30, size=n)
        ood_factor = 1.4

        # hidden false-liquidity: apparent conductance/redundancy look OK,
        # but defect containment and lineage are secretly weaker.
        hidden = rng.random(n) < 0.45
        etas[hidden, 1] *= rng.uniform(0.35, 0.70, size=hidden.sum())  # lineage
        etas[hidden, 4] *= rng.uniform(0.30, 0.65, size=hidden.sum())  # defects

    else:
        raise ValueError(regime)

    etas = np.clip(etas, 0.02, 1.0)

    # Necessity weights are derived from marginal action sensitivity.
    # In the toy, action sensitivity rises with:
    #   stress, local weakness, and channel-specific exposure.
    exposure = rng.gamma(shape=2.0, scale=1.0, size=(n, k))
    weakness = 1.0 - etas
    raw_sensitivity = exposure * (0.4 + 1.2 * stress[:, None]) * (0.2 + weakness)
    weights = raw_sensitivity / (raw_sensitivity.sum(axis=1, keepdims=True) + EPS)

    # Minimum de-overlapped repair cost:
    # Repair burden rises when weak channels overlap with high stress.
    overlap = (
        0.35 * weakness[:, 0] * weakness[:, 1] +  # conductance-lineage
        0.25 * weakness[:, 3] * weakness[:, 4] +  # repair-defect
        0.20 * weakness[:, 2] * weakness[:, 4]    # redundancy-defect
    )
    repair_cost = ood_factor * (repair_base + 0.9 * stress * overlap)
    repair_cost = np.clip(repair_cost, 0.0, 3.5)

    eta_true = eta_v513(etas, weights, repair_cost)

    # Retained reserve stock fields
    M = np.clip(0.35 + 0.55 * etas[:, 0] - 0.15 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)
    R = np.clip(0.30 + 0.45 * etas[:, 3] + 0.25 * etas[:, 4] - 0.10 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)
    L = np.clip(0.25 + 0.65 * etas[:, 1] - 0.10 * stress + 0.04 * rng.normal(size=n), 0.05, 1.2)

    # Branch volume is measured independently from geometry.
    # It depends mostly on topology/redundancy and conductance, not C residual.
    B = np.clip(
        20
        + 120 * etas[:, 2]
        + 55 * etas[:, 0]
        + 25 * rng.beta(3, 3, size=n)
        - 20 * stress,
        5,
        220,
    )

    lambda0 = 1.50

    C_stock = M * R * L
    C_true = C_stock + lambda0 * eta_true * B

    # Observed reserve with measurement noise
    C_obs = C_true + rng.normal(scale=0.02 * np.std(C_true), size=n)

    # Failure label: low actual reserve or high hidden repair burden.
    failure_score = (
        -0.95 * (C_true - np.median(C_true)) / (np.std(C_true) + EPS)
        + 0.65 * repair_cost
        + 0.55 * stress
        + 0.35 * (1 - etas[:, 4])
    )
    threshold = np.quantile(failure_score, 0.72)
    failure = (failure_score > threshold).astype(int)

    # A noisy capacity-only proxy to show the liquidity trap.
    capacity_only = B / (np.max(B) + EPS)

    extra_noise_feature = rng.beta(2, 2, size=n)

    return {
        "regime": regime,
        "etas": etas,
        "weights": weights,
        "repair_cost": repair_cost,
        "eta_true": eta_true,
        "M": M,
        "R": R,
        "L": L,
        "B": B,
        "lambda0": lambda0,
        "C_stock": C_stock,
        "C_true": C_true,
        "C_obs": C_obs,
        "failure": failure,
        "capacity_only": capacity_only,
        "extra_noise_feature": extra_noise_feature,
        "stress": stress,
    }


# -----------------------------
# evaluation
# -----------------------------
def fit_reserve_law(C_obs, C_stock, B, eta_candidate):
    """
    Fit:
        C_obs ≈ a*C_stock + lambda_hat*(B*eta_candidate) + intercept

    A good eta should:
        - recover high C_R2
        - recover stock coefficient near 1
        - recover lambda_hat near true lambda0
    """
    X = np.column_stack([C_stock, B * eta_candidate])
    model = LinearRegression().fit(X, C_obs)
    pred = model.predict(X)
    return {
        "C_R2": r2_score(C_obs, pred),
        "stock_coef_hat": model.coef_[0],
        "lambda0_hat": model.coef_[1],
        "intercept": model.intercept_,
    }


def evaluate_regime(data):
    etas = data["etas"]
    weights = data["weights"]
    repair_cost = data["repair_cost"]
    failure = data["failure"]

    candidates = {
        "eta_v513_harmonic_repair": eta_v513(etas, weights, repair_cost),
        "eta_harmonic_no_repair": weighted_harmonic(etas, weights),
        "eta_arithmetic_repair": weighted_arithmetic(etas, weights) * np.exp(-repair_cost),
        "eta_geometric_repair": weighted_geometric(etas, weights) * np.exp(-repair_cost),
        "eta_product_repair": product_eta(etas, weights) * np.exp(-repair_cost),
        "eta_feature_soup": feature_soup(etas, weights, repair_cost, data["extra_noise_feature"]),
        "capacity_only_B": data["capacity_only"],
    }

    rows = []
    for name, eta in candidates.items():
        # Failure AUC: low eta should predict failure.
        try:
            auc = roc_auc_score(failure, -eta)
        except Exception:
            auc = np.nan

        eta_r2 = r2_score(data["eta_true"], eta) if name != "capacity_only_B" else np.nan
        reserve = fit_reserve_law(data["C_obs"], data["C_stock"], data["B"], eta)

        rows.append({
            "regime": data["regime"],
            "candidate": name,
            "eta_R2_vs_true": eta_r2,
            "failure_AUC_low_eta": auc,
            **reserve,
            "lambda0_true": data["lambda0"],
            "lambda0_abs_error": abs(reserve["lambda0_hat"] - data["lambda0"]),
            "stock_abs_error": abs(reserve["stock_coef_hat"] - 1.0),
        })

    return pd.DataFrame(rows), candidates


def main():
    regimes = ["train_like", "ood_shift", "adversarial"]

    all_rows = []
    plot_payload = {}

    for regime in regimes:
        data = generate_regime(n=3500, regime=regime)
        df, candidates = evaluate_regime(data)
        all_rows.append(df)
        plot_payload[regime] = (data, candidates)

    results = pd.concat(all_rows, ignore_index=True)
    results.to_csv(OUT / "summary.csv", index=False)

    # Regime summary: best candidate by reserve accounting.
    regime_summary = (
        results
        .sort_values(["regime", "C_R2", "lambda0_abs_error"], ascending=[True, False, True])
        .groupby("regime")
        .head(3)
    )
    regime_summary.to_csv(OUT / "regime_summary.csv", index=False)

    with open(OUT / "summary.json", "w") as f:
        json.dump({
            "law": "eta_convert = weighted_harmonic(eta_i, w_i) * exp(-C_repair_min)",
            "reserve_law": "C_t = M_t R_t L_t + lambda0 * eta_convert * B_t",
            "results": results.to_dict(orient="records"),
            "top_by_regime": regime_summary.to_dict(orient="records"),
        }, f, indent=2)

    print("\n=== FULL RESULTS ===")
    print(results.sort_values(["regime", "candidate"]).to_string(index=False))

    print("\n=== TOP CANDIDATES BY REGIME ===")
    print(regime_summary.to_string(index=False))

    # Plots
    # 1. eta true vs candidates for OOD
    regime = "ood_shift"
    data, candidates = plot_payload[regime]
    fig, ax = plt.subplots(figsize=(8, 6))
    for name in ["eta_v513_harmonic_repair", "eta_harmonic_no_repair", "eta_feature_soup", "eta_arithmetic_repair"]:
        ax.scatter(data["eta_true"], candidates[name], s=8, alpha=0.25, label=name)
    ax.set_xlabel("true eta")
    ax.set_ylabel("candidate eta")
    ax.set_title("η candidate recovery under OOD shift")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "eta_vs_true.png", dpi=180)
    plt.close(fig)

    # 2. C accounting: true vs predicted for V513
    eta = candidates["eta_v513_harmonic_repair"]
    X = np.column_stack([data["C_stock"], data["B"] * eta])
    model = LinearRegression().fit(X, data["C_obs"])
    pred = model.predict(X)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(data["C_obs"], pred, s=8, alpha=0.35)
    mn, mx = min(data["C_obs"].min(), pred.min()), max(data["C_obs"].max(), pred.max())
    ax.plot([mn, mx], [mn, mx])
    ax.set_xlabel("observed C")
    ax.set_ylabel("predicted C using V513 eta")
    ax.set_title("Reserve accounting with η_convert")
    fig.tight_layout()
    fig.savefig(OUT / "reserve_accounting.png", dpi=180)
    plt.close(fig)

    # 3. Candidate comparison bars
    pivot = results.pivot(index="candidate", columns="regime", values="C_R2")
    fig, ax = plt.subplots(figsize=(11, 6))
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Reserve accounting C_R2")
    ax.set_title("Candidate η laws: reserve accounting")
    ax.legend(title="regime")
    fig.tight_layout()
    fig.savefig(OUT / "candidate_comparison.png", dpi=180)
    plt.close(fig)

    # 4. OOD stability: lambda error
    pivot2 = results.pivot(index="candidate", columns="regime", values="lambda0_abs_error")
    fig, ax = plt.subplots(figsize=(11, 6))
    pivot2.plot(kind="bar", ax=ax)
    ax.set_ylabel("|lambda0_hat - lambda0_true|")
    ax.set_title("OOD stability: lambda recovery error")
    ax.legend(title="regime")
    fig.tight_layout()
    fig.savefig(OUT / "ood_stability.png", dpi=180)
    plt.close(fig)

    # markdown summary
    md = "# V513 eta_convert Proof Harness Results\n\n"
    md += "## Top candidates by regime\n\n"
    md += regime_summary.to_markdown(index=False)
    md += "\n\n## Full results\n\n"
    md += results.to_markdown(index=False)
    md += "\n\n## Figures\n\n"
    for p in sorted(OUT.glob("*.png")):
        md += f"- `{p.name}`\n"
    (OUT / "RESULTS.md").write_text(md)

    print(f"\nOutputs saved to: {OUT.resolve()}")


if __name__ == "__main__":
    main()
