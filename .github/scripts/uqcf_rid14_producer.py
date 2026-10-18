"""receiver_identification d14 freeze (revised sec 18, secs 19-20, GPT fixed-effect follow-up): PRODUCER.
Pure-Python exact arithmetic (Fractions, Gaussian rationals), Kraus-form extensions with exact Cayley unitaries
(seed 20261018), prefix-sum typing, row-span algebra ranks. Writes a canonical JSON certificate."""
import hashlib, itertools, json, random, sys
from fractions import Fraction as F

random.seed(20261018)
RESULT_SHA = "f6cc849663224a5a2c877cd32a6700ecad9df1ea2d4f723a040c66e55dbc38f9"
VIOL = []


def ok(c, msg):
    if not c:
        VIOL.append(msg)


class G:
    __slots__ = ("r", "i")

    def __init__(s, r=0, i=0):
        s.r = F(r); s.i = F(i)

    def __add__(s, o): o = g(o); return G(s.r + o.r, s.i + o.i)
    __radd__ = __add__

    def __sub__(s, o): o = g(o); return G(s.r - o.r, s.i - o.i)

    def __neg__(s): return G(-s.r, -s.i)

    def __mul__(s, o): o = g(o); return G(s.r * o.r - s.i * o.i, s.r * o.i + s.i * o.r)
    __rmul__ = __mul__

    def conj(s): return G(s.r, -s.i)

    def inv(s): d = s.r * s.r + s.i * s.i; return G(s.r / d, -s.i / d)

    def __eq__(s, o): o = g(o); return s.r == o.r and s.i == o.i

    def z(s): return s.r == 0 and s.i == 0


def g(x): return x if isinstance(x, G) else G(x)


def zeros(m, n): return [[G() for _ in range(n)] for _ in range(m)]


def eye(n):
    M = zeros(n, n)
    for k in range(n): M[k][k] = G(1)
    return M


def mm(A, B):
    return [[sum((A[i][t] * B[t][j] for t in range(len(B)) if not A[i][t].z()), G()) for j in range(len(B[0]))]
            for i in range(len(A))]


def dag(A): return [[A[i][j].conj() for i in range(len(A))] for j in range(len(A[0]))]


def minv(A):
    n = len(A); M = [list(r) + e for r, e in zip(A, eye(n))]
    for c in range(n):
        p = next(r for r in range(c, n) if not M[r][c].z()); M[c], M[p] = M[p], M[c]
        iv = M[c][c].inv(); M[c] = [x * iv for x in M[c]]
        for r in range(n):
            if r != c and not M[r][c].z():
                f = M[r][c]; M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [r[n:] for r in M]


def cayley(n, cplx):
    A = zeros(n, n)
    for i in range(n):
        if cplx: A[i][i] = G(0, F(random.randint(-3, 3), random.randint(1, 3)))
        for j in range(i + 1, n):
            a = G(F(random.randint(-3, 3), random.randint(1, 3)), F(random.randint(-3, 3), random.randint(1, 3)) if cplx else 0)
            A[i][j] = a; A[j][i] = -a.conj()
    I = eye(n)
    return mm([[I[i][j] - A[i][j] for j in range(n)] for i in range(n)],
              minv([[I[i][j] + A[i][j] for j in range(n)] for i in range(n)]))


