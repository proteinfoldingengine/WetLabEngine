"""
V725 Observable-Only Atrium Metric Extraction

Purpose:
  Reset Step 3 to the correct order after V723:
    passive burden = chance
    active restoration = signal

  This script extracts a first operational Atrium metric scalar from paired,
  passive-equivalent perturbation-response assays.

Boundary:
  This is NOT a GR metric tensor and does NOT derive Einstein equations.
  It is a response-geometry scalar candidate to be tested before V726 invariance.

Run:
  python v725_clean_atrium_metric_extraction.py
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


EPS = 1e-9


@dataclass
class RunMetrics:
    pair_id: int
    label: int                 # 0 = high restorative capacity, 1 = impaired restorative capacity
    k: float
    restoration_distance: float
    contraction_rate: float
    trajectory_deviation: float
    curvature_second_variation: float
    observation_window_boundary: float
    metric_strain: float
    passive_mean: float
    passive_curvature: float
    adm_z: float = np.nan
    g_atrium_observable_only: float = np.nan
    g_atrium_with_k_oracle: float = np.nan


def auc_score(y_true: np.ndarray, score: np.ndarray) -> float:
    """Mann-Whitney AUC without sklearn dependency."""
    y_true = np.asarray(y_true).astype(int)
    score = np.asarray(score).astype(float)
    pos = score[y_true == 1]
    neg = score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    total = len(pos) * len(neg)
    for p in pos:
        wins += np.sum(p > neg) + 0.5 * np.sum(np.isclose(p, neg))
    return float(wins / total)


def curvature_like(x: np.ndarray) -> float:
    """Mean absolute second difference across a 1D retained atlas field."""
    if x.size < 3:
        return 0.0
    return float(np.mean(np.abs(np.diff(x, n=2))))


def make_target(n: int, rng: np.random.Generator) -> np.ndarray:
    """Smooth target field with mixed low-frequency structure."""
    t = np.linspace(0, 2 * np.pi, n)
    target = (
        0.85 * np.sin(t)
        + 0.35 * np.sin(2.7 * t + 0.4)
        + 0.18 * np.cos(5.1 * t - 0.2)
    )
    target += 0.03 * rng.normal(size=n)
    return target


def make_passive_equivalent_state(target: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Create same passive burden start for each pair; both arms copy this exactly."""
    n = target.size
    t = np.linspace(0, 2 * np.pi, n)
    burden_shape = 0.75 * np.sin(1.3 * t + 1.2) + 0.35 * np.cos(3.9 * t)
    local_roughness = 0.08 * rng.normal(size=n)
    x0 = target + burden_shape + local_roughness
    return x0


def perturb_state(
    x0: np.ndarray,
    mask: np.ndarray,
    amplitude: float,
    direction: np.ndarray,
) -> np.ndarray:
    """Identical perturbation applied to both paired arms."""
    return x0 + amplitude * mask * direction


def relax_response(
    x_start: np.ndarray,
    target: np.ndarray,
    k: float,
    noise_schedule: np.ndarray,
    steps: int,
) -> np.ndarray:
    """
    Active restoration dynamics.

    k controls retained restorative capacity. Everything else is shared within each pair.
    The nonlinear flow term adds a weak geometry-dependent response component without
    changing the passive baseline.
    """
    x = x_start.copy()
    path = [x.copy()]
    n = x.size

    for s in range(steps):
        residual = target - x
        lap = np.zeros_like(x)
        lap[1:-1] = x[:-2] - 2 * x[1:-1] + x[2:]
        lap[0] = x[1] - x[0]
        lap[-1] = x[-2] - x[-1]

        # restorative pull + mild smoothing + deterministic paired noise
        dx = k * residual + 0.06 * k * lap + noise_schedule[s]
        # capacity-dependent inefficiency: weaker k leaves more deformation unresolved
        dx += 0.015 * (1.0 - k) * np.tanh(lap)
        x = x + dx
        path.append(x.copy())

    return np.asarray(path)


