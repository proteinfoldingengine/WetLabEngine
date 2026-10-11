"""Exact producer for the frozen perfect-matching escape obstruction."""
if not __debug__:
    raise RuntimeError("escape-obstruction requires assertions enabled")

import argparse
import hashlib
import itertools as it
import json
from collections import Counter
from pathlib import Path

VERTICES = tuple(range(6))
H_EDGES = tuple(e for e in it.combinations(VERTICES, 2) if e != (4, 5))
EDGE_INDEX = {e: i for i, e in enumerate(H_EDGES)}
FULL = (1 << len(H_EDGES)) - 1
STARS = tuple(sum(1 << i for i, e in enumerate(H_EDGES) if v in e) for v in VERTICES)
RED_RUN = 38167334252


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def perfect_matchings():
    def rec(left):
        if not left:
            yield ()
            return
        u = left[0]
        for v in left[1:]:
            edge = tuple(sorted((u, v)))
            if edge not in EDGE_INDEX:
                continue
            rest = tuple(x for x in left if x not in (u, v))
            for tail in rec(rest):
                yield tuple(sorted((edge,) + tail))
    return tuple(sorted(set(rec(VERTICES))))


def multiplicity_profiles():
    return tuple(it.product((1, 2), repeat=6))


def covers_at_most_four():
    return tuple(
        C for n in range(5) for C in it.combinations(VERTICES, n)
        if all(u in C or v in C for u, v in H_EDGES)
    )


COVERS = covers_at_most_four()
B = tuple(tuple(C for C in COVERS if v not in C) for v in VERTICES)
PROTECTED_MASKS = tuple(
    h for h in range(FULL + 1)
    if (FULL ^ h) and all((FULL ^ h) & ~star for star in STARS)
)
PROTECTED_EXPOSED_BITS = sum(1 << (FULL ^ h) for h in PROTECTED_MASKS)


def validate_matching(matching):
    edges = tuple(tuple(e) for e in matching)
    if len(edges) != 3 or any(e not in EDGE_INDEX for e in edges):
        return False
    return sorted(x for e in edges for x in e) == list(VERTICES)


def labels(profile):
    return tuple((v, j) for v, count in enumerate(profile) for j in range(count))


def floors(matching, profile):
    saturated = set(matching)
    return tuple(profile[u] + profile[v] if e in saturated else 1 for e, (u, v) in zip(H_EDGES, H_EDGES))


def classify_candidates(matching, profile):
    assert validate_matching(matching)
    saturated = set(matching)
    result = []
    for v in VERTICES:
        gate = profile[v] >= 2 or bool(B[v])
        trace = tuple(i for i, e in enumerate(H_EDGES) if v in e and e in saturated)
        result.append({"admitted": False, "gate": gate, "kind": "V", "trace": trace, "v": v})
        for w in VERTICES:
            for z in VERTICES:
                if len({v, w, z}) != 3:
                    continue
                vw = tuple(sorted((v, w)))
                wz = tuple(sorted((w, z)))
                geometry = vw in EDGE_INDEX and wz in EDGE_INDEX
                trace_ok = geometry and set(trace) <= {EDGE_INDEX[vw]}
                admitted = bool(gate and trace_ok)
                result.append({
                    "admitted": admitted, "gate": gate, "geometry": geometry,
                    "kind": "X", "trace_ok": trace_ok, "v": v, "w": w, "z": z,
                })
    return result


def independent_set_rows(matching):
    partner = {u: v for u, v in matching}
    partner.update({v: u for u, v in matching})
    rows = []
    for mask in range(1, 1 << 6):
        I = tuple(v for v in VERTICES if mask >> v & 1)
        independent = not any(u in I and v in I for u, v in matching)
        N = tuple(sorted({partner[v] for v in I}))
        rows.append({
            "deficient": bool(independent and len(I) > len(N)),
            "independent": independent, "mask": mask, "neighborhood": N,
        })
    return rows


