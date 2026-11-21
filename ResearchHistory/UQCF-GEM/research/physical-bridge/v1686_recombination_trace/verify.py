"""Reproduce the four frozen V1686.35 controls without running the media dashboard."""
import argparse
import ast
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Tuple

import numpy as np


SOURCE = "Tmp/TOE/Einstein 9_v1686_l3_geometry_plus_information/v1686_35_forced_hd_export_fix_colab.py"
SOURCE_BLOB = "b780961cebf14a5bff0153d109e2855c878090ec"
DEFINITIONS = {
    "BranchCurrent", "RecombinedState", "as_state", "overlap_gate",
    "retained_order_orientation", "harmonic_closure_weight", "kernel_order_overlap",
    "retained_recombine", "associator_obstruction",
}
SIZE = 5
U, R, V, W = (2, 1), (2, 2), (0, 0), (4, 4)
CELLS = tuple(np.ndindex(SIZE, SIZE))


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def source_functions(path):
    raw = path.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(blob == SOURCE_BLOB, "Historical source identity changed")
    trees = ast.parse(raw, filename=str(path)).body
    nodes = [node for node in trees if isinstance(node, (ast.FunctionDef, ast.ClassDef))
             and node.name in DEFINITIONS]
    require(len(nodes) == len(DEFINITIONS) and {n.name for n in nodes} == DEFINITIONS,
            "Historical definitions are missing or duplicated")
    namespace = {"__name__": __name__, "np": np, "dataclass": dataclass, "Tuple": Tuple}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def field(entries):
    values = np.zeros((SIZE, SIZE))
    for location, amount in entries.items():
        values[location] = amount
    return values


def branch(ns, name, order, values):
    return ns["BranchCurrent"](name, name, order, np.ones_like(values), values.copy(), 1.0)


def exact_edges(a, b, use_destination_at_both_ends=False):
    """Independent scatter over forward edges using rational endpoint gates."""
    av = {p: Fraction(int(a[p])) for p in CELLS}
    bv = {p: Fraction(int(b[p])) for p in CELLS}
    raw_overlap = {p: min(abs(av[p]), abs(bv[p])) for p in CELLS}
    gate = {p: raw_overlap[p] / (1 + raw_overlap[p]) for p in CELLS}
    result = {p: av[p] + bv[p] for p in CELLS}
    for i, j in CELLS:
        origin = (i, j)
        for destination in (((i + 1) % SIZE, j), (i, (j + 1) % SIZE)):
            flux = av[origin] * bv[destination] / 2
            debit_gate = gate[destination] if use_destination_at_both_ends else gate[origin]
            result[origin] -= debit_gate * flux
            result[destination] += gate[destination] * flux
    return result


def nonlinear_same_roll(a, b):
    overlap = np.minimum(np.abs(a), np.abs(b))
    roll_a = (np.roll(a, 1, axis=0) + np.roll(a, 1, axis=1)) / 2
    roll_b = (np.roll(b, 1, axis=0) + np.roll(b, 1, axis=1)) / 2
    return a + b + overlap / (1 + overlap) * (roll_a * b - a * roll_b)


def exact_array_equal(array, values):
    return all(Fraction(float(array[p])) == values[p] for p in CELLS)


def witness(ns, beta, eta):
    a_minus = field({R: 1, V: 1})
    a_plus = field({R: 1, U: 1})
    b = field({R: beta, U: eta, W: 1 - eta})
    original = ns["retained_recombine"]
    input_b = branch(ns, "B", 2, b)
    outputs = []
    for a in (a_minus, a_plus):
        input_a = branch(ns, "A", 1, a)
        z = original(input_a, input_b)
        require(exact_array_equal(z.vector, exact_edges(a, b)), "Directed-edge verifier mismatch")
        require(z is not input_a and z is not input_b and z.sources == ("A", "B")
                and z.retained_order_signature == (1, 2), "Composite identity or provenance mismatch")
        require(np.array_equal(input_a.flow, a) and np.array_equal(input_b.flow, b)
                and np.all(input_a.support == 1) and np.all(input_b.support == 1)
                and not np.shares_memory(input_b.flow, z.vector), "Input branch was changed or aliased")
        tied = original(input_a, branch(ns, "B", 1, b))
        require(np.array_equal(tied.vector, a + b), "Tied order did not cancel the correction")
        calls = []

        def observed(left, right):
            out = original(left, right)
            calls.append((left, right, out))
            return out

        ns["retained_recombine"] = observed
        try:
            ns["associator_obstruction"](input_a, input_b, branch(ns, "C", 3, np.zeros_like(a)))
        finally:
            ns["retained_recombine"] = original
        require(len(calls) == 4 and calls[1][0] is calls[0][2]
                and np.array_equal(calls[1][2].vector, z.vector),
                "Historical nested caller did not reuse the first composite")
        outputs.append(z.vector)

    expected = field({U: 1 - eta * beta / 4, R: beta / 4, V: -1})
    delta = outputs[1] - outputs[0]
    require(np.array_equal(delta, expected), "Full 25-cell contrast differs from the frozen formula")
    require(a_plus.sum() == a_minus.sum() and delta.sum() == (1 - eta) * beta / 4,
            "Incorrect input or output balance")
    require(delta[R] != 0, "Constant-destination control was not rejected")
    if eta == 0:
        require(delta[U] == 1 and delta.sum() > 0, "Mandatory source-debit control survived")
        require(not exact_array_equal(outputs[1], exact_edges(a_plus, b, True)),
                "Using the destination gate for the debit was not rejected")
    if eta == 1:
        require(not np.array_equal(outputs[1], nonlinear_same_roll(a_plus, b)),
                "Same-direction kernel mutation was not rejected")
    return {"beta": beta, "eta": eta, "source_contrast": delta[U].item(),
            "destination_contrast": delta[R].item(), "compensator_contrast": delta[V].item(),
            "total_contrast": delta.sum().item(), "input_total_each": (a_plus + b).sum().item(),
            "checked_cells_per_output": len(CELLS)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(SOURCE))
    args = parser.parse_args()
    ns = source_functions(args.source)
    rows = [witness(ns, beta, eta) for beta in (1, 4) for eta in (1, 0)]
    print(json.dumps({"source_git_blob": SOURCE_BLOB, "cases": rows,
                      "fixture_status": "PASS", "native_owner_access": "NOT_DERIVED"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
