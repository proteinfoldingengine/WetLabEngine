import numpy as np

from w_holonomy_replication import (
    generalized_w_density,
    ghz_density,
    loop_result,
    noise_transition_threshold,
)


def test_pure_generalized_w_reflection():
    amplitudes = np.array([
        0.5 * np.exp(0.2j),
        0.6 * np.exp(-0.7j),
        0.7 * np.exp(1.1j),
    ])
    result = loop_result(generalized_w_density(amplitudes))
    np.testing.assert_allclose(
        np.sort_complex(result.eigenvalues),
        np.array([-1.0, 1.0, 1.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(result.loop.T @ result.loop, np.eye(3), atol=1e-10)


def test_controls():
    product = loop_result(np.eye(8) / 8.0)
    classical = loop_result(ghz_density(False))
    coherent = loop_result(ghz_density(True))

    np.testing.assert_allclose(product.singular_values, [0.0, 0.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(classical.singular_values, [1.0, 0.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(coherent.singular_values, [1.0, 0.0, 0.0], atol=1e-10)


def test_noise_transition():
    amplitudes = np.sqrt(np.array([0.8, 0.1, 0.1]))
    _, threshold = noise_transition_threshold(np.abs(amplitudes) ** 2)
    np.testing.assert_allclose(threshold, 1.0 / 16.0, atol=1e-14)

    below = loop_result(generalized_w_density(amplitudes, 0.05), rank_tolerance=1e-12)
    at = loop_result(generalized_w_density(amplitudes, threshold), rank_tolerance=1e-12)
    above = loop_result(generalized_w_density(amplitudes, 0.07), rank_tolerance=1e-12)

    np.testing.assert_allclose(
        np.sort_complex(below.eigenvalues),
        np.array([-1.0, 1.0, 1.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(at.singular_values, [1.0, 1.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(
        np.sort_complex(above.eigenvalues),
        np.array([1.0, 1.0, 1.0]),
        atol=1e-10,
    )
