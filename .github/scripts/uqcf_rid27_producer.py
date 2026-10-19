"""receiver_identification d27 freeze (sections 31-32): PRODUCER. Recursive rooted-subtree enumeration, sparse holding rows,
HiGHS LP range ends followed by exact rational certification (primal point + dual multipliers, or exact ray), exact tables."""
import hashlib, itertools, json, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOTP = "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d27_review/RESULT.md"
TREES = {
    "TB": lambda v: (0, 1) if len(v) < 3 else (),
    "TM": lambda v: (0, 1, 2) if len(v) == 0 else ((0, 1) if len(v) < 3 else ()),
    "S1": lambda v: (0, 1) if len(v) == 0 else (),
    "S2": lambda v: (0, 1) if len(v) == 0 else ((0,) if v == (0,) else ()),
}
def astr(v): return "r" + "".join("." + str(i) for i in v)
def anc(v): return [v[:i] for i in range(len(v) + 1)]
def meet(v, z):
    i = 0
    while i < min(len(v), len(z)) and v[i] == z[i]: i += 1
    return v[:i]
def below(x, v): return len(x) > len(v) and x[:len(v)] == v
def ac(d): return (0,) * d
def um(m): return (0,) * m + (1,)

class Tree:
    def __init__(self, name):
        self.name = name; k = TREES[name]; self.k = k
        def addrs(v=()):
            out = [v]
            for i in k(v): out += addrs(v + (i,))
            return out
        def subs(v=()):
            opts = [[None] + subs(v + (i,)) for i in k(v)]
            res = []
            for combo in itertools.product(*opts):
                s = {v}
                for x in combo:
                    if x: s |= x
                res.append(frozenset(s))
            return res
        self.addr = addrs(); self.car = subs()
        self.vars = [(v, w) for v in self.addr for w in anc(v)]; self.ix = {x: i for i, x in enumerate(self.vars)}
        self.leaves = [v for v in self.addr if not k(v)]
    def ch(self, W, v): return [v + (i,) for i in self.k(v) if v + (i,) in W]
    def row(self, W, v, z):
        r = {self.ix[(v, meet(v, z))]: Fr(1)}
        for u in self.ch(W, v):
            q = self.ix[(u, meet(u, z))]; r[q] = r.get(q, 0) - 1
        return {a: b for a, b in r.items() if b != 0}
    def digest(self):
        lines = sorted(",".join(sorted(astr(v) for v in W)) for W in self.car)
        return hashlib.sha256("\n".join(lines).encode()).hexdigest()
    def fork(self, m, x): return frozenset(anc(ac(m)) + [ac(m + 1), x])
    def chain(self, l): return frozenset(anc(l))

def dedup(rows):
    S = set()
    for r in rows:
        if r: S.add(tuple(sorted(r.items())))
    return [dict(x) for x in sorted(S)]

def full_rows(T): return dedup(T.row(W, v, z) for W in T.car for v in W for z in W)

def test_class(T, D, drop_fork=None, drop_cover=None):
    C = [(frozenset([()]), [()])]
    for m in range(D):
        for x in [ac(m) + (i,) for i in T.k(ac(m)) if ac(m) + (i,) != ac(m + 1)]:
            if (m, x) == drop_fork: continue
            C.append((T.fork(m, x), [ac(j) for j in range(m + 2)]))
    for l in T.leaves:
        if drop_cover is not None and l[:len(drop_cover)] == drop_cover: continue
        W = T.chain(l); C.append((W, [ac(j) for j in range(D) if ac(j) in W]))
    return C

def rest_rows(T, D, **kw): return dedup(T.row(W, v, z) for W, units in test_class(T, D, **kw) for z in units for v in W)

