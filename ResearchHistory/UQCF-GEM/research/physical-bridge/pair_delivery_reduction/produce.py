#!/usr/bin/env python3
"""T-235 producer: pair-delivery premise reduction (exact, sympy over Q).

Enumeration: rooted unlabeled trees by recursive multiset partitions of child subtrees.
Linear algebra: sympy nullspaces of stacked constraint matrices.
Writes a canonical JSON certificate to stdout (deterministic bytes)."""
import hashlib
import json
import sys
from fractions import Fraction
from itertools import combinations_with_replacement

import sympy as sp

# ---------- trees as nested sorted tuples ----------
def trees(n, memo={}):
    """All rooted unlabeled trees with n vertices, as canonical nested tuples."""
    if n in memo:
        return memo[n]
    if n == 1:
        memo[1] = [()]
        return memo[1]
    out = set()
    def forests(m, maxkey):
        if m == 0:
            yield ()
            return
        for k in range(1, m + 1):
            for t in trees(k):
                key = (k, t)
                if maxkey is not None and key > maxkey:
                    continue
                for rest in forests(m - k, key):
                    yield (t,) + rest
    for f in forests(n - 1, None):
        out.add(tuple(sorted(f)))
    memo[n] = sorted(out)
    return memo[n]

def size(t):
    return 1 + sum(size(c) for c in t)

def materialize(t):
    """Vertices as address tuples, preorder; returns list of addresses."""
    out = []
    def rec(node, addr):
        out.append(addr)
        for i, c in enumerate(node):
            rec(c, addr + (i,))
    rec(t, ())
    return out

def subtree_at(t, addr):
    for i in addr:
        t = t[i]
    return t

def canon_with_marks(t, marks):
    """Canonical string of tree with some addresses marked (for orbit identification)."""
    def rec(node, addr):
        kids = sorted(rec(c, addr + (i,)) for i, c in enumerate(node))
        return '(' + marks.get(addr, '') + ''.join(kids) + ')'
    return rec(t, ())

# ---------- linear maps ----------
def pushforward(V, u):
    """P for pruning leaf u; rows indexed by V\\{u}, columns by V."""
    Y = [w for w in V if w != u]
    P = sp.zeros(len(Y), len(V))
    for j, w in enumerate(V):
        tgt = w[:-1] if w == u else w
        P[Y.index(tgt), j] = 1
    return Y, P

def retract_matrix(V, Z):
    """P_{V->Z}: longest prefix in Z."""
    M = sp.zeros(len(Z), len(V))
    for j, w in enumerate(V):
        k = len(w)
        while w[:k] not in Z:
            k -= 1
        M[Z.index(w[:k]), j] = 1
    return M

def perm_matrix(V, perm):
    n = len(V)
    S = sp.zeros(n, n)
    for j, w in enumerate(V):
        S[V.index(perm.get(w, w)), j] = 1
    return S

def unknown_matrix(n, offset):
    return sp.Matrix(n, n, lambda i, j: sp.Symbol('m%d' % (offset + i * n + j)))

def solve_space(constraints, syms):
    """Basis (list of dicts sym->Rational) of the solution space of homogeneous linear eqs."""
    if constraints:
        A = sp.Matrix([[sp.diff(c, s) for s in syms] for c in constraints])
        ns = A.nullspace()
    else:
        ns = [sp.Matrix([1 if k == i else 0 for k in range(len(syms))]) for i in range(len(syms))]
    return [dict(zip(syms, list(vec))) for vec in ns]

def frac(x):
    x = sp.Rational(x)
    return str(Fraction(int(x.p), int(x.q)))

# ---------- claim P ----------
def pair_cases(t):
    V = materialize(t)
    seen = {}
    for p in V:
        kids = [p + (i,) for i in range(len(subtree_at(t, p)))]
        leaves = [k for k in kids if len(subtree_at(t, k)) == 0]
        for a in range(len(leaves)):
            for b in range(a + 1, len(leaves)):
                u, v = leaves[a], leaves[b]
                key = canon_with_marks(t, {u: 'u', v: 'u'})
                if key not in seen:
                    seen[key] = (p, u, v)
    return [(k,) + seen[k] for k in sorted(seen)]

