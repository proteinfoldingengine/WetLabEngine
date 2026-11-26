"""Find primitive paths for the first edit of a privately split binary subtree."""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import permutations, product
import json
import lzma
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "endogenous_junction"))
from historical import History, move, toggle


START = (409, 681, 79)
CHAMBER = (159, 681, 457)
AFTER = (31, 681, 457)
FINAL = (31, 425, 713)
TARGET = (2, 3, 2)
X, Y, W, S, LEFT, RIGHT = 1, 2, 3, 7, 8, 9
ROLES = (0, 1, 2)
BINARY = (LEFT, RIGHT)
MUTABLE = (X, Y, S, LEFT, RIGHT)


def allowed(profile, mode):
    dr, dw, ds = (abs(a - b) for a, b in zip(profile, TARGET))
    if mode == "exact":
        return (dr, dw, ds) == (0, 0, 0)
    if mode == "root_only":
        return dr <= 1 and dw == ds == 0
    if mode == "binary_only":
        return ds <= 1 and dw == dr == 0
    if mode == "unit_band":
        return dr + dw + ds <= 1
    raise ValueError(mode)


def held(state, site):
    return {j for j, mask in enumerate(state) if mask & (1 << site)}


def enumerate_slice(lib, tree):
    """Independently enumerate all atlas states extending the fixed ternary leaf assignment."""
    base = [mask & sum(1 << t for t in (0, W, 4, 5, 6)) for mask in AFTER]
    all_states = {}
    for mx, my, ms, left, right in product(range(1, 8), repeat=5):
        if left & ~ms or right & ~ms:
            continue
        state = list(base)
        for site, group in zip(MUTABLE, (mx, my, ms, left, right)):
            for j in ROLES:
                if group & (1 << j):
                    state[j] |= 1 << site
        state = tuple(state)
        all_states[state] = lib.profile(tree, state)
    return all_states


def build_graph(states):
    graph = {}
    for state in states:
        graph[state] = sorted(nxt for j in ROLES for site in MUTABLE
                              if (nxt := toggle(state, j, site)) in states)
    return graph


def search(graph, start, freeze_leaves=False):
    distance, ways, witness = {start: 0}, {start: 1}, {start: None}
    pending = deque([start])
    while pending:
        state = pending.popleft()
        for nxt in graph[state]:
            if freeze_leaves and move(state, nxt)[1] in BINARY:
                continue
            steps = distance[state] + 1
            if nxt not in distance:
                distance[nxt], ways[nxt], witness[nxt] = steps, 0, state
                pending.append(nxt)
            if steps == distance[nxt]:
                ways[nxt] += ways[state]
    return distance, ways, witness


def trace(witness, end):
    path = []
    while end is not None:
        path.append(end)
        end = witness[end]
    return path[::-1]


def certify(lib, tree, path, mode):
    for state in path:
        assert allowed(lib.profile(tree, state), mode)
    for a, b in zip(path, path[1:]):
        j, site, sign = move(a, b)
        high, low = (b, a) if sign > 0 else (a, b)
        assert lib.verify_cut(tree, high, j, site)[0] == low


def first_edits(lib, tree, graph, mode):
    distance, ways, witness = search(graph, AFTER, freeze_leaves=True)
    best, rows = {}, []
    for state in sorted(distance):
        for nxt in graph[state]:
            j, site, sign = move(state, nxt)
            if site not in BINARY:
                continue
            assert sign == 1
            prior, following = lib.profile(tree, state), lib.profile(tree, nxt)
            assert prior[2] == 2
            assert (following[2] == 2) == (j == 0)
            if mode == "exact":
                assert j == 0 and not all(state[0] & (1 << v) for v in (X, Y))
                assert state[0] & (1 << S)
            rows.append([state, nxt, [j, site], distance[state] + 1, ways[state]])
            key = j, site
            cost = distance[state] + 1
            if key not in best or cost < best[key][0]:
                best[key] = [cost, 0, trace(witness, state) + [nxt]]
            if cost == best[key][0]:
                best[key][1] += ways[state]
    report = []
    witnesses = []
    for (j, site), (minimum, count, path) in sorted(best.items()):
        certify(lib, tree, path, mode)
        report.append(dict(chart=j, site=site, distance=minimum, shortest_paths=count))
        witnesses.append(path)
    return dict(prior_states=len(distance), first_edge_count=len(rows), types=report), rows, witnesses


