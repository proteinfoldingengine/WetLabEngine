"""receiver_identification d27 freeze (sections 31-32): CHECKER (independent of the producer; no LP). Bitmask enumeration of
parent-closed vertex sets, own holding forms, each bounded range end by the proofs' multiplier certificates (fork sandwich,
telescoping chains, chain row at a_m, SE/SX equalities) on named carriers of the system's own row set, unbounded ends by
absence of the target from every row, attainment by explicit exact tables checked against every row of the system."""
import hashlib, json, sys
from fractions import Fraction as Q

ROOTP = "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d27_review/RESULT.md"
VIOL = []


def note(ok, msg):
    if not ok: VIOL.append(msg)
    return ok


def build(name):
    # address list in breadth-first order from explicit child counts
    def nk(v):
        if name == "TB": return 2 if len(v) < 3 else 0
        if name == "TM": return 3 if len(v) == 0 else (2 if len(v) < 3 else 0)
        if name == "S1": return 2 if len(v) == 0 else 0
        if name == "S2": return 2 if len(v) == 0 else (1 if v == (0,) else 0)
    A, frontier = [()], [()]
    while frontier:
        nxt = []
        for v in frontier:
            for i in range(nk(v)): nxt.append(v + (i,))
        A += nxt; frontier = nxt
    return A, nk


class Tr:
    def __init__(self, name):
        self.name = name
        self.A, self.nk = build(name)
        self.pos = {v: i for i, v in enumerate(self.A)}
        n = len(self.A)
        par = [None] + [self.pos[v[:-1]] for v in self.A[1:]]
        # enumerate parent-closed subsets containing root by extension in BFS order
        cars = []
        def rec(i, mask):
            if i == n: cars.append(mask); return
            rec(i + 1, mask)
            if mask >> par[i] & 1: rec(i + 1, mask | (1 << i))
        rec(1, 1)
        self.cars = [frozenset(self.A[i] for i in range(n) if m >> i & 1) for m in cars]
        self.leaves = [v for v in self.A if self.nk(v) == 0]
    def kids(self, W, v): return [v + (i,) for i in range(self.nk(v)) if v + (i,) in W]
    def var_count(self): return sum(len(v) + 1 for v in self.A)


def lca(v, z):
    k = 0
    for x, y in zip(v, z):
        if x != y: break
        k += 1
    return v[:k]


def H(T, W, v, z):
    """holding form of v under e_z on W: dict (v,w) -> coefficient (no constant)."""
    f = {(v, lca(v, z)): Q(1)}
    for u in T.kids(W, v):
        key = (u, lca(u, z)); f[key] = f.get(key, Q(0)) - 1
    return {k: c for k, c in f.items() if c}


def add(*fs):
    out = {}
    for c, f in fs:
        for k, x in f.items(): out[k] = out.get(k, Q(0)) + c * x
    return {k: x for k, x in out.items() if x}


def s(v): return "r" + "".join("." + str(i) for i in v)


def a(d): return (0,) * d


def um(m): return (0,) * m + (1,)


def sb(x, v): return len(x) > len(v) and x[:len(v)] == v


def chain(v): return frozenset(v[:i] for i in range(len(v) + 1))


def fork(m, x): return frozenset(list(chain(a(m))) + [a(m + 1), x])


