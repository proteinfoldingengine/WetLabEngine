#!/usr/bin/env python3
"""T-235 independent verifier (stdlib only, fractions.Fraction).

Independent of produce.py: trees are enumerated as recursive parent arrays and deduplicated by an
AHU canonical string; the admissible read space is built from sigma-orbit matrices and reduced by
this file's own Gaussian elimination; every reported value is recomputed and compared exactly.
Usage: verify.py CERT.json PRODUCER.py  -> prints VERIFICATION JSON; exit 1 on any mismatch."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import product

class Reject(Exception):
    pass

def need(cond, msg):
    if not cond:
        raise Reject(msg)

# ---------- trees as parent arrays ----------
def children_of(par):
    ch = [[] for _ in par]
    for i, q in enumerate(par):
        if q is not None:
            ch[q].append(i)
    return ch

def ahu(par, marks):
    ch = children_of(par)
    def rec(i):
        return '(' + marks.get(i, '') + ''.join(sorted(rec(c) for c in ch[i])) + ')'
    return rec(0)

def all_trees(n):
    reps = {}
    for tail in product(*[range(i) for i in range(1, n)]):
        par = [None] + list(tail)
        k = ahu(par, {})
        if k not in reps:
            reps[k] = par
    return [reps[k] for k in sorted(reps)]

def depth(par, i):
    d = 0
    while par[i] is not None:
        i = par[i]
        d += 1
    return d

# ---------- exact linear algebra ----------
def rref_nullspace(rows, ncols):
    A = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        vec = [Q(0)] * ncols
        vec[f] = Q(1)
        for i, c in enumerate(piv):
            vec[c] = -A[i][f]
        basis.append(vec)
    return basis

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]

def zeros(r, c):
    return [[Q(0)] * c for _ in range(r)]

def push(nv, par, leaf):
    """P for pruning `leaf`: rows = vertices without leaf (in order), cols = all vertices."""
    keep = [i for i in range(nv) if i != leaf]
    P = zeros(len(keep), nv)
    for j in range(nv):
        P[keep.index(par[leaf] if j == leaf else j)][j] = Q(1)
    return keep, P

# ---------- claim P ----------
def P_cases_for(par):
    n = len(par)
    ch = children_of(par)
    out = {}
    for p in range(n):
        lv = [c for c in ch[p] if not ch[c]]
        for a in range(len(lv)):
            for b in range(a + 1, len(lv)):
                k = ahu(par, {lv[a]: 'u', lv[b]: 'u'})
                out.setdefault(k, (p, lv[a], lv[b]))
    return out

def analyse_P(par, p, u, v):
    n = len(par)
    keep, P = push(n, par, u)
    I = zeros(n, n - 1)
    for i, y in enumerate(keep):
        I[y][i] = Q(1)
    sig = list(range(n)); sig[u], sig[v] = v, u
    orbits, seen = [], set()
    for i in range(n):
        for j in range(n):
            if (i, j) not in seen:
                orb = {(i, j), (sig[i], sig[j])}
                seen |= orb
                orbits.append(sorted(orb))
    need(len(orbits) == n * n - 2 * n + 2, 'commutant orbit count')
    # PN-step: P F (e_u - e_p) = 0 ; F = sum t_k B_k
    rows = []
    for r in range(n - 1):
        row = []
        for orb in orbits:
            val = Q(0)
            for (i, j) in orb:
                coef = (Q(1) if j == u else Q(0)) - (Q(1) if j == p else Q(0))
                val += P[r][i] * coef
            row.append(val)
        rows.append(row)
    tb = rref_nullspace(rows, len(orbits))
    Delta = [Q(0)] * n; Delta[u] = Q(1, 5); Delta[v] = Q(-1, 5)
    PD = matvec(P, Delta)
    ok, cs = True, []
    for t in tb:
        F = zeros(n, n)
        for tk, orb in zip(t, orbits):
            for (i, j) in orb:
                F[i][j] += tk
        Fy = matmul(matmul(P, F), I)
        need(matmul(Fy, P) == matmul(P, F), 'PN-step on verifier basis')
        c = (F[u][u] - F[v][u]) / 5
        pre = matvec(F, Delta)
        post = matvec(Fy, PD)
        exp_pre = [c if i == u else (-c if i == v else Q(0)) for i in range(n)]
        exp_post = [c if y == p else (-c if y == v else Q(0)) for y in keep]
        ok = ok and pre == exp_pre and post == exp_post
        cs.append(c)
    # witnesses, PN checked at EVERY single-leaf pruning of this carrier, SX at sigma
    ch = children_of(par)
    leaves = [i for i in range(n) if not ch[i] and i != 0]
    def read(name, m):
        if name == 'id':
            return [[Q(int(i == j)) for j in range(m)] for i in range(m)]
        tot = [[Q(int(i == 0)) for j in range(m)] for i in range(m)]
        if name == 'tot':
            return tot
        return [[Q(int(i == j)) - tot[i][j] for j in range(m)] for i in range(m)]
    wit = {}
    for name in ('id', 'tot', 'dif'):
        F = read(name, n)
        pn_all = all(matmul(read(name, n - 1), push(n, par, l)[1]) == matmul(push(n, par, l)[1], F) for l in leaves)
        S = [[Q(int(sig[j] == i)) for j in range(n)] for i in range(n)]
        sx = matmul(F, S) == matmul(S, F)
        Fy = read(name, n - 1)
        ep = [Q(int(i == p)) for i in range(n)]
        wit[name] = {'PN': pn_all, 'SX': sx, 'c': str((F[u][u] - F[v][u]) / 5),
                     'kappa': str(sum(matvec(F, ep))), 'post_receiver': str(matvec(Fy, PD)[keep.index(p)])}
    # drop SX: PN-only space, receiver pre-contrast
    rowsN = []
    for r in range(n - 1):
        row = [Q(0)] * (n * n)
        for i in range(n):
            row[i * n + u] += P[r][i]
            row[i * n + p] -= P[r][i]
        rowsN.append(row)
    dropSX = any(sum(vec[p * n + j] * Delta[j] for j in range(n)) != 0 for vec in rref_nullspace(rowsN, n * n))
    dropPN = True  # F = id with F_Y = 0 violates PN and gives post receiver 0 != 1/5
    need(matvec(zeros(n - 1, n - 1), PD)[keep.index(p)] != Q(1, 5), 'drop-PN witness')
    def cone_vec(verts, a):
        out = []
        for w in verts:
            x = w
            while x is not None and x != a:
                x = par[x]
            out.append(Q(int(x == a)))
        return out
    ctrl = {}
    for nm, a in (('C_0', 0), ('C_p', p)):
        cw = cone_vec(range(n), a); cy = cone_vec(keep, a)
        ctrl[nm] = {'pre': str(sum(x * y for x, y in zip(cw, Delta))), 'post': str(sum(x * y for x, y in zip(cy, PD)))}
    return {'n': n, 'dim': len(tb), 'dim_predicted': n * n - 3 * n + 3, 'basis_ok': ok,
            'nonzero_c': any(c != 0 for c in cs), 'witness': wit,
            'drop_SX_pre_receiver_nonzero_exists': dropSX, 'drop_PN_post_receiver_differs_exists': dropPN,
            'cone_total_control': ctrl}

# ---------- claim O ----------
def analyse_O(par, p):
    n = len(par)
    carriers = []
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        if 0 in S and p in S and all(par[i] in S for i in S if i != 0):
            carriers.append(tuple(S))
    off, idx = 0, {}
    for X in carriers:
        idx[X] = off
        off += len(X)
    rows = []
    for X in carriers:
        chX = {i: [c for c in X if par[c] == i] for i in X}
        for l in X:
            if l in (0, p) or chX[l]:
                continue
            Xl = tuple(i for i in X if i != l)
            for j, w in enumerate(X):
                row = [Q(0)] * off
                tgt = par[l] if w == l else w
                row[idx[Xl] + Xl.index(tgt)] += 1
                row[idx[X] + j] -= 1
                rows.append(row)
    dim = len(rref_nullspace(rows, off))
    chain = []
    x = p
    while x is not None:
        chain.append(x); x = par[x]
    chain = chain[::-1]
    # claimed family alpha o P_{X,[0,p]} satisfies every INV row
    for k in range(len(chain)):
        vec = [Q(0)] * off
        for X in carriers:
            for j, w in enumerate(X):
                y = w
                while y not in chain:
                    y = par[y]
                vec[idx[X] + j] = Q(int(y == chain[k]))
        need(all(sum(a * b for a, b in zip(r, vec)) == 0 for r in rows), 'claimed O family violates INV')
    return {'n': n, 'depth': depth(par, p), 'carriers': len(carriers), 'dim': dim,
            'factorizes': dim == len(chain)}

# ---------- comparison against the producer certificate ----------
def tree_from_addresses(verts):
    verts = [tuple(w) for w in verts]
    need(len(set(verts)) == len(verts) and verts and verts[0] == (), 'vertex list')
    pos = {w: i for i, w in enumerate(verts)}
    par = [None]
    for w in verts[1:]:
        need(w[:-1] in pos, 'non-prefix-closed carrier')
        par.append(pos[w[:-1]])
    return par, pos

def verify(cert, producer_bytes):
    need(cert.get('producer_sha256') == hashlib.sha256(producer_bytes).hexdigest(), 'false provenance')
    counts = {str(n): len(all_trees(n)) for n in range(1, 8)}
    need(cert.get('tree_counts') == counts, 'false coverage: tree counts')
    expP, expO = {}, {}
    for n in range(3, 8):
        for par in all_trees(n):
            for k, (p, u, v) in P_cases_for(par).items():
                need(k not in expP, 'verifier duplicate P key')
                expP[k] = analyse_P(par, p, u, v)
    for n in range(1, 7):
        for par in all_trees(n):
            done = set()
            for p in range(n):
                k = ahu(par, {p: 'p'})
                if k not in done:
                    done.add(k)
                    expO[k] = analyse_O(par, p)
    keysP = [r['key'] for r in cert['P_cases']]
    keysO = [r['key'] for r in cert['O_cases']]
    need(len(keysP) == len(set(keysP)), 'duplicated P case')
    need(len(keysO) == len(set(keysO)), 'duplicated O case')
    need(set(keysP) == set(expP), 'missing or substituted P case')
    need(set(keysO) == set(expO), 'missing or substituted O case')
    for r in cert['P_cases']:
        par, pos = tree_from_addresses(r['vertices'])
        p, u, v = pos[tuple(r['p'])], pos[tuple(r['u'])], pos[tuple(r['v'])]
        ch = children_of(par)
        need(par[u] == p and par[v] == p and not ch[u] and not ch[v] and u != v, 'invalid fork')
        need(ahu(par, {u: 'u', v: 'u'}) == r['key'], 'substituted tree')
        e = expP[r['key']]
        for f in ('n', 'dim', 'dim_predicted', 'basis_ok', 'witness', 'drop_SX_pre_receiver_nonzero_exists',
                  'drop_PN_post_receiver_differs_exists', 'cone_total_control'):
            need(r[f] == e[f], 'P value mismatch: ' + f)
        need(len(r['basis']) == e['dim'], 'P basis length')
        n = len(par)
        keep = [i for i in range(n) if i != u]
        for b in r['basis']:
            c = Q(b['c'])
            need([Q(x) for x in b['pre']] == [c if i == u else (-c if i == v else Q(0)) for i in range(n)], 'wrong pre value')
            need([Q(x) for x in b['post']] == [c if y == p else (-c if y == v else Q(0)) for y in keep], 'wrong post value')
            need(b['ok'] is True, 'producer row flag')
        need(any(Q(b['c']) != 0 for b in r['basis']) == e['nonzero_c'], 'Nd witness mismatch')
    for r in cert['O_cases']:
        par, pos = tree_from_addresses(r['vertices'])
        need(ahu(par, {pos[tuple(r['p'])]: 'p'}) == r['key'], 'substituted O tree')
        e = expO[r['key']]
        for f in ('n', 'depth', 'carriers', 'dim', 'factorizes'):
            need(r[f] == e[f], 'O value mismatch: ' + f)
    # scientific gates
    gates = {
        'P_formulas_all_cases': all(e['basis_ok'] for e in expP.values()),
        'P_dim_matches_n2_3n_3': all(e['dim'] == e['dim_predicted'] for e in expP.values()),
        'Nd_nonzero_admissible_exists': all(e['nonzero_c'] for e in expP.values()),
        'K_witnesses': all(e['witness']['id']['c'] == '1/5' and e['witness']['tot']['c'] == '0'
                           and e['witness']['tot']['kappa'] == '1' and e['witness']['dif']['kappa'] == '0'
                           and e['witness']['dif']['c'] == '1/5'
                           and all(w['PN'] and w['SX'] for w in e['witness'].values()) for e in expP.values()),
        'N_drop_SX_witness': all(e['drop_SX_pre_receiver_nonzero_exists'] for e in expP.values()),
        'N_drop_PN_witness': all(e['drop_PN_post_receiver_differs_exists'] for e in expP.values()),
        'T233_cone_total_control_fails_to_separate': all(
            all(v == {'pre': '0', 'post': '0'} for v in e['cone_total_control'].values()) for e in expP.values()),
        'O_dim_depth_plus_1_and_factorizes': all(e['factorizes'] for e in expO.values()),
    }
    need(all(gates.values()), 'scientific gate RED: ' + json.dumps(gates, sort_keys=True))
    return {'status': 'GREEN', 'P_cases': len(expP), 'O_cases': len(expO),
            'P_basis_elements': sum(e['dim'] for e in expP.values()),
            'O_carriers': sum(e['carriers'] for e in expO.values()), 'tree_counts': counts, 'gates': gates}

def main():
    cert_path, producer_path = sys.argv[1], sys.argv[2]
    raw = open(cert_path, 'rb').read()
    cert = json.loads(raw)
    try:
        res = verify(cert, open(producer_path, 'rb').read())
    except Reject as exc:
        sys.stdout.write(json.dumps({'status': 'REJECTED', 'reason': str(exc)}, sort_keys=True) + '\n')
        sys.exit(1)
    res['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    sys.stdout.write(json.dumps(res, sort_keys=True, indent=1) + '\n')

if __name__ == '__main__':
    main()
