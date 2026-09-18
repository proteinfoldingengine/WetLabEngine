from __future__ import annotations

import csv
import json
import math
import os
import statistics
from dataclasses import replace
from pathlib import Path

import torch

import p6_core as p6

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "measurement_output"
CHECKPOINTS = (0, 50, 100, 200, p6.STEPS)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _parse_evaluator_backbone(name: str) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    path = p6.TARGET_PATHS[name]
    rows: dict[tuple[str, int, str], dict[str, tuple[float, float, float]]] = {}
    order: list[tuple[str, int, str]] = []
    for line in p6._first_model_records(path):
        if (
            not line.startswith("ATOM")
            or len(line) < 54
            or line[21:22] != "A"
            or line[16:17] not in (" ", "A")
        ):
            continue
        atom = line[12:16].strip()
        if atom not in ("N", "CA", "C"):
            continue
        key = (line[21:22], int(line[22:26]), line[26:27].strip())
        if key not in rows:
            rows[key] = {}
            order.append(key)
        rows[key].setdefault(
            atom,
            (
                float(line[30:38]),
                float(line[38:46]),
                float(line[46:54]),
            ),
        )
    complete = [key for key in order if all(a in rows[key] for a in ("N", "CA", "C"))]
    if len(complete) != p6.EXPECTED_LENGTHS[name]:
        raise ValueError(f"{name}: incomplete evaluator backbone")
    n = torch.tensor([rows[key]["N"] for key in complete], dtype=torch.float64)
    ca = torch.tensor([rows[key]["CA"] for key in complete], dtype=torch.float64)
    c = torch.tensor([rows[key]["C"] for key in complete], dtype=torch.float64)
    return n, ca, c


def _dihedral(
    a: torch.Tensor,
    b: torch.Tensor,
    c: torch.Tensor,
    d: torch.Tensor,
) -> torch.Tensor:
    b1 = b - a
    b2 = c - b
    b3 = d - c
    n1 = p6._safe_normalize(torch.cross(b1, b2, dim=-1))
    n2 = p6._safe_normalize(torch.cross(b2, b3, dim=-1))
    b2n = p6._safe_normalize(b2)
    x = (n1 * n2).sum(dim=-1)
    y = (torch.cross(n1, b2n, dim=-1) * n2).sum(dim=-1)
    return torch.atan2(-y, x)


def native_torsions(name: str) -> tuple[torch.Tensor, torch.Tensor]:
    n, ca, c = _parse_evaluator_backbone(name)
    phi = _dihedral(c[:-1], n[1:], ca[1:], c[1:])
    psi = _dihedral(n[:-1], ca[:-1], c[:-1], n[1:])
    return phi, psi


def native_torsion_rmse(
    name: str,
    phi: torch.Tensor,
    psi: torch.Tensor,
) -> float:
    native_phi, native_psi = native_torsions(name)
    if phi.numel() < 3:
        return float("nan")
    # Compare the N-2 shared interior torsions only.
    model_phi = phi[1:-1]
    model_psi = psi[1:]
    ref_phi = native_phi[:-1]
    ref_psi = native_psi[1:]
    dphi = p6.wrap_angle(model_phi - ref_phi)
    dpsi = p6.wrap_angle(model_psi - ref_psi)
    return float(torch.sqrt(torch.mean(torch.cat([dphi * dphi, dpsi * dpsi]))))


def native_contact_recall(model_ca: torch.Tensor, native_ca: torch.Tensor) -> float:
    model_d = torch.cdist(model_ca, model_ca)
    native_d = torch.cdist(native_ca, native_ca)
    pairs = [
        (i, j)
        for i in range(native_ca.shape[0])
        for j in range(i + p6.CONTACT_MIN_SEQ_SEPARATION, native_ca.shape[0])
        if float(native_d[i, j]) < p6.NATIVE_CONTACT_CUTOFF_A
    ]
    if not pairs:
        return float("nan")
    hits = sum(float(model_d[i, j]) < p6.NATIVE_CONTACT_CUTOFF_A for i, j in pairs)
    return hits / len(pairs)