class System:
    def __init__(self, T, kind, D, cond, extra=None):
        self.T, self.kind, self.D, self.cond, self.extra = T, kind, D, cond, extra
        self.allowed = set()  # (carrier, unit) pairs whose holdings are rows
        if kind == "FULL":
            for W in T.cars:
                for z in W: self.allowed.add((W, z))
            self.carset = set(T.cars)
        else:
            self.carset = set()
            self.allowed.add((frozenset([()]), ())); self.carset.add(frozenset([()]))
            for m in range(D):
                for i in range(T.nk(a(m))):
                    x = a(m) + (i,)
                    if x == a(m + 1) or (kind == "DROPF" and (m, x) == extra): continue
                    F = fork(m, x); self.carset.add(F)
                    for j in range(m + 2): self.allowed.add((F, a(j)))
            for l in T.leaves:
                if kind == "DROPC" and l[:len(extra[0])] == extra[0]: continue
                C = chain(l); self.carset.add(C)
                for j in range(D):
                    if a(j) in C: self.allowed.add((C, a(j)))
        self.eqs = {"norm": ({((), ()): Q(1)}, Q(1))}
        for d in range(1, D + 1): self.eqs["Bl%d" % d] = ({(a(d), a(d)): Q(1), (a(d - 1), a(d - 1)): Q(-1)}, Q(0))
        for m in range(D):
            F = fork(m, um(m))
            if cond == "SE": self.eqs["SE%d" % m] = (add((1, H(T, F, a(m + 1), a(m))), (-1, H(T, F, um(m), a(m)))), Q(0))
            if cond == "SX":
                sg = lambda x: um(m) if x == a(m + 1) else (a(m + 1) if x == um(m) else x)
                for v in F:
                    for z in F:
                        self.eqs["SX%d|%s|%s" % (m, s(v), s(z))] = (add((1, H(T, F, sg(v), sg(z))), (-1, H(T, F, v, z))), Q(0))
    def row(self, W, v, z):
        note((W, z) in self.allowed and v in W, ("row not in system", self.kind, sorted(W), v, z))
        return H(self.T, W, v, z)
    def all_rows(self):
        return [H(self.T, W, v, z) for (W, z) in self.allowed for v in W]
    def leaf_through(self, x):
        for l in self.T.leaves:
            if l[:len(x)] == x and chain(l) in self.carset: return chain(l)
        return None
    # --- certificates: return (form, const) meaning  form + const >= 0 is implied, as a combination (lam>=0 on rows, any mu on eqs)
    def tele(self, top, x, unit):
        """sum of holdings of e_unit on a root-to-leaf chain through x, from top down to (excluding) x: = A[top|unit∧top] - A[x|...]."""
        L = self.leaf_through(x)
        note(L is not None, ("no chain", s(x)))
        f = {}; y = top
        while y != x:
            f = add((1, f), (1, self.row(L, y, unit)))
            y = x[:len(y) + 1]
        return f
    def tele_to_leaf(self, x, unit):
        L = self.leaf_through(x)
        note(L is not None, ("no chain", s(x)))
        leaf = max(L, key=len); f = {}; y = x
        while True:
            f = add((1, f), (1, self.row(L, y, unit)))
            if y == leaf: break
            y = leaf[:len(y) + 1]
        return f


def eqv(sysm, f, const, target, lo_or_hi, b):
    """check identity: for 'hi', b - target == f + const ; for 'lo', target - b == f + const (f a nonneg combination)."""
    t = {target: Q(1)}
    lhs = add((-1, t), ) if lo_or_hi == "hi" else dict(t)
    lhs_const = Q(b) if lo_or_hi == "hi" else -Q(b)
    return lhs == {k: x for k, x in f.items() if x} and lhs_const == const