def geodesic(lib, tree, start, end, mode):
    """Dynamic programming on the Hamming interval. Each shortest candidate flips only net bits."""
    bits = [(j, v) for j in ROLES for v in range(1, 10) if (start[j] ^ end[j]) & (1 << v)]
    ways, parents = {start: 1}, {start: None}
    layers = [{start}]
    arcs = []
    for depth in range(len(bits)):
        next_layer = set()
        for state in sorted(layers[depth]):
            for j, site in bits:
                if not ((state[j] ^ end[j]) & (1 << site)):
                    continue
                nxt = toggle(state, j, site)
                try:
                    profile = lib.profile(tree, nxt)
                except lib.v.InterfaceNotPreserved:
                    continue
                if not allowed(profile, mode):
                    continue
                ways[nxt] = ways.get(nxt, 0) + ways[state]
                parents.setdefault(nxt, state)
                next_layer.add(nxt)
                arcs.append([state, nxt])
        layers.append(next_layer)
    assert ways.get(end, 0) > 0
    path = trace(parents, end)
    certify(lib, tree, path, mode)
    assert lib.v.path_check(tree, 3, list(TARGET), list(map(list, path)), list(start), list(end)) <= 1
    # Count only vertices which actually lie on complete shortest paths.
    live = {end}
    for a, b in reversed(arcs):
        if b in live:
            live.add(a)
    return dict(distance=len(bits), shortest_paths=ways[end], geodesic_states=len(live),
                passes_through_chamber=CHAMBER in live, passes_through_after=AFTER in live,
                witness=path), [edge for edge in arcs if edge[1] in live]


def relabel_checks(lib, tree, paths):
    count = 0
    orbit = set()
    for charts, singletons, ternary, binary in product(permutations(ROLES), permutations((X, Y)),
                                                        permutations((4, 5, 6)), permutations(BINARY)):
        nodes = (0, *singletons, W, *ternary, S, *binary)
        def relabel(state):
            out = [0] * 3
            for j, mask in enumerate(state):
                out[charts[j]] = sum(1 << nodes[v] for v in range(10) if mask & (1 << v))
            return tuple(out)
        orbit.add(relabel(AFTER))
        for path in paths:
            renamed = list(map(relabel, path))
            certify(lib, tree, renamed, "exact")
            for a, b in zip(renamed, renamed[1:]):
                j, site, sign = move(a, b)
                if site in BINARY:
                    assert j == charts[0] and sign == 1
                    break
            else:
                raise AssertionError("missing first leaf edit")
        count += 1
    return count, orbit


def preparation_family(lib, tree, orbit):
    previous = Path(__file__).resolve().parent.parent / "endogenous_junction/raw.json.xz"
    presentations = json.loads(lzma.decompress(previous.read_bytes()))["extension"]["presentations"]
    actual = {tuple(row[4]) for row in presentations if row[5][0] == 2}
    assert actual == orbit and START in orbit
    counts, rows = Counter(), []
    for state in sorted(actual):
        outsider, = set(ROLES) - held(state, S)
        assert held(state, X) == held(state, Y) == {outsider}
        path = lib.normalize(tree, TARGET, state)
        index = next((n for n in range(1, len(path)) if move(path[n-1], path[n])[1] in BINARY), None)
        if index is None:
            counts["no binary leaf edit"] += 1
            rows.append(dict(start=state, outsider=outsider, first=None))
            continue
        prior, after = path[index-1:index+1]
        j, site, sign = move(prior, after)
        old_q, new_q = lib.profile(tree, prior), lib.profile(tree, after)
        assert sign == 1 and old_q[2] == 2 and (j == outsider) == (new_q[2] == 2)
        label = "outsider copies" if j == outsider else "existing holder copies the other leaf"
        counts[label] += 1
        prefix_exact = all(lib.profile(tree, p) == TARGET for p in path[:index+1])
        rows.append(dict(start=state, outsider=outsider, step=index, first=[j,site,sign],
                         profile_before=old_q, profile_after=new_q, exact_prefix=prefix_exact,
                         still_holds_copied_leaf_at_return=bool(path[-1][j] & (1 << site))))
    return dict(indexed=len(actual), named=sum(row[5][0] == 2 for row in presentations),
                by_first_event=dict(sorted(counts.items())),
                exact_through_first=sum(row.get("exact_prefix",False) for row in rows),
                first_copy_absent_at_return=sum(row.get("still_holds_copied_leaf_at_return") is False for row in rows),
                example=next(row for row in rows if tuple(row["start"])==START)), rows


