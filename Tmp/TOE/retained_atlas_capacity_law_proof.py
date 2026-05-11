"""
Retained Atlas Toy Model — Capacity Law Validation Proof Script
Version: V222 report-out proof

Purpose
-------
This standalone script reproduces the bounded toy-model claim:

    A retained atlas remains self-healing when adaptive repair/plasticity/mobility
    exceeds accumulated shock-congestion-clustering load.

This is NOT a GR proof. It is a pre-geometry / emergent-atlas toy model.

Core tested order parameter:

    C* = (repair * decay * mobility) / (shock * congestion * clustering * cycles)

The script calibrates C*_critical on a calibration split, then validates
C_norm = C* / C*_critical on fresh held-out cases.

Expected qualitative result:
    C_norm > 1  -> bounded self-healing geometry tends to hold
    C_norm < 1  -> frozen-scar / capacity failure tends to occur

Dependencies: numpy only.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

EPS = 1e-9


@dataclass
class CaseResult:
    passed: bool
    residual: float
    late_field_strain: float
    late_action: float
    late_mobility2: float
    c_star_scaled: float
    c_norm: float = np.nan
    shock: float = np.nan
    repair: float = np.nan
    decay: float = np.nan
    congestion: float = np.nan
    cycles: int = 0
    separation: str = ""


def balanced_accuracy(pred: np.ndarray, truth: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=bool)
    truth = np.asarray(truth, dtype=bool)
    pos = truth
    neg = ~truth
    if pos.sum() == 0 or neg.sum() == 0:
        return float((pred == truth).mean())
    return 0.5 * ((pred[pos] == truth[pos]).mean() + (pred[neg] == truth[neg]).mean())


def best_threshold(score: np.ndarray, truth: np.ndarray, greater: bool = True) -> Tuple[float, float, float]:
    score = np.asarray(score, dtype=float)
    truth = np.asarray(truth, dtype=bool)
    thresholds = np.linspace(np.nanmin(score), np.nanmax(score), 401)
    best_bal, best_acc, best_th = -1.0, -1.0, float(thresholds[0])
    for th in thresholds:
        pred = score > th if greater else score < th
        bal = balanced_accuracy(pred, truth)
        acc = float((pred == truth).mean())
        if bal > best_bal:
            best_bal, best_acc, best_th = bal, acc, float(th)
    return best_bal, best_acc, best_th


def run_atlas_case(
    seed: int,
    intervention: bool = True,
    shock: float = 1.25,
    separation: str = "near",
    repair: float = 0.95,
    decay: float = 0.85,
    congestion: float = 1.35,
    cycles: int = 5,
) -> Dict[str, float]:
    """Run one compact retained-atlas simulation case.

    The model has local nodes/charts, register R, holonomy H, connection rotation T,
    load L, repeated localized shocks, and endogenous targeted unlocking.
    """

    rng = np.random.default_rng(seed)
    np.random.seed(seed)
    n_nodes = 18
    steps = 260
    k_neighbors = 3

    coords = rng.normal(size=(n_nodes, 2))
    adj = np.zeros((n_nodes, n_nodes), dtype=bool)
    for i in range(n_nodes):
        d = np.sum((coords - coords[i]) ** 2, axis=1)
        for j in np.argsort(d)[1 : k_neighbors + 1]:
            adj[i, j] = adj[j, i] = True

    neigh = [np.where(adj[i])[0] for i in range(n_nodes)]
    edges = [(i, j) for i in range(n_nodes) for j in range(i + 1, n_nodes) if adj[i, j]]

    # Source/scar layout.
    c1 = int(np.argmin(coords[:, 0]))
    d1 = np.sum((coords - coords[c1]) ** 2, axis=1)
    if separation == "cluster":
        centers = [c1, int(np.argsort(d1)[2]), int(np.argsort(d1)[4])]
    else:
        c2 = int(np.argsort(d1)[3]) if separation == "near" else int(np.argmax(d1))
        centers = [c1, c2]

    scar_nodes = np.zeros(n_nodes, dtype=bool)
    for c in centers:
        local = np.argsort(np.sum((coords - coords[c]) ** 2, axis=1))[:4]
        scar_nodes[local] = True

    scar_edges = {(i, j) for i, j in edges if scar_nodes[i] or scar_nodes[j]}

    addressability = np.ones(n_nodes)
    register = np.zeros((n_nodes, n_nodes))
    holonomy = np.zeros((n_nodes, n_nodes))
    rotation = np.zeros((n_nodes, n_nodes))
    load = np.zeros((n_nodes, n_nodes))
    route_memory = np.zeros((n_nodes, n_nodes))

    # Representative repair-transport pairs.
    pairs = [tuple(rng.choice(n_nodes, size=2, replace=False)) for _ in range(5)]

    def edge_terms(i: int, j: int) -> Tuple[float, float, float, float, float, float, float, float]:
        r = 0.5 * (register[i, j] + register[j, i])
        h = 0.5 * (holonomy[i, j] + holonomy[j, i])
        l = 0.5 * (load[i, j] + load[j, i])
        th = abs(rotation[i, j])
        a = 0.5 * (addressability[i] + addressability[j])
        metric_cost = (1.0 + 2.0 * (1.0 - a)) / (0.20 + r + EPS)
        action_cost = metric_cost + 1.35 * h + 2.25 * th + 0.90 * l
        field_strain = 0.62 * h + 0.95 * th + 0.45 * l
        return metric_cost, action_cost, h, th, l, r, field_strain, a

    def shortest_path(src: int, dst: int, cost_index: int) -> Tuple[float, Tuple[int, ...]]:
        pq = [(0.0, int(src), tuple())]
        seen = set()
        while pq:
            cost, u, path = heapq.heappop(pq)
            if u in seen:
                continue
            seen.add(u)
            path = path + (u,)
            if u == dst:
                return cost, path
            for v0 in neigh[u]:
                v = int(v0)
                if v not in seen:
                    heapq.heappush(pq, (cost + edge_terms(u, v)[cost_index], v, path))
        return float("inf"), tuple()

    @staticmethod
    def path_edges(path: Tuple[int, ...]) -> set[Tuple[int, int]]:
        return {tuple(sorted((u, v))) for u, v in zip(path[:-1], path[1:])}

    def path_sum(path: Tuple[int, ...]) -> np.ndarray:
        vals = [edge_terms(u, v)[:7] for u, v in zip(path[:-1], path[1:])]
        return np.sum(np.array(vals), axis=0) if vals else np.zeros(7)

    def sample(t: int) -> Dict[str, float]:
        changed = 0
        savings = []
        scar_use_metric = []
        scar_use_action = []
        for a, b in pairs:
            _, metric_path = shortest_path(a, b, 0)
            _, action_path = shortest_path(a, b, 1)
            me = path_edges(metric_path)
            ae = path_edges(action_path)
            changed += me != ae
            savings.append(path_sum(metric_path)[1] - path_sum(action_path)[1])
            scar_use_metric.append(len(me & scar_edges) / max(1, len(me)))
            scar_use_action.append(len(ae & scar_edges) / max(1, len(ae)))

        vals = np.array([edge_terms(i, j) for i, j in edges])
        field_strain = float(vals[:, 6].mean())
        raw_mobility = (changed / len(pairs)) * max(float(np.mean(savings)), 0.0)
        mobility2 = raw_mobility / (field_strain + EPS) ** 2

        scar_vals = np.array([edge_terms(i, j) for i, j in edges if (i, j) in scar_edges])
        non_vals = np.array([edge_terms(i, j) for i, j in edges if (i, j) not in scar_edges])
        return {
            "t": float(t),
            "field_strain": field_strain,
            "mobility2": float(mobility2),
            "changed": float(changed / len(pairs)),
            "saving": float(np.mean(savings)),
            "action": float(vals[:, 1].mean()),
            "scar_field": float(scar_vals[:, 6].mean()) if len(scar_vals) else 0.0,
            "non_field": float(non_vals[:, 6].mean()) if len(non_vals) else 0.0,
            "scar_action": float(scar_vals[:, 1].mean()) if len(scar_vals) else 0.0,
            "non_action": float(non_vals[:, 1].mean()) if len(non_vals) else 0.0,
            "scar_path_metric": float(np.mean(scar_use_metric)),
            "scar_path_action": float(np.mean(scar_use_action)),
        }

    active_until = 0
    trigger_events = 0
    targeted_updates = 0
    hist: List[Dict[str, float]] = []
    shock_windows = [(35 + 42 * c, 40 + 42 * c) for c in range(cycles)]

    for t in range(1, steps + 1):
        in_shock = any(a <= t <= b for a, b in shock_windows)
        if in_shock:
            prob = 0.72 if separation != "far" else 0.55
            for i in np.where(scar_nodes & (rng.random(n_nodes) < prob))[0]:
                dmg = rng.uniform(0.20 * shock, 0.60 * shock)
                addressability[i] -= dmg
                for j in neigh[int(i)]:
                    j = int(j)
                    holonomy[i, j] += 0.32 * dmg
                    holonomy[j, i] = holonomy[i, j]
                    rotation[i, j] += 0.070 * dmg
                    rotation[j, i] = -rotation[i, j]
        addressability = np.clip(addressability, 0.0, 1.0)

        # Endogenous targeted unlock trigger.
        if intervention and t >= 50 and t % 10 == 0 and len(hist) >= 4:
            e1 = [x for x in hist if t - 25 <= x["t"] < t - 10]
            e2 = [x for x in hist if t - 10 <= x["t"] <= t]
            if e1 and e2:
                fs1 = float(np.mean([x["field_strain"] for x in e1]))
                fs2 = float(np.mean([x["field_strain"] for x in e2]))
                m2 = float(np.mean([x["mobility2"] for x in e2]))
                raw = float(np.mean([x["changed"] * max(x["saving"], 0.0) for x in e2]))
                if (fs2 - fs1 > 0.006 and m2 < 0.20) or (fs2 > 0.48 and raw < 0.14):
                    active_until = max(active_until, t + 18)
                    trigger_events += 1

        boost_global = intervention and (t <= active_until)

        # Base repair and registration.
        repair_power = np.array(
            [
                addressability[i] * (0.35 + (np.mean(register[i, neigh[i]]) if len(neigh[i]) else 0.0))
                for i in range(n_nodes)
            ]
        )
        for i, j in edges:
            boost = 1.15 if boost_global else 1.0
            imp = 0.5 * (repair_power[i] + repair_power[j])
            holonomy[i, j] *= max(0.0, 1.0 - 0.012 * repair * boost * (repair_power[i] + repair_power[j]))
            holonomy[j, i] = holonomy[i, j]
            rotation[i, j] *= max(0.0, 1.0 - 0.0085 * repair * boost * (repair_power[i] + repair_power[j]))
            rotation[j, i] = -rotation[i, j]
            register[i, j] += 0.021 * repair * imp - 0.0023 * decay * register[i, j]
            register[j, i] = register[i, j]
        register = np.clip(register, 0.0, 1.0)

        cost_index = 0 if t < 48 else 1
        paths = [shortest_path(a, b, cost_index)[1] for a, b in pairs]
        load *= 0.945
        route_memory *= 0.987
        for p in paths:
            for u, v in zip(p[:-1], p[1:]):
                load[u, v] += 0.03
                load[v, u] = load[u, v]
                route_memory[u, v] += 0.017
                route_memory[v, u] = route_memory[u, v]
                rotation[u, v] += 0.012 * congestion * max(0.0, load[u, v] - 0.1)
                rotation[v, u] = -rotation[u, v]

        # Action-memory update: reward lower-action corridors; slightly decay abandoned metric-only routes.
        if t >= 55 and t % 10 == 0:
            for a, b in pairs:
                _, metric_path = shortest_path(a, b, 0)
                _, action_path = shortest_path(a, b, 1)
                me = path_edges(metric_path)
                ae = path_edges(action_path)
                action_only = ae - me
                metric_only = me - ae
                if action_only:
                    mt = path_sum(metric_path)
                    at = path_sum(action_path)
                    saving = mt[1] - at[1]
                    strain = (mt[1] - mt[0]) - (at[1] - at[0])
                    if saving > 0 and strain > 0:
                        for u, v in action_only:
                            register[u, v] += 0.0022 * np.tanh(saving)
                            register[v, u] = register[u, v]
                        for u, v in metric_only:
                            register[u, v] *= 1.0 - 0.0016 * decay * np.tanh(strain) * np.tanh(saving)
                            register[v, u] = register[u, v]

        # Targeted unlocking: only a small high-risk edge subset.
        if boost_global:
            risks = []
            for i, j in edges:
                _, _, _, _, _, r, field, _ = edge_terms(i, j)
                risk = field * (1.0 - r) * (1.0 + 0.5 * ((i, j) in scar_edges))
                risks.append((risk, i, j))
            risks.sort(reverse=True)
            k = max(1, int(0.12 * len(edges)))
            for risk, i, j in risks[:k]:
                if risk > 0.12:
                    holonomy[i, j] *= 0.965
                    holonomy[j, i] = holonomy[i, j]
                    rotation[i, j] *= 0.965
                    rotation[j, i] = -rotation[i, j]
                    register[i, j] += 0.006 * np.tanh(risk)
                    register[j, i] = register[i, j]
                    targeted_updates += 1

        # Congestion backreaction and addressability recovery.
        for i, j in edges:
            holonomy[i, j] += 0.017 * congestion * max(0.0, load[i, j] - 0.1)
            holonomy[j, i] = holonomy[i, j]
            register[i, j] += 0.0018 * route_memory[i, j]
            register[j, i] = register[i, j]
        register = np.clip(register, 0.0, 1.0)

        addressability = np.clip(
            addressability
            + 0.0055
            * repair
            * np.array([np.mean(register[i, neigh[i]]) if len(neigh[i]) else 0.0 for i in range(n_nodes)]),
            0.0,
            1.0,
        )

        if t % 5 == 0:
            hist.append(sample(t))

    pre = [x for x in hist if 20 <= x["t"] < 35]
    late = [x for x in hist if x["t"] >= 220]
    mid = [x for x in hist if 120 <= x["t"] < 160]

    def avg(xs: List[Dict[str, float]], key: str) -> float:
        return float(np.mean([x[key] for x in xs])) if xs else 0.0

    pre_fs = avg(pre, "field_strain")
    pre_action = avg(pre, "action")
    late_fs = avg(late, "field_strain")
    late_action = avg(late, "action")
    residual = max(late_fs - pre_fs, 0.0) + 0.5 * max(late_action - pre_action, 0.0)

    return {
        "residual": residual,
        "late_fs": late_fs,
        "late_action": late_action,
        "late_M2": avg(late, "mobility2"),
        "late_changed": avg(late, "changed"),
        "late_saving": avg(late, "saving"),
        "scar_field_ratio": avg(late, "scar_field") / (avg(late, "non_field") + EPS),
        "scar_action_ratio": avg(late, "scar_action") / (avg(late, "non_action") + EPS),
        "scar_avoidance": avg(late, "scar_path_metric") - avg(late, "scar_path_action"),
        "slope_field": late_fs - avg(mid, "field_strain"),
        "slope_action": late_action - avg(mid, "action"),
        "triggers": float(trigger_events),
        "updates": float(targeted_updates),
    }


def build_validation_cases(n_cases: int = 40, seed: int = 222) -> List[CaseResult]:
    rng = np.random.default_rng(seed)
    separations = ["far", "near", "cluster"]
    clustering = {"far": 0.75, "near": 1.00, "cluster": 1.35}
    rows: List[CaseResult] = []

    for idx in range(n_cases):
        shock = float(rng.uniform(0.80, 1.70))
        repair = float(rng.uniform(0.72, 1.62))
        decay = float(rng.uniform(0.74, 0.98))
        congestion = float(rng.uniform(0.75, 1.90))
        cycles = int(rng.choice([2, 3, 4, 5, 6, 7, 8]))
        separation = str(rng.choice(separations, p=[0.34, 0.33, 0.33]))
        case_seed = 70000 + idx * 23

        q = run_atlas_case(
            case_seed,
            intervention=True,
            shock=shock,
            separation=separation,
            repair=repair,
            decay=decay,
            congestion=congestion,
            cycles=cycles,
        )

        # Bounded/self-healed outcome definition.
        passed = bool(q["residual"] < 1.10 and q["late_fs"] < 0.95 and q["late_action"] < 3.80 and q["late_M2"] > 0.05)

        c_base = (repair * decay) / (shock * congestion * clustering[separation] * cycles)
        c_star_scaled = 100.0 * c_base * q["late_M2"]

        rows.append(
            CaseResult(
                passed=passed,
                residual=float(q["residual"]),
                late_field_strain=float(q["late_fs"]),
                late_action=float(q["late_action"]),
                late_mobility2=float(q["late_M2"]),
                c_star_scaled=float(c_star_scaled),
                shock=shock,
                repair=repair,
                decay=decay,
                congestion=congestion,
                cycles=cycles,
                separation=separation,
            )
        )
    return rows


def main() -> None:
    rows = build_validation_cases(n_cases=40, seed=222)
    calibration = rows[:20]
    validation = rows[20:]

    y_cal = np.array([r.passed for r in calibration])
    s_cal = np.array([r.c_star_scaled for r in calibration])
    cal_bal, cal_acc, c_critical = best_threshold(s_cal, y_cal, greater=True)

    for r in rows:
        r.c_norm = r.c_star_scaled / c_critical

    def report_split(name: str, data: List[CaseResult]) -> None:
        truth = np.array([r.passed for r in data])
        pred = np.array([r.c_norm > 1.0 for r in data])
        tp = int(((pred == 1) & (truth == 1)).sum())
        tn = int(((pred == 0) & (truth == 0)).sum())
        fp = int(((pred == 1) & (truth == 0)).sum())
        fn = int(((pred == 0) & (truth == 1)).sum())
        print(f"\n{name}")
        print("-" * len(name))
        print(f"n={len(data)} pass={int(truth.sum())} fail={int((~truth).sum())}")
        print(f"C_norm > 1 balanced_accuracy={balanced_accuracy(pred, truth):.3f} overall_accuracy={(pred == truth).mean():.3f}")
        print(f"confusion: TP={tp} TN={tn} FP={fp} FN={fn}")
        for lo, hi in [(0, 0.5), (0.5, 0.8), (0.8, 1.2), (1.2, 2.0), (2.0, 999.0)]:
            sub = [r for r in data if lo <= r.c_norm < hi]
            if sub:
                print(
                    f"  C_norm {lo:>3}-{hi:<5}: n={len(sub):2d} "
                    f"pass_rate={np.mean([r.passed for r in sub]):.3f} "
                    f"residual={np.mean([r.residual for r in sub]):.3f} "
                    f"action={np.mean([r.late_action for r in sub]):.3f} "
                    f"field={np.mean([r.late_field_strain for r in sub]):.3f}"
                )

    print("Retained Atlas Capacity Law Validation")
    print("======================================")
    print(f"Calibrated C*_critical={c_critical:.6f}")
    print(f"Calibration split: balanced_accuracy={cal_bal:.3f}, overall_accuracy={cal_acc:.3f}")

    report_split("Calibration split", calibration)
    report_split("Fresh validation split", validation)
    report_split("All cases", rows)

    pass_c = np.array([r.c_norm for r in rows if r.passed])
    fail_c = np.array([r.c_norm for r in rows if not r.passed])
    print("\nSummary")
    print("-------")
    print(f"mean C_norm pass={pass_c.mean():.3f}, fail={fail_c.mean():.3f}")
    print(f"median C_norm pass={np.median(pass_c):.3f}, fail={np.median(fail_c):.3f}")
    print("\nBounded interpretation:")
    print("  C_norm > 1    -> self-healing geometry usually holds")
    print("  C_norm ~ 1    -> transition/plastic adaptation band")
    print("  C_norm < 1    -> frozen scar/capacity failure likely")
    print("\nThis is a toy-model capacity law, not a GR derivation or physical validation.")


if __name__ == "__main__":
    main()