def cert(sysm, var, end):
    """returns (value string or None, ok). Builds the proof's certificate for this end."""
    T, D, c = sysm.T, sysm.D, sysm.cond
    x, w = var
    E = sysm.eqs
    def eqf(name, mult):  # mult * (form - rhs) == 0 contributes form*mult, const -mult*rhs
        f, r = E[name]; return ({k: mult * v for k, v in f.items()}, -mult * r)
    def combine(parts):
        f, cst = {}, Q(0)
        for pf, pc in parts: f = add((1, f), (1, pf)); cst += pc
        return f, cst
    def diag_eq(d):  # A[a_d|a_d] - 1 == sum Bl + norm  -> returns (form, const) of A[a_d|a_d] - 1
        return combine([eqf("norm", Q(1))] + [eqf("Bl%d" % i, Q(1)) for i in range(1, d + 1)])
    # diagonal of climb
    if x == w and x == a(len(x)) and len(x) <= D:
        f, cst = diag_eq(len(x))
        if end == "lo": return "1", eqv(sysm, f, cst, var, "lo", 1)
        g = {k: -v for k, v in f.items()}; return "1", eqv(sysm, g, -cst, var, "hi", 1)
    m = len(w)
    # side-subtree entry (or dropped-fork entry)
    if w == a(m) and m < D and sb(x, w) and not (x == a(m + 1) or sb(x, a(m + 1))):
        u = x[:m + 1]
        if end == "lo":
            return "0", eqv(sysm, sysm.tele_to_leaf(x, w), Q(0), var, "lo", 0)
        if sysm.kind == "DROPF" and (m, u) == sysm.extra:
            L = sysm.leaf_through(u)
            f, cst = combine([(sysm.row(L, a(m), a(m)), Q(0)), eqf("norm", Q(-1))] + [eqf("Bl%d" % i, Q(-1)) for i in range(1, m + 1)])
            return "1", eqv(sysm, f, cst, var, "hi", 1)
        # fork sandwich: -A[u|a_m] = h_{a_m}(e_{a_{m+1}}) on F(m,u) + Bl_{m+1}
        f, cst = combine([(sysm.row(fork(m, u), a(m), a(m + 1)), Q(0)), eqf("Bl%d" % (m + 1), Q(1))])
        if x != u: f = add((1, f), (1, sysm.tele(u, x, w)))
        return "0", eqv(sysm, f, cst, var, "hi", 0)
    # entries at or below a_{m+1}
    if w == a(m) and m < D and (x == a(m + 1) or sb(x, a(m + 1))):
        if end == "lo": return "0", eqv(sysm, sysm.tele_to_leaf(x, w), Q(0), var, "lo", 0)
        L = sysm.leaf_through(a(m + 1))
        if c in ("SE", "SX"):
            if sysm.kind == "DROPF" and (m, um(m)) == sysm.extra:
                Lu = sysm.leaf_through(um(m))
                base = combine([eqf("SE%d" % m, Q(-1)), (sysm.row(Lu, a(m), a(m)), Q(0)), eqf("norm", Q(-1))] + [eqf("Bl%d" % i, Q(-1)) for i in range(1, m + 1)])
                f = base[0] if x == a(m + 1) else add((1, base[0]), (1, sysm.tele(a(m + 1), x, w)))
                return "1", eqv(sysm, f, base[1], var, "hi", 1)
            # -t_m = -SE_m - A[u_m|a_m] ; -A[u_m|a_m] from the fork sandwich (or SX equality)
            if c == "SE":
                base = combine([eqf("SE%d" % m, Q(-1)), (sysm.row(fork(m, um(m)), a(m), a(m + 1)), Q(0)), eqf("Bl%d" % (m + 1), Q(1))])
            else:
                base = combine([eqf("SX%d|%s|%s" % (m, s(a(m + 1)), s(a(m))), Q(1)), (sysm.row(fork(m, um(m)), a(m), a(m + 1)), Q(0)), eqf("Bl%d" % (m + 1), Q(1))])
            f = base[0] if x == a(m + 1) else add((1, base[0]), (1, sysm.tele(a(m + 1), x, w)))
            return "0", eqv(sysm, f, base[1], var, "hi", 0)
        # none: 1 - t_m = h_{a_m}(e_{a_m}) on a chain through a_{m+1} + (1 - A[a_m|a_m])
        f, cst = combine([(sysm.row(L, a(m), a(m)), Q(0)), eqf("norm", Q(-1))] + [eqf("Bl%d" % i, Q(-1)) for i in range(1, m + 1)])
        if x != a(m + 1): f = add((1, f), (1, sysm.tele(a(m + 1), x, w)))
        return "1", eqv(sysm, f, cst, var, "hi", 1)
    # side child's own diagonal
    if x == w and x == um(m - 1) and sysm.kind == "FULL":
        mm = m - 1
        if end == "lo": return "0", eqv(sysm, sysm.tele_to_leaf(x, x), Q(0), var, "lo", 0)
        if c == "SX":
            f, cst = combine([eqf("SX%d|%s|%s" % (mm, s(a(mm + 1)), s(a(mm + 1))), Q(-1))] + [eqf("norm", Q(-1))] + [eqf("Bl%d" % i, Q(-1)) for i in range(1, mm + 2)])
            if end == "hi": return "1", eqv(sysm, f, cst, var, "hi", 1)
        L = sysm.leaf_through(x)
        f, cst = combine([(sysm.row(L, a(mm), x), Q(0)), eqf("norm", Q(-1))] + [eqf("Bl%d" % i, Q(-1)) for i in range(1, mm + 1)])
        return "1", eqv(sysm, f, cst, var, "hi", 1)
    return None, False