def minimum_hitting(footprints):
    active = tuple(sorted(set(m for m in footprints if m)))
    for n in range(5):
        for choice in it.combinations(active, n):
            union = 0
            for mask in choice:
                union |= mask
            if union == FULL:
                return n
    return 5


def hidden_safe(footprints):
    for footprint in set(footprints):
        sub = footprint
        while sub:
            if PROTECTED_EXPOSED_BITS >> sub & 1:
                return False
            sub = (sub - 1) & footprint
    return True


def evaluate_state(state, floor_vector):
    counts = tuple(sum(bool(mask >> r & 1) for mask in state) for r in range(len(H_EDGES)))
    hitting = minimum_hitting(state)
    return {
        "counts": counts,
        "domination_ok": all(any(mask & ~star == 0 for star in STARS) for mask in state),
        "floors_ok": all(c >= f for c, f in zip(counts, floor_vector)),
        "hidden_ok": hidden_safe(state),
        "hitting": hitting,
        "hitting_ok": hitting <= 4,
        "vacancy": any(mask == 0 for mask in state),
    }


def _route_records(matching, profile):
    labs = labels(profile)
    source = tuple(STARS[v] for v, _ in labs)
    floor_vector = floors(matching, profile)
    admitted = [r for r in classify_candidates(matching, profile) if r["kind"] == "X" and r["admitted"]]
    cache = {}
    records = []
    for candidate in admitted:
        v, w, z = candidate["v"], candidate["w"], candidate["z"]
        keep = EDGE_INDEX[tuple(sorted((v, w)))]
        add = EDGE_INDEX[tuple(sorted((w, z)))]
        for label_index, label in enumerate(labs):
            if label[0] != v:
                continue
            state = list(source)
            states = [tuple(state)]
            ops = []
            for r in range(len(H_EDGES)):
                if STARS[v] >> r & 1 and r != keep:
                    state[label_index] &= ~(1 << r)
                    ops.append((r, 0))
                    states.append(tuple(state))
            state[label_index] |= 1 << add
            ops.append((add, 1))
            states.append(tuple(state))
            checks = []
            for s in states:
                if s not in cache:
                    cache[s] = evaluate_state(s, floor_vector)
                ev = cache[s]
                assert ev["floors_ok"] and ev["hitting_ok"] and ev["domination_ok"] and ev["hidden_ok"]
                assert not ev["vacancy"]
                checks.append(ev)
            assert all(not (s[label_index] & ~STARS[v]) for s in states[:-1])
            assert states[-1][label_index] & ~STARS[v]
            records.append({
                "add": add, "candidate": (v, w, z), "label": label,
                "label_index": label_index, "ops": ops,
                "states": tuple({
                    "counts": ev["counts"], "domination_ok": ev["domination_ok"],
                    "floors_ok": ev["floors_ok"], "hidden_ok": ev["hidden_ok"],
                    "hitting": ev["hitting"], "hitting_ok": ev["hitting_ok"],
                    "vacancy": ev["vacancy"], "x_footprint": s[label_index],
                } for s, ev in zip(states, checks)),
            })
    return records, cache


def iter_admitted_routes(matching, profile):
    records, _ = _route_records(matching, profile)
    for record in records:
        yield record["states"]


def saturated_bridge_substitution_control(matching, profile):
    assert validate_matching(matching)
    v, w = matching[0]
    labs = labels(profile)
    source = [STARS[t] for t, _ in labs]
    x = next(i for i, label in enumerate(labs) if label[0] == v)
    y = next(i for i, label in enumerate(labs) if label[0] == w)
    source[x] = STARS[w]
    source[y] = 0
    edge = tuple(sorted((v, w)))
    r = EDGE_INDEX[edge]
    count = sum(bool(mask >> r & 1) for mask in source)
    required = profile[v] + profile[w]
    return {
        "accepted": count >= required, "bridge": edge, "count": count,
        "reason": "floor_violation" if count < required else "unexpected_acceptance",
        "required": required,
    }


