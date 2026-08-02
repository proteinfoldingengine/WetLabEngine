#!/usr/bin/env python3
"""
UQCF-GEM observable-response holonomy landscape, Phase 2.

This script verifies the exact full-rank qubit-loop structure:

    H = V_31 V_23 V_12 ∈ O(3),

and the orientation parity

    det(H) = ∏_edges sign(det Γ_ij),

where Γ_ij is the connected Pauli covariance matrix. Positive BKM whitening
factors cannot change determinant signs.

It also:
- reproduces the generalized-W reflection;
- surveys random pure and mixed three-qubit states;
- finds a convex mixed-state path where orientation parity changes;
- verifies that the parity change occurs through an edge-rank-loss surface.

The numerical survey supports finite-model classification. The O(3) and parity
identities are direct consequences of polar decomposition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

from w_holonomy_core import (
    PAULI,
    EDGES,
    generalized_w_density,
    loop_result,
    reduced_density,
    centered_pauli_basis,
    cross_covariance,
)


def random_pure_state(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=8) + 1j * rng.normal(size=8)
    vector /= np.linalg.norm(vector)
    return np.outer(vector, vector.conj())


def random_mixed_state(rng: np.random.Generator, rank: int = 8) -> np.ndarray:
    matrix = rng.normal(size=(8, rank)) + 1j * rng.normal(size=(8, rank))
    rho = matrix @ matrix.conj().T
    return rho / np.trace(rho)


def edge_covariance_determinants(rho: np.ndarray) -> np.ndarray:
    determinants = []
    for i, j in EDGES:
        rho_i = reduced_density(rho, (i,))
        rho_j = reduced_density(rho, (j,))
        rho_ij = reduced_density(rho, (i, j))
        covariance = cross_covariance(
            rho_ij,
            centered_pauli_basis(rho_i),
            centered_pauli_basis(rho_j),
        )
        determinants.append(float(np.linalg.det(covariance)))
    return np.asarray(determinants)


def orientation_angle(loop: np.ndarray) -> tuple[int, float]:
    determinant = float(np.linalg.det(loop))
    parity = 1 if determinant > 0 else -1
    trace = float(np.trace(loop))
    if parity > 0:
        cosine = (trace - 1.0) / 2.0
    else:
        cosine = (trace + 1.0) / 2.0
    angle = float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return parity, angle


def analyze_state(rho: np.ndarray, rank_tolerance: float = 1e-10) -> dict:
    result = loop_result(rho, rank_tolerance=rank_tolerance)
    edge_ranks = [
        int(np.sum(edge.singular_values > rank_tolerance))
        for edge in result.edge_results
    ]
    covariance_dets = edge_covariance_determinants(rho)
    full_rank = min(edge_ranks) == 3

    orthogonality_error = float(
        np.max(np.abs(result.loop.T @ result.loop - np.eye(3)))
    )
    parity = 0
    angle = None
    parity_formula = 0

    if full_rank:
        parity, angle = orientation_angle(result.loop)
        parity_formula = int(np.prod(np.sign(covariance_dets)))
        if parity != parity_formula:
            raise AssertionError(
                f"parity mismatch: loop={parity}, covariance={parity_formula}"
            )
        if orthogonality_error > 1e-9:
            raise AssertionError(
                f"full-rank loop is not orthogonal: {orthogonality_error}"
            )

    return {
        "full_rank": full_rank,
        "edge_ranks": edge_ranks,
        "edge_covariance_determinants": covariance_dets.tolist(),
        "loop_determinant": float(np.linalg.det(result.loop)),
        "loop_trace": float(np.trace(result.loop)),
        "loop_singular_values": result.singular_values.tolist(),
        "loop_eigenvalues": [
            [float(value.real), float(value.imag)]
            for value in np.linalg.eigvals(result.loop)
        ],
        "orthogonality_error": orthogonality_error,
        "parity": parity,
        "parity_formula": parity_formula,
        "angle_radians": angle,
    }


def find_opposite_parity_states(
    rng: np.random.Generator,
    max_attempts: int = 10000,
) -> tuple[np.ndarray, np.ndarray]:
    positive = None
    negative = None
    for _ in range(max_attempts):
        rho = random_mixed_state(rng)
        data = analyze_state(rho)
        if not data["full_rank"]:
            continue
        if data["parity"] > 0 and positive is None:
            positive = rho
        if data["parity"] < 0 and negative is None:
            negative = rho
        if positive is not None and negative is not None:
            return negative, positive
    raise RuntimeError("failed to find both parity sectors")


def transition_scan(
    rho_minus: np.ndarray,
    rho_plus: np.ndarray,
    points: int = 401,
) -> dict:
    def state(t: float) -> np.ndarray:
        return (1.0 - t) * rho_minus + t * rho_plus

    grid = np.linspace(0.0, 1.0, points)
    determinant_curves = np.array([
        edge_covariance_determinants(state(t))
        for t in grid
    ])

    roots = []
    for edge_index in range(3):
        values = determinant_curves[:, edge_index]
        for index in range(len(grid) - 1):
            if values[index] == 0:
                roots.append((edge_index, grid[index]))
            elif values[index] * values[index + 1] < 0:
                root = brentq(
                    lambda t: edge_covariance_determinants(state(t))[edge_index],
                    grid[index],
                    grid[index + 1],
                    xtol=1e-13,
                )
                roots.append((edge_index, root))

    if not roots:
        raise AssertionError("parity changed without a covariance determinant root")

    roots.sort(key=lambda item: item[1])
    edge_index, root = roots[0]
    delta = 2e-5
    left_t = max(0.0, root - delta)
    right_t = min(1.0, root + delta)

    left = analyze_state(state(left_t), rank_tolerance=1e-9)
    at = analyze_state(state(root), rank_tolerance=1e-8)
    right = analyze_state(state(right_t), rank_tolerance=1e-9)

    return {
        "grid": grid,
        "determinant_curves": determinant_curves,
        "transition_edge_index": edge_index,
        "transition_edge": EDGES[edge_index],
        "root": root,
        "left": left,
        "at": at,
        "right": right,
    }


def save_angle_histogram(
    pure_angles: list[float],
    mixed_positive: list[float],
    mixed_negative: list[float],
    output: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(pure_angles, bins=40, alpha=0.55, label="pure, parity −1")
    ax.hist(mixed_negative, bins=40, alpha=0.55, label="mixed, parity −1")
    ax.hist(mixed_positive, bins=40, alpha=0.55, label="mixed, parity +1")
    ax.set_xlabel("loop orientation angle θ (radians)")
    ax.set_ylabel("count")
    ax.set_title("Full-rank observable-response holonomy landscape")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_transition_plot(transition: dict, output: Path) -> None:
    grid = transition["grid"]
    curves = transition["determinant_curves"]
    root = transition["root"]

    fig, ax = plt.subplots(figsize=(9, 6))
    for edge_index, (i, j) in enumerate(EDGES):
        ax.plot(grid, curves[:, edge_index], label=f"det Γ{i+1}{j+1}")
    ax.axhline(0.0, linewidth=1)
    ax.axvline(root, linestyle="--", linewidth=2, label=f"rank-loss root t={root:.6f}")
    ax.set_xlabel("convex interpolation parameter t")
    ax.set_ylabel("edge covariance determinant")
    ax.set_title("Orientation parity can change only through edge rank loss")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def run(seed: int, samples: int, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    # Exact generalized-W control.
    amplitudes = np.array([
        np.sqrt(0.45) * np.exp(0.21j),
        np.sqrt(0.33) * np.exp(-0.74j),
        np.sqrt(0.22) * np.exp(1.13j),
    ])
    w_data = analyze_state(generalized_w_density(amplitudes))
    expected_w = np.array([-1.0, 1.0, 1.0])
    actual_w = np.sort_complex(
        np.array([complex(real, imag) for real, imag in w_data["loop_eigenvalues"]])
    )
    np.testing.assert_allclose(actual_w, expected_w, atol=1e-10)

    pure_records = []
    mixed_records = []
    for _ in range(samples):
        pure_records.append(analyze_state(random_pure_state(rng)))
        mixed_records.append(analyze_state(random_mixed_state(rng)))

    pure_full = [record for record in pure_records if record["full_rank"]]
    mixed_full = [record for record in mixed_records if record["full_rank"]]

    pure_parities = [record["parity"] for record in pure_full]
    mixed_positive = [
        record["angle_radians"] for record in mixed_full if record["parity"] > 0
    ]
    mixed_negative = [
        record["angle_radians"] for record in mixed_full if record["parity"] < 0
    ]
    pure_angles = [record["angle_radians"] for record in pure_full]

    rho_minus, rho_plus = find_opposite_parity_states(rng)
    transition = transition_scan(rho_minus, rho_plus)

    save_angle_histogram(
        pure_angles,
        mixed_positive,
        mixed_negative,
        output_dir / "01_holonomy_angle_landscape.png",
    )
    save_transition_plot(
        transition,
        output_dir / "02_parity_rank_loss_transition.png",
    )

    summary = {
        "seed": seed,
        "samples_per_ensemble": samples,
        "w_control": w_data,
        "pure": {
            "full_rank_count": len(pure_full),
            "parity_counts": {
                "-1": pure_parities.count(-1),
                "+1": pure_parities.count(1),
            },
            "angle_min": float(np.min(pure_angles)),
            "angle_median": float(np.median(pure_angles)),
            "angle_mean": float(np.mean(pure_angles)),
            "angle_max": float(np.max(pure_angles)),
            "maximum_orthogonality_error": float(
                max(record["orthogonality_error"] for record in pure_full)
            ),
        },
        "mixed": {
            "full_rank_count": len(mixed_full),
            "parity_counts": {
                "-1": len(mixed_negative),
                "+1": len(mixed_positive),
            },
            "negative_angle_min": float(np.min(mixed_negative)),
            "negative_angle_max": float(np.max(mixed_negative)),
            "positive_angle_min": float(np.min(mixed_positive)),
            "positive_angle_max": float(np.max(mixed_positive)),
            "maximum_orthogonality_error": float(
                max(record["orthogonality_error"] for record in mixed_full)
            ),
        },
        "transition": {
            "edge": [int(x) for x in transition["transition_edge"]],
            "root": float(transition["root"]),
            "left_parity": int(transition["left"]["parity"]),
            "at_edge_ranks": transition["at"]["edge_ranks"],
            "at_loop_singular_values": transition["at"]["loop_singular_values"],
            "right_parity": int(transition["right"]["parity"]),
        },
    }

    (output_dir / "phase2_results.json").write_text(
        json.dumps(summary, indent=2)
    )

    print("PHASE 2 HOLONOMY LANDSCAPE: PASS")
    print(f"Pure full-rank states: {len(pure_full)}/{samples}")
    print("Pure parity counts:", summary["pure"]["parity_counts"])
    print(
        "Pure angle range:",
        summary["pure"]["angle_min"],
        "to",
        summary["pure"]["angle_max"],
    )
    print(f"Mixed full-rank states: {len(mixed_full)}/{samples}")
    print("Mixed parity counts:", summary["mixed"]["parity_counts"])
    print(
        "Parity transition:",
        summary["transition"]["left_parity"],
        "-> rank",
        summary["transition"]["at_edge_ranks"],
        "->",
        summary["transition"]["right_parity"],
    )
    print("Transition root:", summary["transition"]["root"])
    print(
        "Maximum orthogonality errors:",
        summary["pure"]["maximum_orthogonality_error"],
        summary["mixed"]["maximum_orthogonality_error"],
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--output", type=Path, default=Path("phase2_output"))
    args = parser.parse_args()
    run(args.seed, args.samples, args.output)


if __name__ == "__main__":
    main()