def sx_lo(sysm, var):
    # SX: A[u_m|u_m] - 1 = SX(a_{m+1},a_{m+1}) + diag eq
    T = sysm.T; m = len(var[0]) - 1
    f, r = sysm.eqs["SX%d|%s|%s" % (m, s(a(m + 1)), s(a(m + 1)))]
    g = add((1, f), (1, sysm.eqs["norm"][0]), *[(1, sysm.eqs["Bl%d" % i][0]) for i in range(1, m + 2)])
    return g == {var: Q(1)}


def val(A, f): return sum((c * A.get(k, Q(0)) for k, c in f.items()), Q(0))


def tab_id(T): return {(v, v): Q(1) for v in T.A}


def tab_fam(T, m, t):
    A = tab_id(T); A[(a(m + 1), a(m))] = Q(t)
    for v in T.A:
        if sb(v, a(m)) and v != a(m + 1) and not sb(v, a(m + 1)): A[(v, v)] = Q(1) - Q(t)
    return A


def tab_cone(T, u, q):
    A = tab_id(T)
    for v in T.A:
        if v == u or sb(v, u): A[(v, v)] = Q(q)
    return A


def sat(sysm, A, rows):
    return all(val(A, r) >= 0 for r in rows) and all(val(A, f) == rhs for f, rhs in sysm.eqs.values())


def hv(T, A, W, v, z): return val(A, H(T, W, v, z))