def check_P(t, key, p, u, v):
    V = materialize(t)
    n = len(V)
    Y, P = pushforward(V, u)
    I = P.T * 0
    for i, y in enumerate(Y):
        I[V.index(y), i] = 1
    S = perm_matrix(V, {u: v, v: u})
    F = unknown_matrix(n, 0)
    syms = list(F)
    cons = list(F * S - S * F)
    eu = sp.Matrix([1 if w == u else 0 for w in V])
    ep = sp.Matrix([1 if w == p else 0 for w in V])
    ev = sp.Matrix([1 if w == v else 0 for w in V])
    cons += list(P * F * (eu - ep))
    cons = [c for c in cons if c != 0]
    basis = solve_space(cons, syms)
    Delta = (eu - ev) / 5
    rows = []
    ok = True
    for b in basis:
        Fw = F.subs(b)
        Fy = P * Fw * I
        assert Fy * P == P * Fw, 'PN-step must hold on the admissible basis'
        pre = Fw * Delta
        post = Fy * (P * Delta)
        c = (Fw[V.index(u), V.index(u)] - Fw[V.index(v), V.index(u)]) / 5
        exp_pre = c * (eu - ev)
        exp_post = sp.Matrix([c if y == p else (-c if y == v else 0) for y in Y])
        good = (pre == exp_pre) and (post == exp_post)
        ok = ok and good
        rows.append({'c': frac(c), 'pre': [frac(x) for x in pre], 'post': [frac(x) for x in post], 'ok': bool(good)})
    # Nd witnesses: kappa-id read and total-at-root read
    Fid = sp.eye(n)
    Ftot = sp.zeros(n, n)
    Ftot[0, :] = sp.ones(1, n)
    Fdif = sp.eye(n) - Ftot
    wit = {}
    for name, Fw in (('id', Fid), ('tot', Ftot), ('dif', Fdif)):
        Fy = P * Fw * I
        pn = (Fy * P == P * Fw)
        sx = (Fw * S == S * Fw)
        c = (Fw[V.index(u), V.index(u)] - Fw[V.index(v), V.index(u)]) / 5
        kappa = sum(Fw * ep)  # total holding of a unit (constant for these reads)
        post_p = (Fy * (P * Delta))[Y.index(p)]
        wit[name] = {'PN': bool(pn), 'SX': bool(sx), 'c': frac(c), 'kappa': frac(kappa), 'post_receiver': frac(post_p)}
    # N: drop SX -> pre-event receiver contrast can be nonzero
    consN = [x for x in list(P * F * (eu - ep)) if x != 0]
    basN = solve_space(consN, syms)
    pre_p_nonzero = any((F.subs(b) * Delta)[V.index(p)] != 0 for b in basN)
    # N: drop PN -> Fy free; post receiver contrast differs from c for some (Fw, Fy)
    G = unknown_matrix(n - 1, n * n)
    Fw0 = Fid
    alt_post = (G * (P * Delta))[Y.index(p)]
    drop_pn_witness = (alt_post.subs({s: 0 for s in G}) != Fraction(1, 5))
    # T-233 control: cone totals C_0 and C_p (invariant effects)
    def cone(Vs, a):
        return sp.Matrix([[1 if w[:len(a)] == a else 0 for w in Vs]])
    ctrl = {}
    for nm, a in (('C_0', ()), ('C_p', p)):
        ctrl[nm] = {'pre': frac((cone(V, a) * Delta)[0]), 'post': frac((cone(Y, a) * (P * Delta))[0])}
    return {
        'key': key, 'n': n, 'p': list(p), 'u': list(u), 'v': list(v), 'vertices': [list(w) for w in V],
        'dim': len(basis), 'dim_predicted': n * n - 3 * n + 3,
        'basis_ok': ok, 'basis': rows, 'witness': wit,
        'drop_SX_pre_receiver_nonzero_exists': bool(pre_p_nonzero),
        'drop_PN_post_receiver_differs_exists': bool(drop_pn_witness),
        'cone_total_control': ctrl,
    }

# ---------- claim O ----------
def carriers_containing(V, p):
    """All prefix-closed subsets of V (rooted) containing p, as sorted tuples."""
    V = sorted(V, key=lambda w: (len(w), w))
    res = []
    def rec(i, chosen):
        if i == len(V):
            if p in chosen:
                res.append(tuple(sorted(chosen, key=lambda w: (len(w), w))))
            return
        w = V[i]
        if w == () or w[:-1] in chosen:
            rec(i + 1, chosen | {w})
        if w != ():
            rec(i + 1, chosen)
    rec(0, frozenset())
    return res

def check_O(t, p):
    V = materialize(t)
    Xs = carriers_containing(V, p)
    syms, ell = [], {}
    for X in Xs:
        row = []
        for w in X:
            s = sp.Symbol('l%d' % len(syms))
            syms.append(s)
            row.append(s)
        ell[X] = sp.Matrix([row])
    cons = []
    for X in Xs:
        for l in X:
            if l == p or l == ():
                continue
            if any(w[:-1] == l for w in X if w != ()):
                continue
            Xl, P = pushforward(list(X), l)
            Xl = tuple(Xl)
            cons += list(ell[Xl] * P - ell[X])
    cons = [c for c in cons if c != 0]
    basis = solve_space(cons, syms)
    chain = tuple(p[:k] for k in range(len(p) + 1))
    W = tuple(sorted(V, key=lambda w: (len(w), w)))
    fact_ok = True
    for b in basis:
        lw = ell[W].subs(b)
        lc = ell[chain].subs(b)
        if lw != lc * retract_matrix(list(W), list(chain)):
            fact_ok = False
    return {'key': canon_with_marks(t, {p: 'p'}), 'n': len(V), 'depth': len(p), 'p': list(p), 'vertices': [list(w) for w in V],
            'carriers': len(Xs), 'dim': len(basis), 'factorizes': fact_ok}

def main():
    out = {'stage': 'T-235 pair_delivery_reduction', 'producer': 'produce.py', 'P_cases': [], 'O_cases': []}
    for n in range(3, 8):
        for t in trees(n):
            for key, p, u, v in pair_cases(t):
                out['P_cases'].append(check_P(t, key, p, u, v))
    for n in range(1, 7):
        for t in trees(n):
            seenp = set()
            for p in materialize(t):
                k = canon_with_marks(t, {p: 'p'})
                if k in seenp:
                    continue
                seenp.add(k)
                out['O_cases'].append(check_O(t, p))
    out['P_cases'].sort(key=lambda r: (r['n'], r['key']))
    out['O_cases'].sort(key=lambda r: (r['n'], r['key']))
    with open(__file__, 'rb') as fh:
        out['producer_sha256'] = hashlib.sha256(fh.read()).hexdigest()
    out['tree_counts'] = {str(n): len(trees(n)) for n in range(1, 8)}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')) + '\n')

if __name__ == '__main__':
    main()
