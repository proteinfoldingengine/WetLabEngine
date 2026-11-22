"""Replay the pinned P1 carrier and Package 17 curvature routines on one slice."""

import hashlib
import importlib.util
from itertools import combinations
import json
import math
from pathlib import Path
import sys

import numpy as np


SOURCES = {
    "lineage.py": (
        Path("ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py"),
        "e95e3e978779164dd91f09b80e3389247e6320c2",
    ),
    "spatial_graph_curvature_verifier.py": (
        Path("Tmp/TOE/package17_bundle/spatial_graph_curvature_verifier.py"),
        "c8043250f0a61077faabbc029ef7e248905f3f32",
    ),
}
P = (7,)
A = (0,)
U = (7, 1)
V = (8, 3)
EPSILON = 1e-12
TOLERANCE = 1e-11


def pinned_module(name, out):
    path, expected = SOURCES[name]
    contents = path.read_bytes()
    blob = hashlib.sha1(f"blob {len(contents)}\0".encode() + contents).hexdigest()
    assert blob == expected
    (out / name).write_bytes(contents)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    metadata = {"path": str(path), "blob": blob, "sha256": hashlib.sha256(contents).hexdigest()}
    return module, metadata


def carriers(lineage):
    siblings = [(i,) for i in range(18)]
    leaves = [parent + (j,) for parent in siblings[7:] for j in range({P: 2, (8,): 4}.get(parent, 3))]
    fine = lineage.Carrier("package17-structural-control", ((), *siblings, *leaves))
    local = lineage.Carrier(fine.genesis, tuple(key for key in fine.keys if key != U))
    remote = lineage.Carrier(fine.genesis, tuple(key for key in fine.keys if key != V))
    return fine, lineage.Pruning(fine, local), lineage.Pruning(fine, remote)


def incidence(carrier):
    keys = sorted(carrier.keys, key=lambda key: (len(key), key))
    position = {key: i for i, key in enumerate(keys)}
    edges = np.zeros((len(keys), len(keys)), dtype=bool)
    for key in keys[1:]:
        edges[position[key[:-1]], position[key]] = True
    return keys, edges


def check(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=0, atol=TOLERANCE)


def rounded(value):
    return np.asarray(value).round(12).tolist()


def compare_with_closed_form(keys, slice_keys, weights, values, archive_edges, k):
    assert slice_keys == [(i,) for i in range(18)]
    assert k == 7
    ancestry_sizes = {key: sum(len(leaf) == 2 and leaf[:-1] == key for leaf in keys) for key in slice_keys}
    expected = np.zeros_like(weights)
    edge_ids, edge_values = [], []
    for i, j in combinations(range(len(slice_keys)), 2):
        if i >= k:
            continue
        ni = math.sqrt(1 + ancestry_sizes[slice_keys[i]]) + EPSILON
        nj = math.sqrt(1 + ancestry_sizes[slice_keys[j]]) + EPSILON
        weight = 1 / (ni * nj)
        expected[i, j] = expected[j, i] = weight
        degrees_j = 17 if j < k else k
        edge_ids.append((i, j))
        edge_values.append((4 - 17 - degrees_j) * weight)
    np.testing.assert_array_equal(weights > 0, expected > 0)
    check(weights, expected)
    np.testing.assert_array_equal(archive_edges, edge_ids)
    check(values, edge_values)


