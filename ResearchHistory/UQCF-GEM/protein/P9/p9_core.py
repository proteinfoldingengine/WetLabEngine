from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Iterable

import torch

torch.set_default_dtype(torch.float64)

ROOT = Path(__file__).resolve().parent
P1_DIR = ROOT.parent / "P1"
P5_DIR = ROOT.parent / "P5"
P6_DIR = ROOT.parent / "P6"
for path in (P1_DIR, P5_DIR, P6_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import p1_core as p1
import p5_core as p5
import p6_core as p6

TARGET_NAMES = ("1VII", "1L2Y", "1UAO", "1CRN")
SEEDS = tuple(range(6))
CHECKPOINTS = (50, 100, 150, 200)
GENERATOR_STEPS = 200
HANDOFF_STEPS = 100
LEARNING_RATE = p6.LEARNING_RATE
PRIMARY_SCORES = ("closure_ready", "flat_primary", "flat_secondary")


def load_target(name: str) -> p6.Target:
    if name in p6.TARGET_NAMES:
        return p6.load_target(name)
    if name == "1CRN":
        source = p5.load_target("1CRN")
        return p6.Target(
            name="1CRN",
            sequence=source.sequence,
            native_ca=source.native_ca.detach().clone().to(dtype=torch.float64),
        )
    raise KeyError(name)


def expected_state_keys() -> list[tuple[str, int, int]]:
    return [
        (target, seed, checkpoint)
        for target in TARGET_NAMES
        for seed in SEEDS
        for checkpoint in CHECKPOINTS
    ]


def _reconstruct(
    target: p6.Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
) -> tuple[p6.CanonicalGeometry, torch.Tensor, torch.Tensor, torch.Tensor]:
    geometry = p6.canonical_geometry(len(target.sequence))
    phi = torch.cat([geometry.phi[:1], phi_free])
    n, ca, c = p6.reconstruct_backbone(geometry, phi, psi)
    return geometry, n, ca, c


def p6_objective_from_state(
    target: p6.Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
):
    return p6.objective(
        target,
        phi_free,
        psi,
        "physical_real_sequence",
        generic_scale=1.0,
    )


def coherence_scores(ca: torch.Tensor) -> dict[str, float]:
    ctx = p1.FoldContext(
        torch.zeros((int(ca.shape[0]), 3), dtype=ca.dtype, device=ca.device),
        "p9_native_blind",
    )
    obs = p1.bridge_observables(ca, ctx)
    values = {
        key: float(value.detach())
        for key, value in obs.items()
    }

    r_micro = math.exp(
        -(
            0.60 * values["dir_pen"]
            + 0.20 * values["angle_var"]
            + 0.26 * values["dihed_smooth"]
        )
    )
    compactness = math.exp(-0.12 * values["rg"])
    c_meso_logit = (
        1.8 * (values["soft_contacts"] - 0.40)
        - 0.42 * values["density_var"]
        + 0.8 * compactness
    )
    c_meso = 1.0 / (1.0 + math.exp(-c_meso_logit))
    flat_primary = (
        0.36 * r_micro
        + 0.24 * c_meso
        + 0.40 * values["loop_compat"]
    )
    flat_secondary = (
        0.32 * r_micro
        + 0.20 * c_meso
        + 0.48 * values["loop_compat"]
    )

    values.update(
        {
            "R_micro": r_micro,
            "compactness": compactness,
            "C_meso": c_meso,
            "flat_primary": flat_primary,
            "flat_secondary": flat_secondary,
        }
    )
    return values


def native_contact_recall(
    model_ca: torch.Tensor,
    native_ca: torch.Tensor,
) -> float:
    native_d = torch.cdist(native_ca, native_ca)
    model_d = torch.cdist(model_ca, model_ca)
    pairs = [
        (i, j)
        for i in range(native_ca.shape[0])
        for j in range(
            i + p6.CONTACT_MIN_SEQ_SEPARATION,
            native_ca.shape[0],
        )
        if float(native_d[i, j]) < p6.NATIVE_CONTACT_CUTOFF_A
    ]
    if not pairs:
        return float("nan")
    return (
        sum(
            float(model_d[i, j]) < p6.NATIVE_CONTACT_CUTOFF_A
            for i, j in pairs
        )
        / len(pairs)
    )


def generate_state_bank(
    target: p6.Target,
    *,
    seed: int,
) -> dict[int, tuple[torch.Tensor, torch.Tensor]]:
    torch.use_deterministic_algorithms(True)
    phi0, psi0 = p6.initial_torsions(len(target.sequence), seed)
    phi_free = torch.nn.Parameter(phi0.detach().clone())
    psi = torch.nn.Parameter(psi0.detach().clone())
    optimizer = torch.optim.Adam([phi_free, psi], lr=LEARNING_RATE)

    snapshots: dict[int, tuple[torch.Tensor, torch.Tensor]] = {}

    for completed in range(1, GENERATOR_STEPS + 1):
        optimizer.zero_grad(set_to_none=True)
        energy, (_, ca, _), _ = p6_objective_from_state(
            target, phi_free, psi
        )
        if not bool(torch.isfinite(energy)) or not bool(torch.isfinite(ca).all()):
            raise FloatingPointError(
                f"nonfinite generator state target={target.name} seed={seed} step={completed - 1}"
            )
        energy.backward()
        if (
            phi_free.grad is None
            or psi.grad is None
            or not bool(torch.isfinite(phi_free.grad).all())
            or not bool(torch.isfinite(psi.grad).all())
        ):
            raise FloatingPointError(
                f"nonfinite generator gradient target={target.name} seed={seed} step={completed - 1}"
            )
        optimizer.step()
        with torch.no_grad():
            phi_free.copy_(p6.wrap_angle(phi_free))
            psi.copy_(p6.wrap_angle(psi))

        if completed in CHECKPOINTS:
            snapshots[completed] = (
                phi_free.detach().clone(),
                psi.detach().clone(),
            )

    if tuple(sorted(snapshots)) != CHECKPOINTS:
        raise AssertionError(tuple(sorted(snapshots)))
    return snapshots


def _evaluate_state(
    target: p6.Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
) -> dict[str, float]:
    geometry, n, ca, c = _reconstruct(target, phi_free, psi)
    precision, k = p6.topk_native_contact_precision(ca, target.native_ca)
    modeled_rg = p6.radius_of_gyration(ca)
    native_rg = p6.radius_of_gyration(target.native_ca)
    length_drift, angle_drift = p6.covalent_drift(
        geometry, n, ca, c
    )
    return {
        "ca_rmsd_A": p6.kabsch_rmsd(ca, target.native_ca),
        "topk_native_contact_precision": precision,
        "topk_contact_budget": float(k),
        "native_contact_recall": native_contact_recall(
            ca, target.native_ca
        ),
        "rg_A": modeled_rg,
        "native_rg_A": native_rg,
        "rg_ratio": modeled_rg / native_rg,
        "bond_length_drift_A": float(length_drift),
        "bond_angle_drift_rad": float(angle_drift),
    }


def run_handoff(
    target: p6.Target,
    phi_free_state: torch.Tensor,
    psi_state: torch.Tensor,
) -> dict[str, object]:
    torch.use_deterministic_algorithms(True)
    phi_free = torch.nn.Parameter(phi_free_state.detach().clone())
    psi = torch.nn.Parameter(psi_state.detach().clone())
    optimizer = torch.optim.Adam([phi_free, psi], lr=LEARNING_RATE)

    start = _evaluate_state(target, phi_free.detach(), psi.detach())
    best_rmsd = float("inf")
    best_precision = -float("inf")
    max_length_drift = 0.0
    max_angle_drift = 0.0
    failed = False
    failure_reason = ""
    completed_steps = 0
    last_eval = start
    last_components: dict[str, float] = {}

    for completed in range(1, HANDOFF_STEPS + 1):
        optimizer.zero_grad(set_to_none=True)
        energy, (_, ca, _), components = p6_objective_from_state(
            target, phi_free, psi
        )
        if not bool(torch.isfinite(energy)) or not bool(torch.isfinite(ca).all()):
            failed = True
            failure_reason = f"nonfinite_energy_or_coords_step_{completed - 1}"
            break

        energy.backward()
        if (
            phi_free.grad is None
            or psi.grad is None
            or not bool(torch.isfinite(phi_free.grad).all())
            or not bool(torch.isfinite(psi.grad).all())
        ):
            failed = True
            failure_reason = f"nonfinite_gradient_step_{completed - 1}"
            break

        optimizer.step()
        with torch.no_grad():
            phi_free.copy_(p6.wrap_angle(phi_free))
            psi.copy_(p6.wrap_angle(psi))

        completed_steps = completed
        current = _evaluate_state(
            target,
            phi_free.detach(),
            psi.detach(),
        )
        best_rmsd = min(best_rmsd, float(current["ca_rmsd_A"]))
        best_precision = max(
            best_precision,
            float(current["topk_native_contact_precision"]),
        )
        max_length_drift = max(
            max_length_drift,
            float(current["bond_length_drift_A"]),
        )
        max_angle_drift = max(
            max_angle_drift,
            float(current["bond_angle_drift_rad"]),
        )
        last_eval = current
        last_components = components

    if best_rmsd == float("inf"):
        best_rmsd = float(start["ca_rmsd_A"])
    if best_precision == -float("inf"):
        best_precision = float(start["topk_native_contact_precision"])

    out: dict[str, object] = {
        "start_ca_rmsd_A": float(start["ca_rmsd_A"]),
        "best_handoff_ca_rmsd_A": float(best_rmsd),
        "best_handoff_topk_native_contact_precision": float(best_precision),
        "final_ca_rmsd_A": float(last_eval["ca_rmsd_A"]),
        "final_topk_native_contact_precision": float(
            last_eval["topk_native_contact_precision"]
        ),
        "final_topk_contact_budget": int(
            last_eval["topk_contact_budget"]
        ),
        "final_native_contact_recall": float(
            last_eval["native_contact_recall"]
        ),
        "final_rg_A": float(last_eval["rg_A"]),
        "native_rg_A": float(last_eval["native_rg_A"]),
        "final_rg_ratio": float(last_eval["rg_ratio"]),
        "max_bond_length_drift_A": max_length_drift,
        "max_bond_angle_drift_rad": max_angle_drift,
        "failed": failed,
        "failure_reason": failure_reason,
        "final_step": completed_steps,
    }
    for key, value in last_components.items():
        out[f"final_energy_{key}"] = value
    return out


def _average_ranks(values: Iterable[float]) -> list[float]:
    vals = [float(v) for v in values]
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and vals[order[j]] == vals[order[i]]:
            j += 1
        average = ((i + 1) + j) / 2.0
        for pos in range(i, j):
            ranks[order[pos]] = average
        i = j
    return ranks


def spearman_rank(
    x: Iterable[float],
    y: Iterable[float],
) -> float:
    rx = _average_ranks(x)
    ry = _average_ranks(y)
    if len(rx) != len(ry) or len(rx) < 2:
        raise ValueError("matched rank vectors with length >=2 required")
    mx = sum(rx) / len(rx)
    my = sum(ry) / len(ry)
    dx = [v - mx for v in rx]
    dy = [v - my for v in ry]
    vx = sum(v * v for v in dx)
    vy = sum(v * v for v in dy)
    if vx <= 0.0 or vy <= 0.0:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(vx * vy)


def exact_sign_flip_p(differences: Iterable[float]) -> float:
    values = [float(v) for v in differences]
    if not values:
        raise ValueError("empty differences")
    observed = abs(sum(values) / len(values))
    total = 1 << len(values)
    extreme = 0
    for bits in range(total):
        signed = 0.0
        for index, value in enumerate(values):
            signed += value if ((bits >> index) & 1) else -value
        statistic = abs(signed / len(values))
        if statistic + 1e-15 >= observed:
            extreme += 1
    return extreme / total


def holm_two(p1_value: float, p2_value: float) -> tuple[float, float]:
    values = [(float(p1_value), 0), (float(p2_value), 1)]
    values.sort()
    adjusted = [0.0, 0.0]
    first = min(1.0, 2.0 * values[0][0])
    second = min(1.0, max(first, values[1][0]))
    adjusted[values[0][1]] = first
    adjusted[values[1][1]] = second
    return adjusted[0], adjusted[1]


def formula_selfcheck() -> bool:
    target = load_target("1VII")
    phi_free, psi = p6.initial_torsions(len(target.sequence), seed=0)
    _, (_, ca, _), _ = p6_objective_from_state(
        target, phi_free, psi
    )
    score = coherence_scores(ca)
    ctx = p1.FoldContext(
        torch.zeros((ca.shape[0], 3), dtype=ca.dtype),
        "formula_check",
    )
    obs = p1.bridge_observables(ca, ctx)
    return (
        abs(score["sigma_bridge"] - float(obs["sigma_bridge"])) < 1e-12
        and abs(score["closure_ready"] - float(obs["closure_ready"])) < 1e-12
    )


def native_firewall_selfcheck() -> bool:
    target = load_target("1L2Y")
    phi_free, psi = p6.initial_torsions(len(target.sequence), seed=2)
    e0, (_, ca0, _), _ = p6_objective_from_state(
        target, phi_free, psi
    )
    s0 = coherence_scores(ca0)
    changed = p6.Target(
        name=target.name,
        sequence=target.sequence,
        native_ca=target.native_ca * 11.0 + 777.0,
    )
    e1, (_, ca1, _), _ = p6_objective_from_state(
        changed, phi_free, psi
    )
    s1 = coherence_scores(ca1)
    if abs(float(e0) - float(e1)) >= 1e-12:
        return False
    if not torch.allclose(ca0, ca1, rtol=0.0, atol=1e-12):
        return False
    return all(
        abs(s0[key] - s1[key]) < 1e-12
        for key in PRIMARY_SCORES
    )


def _group_correlations(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    for target in TARGET_NAMES:
        for checkpoint in CHECKPOINTS:
            subset = [
                row
                for row in rows
                if row["target"] == target
                and int(row["checkpoint"]) == checkpoint
            ]
            if len(subset) != len(SEEDS):
                continue
            future_quality = [
                -float(row["best_handoff_ca_rmsd_A"])
                for row in subset
            ]
            groups.append(
                {
                    "target": target,
                    "checkpoint": checkpoint,
                    **{
                        f"spearman_{score}": spearman_rank(
                            [float(row[score]) for row in subset],
                            future_quality,
                        )
                        for score in PRIMARY_SCORES
                    },
                }
            )
    return groups


def adjudicate(rows: list[dict[str, object]]) -> dict[str, object]:
    observed = [
        (
            str(row["target"]),
            int(row["seed"]),
            int(row["checkpoint"]),
        )
        for row in rows
    ]
    expected = expected_state_keys()
    matrix_complete = (
        len(observed) == len(expected)
        and len(set(observed)) == len(expected)
        and set(observed) == set(expected)
    )

    groups = _group_correlations(rows) if matrix_complete else []
    if len(groups) != len(TARGET_NAMES) * len(CHECKPOINTS):
        matrix_complete = False

    score_means = {
        score: (
            sum(float(g[f"spearman_{score}"]) for g in groups)
            / len(groups)
            if groups
            else float("nan")
        )
        for score in PRIMARY_SCORES
    }

    controls = ("flat_primary", "flat_secondary")
    comparison_rows: list[dict[str, object]] = []
    raw_p: list[float] = []
    target_deltas: dict[str, dict[str, float]] = {}

    if groups:
        for control in controls:
            diffs = [
                float(g["spearman_closure_ready"])
                - float(g[f"spearman_{control}"])
                for g in groups
            ]
            p_value = exact_sign_flip_p(diffs)
            raw_p.append(p_value)
            target_deltas[control] = {
                target: sum(
                    float(g["spearman_closure_ready"])
                    - float(g[f"spearman_{control}"])
                    for g in groups
                    if g["target"] == target
                )
                / len(CHECKPOINTS)
                for target in TARGET_NAMES
            }
            comparison_rows.append(
                {
                    "comparison": f"closure_ready_vs_{control}",
                    "n_groups": len(diffs),
                    "mean_spearman_delta": sum(diffs) / len(diffs),
                    "raw_exact_sign_flip_p": p_value,
                    **{
                        f"{target}_mean_spearman_delta":
                            target_deltas[control][target]
                        for target in TARGET_NAMES
                    },
                }
            )
        adjusted = holm_two(raw_p[0], raw_p[1])
        for row, value in zip(comparison_rows, adjusted):
            row["holm_adjusted_p"] = value
    else:
        adjusted = (1.0, 1.0)

    target_candidate_means = {
        target: (
            sum(
                float(g["spearman_closure_ready"])
                for g in groups
                if g["target"] == target
            )
            / len(CHECKPOINTS)
            if groups
            else float("nan")
        )
        for target in TARGET_NAMES
    }

    geometry_good = matrix_complete and all(
        float(row["max_bond_length_drift_A"]) < 1e-8
        and float(row["max_bond_angle_drift_rad"]) < 1e-8
        for row in rows
    )
    numerical_good = matrix_complete and all(
        not bool(row["failed"])
        and int(row["final_step"]) == HANDOFF_STEPS
        and math.isfinite(float(row["best_handoff_ca_rmsd_A"]))
        for row in rows
    )

    conditions = {
        "complete_unique_96_state_matrix": matrix_complete,
        "mean_candidate_group_spearman_at_least_0_35": (
            matrix_complete
            and score_means["closure_ready"] >= 0.35
        ),
        "candidate_mean_exceeds_both_flattened_controls": (
            matrix_complete
            and all(
                score_means["closure_ready"] > score_means[control]
                for control in controls
            )
        ),
        "candidate_positive_on_every_target": (
            matrix_complete
            and all(
                target_candidate_means[target] > 0.0
                for target in TARGET_NAMES
            )
        ),
        "candidate_minus_control_positive_every_target": (
            matrix_complete
            and all(
                target_deltas[control][target] > 0.0
                for control in controls
                for target in TARGET_NAMES
            )
        ),
        "both_holm_adjusted_p_lt_0_05": (
            matrix_complete
            and all(value < 0.05 for value in adjusted)
        ),
        "all_runs_preserve_canonical_covalent_geometry": geometry_good,
        "all_runs_numerically_healthy": numerical_good,
        "native_information_firewall_passed": native_firewall_selfcheck(),
        "frozen_v9_formula_reproduction_passed": formula_selfcheck(),
    }

    decision = (
        "GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE"
        if all(conditions.values())
        else "NO_GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE"
    )
    return {
        "decision": decision,
        "conditions": conditions,
        "score_mean_group_spearman": score_means,
        "candidate_target_mean_spearman": target_candidate_means,
        "primary_comparisons": comparison_rows,
        "group_correlations": groups,
        "claim_boundary": (
            "A GO establishes only that the frozen v9 hierarchical "
            "multiscale compression is a compact transferable predictor "
            "of downstream ordinary-relaxation quality beyond two "
            "flattened same-information controls on this benchmark."
        ),
    }


def synthetic_acceptance_fixture(*, go: bool) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in TARGET_NAMES:
        for checkpoint in CHECKPOINTS:
            for seed in SEEDS:
                if go:
                    closure = float(seed)
                    flat_primary = float(-seed)
                    flat_secondary = float(5 - seed)
                    future_quality = float(seed)
                else:
                    closure = float(-seed)
                    flat_primary = float(seed)
                    flat_secondary = float(seed)
                    future_quality = float(seed)
                rows.append(
                    {
                        "target": target,
                        "seed": seed,
                        "checkpoint": checkpoint,
                        "closure_ready": closure,
                        "flat_primary": flat_primary,
                        "flat_secondary": flat_secondary,
                        "best_handoff_ca_rmsd_A": 20.0 - future_quality,
                        "max_bond_length_drift_A": 1e-12,
                        "max_bond_angle_drift_rad": 1e-12,
                        "failed": False,
                        "final_step": HANDOFF_STEPS,
                    }
                )
    return rows
