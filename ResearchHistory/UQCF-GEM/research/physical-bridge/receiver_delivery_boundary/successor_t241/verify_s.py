"""Successor independent checker (stdlib only: fractions, json, hashlib, math).
Rebuilds every operator from the definitions in CORRECTION_T241 section 4 and CORRECTION_T242 section 4 using its own
exact arithmetic in Q(sqrt2), its own sparse tensor indexing and its own 2x2 trace norm; requires exact identity with
the producer certificate and evaluates the frozen predictions V1-V7. Exit 0 = GREEN, 1 = RED.
Usage: verify_s.py certificate.json produce_s.py"""
import hashlib, json, sys
from fractions import Fraction as Fr
from math import isqrt


class Q2:
    """a + b*sqrt(2) with rational a, b."""
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(s, o): o = q(o); return Q2(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q(o); return Q2(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q(o) - s
    def __neg__(s): return Q2(-s.a, -s.b)
    def __mul__(s, o): o = q(o); return Q2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def rat(s):
        if s.b != 0:
            raise ValueError('irrational value outside checker scope')
        return s.a


def q(x):
    return x if isinstance(x, Q2) else Q2(x)


def sqrt_rat(x):
    x = Fr(x)
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    if x < 0 or n * n != x.numerator or d * d != x.denominator:
        raise ValueError('non-square')
    return Fr(n, d)


SITES = 'opuv'
H = Q2(0, Fr(1, 2))                       # sqrt(2)/2
PSI = {'o': Q2(0), 'p': H, 'u': Q2(Fr(1, 2)), 'v': Q2(Fr(1, 2))}
# K basis labelled (e, r) in {0,1}^2
KB = [(e, r) for e in (0, 1) for r in (0, 1)]


def kvec(d):
    return {k: q(x) for k, x in d.items() if q(x) != 0}


def theta(c):
    c = Fr(c)
    sn = sqrt_rat(1 - c * c)
    return (kvec({(0, 0): 1}), kvec({(1, 0): c, (0, 1): sn}))   # a=R, b=E: a0(x)b1 = (e=1,r=0); a1(x)b0 = (e=0,r=1)


REAL = {
    'W_E': (kvec({(0, 0): 1}), kvec({(1, 0): 1})),
    'W_R': (kvec({(0, 0): 1}), kvec({(0, 1): 1})),
    'W_c3_5': theta(Fr(3, 5)),
    'W_c4_5': theta(Fr(4, 5)),
    'W_N': (kvec({(0, 0): Fr(3, 5), (1, 1): Fr(4, 5)}), kvec({(0, 1): 1})),
    'W_X': (kvec({(1, 1): 1}), kvec({(0, 0): 1})),
}
THETA = {'1': 'W_E', '4/5': 'W_c4_5', '3/5': 'W_c3_5', '0': 'W_R'}
ZP = {'plus': dict(zip(SITES, [Fr(1, 5), Fr(1, 5), Fr(2, 5), Fr(1, 5)])), 'minus': dict(zip(SITES, [Fr(1, 5), Fr(1, 5), Fr(1, 5), Fr(2, 5)]))}
ZQ = {'plus': dict(zip(SITES, [Fr(1, 5), Fr(2, 5), Fr(1, 5), Fr(1, 5)])), 'minus': dict(zip(SITES, [Fr(1, 5), Fr(1, 5), Fr(2, 5), Fr(1, 5)]))}


def W_col(real, j):
    e0, eu = real
    return {('p', k): x for k, x in eu.items()} if j == 'u' else {(j, k): x for k, x in e0.items()}


def W_diag_state(real, z):
    """W diag(z) W^T as sparse dict {((s,k),(t,l)): x}"""
    out = {}
    for j in SITES:
        col = W_col(real, j)
        for a, x in col.items():
            for b, y in col.items():
                out[(a, b)] = out.get((a, b), Q2()) + z[j] * x * y
    return out


def sub(A, B):
    out = dict(A)
    for k, x in B.items():
        out[k] = out.get(k, Q2()) - x
    return out


def y_of(z):
    return {'o': z['o'], 'p': z['p'] + z['u'], 'u': Fr(0), 'v': z['v']}


def inner(a, b):
    return sum((x * b.get(k, Q2()) for k, x in a.items()), Q2())


def check_realization(real):
    cols = {j: W_col(real, j) for j in SITES}
    iso = all(inner(cols[a], cols[b]) == (1 if a == b else 0) for a in SITES for b in SITES)
    impl = True
    for a in SITES:
        for b in SITES:
            # Tr_K W|a><b|W^T  vs  C(|a><b|)
            red = {}
            for (s1, k1), x in cols[a].items():
                for (s2, k2), y in cols[b].items():
                    if k1 == k2:
                        red[(s1, s2)] = red.get((s1, s2), Q2()) + x * y
            red = {k: v for k, v in red.items() if v != 0}
            if a == 'u' and b == 'u':
                want = {('p', 'p'): Q2(1)}
            elif 'u' in (a, b):
                want = {}
            else:
                want = {(a, b): Q2(1)}
            impl = impl and red == want
    return iso, impl


def proj_psi(s, t):
    return PSI[s] * PSI[t]


ALG = {
    'psi': [lambda s, t: proj_psi(s, t), lambda s, t: Q2(1 if s == t else 0) - proj_psi(s, t)],
    'C1': [lambda s, t: Q2(1 if s == t else 0)],
    'pi_p': [lambda s, t: Q2(1 if s == t == 'p' else 0), lambda s, t: Q2(1 if s == t != 'p' else 0)],
}


def tn2(m):
    """trace norm of a real symmetric 2x2 [[a,b],[b,d]] with rational entries"""
    a, b, d = m[0][0], m[0][1], m[1][1]
    if m[1][0] != b:
        raise ValueError('not symmetric')
    tr, det = a + d, a * d - b * b
    if det >= 0:
        return abs(tr)
    return sqrt_rat(tr * tr - 4 * det)


def delta_iface(D, alg):
    tot = Fr(0)
    for Qf in ALG[alg]:
        m = [[Q2(), Q2()], [Q2(), Q2()]]
        for ((s, (e, r)), (t, (f, qq))), x in D.items():
            if e == f:
                m[r][qq] = m[r][qq] + Qf(t, s) * x
        tot += tn2([[m[i][j].rat() for j in range(2)] for i in range(2)])
    return tot / 2


def delta_S(dy, alg):
    return sum(abs(sum((Qf(s, s) * dy[s] for s in SITES), Q2()).rat()) for Qf in ALG[alg]) / 2


def trace_FD(Fentry, D):
    return sum((Fentry(b, a) * x for (a, b), x in D.items()), Q2())


# ---- V5 operators (overridable by controls) ----
FY = {'o': Fr(1, 3), 'p': Fr(1, 2), 'v': Fr(1, 4)}


def F5(a, b):
    (s, k), (t, l) = a, b
    if s == t and s in FY:
        return Q2(FY[s] if k == l else 0)
    if s == t == 'u':
        return Q2(Fr(KB.index(k) + 1, 7) if k == l else 0)
    if {s, t} == {'o', 'p'}:
        ko, kp = (k, l) if s == 'o' else (l, k)
        if (KB.index(ko), KB.index(kp)) == (0, 1):
            return Q2(Fr(1, 9))
        if (KB.index(ko), KB.index(kp)) == (2, 3):
            return Q2(Fr(2, 11))
    return Q2(0)


def F5b(a, b):
    return Q2(1 if a == b == ('p', (0, 0)) else 0)


def F4(a, b):
    return Q2(1 if a == b and a[1] == (0, 1) else 0)


def dotF_entry(sigma_x):
    def U(j, k):  # U_j |k>
        if j == 'u' and sigma_x:
            return (1 - k[0], k[1])
        return k
    def F(a, b):
        (s, k), (t, l) = a, b
        # F = V (P_psi (x) 1) V^T : <s k|F|t l> = psi_s psi_t <k|U_s U_t^T|l>
        # U_t^T|l> = U_t^{-1}|l> (permutation, involution here)
        return PSI[s] * PSI[t] * Q2(1 if U(s, U(t, l)) == k else 0) if True else None
    return F


def dot_analysis(sigma_x, Dout):
    F = dotF_entry(sigma_x)
    basis = [(s, k) for s in SITES for k in KB]
    M = {(a, b): F(a, b) for a in basis for b in basis}
    idem = all(sum((M[(a, c)] * M[(c, b)] for c in basis), Q2()) == M[(a, b)] for a in basis for b in basis)
    def blk(s, t):
        return [[M[((s, k), (t, l))] for l in KB] for k in KB]
    def scal(B):
        return all(B[i][j] == (B[0][0] if i == j else 0) for i in range(4) for j in range(4))
    diag = [str(blk(s, s)[0][0].rat()) if scal(blk(s, s)) else 'nonscalar' for s in SITES]
    allscal = all(scal(blk(s, t)) for s in SITES for t in SITES)
    dz = {s: ZP['plus'][s] - ZP['minus'][s] for s in SITES}
    init = sum((M[((s, (0, 0)), (s, (0, 0)))] * dz[s] for s in SITES), Q2()).rat()
    pc = {n: str(abs(sum((M[(b, a)] * x for (a, b), x in D.items()), Q2()).rat())) for n, D in Dout.items()}
    return {'idempotent': idem, 'diag_blocks': diag, 'in_BHS_tensor_1K': allscal, 'b_nonzero_solution_exists': allscal,
            'initial_contrast': str(abs(init)), 'pair_contrast': pc}


def rank(rows):
    rows = [list(r) for r in rows]
    rk, col, n = 0, 0, len(rows[0])
    while rk < len(rows) and col < n:
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            col += 1; continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][col] != 0:
                f = rows[i][col] / rows[rk][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        rk += 1; col += 1
    return rk


def recompute():
    c = {}
    c['realizations'] = {}
    for n, real in REAL.items():
        iso, impl = check_realization(real)
        ser = lambda v: [str(v.get(k, Q2()).rat()) for k in KB]
        c['realizations'][n] = {'e0': ser(real[0]), 'eu': ser(real[1]), 'isometry': iso, 'implements_C': impl}
    Dout = {n: sub(W_diag_state(r, ZP['plus']), W_diag_state(r, ZP['minus'])) for n, r in REAL.items()}
    dz = {s: ZP['plus'][s] - ZP['minus'][s] for s in SITES}
    dy = {s: y_of(ZP['plus'])[s] - y_of(ZP['minus'])[s] for s in SITES}
    c['V1'] = {'pre_event_contrast': str(delta_S(dz, 'psi')), 'd_S': str(delta_S(dy, 'psi')),
               'Delta': {n: str(delta_iface(Dout[n], 'psi')) for n in ('W_E', 'W_R')}}
    c['V2'] = {a: {'d_S': str(delta_S(dy, a)), 'Delta': {th: str(delta_iface(Dout[n], a)) for th, n in THETA.items()}} for a in ALG}
    yq = {k: y_of(ZQ[k]) for k in ZQ}
    c['V3'] = {'pre_pi_p': {k: str(ZQ[k]['p']) for k in ZQ}, 'post_equal': yq['plus'] == yq['minus'],
               'post_y': [str(yq['plus'][s]) for s in SITES]}
    c['V4'] = {n: str(abs(trace_FD(F4, Dout[n]).rat())) for n in ('W_R', 'W_E')}
    stats = {}
    for n, r in REAL.items():
        stats[n] = {k: str(trace_FD(F5, W_diag_state(r, ZP[k])).rat()) for k in ZP}
    sig = {k: str(sum(FY[j] * y_of(ZP[k])[j] for j in FY)) for k in ZP}
    c['V5'] = {'i': {'stats': stats, 'sigma_f_y': sig}, 'ii': {n: str(abs(trace_FD(F5b, Dout[n]).rat())) for n in REAL}}
    c['V6'] = dot_analysis(True, Dout)
    c['V6b'] = dot_analysis(False, Dout)
    # V7: unknowns g = (G1 entries r-major, G2 entries r-major); constraints on Y-blocks G1 + |psi_j|^2 G2
    rows = []
    for j in 'opv':
        w = (PSI[j] * PSI[j]).rat()
        for (i1, j1, i2, j2) in ((0, 1, None, None), (1, 0, None, None), (0, 0, 1, 1)):
            row = [Fr(0)] * 8
            row[2 * i1 + j1] += 1; row[4 + 2 * i1 + j1] += w
            if i2 is not None:
                row[2 * i2 + j2] -= 1; row[4 + 2 * i2 + j2] -= w
            rows.append(row)
    dim = 8 - rank(rows)
    alpha, beta = Fr(1, 3), Fr(1, 2)
    f = {j: alpha + beta * (PSI[j] * PSI[j]).rat() for j in 'opv'}
    phis = {'a0': {0: Q2(1)}, 'a1': {1: Q2(1)}, 'a+': {0: H, 1: H}}
    comp = {}
    for pn, phi in phis.items():
        nrm = sum((x * x for x in phi.values()), Q2())          # <phi|1_R|phi>
        def G(s, t):
            return (alpha * (1 if s == t else 0) + beta * proj_psi(s, t)) * nrm
        comp[pn] = {k: str(sum((G(s, s) * y_of(ZP[k])[s] for s in SITES), Q2()).rat()) for k in ZP}
    c['V7'] = {'invariant_dim': dim, 'compression': comp,
               'sigma_f_y': {k: str(sum(f[j] * y_of(ZP[k])[j] for j in f)) for k in ZP}}
    return c


def predictions(c):
    f = Fr
    p = {}
    p['realizations_valid'] = all(r['isometry'] and r['implements_C'] for r in c['realizations'].values())
    v1 = c['V1']
    p['V1'] = (f(v1['pre_event_contrast']) == 0 and f(v1['Delta']['W_E']) == f(1, 20) and f(v1['Delta']['W_R']) == f(1, 5)
               and f(v1['d_S']) == f(1, 20))
    ends = {'psi': (f(1, 20), f(1, 5)), 'C1': (f(0), f(1, 5)), 'pi_p': (f(1, 5), f(1, 5))}
    ok = True
    for a, (lo, hi) in ends.items():
        v = c['V2'][a]
        ok = ok and f(v['d_S']) == lo and f(v['Delta']['1']) == lo and f(v['Delta']['0']) == hi
        ok = ok and all(lo <= f(x) <= f(1, 5) for x in v['Delta'].values())
    p['V2'] = ok
    v3 = c['V3']
    p['V3'] = f(v3['pre_pi_p']['plus']) == f(2, 5) and f(v3['pre_pi_p']['minus']) == f(1, 5) and v3['post_equal'] is True
    p['V4'] = f(c['V4']['W_R']) == f(1, 5) and f(c['V4']['W_E']) == 0
    v5 = c['V5']
    sig = v5['i']['sigma_f_y']
    p['V5_i'] = (f(sig['plus']) == f(5, 12) and f(sig['minus']) == f(11, 30)
                 and all(st == sig for st in v5['i']['stats'].values()))
    p['V5_ii'] = len(set(v5['ii'].values())) >= 2
    v6 = c['V6']
    p['V6'] = (v6['idempotent'] is True and v6['diag_blocks'] == ['0', '1/2', '1/4', '1/4'] and f(v6['initial_contrast']) == 0
               and all(f(x) == f(1, 20) for x in v6['pair_contrast'].values()) and v6['in_BHS_tensor_1K'] is False
               and v6['b_nonzero_solution_exists'] is False)
    p['V6b'] = c['V6b']['in_BHS_tensor_1K'] is True and c['V6b']['b_nonzero_solution_exists'] is True
    v7 = c['V7']
    p['V7'] = v7['invariant_dim'] == 2 and all(v == v7['sigma_f_y'] for v in v7['compression'].values())
    return p


def main():
    cert = json.load(open(sys.argv[1]))
    prod_hash = hashlib.sha256(open(sys.argv[2], 'rb').read()).hexdigest()
    mine = recompute()
    mism = sorted(k for k in mine if cert.get(k) != mine[k])
    pred = predictions(mine)
    out = {'producer_hash_matches': cert.get('producer_sha256') == prod_hash,
           'certificate_matches_recomputation': not mism, 'mismatched_sections': mism,
           'predictions': pred, 'schema_ok': cert.get('schema') == 'uqcf-t241-successor-v1'}
    out['status'] = 'GREEN' if (out['producer_hash_matches'] and not mism and all(pred.values()) and out['schema_ok']) else 'RED'
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if out['status'] == 'GREEN' else 1)


if __name__ == '__main__':
    main()
