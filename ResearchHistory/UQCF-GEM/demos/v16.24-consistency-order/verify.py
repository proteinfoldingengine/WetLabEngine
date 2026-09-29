"""v16.24 independent verifier: Pruefer shapes, direct fibers and matrix inversion.

Imports neither producer nor its helpers. Bounds are verifier inputs, not producer
pass fields. All malformed, missing and mathematically false certificates fail.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import lzma
import sympy as sp

HERE = Path(__file__).resolve().parent
GENESIS = 'v16.24-common-genesis'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def exact(x):
    need(type(x) in (int, str) or isinstance(x, Fraction), 'non-exact scalar')
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise ValueError('invalid rational') from exc

def vector(raw, n):
    need(isinstance(raw, (list, tuple)) and len(raw) == n, 'vector dimension')
    return tuple(exact(v) for v in raw)

def validate(raw, rawviews):
    need(isinstance(raw, (list, tuple)) and len(raw) > 0, 'empty parent carrier')
    p = tuple(raw)
    need(all(type(a) is int for a in p), 'non-integer parent')
    need(p[0] == -1 and all(0 <= a < len(p) for a in p[1:]), 'parent endpoint')
    for node in range(1, len(p)):
        reached = set()
        while node != 0:
            need(node not in reached, 'cycle')
            reached.add(node)
            node = p[node]
    need(isinstance(rawviews, (list, tuple)) and len(rawviews) > 0, 'empty cover')
    ys = []
    for item in rawviews:
        need(isinstance(item, (list, tuple)) and len(item) > 0, 'empty view')
        y = tuple(item)
        need(all(type(a) is int and 0 <= a < len(p) for a in y), 'view identifier')
        need(0 in y and len(set(y)) == len(y), 'root/duplicate view identity')
        need(all(a == 0 or p[a] in y for a in y), 'missing ancestor')
        ys.append(y)
    need(set().union(*map(set, ys)) == set(range(len(p))), 'union/domain mismatch')
    return p, tuple(ys)

@lru_cache(None)
def chains(p):
    result = []
    for node in range(len(p)):
        line = [node]
        while node:
            node = p[node]
            line.append(node)
        result.append(tuple(line))
    return tuple(result)

@lru_cache(None)
def inverse_zeta(p):
    z = sp.Matrix([[int(v in path) for path in chains(p)] for v in range(len(p))])
    inv = z.inv()
    need(z * inv == sp.eye(len(p)), 'subtree inverse identity')
    need(all(x.q == 1 for x in inv), 'nonintegral inherited transform')
    return tuple(tuple(int(inv[i, j]) for j in range(len(p))) for i in range(len(p)))

@lru_cache(None)
def fibers(p, y):
    rows = [[0] * len(p) for _ in y]
    pos = {v: i for i, v in enumerate(y)}
    for v in range(len(p)):
        u = v
        while u not in pos:
            u = p[u]
        rows[pos[u]][v] = 1
    need(all(sum(row[j] for row in rows) == 1 for j in range(len(p))), 'fiber partition')
    return tuple(map(tuple, rows))

def mv(rows, x):
    return tuple(sum(a * b for a, b in zip(row, x)) for row in rows)

@lru_cache(None)
def local_rows(p, y):
    inv = inverse_zeta(p)
    return tuple(tuple(sum(a * inv[k][j] for k, a in enumerate(row)) for j in range(len(p)))
                 for row in fibers(p, y))

def subsets(ys):
    result = []
    for size in range(1, len(ys) + 1):
        for ids in combinations(range(len(ys)), size):
            mask = sum(1 << i for i in ids)
            nodes = tuple(sorted(set().union(*(set(ys[i]) for i in ids))))
            result.append((mask, nodes))
    return sorted(result, key=lambda r: (r[0].bit_count(), r[0]))

def check_section(P, I, fine_relabel, coarse_relabel):
    need(P * I == sp.eye(P.rows), 'invalid section')
    need(fine_relabel * I == I * coarse_relabel, 'retained naturality failure')

def check_dual(rawparents, rawviews, rawlocal, rawdual, vertex):
    p, ys = validate(rawparents, rawviews)
    need(type(vertex) is int and 0 <= vertex < len(p), 'dual vertex')
    need(isinstance(rawlocal, (list, tuple)) and len(rawlocal) == len(ys), 'local family dimension')
    local = [vector(row, len(y)) for row, y in zip(rawlocal, ys)]
    need(all(a >= 0 for row in local for a in row), 'negative local witness')
    A = sp.Matrix([row for y in ys for row in fibers(p, y)])
    lam = sp.Matrix(vector(rawdual, A.rows))
    target = A.T * lam
    need(target[vertex] > 0 and all(target[i] == 0 for i in range(len(p)) if i != vertex), 'false separating functional')
    b = sp.Matrix([a for row in local for a in row])
    need((lam.T * b)[0] < 0, 'no strict separation')
    # Non-permutation computational coordinates, with cone and dual pulled along.
    C = sp.eye(A.cols)
    if A.cols > 1:
        C[0, 1] = 1
    D = sp.eye(A.rows)
    D[0, 0] = 2
    Ap = D * A * C
    lp = D.T.inv() * lam
    need(Ap.T * lp == C.T * target, 'dual basis covariance')
    need((lp.T * D * b)[0] == (lam.T * b)[0], 'pairing basis covariance')
    return True

def _verify_case(d):
    required = {'version', 'genesis', 'parents', 'views', 'h', 'child_covers', 'witness', 'samples'}
    need(isinstance(d, dict) and required <= d.keys(), 'missing required field')
    need(d['version'] == '16.24' and d['genesis'] == GENESIS, 'version/origin mismatch')
    p, ys = validate(d['parents'], d['views'])
    n = len(p)
    ch = [tuple(w for w in range(1, n) if p[w] == v) for v in range(n)]
    sub = subsets(ys)
    actual_tau = []
    need(isinstance(d['child_covers'], list) and len(d['child_covers']) == n, 'incomplete child ledger')
    for v, row in enumerate(d['child_covers']):
        need(isinstance(row, dict) and {'vertex', 'children', 'tau', 'support'} <= row.keys(), 'incomplete child record')
        need(type(row['vertex']) is int and row['vertex'] == v, 'child vertex identity')
        need(isinstance(row['children'], list) and all(type(w) is int for w in row['children']), 'child identity type')
        need(tuple(row['children']) == ch[v], 'wrong child incidence')
        tau = 0 if not ch[v] else min(mask.bit_count() for mask, u in sub if set(ch[v]) <= set(u))
        need(type(row['tau']) is int and row['tau'] == tau, 'false child cover optimum')
        ids = row['support']
        need(isinstance(ids, list) and all(type(i) is int and 0 <= i < len(ys) for i in ids), 'cover support identity')
        need(len(set(ids)) == len(ids) == tau, 'false minimum-cover size')
        selected = set().union(*(set(ys[i]) for i in ids)) if ids else set()
        need(set(ch[v]) <= selected, 'false child-cover support')
        actual_tau.append(tau)
    h = max([1] + actual_tau)
    need(type(d['h']) is int and d['h'] == h, 'false consistency order')
    need(h <= max([1] + [len(row) for row in ch]), 'branch bound')
    Arows = tuple(row for y in ys for row in fibers(p, y))
    A = sp.Matrix(Arows)
    # Reconstruct a left inverse from raw marginals via subtree evaluations.
    Crows = []
    offsets = [sum(len(y) for y in ys[:i]) for i in range(len(ys))]
    for v in range(n):
        i = next(i for i, y in enumerate(ys) if v in y)
        row = [0] * len(Arows)
        for j, node in enumerate(ys[i]):
            row[offsets[i] + j] = int(v in chains(p)[node])
        Crows.append(row)
    left = sp.Matrix(inverse_zeta(p)) * sp.Matrix(Crows)
    need(left * A == sp.eye(n), 'unique reconstruction left inverse')
    # Every raw local compatible input generated by the frozen complete grid.
    got = {}
    need(isinstance(d['samples'], list), 'sample list')
    for row in d['samples']:
        need(isinstance(row, list) and len(row) == 2, 'sample schema')
        c, bad = row
        need(isinstance(c, list) and len(c) == n and all(type(a) is int and 0 <= a <= 2 for a in c), 'sample input type')
        need(type(bad) is int and 0 <= bad < (1 << len(ys)), 'sample failure mask')
        need(tuple(c) not in got, 'duplicated sample')
        got[tuple(c)] = bad
    expected = set()
    order_hist = Counter()
    for c in product(range(3), repeat=n):
        if any(min(mv(local_rows(p, y), c)) < 0 for y in ys):
            continue
        expected.add(c)
        need(c in got, 'missing compatible sample')
        failed = {mask for mask, y in sub if min(mv(local_rows(p, y), c)) < 0}
        bad = got[c]
        if not failed:
            need(bad == 0, 'false infeasibility')
            order_hist[0] += 1
        else:
            first_order = min(mask.bit_count() for mask in failed)
            need(bad in failed and bad.bit_count() == first_order, 'false sample feasibility/order')
            need(first_order <= h, 'sufficiency contradicted by actual source')
            order_hist[first_order] += 1
    need(set(got) == expected, 'extra or invalid sample')
    if h == 1:
        need(d['witness'] is None, 'spurious sharp witness')
    else:
        w = d['witness']
        need(isinstance(w, dict) and {'vertex', 'c', 'global', 'local', 'dual', 'bad_support'} <= w.keys(), 'missing sharp witness')
        vertex = w['vertex']
        need(type(vertex) is int and 0 <= vertex < n and actual_tau[vertex] == h, 'wrong critical vertex')
        c = vector(w['c'], n)
        x = vector(w['global'], n)
        need(x == mv(inverse_zeta(p), c), 'false signed global reconstruction')
        need(x[vertex] < 0, 'witness does not refute nonnegative gluing')
        need(isinstance(w['local'], list) and len(w['local']) == len(ys), 'witness local coverage')
        local = [vector(row, len(y)) for row, y in zip(w['local'], ys)]
        need(all(row == mv(fibers(p, y), x) for row, y in zip(local, ys)), 'false local marginal')
        need(all(a >= 0 for row in local for a in row), 'inadmissible local witness')
        failed = [mask for mask, u in sub if min(mv(fibers(p, u), x)) < 0]
        need(failed and min(mask.bit_count() for mask in failed) == h, 'witness fails sharpness')
        support = w['bad_support']
        need(isinstance(support, list) and all(type(i) is int and 0 <= i < len(ys) for i in support), 'bad witness support')
        need(len(set(support)) == len(support) == h, 'bad support size')
        need(sum(1 << i for i in support) in failed, 'support is not an obstruction')
        check_dual(p, ys, w['local'], w['dual'], vertex)
    return {'h': h, 'samples': len(expected), 'sample_orders': {str(k): order_hist[k] for k in sorted(order_hist)},
            'sharp_witnesses': int(h > 1), 'subfamilies': len(sub), 'vertices': n}

def verify_case(d):
    try:
        return _verify_case(d)
    except (KeyError, IndexError, TypeError, ZeroDivisionError) as exc:
        raise ValueError('malformed certificate: ' + str(exc)) from exc

def code_for(p):
    def walk(v):
        return '(' + ''.join(sorted(walk(w) for w in range(1, len(p)) if p[w] == v)) + ')'
    return walk(0)

@lru_cache(None)
def independent_shapes(bound):
    found = set()
    for n in range(1, bound + 1):
        if n == 1:
            found.add('()')
            continue
        for seq in product(range(n), repeat=n - 2):
            degree = [1 + seq.count(v) for v in range(n)]
            adjacency = [set() for _ in range(n)]
            for a in seq:
                leaf = next(i for i, d in enumerate(degree) if d == 1)
                adjacency[a].add(leaf); adjacency[leaf].add(a)
                degree[a] -= 1; degree[leaf] -= 1
            a, b = [i for i, d in enumerate(degree) if d == 1]
            adjacency[a].add(b); adjacency[b].add(a)
            p = [-2] * n; p[0] = -1; stack = [0]
            while stack:
                v = stack.pop()
                for w in adjacency[v]:
                    if p[w] == -2:
                        p[w] = v; stack.append(w)
            found.add(code_for(tuple(p)))
    return frozenset(found)

def cover_key(ys):
    return tuple(sorted(tuple(sorted(y)) for y in ys))

def expected_covers(p):
    legal = []
    for flags in product((0, 1), repeat=len(p) - 1):
        y = (0,) + tuple(i + 1 for i, flag in enumerate(flags) if flag)
        if all(p[v] in y for v in y if v):
            legal.append(y)
    found = set()
    for count in range(1, min(4, len(legal)) + 1):
        for ys in combinations(legal, count):
            if set().union(*map(set, ys)) == set(range(len(p))):
                found.add(cover_key(ys))
    return found

def verify_document(doc, bound=5):
    need(isinstance(doc, dict) and {'version','genesis','tree_bound','view_bound','integer_total_bound','instances'} <= doc.keys(), 'document schema')
    need(doc['version'] == '16.24' and doc['genesis'] == GENESIS, 'document origin/version')
    for key, value in [('tree_bound',bound),('view_bound',4),('integer_total_bound',2)]:
        need(type(doc[key]) is int and doc[key] == value, 'changed declared bound')
    need(isinstance(doc['instances'], list), 'missing instances')
    lookup = {}
    for inst in doc['instances']:
        need(isinstance(inst, dict) and {'code','variant','parents','cases'} <= inst.keys(), 'instance schema')
        key = (inst['code'], inst['variant'])
        need(key not in lookup, 'duplicate instance')
        need(inst['variant'] in ('original','relabeled') and isinstance(inst['cases'], list), 'variant/schema')
        p, _ = validate(inst['parents'], [list(range(len(inst['parents'])))])
        need(code_for(p) == inst['code'], 'wrong rooted shape identity')
        lookup[key] = inst
    shapes = independent_shapes(bound)
    need(set(lookup) == {(c, variant) for c in shapes for variant in ('original','relabeled')}, 'incomplete shape coverage')
    summary = {}
    counts = Counter()
    for code in sorted(shapes):
        old = lookup[(code,'original')]; new = lookup[(code,'relabeled')]
        p = tuple(old['parents']); n = len(p)
        need(all(0 <= p[i] < i for i in range(1,n)), 'original enumeration is not ancestor-first')
        perm = [0] + list(range(n-1,0,-1)); q = [-1] * n
        for i in range(1,n): q[perm[i]] = perm[p[i]]
        need(new['parents'] == q, 'false declared relabeling')
        original_cases = {}
        per_variant = []
        for inst in (old,new):
            expected = expected_covers(tuple(inst['parents']))
            actual = set(); metrics = Counter(); hist = Counter()
            for case in inst['cases']:
                need(case.get('parents') == inst['parents'], 'foreign carrier')
                key = cover_key(case.get('views', []))
                need(key not in actual and key in expected, 'duplicate or undeclared cover')
                actual.add(key)
                if inst['variant'] == 'original':
                    original_cases[key] = case
                else:
                    inverse_key = cover_key([[perm[v] for v in y] for y in case['views']])
                    need(inverse_key in original_cases, 'missing metamorphic source')
                    source = original_cases[inverse_key]
                    transformed = [[perm[v] for v in reversed(y)] for y in reversed(source['views'])]
                    need(case['views'] == transformed, 'false view/storage transform')
                result = verify_case(case)
                metrics.update({'covers':1,'samples':result['samples'],'sharp_witnesses':result['sharp_witnesses'],'subfamilies':result['subfamilies']})
                hist[result['h']] += 1
                for k, number in result['sample_orders'].items():metrics['sample_order_'+k] += number
            need(actual == expected, 'missing cover')
            entry = dict(metrics); entry['order_histogram'] = {str(k):hist[k] for k in sorted(hist)}
            summary[code+'|'+inst['variant']] = entry
            per_variant.append(entry)
            if inst['variant'] == 'original':counts.update(metrics)
        need(per_variant[0] == per_variant[1], 'metamorphic result mismatch')
    need(counts['covers'] > 0 and len(summary) == 2*len(shapes), 'no complete checks')
    return {'version':'16.24','execution_status':'COMPLETED','input_validity':'VALID',
            'proof_status':'bounded independently reconstructed certificates; general arguments H0-H6 in TYPE_AND_PROOF.md',
            'scope':'formal nonnegative rational retained sources; no physical-law inference',
            'shapes':len(shapes),'covers':counts['covers'],'original':dict(counts),
            'by_instance':summary,'metamorphic_copies':counts['covers'],
            'scientific_verdict':'SHARP_COVER_CONSISTENCY_ORDER_CERTIFIED_ON_DECLARED_UNIVERSE'}

if __name__ == '__main__':
    raw = lzma.decompress((HERE/'evidence/certificates.json.xz').read_bytes())
    result = verify_document(json.loads(raw))
    result['raw_sha256'] = hashlib.sha256(raw).hexdigest()
    (HERE/'evidence/VERIFICATION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'by_instance'},sort_keys=True))
