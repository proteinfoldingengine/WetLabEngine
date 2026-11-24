"""Independently verify the full case identities, stored paths, and geometric claims."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys

CHARTS = range(4)
LEAVES = (1, 2, 3, 4)
MASKS = range(1, 32, 2)
BASE = ((1,), (2,), (2, 3), (1, 2))


def check(value, message):
    if not value:
        raise ValueError(message)


def reject(f, message):
    try:
        f()
    except ValueError as error:
        check(str(error) == message, f"wrong rejection: {error}")
    else:
        raise ValueError(f"accepted control: {message}")


@lru_cache(maxsize=None)
def inspect_state(row):
    check(len(row) == 4 and all(type(x) is int and x in MASKS for x in row), "invalid chart")
    columns = [{j for j, m in enumerate(row) if m & (1 << v)} for v in LEAVES]
    check(all(columns), "uncovered leaf")
    height = next(n for n in range(1, 5) if any(
        all(col.intersection(team) for col in columns) for team in combinations(CHARTS, n)))
    work = sum(len(col) * (4 - len(col)) for col in columns)
    counts = [sum(j in col for col in columns) for j in CHARTS]
    return height, work, counts


@lru_cache(maxsize=None)
def endpoint(q):
    assignment = min(a for a in product(CHARTS, repeat=4) if len(set(a)) == q)
    return [1 + sum(1 << v for v, owner in zip(LEAVES, assignment) if owner == j) for j in CHARTS]


def verify_path(key, path):
    start = tuple(map(int, key.split(",")))
    check(path and tuple(path[0]) == start, "path identity")
    q = inspect_state(start)[0]
    check(path[-1] == endpoint(q), "endpoint")
    stats = [inspect_state(tuple(state)) for state in path]
    check(all(sum((x ^ y).bit_count() for x, y in zip(a, b)) == 1 for a, b in zip(path, path[1:])),
          "nonprimitive step")
    check(all(abs(h-q) <= 1 for h, _, _ in stats), "cover excursion")
    counts = [n for _, _, n in stats]
    local = [4 in c for c in zip(*counts)]
    exits = [sum(a == 4 and b == 3 for a, b in zip(c, c[1:])) for c in zip(*counts)]
    result = [q, local, [4]*4 in counts, any(w == 0 for _, w, _ in stats), exits]
    crosses = q in (1, 2)
    check(result == [q, [crosses]*4, crosses, crosses,
                     [int(crosses and m.bit_count() < 5) for m in endpoint(q)]], "passage")
    return result


def arm_key(start, c, v):
    after = list(start)
    check(bool(after[c] & (1 << v)), "source does not hold leaf")
    after[c] -= 1 << v
    inspect_state(tuple(after))
    return ",".join(map(str, after))


def unique_rows(rows, expected):
    check(len(rows) == len(expected), "population size")
    check(len({tuple(row[0]) for row in rows}) == len(rows), "duplicate preparation")
    check(dict((tuple(k), v) for k, v in rows) == expected, "identity or state")


def main(directory):
    d = Path(directory)
    raw = lzma.decompress((d/"all_chart_paths.json.xz").read_bytes())
    doc = json.loads(raw)
    cert = json.loads((d/"all_chart_certificate.json").read_bytes())
    check(sha256(raw).hexdigest() == cert["universe_sha256"], "universe digest")
    paths = doc["paths"]
    observed = {key: verify_path(key, path) for key, path in paths.items()}
    requested, expected, pairs = set(), {}, []
    for others in product(MASKS, repeat=3):
        start = (1, *others)
        if (others[0] | others[1] | others[2]) != 31:
            continue
        cols = tuple(sum(1 << j for j, m in enumerate(start) if m & (1 << v)) for v in LEAVES)
        moves = []
        for v in LEAVES:
            bit = 1 << v
            if start[2] & bit and (start[1] | start[3]) & bit:
                key = arm_key(start, 2, v)
                requested.add(key)
                moves.append([v, observed[key]])
        expected[cols] = moves
        for (u, a), (v, b) in combinations(moves, 2):
            pairs.append([list(cols), u, v, a[1] != b[1]])
    rows = doc["preparations"]
    unique_rows(rows, expected)
    check(sorted(pairs) == doc["pairs"], "pair identities")
    chart_perms, leaf_perms = list(permutations(CHARTS)), list(permutations(LEAVES))
    seen = set()
    for cm, lm, strict, flat in doc["relabelings"]:
        identity = tuple(cm), tuple(lm)
        check(identity not in seen, "duplicate relabeling")
        seen.add(identity)
        state = [1]*4
        for v, original_holders in enumerate(BASE):
            for j in original_holders:
                state[cm[j]] |= 1 << lm[v]
        keys = [arm_key(state, cm[2], lm[pos]) for pos in (2, 3)]
        check(keys == [strict, flat], "relabeled source identity")
        requested.update(keys)
        for key, flag in zip(keys, (False, True)):
            check(observed[key][1][cm[0]] == flag and observed[key][4] == [int(flag)]*4,
                  "transported blank or local deletions")
    check(seen == set(product(chart_perms, leaf_perms)), "permutation coverage")
    check(requested == set(paths), "post-cut path coverage")

    for arm in cert["witness"]:
        rows_path = paths[",".join(map(str, arm["after_source"]))]
        stats = [inspect_state(tuple(x)) for x in rows_path]
        reads = [h for h, _, _ in stats[1:]]
        check(reads == arm["live_guard_cover"] and arm["live_guard_checked_every_edit"], "guard read")
        departures = []
        for index, (before, after) in enumerate(zip(rows_path, rows_path[1:]), 1):
            for j in CHARTS:
                if before[j].bit_count() == 5 and after[j].bit_count() == 4:
                    departures.append([index, j, (before[j]^after[j]).bit_length()-1, before])
        check(departures == arm["full_chart_deletions"], "local edits")
        zero = [i for i, (_, w, _) in enumerate(stats) if w == 0]
        check(zero == arm["zero_work_indices"] == arm["simultaneous_full_indices"], "zero-work section")
        check(min(w for _, w, _ in stats) == arm["minimum_total_pair_work"], "minimum work")
        check([5-max(c) for c in zip(*(n for _,_,n in stats))] == arm["minimum_root_grades"], "P1 roots")
        check(arm["p1_calls_in_writer"] == 0, "P1 provenance")

    alt = cert["exact_cover_two_detour"]
    flat = cert["witness"][1]
    check(alt[0] == flat["after_source"] and alt[-1] == flat["end"], "alternate endpoints")
    check(all(inspect_state(tuple(s))[0] == 2 and 31 not in s for s in alt), "alternate exact cover")
    check(all(sum((x ^ y).bit_count() for x, y in zip(a,b)) == 1 for a,b in zip(alt, alt[1:])),
          "alternate move")
    check(len(alt)-1 == sum((x ^ y).bit_count() for x,y in zip(alt[0], alt[-1])), "alternate length")
    summary = dict(preparations=len(expected), arms=sum(map(len,expected.values())), pairs=len(pairs),
                   separating_pairs=sum(row[3] for row in pairs), relabelings=len(seen), unique_paths_stored=len(paths))
    check(all(cert[k] == val for k,val in summary.items()), "summary")
    check({str(q): n for q,n in Counter(m[0] for moves in expected.values() for _,m in moves).items()}
          == cert["arms_by_cover"], "arm histogram")
    check(cert["swapped_blank_end_masks"] == [1,1], "endpoint persistence")
    check(cert["same_target_control"][0] == cert["same_target_control"][1], "same-target control")

    reject(lambda: unique_rows(rows[:-1],expected), "population size")
    reject(lambda: unique_rows(rows[:-1]+rows[:1],expected), "duplicate preparation")
    reject(lambda: unique_rows([[[-1,-1,-1,-1],rows[0][1]],*rows[1:]],expected), "identity or state")
    reject(lambda: arm_key([1,19,29,9],2,2), "uncovered leaf")
    strict = cert["witness"][0]
    forced = [strict["after_source"].copy()]
    for target, adding in (([31]*4,True),(strict["end"],False)):
        for j in CHARTS:
            for v in LEAVES:
                if bool(forced[-1][j] & (1<<v)) != adding and bool(target[j] & (1<<v)) == adding:
                    state = forced[-1].copy()
                    state[j] ^= 1<<v
                    forced.append(state)
    reject(lambda: verify_path(",".join(map(str,forced[0])),forced), "cover excursion")
    reject(lambda: check(cert["swapped_blank_end_masks"][0] != cert["swapped_blank_end_masks"][1],
                         "endpoint persistence"), "endpoint persistence")
    print(json.dumps(dict(**summary, independent_controls="passed", alternate_moves=len(alt)-1)))


if __name__ == "__main__":
    main(sys.argv[1])