def main(outp):
    TT = {n: Tr(n) for n in ("TB", "TM", "S1", "S2")}
    out = {"role": "checker", "classes": {}}
    for n, T in TT.items():
        lines = sorted(",".join(sorted(s(v) for v in W)) for W in T.cars)
        out["classes"][n] = {"carriers": len(T.cars), "digest": hashlib.sha256("\n".join(lines).encode()).hexdigest(), "vars": T.var_count()}
    FULLR = {}
    for n in TT:
        S = set()
        for W in TT[n].cars:
            for v in W:
                for z in W:
                    f = H(TT[n], W, v, z)
                    if f: S.add(tuple(sorted(f.items())))
        FULLR[n] = [dict(x) for x in S]
    out["full_pos_rows"] = {"TB": len(FULLR["TB"]), "TM": len(FULLR["TM"])}
    systems = []
    for tn in ("TB", "TM"):
        for D in (1, 2, 3):
            for c in ("none", "SE", "SX"): systems.append(("FULL", tn, D, c, None))
    for D in (1, 2, 3):
        for c in ("none", "SE"): systems.append(("REST", "TM", D, c, None))
    for e in ((0, (1,)), (0, (2,)), (1, (0, 1))): systems.append(("DROPF", "TM", 2, "SE", e))
    for e in (((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)): systems.append(("DROPC", "TM", 2, "SE", e))
    ranges = {}; lp_only = []
    for (kind, tn, D, c, e) in systems:
        T = TT[tn]; sysm = System(T, kind, D, c, e)
        rows = FULLR[tn] if kind == "FULL" else [r for r in sysm.all_rows() if r]
        key = "%s|%s|%d|%s" % (kind, tn, D, c)
        if kind == "DROPF": key += "|%d,%s" % (e[0], s(e[1]))
        if kind == "DROPC": key += "|%s,%d" % (s(e[0]), e[1])
        # targets
        tg = []
        if kind in ("FULL", "REST"):
            tg += [(a(d), a(d)) for d in range(D + 1)]
            for m in range(D):
                tg += [(x, a(m)) for x in T.A if sb(x, a(m)) and x != a(m + 1) and not sb(x, a(m + 1))]
                tg.append((a(m + 1), a(m)))
                if c != "none" or (kind == "FULL" and tn == "TB"): tg += [(x, a(m)) for x in T.A if sb(x, a(m + 1))]
                tg.append((um(m), um(m)))
        elif kind == "DROPF":
            m, u = e; tg.append((u, a(m)))
            if u == um(m): tg.append((a(m + 1), a(m)))
        else:
            tg.append((e[0], a(e[1])))
        cands = [tab_id(T)] + [tab_fam(T, m, 1) for m in range(D)] + [tab_cone(T, um(m), 0) for m in range(D)]
        if kind == "DROPF":
            A1 = tab_id(T); A1[(e[1], a(e[0]))] = Q(1)
            if e[1] == um(e[0]): A1[(a(e[0] + 1), a(e[0]))] = Q(1)
            cands.append(A1)
        feas = [A for A in cands if sat(sysm, A, rows)]
        note(len(feas) >= 1, ("no feasible table", key))
        r = {}
        for var in tg:
            name = "A[%s|%s]" % (s(var[0]), s(var[1]))
            absent = all(var not in f for f in rows) and all(var not in f for f, _ in sysm.eqs.values())
            if kind == "REST" and var[0] == var[1] and var[0] == um(len(var[0]) - 1) or kind == "DROPC":
                note(absent, ("not absent", key, name)); r[name] = ["-inf", "inf"]; continue
            ends = []
            for end in ("lo", "hi"):
                if kind == "FULL" and c == "SX" and var[0] == var[1] and var[0] != a(len(var[0])) and end == "lo":
                    note(sx_lo(sysm, var), ("SX lo cert", key, name)); v = "1"
                else:
                    v, ok = cert(sysm, var, end); note(ok, ("cert", key, name, end, v))
                ends.append(v)
                attained = any(A.get(var, Q(0)) == Q(v) for A in feas) if v is not None else False
                if not attained:
                    if kind == "FULL" and tn == "TB" and c == "none" and end == "hi" and sb(var[0], a(len(var[1]) + 1)):
                        lp_only.append("%s|%s" % (key, name))
                    else:
                        note(False, ("not attained", key, name, end))
            r[name] = ends
        ranges[key] = r
    out["ranges"] = ranges; out["lp_only_upper_ends"] = sorted(lp_only)
    # ---------- tables ----------
    TB, TM, S1, S2 = TT["TB"], TT["TM"], TT["S1"], TT["S2"]
    def allpos(T, A): return all(val(A, f) >= 0 for f in FULLR[T.name])
    def bl(T, A, D): return A.get(((), ()), 0) == 1 and all(hv(T, A, chain(a(d)), a(d - 1), a(d)) == 0 for d in range(1, D + 1))
    def se(T, A, m): F = fork(m, um(m)); return hv(T, A, F, a(m + 1), a(m)) == hv(T, A, F, um(m), a(m))
    def sx(T, A, m):
        F = fork(m, um(m)); g = lambda x: um(m) if x == a(m + 1) else (a(m + 1) if x == um(m) else x)
        return all(hv(T, A, F, g(v), g(z)) == hv(T, A, F, v, z) for v in F for z in F)
    def fc(T, A, D, ms=None):
        for W in T.cars:
            for m in (range(D + 1) if ms is None else ms):
                z = a(m)
                if z not in W or (m == D and T.kids(W, z)): continue
                for v in W:
                    if hv(T, A, W, v, z) != (1 if v == z else 0): return False
        return True
    def posT(T, A, D, kind="REST", e=None):
        sm = System(T, kind, D, "SE", e)
        return all(hv(T, A, W, v, z) >= 0 for (W, z) in sm.allowed for v in W)
    X = {}
    ok = True
    for T in (TB, TM):
        for m in range(3):
            for t in (Q(1, 3), Q(1, 2), Q(1)):
                A = tab_fam(T, m, t); F = fork(m, um(m))
                ok &= allpos(T, A) and bl(T, A, 3) and hv(T, A, chain(a(m + 1)), a(m + 1), a(m)) == t
                ok &= hv(T, A, F, a(m + 1), a(m)) == t and hv(T, A, F, um(m), a(m)) == 0 and not se(T, A, m)
    X["X1"] = ok
    X["X2"] = all(allpos(TM, A) and bl(TM, A, 2) and se(TM, A, 0) and se(TM, A, 1) and fc(TM, A, 2) and not sx(TM, A, 0)
                  for A in (tab_cone(TM, um(0), q) for q in (Q(0), Q(1, 3), Q(1, 2))))
    o, p_, c2, u = (), (0,), (0, 0), (1,)
    full = frozenset([o, p_, c2, u]); order = [o, p_, c2, u]
    def colv(T, A, W, z, order): return [hv(T, A, W, v, z) for v in order]
    ok = True
    for r in (Q(1, 3), Q(1, 2), Q(1)):
        A = tab_id(S2); A[(c2, p_)] = r
        ok &= allpos(S2, A) and bl(S2, A, 1) and sx(S2, A, 0) and colv(S2, A, full, p_, order) == [0, 1 - r, r, 0]
        for W in (frozenset([o, p_]), frozenset([o, p_, u])):
            ok &= all(hv(S2, A, W, v, p_) == (1 if v == p_ else 0) for v in W)
    X["X3"] = ok
    def bot(sv, t): return {(o, o): Q(1), (p_, o): t, (p_, p_): Q(1), (u, o): Q(0), (u, u): 1 - t, (c2, o): sv, (c2, p_): sv, (c2, c2): Q(1)}
    X["X4"] = all(allpos(S2, bot(sv, t)) and bl(S2, bot(sv, t), 1) and colv(S2, bot(sv, t), full, o, order) == [1 - t, t - sv, sv, 0]
                  for sv, t in ((Q(0), Q(1, 2)), (Q(1, 4), Q(1, 2)), (Q(1, 2), Q(1, 2)), (Q(0), Q(0)), (Q(1, 3), Q(1))))
    A5 = tab_id(TM); A5[(um(0), um(0))] = Q(-1)
    X["X5"] = posT(TM, A5, 2) and bl(TM, A5, 2) and se(TM, A5, 0) and se(TM, A5, 1) and fc(TM, A5, 2) and \
        hv(TM, A5, chain(um(0)), um(0), um(0)) == -1 and not allpos(TM, A5)
    ok = True
    for (m, x) in ((0, (1,)), (0, (2,)), (1, (0, 1))):
        for eps in (Q(1, 2), Q(1)):
            A = tab_id(TM); A[(x, a(m))] = eps
            if x == um(m): A[(a(m + 1), a(m))] = eps
            ok &= posT(TM, A, 2, "DROPF", (m, x)) and bl(TM, A, 2) and se(TM, A, 0) and se(TM, A, 1)
            ok &= (not posT(TM, A, 2)) and not fc(TM, A, 2)
    X["X6"] = ok
    ok = True
    for (cc, m) in (((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)):
        A = tab_id(TM); A[(cc, a(m))] = Q(1, 2)
        ok &= posT(TM, A, 2, "DROPC", (cc, m)) and bl(TM, A, 2) and se(TM, A, 0) and se(TM, A, 1)
        ok &= (not posT(TM, A, 2)) and (not fc(TM, A, 2)) and hv(TM, A, chain(cc), cc, a(m)) == Q(1, 2)
    X["X7"] = ok
    def d27b(sv): A = tab_id(S2); A[(c2, o)] = sv; return A
    ok = True
    for sv in (Q(1, 2), Q(1)):
        A = d27b(sv)
        ok &= bl(S2, A, 1) and se(S2, A, 0)
        for W in (frozenset([o, p_]), frozenset([o, p_, u]), frozenset([o]), frozenset([o, u])):
            ok &= all(hv(S2, A, W, v, z) == (1 if v == z else 0) for v in W for z in W)
        ok &= colv(S2, A, full, o, order) == [1, -sv, sv, 0] and not fc(S2, A, 1) and not posT(S2, A, 1)
    X["X8"] = ok
    def d27c(eps): A = tab_id(S1); A[(p_, o)] = eps; A[(u, o)] = eps; return A
    fk = frozenset([o, p_, u]); fo = [o, p_, u]
    X["X9"] = all(bl(S1, d27c(eps), 1) and se(S1, d27c(eps), 0) and all(hv(S1, d27c(eps), W, v, o) >= 0 for W in S1.cars for v in W)
                  and colv(S1, d27c(eps), fk, p_, fo) == [-eps, 1, eps] for eps in (Q(1, 4), Q(1, 2)))
    A10 = tab_fam(TM, 1, Q(1, 2)); ok = not se(TM, A10, 1)
    for d in (1, 2):
        for W in TM.cars:
            if a(d) in W and not TM.kids(W, a(d)):
                Y = W - {a(d)}
                ok &= all(hv(TM, A10, W, v, a(d)) == (1 if v == a(d) else 0) for v in W)
                ok &= all(hv(TM, A10, Y, v, a(d - 1)) == (1 if v == a(d - 1) else 0) for v in Y)
    X["X10"] = ok and not fc(TM, A10, 2, ms=[1])
    # X11: history; F as a map on grade vectors over chain vertices 0..n-1
    def hist(t):
        res = [True, True, True]
        for n in (3, 2):
            l, p = n - 1, n - 2
            def F(x):
                y = list(x); y[l] = x[l] + t * x[p]; y[p] = x[p] - t * x[p]; return y
            units = [[Q(1) if i == j else Q(0) for i in range(n)] for j in range(n)]
            res[0] &= all(c_ >= 0 for e in units for c_ in F(e))
            res[1] &= F(units[l])[p] == 0
            for e in units:
                Fe = F(e); Pfe = Fe[:n - 1]; Pfe[p] += Fe[l]
                Pe = e[:n - 1]; Pe[p] += e[l]
                res[2] &= Pfe == Pe
        return res
    X["X11"] = all(all(hist(t)) for t in (Q(0), Q(1, 2), Q(1))) and all(hist(t) == [False, True, True] for t in (Q(-1, 2), Q(3, 2)))
    def pn(T, A):
        for W in T.cars:
            for l in W:
                if l == () or T.kids(W, l): continue
                Y = W - {l}; p = l[:-1]
                for z in W:
                    Pz = p if z == l else z
                    for v in Y:
                        want = hv(T, A, W, v, z) + (hv(T, A, W, l, z) if v == p else 0)
                        if hv(T, A, Y, v, Pz) != want: return False
        return True
    X["X12"] = pn(TB, tab_id(TB)) and pn(TB, tab_fam(TB, 0, Q(1, 2))) and pn(S2, bot(Q(1, 4), Q(1, 2))) and pn(S2, tab_id(S2))
    out["tables"] = X
    A = tab_fam(TB, 0, Q(1, 2)); F0 = fork(0, um(0))
    out["instances"] = {
        "Y1": [str(hv(TB, A, chain(a(1)), a(1), o)), str(hv(TB, A, F0, a(1), o)), str(hv(TB, A, F0, um(0), o))],
        "Y2": [str(x) for x in colv(TM, tab_cone(TM, um(0), Q(1, 3)), fork(0, um(0)), um(0), [o, (0,), (1,)])],
        "Y3": [str(x) for x in colv(S2, bot(Q(1, 4), Q(1, 2)), full, o, order)],
        "Y4": [str(x) for x in colv(S2, {**tab_id(S2), (c2, p_): Q(1, 2)}, full, p_, order)],
        "Y5": [str(x) for x in colv(S2, d27b(Q(1, 2)), full, o, order)],
        "Y6": [str(x) for x in colv(S1, d27c(Q(1, 2)), fk, p_, fo)],
        "Y7": str(hv(TM, A5, chain(um(0)), um(0), um(0)))}
    sm = System(TM, "REST", 2, "SE")
    R = {"R1": se(TM, tab_fam(TM, 0, Q(1, 2)), 0),
         "R2": ranges["FULL|TB|1|none"]["A[r.0|r]"][1] == "0",
         "R3": sx(TM, tab_cone(TM, um(0), Q(1, 2)), 0),
         "R4": allpos(TM, A5),
         "R5": any(ranges[k][n][1] == "0" for k, n in (("DROPF|TM|2|SE|0,r.1", "A[r.1|r]"), ("DROPF|TM|2|SE|0,r.2", "A[r.2|r]"),
                                                       ("DROPF|TM|2|SE|1,r.0.1", "A[r.0.1|r.0]"))),
         "R6": fc(S2, d27b(Q(1, 2)), 1),
         "R7": all(hv(S1, d27c(Q(1, 2)), fk, v, p_) >= 0 for v in fk),
         "R8": hist(Q(3, 2))[0],
         "R9": any((um(0), um(0)) in f for f in sm.all_rows()) or any((um(0), um(0)) in f for f, _ in sm.eqs.values()),
         "R10": fc(TM, tab_fam(TM, 1, Q(1, 2)), 2, ms=[1])}
    out["controls"] = {k: ("ACCEPTED" if v else "REJECTED") for k, v in R.items()}
    out["violations"] = len(VIOL)
    try: out["result_sha256"] = hashlib.sha256(open(ROOTP, "rb").read()).hexdigest()
    except OSError: out["result_sha256"] = None
    with open(outp, "w") as f: json.dump(out, f, indent=1, sort_keys=True)
    print("violations", len(VIOL), VIOL[:10])


if __name__ == "__main__": main(sys.argv[1])