def rank(rows):
    M = [list(r) for r in rows]; rk = 0
    if not M: return 0
    for c in range(len(M[0])):
        p = next((r for r in range(rk, len(M)) if not M[r][c].z()), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; iv = M[rk][c].inv(); M[rk] = [x * iv for x in M[rk]]
        for r in range(len(M)):
            if r != rk and not M[r][c].z():
                f = M[r][c]; M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk


def frs(x): x = F(x); return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def gstr(x):
    assert x.i == 0; return frs(x.r)


def digest(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ---------------- regions and extensions ----------------
REGIONS = [((0, 1), (0, 1), (0,), (0, 1, 2)), ((0, 1, 2), (0, 1), (0,), (0, 1, 2, 3)), ((0, 1), (0, 1, 2), (0,), (0, 1, 2, 3)),
           ((0, 1, 2), (0, 1, 2), (0,), (0, 1, 2, 3, 4)), ((0, 2), (0,), (0,), (0, 1, 2)), ((0, 2), (0, 1), (0,), (0, 1, 2, 3)),
           ((0, 1), (0, 1), (0, 1), (0, 1, 2)), ((0, 1), (0,), (0, 1), (0, 1)), ((0, 1), (0, 1), (0,), (0, 1, 2, 3))]
BYSTANDER = [False] * 6 + [True, True, False]


def region(Ol, Op, Oz, reg, f=None):
    B = [(j, x, z) for j in Ol for x in Op for z in Oz]
    fm = {b: (b[0] + b[1], b[2]) for b in B} if f is None else {b: f(b) for b in B}
    outs = [(y, z) for y in reg for z in Oz]
    return B, fm, outs, {o: k for k, o in enumerate(outs)}


def kraus_cols(B, fm, oi, cols, m):
    Ks = []
    for i in range(m):
        K = zeros(len(oi), len(B))
        for bi, b in enumerate(B): K[oi[fm[b]]][bi] = cols[b][i]
        Ks.append(K)
    return Ks


def ext_dephase(B, fm, oi):
    return kraus_cols(B, fm, oi, {b: [G(1) if k == bi else G() for k in range(len(B))] for bi, b in enumerate(B)}, len(B))


def ext_pair(B, fm, oi, b0, b1):
    K0 = zeros(len(oi), len(B)); K0[oi[fm[b0]]][B.index(b0)] = G(1); K0[oi[fm[b1]]][B.index(b1)] = G(1)
    Ks = [K0]
    for bi, b in enumerate(B):
        if b in (b0, b1): continue
        K = zeros(len(oi), len(B)); K[oi[fm[b]]][bi] = G(1); Ks.append(K)
    return Ks


def ext_random(B, fm, oi, cplx, extra):
    fib = {}
    for b in B: fib.setdefault(fm[b], []).append(b)
    m = max(len(v) for v in fib.values()) + extra; cols = {}
    for y in sorted(fib):
        U = cayley(m, cplx)
        for t, b in enumerate(fib[y]): cols[b] = [U[t][i] for i in range(m)]
    return kraus_cols(B, fm, oi, cols, m)


def family(B, fm, oi):
    pairs = [(b0, b1) for b0, b1 in itertools.combinations(B, 2) if fm[b0] != fm[b1]]
    fam = [("dep", ext_dephase(B, fm, oi))] + [("pair", ext_pair(B, fm, oi, a, b)) for a, b in pairs]
    fam += [("rand", ext_random(B, fm, oi, cplx=(k % 2 == 1), extra=(0 if k < 3 else 1))) for k in range(6)]
    return fam, len(pairs)


def heis_unit(Ks, u, v, nb):
    return [[sum((Ks[i][u][b].conj() * Ks[i][v][c] for i in range(len(Ks)) if not Ks[i][u][b].z() and not Ks[i][v][c].z()), G())
             for c in range(nb)] for b in range(nb)]


def heis(Ks, E):
    S = None
    for K in Ks:
        X = mm(mm(dag(K), E), K); S = X if S is None else [[a + b for a, b in zip(r, s)] for r, s in zip(S, X)]
    return S


def schr(Ks, rho):
    S = None
    for K in Ks:
        X = mm(mm(K, rho), dag(K)); S = X if S is None else [[a + b for a, b in zip(r, s)] for r, s in zip(S, X)]
    return S


def meq(A, B): return all(a == b for r, s in zip(A, B) for a, b in zip(r, s))


def diagm(vals): M = zeros(len(vals), len(vals)); [M[k].__setitem__(k, G(v)) for k, v in enumerate(vals)]; return M


def u19a():
    out = []; stats = {"extensions": 0, "pair": 0, "rand": 0, "dep": 0, "units": 0, "inv": 0, "noninv": 0, "kraus_ops": 0,
                       "coherent_inputs": 0}
    dims = []; units = []; pairs_l = []; plocal = []
    for ri, (Ol, Op, Oz, reg) in enumerate(REGIONS):
        B, fm, outs, oi = region(Ol, Op, Oz, reg); nb, d = len(B), len(outs)
        R = {fm[b] for b in B}
        fam, npairs = family(B, fm, oi)
        for kind, Ks in fam:
            stats[kind] += 1; stats["extensions"] += 1; stats["kraus_ops"] += len(Ks)
            ok(meq(heis(Ks, eye(d)), eye(nb)), "TP r%d" % ri)
            for bi, b in enumerate(B):
                rho = zeros(nb, nb); rho[bi][bi] = G(1); o = schr(Ks, rho)
                tgt = zeros(d, d); tgt[oi[fm[b]]][oi[fm[b]]] = G(1); ok(meq(o, tgt), "classical r%d" % ri)
            Qo = diagm([1 if outs[k][0] > 0 else 0 for k in range(d)]); Pi = diagm([1 if b[0] + b[1] > 0 else 0 for b in B])
            for K in Ks: ok(meq(mm(Qo, K), mm(K, Pi)), "QK=KP r%d" % ri)
            ok(meq(heis(Ks, Qo), Pi), "Phi*(Q)=P r%d" % ri)
            Eab = diagm([F(3, 4) if outs[k][0] > 0 else F(1, 4) for k in range(d)])
            ok(meq(heis(Ks, Eab), diagm([F(3, 4) if b[0] + b[1] > 0 else F(1, 4) for b in B])), "E_ab r%d" % ri)
            for y in outs:
                Py = diagm([1 if fm[b] == y else 0 for b in B]); ok(meq(heis_unit(Ks, oi[y], oi[y], nb), Py), "19.4b r%d" % ri)
            for t in range(3):
                v = [G(F(random.randint(-3, 3), random.randint(1, 2)), F(random.randint(-3, 3), random.randint(1, 2))) for _ in B]
                if all(x.z() for x in v): v[0] = G(1)
                nrm = sum((x.conj() * x).r for x in v)
                rho = [[v[a] * v[c].conj() * G(1 / nrm) for c in range(nb)] for a in range(nb)]
                o = schr(Ks, rho); stats["coherent_inputs"] += 1
                for k in range(d):
                    ok(o[k][k] == sum((rho[bi][bi] for bi, b in enumerate(B) if fm[b] == outs[k]), G()), "19.4c r%d" % ri)
        dep = fam[0][1]
        inv_list = []
        for u in range(d):
            for v in range(d):
                ref = heis_unit(dep, u, v, nb)
                inv = all(meq(heis_unit(Ks, u, v, nb), ref) for _, Ks in fam[1:])
                pred = u == v or outs[u] not in R or outs[v] not in R
                ok(inv == pred, "19.4a r%d (%d,%d)" % (ri, u, v))
                stats["units"] += 1; stats["inv" if inv else "noninv"] += 1
                if inv: inv_list.append([u, v])
        rows = []
        for kind, Ks in fam:
            if kind != "rand": continue
            cols = []
            for u in range(d):
                for v in range(d):
                    D = heis_unit(Ks, u, v, nb); D0 = heis_unit(dep, u, v, nb)
                    cols.append([D[a][c] - D0[a][c] for a in range(nb) for c in range(nb)])
            rows += [list(r) for r in zip(*cols)]
        kd = d * d - rank(rows)
        pl = []
        if BYSTANDER[ri]:
            Oz_l = list(Oz); ys = list(reg)
            for a in range(len(ys)):
                for c in range(len(ys)):
                    E = zeros(d, d)
                    for z in Oz_l: E[oi[(ys[a], z)]][oi[(ys[c], z)]] = G(1)
                    ref = heis(dep, E); inv = all(meq(heis(Ks, E), ref) for _, Ks in fam[1:])
                    ok(inv == (a == c), "19.4d r%d" % ri)
                    if inv: pl.append([a, c])
            plocal.append([len(ys) ** 2, len(pl)])
        dims.append(kd); units.append(d * d); pairs_l.append(npairs)
        out.append([inv_list, pl, npairs, kd])
    return {"digest": digest(out), "det_dim": dims, "units": units, "pair_ext": pairs_l, "plocal": plocal,
            "counts": stats}


def witness_19_6():
    B, fm, outs, oi = region((0, 1), (0, 1), (0,), (0, 1, 2)); nb = 4
    dep = ext_dephase(B, fm, oi)
    can = kraus_cols(B, fm, oi, {b: [G(1) if b[0] == k else G() for k in range(2)] for b in B}, 2)
    alt = kraus_cols(B, fm, oi, {b: [G(1) if b[1] == k else G() for k in range(2)] for b in B}, 2)

    def gram(Ks):
        cb = {b: [Ks[i][oi[fm[b]]][bi] for i in range(len(Ks))] for bi, b in enumerate(B)}
        return [[int(sum((cb[b][i] * cb[c][i].conj() for i in range(len(Ks))), G()).r) for c in B] for b in B]
    psi = [[1, 0, 1, 0], [1, 1, 0, 0]]
    sig, Nv, Qv = [], [], []
    for v in psi:
        rho = [[G(F(v[a] * v[c], 2)) for c in range(nb)] for a in range(nb)]
        row = []
        for Ks in (dep, can, alt):
            o = schr(Ks, rho); row.append(gstr(o[0][1] + o[1][0]))
            Nv.append(gstr(sum((o[k][k] * G(outs[k][0]) for k in range(3)), G())))
            Qv.append(gstr(o[1][1] + o[2][2]))
        sig.append(row)
    for Ks in (can, alt): ok(meq(heis(Ks, eye(3)), eye(4)), "19.6 TP")
    return {"X2.sigma": sig, "X2.N": Nv, "X2.Q": Qv, "X2.G_can": gram(can), "X2.G_alt": gram(alt)}, (dep, can, alt)


# ---------------- subsets, partitions, laws ----------------
def subsets(base):
    return [tuple(c) for r in range(1, len(base) + 1) for c in itertools.combinations(base, r)]


def partitions(s):
    s = list(s)
    if not s:
        yield []
        return
    first, rest = s[0], s[1:]
    for p in partitions(rest):
        for i in range(len(p)): yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def laws(n):
    seen = set()
    for w in itertools.product(range(3), repeat=n):
        if sum(w): seen.add(tuple(F(x, sum(w)) for x in w))
    return [dict((i, p) for i, p in enumerate(l) if p) for l in sorted(seen)]


def shift(l, gg): return {y + gg: p for y, p in l.items()}


def tv(a, b): return sum(abs(a.get(y, 0) - b.get(y, 0)) for y in set(a) | set(b)) / 2


def push(l, part): return [sum(l.get(y, 0) for y in blk) for blk in part]


def tvp(a, b, part): return sum(abs(x - y) for x, y in zip(push(a, part), push(b, part))) / 2


def unit_invariant(S, part):
    blk = {y: k for k, b in enumerate(part) for y in b}
    for y in S:
        for y2 in S:
            if y > 0 and y2 > 0 and blk[y] != blk[y2]: return False  # c = y2 / y > 0 maps y to y2
    return True


def cnu(l, gg): return max(sum(p for y, p in l.items() if t - gg < y <= t) for t in l)


def unit_free_contrast(plus, minus):
    reach = sorted(set(plus) | set(minus))
    return max(tvp(plus, minus, pt) for pt in partitions(reach) if unit_invariant(reach, pt))


def u19b():
    subs = subsets(range(4)); dec = []; inj_n = 0
    for A in subs:
        for Bq in subs:
            inj = len({a + b for a in A for b in Bq}) == len(A) * len(Bq)
            crit = not ({a - a2 for a in A for a2 in A} & {b - b2 for b in Bq for b2 in Bq}) - {0}
            ok(inj == crit, "19.1b"); dec.append([list(A), list(Bq), inj]); inj_n += inj
    return {"digest": digest(dec), "pairs": len(dec), "injective": inj_n, "noninjective": len(dec) - inj_n}


SW = [F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(3, 2)]


def prefix(w): return [sum(w[:j + 1]) for j in range(len(w))]


def u19c():
    dec = []; rt, e2rp, sig, nonneg, n = [], [], [], [], 0
    for k in range(1, 5):
        a = b = c = e = 0
        for w in itertools.product(SW, repeat=k):
            n += 1; ps = prefix(w); R = all(x == 1 for x in ps); e1 = list(w) == [1] + [0] * (k - 1)
            ok(R == e1, "19.8a"); E2Rp = w[0] == 1 and ps[-1] == 1
            nn = E2Rp and all(x >= 0 for x in w); ok(nn == e1, "19.8c")
            a += R; b += E2Rp; c += E2Rp and not R; e += nn; dec.append([R, E2Rp])
        rt.append(a); e2rp.append(b); sig.append(c); nonneg.append(e)
    return {"digest": digest(dec), "vectors": n, "R_true": rt, "E2Rp": e2rp, "E2Rp_notR": sig, "E2Rp_nonneg": nonneg}


def frank(rows):
    return rank([[G(x) for x in r] for r in rows])


def u20a():
    dec = []; npart = nfun = 0
    for S in subsets(range(5)):
        dims = []
        for pt in partitions(S):
            ind = [[1 if y in blk else 0 for y in S] for blk in pt]
            ok(sum(map(sum, ind)) == len(S), "20.1 cover")
            for a in ind:
                for b in ind:
                    pr = [x * y for x, y in zip(a, b)]
                    ok(frank(ind + [pr]) == len(ind), "20.1 closed")
            dims.append(frank(ind)); ok(dims[-1] == len(pt), "20.1 dim"); npart += 1
        gd = []
        for fv in itertools.product(range(3), repeat=len(S)):
            pw = [[F(x) ** e for x in fv] for e in range(len(S))]
            dm = frank(pw); nfun += 1
            ok(dm == len(set(fv)), "20.1 gen dim")
            for val in set(fv):
                ok(frank(pw + [[1 if x == val else 0 for x in fv]]) == dm, "20.1 level set in algebra")
            gd.append(dm)
        dec.append([len(dims), sorted(dims), gd])
    return {"digest": digest(dec), "subsets": 31, "partitions": npart, "functions": nfun}


def u20b():
    dec = []; tot = cov = strict = pos = 0
    for l in laws(3):
        for gg in (1, 2):
            plus, minus = shift(l, gg), l; reach = sorted(set(plus) | set(minus)); full = tv(plus, minus)
            ps = list(partitions(reach)); npos = nst = ncv = 0
            for pt in ps:
                c = tvp(plus, minus, pt); ok(c <= full, "20.2 <= full"); ok(c <= 1, "20.2 field")
                ok((c > 0) == any(sum(l.get(y, 0) for y in blk) != sum(l.get(y - gg, 0) for y in blk) for blk in pt), "20.2c")
                npos += c > 0
                for i, j in itertools.combinations(range(len(pt)), 2):
                    m = [b for k, b in enumerate(pt) if k not in (i, j)] + [pt[i] + pt[j]]
                    cm = tvp(plus, minus, m); ok(cm <= c, "20.2 monotone"); ncv += 1; nst += cm < c
            ok(tvp(plus, minus, [[y] for y in reach]) == full, "20.2 finest"); ok(tvp(plus, minus, [reach]) == 0, "20.2 trivial")
            tot += len(ps); cov += ncv; strict += nst; pos += npos
            dec.append([len(ps), npos, ncv, nst, frs(full)])
    return {"digest": digest(dec), "cases": len(dec), "partitions": tot, "covering": cov, "strict_decrease": strict,
            "positive": pos}


T = [F(0), F(1, 2), F(1), F(3, 2), F(2), F(3)]


def u20c():
    dec = []; npart = ninv = adm = 0
    for S in subsets(T):
        ps = list(partitions(S)); inv = [pt for pt in ps if unit_invariant(S, pt)]
        nontriv = [pt for pt in inv if len(pt) > 1]
        has0, haspos = 0 in S, any(y > 0 for y in S)
        ok((len(nontriv) > 0) == (has0 and haspos), "20.3a")
        ok(len(nontriv) <= 1, "20.3 unique")
        if nontriv: ok(sorted(map(sorted, nontriv[0])) == sorted([[F(0)], sorted(y for y in S if y > 0)]), "20.3 Q")
        npart += len(ps); ninv += len(inv); adm += bool(nontriv)
        dec.append([len(ps), len(inv), bool(nontriv)])
    return {"digest": digest(dec), "subsets": len(dec), "partitions": npart, "invariant": ninv, "admit_nontrivial": adm}


GS = [F(1, 2), F(1), F(2), F(3)]
AB = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]


def u20d():
    dec = []; tr = 0
    for l in laws(4):
        for gg in GS:
            plus, minus = shift(l, gg), l; reach = sorted(set(plus) | set(minus))
            q = tvp(plus, minus, [[y for y in reach if y == 0], [y for y in reach if y > 0]])
            full = tv(plus, minus); c = cnu(l, gg); z = l.get(0, F(0))
            ok(q == z, "20.4b contrast"); ok((q > 0) == (z > 0), "20.4b iff"); ok(q <= full, "20.4d"); ok(full >= c > 0, "18.2c")
            ok(unit_free_contrast(plus, minus) == q, "20.3 unit-free = Q"); tr += q > 0
            dec.append([frs(q), frs(full), frs(c), q > 0])
    return {"digest": digest(dec), "cases": len(dec), "transfers": tr, "nontransfers": len(dec) - tr}


def u20e():
    dec = []; tr = 0
    for a in AB:
        for b in AB:
            for l in laws(4):
                for gg in GS:
                    plus, minus = shift(l, gg), l
                    pp = sum(p * (a if y == 0 else b) for y, p in plus.items())
                    pm = sum(p * (a if y == 0 else b) for y, p in minus.items())
                    t = abs(pp - pm); z = l.get(0, F(0))
                    ok(t == abs(b - a) * z, "FU (3)"); ok((t > 0) == (a != b and z > 0), "FU (4)")
                    ok(pp == b and pm == a * z + b * (1 - z), "FU p"); tr += t > 0; dec.append(t > 0)
    return {"digest": digest(dec), "cases": len(dec), "transfers": tr, "nontransfers": len(dec) - tr}


def instances(w196):
    inst = {}
    pts = [(j, x) for j in (0, 1) for x in (0, 1)]
    inst["X1.inj_01_01"] = len({j + x for j, x in pts}) == 4
    inst["X1.collision"] = next([list(a), list(b)] for a, b in itertools.combinations(pts, 2) if sum(a) == sum(b))
    inst.update(w196)
    d1 = {1: F(1)}; inst["X4.a"] = [frs(tv(shift(d1, 1), d1)), frs(unit_free_contrast(shift(d1, 1), d1))]
    nb = {0: F(1, 2), 2: F(1, 2)}; pl, mi = shift(nb, 1), nb
    inst["X4.b"] = [frs(tv(pl, mi)), frs(tvp(pl, mi, [[0], [1, 2, 3]])), frs(tvp(pl, mi, [[0, 1], [2, 3]])),
                    frs(tvp(pl, mi, [[0, 2], [1, 3]])), frs(tvp(pl, mi, [[0, 1, 2, 3]]))]
    un = {0: F(1, 3), 1: F(1, 3), 2: F(1, 3)}
    inst["X4.c"] = [frs(tv(shift(un, 1), un)), frs(tvp(shift(un, 1), un, [[0], [1, 2, 3]]))]

    def resp(l, a, b): return sum(p * (a if y == 0 else b) for y, p in l.items())
    a, b = F(1, 4), F(3, 4)
    inst["X5.illus"] = [frs(resp(mi, a, b)), frs(resp(pl, a, b)), frs(abs(resp(pl, a, b) - resp(mi, a, b)))]
    inst["X5.controls"] = [frs(abs(resp(pl, F(1, 2), F(1, 2)) - resp(mi, F(1, 2), F(1, 2)))),
                           frs(abs(resp(shift(d1, 1), a, b) - resp(d1, a, b)))]
    inst["X5.vminusu"] = frs(1 / (b - a))
    vs = [(F(1), F(1), F(-1)), (F(0), F(0), F(1)), (F(0), F(1), F(0)), (F(1, 2), F(1, 2), F(0))]
    inst["X6.prefix"] = [[frs(x) for x in prefix(w)] for w in vs]
    inst["X6.rfail"] = [[j + 1 for j, x in enumerate(prefix(w)) if x != 1] for w in vs]
    # X7 Genesis dump on (o, l, p): f(xo, j, x) = (xo + j, x); output register (o', p')
    B = [(xo, j, x) for xo in (0,) for j in (0, 1) for x in (0, 1)]
    fm = {bb: (bb[0] + bb[1], bb[2]) for bb in B}; outs = [(o, p) for o in (0, 1) for p in (0, 1)]
    oi = {o: k for k, o in enumerate(outs)}
    fam, _ = family(B, fm, oi); dep = fam[0][1]; pinv = 0
    for y in (0, 1):
        for y2 in (0, 1):
            E = zeros(4, 4)
            for o in (0, 1): E[oi[(o, y)]][oi[(o, y2)]] = G(1)
            ref = heis(dep, E); inv = all(meq(heis(Ks, E), ref) for _, Ks in fam[1:]); pinv += inv
            ok(inv == (y == y2), "X7 plocal")
    mx = F(0)
    for l in laws(4):  # receiver p's law is the background law nu in both preparations (dump sends l's grade to o)
        mx = max(mx, tvp(l, l, [[0], [1, 2, 3]]))
    inst["X7.dump"] = [4, pinv, frs(mx)]
    return inst


def controls(inst, w):
    dep, can, alt = w
    c = {}
    c["R1_trivial_availability_transfers"] = any(tvp(shift(l, gg), l, [sorted(set(shift(l, gg)) | set(l))]) > 0
                                                for l in laws(4) for gg in GS)
    c["R2_genesis_dump_receiver_gains"] = inst["X7.dump"][2] != "0"
    B, fm, outs, oi = region((0, 1), (0, 1), (0,), (0, 1, 2)); fam, _ = family(B, fm, oi)
    sg = zeros(3, 3); sg[0][1] = G(1); sg[1][0] = G(1); ref = heis(fam[0][1], sg)
    c["R3_sigma_event_determined"] = all(meq(heis(Ks, sg), ref) for _, Ks in fam[1:])
    c["R4_canonical_extension_unique"] = inst["X2.sigma"][0][1] == inst["X2.sigma"][0][2] and inst["X2.sigma"][1][1] == inst["X2.sigma"][1][2]
    c["R5_addition_injective_01"] = inst["X1.inj_01_01"]
    c["R6_threshold_unit_invariant"] = unit_invariant([0, 1, 2, 3], [[0, 1], [2, 3]])
    c["R7_E2_Rp_imply_R_signed"] = all(x == 1 for x in prefix((F(1), F(1), F(-1))))
    grid = [F(k, 8) for k in range(9)]
    c["R8_relabel_sharpens_E"] = any(u + (v - u) * F(1, 4) == 0 and u + (v - u) * F(3, 4) == 1 for u in grid for v in grid)
    d1 = {1: F(1)}; c["R9_unit_free_transfers_without_empty"] = unit_free_contrast(shift(d1, 1), d1) > 0
    idinv = all(meq(heis(Ks, eye(3)), heis(fam[0][1], eye(3))) for _, Ks in fam[1:])  # C.1 is local (A1) and determined (A2)
    c["R10_A1_A2_force_full_access"] = not (idinv and inst["X3.det_dim"][0] != 1)  # yet dim C.1 = 1 != dim D_p
    return {k: ("ACCEPTED_WRONGLY" if v else "REJECTED") for k, v in c.items()}


def main():
    w196, w = witness_19_6()
    inst = instances(w196)
    uni = {"U19A": u19a(), "U19B": u19b(), "U19C": u19c(), "U20A": u20a(), "U20B": u20b(), "U20C": u20c(),
           "U20D": u20d(), "U20E": u20e()}
    inst["X3.units"] = uni["U19A"]["units"]; inst["X3.det_dim"] = uni["U19A"]["det_dim"]
    inst["X3.pair_ext"] = uni["U19A"]["pair_ext"]; inst["X3.plocal"] = uni["U19A"]["plocal"]
    cert = {"role": "producer", "result_sha256": RESULT_SHA, "instances": inst, "universes": uni,
            "controls": controls(inst, w), "violations": VIOL}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print("producer violations", len(VIOL))


if __name__ == "__main__":
    main()
