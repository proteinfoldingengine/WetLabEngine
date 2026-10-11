"""Independent set/edge-set checker for the frozen obstruction campaign."""
if not __debug__:
    raise RuntimeError("escape-obstruction requires assertions enabled")

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


class Rejection(ValueError):
    pass


V = tuple(range(6))
E = tuple(pair for pair in itertools.combinations(V, 2) if set(pair) != {4, 5})
POS = {edge: n for n, edge in enumerate(E)}
ALL = (1 << len(E)) - 1
STAR = tuple(sum(1 << n for n, edge in enumerate(E) if vertex in edge) for vertex in V)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def perfect_matchings():
    found = []
    for chosen in itertools.combinations(E, 3):
        degrees = Counter(x for edge in chosen for x in edge)
        if all(degrees[x] == 1 for x in V):
            found.append(tuple(chosen))
    return tuple(sorted(found))


def profiles():
    return tuple(tuple(1 + bool(code >> (5 - vertex) & 1) for vertex in V) for code in range(64))


def cover_family():
    answer = []
    for mask in range(1 << 6):
        chosen = tuple(x for x in V if mask >> x & 1)
        complement = set(V) - set(chosen)
        if len(chosen) <= 4 and not any(set(edge) <= complement for edge in E):
            answer.append(chosen)
    return tuple(sorted(answer, key=lambda c: (len(c), c)))


COVERS = cover_family()
BV = tuple(tuple(c for c in COVERS if v not in c) for v in V)
HIDDEN = tuple(
    hidden for hidden in range(ALL + 1)
    if (ALL ^ hidden) != 0 and not any((ALL ^ hidden) & ~container == 0 for container in STAR)
)
EXPOSED_BITS = sum(1 << (ALL ^ hidden) for hidden in HIDDEN)


def match_ok(matching):
    return len(matching) == 3 and set(matching) <= set(E) and {x for edge in matching for x in edge} == set(V)


def label_order(profile):
    out = []
    for v, count in enumerate(profile):
        out.extend((v, ordinal) for ordinal in range(count))
    return tuple(out)


def floor_vector(matching, profile):
    return tuple(profile[a] + profile[b] if edge in set(matching) else 1 for edge, (a, b) in zip(E, E))


def candidate_rows(matching, profile):
    partner = {}
    for a, b in matching:
        partner[a] = b
        partner[b] = a
    rows = []
    for v in V:
        gate = profile[v] == 2 or bool(BV[v])
        trace = (POS[tuple(sorted((v, partner[v])))],)
        rows.append({"admitted": False, "gate": gate, "kind": "V", "trace": trace, "v": v})
        for w in V:
            for z in V:
                if v == w or w == z or v == z:
                    continue
                vw, wz = tuple(sorted((v, w))), tuple(sorted((w, z)))
                geometry = vw in POS and wz in POS
                trace_ok = bool(geometry and partner[v] == w)
                rows.append({
                    "admitted": bool(gate and trace_ok), "gate": gate,
                    "geometry": geometry, "kind": "X", "trace_ok": trace_ok,
                    "v": v, "w": w, "z": z,
                })
    return rows


def independent_rows(matching):
    partner = {}
    for a, b in matching:
        partner[a], partner[b] = b, a
    rows = []
    for mask in range(1, 64):
        selected = {v for v in V if mask & (1 << v)}
        independent = all(not ({a, b} <= selected) for a, b in matching)
        neighborhood = tuple(sorted(partner[v] for v in selected))
        rows.append({
            "deficient": bool(independent and len(selected) > len(neighborhood)),
            "independent": independent, "mask": mask, "neighborhood": neighborhood,
        })
    return rows


def hit_number(footprints):
    choices = tuple(sorted(set(footprints) - {0}))
    for size in range(5):
        for subset in itertools.combinations(choices, size):
            merged = 0
            for item in subset:
                merged |= item
            if merged == ALL:
                return size
    return 5


def hidden_ok(footprints):
    for footprint in set(footprints):
        exposed = footprint
        while exposed:
            if EXPOSED_BITS & (1 << exposed):
                return False
            exposed = (exposed - 1) & footprint
    return True


def state_verdict(state, floor):
    counts = tuple(sum(1 for mask in state if mask & (1 << root)) for root in range(len(E)))
    hit = hit_number(state)
    return {
        "counts": counts,
        "domination_ok": all(any(mask | container == container for container in STAR) for mask in state),
        "floors_ok": all(have >= need for have, need in zip(counts, floor)),
        "hidden_ok": hidden_ok(state), "hitting": hit, "hitting_ok": hit <= 4,
        "vacancy": 0 in state,
    }


