"""v16.24 producer: cover-mask optimization and exact subtree reconstruction.

No scientific verdict is hard-coded. Proofs are separate from this bounded audit.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import lzma

GENESIS = 'v16.24-common-genesis'
HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def parents(raw):
    need(isinstance(raw, (list, tuple)) and len(raw) > 0, 'empty parent carrier')
    p = tuple(raw)
    need(all(type(x) is int for x in p), 'exact integer parent identifiers required')
    need(p[0] == -1, 'root identifier')
    need(all(0 <= target < len(p) for target in p[1:]), 'parent outside carrier')
    for v in range(1, len(p)):
        seen = set()
        u = v
        while u != 0:
            need(u not in seen, 'cyclic lineage')
            seen.add(u)
            u = p[u]
    return p

def retained(p, raw):
    need(isinstance(raw, (list, tuple)) and len(raw) > 0, 'empty retained view')
    y = tuple(raw)
    need(all(type(x) is int and 0 <= x < len(p) for x in y), 'retained identifier')
    need(len(set(y)) == len(y) and 0 in y, 'duplicate identity or missing root')
    need(all(v == 0 or p[v] in y for v in y), 'missing ancestor')
    return y

def validate(raw, views):
    p = parents(raw)
    need(isinstance(views, (list, tuple)) and len(views) > 0, 'empty cover')
    ys = tuple(retained(p, y) for y in views)
    need(set().union(*map(set, ys)) == set(range(len(p))), 'cover union must equal carrier')
    return p, ys

def exact(x):
    need(type(x) in (int, str) or isinstance(x, Fraction), 'inexact scalar')
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise ValueError('invalid exact scalar') from exc

def push(raw, keep, source):
    p = parents(raw)
    y = retained(p, keep)
    need(isinstance(source, (list, tuple)) and len(source) == len(p), 'source dimension')
    x = tuple(exact(a) for a in source)
    out = dict.fromkeys(y, Fraction(0))
    for v, amount in enumerate(x):
        while v not in out:
            v = p[v]
        out[v] += amount
    return tuple(out[v] for v in y)

def children(p):
    return tuple(tuple(w for w in range(1, len(p)) if p[w] == v) for v in range(len(p)))

def ancestors(p, v):
    chain = [v]
    while v:
        v = p[v]
        chain.append(v)
    return tuple(chain)

def _local(p, c, y):
    ch = children(p)
    return tuple(c[v] - sum(c[w] for w in ch[v] if w in y) for v in y)

def child_covers(p, ys):
    rows = []
    for v, ch in enumerate(children(p)):
        target = sum(1 << w for w in ch)
        dp = {0: ()}
        for i, y in enumerate(ys):
            added = sum(1 << w for w in ch if w in y)
            for old, chosen in list(dp.items()):
                new = old | added
                candidate = chosen + (i,)
                if new not in dp or (len(candidate), candidate) < (len(dp[new]), dp[new]):
                    dp[new] = candidate
        need(target in dp, 'child cover missing')
        support = dp[target]
        rows.append({'vertex': v, 'children': list(ch), 'tau': len(support), 'support': list(support)})
    return rows

def threshold(raw, views):
    p, ys = validate(raw, views)
    return max([1] + [r['tau'] for r in child_covers(p, ys)])

def subunions(ys):
    out = []
    for mask in sorted(range(1, 1 << len(ys)), key=lambda m: (m.bit_count(), m)):
        union = tuple(sorted(set().union(*(set(y) for i, y in enumerate(ys) if mask >> i & 1))))
        out.append((mask, union))
    return out

def sharp_witness(p, ys, rows, h):
    if h == 1:
        return None
    row = next(r for r in rows if r['tau'] == h)
    v, ch = row['vertex'], row['children']
    c = [0] * len(p)
    for u in ancestors(p, v):
        c[u] = len(ch) - 1
    for w in ch:
        c[w] = 1
    global_x = _local(p, c, tuple(range(len(p))))
    local = [_local(p, c, y) for y in ys]
    coefficients = [[0] * len(y) for y in ys]
    for node, sign in [(v, 1)] + [(w, -1) for w in ch]:
        i = next(i for i, y in enumerate(ys) if node in y)
        for j, u in enumerate(ys[i]):
            if node in ancestors(p, u):
                coefficients[i][j] += sign
    return {'vertex': v, 'c': c, 'global': list(global_x),
            'local': [list(x) for x in local],
            'dual': [a for block in coefficients for a in block],
            'bad_support': row['support']}

def certify(raw, views):
    p, ys = validate(raw, views)
    rows = child_covers(p, ys)
    h = max([1] + [r['tau'] for r in rows])
    unions = subunions(ys)
    samples = []
    for c in product(range(3), repeat=len(p)):
        if any(min(_local(p, c, y)) < 0 for y in ys):
            continue
        bad = next((mask for mask, y in unions if min(_local(p, c, y)) < 0), 0)
        samples.append([list(c), bad])
    return {'version': '16.24', 'genesis': GENESIS, 'parents': list(p),
            'views': [list(y) for y in ys], 'h': h, 'child_covers': rows,
            'witness': sharp_witness(p, ys, rows, h), 'samples': samples}

def shape_code(p, root=0):
    ch = children(p)
    def rec(v):
        return '(' + ''.join(sorted(rec(w) for w in ch[v])) + ')'
    return rec(root)

def shapes(bound):
    found = {}
    for n in range(1, bound + 1):
        for q in product(*(range(i) for i in range(1, n))):
            p = (-1,) + q
            found.setdefault(shape_code(p), p)
    return [(code, found[code]) for code in sorted(found, key=lambda c: (len(c), c))]

def covers(p):
    legal = []
    for mask in range(1, 1 << len(p), 2):
        y = tuple(i for i in range(len(p)) if mask >> i & 1)
        if all(v == 0 or p[v] in y for v in y):
            legal.append(y)
    for size in range(1, min(4, len(legal)) + 1):
        for ys in combinations(legal, size):
            if set().union(*map(set, ys)) == set(range(len(p))):
                yield ys

def produce(bound=5):
    need(type(bound) is int and 1 <= bound <= 5, 'test-universe bound')
    instances = []
    for code, p in shapes(bound):
        ys_list = list(covers(p))
        cases = [certify(p, ys) for ys in ys_list]
        instances.append({'code': code, 'variant': 'original', 'parents': list(p), 'cases': cases})
        perm = [0] + list(range(len(p) - 1, 0, -1))
        q = [-1] * len(p)
        for i in range(1, len(p)):
            q[perm[i]] = perm[p[i]]
        transformed = [[tuple(perm[i] for i in reversed(y)) for y in reversed(ys)] for ys in ys_list]
        instances.append({'code': code, 'variant': 'relabeled', 'parents': q,
                          'cases': [certify(q, ys) for ys in transformed]})
    return {'version': '16.24', 'genesis': GENESIS, 'tree_bound': bound,
            'view_bound': 4, 'integer_total_bound': 2, 'instances': instances}

if __name__ == '__main__':
    raw = (json.dumps(produce(), sort_keys=True, separators=(',', ':')) + '\n').encode()
    out = HERE / 'evidence'
    out.mkdir(exist_ok=True)
    (out / 'certificates.json.xz').write_bytes(lzma.compress(raw))
    record = {'execution_status': 'COMPLETED', 'raw_bytes': len(raw),
              'raw_sha256': hashlib.sha256(raw).hexdigest(),
              'scope': 'bounded producer certificate; scientific verification is separate'}
    (out / 'PRODUCTION.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))
