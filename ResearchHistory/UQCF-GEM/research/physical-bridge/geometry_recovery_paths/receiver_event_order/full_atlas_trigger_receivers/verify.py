"""Independent coordinate reconstruction, cover extensions and small transition graph."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

SHAPE = ((0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
         (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),
         (9,3),(9,8),(10,0),(10,1),(10,10))
A = (41,217,278,454)
B = (91,157,338,404)
ANCHORS = {0:2,18:80,25:135,43:113,50:70,57:29,75:105,82:62,89:19,107:97,114:54}
LINE_PAIRS = {18:(454,91),50:(217,157),82:(41,404)}


def encode(items):
    return sum(1 << x for x in items)


def indices(bits):
    while bits:
        low = bits & -bits
        yield low.bit_length()-1
        bits -= low


def catalog():
    supports = []
    for swap,sx,sy,tx,ty in product((False,True),(-1,1),(-1,1),range(11),range(11)):
        support = [((tx+sx*(y if swap else x))%11) + 11*((ty+sy*(x if swap else y))%11)
                   for x,y in SHAPE]
        supports.append(encode(support))
    return [encode(a for a,col in enumerate(supports,1) if col >> j & 1) for j in range(121)]


def dense():
    before = catalog()
    target = encode(A+B)
    rows = before.copy()
    for chart, old in enumerate(before):
        for owner, address in ANCHORS.items():
            if owner != chart:
                rows[chart] &= ~(1 << address)
        if chart in (0,5,15):
            continue
        if chart in ANCHORS:
            leaves = LINE_PAIRS.get(chart, ())
        else:
            aa = [a for a in A if a != 278 and old >> a & 1]
            bb = [a for a in B if a != 338 and old >> a & 1]
            leaves = [x for pair in zip(aa,bb) for x in pair]
        rows[chart] = (rows[chart] & ~target) | encode(leaves)
    all_leaves = (1 << 969)-2
    anchor_union = 0
    for j in ANCHORS:
        anchor_union |= rows[j]
    assert anchor_union == all_leaves
    for j,a in ANCHORS.items():
        assert [k for k,row in enumerate(rows) if row >> a & 1] == [j]
    assert all((p & q)==q for p,q in zip(before,rows))
    assert len({row.bit_count() for row in before})==1 and before[15].bit_count()==200

    @lru_cache(None)
    def others_on_line(chart):
        u = 0
        for j in ANCHORS:
            if j != chart:
                u |= rows[j]
        return u

    deficient = Counter()
    pairs = []
    available = 0
    for j,row in enumerate(rows):
        other = 0
        for k,other_row in enumerate(rows):
            if j != k:
                other |= other_row
        for a in indices(row & other):
            available += 1
            surviving = others_on_line(j) | ((row ^ (1<<a)) if j in ANCHORS else 0)
            missing = all_leaves & ~surviving
            if missing:
                # Enumerate every size-12 extension of the eleven compulsory charts.
                plus = [k for k,extra in enumerate(rows) if k not in ANCHORS and extra & missing == missing]
                assert plus
                deficient[len(plus)] += 1
                if len(plus) == 1:
                    pairs.append([j,a,plus[0]])

    digests = []
    states = []
    for arm in (A,B):
        s = rows.copy()
        signatures = []
        for addr in (None, *arm):
            if addr is not None:
                s[0] ^= 1 << addr
            W = [4*(s[i]^s[j]).bit_count() for i,j in combinations(range(121),2)]
            signatures.append(sha256(json.dumps(W,separators=(',',':')).encode()).hexdigest())
        digests.append(signatures)
        states.append(s)
    assert digests[0][-1] == digests[1][-1] and states[0][1:] == states[1][1:]
    recipes = []
    for idx,state in enumerate(states):
        receiver = (15,5)[idx]
        cover = {*ANCHORS, receiver}
        all_others = 0
        for j in cover - {receiver}:
            all_others |= state[j]
        earmarked = list(indices(state[receiver] & ~all_others))
        assert earmarked == [(278,338)[idx]]
        recipes.append([len(earmarked), state[receiver].bit_count()])
    return dict(withdrawals=sum((p^q).bit_count() for p,q in zip(before,rows)),
                available=available, positive_outcome_multiplicities=dict(sorted(deficient.items())),
                unique=sorted(pairs), signatures=digests, recipient_extremes=recipes)


@lru_cache(None)
def cover_number(columns):
    for n in range(1,5):
        for combination in combinations(range(4),n):
            candidate = encode(combination)
            if all(c & candidate for c in columns):
                return n
    raise ValueError('Uncovered leaf')


def descendants(state, fixed):
    reached = {state}
    frontier = [state]
    terminals = []
    while frontier:
        current = frontier.pop()
        successors = []
        for i,col in enumerate(current):
            if col.bit_count() <= 1:
                continue
            for j in indices(col):
                successor = current[:i]+(col ^ (1<<j),)+current[i+1:]
                if not fixed or cover_number(successor)==cover_number(current):
                    successors.append(successor)
        if not successors:
            terminals.append(current)
        for child in successors:
            if child not in reached:
                reached.add(child)
                frontier.append(child)
    return reached, terminals


def small():
    # C, T, R and S are chart bits. The first two leaves force C and T.
    common = (1,2,5,11,9,7)
    worlds = [(1,2,4,10,9,7), (1,2,5,11,8,6)]
    def matrix(s):
        return [sum(((c>>i)^(c>>j))&1 for c in s) for i,j in combinations(range(4),2)]
    assert matrix(worlds[0]) == matrix(worlds[1])
    assert cover_number(common)==2 and all(cover_number(s)==3 for s in worlds)
    levels = [descendants(s,True) for s in worlds]
    free = [descendants(s,False)[0] for s in worlds]
    assert not levels[0][0] & levels[1][0]
    joined = free[0] & free[1]
    assert joined and {cover_number(s) for s in joined}=={4}
    counts = []
    for reached, terminals in levels:
        counts.append(sorted({(sum(bool(c&4) for c in s),sum(bool(c&8) for c in s))
                              for s in terminals}))
    assert all(r>0 and s==0 for r,s in counts[0])
    assert all(s>0 and r==0 for r,s in counts[1])
    return dict(fixed_level_states=[len(x[0]) for x in levels],
                fixed_level_terminals=[len(x[1]) for x in levels], terminal_counts=counts,
                unrestricted_states=list(map(len,free)), unrestricted_common_states=len(joined))


if __name__=='__main__':
    result = json.loads(Path(__file__).with_name('results.json').read_text())
    full = dense()
    assert full['withdrawals'] == result['preparatory_withdrawals']
    assert full['available'] == sum(result['starting_menu'][key] for key in ('zero','positive'))
    assert sum(full['positive_outcome_multiplicities'].values()) == result['starting_menu']['positive']
    assert full['unique'] == result['unique_new_chart_events']
    assert full['signatures'] == [entry['pair_signatures'] for entry in result['arms']]
    print(json.dumps(dict(full=full, small=small()),sort_keys=True,indent=2))
