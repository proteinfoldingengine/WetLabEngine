"""Reconstruct the orbit from incidence roles and the writer from leaf owners.

The checker does not import a producer or any historical implementation.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
import lzma
from pathlib import Path
import sys

LABELS = range(1, 7)
CHARTS = range(4)
TEAMS = [group for n in range(1, 5) for group in combinations(CHARTS, n)]
FULL = set(LABELS)
ORIGINAL = (33, 83, 5, 57)
GRADE = {"unit": (1,)*7, "common": (1, 1, 1, 2, 1, 1, 2),
         "equal_root": (1, 1, 1, 2, 1, 1, 1),
         "matched": {1:(1, 1, 1, 4, 3, 1, 5), 3:(1, 1, 1, 5, 3, 1, 4)}}


def demand(test, msg):
    if not test:
        raise ValueError(msg)


def unpack(state):
    return [{v for v in LABELS if n & (1 << v)} for n in state]


def pack(views):
    return tuple(1 + sum(2**v for v in members) for members in views)


@lru_cache(maxsize=None)
def smallest_team(state):
    views = unpack(state)
    return next(team for team in TEAMS if set.union(*(views[j] for j in team)) == FULL)


def apply(state, command):
    j, leaf = divmod(abs(command)-1, 6)
    bit = 2**(leaf+1)
    demand(0 <= j < 4 and 1 <= leaf+1 <= 6, "command outside star")
    demand(bool(state[j] & bit) == (command < 0), "idle or wrong polarity")
    return tuple(n ^ bit if i == j else n for i, n in enumerate(state))


def remove(state, chart, leaf):
    child = apply(state, -(6*chart+leaf))
    demand(set.union(*unpack(child)) == FULL, "would destroy last copy")
    return child


def receiver_stream(seq, j):
    return tuple((1 if n > 0 else -1)*((abs(n)-1)%6+1) for n in seq if (abs(n)-1)//6 == j)


@lru_cache(maxsize=None)
def reference(start, q):
    """Choose surviving owners, then put each canonical slot in place."""
    team = smallest_team(start)
    demand(len(team) == q, "unexpected initial cover")
    views, commands, reads = unpack(start), [], []
    def change(chart, leaf, putting):
        (views[chart].add if putting else views[chart].remove)(leaf)
        commands.append((1 if putting else -1)*(6*chart+leaf))
    def move(leaf, source, target):
        if source != target:
            change(target, leaf, True)
            change(source, leaf, False)
    for leaf in LABELS:
        preferred = next(j for j in team if leaf in views[j])
        for j, members in enumerate(views):
            if j != preferred and leaf in members:
                change(j, leaf, False)
    slots = set(range(q))
    for old, new in zip(sorted(set(team)-slots), sorted(slots-set(team))):
        cargo = sorted(views[old])
        for leaf in cargo:
            change(new, leaf, True)
        for leaf in cargo:
            change(old, leaf, False)
    def owner(v):
        single, = [j for j, contents in enumerate(views) if v in contents]
        return single
    for target in range(q):
        required = target+1
        source = owner(required)
        reads.append((target, tuple(owner(v) for v in LABELS), tuple(sorted(views[2]))))
        if source != target:
            if len(views[source]) == 1:
                replacement = min(v for v in LABELS if v > required and len(views[owner(v)]) > 1)
                move(replacement, owner(replacement), source)
            move(required, source, target)
    for leaf in range(q+1, 7):
        move(leaf, owner(leaf), 0)
    return tuple(commands), tuple(reads)


def canonical(q):
    return pack([{v for v in LABELS if (v-1 if v <= q else 0) == j} for j in CHARTS])


@lru_cache(maxsize=None)
def states(start, q, seq):
    path = [start]
    for command in seq:
        path.append(apply(path[-1], command))
    demand(all(len(smallest_team(s)) == q for s in path), "wrong cover along path")
    demand(path[-1] == canonical(q), "wrong canonical endpoint")
    return tuple(path)


def format_reads(reads):
    return [dict(index=i, owners=list(o), receiver=list(r)) for i, o, r in reads]


def graded(state, grades):
    views = unpack(state)
    work = [sum(grades[v]**2 for v in views[i]^views[j]) for i, j in combinations(CHARTS, 2)]
    local = [sum(grades) - sum(grades[v] for v in views[2])]
    return dict(work=work, receiver_p1=local+[grades[v] for v in sorted(views[2])])


def test_trace(trace, seq, reads, priority):
    commands = [(1 if add else -1)*(6*j+v) for j, v, add in trace["edits"]]
    demand(tuple(commands) == seq and trace["owner_reads"] == format_reads(reads), "live instruction data")
    demand(trace["priority_calls"] == ([[3, 2, 1, 0]] if priority else []), "keeper intervention")
    demand(trace["single_internal_list"] is True and trace["independent_snapshots"] is True, "live/copy")
    demand(trace["numeric_calls"] == {"pair_work":0, "p1":0, "carrier":0}, "numeric dependency")


def working_case(doc):
    orig = ORIGINAL
    prep = remove(orig, 3, 5)
    demand(doc["original"] == list(orig) and doc["prepared"] == list(prep), "named state")
    demand(doc["archive_campaign_includes_6_4"] is False, "archive scope")
    demand([(x["actor"],x["nuisance"]) for x in doc["primary"]] ==
           [(a,b) for a in (1,3) for b in (None,0,3)], "six named comparisons")
    for row in doc["primary"]:
        actor, nuisance = row["actor"], row["nuisance"]
        source = remove(orig, actor, 4)
        successors = {(j,v) for v in LABELS for j in CHARTS if v in unpack(source)[j]
                      and sum(v in group for group in unpack(source)) > 1}
        demand(successors == {(0,5),(3,5)}, "incomplete pure continuations")
        start = source
        if nuisance is not None:
            start = remove(start, nuisance, 5)
            demand(remove(remove(orig, nuisance, 5), actor, 4) == start, "noncommuting preparatory cut")
        q = 4 if nuisance == 3 else 3
        seq, reads = reference(start, q)
        path = states(start, q, seq)
        local = receiver_stream(seq, 2)
        first = next(s for s in path if s[2] != start[2])
        demand(row["cover"] == q and tuple(row["start"]) == start and tuple(row["path"]) == seq, "named path")
        demand(tuple(row["receiver_edits"]) == local and row["receiver_first"] == sorted(unpack(first)[2])
               and row["final_receiver"] == [3], "named observable")
        demand(row["unit"] == graded(start, (1,)*7), "named unit geometry")
        demand(row["carrier"] == "degree_not_four" and len(CHARTS)-1 < 4, "carrier failure")
        test_trace(row["trace"], seq, reads, False)
    demand([(r["actor"],r["label"]) for r in doc["grade_controls"]] ==
           [(a,g) for a in (1,3) for g in ("unit","common","matched","equal_root")], "grade cases")
    for row in doc["grade_controls"]:
        actor = row["actor"]
        grades = GRADE[row["label"]]
        if row["label"] == "matched":
            grades = grades[actor]
        demand(tuple(row["grades"]) == grades, "grade substitution")
        post = remove(prep, actor, 4)
        seq, _ = reference(post, 4)
        path = states(post, 4, seq)
        first = next(s for s in path if s[2] != prep[2])
        for k, s in (("original",orig),("prepared",prep),("post",post),("first_receiver_edit",first),("end",path[-1])):
            demand(graded(s, grades) == row[k], "grade/work calculation")
        if row["label"] == "equal_root":
            source_values = []
            for state in (prep,post):
                owned = sorted(unpack(state)[actor])
                source_values.append([sum(grades)-sum(grades[v] for v in owned)]+[grades[v] for v in owned])
            demand(source_values == row["source_before_after"] and [s[0] for s in source_values] == [5,6],
                   "equal-root source transfer")
            work = row["prepared"]["work"]
            demand(work[5]-work[3] == 2*grades[1]*grades[6] and row["post"]["receiver_p1"] == [7,1],
                   "source-distance identity")
            demand(row["first_receiver_edit"]["receiver_p1"][0] == {1:5,3:6}[actor], "graded first write")
    matched = [r for r in doc["grade_controls"] if r["label"] == "matched"]
    demand(matched[0]["post"] == matched[1]["post"] and
           matched[0]["prepared"]["work"] != matched[1]["prepared"]["work"], "match only post-source geometry")
    demand([(p["actor"],p["reversed_priority"]) for p in doc["one_call"]] == [(3,False),(1,True)], "one-call arms")
    for row in doc["one_call"]:
        actor = row["actor"]
        post = remove(prep, actor, 4)
        tail, reads = reference(post, 4)
        seq = (-(6*actor+4),)+tail
        demand(tuple(row["path"]) == seq and states(prep,4,seq)[1] == post, "one-call prefix/suffix")
        test_trace(row["trace"], seq, reads, row["reversed_priority"])
        if not row["reversed_priority"]:
            demand(reference(prep,4)[0] == seq, "default source")
    demand([r["actor"] for r in doc["legal_detours"]] == [3,1], "detour arms")
    for row in doc["legal_detours"]:
        start = remove(prep, row["actor"], 4)
        seq = tuple(row["path"])
        path = states(start, 4, seq)
        prefix = (1,-7,17,-5,8,-14)
        demand(seq == prefix+reference(path[len(prefix)],4)[0] and seq[:len(prefix)] == prefix,
               "legal common-spare detour")
        demand(receiver_stream(seq, 2)[0] == 5 and tuple(row["receiver_edits"]) == receiver_stream(seq,2),
               "common alternative replacement")


def priors():
    # A shares only the second duplicated leaf, C holds one private leaf. B and D
    # share the disputed leaf. B's two private leaves form an unordered pair.
    index = {}
    for a,b,c,d in permutations(CHARTS):
        for disputed, second, c_private, d_private in permutations(LABELS,4):
            b_private = FULL-{disputed,second,c_private,d_private}
            views = [None]*4
            views[a],views[b],views[c],views[d] = {second},b_private|{disputed},{c_private},{d_private,disputed,second}
            key = pack(views)
            demand(key not in index, "duplicate independently generated prior")
            index[key] = (a,b,c,d,disputed,second)
    return index


def classify(x, y):
    if x and y and x[0] != y[0]:
        return "first_differs"
    if not x and not y:
        return "both_empty"
    if not x or not y:
        return "one_empty"
    return "identical" if x == y else "later_differs"


def check_row(row, key, roles):
    demand(row[:2] == [list(key),list(roles)] and len(row[2]) == 3, "prior identity, order or roles")
    a,b,r,d,v,w = roles
    classes = []
    for i, (remover, q) in enumerate(((None,3),(a,3),(d,4))):
        before = key if remover is None else remove(key, remover, w)
        streams = []
        pair = row[2][i]
        demand(len(pair) == 2, "paired event identity")
        for source, encoded in zip((b,d), pair):
            post = remove(before, source, v)
            seq = tuple(n-32 for n in bytes.fromhex(encoded))
            demand(reference(post, q)[0] == seq, "wrong exact native edit sequence")
            path = states(post, q, seq)
            demand(path[0][r] == key[r] and path[-1][r] == canonical(q)[r], "receiver boundary masks")
            streams.append(receiver_stream(seq,r))
        classes.append(classify(*streams))
    return classes


def identities(rows, ordered):
    demand([tuple(row[0]) for row in rows] == ordered, "missing/duplicate/substituted prior")


def reject(fn, *args):
    try:
        fn(*args)
    except (ValueError, KeyError):
        return
    raise ValueError("corruption survived")


def verify(raw, cert):
    rows = json.loads(raw)
    index = priors()
    ordered = sorted(index)
    identities(rows, ordered)
    demand(cert["schema"] == 1 and sha256(raw).hexdigest() == cert["raw_sha256"], "raw bytes/schema")
    demand((cert["priors"],cert["group_elements"],cert["paired_histories"],cert["arms"]) ==
           (len(index),2*len(index),3*len(index),6*len(index)) and len(index)==8640, "orbit accounting")
    counts = [Counter() for _ in range(3)]
    for row, key in zip(rows,ordered):
        for j, case in enumerate(check_row(row,key,index[key])):
            counts[j][case] += 1
    demand(counts == cert["counts"], "local classification counts")
    working_case(cert["named"])
    reject(identities, rows[1:], ordered)
    reject(identities, [rows[1]]+rows[1:], ordered)
    changed = json.loads(json.dumps(rows[0]))
    changed[2][0][0] = changed[2][0][0]+"21"
    reject(check_row, changed, ordered[0], index[ordered[0]])
    changed = json.loads(json.dumps(rows[0]))
    changed[1][1],changed[1][3] = changed[1][3],changed[1][1]
    reject(check_row, changed, ordered[0], index[ordered[0]])
    for kind in ("owner","endpoint","numeric","grade","scope","priority"):
        bad = json.loads(json.dumps(cert["named"]))
        if kind == "owner":
            bad["primary"][2]["trace"]["owner_reads"][2]["owners"][2] = 3
        elif kind == "endpoint":
            bad["primary"][5]["receiver_first"] = bad["primary"][5]["final_receiver"]
        elif kind == "numeric":
            bad["primary"][2]["trace"]["numeric_calls"]["pair_work"] = 1
        elif kind == "grade":
            bad["grade_controls"].pop()
        elif kind == "scope":
            bad["archive_campaign_includes_6_4"] = True
        else:
            bad["one_call"][1]["actor"] = 3
        reject(working_case, bad)
    return dict(priors=len(index), histories=cert["arms"], all_additions_deletions_replayed=True,
                named_controls_verified=True, rejected_corruptions=10, verdict="PASS")


if __name__ == "__main__":
    out = Path(sys.argv[2])
    print(json.dumps(verify(lzma.decompress((out/"receiver_spare_universe.json.xz").read_bytes()),
                            json.loads((out/"receiver_spare_certificate.json").read_bytes())), sort_keys=True))