def _hbond_count(
    n: torch.Tensor,
    ca: torch.Tensor,
    c: torch.Tensor,
    sequence: str,
) -> int:
    # Secondary diagnostic only: DSSP-like favorable pair energy < -0.5 kcal/mol.
    oxygens = [
        p6._virtual_oxygen(ca[i], c[i], n[i + 1])
        for i in range(len(sequence) - 1)
    ]
    hydrogens = {
        i: p6._virtual_hydrogen(c[i - 1], n[i], ca[i])
        for i in range(1, len(sequence))
        if sequence[i] != "P"
    }
    count = 0
    for donor_i, h in hydrogens.items():
        for acceptor_i, o in enumerate(oxygens):
            if abs(donor_i - acceptor_i) < p6.HBOND_MIN_SEP:
                continue
            r_on = torch.clamp(torch.linalg.norm(o - n[donor_i]), min=p6.HBOND_DISTANCE_FLOOR_A)
            r_ch = torch.clamp(torch.linalg.norm(c[acceptor_i] - h), min=p6.HBOND_DISTANCE_FLOOR_A)
            r_oh = torch.clamp(torch.linalg.norm(o - h), min=p6.HBOND_DISTANCE_FLOOR_A)
            r_cn = torch.clamp(torch.linalg.norm(c[acceptor_i] - n[donor_i]), min=p6.HBOND_DISTANCE_FLOOR_A)
            e = p6.HBOND_COEFF * (1.0 / r_on + 1.0 / r_ch - 1.0 / r_oh - 1.0 / r_cn)
            if float(e.detach()) < -0.5:
                count += 1
    return count


def _hydrophobic_contact_count(ca: torch.Tensor, sequence: str) -> int:
    d = torch.cdist(ca, ca)
    count = 0
    for i in range(len(sequence)):
        if p6.HYDROPATHY[sequence[i]] <= 0:
            continue
        for j in range(i + 3, len(sequence)):
            if p6.HYDROPATHY[sequence[j]] > 0 and float(d[i, j]) < p6.CONTACT_MIDPOINT_A:
                count += 1
    return count


def _evaluate_snapshot(
    target: p6.Target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    mode: str,
    generic_scale: float,
    step: int,
) -> dict[str, object]:
    geometry = p6.canonical_geometry(len(target.sequence))
    phi = torch.cat([geometry.phi[:1], phi_free])
    n, ca, c = p6.reconstruct_backbone(geometry, phi, psi)
    precision, k = p6.topk_native_contact_precision(ca, target.native_ca)
    dl, da = p6.covalent_drift(geometry, n, ca, c)
    sequence_labels = (
        p6.shuffled_sequence(target.name)
        if mode == "physical_shuffled_sequence"
        else target.sequence
    )
    return {
        "target": target.name,
        "mode": mode,
        "step": step,
        "topk_native_contact_precision": precision,
        "topk_contact_budget": k,
        "ca_rmsd_A": p6.kabsch_rmsd(ca, target.native_ca),
        "contact_recall": native_contact_recall(ca, target.native_ca),
        "rg_A": p6.radius_of_gyration(ca),
        "native_rg_A": p6.radius_of_gyration(target.native_ca),
        "rg_ratio": p6.radius_of_gyration(ca) / p6.radius_of_gyration(target.native_ca),
        "native_torsion_rmse_rad": native_torsion_rmse(target.name, phi, psi),
        "hbond_count_secondary": _hbond_count(n, ca, c, target.sequence),
        "hydrophobic_contact_count_secondary": _hydrophobic_contact_count(ca, sequence_labels),
        "max_bond_length_drift_A": dl,
        "max_bond_angle_drift_rad": da,
        "generic_collapse_scale": generic_scale,
    }


