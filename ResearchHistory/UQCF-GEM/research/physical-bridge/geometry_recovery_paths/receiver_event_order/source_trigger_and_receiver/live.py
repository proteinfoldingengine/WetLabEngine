"""Observe a fixed original frame and supply only a verified source withdrawal."""
from collections import Counter
from itertools import groupby, permutations
import sys


def local(path, chart):
    return tuple(m for m, group in groupby(row[chart] for row in path))


def sites(mask, size):
    return [v for v in range(size) if mask & (1 << v)]


def apply_atom(lib, parents, state, actor, site):
    views = [sites(m, len(parents)) for m in state]
    cert = lib.atom.atomic(parents, views, actor, site)
    delta, trigger = lib.av.verify_atomic(cert)
    out = [sum(1 << v for v in row) for row in cert["after"]]
    assert out[actor] == state[actor] ^ (1 << site)
    return out, [delta, trigger, cert["tau_before"], cert["tau_after"]]


def fixture(lib, branches, palette):
    p = lib.p
    tree = tuple(p.B if x in ("work", "source") else p.L for x in branches)
    nodes = p.layout(tree)
    parents = [-1] + [next(j for j, kids in enumerate(nodes) if v in kids)
                     for v in range(1, len(nodes))]
    w, s, r, t = (nodes[0][branches.index(x)] for x in ("work", "source", "private", "shared"))
    by_name = {"A": [0, w, *nodes[w], s, r], "B": [0, w, *nodes[w], s, t],
               "C": [0, s, *nodes[s], t]}
    state = [sum(1 << v for v in by_name[x]) for x in palette]
    return tree, parents, s, state


def evaluate(lib, branches, palette, actors):
    p, verifier = lib.p, lib.v
    tree, parents, site, start = fixture(lib, branches, palette)
    target = [2, 1, 1]
    assert verifier.profile_check(tree, 3, start) == target
    c = palette.index("C")
    actor_ids = [palette.index(a) for a in actors]
    observed = {}

    def watch(frame, event, value):
        caller = frame.f_back
        if caller is None or caller.f_code.co_name != "child_call":
            return
        outer = caller.f_back
        if outer.f_code is not p.normalize_four.__code__ or outer.f_locals["t"] != tree:
            return
        if caller.f_locals.get("c") != site:
            return
        if event == "call" and frame.f_code is p.require_exact_parent.__code__ and not observed:
            state = frame.f_locals["state"]
            assert state is outer.f_locals["current"]
            observed.update(position=len(outer.f_locals["path"]), snapshots=[], receipts=[])
            for actor in actor_ids:
                after, fields = apply_atom(lib, parents, state, actor, site)
                assert fields == [0, False, 2, 2]
                assert verifier.profile_check(tree, 3, after) == target and after[c] == start[c]
                state[actor] = after[actor]  # Only the input event alters the running program.
                observed["snapshots"].append(after)
                observed["receipts"].append(fields)
        if event == "return" and frame.f_code is p.normalize.__code__ and "labels" not in observed:
            observed["labels"] = list(caller.f_locals["labels"])
            observed["inner_path"] = value

    previous = sys.getprofile()
    sys.setprofile(watch)
    try:
        saved = p.normalize(start, tree, 3, target)
    finally:
        sys.setprofile(previous)
    pos = observed["position"]
    # The original logger records writer steps. Interleave the independent atom receipts for verification.
    path = saved[:pos] + observed["snapshots"] + saved[pos:]
    _, _, end = verifier.model(tree, target, 3)
    verifier.path_check(tree, 3, target, path, start, end)
    assert (pos - 1) == (2 if branches.index("work") < branches.index("source") else 0)
    assert all(st[c] == start[c] for st in path[:pos + len(actors)])
    prepared = start[:]
    for actor in actor_ids:
        prepared, _ = apply_atom(lib, parents, prepared, actor, site)
    ordinary = p.normalize(prepared, tree, 3, target)
    verifier.path_check(tree, 3, target, ordinary, prepared, end)
    at = pos + len(actors) - 1
    assert path[at:] == ordinary[pos - 1:]  # Uninstrumented computation of every remaining state.
    future = local(path[at:], c)
    assert len(future) >= 2
    expected_owners = [i for i in range(3) if i not in actor_ids]
    assert observed["labels"] == expected_owners
    added = future[1] > future[0]
    assert added == (expected_owners[0] == c)
    delta = future[1] ^ future[0]
    j = delta.bit_length() - 1
    assert delta and delta == 1 << j
    assert j in (p.layout(tree)[0] if added else p.layout(tree)[site])
    grades = []
    for mask in future[:2]:
        coords = sites(mask, len(parents))
        g = lib.p1.push(tuple(parents), tuple(range(len(parents))), tuple(coords), tuple([1]*len(parents)))
        grades.append(list(zip(coords, map(int, g))))
    return {"actors": actors, "prefix_edits": pos-1, "read_labels": observed["labels"],
            "receipts": observed["receipts"], "child_steps": observed["inner_path"],
            "event_states": observed["snapshots"], "first_change": [added, j], "c_trace": future,
            "first_two_P1": grades, "path": path}


def sweep(lib):
    raw = []
    sign_counts = Counter()
    trace_counts = Counter()
    earlier_counts = Counter()
    noop_counts = Counter()
    for branches in permutations(("work", "source", "private", "shared")):
        for palette in permutations(("A", "C", "B")):
            runs = {key: evaluate(lib, branches, palette, key) for key in ("", "A", "B", "AB", "BA")}
            a, b, ab, ba = (runs[k] for k in ("A", "B", "AB", "BA"))
            pos = a["prefix_edits"]
            assert a["path"][:pos+1] == b["path"][:pos+1]
            assert ab["path"][pos+2:] == ba["path"][pos+2:]
            assert ab["c_trace"] == ba["c_trace"]
            signs = tuple(r["first_change"][0] for r in (a,b))
            rank = palette.index("C")
            assert (signs[0] != signs[1]) == (rank == 1)
            if rank == 1:
                assert (signs[0] == (palette.index("A") < rank))
            sign_counts[rank, signs[0]!=signs[1]] += 1
            trace_counts[rank, a["c_trace"]!=b["c_trace"]] += 1
            earlier_counts[pos, signs[0]!=signs[1]] += 1
            noop_counts[tuple(runs[""]["c_trace"] == r["c_trace"] for r in (a,b))] += 1
            raw.append({"order": branches, "palette": palette, "runs": runs})
    counts = lambda cnt: [list(k)+[v] for k,v in sorted(cnt.items())]
    return {"orders":len(raw),"intervention_runs":len(raw)*5,"two_edit_prefix_by_sign_difference":counts(earlier_counts),
            "first_sign_by_receiver_position":counts(sign_counts),"whole_trace_by_receiver_position":counts(trace_counts),
            "no_intervention_matches_A_and_B":counts(noop_counts)}, raw