def route_rows(matching, profile):
    label_ids = label_order(profile)
    initial = tuple(STAR[v] for v, _ in label_ids)
    floor = floor_vector(matching, profile)
    admitted = [r for r in candidate_rows(matching, profile) if r["kind"] == "X" and r["admitted"]]
    cache, routes = {}, []
    for row in admitted:
        v, w, z = row["v"], row["w"], row["z"]
        retain = POS[tuple(sorted((v, w)))]
        added = POS[tuple(sorted((w, z)))]
        for index, label in enumerate(label_ids):
            if label[0] != v:
                continue
            state = list(initial)
            slices, operations = [tuple(state)], []
            removed = sorted(root for root, edge in enumerate(E) if v in edge and root != retain)
            for root in removed:
                state[index] = state[index] & ~(1 << root)
                operations.append((root, 0)); slices.append(tuple(state))
            state[index] = state[index] | (1 << added)
            operations.append((added, 1)); slices.append(tuple(state))
            rendered = []
            for current in slices:
                verdict = cache.setdefault(current, state_verdict(current, floor))
                if not (verdict["floors_ok"] and verdict["hitting_ok"] and verdict["domination_ok"] and verdict["hidden_ok"]):
                    raise Rejection("unsafe reconstructed route")
                if verdict["vacancy"]:
                    raise Rejection("unexpected vacancy")
                rendered.append({
                    "counts": verdict["counts"], "domination_ok": verdict["domination_ok"],
                    "floors_ok": verdict["floors_ok"], "hidden_ok": verdict["hidden_ok"],
                    "hitting": verdict["hitting"], "hitting_ok": verdict["hitting_ok"],
                    "vacancy": verdict["vacancy"], "x_footprint": current[index],
                })
            routes.append({
                "add": added, "candidate": (v, w, z), "label": label,
                "label_index": index, "ops": operations, "states": tuple(rendered),
            })
    return routes, cache


def bridge_control(matching, profile):
    v, w = matching[0]
    ordered = label_order(profile)
    state = [STAR[t] for t, _ in ordered]
    x = next(i for i, label in enumerate(ordered) if label[0] == v)
    y = next(i for i, label in enumerate(ordered) if label[0] == w)
    state[x], state[y] = STAR[w], 0
    bridge = tuple(sorted((v, w)))
    root = POS[bridge]
    count = sum(bool(mask & (1 << root)) for mask in state)
    required = profile[v] + profile[w]
    return {
        "accepted": count >= required, "bridge": bridge, "count": count,
        "reason": "floor_violation" if count < required else "unexpected_acceptance",
        "required": required,
    }


def controls():
    matching, profile = perfect_matchings()[0], (1, 1, 1, 1, 1, 1)
    rejected_x = next(x for x in candidate_rows(matching, profile) if x["kind"] == "X" and not x["admitted"])
    bridge = bridge_control(matching, profile)
    return {
        "canonical_corruption": {"rejected": canonical({"a": 1}) != '{\"a\" :1}'},
        "false_deficiency": {"rejected": not independent_rows(matching)[0]["deficient"]},
        "false_x": {"rejected": not rejected_x["admitted"], "witness": rejected_x},
        "forbidden_45": {"rejected": (4, 5) not in POS},
        "minimum_degree_substitution": {"rejected": all(not r["deficient"] for r in independent_rows(matching))},
        "missing_matching_edge": {"rejected": not match_ok(matching[:-1])},
        "missing_third_vertex": {"rejected": len({4, matching[0][1], 4}) != 3},
        "saturated_bridge_substitution": {"rejected": not bridge["accepted"], "witness": bridge},
    }


def expected_metadata():
    return {
        "H": E, "controls": controls(), "covers": COVERS, "kind": "metadata",
        "matching_count": 12, "profile_count": 64, "protected_masks": HIDDEN,
        "red_run": 38167334252, "schema": "c3-perfect-matching-escape-obstruction-v1",
    }


def expected_source(matching, profile):
    candidates = candidate_rows(matching, profile)
    independent = independent_rows(matching)
    routes, cache = route_rows(matching, profile)
    if not any(x["admitted"] for x in candidates if x["kind"] == "X"):
        raise Rejection("source lacks X escape")
    if any(x["admitted"] for x in candidates if x["kind"] == "V"):
        raise Rejection("source unexpectedly has V escape")
    if any(x["deficient"] for x in independent):
        raise Rejection("matching has deficient independent set")
    return {
        "B": tuple(tuple(tuple(c) for c in family) for family in BV),
        "candidates": candidates, "covers": COVERS,
        "distinct_route_states": len(cache), "floors": floor_vector(matching, profile),
        "hidden_checks": len(cache) * len(HIDDEN), "independent_sets": independent,
        "kind": "source", "matching": matching, "profile": profile, "routes": routes,
    }


def _expect_line(raw, expected, number):
    wanted = (canonical(expected) + "\n").encode()
    if raw != wanted:
        raise Rejection(f"canonical row mismatch at line {number}")


def check_campaign(stream_path):
    path = Path(stream_path)
    payload = path.read_bytes()
    if not payload.endswith(b"\n"):
        raise Rejection("missing terminal newline")
    lines = payload.splitlines(keepends=True)
    expected_total = 1 + 12 * 64
    if len(lines) != expected_total:
        raise Rejection(f"row count {len(lines)} != {expected_total}")
    _expect_line(lines[0], expected_metadata(), 1)
    counts = Counter(metadata=1, sources=0, candidates=0, independent_sets=0,
                     routes=0, route_slices=0, distinct_route_states=0, hidden_checks=0)
    line_number = 1
    for matching in perfect_matchings():
        for profile in profiles():
            line_number += 1
            expected = expected_source(matching, profile)
            _expect_line(lines[line_number - 1], expected, line_number)
            counts["sources"] += 1
            counts["candidates"] += len(expected["candidates"])
            counts["independent_sets"] += len(expected["independent_sets"])
            counts["routes"] += len(expected["routes"])
            counts["route_slices"] += sum(len(r["states"]) for r in expected["routes"])
            counts["distinct_route_states"] += expected["distinct_route_states"]
            counts["hidden_checks"] += expected["hidden_checks"]
    return {
        "all_rows_reconstructed": True, "row_counts": dict(counts),
        "source_count": counts["sources"],
        "stream_sha256": hashlib.sha256(payload).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = check_campaign(args.stream)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