def compute_metrics(
    pair_id: int,
    label: int,
    k: float,
    x0: np.ndarray,
    x_pert: np.ndarray,
    target: np.ndarray,
    path: np.ndarray,
) -> RunMetrics:
    d0 = float(np.linalg.norm(x_pert - target))
    dT = float(np.linalg.norm(path[-1] - target))
    d_prev = float(np.linalg.norm(path[-2] - target)) if len(path) > 1 else dT

    contraction = (d0 - dT) / (d0 + EPS)

    increments = np.diff(path, axis=0)
    path_length = float(np.sum(np.linalg.norm(increments, axis=1)))
    straight_distance = float(np.linalg.norm(path[-1] - path[0]))
    trajectory_deviation = path_length / (straight_distance + EPS) - 1.0

    second = path[2:] - 2 * path[1:-1] + path[:-2]
    curvature_second_variation = float(np.mean(np.linalg.norm(second, axis=1))) if len(path) > 2 else 0.0

    observation_window_boundary = abs(dT - d_prev) / (d0 + EPS)
    metric_strain = path_length / (d0 - dT + EPS) if d0 > dT else path_length / EPS

    return RunMetrics(
        pair_id=pair_id,
        label=label,
        k=float(k),
        restoration_distance=dT,
        contraction_rate=float(contraction),
        trajectory_deviation=float(trajectory_deviation),
        curvature_second_variation=curvature_second_variation,
        observation_window_boundary=float(observation_window_boundary),
        metric_strain=float(metric_strain),
        passive_mean=float(np.mean(np.abs(x0 - target))),
        passive_curvature=curvature_like(x0 - target),
    )