def eq_rows(T, D, cond):
    E = [({T.ix[((), ())]: Fr(1)}, Fr(1))]
    for d in range(1, D + 1):
        E.append(({T.ix[(ac(d), ac(d))]: Fr(1), T.ix[(ac(d - 1), ac(d - 1))]: Fr(-1)}, Fr(0)))
    for m in range(D):
        W = T.fork(m, um(m))
        def diff(r1, r2):
            r = dict(r1)
            for a, b in r2.items(): r[a] = r.get(a, 0) - b
            return {a: b for a, b in r.items() if b != 0}
        if cond == "SE":
            r = diff(T.row(W, ac(m + 1), ac(m)), T.row(W, um(m), ac(m)))
            if r: E.append((r, Fr(0)))
        if cond == "SX":
            s = lambda x: um(m) if x == ac(m + 1) else (ac(m + 1) if x == um(m) else x)
            seen = set()
            for v in sorted(W):
                for z in sorted(W):
                    r = diff(T.row(W, s(v), s(z)), T.row(W, v, z))
                    key = tuple(sorted(r.items()))
                    if r and key not in seen: seen.add(key); E.append((r, Fr(0)))
    return E

def lp_end(T, rows, eqs, var, sense, Aub, Aeq, beq):
    nv = len(T.vars); j = T.ix[var]
    c = np.zeros(nv); c[j] = sense
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(Aub.shape[0]), A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * nv, method="highs")
    if res.status == 3:
        # exact ray: d = -sense * e_j; need every row and eq homogeneous part to vanish/stay >= 0 along d, and a feasible point
        d = -sense
        okray = all(r.get(j, 0) * d >= 0 for r in rows) and all(e.get(j, 0) == 0 for e, _ in eqs)
        x = {T.ix[(v, v)]: Fr(1) for v in T.addr}
        okpt = all(sum(b * x.get(a, 0) for a, b in r.items()) >= 0 for r in rows) and \
               all(sum(b * x.get(a, 0) for a, b in e.items()) == rhs for e, rhs in eqs)
        return ("-inf" if sense == 1 else "inf"), okray and okpt
    if res.status != 0: return None, False
    x = [Fr(float(v)).limit_denominator(10 ** 6) for v in res.x]
    lam = [Fr(float(-m)).limit_denominator(10 ** 6) for m in res.ineqlin.marginals]
    mu = [Fr(float(m)).limit_denominator(10 ** 6) for m in res.eqlin.marginals]
    ok = all(l >= 0 for l in lam)
    for r in rows:
        if sum(b * x[a] for a, b in r.items()) < 0: ok = False
    for e, rhs in eqs:
        if sum(b * x[a] for a, b in e.items()) != rhs: ok = False
    recon = [Fr(0)] * nv
    for l, r in zip(lam, rows):
        if l:
            for a, b in r.items(): recon[a] += l * b
    for m_, (e, _) in zip(mu, eqs):
        if m_:
            for a, b in e.items(): recon[a] += m_ * b
    cex = [Fr(0)] * nv; cex[j] = Fr(sense)
    if recon != cex: ok = False
    primal = sense * x[j]; dual = sum(m_ * rhs for m_, (e, rhs) in zip(mu, eqs))
    if primal != dual: ok = False
    return str(sense * primal), ok

def sparse(T, rows, sign):
    data, ri, ci = [], [], []
    for i, r in enumerate(rows):
        for a, b in r.items(): ri.append(i); ci.append(a); data.append(sign * float(b))
    return csr_matrix((data, (ri, ci)), shape=(max(1, len(rows)), len(T.vars)))

def targets(T, kind, D, cond, extra=None):
    t = []
    if kind in ("FULL", "REST"):
        t += [(ac(d), ac(d)) for d in range(D + 1)]
        for m in range(D):
            for x in T.addr:
                if below(x, ac(m)) and not (x == ac(m + 1) or below(x, ac(m + 1))): t.append((x, ac(m)))
            t.append((ac(m + 1), ac(m)))
            if cond in ("SE", "SX") or (kind == "FULL" and T.name == "TB"):
                t += [(x, ac(m)) for x in T.addr if below(x, ac(m + 1))]
            t.append((um(m), um(m)))
    elif kind == "DROPF":
        m, u = extra; t.append((u, ac(m)))
        if u == um(m): t.append((ac(m + 1), ac(m)))
    else:
        c, m = extra; t.append((c, ac(m)))
    return t

