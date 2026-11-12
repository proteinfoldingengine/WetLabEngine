"""receiver_identification draft 12 (sec 18) freeze: CHECKER. Independent of the producer (imports nothing from it).
Bitmask carriers; integer-scaled numpy grade vectors and column-form ownership matrices; laws as integer numerators
over a per-law common denominator, enumerated by record-presence bitmasks; Kraus families from products of rational
Householder reflections as dense matrices. Also bounded evidence (FREEZE.md sec 4) and rejecting controls (sec 5)."""
import hashlib, itertools, json, math, sys
from fractions import Fraction as Fr
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d12_review")


def q2s(q):
    q = Fr(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def H(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def bits(m):
    return [i for i in range(m.bit_length()) if m >> i & 1]


def all_trees(nmax):
    res, stack = [], [(None,)]
    while stack:
        t = stack.pop()
        res.append(t)
        if len(t) < nmax:
            stack.extend(t + (q,) for q in range(len(t)))
    return res


def carrier_masks(par):
    n = len(par)
    return [m for m in range(1, 1 << n, 2) if all(not m >> i & 1 or m >> par[i] & 1 for i in range(1, n))]


def leaf_list(par, m):
    kids = 0
    for i in bits(m):
        if i:
            kids |= 1 << par[i]
    return [i for i in bits(m) if i and not kids >> i & 1]


def lp(par, k, ym):
    while not ym >> k & 1:
        k = par[k]
    return k


def P1(par, m, l):
    """0/1 matrix rows = addresses of m minus l, columns = addresses of m"""
    xs, ys = bits(m), bits(m & ~(1 << l))
    A = np.zeros((len(ys), len(xs)), dtype=np.int64)
    for c, u in enumerate(xs):
        A[ys.index(par[l] if u == l else u), c] = 1
    return A


def pstr(par):
    return "".join("-" if q is None else str(q) for q in par)


def mstr(m):
    return ",".join(map(str, bits(m)))


# ---------- U18A ----------
def u18a():
    L = 420
    out, lines, viol = dict(t=0, c=0, l=0, pr=0, o=0), [], 0
    for par in all_trees(6):
        out["t"] += 1
        cs = carrier_masks(par)
        out["c"] += len(cs)
        for m in cs:
            xs = bits(m)
            J = np.array([L * (u + 1) + L // (u + 2) for u in xs], dtype=np.int64)
            recs = [(u, L * (u + 1)) for u in xs] + [(u, L // (u + 2)) for u in xs]
            for l in leaf_list(par, m):
                out["l"] += 1
                ym = m & ~(1 << l)
                ys = bits(ym)
                pf = np.zeros(len(ys), dtype=np.int64)
                mv = 0
                for k, g in recs:
                    r = lp(par, k, ym)
                    pf[ys.index(r)] += g
                    if r != k:
                        mv += 1
                        viol += not (k == l and r == par[l])
                viol += mv != 2
                viol += not np.array_equal(pf, P1(par, m, l) @ J)
                lines.append("%s|%s|%d|%s" % (pstr(par), mstr(m), l, ",".join(q2s(Fr(int(v), L)) for v in pf)))
            for ym in cs:
                if ym != m and ym & m == ym:
                    out["pr"] += 1
                    ys = bits(ym)
                    tgt = np.zeros(len(ys), dtype=np.int64)
                    for k, g in recs:
                        tgt[ys.index(lp(par, k, ym))] += g
                    stack, n_ord = [(m, J)], 0
                    while stack:
                        z, v = stack.pop()
                        if z == ym:
                            n_ord += 1
                            viol += not np.array_equal(v, tgt)
                            continue
                        for l in leaf_list(par, z):
                            if not ym >> l & 1:
                                stack.append((z & ~(1 << l), P1(par, z, l) @ v))
                    out["o"] += n_ord
                    lines.append("%s|%s|%s|%s|%d" % (pstr(par), mstr(m), mstr(ym),
                                                     ",".join(q2s(Fr(int(v), L)) for v in tgt), n_ord))
    return {"u18a_trees": out["t"], "u18a_carriers": out["c"], "u18a_leaf": out["l"], "u18a_pairs": out["pr"],
            "u18a_orders": out["o"], "u18a_digest": H(lines), "u18a_viol": viol}


# ---------- U18B ----------
T5 = (None, 0, 1, 1, 0)
# grades scaled by 2: r1=(1@1) r2=(2@2) r3=(1/2@3) r4=(1@4) r5=(1@0)
REC = [(1, 2), (2, 4), (3, 1), (4, 2), (0, 2)]


def laws_b():
    out = []
    code = {0: "0", 2: "t", 3: "h"}  # q*6
    for qs in itertools.product((0, 2, 3), repeat=5):
        w = {}
        for mask in range(32):
            num = 1
            for i in range(5):
                num *= qs[i] if mask >> i & 1 else 6 - qs[i]
            if num:
                w[mask] = num
        out.append(("prod", "".join(code[q] for q in qs), w, 6 ** 5))
    atoms = [0, 0b00011, 0b00010, 0b01000, 0b10101]
    for wt in itertools.product((0, 1, 2), repeat=5):
        if math.gcd(*wt) != 1:
            continue
        w = {}
        for a, x in zip(atoms, wt):
            if x:
                w[a] = w.get(a, 0) + x
        out.append(("corr", "".join(map(str, wt)), w, sum(wt)))
    return out


def dist(w, den, fn):
    d = {}
    for mask, num in w.items():
        k = fn(mask)
        d[k] = d.get(k, 0) + num
    return d


def tvi(a, b, den):
    return Fr(sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b)), 2 * den)


def vec_before(mask, D):
    v = [0] * 5
    for i in range(5):
        if mask >> i & 1:
            v[REC[i][0]] += REC[i][1]
    for a, g in D:
        v[a] += g
    return tuple(v)


def vec_after(vb, l):
    v = list(vb)
    v[T5[l]] += v[l]
    del v[l]
    return tuple(v)


def product_ok(d, den, dim):
    marg = [{} for _ in range(dim)]
    for k, w in d.items():
        for i in range(dim):
            marg[i][k[i]] = marg[i].get(k[i], 0) + w
    for k in itertools.product(*[list(mm) for mm in marg]):
        lhs = d.get(k, 0) * den ** (dim - 1)
        rhs = 1
        for i in range(dim):
            rhs *= marg[i][k[i]]
        if lhs != rhs:
            return False
    return True


CAT = [()] + [((a, 2 * g),) for g in (1, 2) for a in range(5)]


def cstr(D):
    return "-" if not D else "%s@%d" % (q2s(Fr(D[0][1], 2)), D[0][0])


def u18b():
    lines, viol = [], 0
    cb, csp = [0] * 4, [0] * 4
    c = dict(cases=0, transfer=0, oneloc=0, multi=0, adv=0, beq=0, bgt=0, pf=0, pt=0)
    LB = laws_b()
    for l in (2, 3, 4):
        p = T5[l]
        ipa = [a for a in range(5) if a != l].index(p)
        for cls, lid, w, den in LB:
            pres = lambda mask: [i for i in range(5) if mask >> i & 1]
            mu = dist(w, den, lambda m: sum(REC[i][1] for i in pres(m) if REC[i][0] == p))
            nu = dist(w, den, lambda m: sum(REC[i][1] for i in pres(m) if REC[i][0] in (p, l)))
            bga = dist(w, den, lambda m: vec_after(vec_before(m, ()), l))
            fpr = product_ok(bga, den, 4)
            if cls == "prod":
                c["pt"] += 1
                c["pf"] += fpr
            multi = any(sum(1 for i in pres(m) if REC[i][0] in (p, l)) >= 2 for m in w)
            mx = Fr(max(nu.values()), den)
            for Dp in CAT:
                for Dm in CAT:
                    if Dp == Dm:
                        continue
                    c["cases"] += 1
                    fb = [dist(w, den, lambda m, D=D: vec_before(m, D)) for D in (Dp, Dm)]
                    fa = [dist(w, den, lambda m, D=D: vec_after(vec_before(m, D), l)) for D in (Dp, Dm)]
                    rb = [dist(w, den, lambda m, D=D: vec_before(m, D)[p]) for D in (Dp, Dm)]
                    ra = [dist(w, den, lambda m, D=D: vec_after(vec_before(m, D), l)[ipa]) for D in (Dp, Dm)]
                    for D, b_, a_ in zip((Dp, Dm), rb, ra):
                        sp = sum(g for a, g in D if a == p)
                        spl = sum(g for a, g in D if a in (p, l))
                        viol += b_ != {k + sp: v for k, v in mu.items()}
                        viol += a_ != {k + spl: v for k, v in nu.items()}
                    blind, sep = rb[0] == rb[1], ra[0] != ra[1]
                    db = sum(g for a, g in Dp if a == p) == sum(g for a, g in Dm if a == p)
                    ds = sum(g for a, g in Dp if a in (p, l)) != sum(g for a, g in Dm if a in (p, l))
                    cb[2 * (not blind) + (not db)] += 1
                    csp[2 * (not sep) + (not ds)] += 1
                    c["transfer"] += blind and sep
                    t, tj, tf = tvi(ra[0], ra[1], den), tvi(fa[0], fa[1], den), tvi(fb[0], fb[1], den)
                    qa = [{1: sum(v for k, v in r.items() if k > 0), 0: r.get(0, 0)} for r in ra]
                    tq = tvi(qa[0], qa[1], den)
                    if sep:
                        viol += not (t >= mx and mx > 0)
                        c["beq"] += t == mx
                        c["bgt"] += t > mx
                    viol += not (t <= tj and tj <= tf)
                    viol += tq > t
                    if Dm == () and Dp and Dp[0][0] == l:
                        c["oneloc"] += 1
                        viol += tq != Fr(nu.get(0, 0), den)
                        if fpr:
                            viol += tj != t
                        c["multi"] += multi
                        c["adv"] += cls == "corr" and tj > t
                    lines.append("|".join([str(l), cls, lid, cstr(Dp), cstr(Dm), str(int(blind)), str(int(sep)),
                                           q2s(t), q2s(tj), q2s(tf), q2s(mx), q2s(tq)]))
    return {"u18b_cases": c["cases"], "u18b_conf_blind": cb, "u18b_conf_sep": csp, "u18b_digest": H(lines),
            "u18b_laws": len(LB), "u18b_nv_bound_eq": c["beq"], "u18b_nv_bound_gt": c["bgt"],
            "u18b_nv_corr_adv": c["adv"], "u18b_nv_multi": c["multi"], "u18b_oneloc": c["oneloc"],
            "u18b_prodclass_fiberprod": c["pf"], "u18b_prodclass_total": c["pt"], "u18b_transfer": c["transfer"],
            "u18b_viol": viol}


# ---------- U18C ----------
U17A = (None, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6)
U17B = (None, 0, 0, 0, 1, 1, 1, 2, 2, 4, 7)
SC = 232792560  # lcm(1..20)
NAMES = ["own", "gtax", "mixed", "root", "field", "parent", "uniform", "pert", "rand"]


def chain(par, u):
    c = []
    while u is not None:
        c.append(u)
        u = par[u]
    return c  # u ... 0


def col_scaled(par, name, u):
    """dict v -> integer share scaled by SC"""
    if u == 0:
        return {0: SC}
    ch = chain(par, u)  # u, par(u), ..., 0
    d = len(ch) - 1
    if name in ("own", "field"):
        return {u: SC}
    if name == "parent":
        return {par[u]: SC}
    if name == "uniform":
        return {v: SC // len(ch) for v in ch}
    if name == "pert":
        return {7: SC // 2, 0: SC // 2} if u == 7 else {u: SC}
    if name == "rand":
        ws = {v: 1 + (5 * u + 3 * v) % 4 for v in ch}
        s = sum(ws.values())
        return {v: SC * x // s for v, x in ws.items()}
    # 17.1 family: share b(w) of column u to par(w) for each w on the chain below u's ancestors
    depth = {w: len(chain(par, w)) - 1 for w in ch}
    if name == "gtax":
        b = {w: SC // 2 if depth[w] == 1 else 0 for w in ch if w}
    elif name == "root":
        b = {w: SC if depth[w] == 1 else 0 for w in ch if w}
    else:
        b = {w: SC * ((3 * w + 1) % 5) // 20 for w in ch if w}
    col = {}
    for w, x in b.items():
        col[par[w]] = col.get(par[w], 0) + x
    col[u] = col.get(u, 0) + SC - sum(b.values())
    return col


def matrix(par, name, m):
    xs = bits(m)
    M = np.zeros((len(xs), len(xs)), dtype=np.int64)
    for c, u in enumerate(xs):
        for v, x in col_scaled(par, name, u).items():
            M[xs.index(v), c] += x
    return M


def u18c():
    lines, viol, tr, acq = [], 0, {}, {}
    for un, par in (("U17A", U17A), ("U17B", U17B)):
        cs = carrier_masks(par)
        tr[un] = {}
        for name in NAMES:
            Ms = {m: matrix(par, name, m) for m in cs}
            for m in cs:
                M = Ms[m]
                viol += not ((M.sum(axis=0) == SC).all() and (M >= 0).all())
                for w in range(1, len(par)):
                    if not m >> w & 1 and m >> par[w] & 1:
                        m2 = m | 1 << w
                        xs2 = bits(m2)
                        idx = [xs2.index(u) for u in bits(m)]
                        M2 = Ms[m2]
                        viol += not (np.array_equal(M2[np.ix_(idx, idx)], M) and (M2[xs2.index(w), idx] == 0).all())
            t, allw4, uacq = 0, True, True
            for m in cs:
                xs = bits(m)
                for l in leaf_list(par, m):
                    p = par[l]
                    ym = m & ~(1 << l)
                    ys = bits(ym)
                    Pm = P1(par, m, l)
                    I = np.zeros((len(xs), len(ys)), dtype=np.int64)
                    for c, u in enumerate(ys):
                        I[xs.index(u), c] = 1
                    viol += not np.array_equal(Pm @ I, np.eye(len(ys), dtype=np.int64))
                    MX, MY = Ms[m], Ms[ym]
                    A, B = MY @ Pm, Pm @ MX
                    rows_np = [ys.index(v) for v in ys if v != p]
                    rows_x = [xs.index(v) for v in ys if v != p]
                    c1 = np.array_equal(A[rows_np, :], MX[rows_x, :])
                    c2 = np.array_equal(A, B)
                    dvec = MX[:, xs.index(l)] - MX[:, xs.index(p)]
                    others = [i for i, a in enumerate(xs) if a not in (l, p)]
                    c3 = bool((dvec[others] == 0).all() and dvec[xs.index(l)] == -dvec[xs.index(p)])
                    anc = chain(par, p)[1:]
                    c4 = all(MX[xs.index(v), xs.index(l)] == MX[xs.index(v), xs.index(p)] for v in anc)
                    viol += not (c1 == c2 == c3 == c4)
                    if name == "field":
                        g = np.array([2 * u + 3 for u in xs], dtype=np.int64)
                        pushed = np.zeros(len(ys), dtype=np.int64)
                        for u, x in zip(xs, g):
                            pushed[ys.index(lp(par, u, ym))] += x
                        viol += not np.array_equal(pushed, Pm @ g)
                    t += c1
                    allw4 &= c1
                    uacq &= MX[xs.index(p), xs.index(l)] == 0 and A[ys.index(p), xs.index(l)] != 0
                    lines.append("%s|%s|%s|%d|%d|%d|%d|%d" % (un, name, mstr(m), l, c1, c2, c3, c4))
            tr[un][name] = t
            if allw4:
                acq[un + "." + name] = bool(uacq)
    return {"u18c_true": tr, "u18c_acq": acq, "u18c_digest": H(lines), "u18c_lines": len(lines), "u18c_viol": viol}


# ---------- U18D ----------
def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Fr(0)) for j in range(len(B[0]))] for i in range(len(A))]


def tr_(A):
    return [list(r) for r in zip(*A)]


def eye(n):
    return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]


def householder_orth(r, seed):
    Q = eye(r)
    for t in range(2):
        v = [Fr(((seed + 1) * (i + 2) + 3 * t) % 5 - 2 + (1 if i == t else 0)) for i in range(r)]
        if all(x == 0 for x in v):
            v[0] = Fr(1)
        vv = sum(x * x for x in v)
        Hm = [[Fr(int(i == j)) - 2 * v[i] * v[j] / vv for j in range(r)] for i in range(r)]
        Q = mm(Q, Hm)
    return Q


def frank(A):
    M = [list(r) for r in A]
    rk = 0
    for c in range(len(M[0])):
        pv = None
        for r in range(rk, len(M)):
            if M[r][c] != 0:
                pv = r
                break
        if pv is None:
            continue
        M[rk], M[pv] = M[pv], M[rk]
        for r in range(rk + 1, len(M)):
            f = M[r][c] / M[rk][c]
            if f:
                M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk


def channel(Ks, rho):
    out = None
    for K in Ks:
        t = mm(mm(K, rho), tr_(K))
        out = t if out is None else [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(out, t)]
    return out


def u18d_families():
    for dl, dp in ((2, 2), (2, 3), (3, 2), (3, 3)):
        m = min(dl, dp)
        for r in (m, m + 1):
            for seed in range(3):
                yield dl, dp, m, r, seed


def build(dl, dp, r, seed):
    no, B = dl + dp - 1, [(j, x) for j in range(dl) for x in range(dp)]
    Ks = [[[Fr(0)] * len(B) for _ in range(no)] for _ in range(r)]
    for n in range(no):
        fib = [i for i, b in enumerate(B) if sum(b) == n]
        Q = householder_orth(r, seed + 7 * n)
        for c, bi in enumerate(fib):
            for i in range(r):
                Ks[i][n][bi] = Q[i][c]
    return Ks, B, no


def u18d():
    lines, viol, fam, ops, ncl, nco = [], 0, 0, 0, 0, 0
    for dl, dp, m, r, seed in u18d_families():
        Ks, B, no = build(dl, dp, r, seed)
        fam += 1
        ops += len(Ks)
        Nin = [[Fr(sum(B[i])) if i == j else Fr(0) for j in range(len(B))] for i in range(len(B))]
        Nout = [[Fr(i) if i == j else Fr(0) for j in range(no)] for i in range(no)]
        S = None
        for K in Ks:
            t = mm(tr_(K), K)
            S = t if S is None else [[a + b for a, b in zip(x, y)] for x, y in zip(S, t)]
        tp = S == eye(len(B))
        inter = all(mm(Nout, K) == mm(K, Nin) for K in Ks)
        cl = True
        for i, b in enumerate(B):
            ncl += 1
            rho = [[Fr(int(a == i and c == i)) for c in range(len(B))] for a in range(len(B))]
            o = channel(Ks, rho)
            cl &= o == [[Fr(int(a == sum(b) and c == sum(b))) for c in range(no)] for a in range(no)]
        rk = frank([[K[o][bi] for o in range(no) for bi in range(len(B))] for K in Ks])
        viol += not (tp and inter and cl and rk >= m)
        lines.append("%d|%d|%d|%d|%d|%d|%d|%d" % (dl, dp, r, seed, tp, inter, cl, rk >= m))
        for n in range(no):
            fib = [i for i, b in enumerate(B) if sum(b) == n]
            if len(fib) < 2:
                continue
            for sgn in (0, 1):
                nco += 1
                psi = [Fr(0)] * len(B)
                for k, bi in enumerate(fib):
                    psi[bi] = Fr(-1 if sgn and k % 2 else 1)
                nn = sum(x * x for x in psi)
                rho = [[psi[a] * psi[c] / nn for c in range(len(B))] for a in range(len(B))]
                o = channel(Ks, rho)
                pure = o == [[Fr(int(a == n and c == n)) for c in range(no)] for a in range(no)]
                trq = sum((o[a][a] for a in range(1, no)), Fr(0))
                viol += not (pure and trq == int(n > 0))
                lines.append("%d|%d|%d|%d|%d|%d|%d|%s" % (dl, dp, r, seed, n, len(fib), pure, q2s(trq)))
    return {"u18d_families": fam, "u18d_ops": ops, "u18d_classical": ncl, "u18d_coherent": nco, "u18d_digest": H(lines),
            "u18d_viol": viol}


# ---------- exact instances (independent recomputation on T4; values in Fractions) ----------
def lawlist(d, den, scale=1):
    return [[q2s(Fr(k, scale)), q2s(Fr(v, den))] for k, v in sorted(d.items()) if v]


def t4_case(recs, w, den, Dp, Dm):
    """recs: list of (addr, grade int); w: dict presence-mask -> numerator. T4: 0,1,2,3; prune 2 into 1."""
    def vb(mask, D):
        v = [0, 0, 0, 0]
        for i, (a, g) in enumerate(recs):
            if mask >> i & 1:
                v[a] += g
        for a, g in D:
            v[a] += g
        return tuple(v)

    def va(v):
        return (v[0], v[1] + v[2], v[3])
    fb = [dist(w, den, lambda m, D=D: vb(m, D)) for D in (Dp, Dm)]
    fa = [dist(w, den, lambda m, D=D: va(vb(m, D))) for D in (Dp, Dm)]
    rb = [dist(w, den, lambda m, D=D: vb(m, D)[1]) for D in (Dp, Dm)]
    ra = [dist(w, den, lambda m, D=D: va(vb(m, D))[1]) for D in (Dp, Dm)]
    nu = dist(w, den, lambda m: vb(m, ())[1] + vb(m, ())[2])
    qa = [{1: sum(v for k, v in r.items() if k > 0), 0: r.get(0, 0)} for r in ra]
    bga = dist(w, den, lambda m: va(vb(m, ())))
    return dict(fb=fb, fa=fa, rb=rb, ra=ra, nu=nu, tv=tvi(ra[0], ra[1], den), tj=tvi(fa[0], fa[1], den),
                tf=tvi(fb[0], fb[1], den), tq=tvi(qa[0], qa[1], den), blind=rb[0] == rb[1], sep=ra[0] != ra[1],
                mx=Fr(max(nu.values()), den), fprod=product_ok(bga, den, 3), den=den)


def nonincr_class(nu, den, g):
    pts = {Fr(k): Fr(v, den) for k, v in nu.items() if v}
    if any((k / g).denominator != 1 for k in pts):
        return False
    seq = [pts.get(j * g, Fr(0)) for j in range(int(max(pts) / g) + 2)]
    return all(x >= y for x, y in zip(seq, seq[1:]))


def instances():
    V = {}
    # (a): b1 grade 1 at p w.p. 1/2 ; b2 grade 2 at l w.p. 1/3 -> presence numerators over 6
    w = {0: 2, 1: 2, 2: 1, 3: 1}
    a = t4_case([(1, 1), (2, 2)], w, 6, [(2, 1)], [])
    V["Y1.mu_plus"], V["Y1.mu_minus"] = lawlist(a["rb"][0], 6), lawlist(a["rb"][1], 6)
    V["Y1.nu"], V["Y1.after_plus"] = lawlist(a["nu"], 6), lawlist(a["ra"][0], 6)
    V["Y1.blind"], V["Y1.sep"] = a["blind"], a["sep"]
    V["Y1.tv"], V["Y1.maxnu"], V["Y1.tvq"] = q2s(a["tv"]), q2s(a["mx"]), q2s(a["tq"])
    V["Y1.tv_joint"], V["Y1.tv_full"] = q2s(a["tj"]), q2s(a["tf"])
    V["Y1.eqclass"] = nonincr_class(a["nu"], 6, Fr(1))
    b = t4_case([(1, 1), (2, 2)], w, 6, [(2, 2)], [])
    V["Y2.tv"], V["Y2.tvq"], V["Y2.tv_joint"], V["Y2.tv_full"] = q2s(b["tv"]), q2s(b["tq"]), q2s(b["tj"]), q2s(b["tf"])
    V["Y2.eqclass"] = nonincr_class(b["nu"], 6, Fr(2))
    c = t4_case([(2, 1), (3, 1)], {1: 1, 2: 1}, 2, [(2, 1)], [])
    V["Y3.after_plus"], V["Y3.after_minus"] = lawlist(c["ra"][0], 2), lawlist(c["ra"][1], 2)
    V["Y3.blind"], V["Y3.tv"], V["Y3.maxnu"] = c["blind"], q2s(c["tv"]), q2s(c["mx"])
    V["Y3.tv_joint"], V["Y3.tv_full"], V["Y3.tvq"], V["Y3.fiber_product"] = q2s(c["tj"]), q2s(c["tf"]), q2s(c["tq"]), c["fprod"]
    d = t4_case([], {0: 1}, 1, [(2, 1)], [(3, 1)])
    pb = [list(f)[0] for f in d["fb"]]
    pa = [list(f)[0] for f in d["fa"]]
    V["Y4.p_before"] = [str(pb[0][1]), str(pb[1][1])]
    V["Y4.v_before"] = [str(pb[0][3]), str(pb[1][3])]
    V["Y4.p_after"] = [str(pa[0][1]), str(pa[1][1])]
    V["Y4.tv"], V["Y4.tvq"], V["Y4.tv_full"], V["Y4.blind"] = q2s(d["tv"]), q2s(d["tq"]), q2s(d["tf"]), d["blind"]
    e = t4_case([(1, 1)], {0: 1, 1: 3}, 4, [(2, 1)], [])
    V["Y5.nu"], V["Y5.tv"], V["Y5.tvq"], V["Y5.maxnu"] = lawlist(e["nu"], 4), q2s(e["tv"]), q2s(e["tq"]), q2s(e["mx"])
    V["Y5.eqclass"] = nonincr_class(e["nu"], 4, Fr(1))
    # Y6: dense matrices, columns 00,01,10,11
    K0 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    K1 = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    Ks = [np.array(K0, dtype=np.int64), np.array(K1, dtype=np.int64)]
    V["Y6.K0"], V["Y6.K1"] = [[[str(x) for x in r] for r in K] for K in (K0, K1)]
    V["Y6.tp"] = bool(np.array_equal(sum(K.T @ K for K in Ks), np.eye(4, dtype=np.int64)))
    Nin, Nout = np.diag([0, 1, 1, 2]), np.diag([0, 1, 2])
    V["Y6.intertwine"] = [bool(np.array_equal(Nout @ K, K @ Nin)) for K in Ks]
    psi = np.array([0, 1, 1, 0], dtype=np.int64)  # norm^2 2
    rho = sum(np.outer(K @ psi, K @ psi) for K in Ks)
    V["Y6.out_psi"] = [q2s(Fr(int(rho[i, i]), 2)) for i in range(3)]
    viol_off = int(np.count_nonzero(rho - np.diag(np.diag(rho))))
    assert viol_off == 0
    V["Y6.branch"] = [q2s(Fr(int((K @ psi) @ (K @ psi)), 2)) for K in Ks]
    V["Y6.rank"] = int(np.linalg.matrix_rank(np.stack([K.ravel() for K in Ks]).astype(float)))
    V["Y6.maxfiber"] = max([0, 1, 1, 2].count(n) for n in range(3))
    fams = [[(2, 1), (1, 2)], [(2, 2), (1, 1)], [(2, 3)]]
    vals, comps = [], set()
    for S in fams:
        y = np.zeros(3, dtype=np.int64)
        for k, g in S:
            y[[0, 1, 1, 2][k]] += g
        vals.append(str(int(y[1])))
        comps.add(frozenset((k, g) for k, g in S if k in (1, 2)))
    V["Y7.values"], V["Y7.components"] = vals, len(comps)
    par = (None, 0, 1, 0)
    xv = np.array([3, 5, 7, 2], dtype=np.int64)
    Pm = P1(par, 0b1111, 2)
    for name in ("own", "gtax", "parent"):
        MX, MY = matrix(par, name, 0b1111), matrix(par, name, 0b1011)
        hx, hy, pw = MX @ xv, MY @ (Pm @ xv), Pm @ (MX @ xv)
        dv = MX[:, 2] - MX[:, 1]
        sv = lambda arr: [q2s(Fr(int(z), SC)) for z in arr]
        V["Y8." + name] = [sv(hx), sv(hy), sv(pw), bool(np.array_equal(MY @ Pm, Pm @ MX)), sv(dv)]
    MP = matrix(par, "parent", 0b1111)
    V["Y8.parent_iv"] = [q2s(Fr(int(MP[0, 2]), SC)), q2s(Fr(int(MP[0, 1]), SC))]
    forced = Pm @ xv
    Dm = np.zeros((3, 4), dtype=np.int64)
    Dm[0, 0] = Dm[0, 2] = Dm[1, 1] = Dm[2, 3] = 1
    dump = Dm @ xv
    keep = np.array([3, 5, 2])
    V["Y9.forced"], V["Y9.dump"] = [str(int(z)) for z in forced], [str(int(z)) for z in dump]
    V["Y9.totals"] = [str(int(xv.sum())), str(int(forced.sum())), str(int(dump.sum()))]
    V["Y9.changed"] = [[0, 1, 3][int(np.flatnonzero(forced != keep)[0])], [0, 1, 3][int(np.flatnonzero(dump != keep)[0])]]
    reg = []
    for xo, xl, xp in ((0, 1, 0), (0, 0, 1)):
        reg.append([int(xl + xp > 0), int(xp > 0)])
    V["Y9.region"] = reg
    G = [Fr(0), Fr(1, 2), Fr(1), Fr(2)]
    links = [(i, j) for i, y in enumerate(G) for j, z in enumerate(G) if any(c * y == z for c in (Fr(2), Fr(1, 2)))]
    ninv = nform = 0
    for f in itertools.product(range(3), repeat=4):
        if all(f[i] == f[j] for i, j in links):
            ninv += 1
            nform += f[1] == f[2] == f[3]
    V["Y10.invariant"] = [ninv, nform]
    return V


# ---------- bounded ----------
def bounded():
    B = dict(B18a_cases=0, B18a_class_true=0, B18a_class_false=0, B18a_eq_match=0, B18a_tvq_nu0=0, B18a_tvq_one=0,
             B18a_tvq_one_delta0=0, B18a_e_checks=0, B18a_e_equal=0, B18a_tvq_lt_tv=0)
    gs = [Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
    for h in (Fr(1, 2), Fr(1)):
        for wv in itertools.product(range(4), repeat=4):
            if not any(wv) or math.gcd(*wv) != 1:
                continue
            s = sum(wv)
            nu = {j * h: Fr(x, s) for j, x in enumerate(wv) if x}
            for g in gs:
                B["B18a_cases"] += 1
                sh = {k + g: v for k, v in nu.items()}
                t = sum(abs(nu.get(k, 0) - sh.get(k, 0)) for k in set(nu) | set(sh)) / 2
                tq = 1 - sum(v for k, v in nu.items() if k > 0)  # Q laws: + is 1 a.s.; - is 1 w.p. 1 - nu(0)
                B["B18a_tvq_nu0"] += tq == nu.get(Fr(0), 0)
                cls = nonincr_class({k: v * s for k, v in nu.items()}, s, g)
                B["B18a_class_true" if cls else "B18a_class_false"] += 1
                B["B18a_eq_match"] += (tq == t) == cls
                B["B18a_tvq_lt_tv"] += tq < t
                if tq == 1:
                    B["B18a_tvq_one"] += 1
                    B["B18a_tvq_one_delta0"] += nu == {Fr(0): Fr(1)}
            for g in gs:
                for g2 in gs:
                    if g != g2:
                        B["B18a_e_checks"] += 1
                        q1 = sum(v for k, v in nu.items() if k + g > 0)
                        q2 = sum(v for k, v in nu.items() if k + g2 > 0)
                        B["B18a_e_equal"] += q1 == q2 == 1
    b18b = []
    for par in (U17A, U17B):
        cnt = 0
        for m in carrier_masks(par):
            xs = bits(m)
            for l in leaf_list(par, m):
                p = par[l]
                if p == 0:
                    continue
                x = np.ones(len(xs), dtype=np.int64)
                x[xs.index(l)] += 1
                ys = bits(m & ~(1 << l))
                keep = np.array([x[xs.index(u)] for u in ys])
                f = P1(par, m, l) @ x
                d = keep.copy()
                d[ys.index(0)] += x[xs.index(l)]
                cf, cd = np.flatnonzero(f != keep), np.flatnonzero(d != keep)
                cnt += (f.sum() == x.sum() == d.sum() and len(cf) == 1 and len(cd) == 1 and ys[cf[0]] == p
                        and ys[cd[0]] == 0)
        b18b.append(int(cnt))
    B["B18b"] = b18b
    return B


def controls(V, U, B):
    R = {}
    rej = lambda c: "REJECTED" if c else "ACCEPTED"
    R["R1_sufficiency_every_background"] = rej(Fr(V["Y3.tv_joint"]) > Fr(V["Y3.tv"]) and U["u18b_nv_corr_adv"] > 0)
    R["R2_Q_as_informative_as_coordinate"] = rej(Fr(V["Y2.tvq"]) < Fr(V["Y2.tv"]) and Fr(V["Y5.tvq"]) < Fr(V["Y5.tv"])
                                                 and B["B18a_tvq_lt_tv"] == 2174)
    R["R3_Q_distinguishes_amounts"] = rej(B["B18a_e_equal"] == B["B18a_e_checks"] == 9000)
    R["R4_conservation_selects_receiver"] = rej(V["Y9.totals"] == ["17", "17", "17"] and V["Y9.changed"] == [1, 0]
                                                and V["Y9.region"][0][0] != V["Y9.region"][0][1] and B["B18b"] == [2600, 462])
    t = U["u18c_true"]
    R["R5_W1_W2_grade_facts_imply_W4"] = rej(U["u18c_viol"] == 0 and all(t[u][a] < tot for u, tot in (("U17A", 2652), ("U17B", 593))
                                                                          for a in ("parent", "uniform")))
    R["R6_W4_implies_acquisition"] = rej(all(U["u18c_acq"].get(u + "." + a) is False for u in ("U17A", "U17B")
                                             for a in ("root", "gtax")))
    R["R7_receiver_keeps_source_identity"] = rej(len(set(V["Y7.values"])) == 1 and V["Y7.components"] == 3)
    R["R8_receiver_blind_for_every_pair"] = rej(U["u18b_conf_blind"][3] > 0)
    R["R9_retained_side_initially_blind"] = rej(V["Y4.v_before"][0] != V["Y4.v_before"][1] and V["Y4.tv_full"] == "1")
    # R10: drop and leak operator families on dl = dp = 2
    Bs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    drop = [np.array([[1 if (j == jj and x == o) else 0 for (jj, x) in Bs] for o in range(3)]) for j in range(2)]
    leak = [np.array([[1 if o in (j + x, j + x + 1) else 0 for (j, x) in Bs] for o in range(4)])]
    ok = True
    for Ks, no in ((drop, 3), (leak, 4)):
        Nin, Nout = np.diag([sum(b) for b in Bs]), np.diag(list(range(no)))
        inter = all(np.array_equal(Nout @ K, K @ Nin) for K in Ks)
        agree = all(np.array_equal(sum(np.outer(K[:, i], K[:, i]) for K in Ks),
                                   np.diag([int(o == sum(b)) for o in range(no)])) for i, b in enumerate(Bs))
        ok &= not inter and not agree
    R["R10_leaky_family_agrees_with_forced_step"] = rej(ok)
    return R


def main():
    result_sha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    U = {}
    for fn in (u18a, u18b, u18c, u18d):
        U.update(fn())
    V = instances()
    B = bounded()
    cert = {"meta": {"role": "checker", "result_sha256": result_sha}, "values": V, "universe": U, "bounded": B,
            "controls": controls(V, U, B)}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("universe", "bounded", "controls")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
