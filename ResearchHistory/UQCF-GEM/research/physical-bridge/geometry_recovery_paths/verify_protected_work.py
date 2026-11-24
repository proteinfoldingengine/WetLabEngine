"""Independently derive the entire pure-pruning universe by coordinate submasks and assignments."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys

LABELS = (0, 1, 2, 3)
PAIRS = tuple(combinations(LABELS, 2))
ARCHIVE = Path("ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/evidence/science/scientific/CERTIFICATE.json.gz")
HISTORIC = "f2de35e7f7fea13621c332cae71dbdc69da63cf8dd806827601fa90b07145a25"


def check(value, reason):
    if not value:
        raise ValueError(reason)


def pack(row):
    k = 0
    for value in reversed(row):
        k = 32*k + value
    return k


def remove(row, j, v):
    return tuple(x - (1 << (v-1)) if i == j else x for i, x in enumerate(row))


@lru_cache(None)
def subsets(mask):
    return [x for x in range(mask+1) if x & mask == x]


def union(row):
    return row[0] | row[1] | row[2] | row[3]


@lru_cache(None)
def interval(row):
    full = union(row)
    return tuple(s for s in product(*(subsets(x) for x in row)) if union(s) == full)


@lru_cache(None)
def terminal(row):
    count = union(row).bit_length()
    holders = [tuple(j for j in LABELS if row[j] & (1 << i)) for i in range(count)]
    result = []
    for owners in product(*holders):
        state = tuple(sum(1 << i for i, owner in enumerate(owners) if owner == j) for j in LABELS)
        result.append(state)
    return tuple(result)


@lru_cache(None)
def work(row):
    return tuple((row[i] ^ row[j]).bit_count() for i, j in PAIRS)


def minimum(row):
    teams = []
    for group_bits in range(1, 16):
        team = [j for j in LABELS if group_bits & (1 << j)]
        mass = 0
        for j in team:
            mass |= row[j]
        if mass == union(row):
            teams.append(team)
    least = min(map(len, teams))
    return sorted(t for t in teams if len(t) == least)


def cc_by_separating_cuts(row, v, j):
    # Intersect every chart-side cut containing j that no other leaf crosses.
    support = [sum(1 << k for k in LABELS if row[k] & (1 << i))
               for i in range(4) if i != v-1]
    group = 15
    for side in range(1, 16):
        if side & (1 << j) and all((s & side) in (0, s) for s in support):
            group &= side
    return [k for k in LABELS if group & (1 << k)]


def fork(row, v, owners):
    a, b = owners
    posts = [remove(row, j, v) for j in owners]
    components = [cc_by_separating_cuts(row, v, j) for j in owners]
    shared = []
    for family in (interval, terminal):
        possibilities = [{work(x) for x in family(p)} for p in posts]
        shared.append(sorted(map(list, possibilities[0] & possibilities[1])))
    disjoint = not bool(shared[1])
    check(disjoint == (not shared[0]) == (b not in components[0]), "geometric classification")
    # In a star the other leaves can follow the same labeled history. This
    # supplementary check pairs the complete intervals without comparing clocks.
    bit = 1 << (v-1)
    def switch_owner(state):
        return tuple(mask ^ bit if k in owners else mask for k, mask in enumerate(state))
    matched = {switch_owner(state) for state in interval(posts[0])}
    check(matched == set(interval(posts[1])), "owner switch did not transport the interval")
    expected_shift = tuple(int(b in pair)-int(a in pair) for pair in PAIRS)
    for state in interval(posts[0]):
        moved = switch_owner(state)
        shift = tuple(x-y for x,y in zip(work(state),work(moved)))
        check(shift == expected_shift, "matched geometric shift")
    for passive in set(LABELS) - set(owners):
        check({t[passive] for t in terminal(posts[0])} == {t[passive] for t in terminal(posts[1])},
              "third chart terminals")
    isolated = [j for j, c in zip(owners, components) if c == [j]]
    return dict(start=pack(row), leaf=v, owners=list(owners), post=list(map(pack, posts)),
                components=components, isolated=isolated, disconnected=disjoint,
                common_work=shared[0], common_terminal_work=shared[1])


def build():
    rows = sorted(((0,a,b,c) for a,b,c in product(range(16), repeat=3) if a|b|c == 15), key=pack)
    all_rows = set(rows)
    states, forks = [], []
    totals = Counter()
    for row in rows:
        events = [(j, v) for j in LABELS for v in range(1,5)
                  if row[j] & (1 << (v-1)) and remove(row, j, v) in all_rows]
        pairs = []
        for (j, u), (k, v) in combinations(events, 2):
            after_both = remove(remove(row, j, u), k, v)
            join = pack(after_both) if after_both in all_rows else None
            pairs.append([j, u, k, v, join])
            if join is None:
                check(u == v and j != k, "incorrect conflict")
                forks.append(fork(row, u, (j, k)))
        states.append(dict(start=pack(row), masks=list(row), moves=[[j,v,pack(remove(row,j,v))] for j,v in events],
                           pairs=pairs, reachable=sorted(map(pack, interval(row))), terminals=sorted(map(pack, terminal(row))),
                           work=list(work(row)), metric=len(set(row)) == 4))
        totals["directed_moves"] += len(events)
        totals["event_pairs"] += len(pairs)
    forks.sort(key=lambda x:(x["start"],x["leaf"]))
    bridges = sum(x["disconnected"] for x in forks)
    predicted = 4*3*(2*4**3-3**3)
    check(bridges == predicted and len(forks) == 12*7**3, "analytic census")
    totals.update(preparations=len(rows), conflicts=len(forks), disconnected=bridges,
                  connected=len(forks)-bridges, commuting=totals["event_pairs"]-len(forks))
    return dict(states=states, forks=forks), dict(totals)


def compare(actual, expected):
    for section, key in (("states", lambda x:x["start"]), ("forks", lambda x:(x["start"],x["leaf"]))):
        seen = [key(x) for x in actual[section]]
        check(len(seen) == len(expected[section]), "case count")
        check(len(set(seen)) == len(seen), "duplicate case")
        check(seen == [key(x) for x in expected[section]], "case identity")
        check(actual[section] == expected[section], "false numerical or state record")


def check_named(given, row):
    leaves = union(row).bit_length()
    expected = dict(prior=list(row), prior_work=list(work(row)), prior_covers=minimum(row), disputed=4,
                    receiver=2, partner=1, pair_index=PAIRS.index((1,2)), arms=[])
    for who in (1,3):
        post = remove(row,who,4)
        start_h, end_h = len(minimum(row)[0]), len(minimum(post)[0])
        initial_root = 1 + leaves-row[who].bit_count()
        ends = set(terminal(post))
        records = [dict(masks=list(r), terminal=r in ends, work=list(work(r)), metric=len(set(r)) == 4,
                        h=len(minimum(r)[0]), receiver_p1=[1+leaves-r[2].bit_count()]+[1]*r[2].bit_count())
                   for r in sorted(interval(post))]
        expected["arms"].append(dict(actor=who, post=list(post), atom=[start_h,end_h,end_h-start_h,end_h>start_h],
                                     source_root=[initial_root,initial_root+1], covers=minimum(post), states=records))
    check(given == expected, "named witness")
    return expected


def rejecting(target, reason):
    try:
        target()
    except ValueError as error:
        check(str(error) == reason, "different rejection reason")
        return
    raise ValueError("accepted a corrupted case: " + reason)


def main(history, out):
    raw = lzma.decompress((out/"protected_work_universe.json.xz").read_bytes())
    primary = json.loads(raw)
    cert = json.loads((out/"protected_work_certificate.json").read_bytes())
    expected, counts = build()
    compare(primary, expected)
    check(sha256(raw).hexdigest() == cert["raw_universe_sha256"] and cert["domain"] == counts, "certificate census")
    triangle = (0,10,7,12)
    common = remove(triangle,1,2)
    check(cert["common_cut"] == [1,2], "preparation operation")
    old = check_named(cert["triangle"], triangle)
    opened = check_named(cert["opened"], common)
    for name, start, levels in (("five_leaf",(16,9,2,28),(2,3)), ("six_leaf_equal_source",(16,41,2,28),(3,4))):
        n = check_named(cert[name], start)
        for arm, value in zip(n["arms"],levels):
            check(all(s["work"][n["pair_index"]] == value and s["metric"] for s in arm["states"]), "persistent pair")
            check({s["h"] for s in arm["states"]} == {3,4}, "cover-changing control")
            check(arm["covers"] == n["prior_covers"] == [[1,2,3]] and arm["atom"] == [3,3,0,False],
                  "source cover identity")
        if name == "six_leaf_equal_source":
            check(all(a["source_root"] == [4,5] for a in n["arms"]) and work(start)[3] == work(start)[5] == 4,
                  "matched source roots and distances")
            check({tuple(s["receiver_p1"]) for a in n["arms"] for s in a["states"]} == {(6,1)},
                  "no third-chart acquisition")

    source_a, source_b = remove(triangle,2,2), remove(triangle,2,3)
    joined = remove(source_a,2,3)
    controls = {}
    for label, a, b in (("left",triangle,source_a),("right",triangle,source_b),("second",source_a,joined),
                        ("inverse",source_a,triangle)):
        flat = len(minimum(a)[0]) == len(minimum(b)[0])
        kinds = "flat" if flat else "strict"
        controls[label] = dict(before=list(a), after=list(b), refinement=kinds if b in interval(a) else "rejected",
                               v1633_accepts_as_invisible=flat)
    check(cert["legacy"] == controls, "historical caller controls")
    f = (history/ARCHIVE).read_bytes()
    check(sha256(f).hexdigest() == cert["archive_sha256"] == HISTORIC, "archive provenance")
    entry, = (x for x in json.loads(gzip.decompress(f))["entries"] if x["k"] == x["m"] == 4)
    original = {tuple(v >> 1 for v in y):i for i,y in enumerate(entry["graph"]["states"])}
    named_states = {tuple(n["prior"]) for n in (old,opened)}
    named_states.update(tuple(s["masks"]) for n in (old,opened) for a in n["arms"] for s in a["states"])
    check({str(pack(s)):original[s] for s in named_states} == cert["archived_four_leaf_rows"]
          and original[triangle] == 1349, "original row identities")

    rows = primary["states"]
    rejecting(lambda:compare(dict(primary,states=rows[:-1]),expected),"case count")
    rejecting(lambda:compare(dict(primary,states=[rows[1],*rows[1:]]),expected),"duplicate case")
    rejecting(lambda:compare(dict(primary,states=[dict(rows[0],start=-1),*rows[1:]]),expected),"case identity")
    for change in ("false work","reverse addition","erased last holder"):
        altered = deepcopy(rows[0])
        if change == "false work":
            altered["work"][0] += 1
        else:
            altered["moves"].append([0,1,-1] if change == "reverse addition" else [1,1,0])
        rejecting(lambda:compare(dict(primary,states=[altered,*rows[1:]]),expected),"false numerical or state record")
    collision = next(i for i,x in enumerate(primary["forks"]) if x["common_terminal_work"])
    wrong = list(primary["forks"])
    wrong[collision] = dict(wrong[collision],common_terminal_work=[])
    rejecting(lambda:compare(dict(primary,forks=wrong),expected),"false numerical or state record")
    bad = deepcopy(cert["six_leaf_equal_source"])
    bad["arms"][0]["states"][0]["receiver_p1"][0] += 1
    rejecting(lambda:check_named(bad,(16,41,2,28)),"named witness")
    print(json.dumps(dict(**counts, controls="passed", equal_source_work=[3,4]), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]))
