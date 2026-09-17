from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import mean, median

import torch

import p1_core as p1


TARGETS = {
    "1UAO": {
        "path": "inputs/1UAO.ca_chainA_model1.pdb",
        "sha256": "b7cb0808f7dc0f4ed40bee9ca332696f50c2cc25d34ba53cabd7ba1ed03f468f",
        "ca_count": 10,
    },
    "1L2Y": {
        "path": "inputs/1L2Y.ca_chainA_model1.pdb",
        "sha256": "84179b355a043df03e98f432dd2b2fbba4035b4f7df2e4928feabec8baed4378",
        "ca_count": 20,
    },
}

SEEDS = tuple(range(6))
PRE_STEPS = 180
POST_STEPS = 240
LR = 0.05
NOISE_SCALE = 0.013
TRACE_STRIDE = 60
PRIMARY_COMPARATORS = ("static_combo", "fixed_gate")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_ca_coords(path: Path) -> torch.Tensor:
    """Recovered loader contract: chain A CA atoms, first MODEL if present."""
    lines = path.read_text().splitlines()
    coords: list[list[float]] = []
    saw_model = False
    in_model = False

    for line in lines:
        if line.startswith("MODEL"):
            saw_model = True
            parts = line.split()
            in_model = len(parts) > 1 and parts[1] == "1"
        elif line.startswith("ENDMDL"):
            if in_model:
                break
        elif line.startswith("ATOM") and (in_model or not saw_model):
            atom = line[12:16].strip()
            chain = line[21].strip()
            if atom == "CA" and chain == "A":
                coords.append(
                    [
                        float(line[30:38]),
                        float(line[38:46]),
                        float(line[46:54]),
                    ]
                )

    if not coords:
        raise ValueError(f"No eligible CA coordinates in {path}")

    x = torch.tensor(coords, dtype=torch.float32)
    return x - x.mean(0)


def verify_bound_inputs(base: Path) -> dict[str, dict[str, object]]:
    verified: dict[str, dict[str, object]] = {}
    for target, spec in TARGETS.items():
        path = base / str(spec["path"])
        digest = sha256_file(path)
        if digest != spec["sha256"]:
            raise RuntimeError(
                f"Input hash mismatch for {target}: {digest} != {spec['sha256']}"
            )
        x = load_ca_coords(path)
        if int(x.shape[0]) != int(spec["ca_count"]):
            raise RuntimeError(
                f"CA count mismatch for {target}: {x.shape[0]} != {spec['ca_count']}"
            )
        verified[target] = {
            "path": str(spec["path"]),
            "sha256": digest,
            "ca_count": int(x.shape[0]),
        }
    return verified


