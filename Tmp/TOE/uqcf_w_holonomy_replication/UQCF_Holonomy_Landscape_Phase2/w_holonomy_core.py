#!/usr/bin/env python3
"""
Independent replication harness for pair-marginal BKM observable-response holonomy
in generalized three-qubit W states.

The implementation starts from an explicit 8x8 global density matrix and uses:
- exact pair and one-qubit partial traces,
- centered Pauli observable bases,
- explicit Kubo-Mori/BKM metric matrices,
- covariance-defined Riesz response maps,
- metric whitening,
- SVD-based *supported* polar partial isometries,
- triangle-loop composition.

It verifies:
1. product-state zero-support control;
2. classical/coherent GHZ rank-one support controls;
3. pure generalized-W reflection holonomy;
4. local-unitary, basis, phase, and permutation invariance;
5. the exact white-noise sign-threshold classification;
6. the rank-loss transition surface where reflection changes to identity.

This is an executable finite-model verification, not a claim about spacetime or gravity.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
import numpy as np
from scipy.linalg import eigh, svd
from scipy.stats import unitary_group


I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SIGMA_X, SIGMA_Y, SIGMA_Z)
EDGES = ((0, 1), (1, 2), (2, 0))


def bits_to_index(bits: tuple[int, ...]) -> int:
    idx = 0
    for bit in bits:
        idx = (idx << 1) | bit
    return idx


def reduced_density(rho: np.ndarray, keep_order: tuple[int, ...], n: int = 3) -> np.ndarray:
    """Partial trace while preserving the requested subsystem order."""
    traced = tuple(q for q in range(n) if q not in keep_order)
    out = np.zeros((2 ** len(keep_order), 2 ** len(keep_order)), dtype=complex)
    for ket_keep in itertools.product((0, 1), repeat=len(keep_order)):
        for bra_keep in itertools.product((0, 1), repeat=len(keep_order)):
            total = 0j
            for traced_bits in itertools.product((0, 1), repeat=len(traced)):
                ket = [0] * n
                bra = [0] * n
                for q, value in zip(keep_order, ket_keep):
                    ket[q] = value
                for q, value in zip(keep_order, bra_keep):
                    bra[q] = value
                for q, value in zip(traced, traced_bits):
                    ket[q] = value
                    bra[q] = value
                total += rho[bits_to_index(tuple(ket)), bits_to_index(tuple(bra))]
            out[bits_to_index(ket_keep), bits_to_index(bra_keep)] = total
    return out


def generalized_w_density(
    amplitudes: np.ndarray,
    epsilon: float = 0.0,
) -> np.ndarray:
    amplitudes = np.asarray(amplitudes, dtype=complex)
    if amplitudes.shape != (3,):
        raise ValueError("amplitudes must contain exactly three complex values")
    norm = np.linalg.norm(amplitudes)
    if norm == 0:
        raise ValueError("amplitudes cannot all vanish")
    amplitudes = amplitudes / norm

    psi = np.zeros(8, dtype=complex)
    psi[bits_to_index((1, 0, 0))] = amplitudes[0]
    psi[bits_to_index((0, 1, 0))] = amplitudes[1]
    psi[bits_to_index((0, 0, 1))] = amplitudes[2]
    pure = np.outer(psi, psi.conj())

    if not 0.0 <= epsilon < 1.0:
        raise ValueError("epsilon must satisfy 0 <= epsilon < 1")
    return (1.0 - epsilon) * pure + epsilon * np.eye(8) / 8.0


def ghz_density(coherent: bool) -> np.ndarray:
    if coherent:
        psi = np.zeros(8, dtype=complex)
        psi[0] = psi[7] = 1.0 / np.sqrt(2.0)
        return np.outer(psi, psi.conj())
    rho = np.zeros((8, 8), dtype=complex)
    rho[0, 0] = rho[7, 7] = 0.5
    return rho


def logarithmic_mean(a: float, b: float) -> float:
    scale = max(1.0, abs(a), abs(b))
    if abs(a - b) < 1e-14 * scale:
        return 0.5 * (a + b)
    return (a - b) / (np.log(a) - np.log(b))


def centered_pauli_basis(rho: np.ndarray) -> list[np.ndarray]:
    return [sigma - np.trace(rho @ sigma) * I2 for sigma in PAULI]


def transformed_centered_basis(rho: np.ndarray, transform: np.ndarray) -> list[np.ndarray]:
    base = centered_pauli_basis(rho)
    return [
        sum(transform[row, col] * base[col] for col in range(3))
        for row in range(3)
    ]


def bkm_metric(rho: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    eigenvalues, eigenvectors = eigh(rho)
    if np.min(eigenvalues) <= 0:
        raise ValueError("local marginal must be faithful for this implementation")
    matrices = [eigenvectors.conj().T @ op @ eigenvectors for op in basis]
    metric = np.zeros((3, 3), dtype=float)
    for a, op_a in enumerate(matrices):
        for b, op_b in enumerate(matrices):
            value = 0j
            for m in range(2):
                for n in range(2):
                    value += (
                        logarithmic_mean(eigenvalues[m], eigenvalues[n])
                        * op_a[m, n]
                        * op_b[n, m]
                    )
            metric[a, b] = value.real
    return metric


def inverse_sqrt_spd(matrix: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = eigh(matrix)
    if np.min(eigenvalues) <= 0:
        raise ValueError(f"matrix is not positive definite: {eigenvalues}")
    return (eigenvectors * (1.0 / np.sqrt(eigenvalues))) @ eigenvectors.T


def cross_covariance(
    pair_state: np.ndarray,
    basis_i: list[np.ndarray],
    basis_j: list[np.ndarray],
) -> np.ndarray:
    covariance = np.zeros((3, 3), dtype=float)
    for a, op_i in enumerate(basis_i):
        for b, op_j in enumerate(basis_j):
            covariance[a, b] = np.trace(
                pair_state @ np.kron(op_i, op_j)
            ).real
    return covariance


@dataclass
class EdgeResult:
    polar: np.ndarray
    singular_values: np.ndarray
    whitened_response: np.ndarray


def edge_polar(
    rho_global: np.ndarray,
    i: int,
    j: int,
    basis_transforms: tuple[np.ndarray, np.ndarray] | None = None,
    rank_tolerance: float = 1e-10,
) -> EdgeResult:
    rho_i = reduced_density(rho_global, (i,))
    rho_j = reduced_density(rho_global, (j,))
    rho_ij = reduced_density(rho_global, (i, j))

    if basis_transforms is None:
        basis_i = centered_pauli_basis(rho_i)
        basis_j = centered_pauli_basis(rho_j)
    else:
        basis_i = transformed_centered_basis(rho_i, basis_transforms[0])
        basis_j = transformed_centered_basis(rho_j, basis_transforms[1])

    metric_i = bkm_metric(rho_i, basis_i)
    metric_j = bkm_metric(rho_j, basis_j)
    covariance = cross_covariance(rho_ij, basis_i, basis_j)

    # Coordinates of the whitened Riesz response map i -> j.
    whitened = (
        inverse_sqrt_spd(metric_j)
        @ covariance.T
        @ inverse_sqrt_spd(metric_i)
    )

    left, singular_values, right_h = svd(whitened)
    support = np.diag((singular_values > rank_tolerance).astype(float))

    # Supported polar partial isometry; zero on the kernel.
    polar = left @ support @ right_h
    return EdgeResult(polar, singular_values, whitened)


@dataclass
class LoopResult:
    loop: np.ndarray
    edge_results: list[EdgeResult]

    @property
    def singular_values(self) -> np.ndarray:
        return svd(self.loop, compute_uv=False)

    @property
    def eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvals(self.loop)

    @property
    def determinant(self) -> float:
        return float(np.linalg.det(self.loop))


def loop_result(
    rho_global: np.ndarray,
    basis_transforms: list[np.ndarray] | None = None,
    rank_tolerance: float = 1e-10,
) -> LoopResult:
    edge_results: list[EdgeResult] = []
    for i, j in EDGES:
        transforms = None
        if basis_transforms is not None:
            transforms = (basis_transforms[i], basis_transforms[j])
        edge_results.append(
            edge_polar(rho_global, i, j, transforms, rank_tolerance)
        )

    loop = (
        edge_results[2].polar
        @ edge_results[1].polar
        @ edge_results[0].polar
    )
    return LoopResult(loop, edge_results)


def regularized_population_covariance_signs(
    probabilities: np.ndarray,
    epsilon: float,
) -> tuple[int, list[float]]:
    """
    For generalized W probabilities p_i=|a_i|^2, the centered Z covariance sign
    on edge i-j is the sign of

        q_ij(eps) = eps(1-2p_i)(1-2p_j) - 4p_i p_j.

    The positive prefactor (1-eps) does not affect the sign.
    """
    probabilities = np.asarray(probabilities, dtype=float)
    q_values = []
    for i, j in EDGES:
        q = (
            epsilon
            * (1.0 - 2.0 * probabilities[i])
            * (1.0 - 2.0 * probabilities[j])
            - 4.0 * probabilities[i] * probabilities[j]
        )
        q_values.append(float(q))

    if any(abs(q) < 1e-12 for q in q_values):
        return 0, q_values
    return int(np.prod(np.sign(q_values))), q_values


def noise_transition_threshold(probabilities: np.ndarray) -> tuple[tuple[int, int] | None, float | None]:
    """
    If one probability p_k exceeds 1/2, the edge opposite node k changes its
    population-response sign at

        eps* = 4 p_i p_j / [(1-2p_i)(1-2p_j)].

    Otherwise no transition occurs for 0 <= eps < 1.
    """
    probabilities = np.asarray(probabilities, dtype=float)
    dominant = int(np.argmax(probabilities))
    if probabilities[dominant] <= 0.5:
        return None, None
    opposite = tuple(i for i in range(3) if i != dominant)
    i, j = opposite
    threshold = (
        4.0 * probabilities[i] * probabilities[j]
        / ((1.0 - 2.0 * probabilities[i]) * (1.0 - 2.0 * probabilities[j]))
    )
    return (i, j), float(threshold)


def random_unitary_local_test(rho: np.ndarray, rng: np.random.Generator) -> None:
    unitaries = [unitary_group.rvs(2, random_state=rng) for _ in range(3)]
    total = np.kron(np.kron(unitaries[0], unitaries[1]), unitaries[2])
    transformed = total @ rho @ total.conj().T
    result = loop_result(transformed)
    np.testing.assert_allclose(
        np.sort_complex(result.eigenvalues),
        np.array([-1.0, 1.0, 1.0]),
        atol=1e-10,
    )


def permute_qubits(rho: np.ndarray, permutation: tuple[int, int, int]) -> np.ndarray:
    tensor = rho.reshape([2] * 6)
    axes = list(permutation) + [q + 3 for q in permutation]
    return np.transpose(tensor, axes).reshape(8, 8)


def assert_spectrum(actual: np.ndarray, expected: np.ndarray, atol: float = 1e-10) -> None:
    np.testing.assert_allclose(
        np.sort_complex(actual),
        np.sort_complex(expected),
        atol=atol,
    )


def run_verification(seed: int = 168864, trials: int = 100) -> None:
    rng = np.random.default_rng(seed)

    # Controls.
    product = loop_result(np.eye(8) / 8.0)
    np.testing.assert_allclose(product.singular_values, np.zeros(3), atol=1e-12)

    classical_ghz = loop_result(ghz_density(coherent=False))
    coherent_ghz = loop_result(ghz_density(coherent=True))
    np.testing.assert_allclose(classical_ghz.singular_values, [1.0, 0.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(coherent_ghz.singular_values, [1.0, 0.0, 0.0], atol=1e-10)

    # Random pure generalized-W states.
    max_orthogonality_error = 0.0
    for _ in range(trials):
        magnitudes = rng.uniform(0.05, 1.5, 3)
        phases = rng.uniform(-np.pi, np.pi, 3)
        amplitudes = magnitudes * np.exp(1j * phases)
        amplitudes /= np.linalg.norm(amplitudes)
        rho = generalized_w_density(amplitudes)

        result = loop_result(rho)
        max_orthogonality_error = max(
            max_orthogonality_error,
            float(np.max(np.abs(result.loop.T @ result.loop - np.eye(3)))),
        )
        assert_spectrum(result.eigenvalues, np.array([-1.0, 1.0, 1.0]))
        np.testing.assert_allclose(result.determinant, -1.0, atol=1e-10)

        # Local-unitary covariance.
        random_unitary_local_test(rho, rng)

        # Random source-basis changes.
        transforms = []
        for _node in range(3):
            while True:
                transform = rng.normal(size=(3, 3))
                if abs(np.linalg.det(transform)) > 0.1:
                    transforms.append(transform)
                    break
        basis_result = loop_result(rho, basis_transforms=transforms)
        assert_spectrum(basis_result.eigenvalues, np.array([-1.0, 1.0, 1.0]))

        # All qubit permutations.
        for permutation in itertools.permutations(range(3)):
            permuted = permute_qubits(rho, permutation)
            permuted_result = loop_result(permuted)
            assert_spectrum(permuted_result.eigenvalues, np.array([-1.0, 1.0, 1.0]))

    # Noise-transition classification across random regularized W states.
    classification_mismatches = 0
    for _ in range(trials):
        magnitudes = rng.uniform(0.05, 1.5, 3)
        phases = rng.uniform(-np.pi, np.pi, 3)
        amplitudes = magnitudes * np.exp(1j * phases)
        amplitudes /= np.linalg.norm(amplitudes)
        epsilon = float(rng.uniform(0.0, 0.98))
        rho = generalized_w_density(amplitudes, epsilon)
        result = loop_result(rho, rank_tolerance=1e-9)

        probabilities = np.abs(amplitudes) ** 2
        predicted, _ = regularized_population_covariance_signs(probabilities, epsilon)
        edge_ranks = [
            int(np.sum(edge.singular_values > 1e-9))
            for edge in result.edge_results
        ]

        if predicted != 0 and min(edge_ranks) == 3:
            observed = int(round(result.determinant))
            if observed != predicted:
                classification_mismatches += 1

    if classification_mismatches:
        raise AssertionError(
            f"noise classification mismatches: {classification_mismatches}"
        )

    # Explicit transition example p=(0.8,0.1,0.1), eps*=1/16.
    amplitudes = np.sqrt(np.array([0.8, 0.1, 0.1]))
    _, threshold = noise_transition_threshold(np.abs(amplitudes) ** 2)
    np.testing.assert_allclose(threshold, 1.0 / 16.0, atol=1e-14)

    below = loop_result(generalized_w_density(amplitudes, 0.05), rank_tolerance=1e-12)
    at = loop_result(generalized_w_density(amplitudes, threshold), rank_tolerance=1e-12)
    above = loop_result(generalized_w_density(amplitudes, 0.07), rank_tolerance=1e-12)

    assert_spectrum(below.eigenvalues, np.array([-1.0, 1.0, 1.0]))
    np.testing.assert_allclose(at.singular_values, [1.0, 1.0, 0.0], atol=1e-10)
    assert_spectrum(above.eigenvalues, np.array([1.0, 1.0, 1.0]))

    print("INDEPENDENT W-HOLONOMY REPLICATION: PASS")
    print(f"Pure generalized-W trials: {trials}")
    print(f"Regularized classification trials: {trials}")
    print(f"Maximum pure-state orthogonality error: {max_orthogonality_error:.3e}")
    print()
    print("Controls:")
    print("  product loop singular values:", product.singular_values)
    print("  classical GHZ loop singular values:", classical_ghz.singular_values)
    print("  coherent GHZ loop singular values:", coherent_ghz.singular_values)
    print()
    print("Corrected theorem:")
    print("  Pure generalized-W states: reflection spectrum {-1,+1,+1}.")
    print("  Regularized states: reflection or identity, determined by the")
    print("  product of the three population-covariance signs.")
    print("  Sign changes occur only through an edge-rank-loss surface.")
    print()
    print("Transition example p=(0.8,0.1,0.1):")
    print(f"  epsilon* = {threshold:.12f}")
    print("  below threshold eigenvalues:", np.sort_complex(below.eigenvalues))
    print("  at threshold loop singular values:", at.singular_values)
    print("  above threshold eigenvalues:", np.sort_complex(above.eigenvalues))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=168864)
    parser.add_argument("--trials", type=int, default=100)
    args = parser.parse_args()
    run_verification(args.seed, args.trials)


if __name__ == "__main__":
    main()
