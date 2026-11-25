"""Trace a historical v16.39 caller and bind its internal reads to the emitted chart path."""
from functools import lru_cache
from hashlib import sha1, sha256
import importlib.util
from itertools import permutations, product
import json
import lzma
from pathlib import Path
import sys

import sympy as sp

SOURCE_FILES = {
    "response": ("v16.22-response-selection-closure/engine.py", "9b71ce47bbef83132f00270f8a9a19e7721864d6"),
    "p1": ("v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"),
    "atomic": ("v16.26-consistency-increment-law/engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b"),
    "builder": ("v16.39-theorem-validation/construct.py", "284b8cc9305c14f3ff6f3693c67a2c61ea00e93e"),
    "checker": ("v16.39-theorem-validation/check.py", "d4acda0e79a35b6c42ef0984ad362ba5e3bfb684"),
}


def require(test, msg):
    if not test:
        raise ValueError(msg)


def original(root):
    modules = {}
    for name, (relative, oid) in SOURCE_FILES.items():
        path = root / "ResearchHistory/UQCF-GEM/demos" / relative
        data = path.read_bytes()
        require(sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == oid, relative)
        spec = importlib.util.spec_from_file_location("original_" + name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[name] = module
    return modules


def mask(nodes):
    return sum(1 << v for v in nodes)


def members(bits):
    return tuple(i for i in range(bits.bit_length()) if bits & (1 << i))


def observed_build(builder, parents, q, start, target):
    """Observe nested calls; retain the actual returned list to test object identity."""
    filename = builder.local_path.__code__.co_filename
    assignment = []
    reads = []

    def trace(frame, event, arg):
        if frame.f_code.co_filename != filename or frame.f_code.co_name not in ("shrink", "recolor"):
            return None
        route = frame.f_back
        if route.f_code is not builder.local_path.__code__ or len(route.f_locals["initial"]) != 3:
            return None
        if event == "return" and frame.f_code.co_name == "shrink":
            current, path = arg
            assignment.append((current, list(current), len(path) - 1))
        if event == "call" and frame.f_code.co_name == "recolor":
            args = frame.f_locals
            current, i = args["current"], args["i"]
            require(current is assignment[0][0], "shrunk list replaced before live read")
            reads.append([i, current[i], args["new"]])
        return trace

    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        proof = builder.build(parents, 3, q, start, target)
    finally:
        sys.settrace(previous)
    require(len(assignment) == 2, "expected both live shrink returns")
    return proof, assignment[0][1], assignment[0][2], reads


def produce(root, out):
    mod = original(root)
    atomic = mod["atomic"].atomic
    checker = mod["checker"]

    @lru_cache(None)
    def deletion(p, masks, chart, leaf):
        before = tuple(members(m) for m in masks)
        step = atomic(p, before, chart, leaf)
        return tuple(mask(view) for view in step["after"]), (step["tau_before"], step["tau_after"])

    @lru_cache(None)
    def profile(p, masks):
        return tuple(checker.profile(p, 3, list(masks)))

    @lru_cache(None)
    def legal_continuations(p, masks):
        moves = []
        for j, bits in enumerate(masks):
            for v in members(bits):
                try:
                    deletion(p, masks, j, v)
                except ValueError:
                    continue
                moves.append([j, v])
        return moves

    @lru_cache(None)
    def reading(p, retained, grades, b):
        X = tuple(range(len(p)))
        Y = members(retained)
        projected = mod["p1"].push(p, X, Y, grades)
        P = mod["p1"].maps(p, X, Y)[0]
        query = sp.zeros(1, len(X))
        query[0, b] = 1  # b is a tip
        kernel_readable = P.col_join(query).rank() == P.rank()
        first = [2] * len(X)
        second = list(first)
        second[b] += 1
        second[p[b]] -= 1
        pair_same = mod["p1"].push(p, X, Y, first) == mod["p1"].push(p, X, Y, second)
        small = tuple(-1 if not v else Y.index(p[v]) for v in Y)
        nonroot = sp.Matrix([int(projected[i]) for i, v in enumerate(Y) if v])
        fine = sp.Matrix(grades[1:])
        common = []
        for depth_weighted in (False, True):
            local = mod["response"].candidate(small, depth_weighted) * nonroot
            full = mod["response"].candidate(p, depth_weighted) * fine
            require(all(local[i - 1] == full[v - 1] for i, v in enumerate(Y) if v), "common-address response")
            common.append(int(local[Y.index(1) - 1]))
        return dict(nodes=list(Y), p1=list(map(int, projected)), p=int(projected[Y.index(1)]),
                    b_readable=kernel_readable, positive_pair_same=pair_same, common_p=common)

    rows = []
    for anchored, zeros in product((False, True), repeat=2):
        p = (-1, 0, 1, 1, 1) + ((0,) if anchored else ())
        for order in permutations("SHR"):
            S, H, R = (order.index(key) for key in "SHR")
            for a, b, c in permutations((2, 3, 4)):
                grades = [5, 3, 0, 0, 0] + ([4] if anchored else [])
                grades[a] = grades[b] = 0 if zeros else 2
                grades[c] = 1
                fixed = mask((0, 1))
                bases = [fixed | ((1 << 5) if anchored and j == H else 0) for j in range(3)]
                start = list(bases)
                start[S] |= mask((a, b, c))
                start[H] |= 1 << a
                start[R] |= 1 << b
                for owners in product(range(3), repeat=3):
                    if len(set(owners)) != 2:
                        continue
                    target = list(bases)
                    for v, j in zip((a, b, c), owners):
                        target[j] |= 1 << v
                    for cut, other in ((a, b), (b, a)):
                        post, change = deletion(p, tuple(start), S, cut)
                        joined, free_change = deletion(p, post, S, other)
                        q = profile(p, post)
                        proof, shrunk, stop, reads = observed_build(mod["builder"], p, q, list(post), target)
                        checker.path_states(p, 3, list(q), list(post), target, proof)
                        path = proof["states"]
                        require(proof["zero_prefix"] == proof["zero_suffix"] == 0, "unexpected skeleton filling")
                        at_read = path[stop]
                        require(mod["builder"].supports(p, 3, at_read)[2:5] == shrunk, "materialized shrink state")
                        for left, right in zip(path, path[1:]):
                            j, = (j for j in range(3) if left[j] != right[j])
                            v, = members(left[j] ^ right[j])
                            larger, smaller = (left, right) if left[j] > right[j] else (right, left)
                            require(deletion(p, tuple(larger), j, v)[0] == tuple(smaller), "invalid archived move")
                        # Each recolor is first an addition then a deletion on the same original tip.
                        for n, (i, old, new) in enumerate(reads):
                            node = 2 + i
                            stage = [mod["builder"].supports(p, 3, x)[node] for x in path[stop+2*n:stop+2*n+3]]
                            require(stage == [old, old | new, new], "live read did not drive the emitted route")
                        require(len(path) == 1 + stop + 2 * len(reads), "unaccounted route state")
                        rows.append(dict(anchor=anchored, zero=zeros, chart="".join(order), abc=[a,b,c],
                            owners="".join(order[j] for j in owners), cut="a" if cut == a else "b",
                            prior=start, post=list(post), q=q, source_tau=change, free=list(joined), free_tau=free_change,
                            free_next=legal_continuations(p, joined),
                            target=target, states=path, profiles=[profile(p, tuple(x)) for x in path],
                            source_p=[reading(p, state[S], tuple(grades), b)["p"] for state in (start, post)],
                            prior_R=reading(p, start[R], tuple(grades), b), shrink_index=stop, assignment=shrunk,
                            reads=reads, live_list_verified=bool(reads),
                            first_R=reading(p, at_read[R], tuple(grades), b),
                            final_R=reading(p, target[R], tuple(grades), b)))
    data = (json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n").encode()
    out.mkdir(parents=True, exist_ok=True)
    (out / "receiver_shape_traces.json.xz").write_bytes(lzma.compress(data, preset=6))
    print(json.dumps(dict(archived_calls=len(rows), raw_sha256=sha256(data).hexdigest(), status="PASS"), sort_keys=True))


if __name__ == "__main__":
    produce(Path(sys.argv[1]), Path(sys.argv[2]))