def kabsch_rmsd(p: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
    pc = p - p.mean(0)
    qc = q - q.mean(0)
    c = pc.T @ qc
    v, _, w = torch.linalg.svd(c)
    d = torch.sign(torch.linalg.det(v @ w))
    eye = torch.eye(3, dtype=p.dtype)
    eye[-1, -1] = d
    u = v @ eye @ w
    return torch.sqrt(torch.mean(torch.sum(((pc @ u) - qc) ** 2, dim=1)))


def angle_rms(x: torch.Tensor, target: torch.Tensor) -> float:
    a = p1.angles_from_coords(x)
    b = p1.angles_from_coords(target)
    return float(torch.sqrt(((a - b) ** 2).mean()))


def dihedral_rms(x: torch.Tensor, target: torch.Tensor) -> float:
    a = p1.dihedrals_from_coords(x)
    b = p1.dihedrals_from_coords(target)
    dd = torch.atan2(torch.sin(a - b), torch.cos(a - b))
    return float(torch.sqrt((dd ** 2).mean()))


def contact_recovery(x: torch.Tensor, target: torch.Tensor) -> float:
    td = p1.pairwise_dists(target)
    mask = (td < 8.0) & (td > 0)
    n = int(target.shape[0])
    for i in range(n):
        for j in range(n):
            if abs(i - j) < 3:
                mask[i, j] = False
    native = torch.nonzero(torch.triu(mask, diagonal=3))
    if len(native) == 0:
        return 0.0
    d = p1.pairwise_dists(x)
    return float((d[native[:, 0], native[:, 1]] < 8.0).float().mean())


def make_trial_inputs(
    n: int, target_index: int, seed: int
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Common-random-number packet. The returned tensors are reused unchanged
    across all seven modes for one target/seed pair.
    """
    generator = torch.Generator(device="cpu")
    generator.manual_seed(1_000_003 + 100_003 * target_index + seed)
    perturb = torch.randn((n, 3), generator=generator, dtype=torch.float32)
    pre_noise = torch.randn(
        (PRE_STEPS, n, 3), generator=generator, dtype=torch.float32
    )
    post_noise = torch.randn(
        (POST_STEPS, n, 3), generator=generator, dtype=torch.float32
    )
    init = p1.random_chain(n, seed=seed) + 3.0 * perturb
    return init, pre_noise, post_noise


def optimize_stage(
    x0: torch.Tensor,
    ctx: p1.FoldContext,
    target: torch.Tensor,
    mode: str,
    noise: torch.Tensor,
    phase: str,
    global_start: int,
) -> tuple[torch.Tensor, torch.Tensor, float, list[dict[str, object]]]:
    x = x0.clone().detach().requires_grad_(True)
    opt = torch.optim.Adam([x], lr=LR)
    steps = int(noise.shape[0])

    with torch.no_grad():
        initial_rmsd = float(kabsch_rmsd(x.detach(), target))
    best_rmsd = initial_rmsd
    best_x = x.detach().clone()
    trace: list[dict[str, object]] = [
        {
            "phase": phase,
            "phase_step": 0,
            "global_step": global_start,
            "mode": mode,
            "rmsd": initial_rmsd,
        }
    ]

    for t in range(steps):
        opt.zero_grad(set_to_none=True)
        energy, _ = p1.energy_for_mode(x, ctx, mode)
        energy.backward()
        opt.step()

        with torch.no_grad():
            scale = NOISE_SCALE * (1.0 - t / max(steps, 1))
            x += scale * noise[t]
            rmsd = float(kabsch_rmsd(x.detach(), target))

        if rmsd < best_rmsd:
            best_rmsd = rmsd
            best_x = x.detach().clone()

        if (t + 1) % TRACE_STRIDE == 0 or t == steps - 1:
            trace.append(
                {
                    "phase": phase,
                    "phase_step": t + 1,
                    "global_step": global_start + t + 1,
                    "mode": mode,
                    "rmsd": rmsd,
                    "energy": float(energy.detach()),
                }
            )

    return x.detach(), best_x, best_rmsd, trace


def run_one(
    target_name: str,
    target_index: int,
    target: torch.Tensor,
    seed: int,
    mode: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    ctx = p1.FoldContext(target, target_name)
    init, pre_noise, post_noise = make_trial_inputs(
        int(target.shape[0]), target_index, seed
    )

    pre_end, _, _, pre_trace = optimize_stage(
        init,
        ctx,
        target,
        mode,
        pre_noise,
        phase="precondition",
        global_start=0,
    )
    pre_end_rmsd = float(kabsch_rmsd(pre_end, target))

    post_end, post_best_x, post_best_rmsd, post_trace = optimize_stage(
        pre_end,
        ctx,
        target,
        "baseline",
        post_noise,
        phase="common_baseline_relax",
        global_start=PRE_STEPS,
    )

    row: dict[str, object] = {
        "target": target_name,
        "seed": seed,
        "mode": mode,
        "pre_end_rmsd": pre_end_rmsd,
        "post_best_rmsd": post_best_rmsd,
        "final_rmsd": float(kabsch_rmsd(post_end, target)),
        "angle_rms": angle_rms(post_best_x, target),
        "dihedral_rms": dihedral_rms(post_best_x, target),
        "contact_recovery": contact_recovery(post_best_x, target),
    }
    traces: list[dict[str, object]] = []
    for item in pre_trace + post_trace:
        item = dict(item)
        item.update({"target": target_name, "seed": seed, "protocol_mode": mode})
        traces.append(item)
    return row, traces


def exact_sign_flip_pvalue(differences: list[float]) -> float:
    if not differences:
        raise ValueError("No differences")
    observed = abs(mean(differences))
    extreme = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(differences)):
        stat = abs(mean([s * d for s, d in zip(signs, differences)]))
        total += 1
        if stat + 1e-12 >= observed:
            extreme += 1
    return extreme / total


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for rank, (name, pvalue) in enumerate(ordered):
        value = min(1.0, (m - rank) * pvalue)
        running = max(running, value)
        adjusted[name] = running
    return adjusted


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    targets = tuple(TARGETS)
    for target in targets + ("pooled",):
        for mode in p1.CONTROL_MODES:
            selected = [
                r
                for r in rows
                if r["mode"] == mode
                and (target == "pooled" or r["target"] == target)
            ]
            summary.append(
                {
                    "target": target,
                    "mode": mode,
                    "n": len(selected),
                    "post_best_rmsd_mean": mean(
                        [float(r["post_best_rmsd"]) for r in selected]
                    ),
                    "post_best_rmsd_median": median(
                        [float(r["post_best_rmsd"]) for r in selected]
                    ),
                    "final_rmsd_mean": mean(
                        [float(r["final_rmsd"]) for r in selected]
                    ),
                    "contact_recovery_mean": mean(
                        [float(r["contact_recovery"]) for r in selected]
                    ),
                }
            )
    return summary


def primary_comparisons(
    rows: list[dict[str, object]]
) -> tuple[list[dict[str, object]], dict[str, float]]:
    raw_p: dict[str, float] = {}
    comparisons: list[dict[str, object]] = []

    for control in PRIMARY_COMPARATORS:
        diffs: list[float] = []
        target_deltas: dict[str, float] = {}
        wins = 0
        for target in TARGETS:
            v9 = {
                int(r["seed"]): float(r["post_best_rmsd"])
                for r in rows
                if r["target"] == target and r["mode"] == "v9"
            }
            ctl = {
                int(r["seed"]): float(r["post_best_rmsd"])
                for r in rows
                if r["target"] == target and r["mode"] == control
            }
            target_pairs = [v9[s] - ctl[s] for s in SEEDS]
            diffs.extend(target_pairs)
            target_deltas[target] = mean(target_pairs)
            wins += sum(1 for d in target_pairs if d < 0)

        pvalue = exact_sign_flip_pvalue(diffs)
        raw_p[control] = pvalue
        comparisons.append(
            {
                "comparison": f"v9_vs_{control}",
                "n_pairs": len(diffs),
                "v9_minus_control_mean": mean(diffs),
                "v9_minus_control_median": median(diffs),
                "v9_wins": wins,
                "raw_exact_sign_flip_p": pvalue,
                "1UAO_mean_delta": target_deltas["1UAO"],
                "1L2Y_mean_delta": target_deltas["1L2Y"],
            }
        )

    adjusted = holm_adjust(raw_p)
    for row in comparisons:
        control = str(row["comparison"]).removeprefix("v9_vs_")
        row["holm_adjusted_p"] = adjusted[control]
    return comparisons, adjusted


def decide(
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    comparisons: list[dict[str, object]],
) -> tuple[str, dict[str, bool]]:
    pooled = {
        str(r["mode"]): float(r["post_best_rmsd_mean"])
        for r in summary
        if r["target"] == "pooled"
    }
    v9_best_pooled = all(
        pooled["v9"] < pooled[mode] for mode in p1.CONTROL_MODES if mode != "v9"
    )

    by_comparison = {
        str(r["comparison"]).removeprefix("v9_vs_"): r for r in comparisons
    }
    static = by_comparison["static_combo"]
    fixed = by_comparison["fixed_gate"]

    conditions = {
        "v9_lower_pooled_mean_than_every_control": v9_best_pooled,
        "v9_lower_than_static_on_1UAO": float(static["1UAO_mean_delta"]) < 0,
        "v9_lower_than_static_on_1L2Y": float(static["1L2Y_mean_delta"]) < 0,
        "v9_lower_than_fixed_on_1UAO": float(fixed["1UAO_mean_delta"]) < 0,
        "v9_lower_than_fixed_on_1L2Y": float(fixed["1L2Y_mean_delta"]) < 0,
        "v9_vs_static_holm_p_lt_0_05": float(static["holm_adjusted_p"]) < 0.05,
        "v9_vs_fixed_holm_p_lt_0_05": float(fixed["holm_adjusted_p"]) < 0.05,
    }
    decision = (
        "GO_HIERARCHICAL_V9"
        if all(conditions.values())
        else "NO_GO_HIERARCHICAL_ADVANTAGE"
    )
    return decision, conditions


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")

    # Trace rows intentionally have a sparse schema: the initial checkpoint
    # has no energy value while later checkpoints do. Preserve the union of
    # fields in first-seen order rather than assuming row 0 is exhaustive.
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    base = Path(__file__).resolve().parent
    outdir = base / "measurement_output"
    outdir.mkdir(exist_ok=True)

    verified_inputs = verify_bound_inputs(base)

    targets = {
        name: load_ca_coords(base / str(spec["path"]))
        for name, spec in TARGETS.items()
    }

    rows: list[dict[str, object]] = []
    traces: list[dict[str, object]] = []

    for target_index, (target_name, target) in enumerate(targets.items()):
        for seed in SEEDS:
            for mode in p1.CONTROL_MODES:
                row, trace = run_one(
                    target_name, target_index, target, seed, mode
                )
                rows.append(row)
                traces.extend(trace)

    summary = summarize(rows)
    comparisons, _ = primary_comparisons(rows)
    decision, conditions = decide(rows, summary, comparisons)

    write_csv(outdir / "p1_results.csv", rows)
    write_csv(outdir / "p1_summary.csv", summary)
    write_csv(outdir / "p1_primary_comparisons.csv", comparisons)
    write_csv(outdir / "p1_traces.csv", traces)

    run_manifest = {
        "schema": "protein-p1-measurement-v1",
        "targets": verified_inputs,
        "seeds": list(SEEDS),
        "modes": list(p1.CONTROL_MODES),
        "pre_steps": PRE_STEPS,
        "post_steps": POST_STEPS,
        "optimizer": "Adam",
        "learning_rate": LR,
        "noise_scale": NOISE_SCALE,
        "common_random_numbers": True,
        "optimizer_reset_at_handoff": True,
        "torch_deterministic_algorithms": True,
        "fixed_gate_sigma": p1.FIXED_GATE_SIGMA,
        "fixed_gate_closure": p1.FIXED_GATE_CLOSURE,
    }
    (outdir / "p1_run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2, sort_keys=True) + "\n"
    )

    acceptance = {
        "decision": decision,
        "conditions": conditions,
        "primary_comparisons": comparisons,
        "pooled_post_best_rmsd_mean": {
            str(r["mode"]): float(r["post_best_rmsd_mean"])
            for r in summary
            if r["target"] == "pooled"
        },
    }
    (outdir / "p1_acceptance.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True) + "\n"
    )

    print(json.dumps(acceptance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