def experiment(checkout):
    lib = History(checkout)
    tree = (lib.p.L, lib.p.L, lib.p.T, lib.p.B)
    assert lib.p.layout(tree) == [[X,Y,W,S],[],[],[4,5,6],[],[],[],list(BINARY),[],[]]
    native = lib.normalize(tree, TARGET, START)
    assert lib.endpoint(tree, 3, TARGET) == FINAL == native[-1]
    cut = native.index(CHAMBER)
    assert native[cut + 1] == AFTER and native[cut + 2] == (31, 937, 457)
    assert not [a for a in lib.moves(tree, AFTER) if a[2] == -1]
    states = enumerate_slice(lib, tree)
    reports, raw = {}, {}
    for mode in ("exact", "root_only", "binary_only"):
        graph = build_graph({z for z, q in states.items() if allowed(q, mode)})
        distance, ways, witness = search(graph, AFTER)
        component = sorted(distance)
        route = trace(witness, FINAL)
        certify(lib, tree, route, mode)
        lib.check_path(tree, TARGET, route)
        first, rows, first_paths = first_edits(lib, tree, graph, mode)
        # Every admitted neighbor in this component has been considered. Historical
        # v16.26 checks the edges and also considers moves outside the five-site slice.
        if mode == "exact":
            for state in component:
                historical = {n for n in lib.moves(tree, state).values() if lib.profile(tree, n) == TARGET}
                assert historical == set(graph[state])
            assert all(not (z[0] & (1 << S)) for z in component if held(z,X)==held(z,Y)=={0})
            automorphisms, orbit = relabel_checks(lib, tree, [*first_paths, route])
        # Independent shortest-length check using the two directed distance maps.
        from_end, suffix_ways, _ = search(graph, FINAL)
        assert suffix_ways[AFTER] == ways[FINAL]
        shortest_states = {z for z in component if distance[z] + from_end[z] == distance[FINAL]}
        reports[mode] = dict(states_in_slice=len(graph), reachable_states=len(component),
                             edges=sum(len(graph[z]) for z in component)//2,
                             exchange_distance=distance[FINAL], shortest_exchanges=ways[FINAL],
                             exchange_geodesic_states=len(shortest_states), first=first,
                             exchange_witness=route, first_witnesses=first_paths)
        raw[mode] = dict(component=[[z, graph[z]] for z in component], first_edges=rows,
                         shortest_exchange_layers=[sorted(z for z in shortest_states if distance[z]==d)
                                                   for d in range(distance[FINAL]+1)])
    # A four-cycle keeps the exact profile, stays active and never changes either binary leaf.
    cycle = [AFTER]
    for j, site in ((1,X), (2,Y), (1,X), (2,Y)):
        cycle.append(toggle(cycle[-1], j, site))
    assert cycle[-1] == AFTER and len(set(cycle[:-1])) == 4
    certify(lib, tree, cycle, "exact")
    assert all(held(z,t)==held(AFTER,t) for z in cycle for t in BINARY)
    refs = {}
    for name,start,mode in (("original_exact", START, "exact"), ("original_band", START, "unit_band"),
                            ("after_band", AFTER, "unit_band")):
        refs[name], raw[name] = geodesic(lib, tree, start, FINAL, mode)
    assert not refs["original_exact"]["passes_through_chamber"]
    assert not refs["original_band"]["passes_through_chamber"]
    assert not refs["original_exact"]["passes_through_after"]
    family, raw["original_preparation_family"] = preparation_family(lib, tree, orbit)
    activity = {"exact_cycle":cycle,"original_unmodified_path":native,"parent_cut_step":cut+1,
                "original_binary_first_move":move(native[cut+1],native[cut+2]),
                "original_binary_first_profile":lib.profile(tree,native[cut+2])}
    raw["controls"] = activity
    raw_bytes = (json.dumps(raw, sort_keys=True, separators=(",",":")) + "\n").encode()
    return dict(target=TARGET, roles=["D","B","C"], start=START, chamber=CHAMBER, after=AFTER, final=FINAL,
                modes=reports, geodesics=refs, controls=activity, original_preparations=family,
                exact_witness_relabelings=automorphisms,
                raw_sha256=sha256(raw_bytes).hexdigest()), raw_bytes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_checkout", type=Path)
    parser.add_argument("--raw", type=Path)
    args = parser.parse_args()
    result, raw_bytes = experiment(args.historical_checkout.resolve())
    if args.raw:
        args.raw.write_bytes(raw_bytes)
    print(json.dumps(result, sort_keys=True, indent=2))
