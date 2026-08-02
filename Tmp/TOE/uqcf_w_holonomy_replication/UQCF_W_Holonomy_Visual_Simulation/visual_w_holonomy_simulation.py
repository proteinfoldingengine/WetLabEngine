#!/usr/bin/env python3
"""
Human-readable visual simulation of the generalized-W observable-response
holonomy discovery.

This program does not hard-code the loop result. It starts from an explicit
8x8 global density matrix, forms all pair marginals, constructs the BKM
covariance-response maps, extracts their supported polar factors, and composes
the triangle loop.

Outputs:
  01_edge_transport_triangle.png
  02_loop_reflection_3d.png
  03_noise_threshold.png
  04_noise_phase_diagram.png
  05_transition.gif
  verification_summary.json

The visual simulation is an executable verification and explanatory model.
The accompanying analytic identities provide the theorem-level argument;
a finite numerical simulation alone is not a substitute for a formal proof.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from w_holonomy_core import (
    EDGES,
    generalized_w_density,
    loop_result,
    regularized_population_covariance_signs,
    noise_transition_threshold,
)

NODE_LABELS = ('1', '2', '3')
EDGE_LABELS = ('12', '23', '31')


def normalize_amplitudes(amplitudes: np.ndarray) -> np.ndarray:
    amplitudes = np.asarray(amplitudes, dtype=complex)
    return amplitudes / np.linalg.norm(amplitudes)


def classify_loop(result, tol: float = 1e-8) -> str:
    singular = np.sort(result.singular_values)
    if np.allclose(singular, [1.0, 1.0, 1.0], atol=tol):
        det = round(result.determinant)
        return 'LOSSLESS REFLECTION' if det == -1 else 'LOSSLESS IDENTITY'
    if np.allclose(singular, [0.0, 1.0, 1.0], atol=tol):
        return 'RANK-LOSS SURFACE'
    if np.allclose(singular, [0.0, 0.0, 0.0], atol=tol):
        return 'ZERO RESPONSE SUPPORT'
    return 'MIXED / PARTIAL SUPPORT'


def save_edge_transport_triangle(amplitudes: np.ndarray, epsilon: float, output: Path) -> None:
    amplitudes = normalize_amplitudes(amplitudes)
    probabilities = np.abs(amplitudes) ** 2
    phases = np.angle(amplitudes)
    rho = generalized_w_density(amplitudes, epsilon)
    result = loop_result(rho)
    sign_product, q_values = regularized_population_covariance_signs(probabilities, epsilon)

    positions = np.array([
        [0.0, 1.0],
        [-0.92, -0.55],
        [0.92, -0.55],
    ])

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    for edge_index, (i, j) in enumerate(EDGES):
        start = positions[i]
        end = positions[j]
        direction = end - start
        ax.annotate(
            '',
            xy=end,
            xytext=start,
            arrowprops=dict(arrowstyle='->', linewidth=2.5),
        )
        midpoint = (start + end) / 2
        phi = (phases[i] - phases[j] + np.pi) % (2 * np.pi) - np.pi
        sign_text = '+' if q_values[edge_index] > 0 else ('-' if q_values[edge_index] < 0 else '0')
        singular = result.edge_results[edge_index].singular_values
        label = (
            f"edge {EDGE_LABELS[edge_index]}\n"
            f"XY rotation Δφ={phi:+.2f} rad\n"
            f"Z sign={sign_text}, rank={np.sum(singular > 1e-9)}"
        )
        ax.text(midpoint[0], midpoint[1], label, ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.35', alpha=0.85))

    for idx, position in enumerate(positions):
        ax.scatter(position[0], position[1], s=1100)
        ax.text(position[0], position[1] + 0.02, NODE_LABELS[idx], ha='center', va='center',
                fontsize=18, fontweight='bold')
        ax.text(
            position[0], position[1] - 0.22,
            f"p={probabilities[idx]:.3f}\nφ={phases[idx]:+.2f}",
            ha='center', va='top', fontsize=11,
        )

    phase_sum = sum((phases[i] - phases[j]) for i, j in EDGES)
    ax.text(
        0.0, -1.22,
        "XY rotations telescope: "
        f"(φ₁−φ₂)+(φ₂−φ₃)+(φ₃−φ₁)={phase_sum:+.2e}\n"
        f"Population sign product={sign_product:+d}  →  {classify_loop(result)}",
        ha='center', va='center', fontsize=12,
        bbox=dict(boxstyle='round,pad=0.5', alpha=0.85),
    )
    ax.set_title('Canonical pair-derived edge transports', fontsize=16, pad=18)
    fig.savefig(output, dpi=180, bbox_inches='tight')
    plt.close(fig)


def draw_sphere_wireframe(ax) -> None:
    u = np.linspace(0, 2 * np.pi, 45)
    v = np.linspace(0, np.pi, 24)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, rstride=4, cstride=4, linewidth=0.35, alpha=0.25)


def save_loop_reflection_3d(amplitudes: np.ndarray, epsilon: float, output: Path) -> None:
    amplitudes = normalize_amplitudes(amplitudes)
    result = loop_result(generalized_w_density(amplitudes, epsilon))
    H = np.real_if_close(result.loop).astype(float)

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection='3d')
    draw_sphere_wireframe(ax)

    basis = np.eye(3)
    labels = ('X', 'Y', 'Z')
    for idx, vector in enumerate(basis):
        image = H @ vector
        ax.quiver(0, 0, 0, *vector, linewidth=2.4, arrow_length_ratio=0.12)
        ax.quiver(0, 0, 0, *image, linewidth=4.0, arrow_length_ratio=0.12, linestyle='dashed')
        if idx < 2:
            offset = np.array([0.0, 0.0, 0.10])
            ax.text(*(vector * 1.15 + offset), f'{labels[idx]} unchanged', fontsize=10)
        else:
            ax.text(*(vector * 1.15), 'Z before loop', fontsize=10)
            ax.text(*(image * 1.25), 'Z after loop', fontsize=10)

    ax.text2D(0.03, 0.04, 'Solid = before loop   Dashed = after loop', transform=ax.transAxes, fontsize=10)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_zlim(-1.35, 1.35)
    ax.set_xlabel('Whitened X response')
    ax.set_ylabel('Whitened Y response')
    ax.set_zlabel('Whitened Z response')
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=24, azim=38)

    eigenvalues = np.round(np.real_if_close(np.sort_complex(result.eigenvalues)).real, 6)
    singular_values = np.round(result.singular_values, 6)
    ax.set_title(
        'Loop result: X and Y return unchanged; Z returns reversed\n'
        f'eigenvalues={tuple(eigenvalues)}   singular values={tuple(singular_values)}\n'
        'All singular values are 1, so the flip is not caused by attenuation',
        fontsize=13,
    )
    fig.savefig(output, dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_noise_threshold(probabilities: np.ndarray, output: Path) -> float | None:
    probabilities = np.asarray(probabilities, dtype=float)
    _, threshold = noise_transition_threshold(probabilities)
    eps_values = np.linspace(0.0, 0.2 if threshold is not None and threshold < 0.2 else 0.98, 500)

    q_curves = []
    for i, j in EDGES:
        q_curves.append(
            eps_values * (1 - 2 * probabilities[i]) * (1 - 2 * probabilities[j])
            - 4 * probabilities[i] * probabilities[j]
        )

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, q_values in zip(EDGE_LABELS, q_curves):
        ax.plot(eps_values, q_values, linewidth=2, label=f'q{label}(ε)')
    ax.axhline(0.0, linewidth=1)
    if threshold is not None and eps_values[0] <= threshold <= eps_values[-1]:
        ax.axvline(threshold, linestyle='--', linewidth=2,
                   label=f'exact rank-loss threshold ε*={threshold:.6f}')
    ax.set_xlabel('white-noise fraction ε')
    ax.set_ylabel('population-response sign function qᵢⱼ(ε)')
    ax.set_title(
        'Exact transition mechanism: a loop-class change requires an edge response to cross zero'
    )
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig(output, dpi=180, bbox_inches='tight')
    plt.close(fig)
    return threshold


def save_noise_phase_diagram(output: Path) -> None:
    p1_values = np.linspace(1/3, 0.97, 320)
    epsilon_values = np.linspace(0.0, 0.5, 300)
    image = np.zeros((len(epsilon_values), len(p1_values)))

    # Symmetric slice p2=p3=(1-p1)/2.
    for x_idx, p1 in enumerate(p1_values):
        p2 = p3 = (1.0 - p1) / 2.0
        probabilities = np.array([p1, p2, p3])
        for y_idx, epsilon in enumerate(epsilon_values):
            sign_product, q_values = regularized_population_covariance_signs(probabilities, epsilon)
            if any(abs(q) < 1e-4 for q in q_values):
                image[y_idx, x_idx] = 0.0
            elif sign_product < 0:
                image[y_idx, x_idx] = -1.0
            else:
                image[y_idx, x_idx] = 1.0

    fig, ax = plt.subplots(figsize=(10, 6))
    mesh = ax.imshow(
        image,
        origin='lower',
        aspect='auto',
        extent=[p1_values[0], p1_values[-1], epsilon_values[0], epsilon_values[-1]],
        interpolation='nearest',
    )
    ax.set_xlabel('dominant probability p₁, with p₂=p₃=(1−p₁)/2')
    ax.set_ylabel('white-noise fraction ε')
    ax.set_title('Noise phase diagram: reflection, rank-loss boundary, and identity')
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(['reflection', 'rank loss', 'identity'])
    fig.savefig(output, dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_transition_animation(amplitudes: np.ndarray, output: Path) -> None:
    amplitudes = normalize_amplitudes(amplitudes)
    probabilities = np.abs(amplitudes) ** 2
    _, threshold = noise_transition_threshold(probabilities)
    if threshold is None:
        raise ValueError('animation example requires one dominant probability > 1/2')

    eps_values = np.concatenate([
        np.linspace(max(0.0, threshold - 0.045), threshold - 0.0015, 24),
        np.array([threshold]),
        np.linspace(threshold + 0.0015, threshold + 0.045, 24),
    ])

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(frame: int):
        ax.clear()
        epsilon = float(eps_values[frame])
        result = loop_result(generalized_w_density(amplitudes, epsilon), rank_tolerance=1e-9)
        H = np.real_if_close(result.loop).astype(float)
        draw_sphere_wireframe(ax)

        for vector, label in zip(np.eye(3), ('X', 'Y', 'Z')):
            image = H @ vector
            ax.quiver(0, 0, 0, *vector, linewidth=2.2, arrow_length_ratio=0.12)
            if np.linalg.norm(image) > 1e-10:
                ax.quiver(0, 0, 0, *image, linewidth=4.0, arrow_length_ratio=0.12, linestyle='dashed')
            ax.text(*(vector * 1.12), f'{label} start', fontsize=9)
            if np.linalg.norm(image) > 1e-10:
                ax.text(*(image * 1.25), f'{label} after', fontsize=9)

        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax.set_zlim(-1.35, 1.35)
        ax.set_box_aspect((1, 1, 1))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.view_init(elev=24, azim=38)
        eigenvalues = np.round(np.real_if_close(np.sort_complex(result.eigenvalues)).real, 4)
        singular_values = np.round(result.singular_values, 4)
        ax.set_title(
            f'Noise-driven loop transition   ε={epsilon:.5f}   ε*={threshold:.5f}\n'
            f'{classify_loop(result)}\n'
            f'eigenvalues={tuple(eigenvalues)}   singular={tuple(singular_values)}'
        )
        return []

    animation = FuncAnimation(fig, update, frames=len(eps_values), interval=150, blit=False)
    animation.save(output, writer=PillowWriter(fps=7))
    plt.close(fig)


def run_assertions(amplitudes: np.ndarray) -> dict:
    amplitudes = normalize_amplitudes(amplitudes)
    pure_result = loop_result(generalized_w_density(amplitudes))

    np.testing.assert_allclose(
        pure_result.loop.T @ pure_result.loop,
        np.eye(3),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        np.sort_complex(pure_result.eigenvalues),
        np.array([-1.0, 1.0, 1.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(pure_result.determinant, -1.0, atol=1e-10)

    transition_amplitudes = np.sqrt(np.array([0.8, 0.1, 0.1]))
    probabilities = np.abs(transition_amplitudes) ** 2
    _, threshold = noise_transition_threshold(probabilities)
    assert threshold is not None
    np.testing.assert_allclose(threshold, 1.0 / 16.0, atol=1e-14)

    below = loop_result(generalized_w_density(transition_amplitudes, threshold - 0.01), rank_tolerance=1e-12)
    at = loop_result(generalized_w_density(transition_amplitudes, threshold), rank_tolerance=1e-12)
    above = loop_result(generalized_w_density(transition_amplitudes, threshold + 0.01), rank_tolerance=1e-12)

    np.testing.assert_allclose(np.sort_complex(below.eigenvalues), [-1.0, 1.0, 1.0], atol=1e-10)
    np.testing.assert_allclose(at.singular_values, [1.0, 1.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(np.sort_complex(above.eigenvalues), [1.0, 1.0, 1.0], atol=1e-10)

    return {
        'pure_amplitudes': [[float(z.real), float(z.imag)] for z in amplitudes],
        'pure_probabilities': [float(x) for x in np.abs(amplitudes) ** 2],
        'pure_loop_matrix': np.real_if_close(pure_result.loop).tolist(),
        'pure_loop_eigenvalues': [float(x.real) for x in np.sort_complex(pure_result.eigenvalues)],
        'pure_loop_singular_values': [float(x) for x in pure_result.singular_values],
        'pure_loop_determinant': float(pure_result.determinant),
        'orthogonality_error': float(np.max(np.abs(pure_result.loop.T @ pure_result.loop - np.eye(3)))),
        'transition_example_probabilities': [0.8, 0.1, 0.1],
        'transition_threshold': float(threshold),
        'below_threshold_class': classify_loop(below),
        'at_threshold_class': classify_loop(at),
        'above_threshold_class': classify_loop(above),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path('visual_output'))
    parser.add_argument('--skip-animation', action='store_true')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Unequal magnitudes and nonzero phases make the robustness visible.
    amplitudes = normalize_amplitudes(np.array([
        np.sqrt(0.47) * np.exp(0.31j),
        np.sqrt(0.32) * np.exp(-0.77j),
        np.sqrt(0.21) * np.exp(1.14j),
    ]))

    summary = run_assertions(amplitudes)
    save_edge_transport_triangle(amplitudes, 0.0, args.output_dir / '01_edge_transport_triangle.png')
    save_loop_reflection_3d(amplitudes, 0.0, args.output_dir / '02_loop_reflection_3d.png')

    transition_probabilities = np.array([0.8, 0.1, 0.1])
    save_noise_threshold(transition_probabilities, args.output_dir / '03_noise_threshold.png')
    save_noise_phase_diagram(args.output_dir / '04_noise_phase_diagram.png')
    if not args.skip_animation:
        save_transition_animation(np.sqrt(transition_probabilities), args.output_dir / '05_transition.gif')

    with (args.output_dir / 'verification_summary.json').open('w') as handle:
        json.dump(summary, handle, indent=2)

    print('VISUAL W-HOLONOMY SIMULATION: PASS')
    print(json.dumps(summary, indent=2))
    print(f'Visuals written to: {args.output_dir.resolve()}')


if __name__ == '__main__':
    main()