def run_one(target_name: str, seed: int, mode: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    target = p6.load_target(target_name)
    phi0, psi0 = p6.initial_torsions(len(target.sequence), seed)
    generic_scale = p6.generic_collapse_scale(target.sequence, phi0, psi0)

    phi_free = phi0.clone().requires_grad_(True)
    psi = psi0.clone().requires_grad_(True)
    optimizer = torch.optim.Adam([phi_free, psi], lr=p6.LEARNING_RATE)

    snapshots: dict[int, tuple[torch.Tensor, torch.Tensor]] = {
        0: (phi_free.detach().clone(), psi.detach().clone())
    }
    last_components: dict[str, float] = {}
    failed = False
    failure_reason = ""

    for step in range(1, p6.STEPS + 1):
        optimizer.zero_grad(set_to_none=True)
        energy, coords, components = p6.objective(
            target,
            phi_free,
            psi,
            mode,
            generic_scale=generic_scale,
        )
        if not bool(torch.isfinite(energy)):
            failed = True
            failure_reason = f"nonfinite_energy_step_{step}"
            break
        energy.backward()
        if (
            phi_free.grad is None
            or psi.grad is None
            or not bool(torch.isfinite(phi_free.grad).all())
            or not bool(torch.isfinite(psi.grad).all())
        ):
            failed = True
            failure_reason = f"nonfinite_gradient_step_{step}"
            break
        optimizer.step()
        with torch.no_grad():
            phi_free.copy_(p6.wrap_angle(phi_free))
            psi.copy_(p6.wrap_angle(psi))
        if not all(bool(torch.isfinite(x).all()) for x in coords):
            failed = True
            failure_reason = f"nonfinite_coordinates_step_{step}"
            break
        last_components = components
        if step in CHECKPOINTS:
            snapshots[step] = (phi_free.detach().clone(), psi.detach().clone())

    final_step = max(snapshots)
    if final_step != p6.STEPS:
        failed = True
        if not failure_reason:
            failure_reason = f"incomplete_trajectory_{final_step}"

    # Native evaluation occurs only after the optimization loop is over.
    traces: list[dict[str, object]] = []
    for step in sorted(snapshots):
        pf, ps = snapshots[step]
        row = _evaluate_snapshot(target, pf, ps, mode, generic_scale, step)
        row["seed"] = seed
        traces.append(row)

    final = dict(traces[-1])
    final.pop("step", None)
    final.update(
        {
            "seed": seed,
            "failed": failed,
            "failure_reason": failure_reason,
            "final_step": final_step,
        }
    )
    for key, value in last_components.items():
        final[f"final_energy_{key}"] = value
    return final, traces


def grouped_summary(results: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target_name in (*p6.TARGET_NAMES, "pooled"):
        for mode in p6.MODES:
            subset = [
                row
                for row in results
                if row["mode"] == mode
                and (target_name == "pooled" or row["target"] == target_name)
            ]
            precision = [float(row["topk_native_contact_precision"]) for row in subset]
            rg_ratio = [float(row["rg_ratio"]) for row in subset]
            rmsd = [float(row["ca_rmsd_A"]) for row in subset]
            rows.append(
                {
                    "target": target_name,
                    "mode": mode,
                    "n": len(subset),
                    "primary_precision_mean": statistics.mean(precision),
                    "primary_precision_median": statistics.median(precision),
                    "final_ca_rmsd_mean_A": statistics.mean(rmsd),
                    "final_rg_ratio_mean": statistics.mean(rg_ratio),
                    "final_rg_ratio_median": statistics.median(rg_ratio),
                    "max_bond_length_drift_A": max(float(row["max_bond_length_drift_A"]) for row in subset),
                    "max_bond_angle_drift_rad": max(float(row["max_bond_angle_drift_rad"]) for row in subset),
                    "failed_runs": sum(bool(row["failed"]) for row in subset),
                }
            )
    return rows


def paired_differences(
    results: list[dict[str, object]],
    control: str,
) -> tuple[list[float], dict[str, list[float]]]:
    index = {
        (str(row["target"]), int(row["seed"]), str(row["mode"])): row
        for row in results
    }
    pooled: list[float] = []
    by_target = {name: [] for name in p6.TARGET_NAMES}
    for target_name in p6.TARGET_NAMES:
        for seed in p6.SEEDS:
            candidate = float(
                index[(target_name, seed, "physical_real_sequence")][
                    "topk_native_contact_precision"
                ]
            )
            baseline = float(
                index[(target_name, seed, control)]["topk_native_contact_precision"]
            )
            delta = candidate - baseline
            pooled.append(delta)
            by_target[target_name].append(delta)
    return pooled, by_target


def native_firewall_selfcheck() -> bool:
    target = p6.load_target("1VII")
    pf0, ps0 = p6.initial_torsions(len(target.sequence), 0)
    scale = p6.generic_collapse_scale(target.sequence, pf0, ps0)

    def value_and_grad(t: p6.Target) -> tuple[float, torch.Tensor, torch.Tensor]:
        pf = pf0.clone().requires_grad_(True)
        ps = ps0.clone().requires_grad_(True)
        energy, _, _ = p6.objective(
            t, pf, ps, "physical_real_sequence", generic_scale=scale
        )
        gp, gs = torch.autograd.grad(energy, (pf, ps))
        return float(energy.detach()), gp.detach(), gs.detach()

    e0, gp0, gs0 = value_and_grad(target)
    changed = replace(target, native_ca=target.native_ca * 7.0 + 123.456)
    e1, gp1, gs1 = value_and_grad(changed)
    return (
        abs(e0 - e1) <= 1e-12
        and bool(torch.allclose(gp0, gp1, rtol=0.0, atol=1e-12))
        and bool(torch.allclose(gs0, gs1, rtol=0.0, atol=1e-12))
    )


def adjudicate(
    results: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    summary = grouped_summary(results)
    pooled_means = {
        str(row["mode"]): float(row["primary_precision_mean"])
        for row in summary
        if row["target"] == "pooled"
    }

    comparisons: list[dict[str, object]] = []
    raw_p_values: list[float] = []
    for control in ("generic_collapse", "physical_shuffled_sequence"):
        diffs, by_target = paired_differences(results, control)
        p_raw = p6.exact_sign_flip_p(diffs)
        raw_p_values.append(p_raw)
        row: dict[str, object] = {
            "comparison": f"physical_real_sequence_vs_{control}",
            "n_pairs": len(diffs),
            "candidate_minus_control_mean_precision": statistics.mean(diffs),
            "candidate_minus_control_median_precision": statistics.median(diffs),
            "candidate_wins": sum(delta > 0 for delta in diffs),
            "ties": sum(delta == 0 for delta in diffs),
            "raw_exact_sign_flip_p": p_raw,
        }
        for target_name in p6.TARGET_NAMES:
            row[f"{target_name}_mean_delta_precision"] = statistics.mean(by_target[target_name])
        comparisons.append(row)

    adjusted = p6.holm_two(raw_p_values[0], raw_p_values[1])
    for row, p_adjusted in zip(comparisons, adjusted):
        row["holm_adjusted_p"] = p_adjusted

    cmp_index = {str(row["comparison"]): row for row in comparisons}
    real_mean = pooled_means["physical_real_sequence"]

    rg_medians: dict[str, float] = {}
    for target_name in p6.TARGET_NAMES:
        vals = [
            float(row["rg_ratio"])
            for row in results
            if row["target"] == target_name and row["mode"] == "physical_real_sequence"
        ]
        rg_medians[target_name] = statistics.median(vals)

    geometry_good = all(
        float(row["max_bond_length_drift_A"]) < 1e-8
        and float(row["max_bond_angle_drift_rad"]) < 1e-8
        for row in results
    )
    numerical_good = all(
        not bool(row["failed"])
        and math.isfinite(float(row["topk_native_contact_precision"]))
        and math.isfinite(float(row["ca_rmsd_A"]))
        and math.isfinite(float(row["rg_ratio"]))
        for row in results
    )
    firewall_good = native_firewall_selfcheck()

    real_vs_generic = cmp_index[
        "physical_real_sequence_vs_generic_collapse"
    ]
    real_vs_shuffle = cmp_index[
        "physical_real_sequence_vs_physical_shuffled_sequence"
    ]

    conditions: dict[str, bool] = {
        "real_sequence_highest_pooled_mean_primary_precision": all(
            real_mean > pooled_means[mode]
            for mode in p6.MODES
            if mode != "physical_real_sequence"
        ),
        "real_sequence_beats_generic_on_every_target": all(
            float(real_vs_generic[f"{name}_mean_delta_precision"]) > 0.0
            for name in p6.TARGET_NAMES
        ),
        "real_sequence_beats_shuffle_on_every_target": all(
            float(real_vs_shuffle[f"{name}_mean_delta_precision"]) > 0.0
            for name in p6.TARGET_NAMES
        ),
        "real_vs_generic_holm_p_lt_0_05":
            float(real_vs_generic["holm_adjusted_p"]) < 0.05,
        "real_vs_shuffle_holm_p_lt_0_05":
            float(real_vs_shuffle["holm_adjusted_p"]) < 0.05,
        "real_sequence_rg_ratio_gate_every_target": all(
            p6.RG_RATIO_GATE[0] <= rg_medians[name] <= p6.RG_RATIO_GATE[1]
            for name in p6.TARGET_NAMES
        ),
        "all_runs_preserve_canonical_covalent_geometry": geometry_good,
        "all_runs_numerically_healthy": numerical_good,
        "native_information_firewall_passed": firewall_good,
    }

    decision = (
        "GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION"
        if all(conditions.values())
        else "NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION"
    )
    acceptance = {
        "decision": decision,
        "conditions": conditions,
        "pooled_primary_precision_mean": pooled_means,
        "real_sequence_target_rg_ratio_median": rg_medians,
        "primary_comparisons": comparisons,
        "claim_boundary": (
            "A GO establishes only transferable sequence-specific native-topology "
            "enrichment beyond the matched generic-collapse and side-chain-shuffle controls "
            "under the frozen P6 minimal native-blind model. It is not a claim of general "
            "protein folding, novelty over established force fields, or resurrection of "
            "v9, Patch-630, or TPO entropy."
        ),
    }
    return comparisons, acceptance


def main() -> None:
    OUT.mkdir(exist_ok=True)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    results: list[dict[str, object]] = []
    traces: list[dict[str, object]] = []

    for target_name in p6.TARGET_NAMES:
        for seed in p6.SEEDS:
            for mode in p6.MODES:
                row, trace = run_one(target_name, seed, mode)
                results.append(row)
                traces.extend(trace)

    summary = grouped_summary(results)
    comparisons, acceptance = adjudicate(results)

    manifest = {
        "schema": "protein-p6-measurement-v1",
        "git_head": os.environ.get("GITHUB_SHA"),
        "targets": list(p6.TARGET_NAMES),
        "seeds": list(p6.SEEDS),
        "modes": list(p6.MODES),
        "steps": p6.STEPS,
        "learning_rate": p6.LEARNING_RATE,
        "optimizer": "Adam",
        "dtype": "float64",
        "device": "cpu",
        "torch_deterministic_algorithms": True,
        "common_random_initial_torsions": True,
        "native_information_used_in_objective": False,
        "native_evaluation_timing": "post-trajectory only",
        "representation": "target-independent canonical peptide geometry; phi/psi only",
        "primary_endpoint": "final fixed-budget top-K long-range native-contact precision",
        "contact_min_sequence_separation": p6.CONTACT_MIN_SEQ_SEPARATION,
        "native_contact_cutoff_A": p6.NATIVE_CONTACT_CUTOFF_A,
        "top_k_rule": "max(1,floor(N/2)) capped by eligible pairs",
        "anti_collapse_rg_ratio_gate": list(p6.RG_RATIO_GATE),
        "checkpoints": list(CHECKPOINTS),
    }

    write_csv(OUT / "p6_results.csv", results)
    write_csv(OUT / "p6_traces.csv", traces)
    write_csv(OUT / "p6_summary.csv", summary)
    write_csv(OUT / "p6_primary_comparisons.csv", comparisons)
    (OUT / "p6_acceptance.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "p6_run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(acceptance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