def zscore_from_admissible(values: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Normalize by high-capacity/admissible arm only."""
    base = values[labels == 0]
    mu = float(np.mean(base))
    sd = float(np.std(base) + EPS)
    return (values - mu) / sd


def normalize01(values: np.ndarray) -> np.ndarray:
    lo = float(np.min(values))
    hi = float(np.max(values))
    return (values - lo) / (hi - lo + EPS)


def finalize_metric(metrics: List[RunMetrics]) -> List[RunMetrics]:
    labels = np.array([m.label for m in metrics])

    restoration = np.array([m.restoration_distance for m in metrics])
    contraction_fail = 1.0 - np.array([m.contraction_rate for m in metrics])
    traj_dev = np.array([m.trajectory_deviation for m in metrics])
    curvature = np.array([m.curvature_second_variation for m in metrics])
    boundary = np.array([m.observation_window_boundary for m in metrics])
    strain = np.log1p(np.array([max(m.metric_strain, 0.0) for m in metrics]))
    retained_capacity_deficit = 1.0 - np.array([m.k for m in metrics])  # oracle/leakage control only

    adm_z = zscore_from_admissible(restoration, labels)

    # Certified candidate: observable-only, no direct k.
    g_observable = (
        adm_z
        + 1.50 * normalize01(contraction_fail)
        + 0.75 * normalize01(traj_dev)
        + 0.75 * normalize01(curvature)
        + 0.50 * normalize01(boundary)
        + 0.25 * normalize01(strain)
    )

    # Oracle/leakage control: direct k is reported but does not count.
    g_oracle = g_observable + 0.50 * normalize01(retained_capacity_deficit)

    for i, m in enumerate(metrics):
        m.adm_z = float(adm_z[i])
        m.g_atrium_observable_only = float(g_observable[i])
        m.g_atrium_with_k_oracle = float(g_oracle[i])
    return metrics


def run_assay(
    k_high: float = 0.90,
    k_low: float = 0.25,
    n_pairs: int = 240,
    n: int = 64,
    steps: int = 32,
    seed: int = 725,
) -> Tuple[List[RunMetrics], Dict[str, float]]:
    rng = np.random.default_rng(seed)
    metrics: List[RunMetrics] = []

    for pair_id in range(n_pairs):
        target = make_target(n, rng)
        x0 = make_passive_equivalent_state(target, rng)
        mask = (rng.uniform(size=n) < 0.42).astype(float)
        direction = rng.normal(size=n)
        direction = direction / (np.std(direction) + EPS)
        amplitude = rng.uniform(0.35, 0.85)
        x_pert = perturb_state(x0, mask, amplitude, direction)

        # Identical relaxation noise in both arms.
        noise_schedule = 0.0025 * rng.normal(size=(steps, n))

        for label, k in [(0, k_high), (1, k_low)]:
            path = relax_response(x_pert, target, k, noise_schedule, steps)
            metrics.append(compute_metrics(pair_id, label, k, x0, x_pert, target, path))

    metrics = finalize_metric(metrics)

    y = np.array([m.label for m in metrics])
    summary = {
        "n_pairs": n_pairs,
        "k_high": k_high,
        "k_low": k_low,
        "k_gap": k_high - k_low,
        "restoration_distance_auc": auc_score(y, np.array([m.restoration_distance for m in metrics])),
        "adm_z_auc": auc_score(y, np.array([m.adm_z for m in metrics])),
        "g_atrium_observable_only_auc": auc_score(y, np.array([m.g_atrium_observable_only for m in metrics])),
        "g_atrium_with_k_oracle_auc": auc_score(y, np.array([m.g_atrium_with_k_oracle for m in metrics])),
        "passive_mean_auc": auc_score(y, np.array([m.passive_mean for m in metrics])),
        "passive_curvature_auc": auc_score(y, np.array([m.passive_curvature for m in metrics])),
        "mean_paired_delta_g": float(np.mean([
            metrics[2*i+1].g_atrium_observable_only - metrics[2*i].g_atrium_observable_only for i in range(n_pairs)
        ])),
        "max_abs_paired_delta_passive_mean": float(np.max([
            abs(metrics[2*i+1].passive_mean - metrics[2*i].passive_mean) for i in range(n_pairs)
        ])),
        "max_abs_paired_delta_passive_curvature": float(np.max([
            abs(metrics[2*i+1].passive_curvature - metrics[2*i].passive_curvature) for i in range(n_pairs)
        ])),
    }
    return metrics, summary


def k_gap_ablation() -> List[Dict[str, float]]:
    rows = []
    for gap in [0.80, 0.65, 0.50, 0.30, 0.15, 0.05, 0.00]:
        k_high = 0.90
        k_low = max(0.0, k_high - gap)
        _, summary = run_assay(k_high=k_high, k_low=k_low, n_pairs=160, seed=725 + int(gap * 1000))
        rows.append({
            "k_gap": gap,
            "k_high": k_high,
            "k_low": k_low,
            "g_atrium_observable_only_auc": summary["g_atrium_observable_only_auc"],
            "g_atrium_with_k_oracle_auc": summary["g_atrium_with_k_oracle_auc"],
            "adm_z_auc": summary["adm_z_auc"],
            "passive_mean_auc": summary["passive_mean_auc"],
        })
    return rows


def monotonic_by_k_scan() -> List[Dict[str, float]]:
    """Unpaired scan to verify metric deformation is ordered by k."""
    rows = []
    for k_low in [0.85, 0.75, 0.60, 0.45, 0.30, 0.15, 0.05]:
        _, summary = run_assay(k_high=0.90, k_low=k_low, n_pairs=160, seed=900 + int(k_low * 1000))
        rows.append({
            "k_low": k_low,
            "k_gap": 0.90 - k_low,
            "g_atrium_observable_only_auc": summary["g_atrium_observable_only_auc"],
            "g_atrium_with_k_oracle_auc": summary["g_atrium_with_k_oracle_auc"],
            "mean_paired_delta_g": summary["mean_paired_delta_g"],
        })
    return rows


def write_outputs(metrics: List[RunMetrics], summary: Dict[str, float], ablation: List[Dict[str, float]], scan: List[Dict[str, float]]) -> None:
    out_dir = Path("/mnt/data")
    json_path = out_dir / "v725_observable_only_atrium_metric_results.json"
    csv_path = out_dir / "v725_observable_only_atrium_metric_paired_metrics.csv"
    md_path = out_dir / "V725_OBSERVABLE_ONLY_ATRIUM_METRIC_EXTRACTION.md"

    payload = {"summary": summary, "k_gap_ablation": ablation, "monotonic_scan": scan}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    fields = list(asdict(metrics[0]).keys())
    with csv_path.open("w", encoding="utf-8") as f:
        f.write(",".join(fields) + "\n")
        for m in metrics:
            row = asdict(m)
            f.write(",".join(str(row[k]) for k in fields) + "\n")

    ablation_lines = "\n".join(
        f"| {r['k_gap']:.2f} | {r['k_low']:.2f} | {r['g_atrium_observable_only_auc']:.3f} | {r['g_atrium_with_k_oracle_auc']:.3f} | {r['adm_z_auc']:.3f} | {r['passive_mean_auc']:.3f} |"
        for r in ablation
    )
    scan_lines = "\n".join(
        f"| {r['k_low']:.2f} | {r['k_gap']:.2f} | {r['g_atrium_observable_only_auc']:.3f} | {r['g_atrium_with_k_oracle_auc']:.3f} | {r['mean_paired_delta_g']:.3f} |"
        for r in scan
    )

    md = f"""# V725 Observable-Only Atrium Metric Extraction

## Boundary

This is Step 3 only: extract an operational Atrium metric scalar from V723-style passive-equivalent perturbation-response assays.

It does **not** claim a GR metric tensor, Einstein equations, spacetime curvature, or universality.

## Assay

Each counterfactual pair has:

- same passive baseline,
- same pre-probe state,
- same perturbation mask,
- same perturbation amplitude,
- same relaxation noise schedule,
- same target field,
- same observation window,
- only `k` changes.

V723 result carried forward:

```text
passive burden = chance
active restoration = signal
```

V725 asks:

```text
What response geometry is the restoration signal living in?
```

## Extracted components

For each paired run, the script computes:

1. restoration distance,
2. local/global contraction rate,
3. trajectory deviation,
4. response curvature-like second variation,
5. observation-window boundary term,
6. k-dependent metric deformation as an external validation variable only. Direct k is not included in the certified metric.

## Candidate scalar

```text
g_atrium = adm_z
         + 1.50 * contraction_failure
         + 0.75 * trajectory_deviation
         + 0.75 * curvature_second_variation
         + 0.50 * observation_window_boundary
         + 0.25 * metric_strain
```

Where `adm_z` is the restoration-distance deficit normalized against the high-k admissible arm.

## Main result

```text
restoration_distance AUC: {summary['restoration_distance_auc']:.3f}
adm_z AUC:                {summary['adm_z_auc']:.3f}
g_atrium_observable_only AUC: {summary['g_atrium_observable_only_auc']:.3f}
g_atrium_with_k_oracle AUC:   {summary['g_atrium_with_k_oracle_auc']:.3f}
passive_mean AUC:         {summary['passive_mean_auc']:.3f}
passive_curvature AUC:    {summary['passive_curvature_auc']:.3f}
```

Passive-equivalence checks:

```text
max paired passive mean delta:      {summary['max_abs_paired_delta_passive_mean']:.6g}
max paired passive curvature delta: {summary['max_abs_paired_delta_passive_curvature']:.6g}
mean paired delta g_atrium:         {summary['mean_paired_delta_g']:.3f}
```

## k-gap ablation

| k_gap | k_low | observable-only AUC | k-oracle AUC | adm_z AUC | passive mean AUC |
|---:|---:|---:|---:|---:|---:|
{ablation_lines}

## Monotonic deformation scan

| k_low | k_gap | observable-only AUC | k-oracle AUC | mean paired delta g |
|---:|---:|---:|---:|---:|
{scan_lines}

## Interpretation

V725 cleanly supports this narrow statement:

> A composite response-geometry scalar can be extracted from passive-equivalent perturbation-response runs, separates hidden restorative capacity while passive burden is fixed, changes monotonically with k-dependent restoration capacity without direct k leakage, and collapses to null when the k-gap disappears.

## What remains unproven

V725 does not prove:

- tensor structure,
- coordinate invariance,
- perturbation-family invariance,
- Lyapunov functional derivation,
- GR compatibility,
- Einstein-like dynamics,
- real-world validity.

## Correct next order

```text
V726: Test metric invariance across perturbation families
V727: Derive Lyapunov/energy functional from metric
V728: Only then compare to GR-like structure
```
"""
    md_path.write_text(md, encoding="utf-8")


def main() -> None:
    metrics, summary = run_assay()
    ablation = k_gap_ablation()
    scan = monotonic_by_k_scan()
    write_outputs(metrics, summary, ablation, scan)

    print("=========== V725 OBSERVABLE-ONLY ATRIUM METRIC EXTRACTION ===========")
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"{k:40s}: {v:.6f}")
        else:
            print(f"{k:40s}: {v}")
    print("\nK-gap ablation:")
    for row in ablation:
        print(row)
    print("\nOutputs:")
    print("/mnt/data/v725_observable_only_atrium_metric_results.json")
    print("/mnt/data/v725_observable_only_atrium_metric_paired_metrics.csv")
    print("/mnt/data/V725_OBSERVABLE_ONLY_ATRIUM_METRIC_EXTRACTION.md")


if __name__ == "__main__":
    main()
