import numpy as np
from visual_w_holonomy_simulation import run_assertions


def test_visual_assertion_layer():
    amplitudes = np.array([
        np.sqrt(0.47) * np.exp(0.31j),
        np.sqrt(0.32) * np.exp(-0.77j),
        np.sqrt(0.21) * np.exp(1.14j),
    ])
    summary = run_assertions(amplitudes)
    assert summary['pure_loop_eigenvalues'] == [-1.0, 1.0, 1.0]
    assert abs(summary['pure_loop_determinant'] + 1.0) < 1e-10
    assert summary['transition_threshold'] == 0.0625
    assert summary['below_threshold_class'] == 'LOSSLESS REFLECTION'
    assert summary['at_threshold_class'] == 'RANK-LOSS SURFACE'
    assert summary['above_threshold_class'] == 'LOSSLESS IDENTITY'