def systems():
    S = []
    for tn in ("TB", "TM"):
        for D in (1, 2, 3):
            for c in ("none", "SE", "SX"): S.append(("FULL", tn, D, c, None))
    for D in (1, 2, 3):
        for c in ("none", "SE"): S.append(("REST", "TM", D, c, None))
    for mu_ in ((0, (1,)), (0, (2,)), (1, (0, 1))): S.append(("DROPF", "TM", 2, "SE", mu_))
    for cm in (((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)): S.append(("DROPC", "TM", 2, "SE", cm))
    return S

def skey(kind, tn, D, c, extra):
    k = "%s|%s|%d|%s" % (kind, tn, D, c)
    if kind == "DROPF": k += "|%d,%s" % (extra[0], astr(extra[1]))
    if kind == "DROPC": k += "|%s,%d" % (astr(extra[0]), extra[1])
    return k

# ---------- exact tables ----------
def T_id(T): return {(v, v): Fr(1) for v in T.addr}
def T_fam(T, m, t):
    A = T_id(T); A[(ac(m + 1), ac(m))] = Fr(t)
    for c in T.addr:
        if below(c, ac(m)) and not (c == ac(m + 1) or below(c, ac(m + 1))): A[(c, c)] = 1 - Fr(t)
    return A
def T_cone(T, u, q):
    A = T_id(T)
    for v in T.addr:
        if v == u or below(v, u): A[(v, v)] = Fr(q)
    return A
def hv(T, A, W, v, z): return A.get((v, meet(v, z)), Fr(0)) - sum((A.get((u, meet(u, z)), Fr(0)) for u in T.ch(W, v)), Fr(0))
def col(T, A, W, z, order): return [hv(T, A, W, v, z) for v in order]
def rows_ok(A, T, rows): return all(sum(b * A.get(T.vars[a], Fr(0)) for a, b in r.items()) >= 0 for r in rows)
def eqs_ok(A, T, eqs): return all(sum(b * A.get(T.vars[a], Fr(0)) for a, b in e.items()) == rhs for e, rhs in eqs)
def bl_ok(T, A, D): return all(hv(T, A, T.chain(ac(d)), ac(d - 1), ac(d)) == 0 for d in range(1, D + 1)) and A.get(((), ()), 0) == 1
def se_ok(T, A, m): W = T.fork(m, um(m)); return hv(T, A, W, ac(m + 1), ac(m)) == hv(T, A, W, um(m), ac(m))
def sx_ok(T, A, m):
    W = T.fork(m, um(m)); s = lambda x: um(m) if x == ac(m + 1) else (ac(m + 1) if x == um(m) else x)
    return all(hv(T, A, W, s(v), s(z)) == hv(T, A, W, v, z) for v in W for z in W)
def fc_ok(T, A, D, ms=None):
    for W in T.car:
        for m in (range(D + 1) if ms is None else ms):
            z = ac(m)
            if z not in W or (m == D and T.ch(W, z)): continue
            if any(hv(T, A, W, v, z) != (1 if v == z else 0) for v in W): return False
    return True
def posT_ok(T, A, D, **kw): return all(hv(T, A, W, v, z) >= 0 for W, units in test_class(T, D, **kw) for z in units for v in W)
def pn_ok(T, A):
    for W in T.car:
        for l in W:
            if l == () or T.ch(W, l): continue
            Y = W - {l}; p = l[:-1]
            for z in W:
                FW = {v: hv(T, A, W, v, z) for v in W}
                PF = {v: FW[v] for v in Y}; PF[p] += FW[l]
                Pz = p if z == l else z
                if any(hv(T, A, Y, v, Pz) != PF[v] for v in Y): return False
    return True

def main(outp):
    TT = {n: Tree(n) for n in TREES}
    res = {"role": "producer", "classes": {n: {"carriers": len(T.car), "digest": T.digest(), "vars": len(T.vars)} for n, T in TT.items()}}
    FR = {n: full_rows(TT[n]) for n in TREES}
    res["full_pos_rows"] = {n: len(FR[n]) for n in ("TB", "TM")}
    ranges = {}; allcert = True
    for (kind, tn, D, c, extra) in systems():
        T = TT[tn]
        if kind == "FULL": rows = FR[tn]
        elif kind == "REST": rows = rest_rows(T, D)
        elif kind == "DROPF": rows = rest_rows(T, D, drop_fork=extra)
        else: rows = rest_rows(T, D, drop_cover=extra[0])
        eqs = eq_rows(T, D, c)
        Aub = sparse(T, rows, -1.0)
        Aeq = np.zeros((len(eqs), len(T.vars))); beq = np.array([float(r) for _, r in eqs])
        for i, (e, _) in enumerate(eqs):
            for a, b in e.items(): Aeq[i, a] = float(b)
        out = {}
        for var in targets(T, kind, D, c, extra):
            lo, ok1 = lp_end(T, rows, eqs, var, 1, Aub, Aeq, beq)
            hi, ok2 = lp_end(T, rows, eqs, var, -1, Aub, Aeq, beq)
            allcert &= ok1 and ok2
            out["A[%s|%s]" % (astr(var[0]), astr(var[1]))] = [lo, hi]
        ranges[skey(kind, tn, D, c, extra)] = out
    res["ranges"] = ranges; res["certified_exact"] = allcert
    TBt, TMt, S1, S2 = TT["TB"], TT["TM"], TT["S1"], TT["S2"]
    X = {}
    x1 = True
    for T in (TBt, TMt):
        for m in range(3):
            for t in (Fr(1, 3), Fr(1, 2), Fr(1)):
                A = T_fam(T, m, t); F = T.fork(m, um(m))
                x1 &= rows_ok(A, T, FR[T.name]) and bl_ok(T, A, 3) and hv(T, A, T.chain(ac(m + 1)), ac(m + 1), ac(m)) == t
                x1 &= hv(T, A, F, ac(m + 1), ac(m)) == t and hv(T, A, F, um(m), ac(m)) == 0 and not se_ok(T, A, m)
    X["X1"] = x1
    x2 = True
    for q in (Fr(0), Fr(1, 3), Fr(1, 2)):
        A = T_cone(TMt, um(0), q)
        x2 &= rows_ok(A, TMt, FR["TM"]) and bl_ok(TMt, A, 2) and se_ok(TMt, A, 0) and se_ok(TMt, A, 1) and fc_ok(TMt, A, 2) and not sx_ok(TMt, A, 0)
    X["X2"] = x2
    a, c_, u = (0,), (0, 0), (1,)
    full2 = [(), a, c_, u]
    x3 = True
    for r in (Fr(1, 3), Fr(1, 2), Fr(1)):
        A = T_id(S2); A[(c_, a)] = r
        x3 &= rows_ok(A, S2, FR["S2"]) and bl_ok(S2, A, 1) and sx_ok(S2, A, 0)
        x3 &= col(S2, A, frozenset(full2), a, full2) == [0, 1 - r, r, 0]
        x3 &= all(col(S2, A, W, a, sorted(W)) == [1 if v == a else 0 for v in sorted(W)] for W in (frozenset([(), a]), frozenset([(), a, u])))
    X["X3"] = x3
    def t_bot(s, t):
        return {((), ()): Fr(1), (a, ()): t, (a, a): Fr(1), (u, ()): Fr(0), (u, u): 1 - t, (c_, ()): s, (c_, a): s, (c_, c_): Fr(1)}
    x4 = True
    for s, t in ((Fr(0), Fr(1, 2)), (Fr(1, 4), Fr(1, 2)), (Fr(1, 2), Fr(1, 2)), (Fr(0), Fr(0)), (Fr(1, 3), Fr(1))):
        A = t_bot(s, t)
        x4 &= rows_ok(A, S2, FR["S2"]) and bl_ok(S2, A, 1) and col(S2, A, frozenset(full2), (), full2) == [1 - t, t - s, s, 0]
    X["X4"] = x4
    A5 = T_id(TMt); A5[(um(0), um(0))] = Fr(-1)
    X["X5"] = posT_ok(TMt, A5, 2) and bl_ok(TMt, A5, 2) and se_ok(TMt, A5, 0) and se_ok(TMt, A5, 1) and fc_ok(TMt, A5, 2) \
        and hv(TMt, A5, TMt.chain(um(0)), um(0), um(0)) == -1 and not rows_ok(A5, TMt, FR["TM"])
    def t_dropf(m, x, e):
        A = T_id(TMt); A[(x, ac(m))] = e
        if x == um(m): A[(ac(m + 1), ac(m))] = e
        return A
    x6 = True
    for (m, x) in ((0, (1,)), (0, (2,)), (1, (0, 1))):
        for e in (Fr(1, 2), Fr(1)):
            A = t_dropf(m, x, e)
            x6 &= posT_ok(TMt, A, 2, drop_fork=(m, x)) and bl_ok(TMt, A, 2) and se_ok(TMt, A, 0) and se_ok(TMt, A, 1)
            x6 &= (not posT_ok(TMt, A, 2)) and not fc_ok(TMt, A, 2)
    X["X6"] = x6
    x7 = True
    for (cc, m) in (((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)):
        A = T_id(TMt); A[(cc, ac(m))] = Fr(1, 2)
        x7 &= posT_ok(TMt, A, 2, drop_cover=cc) and bl_ok(TMt, A, 2) and se_ok(TMt, A, 0) and se_ok(TMt, A, 1)
        x7 &= (not posT_ok(TMt, A, 2)) and (not fc_ok(TMt, A, 2)) and hv(TMt, A, TMt.chain(cc), cc, ac(m)) == Fr(1, 2)
    X["X7"] = x7
    def t_d27b(s):
        A = T_id(S2); A[(c_, ())] = s; return A
    x8 = True
    for s in (Fr(1, 2), Fr(1)):
        A = t_d27b(s)
        x8 &= bl_ok(S2, A, 1) and se_ok(S2, A, 0)
        for W in (frozenset([(), a]), frozenset([(), a, u]), frozenset([()]), frozenset([(), u])):
            x8 &= all(col(S2, A, W, z, sorted(W)) == [1 if v == z else 0 for v in sorted(W)] for z in W)
        x8 &= col(S2, A, frozenset(full2), (), full2) == [1, -s, s, 0] and not fc_ok(S2, A, 1) and not posT_ok(S2, A, 1)
    X["X8"] = x8
    def t_d27c(e):
        A = T_id(S1); A[(a, ())] = e; A[(u, ())] = e; return A
    x9 = True
    fk = [(), a, u]
    for e in (Fr(1, 4), Fr(1, 2)):
        A = t_d27c(e)
        x9 &= bl_ok(S1, A, 1) and se_ok(S1, A, 0) and all(hv(S1, A, W, v, ()) >= 0 for W in S1.car for v in W)
        x9 &= col(S1, A, frozenset(fk), a, fk) == [-e, 1, e]
    X["X9"] = x9
    A10 = T_fam(TMt, 1, Fr(1, 2)); x10 = not se_ok(TMt, A10, 1)
    for d in (1, 2):
        for W in TMt.car:
            if ac(d) in W and not TMt.ch(W, ac(d)):
                Y = W - {ac(d)}
                x10 &= all(hv(TMt, A10, W, v, ac(d)) == (1 if v == ac(d) else 0) for v in W)
                x10 &= all(hv(TMt, A10, Y, v, ac(d - 1)) == (1 if v == ac(d - 1) else 0) for v in Y)
    x10 &= not fc_ok(TMt, A10, 2, ms=[1])
    X["X10"] = x10
    # X11: explicit matrices on the history chain
    def hist(t):
        okp = okb = okn = True
        for n in (3, 2):  # W has n vertices 0..n-1 in chain order, leaf l = n-1, receiver p = n-2
            l, p = n - 1, n - 2
            F = [[Fr(1) if i == j else Fr(0) for j in range(n)] for i in range(n)]  # F[holder][unit]
            F[l][p] += t; F[p][p] -= t
            okp &= all(F[i][j] >= 0 for i in range(n) for j in range(n))
            okb &= F[p][l] == 0 and F[l][l] == 1
            G = [[Fr(1) if i == j else Fr(0) for j in range(n - 1)] for i in range(n - 1)]
            for j in range(n):
                PF = [F[i][j] for i in range(n - 1)]; PF[p] += F[l][j]
                Pj = p if j == l else j
                okn &= PF == [G[i][Pj] for i in range(n - 1)]
        return okp, okb, okn
    X["X11"] = all(all(hist(t)) for t in (Fr(0), Fr(1, 2), Fr(1))) and all((not hist(t)[0]) and hist(t)[1] and hist(t)[2] for t in (Fr(-1, 2), Fr(3, 2)))
    X["X12"] = all(pn_ok(T, A) for T, A in ((TBt, T_id(TBt)), (TBt, T_fam(TBt, 0, Fr(1, 2))), (S2, t_bot(Fr(1, 4), Fr(1, 2))), (S2, T_id(S2))))
    res["tables"] = X
    A = T_fam(TBt, 0, Fr(1, 2)); F0 = TBt.fork(0, um(0))
    Y = {"Y1": [str(hv(TBt, A, TBt.chain(ac(1)), ac(1), ())), str(hv(TBt, A, F0, ac(1), ())), str(hv(TBt, A, F0, um(0), ()))],
         "Y2": [str(x) for x in col(TMt, T_cone(TMt, um(0), Fr(1, 3)), TMt.fork(0, um(0)), um(0), [(), (0,), (1,)])],
         "Y3": [str(x) for x in col(S2, t_bot(Fr(1, 4), Fr(1, 2)), frozenset(full2), (), full2)],
         "Y4": [str(x) for x in col(S2, {**T_id(S2), (c_, a): Fr(1, 2)}, frozenset(full2), a, full2)],
         "Y5": [str(x) for x in col(S2, t_d27b(Fr(1, 2)), frozenset(full2), (), full2)],
         "Y6": [str(x) for x in col(S1, t_d27c(Fr(1, 2)), frozenset(fk), a, fk)],
         "Y7": str(hv(TMt, A5, TMt.chain(um(0)), um(0), um(0)))}
    res["instances"] = Y
    R = {
        "R1": se_ok(TMt, T_fam(TMt, 0, Fr(1, 2)), 0),
        "R2": ranges["FULL|TB|1|none"]["A[r.0|r]"][1] == "0",
        "R3": sx_ok(TMt, T_cone(TMt, um(0), Fr(1, 2)), 0),
        "R4": rows_ok(A5, TMt, FR["TM"]),
        "R5": any(ranges[k]["A[%s|%s]" % (astr(x), astr(ac(m)))][1] == "0" for (k, m, x) in
                  (("DROPF|TM|2|SE|0,r.1", 0, (1,)), ("DROPF|TM|2|SE|0,r.2", 0, (2,)), ("DROPF|TM|2|SE|1,r.0.1", 1, (0, 1)))),
        "R6": fc_ok(S2, t_d27b(Fr(1, 2)), 1),
        "R7": all(hv(S1, t_d27c(Fr(1, 2)), frozenset(fk), v, a) >= 0 for v in fk),
        "R8": hist(Fr(3, 2))[0],
        "R9": any(TMt.ix[(um(0), um(0))] in r for r in rest_rows(TMt, 2)) or any(TMt.ix[(um(0), um(0))] in e for e, _ in eq_rows(TMt, 2, "SE")),
        "R10": fc_ok(TMt, T_fam(TMt, 1, Fr(1, 2)), 2, ms=[1]),
    }
    res["controls"] = {k: ("ACCEPTED" if v else "REJECTED") for k, v in R.items()}
    try: res["result_sha256"] = hashlib.sha256(open(ROOTP, "rb").read()).hexdigest()
    except OSError: res["result_sha256"] = None
    with open(outp, "w") as f: json.dump(res, f, indent=1, sort_keys=True)
    print("certified", allcert, "systems", len(ranges), "entries", sum(len(v) for v in ranges.values()))

if __name__ == "__main__": main(sys.argv[1])
