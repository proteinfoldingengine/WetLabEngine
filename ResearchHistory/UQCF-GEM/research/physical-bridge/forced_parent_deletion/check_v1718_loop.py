"""Replay selected V1718 routines at frozen inputs and reconstruct their outputs."""

import ast
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ORIGINAL = Path("Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1718_complete.py")
ORIGINAL_BLOB = "638e68d00762642d6b58f692e7a1747816752232"
DIMENSION = 8
COUPLING = 0.17
TOLERANCE = 1e-12
ORIGINAL_FUNCTIONS = {"roll", "native_T", "Jgen", "invertible_T", "fwd_rev", "loop_drift"}


class ScriptedNormals:
    def __init__(self, vectors):
        self.vectors = list(vectors)
        self.position = 0

    def normal(self, *, size):
        assert size == DIMENSION
        vector = self.vectors[self.position]
        self.position += 1
        return vector.copy()

    def assert_exhausted(self):
        assert self.position == len(self.vectors)


def load_source(output):
    data = ORIGINAL.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    assert blob == ORIGINAL_BLOB
    (output / "v1718_complete.py").write_bytes(data)
    tree = ast.parse(data, filename=str(ORIGINAL))
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ORIGINAL_FUNCTIONS]
    assert {node.name for node in selected} == ORIGINAL_FUNCTIONS and len(selected) == len(ORIGINAL_FUNCTIONS)
    namespace = {"np": np, "expm": expm, "DIM": DIMENSION}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(ORIGINAL), "exec"), namespace)
    return namespace, hashlib.sha256(data).hexdigest()


def original_read(source, function, transport, *draws):
    generator = ScriptedNormals(draws)
    source["rng"] = generator
    result = source[function](source[transport])
    generator.assert_exhausted()
    return result


def independent_matrix(source_value, coupling):
    operator = np.diag(1 - coupling * source_value[np.arange(DIMENSION) - 1])
    for index in range(DIMENSION):
        operator[index, index - 1] = coupling * source_value[index]
    return operator


def original_matrix(transport, q, coupling=COUPLING):
    return np.column_stack([transport(direction, q, coupling) for direction in np.eye(DIMENSION)])


def check(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=0, atol=TOLERANCE)


def rounded(value):
    return np.asarray(value).round(12).tolist()


def run(output):
    output.mkdir(parents=True, exist_ok=True)
    source, source_sha256 = load_source(output)
    native = source["native_T"]
    basis = np.eye(DIMENSION)
    identity = basis.copy()
    zero = np.zeros(DIMENSION)
    result = {"original_path": str(ORIGINAL), "original_blob": ORIGINAL_BLOB, "original_sha256": source_sha256}

    profiles = (basis[0] + basis[2], 2 * basis[0])
    predictions = ((0.6889, 0.83), (0.66, 1.0))
    matched = []
    for q, (expected_determinant, expected_norm) in zip(profiles, predictions, strict=True):
        h = original_matrix(native, zero) @ original_matrix(native, zero) @ original_matrix(native, q)
        check(h, independent_matrix(q, COUPLING))
        determinant = np.linalg.det(h)
        norm = original_read(source, "loop_drift", "native_T", basis[3], zero, q, zero)
        check([q.sum(), determinant, norm], [2, expected_determinant, expected_norm])
        check(np.linalg.norm(h @ basis[3]), norm)
        matched.append({"q1": rounded(q), "matrix": rounded(h), "determinant": rounded(determinant), "loop_norm": rounded(norm)})
    assert abs(matched[0]["determinant"] - matched[1]["determinant"]) > 0.02
    result["matched_source_loops"] = matched

    q = basis[0]
    x = basis[1]
    original_forward_norm, repeated_forward_error = original_read(source, "fwd_rev", "native_T", x, q, q)
    h = original_matrix(native, q)
    check(h, independent_matrix(q, COUPLING))
    forward = native(x, q)
    inverse_reconstruction = np.linalg.solve(h, forward)
    check(inverse_reconstruction, x)
    check([original_forward_norm, repeated_forward_error], [0.83, 0.3111])
    check(np.linalg.norm(h @ h @ x - x), repeated_forward_error)
    result["reverse_comparison"] = {
        "forward_norm": rounded(original_forward_norm),
        "original_reverse_error": rounded(repeated_forward_error),
        "same_operator_inverse_error": rounded(np.linalg.norm(inverse_reconstruction - x)),
    }

    singular_source = q / COUPLING
    singular = original_matrix(native, singular_source)
    check(singular, independent_matrix(singular_source, COUPLING))
    check(singular @ x, zero)
    assert np.linalg.matrix_rank(singular) == DIMENSION - 1
    dense_source = np.full(DIMENSION, 2.0)
    full_cycle = original_matrix(native, dense_source, coupling=0.5)
    check(full_cycle, independent_matrix(dense_source, 0.5))
    check(np.linalg.det(full_cycle), -1)
    result["determinant_controls"] = {"singular_rank": int(np.linalg.matrix_rank(singular)), "full_cycle_determinant": -1}

    orthogonal = source["invertible_T"]
    h = original_matrix(orthogonal, zero) @ original_matrix(orthogonal, zero) @ original_matrix(orthogonal, q)
    norm = original_read(source, "loop_drift", "invertible_T", q, zero, q, zero)
    angle = COUPLING / 2
    rotation = identity.copy()
    rotation[0, 0] = rotation[-1, -1] = np.cos(angle)
    rotation[0, -1] = np.sin(angle)
    rotation[-1, 0] = -np.sin(angle)
    check(h, rotation)
    check(h.T @ h, identity)
    check(norm, 1)
    displacement = np.linalg.norm(h @ q - q)
    check(displacement, 2 * np.sin(angle / 2))
    assert displacement > 0.08
    result["orthogonal_loop"] = {"matrix": rounded(h), "loop_norm": rounded(norm), "vector_displacement": rounded(displacement)}

    samples = np.vstack((basis, -basis)) * np.sqrt(DIMENSION)
    check(samples.mean(axis=0), zero)
    check(samples.T @ samples / len(samples), identity)
    x = np.arange(1.0, DIMENSION + 1)
    x /= np.linalg.norm(x)
    values = np.array([native(x, q) for q in samples])
    check(values.mean(axis=0), x)
    observed = float(np.sum(values * values, axis=1).mean())
    one_step = 1 + 2 * COUPLING**2
    check(observed, one_step)
    result["squared_norm"] = {
        "one_step_moment_control": rounded(observed),
        "finite_source_sample_size": len(samples),
        "unit_initial_vector": rounded(x),
        "one_step_exact_factor": rounded(one_step),
        "three_step_exact_factor": rounded(one_step**3),
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
