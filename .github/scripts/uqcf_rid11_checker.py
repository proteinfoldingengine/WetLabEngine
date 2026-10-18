"""receiver_identification draft 11 (sec 17) freeze: CHECKER. Independent of the producer (does not import it):
carriers as bitmasks filtered by the prefix condition, holdings built in COLUMN form (column u puts a(u) on u and b(w)
on par(w) for each o < w <= u), integer-scaled numpy matrices (scale 60, normalized to reduced fractions only for
output), W4 as the matrix identity M^Y P = M^X on non-receiver rows, Theorem 17.1 dimensions by rank modulo the prime
2147483647 of independently generated constraints (W2 on ALL nested carrier pairs), exact integer check of the family
vectors. Also bounded grid evidence B17a and rejecting controls R1-R10 (FREEZE.md sections 2-5)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d11_review")
PR = 2147483647
L = 60
S = lambda q: str(F(q))


class Tree:
    def __init__(self, par):
        self.par, self.n = list(par), len(par)
        self.anc = []                     # bitmask of prefixes (including self)
        self.dep = []
        for v in range(self.n):
            m, d, w = 1 << v, 0, v
            while w != 0:
                w = self.par[w]; m |= 1 << w; d += 1
            self.anc.append(m); self.dep.append(d)
        self.carriers = [m for m in range(1, 1 << self.n, 2)
                         if all(not (m >> i) & 1 or (m >> self.par[i]) & 1 for i in range(1, self.n))]
        self.carriers.sort(key=lambda m: (bin(m).count("1"), [i for i in range(self.n) if m >> i & 1]))

    def le(self, a, v):
        return bool(self.anc[v] >> a & 1)

    def mem(self, m):
        return [i for i in range(self.n) if m >> i & 1]

    def leaves(self, m):
        return [i for i in range(1, self.n) if m >> i & 1 and not any(m >> j & 1 and self.par[j] == i for j in range(1, self.n))]


# ---------- assignments: integer matrices scaled by L, column form ----------
def bvec(name, t):
    out = [0] * t.n
    for w in range(1, t.n):
        d = t.dep[w]
        q = {"own": F(0), "gtax": F(1, 2) * (d == 1), "half": F(1, 4), "deep": F(1, 3) * (d == 2), "sat": F(int(w == 1)),
             "mixed": F((3 * w + 1) % 5, 20), "negative": F(int(d <= 2))}[name]
        out[w] = int(q * L)
    return out


def avec(t, b):                        # scaled
    return [L - sum(b[w] for w in t.mem(t.anc[u]) if w != 0) for u in range(t.n)]


def mat_cols(t, b, m):
    idx = t.mem(m)
    pos = {v: i for i, v in enumerate(idx)}
    a = avec(t, b)
    M = np.zeros((len(idx), len(idx)), dtype=np.int64)
    for j, u in enumerate(idx):
        M[pos[u], j] += a[u]
        for w in t.mem(t.anc[u]):
            if w != 0:
                M[pos[t.par[w]], j] += b[w]
    return M, idx


def mat_named(name, t, m):
    idx = t.mem(m)
    if name == "cone":
        return np.array([[L * t.le(v, u) for u in idx] for v in idx], dtype=np.int64), idx
    if name == "parent":
        return np.array([[L * ((u != 0 and t.par[u] == v) or (u == v == 0)) for u in idx] for v in idx], dtype=np.int64), idx
    return mat_cols(t, bvec(name, t), m)


def pmat(t, m, l):                     # P1 as |Y| x |X| 0/1 matrix
    X = t.mem(m); Y = [v for v in X if v != l]
    P = np.zeros((len(Y), len(X)), dtype=np.int64)
    for j, u in enumerate(X):
        P[Y.index(u if u != l else t.par[l]), j] = 1
    return P, X, Y


AFFINE = ["own", "gtax", "half", "deep", "sat", "mixed", "negative"]
FAMILY = AFFINE[:6]
PANEL = AFFINE + ["cone", "parent"]
FLAGKEYS = ("W1eq", "W1pos", "W2", "W4", "family", "affine", "L170", "i", "ii", "iii", "iv", "D")


def fr(z):
    return F(int(z), L)


def check_universe(t, uname, lines, nv):
    Cs = t.carriers
    full = {m: None for m in Cs}
    viol = 0
    flags = {}
    prun = [(m, l) for m in Cs for l in t.leaves(m)]
    covers = [(m, m | 1 << w) for m in Cs for w in range(1, t.n) if not m >> w & 1 and m >> t.par[w] & 1]
    Ps = {(m, l): pmat(t, m, l) for m, l in prun}
    for name in PANEL:
        Ms = {m: mat_named(name, t, m) for m in Cs}
        f = {}
        f["W1eq"] = all((Ms[m][0].sum(axis=0) == L).all() for m in Cs)
        f["W1pos"] = all((Ms[m][0] >= 0).all() for m in Cs)
        ok2 = True
        for m, m2 in covers:
            M, X = Ms[m]; M2, X2 = Ms[m2]
            cols = [X2.index(u) for u in X]
            sub = M2[:, cols]
            exp = np.zeros_like(sub)
            for i, v in enumerate(X2):
                if v in X:
                    exp[i] = M[X.index(v)]
            ok2 &= bool((sub == exp).all())
        f["W2"] = ok2
        ok4, iv_ok, ii_ok, iii_ok = True, True, True, True
        per = []
        for m, l in prun:
            P, X, Y = Ps[(m, l)]
            MX, MY = Ms[m][0], Ms[m - (1 << l)][0]
            comp = MY @ P
            p = t.par[l]
            for i, v in enumerate(Y):
                if v != p and not (comp[i] == MX[X.index(v)]).all():
                    ok4 = False
            inc = comp[Y.index(p)] - MX[X.index(p)]
            e = np.zeros(len(X), dtype=np.int64); e[X.index(l)] = L
            iv_ok &= bool((inc == e).all())
            bef, aft = int(MX[X.index(p), X.index(l)]), int(MY[Y.index(p), Y.index(p)])
            iii_ok &= bef == 0
            ii_ok &= bef == 0 and aft != 0
            per.append((m, l, X, Y, MX, MY, comp, inc, bef, aft))
        f["W4"] = ok4
        # recover b from chains and compare with the column-form family everywhere
        bt = [0] * t.n
        for u in range(1, t.n):
            M, X = Ms[t.anc[u]]
            bt[u] = int(M[X.index(t.par[u]), X.index(u)])
        aff = all((mat_cols(t, bt, m)[0] == Ms[m][0]).all() for m in Cs)
        f["affine"] = aff
        f["family"] = aff and min(bt) >= 0 and min(avec(t, bt)) >= 0
        l170 = True
        for m in Cs:
            M, X = Ms[m]
            for j, u in enumerate(X):
                Mc, Xc = Ms[t.anc[u]]
                for i, v in enumerate(X):
                    expv = Mc[Xc.index(v), Xc.index(u)] if t.le(v, u) else 0
                    l170 &= bool(M[i, j] == expv)
        f["L170"] = l170
        f["i"] = all((Ms[m][0] == L * np.eye(len(Ms[m][1]), dtype=np.int64)).all() for m in Cs)
        f["ii"], f["iii"], f["iv"] = ii_ok, iii_ok, iv_ok
        f["D"] = all(Ms[m][0][i, j] == 0 for m in Cs for i, v in enumerate(Ms[m][1]) for j, u in enumerate(Ms[m][1])
                     if u != v and t.le(v, u))
        flags[name] = "".join("1" if f[k] else "0" for k in FLAGKEYS)
        W1 = f["W1eq"] and f["W1pos"]
        if (W1 and f["W2"] and f["W4"]) != f["family"]:
            viol += 1
        if W1 and f["W2"] and f["W4"] and len({f["i"], f["ii"], f["iii"], f["iv"]}) != 1:
            viol += 1
        if (W1 and f["W2"] and f["D"]) != f["i"]:
            viol += 1
        if name not in AFFINE:
            continue
        b = bvec(name, t); a = avec(t, b)
        for (m, l, X, Y, MX, MY, comp, inc, bef, aft) in per:
            p = t.par[l]
            al, bl, ap = a[l], b[l], a[p]
            e = np.zeros(len(X), dtype=np.int64); e[X.index(l)] = al
            viol += int(not (inc == e).all())
            viol += int(bef != bl)
            for w in (1, -2, 3):
                xx = np.zeros(len(X), dtype=np.int64); xx[X.index(l)] = w
                viol += int(int(MX[X.index(p)] @ xx) != w * bl)
                viol += int(int(comp[Y.index(p)] @ xx) != w * ap)
            acq = bef == 0 and aft != 0
            corr = "-"
            if name in FAMILY:
                viol += int(acq != (bl == 0 and ap > 0))
                nv["acq" if acq else "nonacq"] += 1
                nv["b0_a0"] += int(not acq and bl == 0 and ap == 0)
                if p != 0:
                    if al > 0:
                        r = F(bl, ap)
                        cand = [u for u in X if u != 0 and not t.le(p, u)]
                        vs = min(cand) if cand else 0
                        xp = [F(1) + (u == l) for u in X]
                        xm = [F(1) + (r if u == p else 0) + ((1 - r) if u == vs else 0) for u in X]
                        rowX = [fr(z) for z in MX[X.index(p)]]
                        rowC = [fr(z) for z in comp[Y.index(p)]]
                        ok = min(xp + xm) >= 0 and sum(xp) == sum(xm)
                        ok &= sum(c * z for c, z in zip(rowX, xp)) == sum(c * z for c, z in zip(rowX, xm))
                        sep = sum(c * z for c, z in zip(rowC, xp)) - sum(c * z for c, z in zip(rowC, xm))
                        ok &= sep == fr(al)
                        viol += int(not ok)
                        corr = S(sep)
                        nv["corr_bpos"] += int(bl > 0)
                    else:
                        viol += int(bool(inc.any()))
                        corr = "0"
                        nv["D0"] += 1
            lines.append("%s|%s|%d|%d|%s|%s|%s|%s|%s|%d|%s" % (name, ",".join(map(str, X)), l, p, S(fr(al)), S(fr(bl)),
                                                              S(fr(ap)), S(fr(bef)), S(fr(aft)), int(acq), corr))
    for m in Cs:
        X = t.mem(m)
        deg = max(sum(1 for w in X if w != 0 and t.par[w] == v) for v in X)
        nv["deg2"] += deg >= 2
        nv["deg3"] += uname == "U17B" and deg >= 3
    return {"carriers": len(Cs), "covers": len(covers), "prunings": len(prun),
            "prunings_pno": sum(1 for m, l in prun if t.par[l] != 0)}, flags, viol


# ---------- Theorem 17.1: constraint generation and rank modulo PR ----------
def rank_mod(A):
    A = A % PR
    r = 0
    rows, cols = A.shape
    for c in range(cols):
        if A.shape[0] == 0:
            break
        nz = np.nonzero(A[:, c])[0]
        if len(nz) == 0:
            continue
        i = nz[0]
        piv = A[i].copy()
        inv = pow(int(piv[c]), PR - 2, PR)
        piv = (piv * inv) % PR
        others = nz[1:]
        if len(others):
            fac = A[others, c].reshape(-1, 1)
            A[others] = (A[others] - (fac * piv) % PR) % PR
        A = np.delete(A, i, axis=0)
        r += 1
    return r


def constraints(t):
    Cs = t.carriers
    var = {}
    for m in Cs:
        for v in t.mem(m):
            for u in t.mem(m):
                var[(m, v, u)] = len(var)
    rows = {"W1": [], "W2": [], "W4": []}
    for m in Cs:
        for u in t.mem(m):
            rows["W1"].append(([(var[(m, v, u)], 1) for v in t.mem(m)], 1))
    for m in Cs:
        for m2 in Cs:
            if m != m2 and m & m2 == m:
                for u in t.mem(m):
                    for v in t.mem(m2):
                        r = [(var[(m2, v, u)], 1)]
                        if m >> v & 1:
                            r.append((var[(m, v, u)], -1))
                        rows["W2"].append((r, 0))
    for m in Cs:
        for l in t.leaves(m):
            y = m - (1 << l); p = t.par[l]
            for v in t.mem(y):
                if v == p:
                    continue
                for u in t.mem(m):
                    tgt = u if u != l else p
                    if (y, v, tgt) == (m, v, u):
                        continue
                    rows["W4"].append(([(var[(y, v, tgt)], 1), (var[(m, v, u)], -1)], 0))
    return var, rows


def dims(t, var, rows, keys):
    rr = [r for k in keys for r in rows[k]]
    A = np.zeros((len(rr), len(var) + 1), dtype=np.int64)
    for i, (cs, rhs) in enumerate(rr):
        for k, c in cs:
            A[i, k] += c
        A[i, -1] = rhs
    A = np.unique(A, axis=0)
    rk = rank_mod(A[:, :-1].copy())
    rka = rank_mod(A.copy())
    return len(var) - rk, rk == rka


def family_exact(t, var, rows):
    ok = True
    vecs = [[0] * t.n] + [[int(u == w) for u in range(t.n)] for w in range(1, t.n)]
    for b in vecs:
        a = [1 - sum(b[w] for w in t.mem(t.anc[u]) if w != 0) for u in range(t.n)]
        val = [0] * len(var)
        for (m, v, u), k in var.items():
            if v == u:
                val[k] = a[u]
            elif t.le(v, u):
                c = [w for w in t.mem(t.anc[u]) if w != 0 and t.par[w] == v][0]
                val[k] = b[c]
        for key in ("W1", "W2", "W4"):
            for cs, rhs in rows[key]:
                ok &= sum(c * val[k] for k, c in cs) == rhs
    return ok


def ue(par):
    t = Tree(par)
    var, rows = constraints(t)
    d, c1 = dims(t, var, rows, ("W1", "W2", "W4"))
    d4, c2 = dims(t, var, rows, ("W1", "W2"))
    d2, c3 = dims(t, var, rows, ("W1", "W4"))
    fam = family_exact(t, var, rows)
    sd = sum(t.dep[1:])
    viol = int(not (c1 and c2 and c3)) + int(d != t.n - 1) + int(d4 != sd) + int(not fam)
    return {"carriers": len(t.carriers), "unknowns": len(var), "dim": d, "dim_noW4": d4, "dim_noW2": d2, "family_ok": fam}, viol


def trees():
    out = []
    for n in range(1, 7):
        out += [[-1] + list(t) for t in itertools.product(*[range(i) for i in range(1, n)])]
    return out + [[-1, 0, 0, 1, 1, 2, 2], [-1, 0, 0, 1, 1, 1, 2]]


# ---------- explicit instances (independent recomputation) ----------
def hold(M, x):
    return [sum(fr(M[i, j]) * x[j] for j in range(len(x))) for i in range(M.shape[0])]


def explicit():
    V = {}
    T4 = Tree([-1, 0, 1, 0]); C3 = Tree([-1, 0, 1])
    full, Ym = 0b1111, 0b1011
    gt = bvec("gtax", T4)
    M, _ = mat_cols(T4, gt, full)
    V["X1.gtax_M"] = [[S(fr(z)) for z in row] for row in M]
    V["X1.gtax_a"] = [S(fr(z)) for z in avec(T4, gt)]
    V["X1.colsums"] = [S(fr(z)) for z in M.sum(axis=0)]
    x = [F(3), F(5), F(7), F(2)]
    P, X, Y = pmat(T4, full, 2)
    y = [sum(int(P[i, j]) * x[j] for j in range(4)) for i in range(3)]
    MY, _ = mat_cols(T4, gt, Ym)
    hb, ha = hold(M, x), hold(MY, y)
    V["X2.gtax_before"] = [S(z) for z in hb]; V["X2.gtax_after"] = [S(z) for z in ha]
    V["X2.gtax_increment"] = S(ha[1] - hb[1]); V["X2.gtax_totals"] = [S(sum(hb)), S(sum(ha))]
    ob = [0] * 4
    V["X2.own_before"] = [S(z) for z in hold(mat_cols(T4, ob, full)[0], x)]
    V["X2.own_after"] = [S(z) for z in hold(mat_cols(T4, ob, Ym)[0], y)]
    gptb = [0, L // 4, L // 4, 0]
    sat = [0, L, 0, 0]
    acqs = []
    ep, em = [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]
    Pe = lambda v: [sum(int(P[i, j]) * v[j] for j in range(4)) for i in range(3)]
    for key, b in (("gptb", gptb), ("gtax", gt), ("own", ob), ("sat", sat)):
        MX, MYb = mat_cols(T4, b, full)[0], mat_cols(T4, b, Ym)[0]
        bef = [hold(MX, ep)[1], hold(MX, em)[1]]
        aft = [hold(MYb, Pe(ep))[1], hold(MYb, Pe(em))[1]]
        V["X3.%s_p" % key] = [[S(z) for z in bef], [S(z) for z in aft]]
        acqs.append(bef[0] == bef[1] and aft[0] != aft[1])
    V["X3.acq"] = acqs
    a = avec(T4, gptb)
    A, B, D = fr(a[1]), fr(gptb[2]), fr(a[2]); r = B / A
    V["X3.gptb_ABDr"] = [S(A), S(B), S(D), S(r)]
    MX, MYb = mat_cols(T4, gptb, full)[0], mat_cols(T4, gptb, Ym)[0]
    xp = [F(1), F(1), F(2), F(1)]
    xm = [F(1), 1 + r, F(1), 1 + (1 - r)]
    V["X4.x_plus"] = [S(z) for z in xp]; V["X4.x_minus"] = [S(z) for z in xm]
    V["X4.totals"] = [S(sum(xp)), S(sum(xm))]
    bp, bm = hold(MX, xp), hold(MX, xm)
    V["X4.before_plus"] = [S(z) for z in bp]; V["X4.before_minus"] = [S(z) for z in bm]
    V["X4.Px_plus"] = [S(z) for z in Pe(xp)]; V["X4.Px_minus"] = [S(z) for z in Pe(xm)]
    ap_, am_ = hold(MYb, Pe(xp)), hold(MYb, Pe(xm))
    V["X4.after_plus"] = [S(z) for z in ap_]; V["X4.after_minus"] = [S(z) for z in am_]
    V["X4.p_before"] = [S(bp[1]), S(bm[1])]; V["X4.p_after"] = [S(ap_[1]), S(am_[1])]
    V["X4.separation"] = S(ap_[1] - am_[1])
    V["X4.leaf_holding"] = [S(bp[2]), S(bm[2])]
    V["X4.oneloc_before"] = S(hold(MX, ep)[1])
    P3, _, _ = pmat(T4, full, 3)
    Mg3 = mat_cols(T4, gt, 0b0111)[0]
    e3 = [F(0), F(0), F(0), F(1)]
    bef = hold(M, e3)[0]
    aft = hold(Mg3, [sum(int(P3[i, j]) * e3[j] for j in range(4)) for i in range(3)])[0]
    V["X5.before"], V["X5.after"], V["X5.acq"] = S(bef), S(aft), bef == 0 and aft != 0
    Mc, _ = mat_named("cone", C3, 0b111)
    xc = [F(3), F(5), F(7)]
    hc = hold(Mc, xc)
    V["X6.C"] = [S(z) for z in hc]; V["X6.sumC"] = S(sum(hc)); V["X6.total"] = S(sum(xc))
    V["X6.W1eq"] = bool((Mc.sum(axis=0) == L).all())
    Mp, _ = mat_named("parent", C3, 0b111); MpY, _ = mat_named("parent", C3, 0b011)
    yc = [xc[0], xc[1] + xc[2]]
    hb, ha = hold(Mp, xc), hold(MpY, yc)
    V["X7.before"] = [S(z) for z in hb]; V["X7.after"] = [S(z) for z in ha]
    V["X7.changed_nonreceivers"] = [v for v in (0,) if ha[v] != hb[v]]
    for key, par in (("chain2", [-1, 0]), ("chain5", [-1, 0, 1, 2, 3]), ("T4", [-1, 0, 1, 0]), ("star3", [-1, 0, 0, 0]),
                     ("bin2", [-1, 0, 0, 1, 1, 2, 2]), ("mixed7", [-1, 0, 0, 1, 1, 1, 2])):
        rec, _ = ue(par)
        V["X8." + key] = [rec["carriers"], rec["unknowns"], rec["dim"], rec["dim_noW4"]]
        if key == "chain2":
            V["X8.chain2_noW2"] = rec["dim_noW2"]
    Mg = mat_cols(T4, gptb, full)[0]
    V["X9.M12"] = S(fr(Mg[1, 2])); V["X9.M12_chain"] = S(fr(mat_cols(T4, gptb, 0b0111)[0][1, 2]))
    V["X9.M32"] = S(fr(Mg[3, 2])); V["X9.M21"] = S(fr(Mg[2, 1]))
    return V


def bounded():
    t = Tree([-1, 0, 1, 0])
    grid = [0, 15, 30, 45, 60]                      # quarters, scaled by L
    out = {"B17a_grid": 0, "B17a_W1eq_W2_W4": 0, "B17a_valid": 0, "B17a_ii": 0, "B17a_iii": 0, "B17a_iv": 0,
           "B17a_corr": 0, "B17a_corr_bpos": 0, "B17a_oneloc": 0}
    prun = [(m, l) for m in t.carriers for l in t.leaves(m)]
    covers = [(m, m | 1 << w) for m in t.carriers for w in range(1, t.n) if not m >> w & 1 and m >> t.par[w] & 1]
    for b1, b2, b3 in itertools.product(grid, repeat=3):
        b = [0, b1, b2, b3]
        a = avec(t, b)
        out["B17a_grid"] += 1
        Ms = {m: mat_cols(t, b, m) for m in t.carriers}
        w1 = all((Ms[m][0].sum(axis=0) == L).all() for m in t.carriers)
        w2 = all((Ms[m2][0][:, [Ms[m2][1].index(u) for u in Ms[m][1]]] ==
                  np.array([Ms[m][0][Ms[m][1].index(v)] if m >> v & 1 else np.zeros(len(Ms[m][1]), dtype=np.int64)
                            for v in Ms[m2][1]])).all() for m, m2 in covers)
        w4 = True
        ii = iii = iv = True
        for m, l in prun:
            P, X, Y = pmat(t, m, l)
            comp = Ms[m - (1 << l)][0] @ P
            p = t.par[l]
            for i, v in enumerate(Y):
                if v != p and not (comp[i] == Ms[m][0][X.index(v)]).all():
                    w4 = False
            inc = comp[Y.index(p)] - Ms[m][0][X.index(p)]
            e = np.zeros(len(X), dtype=np.int64); e[X.index(l)] = L
            iv &= bool((inc == e).all())
            bef = Ms[m][0][X.index(p), X.index(l)]
            aft = Ms[m - (1 << l)][0][Y.index(p), Y.index(p)]
            iii &= bef == 0
            ii &= bef == 0 and aft != 0
        out["B17a_W1eq_W2_W4"] += int(w1 and w2 and w4)
        valid = min(b) >= 0 and min(a) >= 0
        if not valid:
            continue
        out["B17a_valid"] += 1
        out["B17a_ii"] += int(ii); out["B17a_iii"] += int(iii); out["B17a_iv"] += int(iv)
        if a[2] > 0:                                # correlated pair at prune 2, full carrier, v* = 3
            MX, MYb = Ms[0b1111][0], Ms[0b1011][0]
            r = F(b[2], a[1])
            xp = [F(1), F(1), F(2), F(1)]; xm = [F(1), 1 + r, F(1), 2 - r]
            Pp = lambda v: [v[0], v[1] + v[2], v[3]]
            okb = hold(MX, xp)[1] == hold(MX, xm)[1]
            sep = hold(MYb, Pp(xp))[1] - hold(MYb, Pp(xm))[1]
            if okb and sep == fr(a[2]) and sep > 0:
                out["B17a_corr"] += 1
                out["B17a_corr_bpos"] += int(b[2] > 0)
        MX, MYb = Ms[0b1111][0], Ms[0b1011][0]
        out["B17a_oneloc"] += int(MX[1, 2] == 0 and MYb[1, 1] != 0)
    return out


def main():
    sha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    uni = {}
    lines, viol, n_ge2_pos, gt_w2, recs = [], 0, 0, 0, {}
    tl = trees()
    for par in tl:
        rec, v = ue(par)
        viol += v
        n = len(par)
        recs[tuple(par)] = rec
        n_ge2_pos += n >= 2 and rec["dim"] >= 1
        gt_w2 += rec["dim_noW2"] > n - 1
        lines.append("%d:%s|%d|%d|%d|%d|%d|%d" % (n, ",".join(map(str, par[1:])), rec["carriers"], rec["unknowns"],
                                                 rec["dim"], rec["dim_noW4"], rec["dim_noW2"], int(rec["family_ok"])))
    uni.update({"ue_trees": len(tl), "ue_lines": len(lines),
                "ue_digest": hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest(), "ue_viol": viol,
                "ue_n_ge2_dim_pos": n_ge2_pos, "ue_noW2_gt": gt_w2})
    nv = {k: 0 for k in ("acq", "nonacq", "b0_a0", "corr_bpos", "D0", "deg2", "deg3")}
    panel, flag_lines = {}, []
    for uname, par in (("U17A", [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]), ("U17B", [-1, 0, 0, 0, 1, 1, 1, 2, 2, 4, 7])):
        ul = []
        counts, flags, v = check_universe(Tree(par), uname, ul, nv)
        panel[uname] = flags
        key = uname.lower()
        for k, c in counts.items():
            uni["%s_%s" % (key, k)] = c
        uni[key + "_lines"] = len(ul)
        uni[key + "_digest"] = hashlib.sha256("\n".join(sorted(ul)).encode()).hexdigest()
        uni[key + "_viol"] = v
        flag_lines += ["%s|%s|%s" % (uname, a, f) for a, f in flags.items()]
    uni["flags_digest"] = hashlib.sha256("\n".join(sorted(flag_lines)).encode()).hexdigest()
    for k, c in nv.items():
        uni["nv_" + k] = c
    vals = explicit()
    bnd = bounded()
    fam_ok_others = all(panel[u][a][:4] == "1111" for u in panel for a in ("gtax", "half", "deep", "sat", "mixed"))
    ctl = {}
    rej = lambda cond: "REJECTED" if cond else "ACCEPTED"
    ctl["R1_W1_W2_W4_force_own"] = rej(fam_ok_others and uni["ue_n_ge2_dim_pos"] == len(tl) - 1)
    ctl["R2_cone_is_partition"] = rej(vals["X6.W1eq"] is False and all(panel[u]["cone"][0] == "0" for u in panel))
    ctl["R3_parent_is_local"] = rej(vals["X7.changed_nonreceivers"] == [0] and all(panel[u]["parent"][3] == "0" for u in panel))
    ctl["R4_gtax_every_pruning_acquires"] = rej(vals["X5.acq"] is False and all(panel[u]["gtax"][8] == "0" for u in panel))
    ctl["R5_sign_redundant"] = rej(all(panel[u]["negative"][:4] == "1011" for u in panel))
    ctl["R6_existential_implies_universal"] = rej(vals["X4.separation"] == "1/2" and vals["X4.p_before"][0] == vals["X4.p_before"][1]
                                                  and vals["X4.oneloc_before"] != "0" and uni["nv_corr_bpos"] > 0
                                                  and bnd["B17a_corr_bpos"] > 0)
    ctl["R7_b0_suffices"] = rej(vals["X3.acq"][3] is False and uni["nv_b0_a0"] > 0)
    ctl["R8_without_W4"] = rej(any(r["dim_noW4"] > len(p) - 1 for p, r in recs.items()))
    ctl["R9_without_W2"] = rej(any(r["dim_noW2"] > len(p) - 1 for p, r in recs.items()))
    ctl["R10_blind_with_b_nonzero"] = rej(all(panel[u][a][9] == ("1" if a == "own" else "0") for u in panel for a in FAMILY)
                                          and bnd["B17a_iii"] == 1)
    cert = {"meta": {"role": "checker", "result_sha256": sha}, "values": vals, "universe": uni, "panel": panel,
            "bounded": bnd, "controls": ctl}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"universe": uni, "bounded": bnd, "controls": ctl}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
