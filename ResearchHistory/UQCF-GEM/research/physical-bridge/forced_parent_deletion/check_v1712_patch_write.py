"""Replay four fixed checks in the unchanged archived V1712 caller."""

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from sys import argv
from unittest.mock import patch

import numpy as np


PATH = "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1712_rg.py"
BLOB = "bc4504edbde3bc35815959f7f52288a57dced81a"
DIMENSION = 6
GAIN = Fraction(17, 100)
ONE = (Fraction(1),) * DIMENSION
BASELINE = (Fraction(4),) * DIMENSION
CHANGED = (Fraction(7), Fraction(1), *BASELINE[2:])
SHIFTED = (CHANGED[-1], *CHANGED[:-1])
PARALLEL = (Fraction(5),) * DIMENSION
TOLERANCE = 2e-10


def load_implementation(source_path):
    data = source_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if blob != BLOB:
        raise ValueError("Archived V1712 source does not match the verified blob")
    functions = {}
    definitions = b"".join(data.splitlines(keepends=True)[:60])
    exec(compile(definitions, source_path, "exec"), functions)
    return functions


def expected_patch(right, gain):
    return tuple(1 + gain**2 * (right[i - 1] - right[i]) for i in range(DIMENSION))


def exact_tensor(q, gain):
    """Evaluate the closed form for the no-floor region in rational arithmetic."""
    n = len(q)
    half = Fraction(1, 2)
    metric = [
        [
            int(i == j) * (1 - gain * q[i - 1])
            + half * gain * (int(j == (i - 1) % n) * q[i] + int(i == (j - 1) % n) * q[j])
            for j in range(n)
        ]
        for i in range(n)
    ]
    radius_bound = max(map(abs, q)) + Fraction(1, 10_000)
    assert 1 - 2 * abs(gain) * radius_bound > Fraction(1, 1_000_000)

    layers = []
    for k in range(n):
        successor = (k + 1) % n
        predecessor = (k - 1) % n
        derivative = [
            [gain * (int(i == k and j == predecessor) - int(i == j == successor)) for j in range(n)]
            for i in range(n)
        ]
        layer = []
        for i in range(n):
            row = []
            for j in range(n):
                connection_terms = sum(
                    derivative[l][i] * metric[l][j] + metric[i][l] * derivative[l][j] for l in range(n)
                )
                row.append(half * (derivative[i][j] + derivative[j][i]) - connection_terms)
            layer.append(row)
        assert layer[successor][successor] == gain - 2 * gain**2 * q[k]
        layers.append(layer)
    return layers


def squared_norm(tensor):
    return sum(x**2 for layer in tensor for row in layer for x in row)


def replay_case(implementation, right, gain):
    transport = implementation["native_T"]
    q_at_scale = implementation["Q_at_scale"]
    patch_write = implementation["rg_step"]
    read = implementation["Qtensor"]
    inputs = [np.asarray(state, dtype=float) for state in (ONE, right, ONE, ONE)]
    draws = iter(inputs)

    class FixedDraws:
        def normal(self, size):
            assert size == DIMENSION
            return next(draws).copy()

    expected_q = expected_patch(right, gain)
    expected = exact_tensor(expected_q, gain)
    reference = exact_tensor(ONE, gain)
    predicted = [
        math.sqrt(squared_norm(reference)),
        (math.sqrt(squared_norm(reference)) + math.sqrt(squared_norm(expected))) / 2,
    ]
    with patch.object(np.random, "default_rng", return_value=FixedDraws()):
        rows = q_at_scale(float(gain), transport, n0=len(inputs))
    assert next(draws, None) is None
    assert [(block, count) for block, _, count in rows] == [(1, 4), (2, 2)]
    np.testing.assert_allclose([value for _, value, _ in rows], predicted, rtol=0, atol=TOLERANCE)

    first, second = patch_write(inputs, float(gain), transport)
    np.testing.assert_allclose(first, np.asarray(expected_q, dtype=float), rtol=0, atol=TOLERANCE)
    np.testing.assert_allclose(second, np.asarray(ONE, dtype=float), rtol=0, atol=TOLERANCE)
    np.testing.assert_allclose(
        read(first, float(gain), transport), np.asarray(expected, dtype=float), rtol=0, atol=TOLERANCE
    )
    return {
        "first_coarse_patch": [str(x) for x in expected_q],
        "first_coarse_tensor_norm_squared": str(squared_norm(expected)),
        "scale_medians": [f"{value:.10f}" for value in predicted],
    }


def main(source_path):
    original = load_implementation(source_path)
    baseline = replay_case(original, BASELINE, GAIN)
    changed = replay_case(original, CHANGED, GAIN)
    shifted = replay_case(original, SHIFTED, GAIN)
    parallel = replay_case(original, PARALLEL, GAIN)
    flat = replay_case(original, BASELINE, Fraction(0))
    flat_changed = replay_case(original, CHANGED, Fraction(0))

    assert sum(BASELINE) == sum(CHANGED) == sum(SHIFTED) != sum(PARALLEL)
    assert changed["scale_medians"][0] == baseline["scale_medians"][0]
    assert float(changed["scale_medians"][1]) > float(baseline["scale_medians"][1])
    assert (
        changed["first_coarse_patch"]
        == [str(1 - 3 * GAIN**2), str(1 + 6 * GAIN**2), str(1 - 3 * GAIN**2), "1", "1", "1"]
    )
    assert shifted["first_coarse_patch"] != changed["first_coarse_patch"]
    assert shifted["scale_medians"] == changed["scale_medians"]
    assert parallel == baseline
    assert flat_changed == flat
    assert flat["first_coarse_tensor_norm_squared"] == "0"
    difference = Fraction(changed["first_coarse_tensor_norm_squared"]) - Fraction(
        baseline["first_coarse_tensor_norm_squared"]
    )
    assert difference > 0
    return {
        "source_blob": BLOB,
        "baseline": baseline,
        "changed": changed,
        "shifted": shifted,
        "parallel": parallel,
        "zero_coupling": flat,
        "squared_norm_contrast_at_written_patch": str(difference),
    }


if __name__ == "__main__":
    path = Path(argv[1]) if len(argv) == 2 else Path(__file__).resolve().parents[5] / PATH
    print(json.dumps(main(path), indent=2, sort_keys=True))