def run_rejecting_controls():
    matching = perfect_matchings()[0]
    profile = (1, 1, 1, 1, 1, 1)
    false_x = next(r for r in classify_candidates(matching, profile) if r["kind"] == "X" and not r["admitted"])
    bridge = saturated_bridge_substitution_control(matching, profile)
    return {
        "canonical_corruption": {"rejected": canonical({"a": 1}) != '{\"a\" :1}'},
        "false_deficiency": {"rejected": not independent_set_rows(matching)[0]["deficient"]},
        "false_x": {"rejected": not false_x["admitted"], "witness": false_x},
        "forbidden_45": {"rejected": (4, 5) not in EDGE_INDEX},
        "minimum_degree_substitution": {"rejected": all(not r["deficient"] for r in independent_set_rows(matching))},
        "missing_matching_edge": {"rejected": not validate_matching(matching[:-1])},
        "missing_third_vertex": {"rejected": len({4, matching[0][1], 4}) != 3},
        "saturated_bridge_substitution": {"rejected": not bridge["accepted"], "witness": bridge},
    }


def source_record(matching, profile):
    candidates = classify_candidates(matching, profile)
    independents = independent_set_rows(matching)
    routes, state_cache = _route_records(matching, profile)
    assert any(r["admitted"] for r in candidates if r["kind"] == "X")
    assert not any(r["admitted"] for r in candidates if r["kind"] == "V")
    assert not any(r["deficient"] for r in independents)
    return {
        "B": tuple(tuple(tuple(C) for C in family) for family in B),
        "candidates": candidates, "covers": COVERS,
        "distinct_route_states": len(state_cache), "floors": floors(matching, profile),
        "hidden_checks": len(state_cache) * len(PROTECTED_MASKS),
        "independent_sets": independents, "kind": "source",
        "matching": matching, "profile": profile, "routes": routes,
    }


def metadata():
    return {
        "H": H_EDGES, "controls": run_rejecting_controls(), "covers": COVERS,
        "kind": "metadata", "matching_count": len(perfect_matchings()),
        "profile_count": len(multiplicity_profiles()),
        "protected_masks": PROTECTED_MASKS, "red_run": RED_RUN,
        "schema": "c3-perfect-matching-escape-obstruction-v1",
    }


def write_campaign(stream_path, certificate_path):
    stream_path, certificate_path = Path(stream_path), Path(certificate_path)
    digest = hashlib.sha256()
    counts = Counter(metadata=1, sources=0, candidates=0, independent_sets=0,
                     routes=0, route_slices=0, distinct_route_states=0, hidden_checks=0)
    with stream_path.open("wb") as handle:
        first = (canonical(metadata()) + "\n").encode()
        handle.write(first); digest.update(first)
        for matching in perfect_matchings():
            for profile in multiplicity_profiles():
                record = source_record(matching, profile)
                line = (canonical(record) + "\n").encode()
                handle.write(line); digest.update(line)
                counts["sources"] += 1
                counts["candidates"] += len(record["candidates"])
                counts["independent_sets"] += len(record["independent_sets"])
                counts["routes"] += len(record["routes"])
                counts["route_slices"] += sum(len(r["states"]) for r in record["routes"])
                counts["distinct_route_states"] += record["distinct_route_states"]
                counts["hidden_checks"] += record["hidden_checks"]
    result = {
        "all_sources_escape": True, "all_sources_no_deficiency": True,
        "controls": run_rejecting_controls(), "red_run": RED_RUN,
        "row_counts": dict(counts), "source_count": counts["sources"],
        "stream_sha256": digest.hexdigest(),
    }
    certificate_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", required=True)
    parser.add_argument("--certificate", required=True)
    args = parser.parse_args()
    print(json.dumps(write_campaign(args.stream, args.certificate), sort_keys=True))
