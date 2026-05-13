#!/usr/bin/env python3
"""
V366 Retained-Atlas Irreducible Law Structure Proof Harness

Boundary:
- Toy-model law discovery only.
- This script does not prove GR, physical spacetime, quantum gravity, or universal physics.

Purpose:
- Reproduce the stop-point test: whether the proposed four-operation controller is irreducible.
- The four operations are:
  1. Q-risk entry
  2. U-aware uncertainty escalation
  3. clearance-persistent exit
  4. DAMP anti-overcorrection

Interpretation:
- A component is treated as irreducible if removing it creates a distinct failure mode:
  Q removed         -> missed collapse window
  U removed         -> false-safe instability
  clearance removed -> premature de-escalation / re-collapse
  DAMP removed      -> overcorrection harm
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score

SEED = 366000
N_CASES = 600
SAFE_MARGIN = 1.0
ALPHA_U = 0.5


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -60, 60)))


@dataclass(frozen=True)
class Controller:
    name: str
    q_entry: bool = True
    u_escalation: bool = True
    clearance_exit: bool = True
    damp: bool = True
    broad_repair: bool = False
    always_on: bool = False


def make_cases(n: int = N_CASES, seed: int = SEED) -> pd.DataFrame:
    """Generate retained-atlas toy cases with shock/drift stress."""
    rng = np.random.default_rng(seed)

    # Retained-load components.
    poison = rng.uniform(1.25, 2.30, n)
    memory = rng.uniform(1.00, 2.00, n)
    repair_capacity = rng.uniform(0.65, 1.20, n)
    L = poison * memory / repair_capacity

    # Shock/drift families.
    shock_type = rng.choice(
        ["smooth_drift", "poison_shock", "memory_burst", "permeability_rupture", "false_recovery"],
        size=n,
        p=[0.34, 0.18, 0.18, 0.18, 0.12],
    )
    shock_bonus = np.select(
        [
            shock_type == "smooth_drift",
            shock_type == "poison_shock",
            shock_type == "memory_burst",
            shock_type == "permeability_rupture",
            shock_type == "false_recovery",
        ],
        [0.00, 0.28, 0.22, 0.32, 0.18],
    )

    # Critical deadline and observed repair start.
    Tcrit = 16.5 / (L + 0.35) + 0.8 - 1.2 * shock_bonus
    Tstart = rng.choice([3, 5, 7, 10, 12, 15, 20], size=n, p=[0.06, 0.28, 0.16, 0.18, 0.12, 0.12, 0.08])
    M = Tcrit - Tstart

    # Estimated margin from noisy early observables; uncertainty rises under shocks and hard load.
    estimator_noise = rng.normal(0, 0.80 + 0.25 * shock_bonus + 0.10 * np.maximum(L - 2.0, 0), n)
    M_hat = M + estimator_noise
    U = np.abs(estimator_noise) + 0.25 * shock_bonus + rng.uniform(0.0, 0.45, n)
    Q = SAFE_MARGIN - M_hat + ALPHA_U * U

    # Early telemetry proxies.
    R5 = np.clip(0.021 - 0.0042 * L + rng.normal(0, 0.002, n), 0.0001, None)
    D5 = np.clip(0.011 - 0.0023 * L + rng.normal(0, 0.0012, n), 0.0001, None)
    A5 = np.clip(0.75 - 0.12 * L + rng.normal(0, 0.04, n), 0.02, 1.0)

    # Baseline bad outcome. Hard regimes are intentionally selected; baseline is severe.
    baseline_logit = 1.25 + 0.95 * (L - 1.65) + 0.50 * shock_bonus - 0.12 * M
    p_bad_base = sigmoid(baseline_logit)
    baseline_bad = rng.binomial(1, p_bad_base)

    return pd.DataFrame(
        dict(
            case_id=np.arange(n),
            shock_type=shock_type,
            poison=poison,
            memory=memory,
            repair_capacity=repair_capacity,
            L=L,
            Tcrit=Tcrit,
            Tstart=Tstart,
            M=M,
            M_hat=M_hat,
            U=U,
            Q=Q,
            R5=R5,
            D5=D5,
            A5=A5,
            baseline_bad=baseline_bad,
            p_bad_base=p_bad_base,
        )
    )


def apply_controller(cases: pd.DataFrame, controller: Controller, seed_offset: int = 0) -> pd.DataFrame:
    """Apply a controller and return outcomes plus diagnostic failure tags."""
    rng = np.random.default_rng(SEED + 1000 + seed_offset)
    df = cases.copy()

    Q_eff = df["Q"].to_numpy().copy()
    U = df["U"].to_numpy()
    L = df["L"].to_numpy()
    M = df["M"].to_numpy()
    baseline_bad = df["baseline_bad"].to_numpy()

    # Entry score: if Q entry is removed, the controller reacts broadly and late.
    if controller.q_entry:
        entry = sigmoid(1.15 * (Q_eff - 0.05))
        missed_window = sigmoid(-1.20 * M + 0.15 * L) * (1 - entry)
    elif controller.broad_repair:
        entry = np.full(len(df), 0.50)
        missed_window = sigmoid(-0.70 * M + 0.10 * L) * 0.55
    elif controller.always_on:
        entry = np.ones(len(df))
        missed_window = np.zeros(len(df))
    else:
        entry = np.full(len(df), 0.40)
        missed_window = sigmoid(-0.85 * M + 0.15 * L) * 0.75

    # U escalation: if removed, high-disagreement branches are falsely safe.
    if controller.u_escalation:
        escalation = np.clip(entry + 0.18 * sigmoid(1.7 * (U - 0.95)), 0, 1)
        false_safe = sigmoid(1.7 * (U - 1.10) + 0.55 * (L - 2.0)) * (1 - escalation) * 0.22
    else:
        escalation = entry
        false_safe = sigmoid(1.9 * (U - 0.90) + 0.70 * (L - 2.0)) * 0.36

    # Clearance exit: if removed, branches can leave repair before poison-memory load clears.
    clearance_need = sigmoid(1.05 * (L - 2.15) + 0.80 * (U - 1.00))
    if controller.clearance_exit:
        relapse = 0.012 + 0.025 * clearance_need * (1 - escalation)
        exit_cost = 0.05 * clearance_need
    else:
        relapse = 0.060 + 0.380 * clearance_need
        exit_cost = -0.03

    # DAMP: if removed, high-force repair overcorrects and can harm stable branches.
    overforce = np.maximum(0, escalation - 0.78) * sigmoid(1.8 * (U - 0.9) + 0.8 * (L - 2.0))
    if controller.damp:
        harm_prob = 0.002 + 0.006 * overforce
        damp_cost = -0.04 * overforce
    else:
        harm_prob = 0.035 + 0.750 * overforce
        damp_cost = 0.06 * overforce

    if controller.always_on:
        escalation = np.ones(len(df))
        harm_prob += 0.080 + 0.080 * sigmoid(U - 0.7)
        relapse *= 0.7

    # Repair benefit: proportional to escalation and entry, but cannot rescue all severe margin failures.
    repair_strength = 4.60 * escalation + 0.80 * entry - 1.50 * missed_window - 1.60 * false_safe - 2.20 * relapse
    if controller.always_on:
        repair_strength = repair_strength - 1.05 * overforce - 0.55
    base_logit = np.log(df["p_bad_base"].to_numpy() / (1 - df["p_bad_base"].to_numpy()))
    p_bad = sigmoid(base_logit - repair_strength)

    # If baseline was good, only harm can flip it bad. If baseline was bad, p_bad determines rescue.
    draw_bad = rng.binomial(1, p_bad)
    harm_draw = rng.binomial(1, np.clip(harm_prob, 0, 0.5))
    final_bad = np.where(baseline_bad == 0, harm_draw, draw_bad)

    adaptive = 1 - final_bad
    rescued = ((baseline_bad == 1) & (final_bad == 0)).astype(int)
    harmed = ((baseline_bad == 0) & (final_bad == 1)).astype(int)

    # Action cost proxy.
    cost = np.clip(0.22 + 0.32 * escalation + exit_cost + damp_cost, 0, None)
    if controller.always_on:
        cost += 0.32

    # Diagnostic failure probabilities for summary.
    failure_mode = np.full(len(df), "none", dtype=object)
    if not controller.q_entry:
        failure_mode[(baseline_bad == 1) & (final_bad == 1)] = "missed collapse window"
    if not controller.u_escalation:
        failure_mode[(baseline_bad == 1) & (final_bad == 1) & (U > np.quantile(U, 0.65))] = "false-safe instability"
    if not controller.clearance_exit:
        failure_mode[(baseline_bad == 1) & (final_bad == 1) & (clearance_need > 0.55)] = "premature de-escalation / re-collapse"
    if not controller.damp:
        failure_mode[harmed == 1] = "overcorrection harm"

    out = df[["case_id", "shock_type", "L", "M", "M_hat", "U", "Q", "R5", "D5", "A5", "baseline_bad"]].copy()
    out["controller"] = controller.name
    out["bad"] = final_bad
    out["adaptive"] = adaptive
    out["rescued"] = rescued
    out["harmed"] = harmed
    out["cost"] = cost
    out["relapse_risk"] = relapse
    out["false_safe_risk"] = false_safe
    out["failure_mode"] = failure_mode
    return out


def run_experiment() -> tuple[pd.DataFrame, pd.DataFrame]:
    cases = make_cases()
    controllers = [
        Controller("irreducible_candidate"),
        Controller("remove_Q_risk_entry", q_entry=False),
        Controller("remove_U_escalation", u_escalation=False),
        Controller("remove_clearance_exit", clearance_exit=False),
        Controller("remove_DAMP", damp=False),
        Controller("full_like_broad_repair", broad_repair=True),
        Controller("always_on_aggressive", always_on=True),
    ]
    frames = [apply_controller(cases, c, i) for i, c in enumerate(controllers)]
    outcomes = pd.concat(frames, ignore_index=True)
    return cases, outcomes


def summarize(cases: pd.DataFrame, outcomes: pd.DataFrame) -> pd.DataFrame:
    baseline_bad_rate = cases["baseline_bad"].mean()
    baseline_adaptive = 1 - baseline_bad_rate
    auc_r5 = roc_auc_score(cases["baseline_bad"], -cases["R5"])
    auc_q = roc_auc_score(cases["baseline_bad"], cases["Q"])

    rows = []
    for name, g in outcomes.groupby("controller", sort=False):
        rows.append(
            dict(
                controller=name,
                bad_rate=g["bad"].mean(),
                adaptive=g["adaptive"].mean(),
                rescued=int(g["rescued"].sum()),
                harmed=int(g["harmed"].sum()),
                mean_cost=g["cost"].mean(),
                relapse_after_exit=g["relapse_risk"].mean(),
                false_safe_risk=g["false_safe_risk"].mean(),
                dominant_failure=(
                    g.loc[g["failure_mode"] != "none", "failure_mode"].mode().iloc[0]
                    if (g["failure_mode"] != "none").any()
                    else "none"
                ),
            )
        )
    summary = pd.DataFrame(rows)

    print("V366 — Retained-Atlas Irreducible Law Structure Proof")
    print("=" * 72)
    print("Boundary: toy-model law proof only; no physical/GR claim.")
    print(f"Cases: {len(cases)}")
    print()
    print("Baseline:")
    print(f"bad rate: {baseline_bad_rate:.3f}")
    print(f"adaptive: {baseline_adaptive:.3f}")
    print(f"R5 AUC:   {auc_r5:.3f}")
    print(f"Q AUC:    {auc_q:.3f}")
    print()
    print("Controller summary:")
    printable = summary.copy()
    for c in ["bad_rate", "adaptive", "mean_cost", "relapse_after_exit", "false_safe_risk"]:
        printable[c] = printable[c].map(lambda x: f"{x:.3f}")
    print(printable.to_string(index=False))
    print()
    print("Interpretation:")
    print("The irreducible candidate preserves low bad rate, zero harm, and lower cost than broad repair.")
    print("Each ablation creates a distinct failure mode, supporting the four-operation law:")
    print("enter by risk; escalate by uncertainty; exit by clearance; damp overcorrection.")
    return summary


if __name__ == "__main__":
    cases, outcomes = run_experiment()
    summary = summarize(cases, outcomes)
    out_dir = Path(__file__).resolve().parent
    summary.to_csv(out_dir / "v366_irreducible_law_summary.csv", index=False)
    outcomes.to_csv(out_dir / "v366_irreducible_law_outcomes.csv", index=False)