def read_geometry(archive, keys, edges):
    closure = archive.transitive_closure_bool(edges)
    expected_prefix = np.array([[len(a) < len(b) and b[:len(a)] == a for b in keys] for a in keys])
    np.testing.assert_array_equal(closure, expected_prefix)
    depth = archive.longest_depths(closure)
    np.testing.assert_array_equal(depth, [len(key) for key in keys])
    slices = dict(archive.rank_slices(depth, min_size=max(18, len(keys) // 35)))
    sl = slices[1]
    slice_keys = [keys[i] for i in sl]
    k = archive.SpatialCurvConfig().k_profile_neighbors
    weights = archive.profile_weighted_adjacency(closure, sl, k)
    values, edge_count = archive.forman_curvature(weights)
    archive_edges = np.argwhere(np.triu(weights > 0, k=1))
    assert edge_count == len(archive_edges) == 98
    compare_with_closed_form(keys, slice_keys, weights, values, archive_edges, k)
    overlap = archive.ollivier_overlap_proxy(weights)
    scalar = float(np.mean(overlap) + np.mean(values) / (edge_count + EPSILON))
    return slice_keys, weights, archive_edges, values, overlap, scalar


def check_grade_control(fine, pruning):
    first = [2] * len(fine.keys)
    second = first.copy()
    second[fine.keys.index(U)] += 1
    second[fine.keys.index(V)] -= 1
    retained = [pruning.aggregate(prior) for prior in (first, second)]
    prior_owner = [prior[fine.keys.index(P)] for prior in (first, second)]
    owner = [int(grades[pruning.coarse.keys.index(P)]) for grades in retained]
    assert all(min(prior) > 0 for prior in (first, second))
    assert sum(first) == sum(second) and prior_owner == [2, 2] and owner == [4, 5]
    assert sum(retained[0]) == sum(retained[1]) == sum(first)
    return {"pre_owner_grade": prior_owner, "post_owner_grade": owner, "totals": [sum(first), sum(second)]}


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    lineage, lineage_identity = pinned_module("lineage.py", out)
    archive, geometry_identity = pinned_module("spatial_graph_curvature_verifier.py", out)
    fine, local, remote = carriers(lineage)
    assert local.ancestor(U) == P and remote.ancestor(V) == (8,)
    trees = {"fine": fine, "local": local.coarse, "remote": remote.coarse}
    reads = {name: read_geometry(archive, *incidence(tree)) for name, tree in trees.items()}
    slice_keys, w_before, edge_ids, f_before, o_before, s_before = reads["fine"]
    i_p = slice_keys.index(P)
    i_a = slice_keys.index(A)
    held_edge = np.flatnonzero(np.all(edge_ids == (i_a, i_p), axis=1)).item()
    p_edges = np.any(edge_ids == i_p, axis=1)
    assert np.count_nonzero(p_edges) == 7

    table = {}
    edge_table = {}
    for name, (ids, w, edges, f, o, scalar) in reads.items():
        assert ids == slice_keys
        np.testing.assert_array_equal(edges, edge_ids)
        np.testing.assert_array_equal(o, o_before)
        count = 1 if name == "local" else 2
        expected_weight = 1 / ((1 + EPSILON) * (math.sqrt(1 + count) + EPSILON))
        check([w[i_a, i_p], f[held_edge]], [expected_weight, -20 * expected_weight])
        table[name] = {"carrier_size": len(trees[name].keys), "held_edge_weight": rounded(w[i_a, i_p]),
                       "held_edge_forman_proxy": rounded(f[held_edge]), "scalar_slice_proxy": rounded(scalar),
                       "changed_edge_proxy_count": int(np.count_nonzero(np.abs(f - f_before) > TOLERANCE))}
        edge_table[name] = [{"endpoints": [slice_keys[i], slice_keys[j]], "weight": rounded(w[i, j]),
                             "forman_proxy": rounded(f[index]), "overlap_proxy": rounded(o[index])}
                            for index, (i, j) in enumerate(edges)]
    _, w_after, _, f_after, _, s_after = reads["local"]
    np.testing.assert_array_equal(np.abs(f_after - f_before) > TOLERANCE, p_edges)
    check(reads["remote"][3][held_edge], f_before[held_edge])
    difference = w_after[i_a, i_p] - w_before[i_a, i_p]
    assert difference > 0.12
    check(s_after - s_before, (-20 * 7 * difference) / (98 * (98 + EPSILON)))

    keys, edges = incidence(fine)
    sink_mask = edges.copy()
    sink_mask[keys.index(U), :] = False
    np.testing.assert_array_equal(sink_mask, edges)
    mask_read = read_geometry(archive, keys, sink_mask)
    np.testing.assert_array_equal(mask_read[3], f_before)

    grade_control = check_grade_control(fine, local)
    grade_pair_reads = [read_geometry(archive, *incidence(local.coarse)) for _ in (0, 1)]
    for first, second in zip(grade_pair_reads[0][1:], grade_pair_reads[1][1:], strict=True):
        np.testing.assert_array_equal(first, second)
    grade_control["all_geometry_equal"] = True

    (out / "edges.json").write_text(json.dumps(edge_table, allow_nan=False, sort_keys=True) + "\n")
    return {"sources": [lineage_identity, geometry_identity], "held_edge": [A, P], "slice": slice_keys,
            "edge_count": len(edge_ids), "local_target": U, "remote_target": V, "values": table,
            "sink_mask_comparison_equal": True, "grade_control": grade_control}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
