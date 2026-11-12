"""receiver_identification draft 9 (sec 16) freeze: CHECKER. Independent algorithm: trees grown by appending the next
label, carriers and prefix sets as bitmasks, longest retained prefix as the highest set bit of (prefix mask & Y),
rules as integer-scaled numpy column matrices (scale 2, normalized before every comparison with exact maps), all
single-pruning sequences covered by dynamic programming over the lattice of intermediate carriers (path counts and
edge-consistency of composites instead of explicit sequences), vectorized condition tests, grid brute force for
Theorem 16.1, bounded random evidence and rejecting controls. Preregistration: FREEZE.md (committed before this code)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d9_review")
PANEL = ["P1", "genesis", "grandparent", "halfsplit", "erase", "double", "fixed_e2", "leafshift", "dipole", "sign"]
LAT_RULES = ["P1", "genesis", "grandparent", "halfsplit"]
S = 2  # integer scale of every rule matrix


def q(num, den=1):
    x = F(int(num), int(den))
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def grow(nmax):
    """All parent arrays parent[i] < i with n <= nmax, grown label by label."""
    level = [(None,)]
    out = {1: level}
    for n in range(2, nmax + 1):
        level = [t + (p,) for t in level for p in range(n - 1)]
        out[n] = level
    return out


class Tree:
    def __init__(self, par):
        self.par = par
        self.n = n = len(par)
        self.pre = [0] * n  # prefix mask including v
        for v in range(n):
            self.pre[v] = (1 << v) | (self.pre[par[v]] if v else 0)
        self.kids = [0] * n
        for v in range(1, n):
            self.kids[par[v]] |= 1 << v
        self.full = (1 << n) - 1

    def key(self):
        return "%d:%s" % (self.n, ",".join(str(p) for p in self.par[1:]))

    def carrier(self, W):
        if not (W & 1):
            return False
        for v in range(self.n):
            if (W >> v) & 1 and (self.pre[v] & ~W):
                return False
        return True

    def carriers(self):
        return [W for W in range(1, self.full + 1) if self.carrier(W)]

    def proper_anc(self, v):  # nearest first: descending labels
        m = self.pre[v] & ~(1 << v)
        return [b for b in range(self.n - 1, -1, -1) if (m >> b) & 1]

    def lp(self, Y, v):
        return (self.pre[v] & Y).bit_length() - 1

    def Pmat(self, Y):
        M = np.zeros((self.n, self.n), dtype=np.int64)
        for v in range(self.n):
            M[self.lp(Y, v), v] = 1
        return M

    def leaf(self, W, l):
        return l != 0 and not (self.kids[l] & W)


def bits(m):
    return [b for b in range(m.bit_length()) if (m >> b) & 1]


def col(t, rule, W, l, jvec=None):
    """Scaled column 2*T(e_l) for rule (linear rules), length n."""
    c = np.zeros(t.n, dtype=np.int64)
    a = t.proper_anc(l)
    k = len(a)
    if rule == "P1":
        c[a[0]] = S
    elif rule == "genesis":
        c[0] = S
    elif rule == "grandparent":
        c[a[1] if k >= 2 else 0] = S
    elif rule == "halfsplit":
        if k == 1:
            c[0] = S
        else:
            c[a[0]] += S // 2; c[a[1]] += S // 2
    elif rule == "erase":
        pass
    elif rule == "double":
        c[a[0]] = 2 * S
    elif rule == "fixed_e2":
        if k >= 2:
            c[a[1]] = S
    elif rule == "dipole":
        c[a[0]] = S
        na = [b for b in bits(W & ~(1 << l) & ~t.pre[l])]
        if len(na) >= 2:
            c[na[0]] += S; c[na[1]] -= S
    elif rule == "jump":
        c[a[jvec[k - 1] - 1]] = S
    else:
        raise ValueError(rule)
    return c


def mat(t, rule, W, l, jvec=None):
    M = S * np.eye(t.n, dtype=np.int64)
    if rule == "leafshift":
        for v in bits(W):
            if t.leaf(W, v):
                M[:, v] = 0
                M[t.proper_anc(v)[0], v] = S
        return M
    M[:, l] = col(t, rule, W, l, jvec)
    return M


def applyT(t, rule, W, l, Z):
    """Scaled 2*T applied to the rows of Z (batch, n)."""
    if rule == "sign":
        Z = np.asarray(Z, dtype=np.int64)
        out = S * Z.copy()
        zl = Z[:, l].copy()
        out[:, l] = 0
        par = t.proper_anc(l)[0]
        pos = zl >= 0
        out[pos, par] += S * zl[pos]
        out[~pos, 0] += S * zl[~pos]
        return out
    return np.asarray(Z, dtype=np.int64) @ mat(t, rule, W, l).T


def vecs(t, W, Z2):
    """Scaled integer vector -> list of exact strings on carrier W."""
    return [q(Z2[v], S) for v in bits(W)]


# ---------- exact instances ----------
def instances():
    V = {}
    t = Tree((None, 0, 1)); W = 0b111; Y = 0b011
    x = np.array([[3, 5, 7]])
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        V["X1." + r] = vecs(t, Y, applyT(t, r, W, 2, x)[0])
    for r in ("P1", "genesis", "grandparent"):
        V["X1.receiver_" + r] = int(np.flatnonzero(col(t, r, W, 2))[0])
    t = Tree((None, 0, 1, 0)); W = 0b1111; Y = 0b1011
    xp, xm = np.array([0, 0, 1, 0]), np.array([0, 0, 0, 1])
    Tp, Tm = applyT(t, "P1", W, 2, [xp])[0], applyT(t, "P1", W, 2, [xm])[0]
    V["X2.p_before"] = [q(xp[1]), q(xm[1])]
    V["X2.T_plus"], V["X2.T_minus"] = vecs(t, Y, Tp), vecs(t, Y, Tm)
    V["X2.p_after"] = [q(Tp[1], S), q(Tm[1], S)]
    V["X2.totals"] = [q(xp.sum()), q(Tp.sum(), S), q(xm.sum()), q(Tm.sum(), S)]
    for r in ("genesis", "grandparent", "halfsplit"):
        a, b = applyT(t, r, W, 2, [xp])[0], applyT(t, r, W, 2, [xm])[0]
        V["X2.p_after_" + r] = [q(a[1], S), q(b[1], S)]
    x = np.array([1, -2, 3, 4]); xq = x + np.array([0, 0, -5, 0])
    Tx, Tq = applyT(t, "P1", W, 2, [x])[0], applyT(t, "P1", W, 2, [xq])[0]
    V["X3.Tx"], V["X3.Txp"], V["X3.diff"] = vecs(t, Y, Tx), vecs(t, Y, Tq), vecs(t, Y, Tq - Tx)
    V["X3.changed_before"] = [int(v) for v in np.flatnonzero(x != xq)]
    V["X3.changed_after"] = [v for v in bits(Y) if Tx[v] != Tq[v]]
    V["X3.totals"] = [q(x.sum()), q(Tx.sum(), S), q(xq.sum()), q(Tq.sum(), S)]
    sols, depths = grid_bruteforce()
    V["X4.w"] = [q(a, S) for a in sols[0]] if len(sols) == 1 else ["NONUNIQUE"]
    V["X4.depths"] = depths
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        rows = []
        for k in (1, 2, 3):
            tc = Tree((None,) + tuple(range(k)))
            c = col(tc, r, tc.full, k)
            rows.append([q(c[a], S) for a in tc.proper_anc(k)])
        V["X5." + r] = rows
    t6 = Tree((None, 0, 1, 1, 0, 4)); Y6 = 0b11
    x6 = np.arange(1, 7)
    comps, paths, _, _ = lattice(t6, Y6, LAT_RULES)
    V["X6.orders"] = int(paths)
    D = t6.full & ~Y6
    V["X6.maximal"] = [m for m in bits(D) if not any((t6.pre[c] >> m) & 1 for c in bits(D) if c != m)]
    V["X6.r"] = [t6.lp(Y6, v) for v in range(6)]
    m = bin(D).count("1")
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        out = comps[r] @ x6
        V["X6." + r] = [q(out[v], S ** m) for v in bits(Y6)]
    V["X7.removable"] = [l for l in range(6) if t6.carrier(t6.full & ~(1 << l))]
    V["X7.genesis_removable"] = 0 in V["X7.removable"]
    t = Tree((None, 0, 1)); W = 0b111; Y = 0b011
    a, b = applyT(t, "sign", W, 2, [[0, 0, 1]])[0], applyT(t, "sign", W, 2, [[0, 0, -1]])[0]
    V["X8.T_plus"], V["X8.T_minus"], V["X8.neg_T_plus"] = vecs(t, Y, a), vecs(t, Y, b), vecs(t, Y, -a)
    t = Tree((None, 0, 1, 0)); W = 0b1111; Y = 0b1011
    V["X9.T_e3"] = vecs(t, Y, applyT(t, "leafshift", W, 2, [[0, 0, 0, 1]])[0])
    V["X9.T_e1"] = vecs(t, Y, applyT(t, "leafshift", W, 2, [[0, 1, 0, 0]])[0])
    t = Tree((None, 0, 0, 0)); W = 0b1111; Y = 0b0111
    V["X10.dipole"] = vecs(t, Y, applyT(t, "dipole", W, 3, [[0, 0, 0, 1]])[0])
    V["X10.P1"] = vecs(t, Y, applyT(t, "P1", W, 3, [[0, 0, 0, 1]])[0])
    t = Tree((None, 0))
    for r in ("erase", "double", "fixed_e2"):
        V["X11." + r] = vecs(t, 0b1, applyT(t, r, 0b11, 1, [[0, 1]])[0])
    return V


# ---------- lattice DP over intermediate carriers ----------
def lattice(t, Y, rules, jvec=None, stats=None):
    """Returns composites (scaled S^m) at Y, number of single-pruning sequences, order-independence flags and the
    Lemma 16.0 path-weighted state count. Lemma 16.0 is checked at every lattice state."""
    X = t.full
    comp = {X: {r: np.eye(t.n, dtype=np.int64) for r in rules}}
    paths = {X: 1}
    agree = {r: True for r in rules}
    lemma = 0
    order = sorted(comp, key=lambda m: -bin(m).count("1"))
    frontier = [X]
    by_size = {}
    by_size.setdefault(bin(X).count("1"), set()).add(X)
    size = bin(X).count("1")
    ystates = bin(Y).count("1")
    while size > ystates:
        for W in sorted(by_size.get(size, ())):
            cand = bits(W & ~Y)
            lemma += paths[W] * len(cand)
            nxt = []
            for l in cand:
                pc = t.carrier(W & ~(1 << l))
                if pc != t.leaf(W, l) and stats is not None:
                    stats["viol"] += 1
                if pc:
                    nxt.append(l)
            if not nxt and stats is not None:
                stats["viol"] += 1
            for l in nxt:
                W2 = W & ~(1 << l)
                new = {r: mat(t, "jump" if r == "jump" else r, W, l, jvec) @ comp[W][r] for r in rules}
                if W2 in comp:
                    for r in rules:
                        if not np.array_equal(comp[W2][r], new[r]):
                            agree[r] = False
                    paths[W2] += paths[W]
                else:
                    comp[W2] = new
                    paths[W2] = paths[W]
                    by_size.setdefault(size - 1, set()).add(W2)
        size -= 1
    return comp[Y], paths[Y], agree, lemma


def u16(G):
    st = {"trees": 0, "pairs": 0, "sequences": 0, "nontrivial": 0, "multi_max": 0, "multi_fiber": 0, "multi_order": 0,
          "lemma_states": 0, "viol": 0}
    for r in LAT_RULES:
        st["oi_" + r] = 0; st["eq_" + r] = 0; st["neq_" + r] = 0
    lines = []
    for n in range(1, 8):
        for par in G[n]:
            t = Tree(par)
            st["trees"] += 1
            for Y in t.carriers():
                st["pairs"] += 1
                D = t.full & ~Y
                Dl = bits(D)
                maximal = [m for m in Dl if not any((t.pre[c] >> m) & 1 for c in Dl if c != m)]
                leavesD = [m for m in Dl if not t.kids[m]]
                remov = [m for m in Dl if t.carrier(t.full & ~(1 << m)) and (Y & ~(t.full & ~(1 << m))) == 0]
                if not (maximal == leavesD == remov):
                    st["viol"] += 1
                compY, npaths, agree, lemma = lattice(t, Y, LAT_RULES, stats=st)
                st["lemma_states"] += lemma
                st["sequences"] += npaths
                m = len(Dl)
                P = t.Pmat(Y)
                r = [t.lp(Y, v) for v in range(t.n)]
                oi, eq = [], []
                for ru in LAT_RULES:
                    e = agree[ru] and np.array_equal(compY[ru], (S ** m) * P)  # normalized comparison
                    oi.append(agree[ru]); eq.append(e)
                    st["oi_" + ru] += agree[ru]; st["eq_" + ru] += e; st["neq_" + ru] += (not e)
                st["nontrivial"] += (m > 0)
                st["multi_max"] += (len(maximal) >= 2)
                st["multi_fiber"] += any(r.count(y) >= 3 for y in bits(Y))
                st["multi_order"] += (npaths >= 2)
                lines.append("%s|%s|%d|%s|%s|%s|%s" % (t.key(), ",".join(map(str, bits(Y))), npaths,
                             ",".join(map(str, maximal)), ",".join(map(str, r)),
                             "".join("1" if b else "0" for b in oi), "".join("1" if b else "0" for b in eq)))
    return st, lines


def u16l(G):
    st = {"cases": 0, "pos": 0, "neg": 0, "viol": 0}
    lines = []
    for n in range(1, 8):
        for par in G[n]:
            t = Tree(par)
            for l in range(n):
                W2 = t.full & ~(1 << l)
                pc = W2 != 0 and t.carrier(W2)
                lf = t.leaf(t.full, l)
                st["cases"] += 1; st["pos" if pc else "neg"] += 1; st["viol"] += pc != lf
                lines.append("%s|%d|%d|%d" % (t.key(), l, pc, lf))
    return st, lines


def leaf_instances(G, nmax):
    out = []
    for n in range(1, nmax + 1):
        for par in G[n]:
            t = Tree(par)
            for l in range(1, n):
                if t.leaf(t.full, l):
                    out.append((t, l))
    return out


def u16r(G):
    inst = leaf_instances(G, 7)
    res, lines = {}, []
    AB = [(a, b) for a in (1, -1, 2) for b in (1, -1, 2)]
    for ru in PANEL:
        E = dict(E1=True, E2=True, E3=True, E4=True, E5=True, eqP1=True)
        wseq = {}
        for t, l in inst:
            W, n = t.full, t.n
            I = np.eye(n, dtype=np.int64)
            el = I[l]
            ts = np.concatenate([I, -I, 2 * I, el + I, el - I])  # rows grouped by type; order irrelevant
            ys = np.stack([el, -el])
            Tts, Tys = applyT(t, ru, W, l, ts), applyT(t, ru, W, l, ys)
            lhs_in = np.concatenate([a * ts + b * ys[j] for a, b in AB for j in range(2)])
            rhs = np.concatenate([a * Tts + b * Tys[j] for a, b in AB for j in range(2)])
            if not np.array_equal(applyT(t, ru, W, l, lhs_in), rhs):
                E["E1"] = False
            if not np.array_equal(Tts.sum(axis=1), S * ts.sum(axis=1)):
                E["E2"] = False
            Pm = t.Pmat(W & ~(1 << l))
            if not np.array_equal(Tts, S * (ts @ Pm.T)):
                E["eqP1"] = False
            TI = applyT(t, ru, W, l, I)
            for v in range(n):
                if v != l and not np.array_equal(TI[v], S * I[v]):
                    E["E3"] = False
            c = TI[l]
            supp = set(np.flatnonzero(c).tolist())
            anc = t.proper_anc(l)
            if not supp <= set(anc):
                E["E4"] = False
            for d, an in enumerate(anc, start=1):
                wv = F(int(c[an]), S)  # normalized weight
                if wseq.setdefault(d, wv) != wv:
                    E["E5"] = False
        res[ru] = E
        lines.append("%s|%s|%d" % (ru, "".join("1" if E[k] else "0" for k in ("E1", "E2", "E3", "E4", "E5")), E["eqP1"]))
    viol = sum(all(res[ru][k] for k in ("E1", "E2", "E3", "E4", "E5")) != res[ru]["eqP1"] for ru in PANEL)
    return res, lines, len(inst), viol


def u16p(G):
    st = {"cases": 0, "ycases": 0, "genesis_moved": 0, "viol": 0}
    lines = []
    for n in range(2, 8):
        for par in G[n]:
            t = Tree(par)
            Ys = t.carriers()
            x = np.array([(7 * v + 3) % 11 - 5 for v in range(n)], dtype=np.int64)
            for l in range(1, n):
                if not t.leaf(t.full, l):
                    continue
                p = t.proper_anc(l)[0]
                for w in (-2, 1, 3):
                    st["cases"] += 1
                    xq = x.copy(); xq[l] += w
                    if np.flatnonzero(x != xq).tolist() != [l]:
                        st["viol"] += 1
                    Tx, Tq = applyT(t, "P1", t.full, l, [x, xq])
                    d = Tq - Tx
                    if [v for v in range(n) if v != l and d[v] != 0] != [p] or d[p] != S * w or d[l] != 0:
                        st["viol"] += 1
                    if Tx[p] != S * (x[p] + x[l]) or Tq[p] != S * (xq[p] + xq[l]):
                        st["viol"] += 1
                    if Tx.sum() != S * x.sum() or Tq.sum() != S * xq.sum():
                        st["viol"] += 1
                    g = applyT(t, "genesis", t.full, l, [xq])[0] - applyT(t, "genesis", t.full, l, [x])[0]
                    if np.flatnonzero(g).tolist() != [p]:
                        st["genesis_moved"] += 1
                    for Y in Ys:
                        if (Y >> l) & 1:
                            continue
                        st["ycases"] += 1
                        P = t.Pmat(Y)
                        rl = t.lp(Y, l)
                        e = np.zeros(n, dtype=np.int64); e[rl] = w
                        ok = np.array_equal(P @ (xq - x), e) and np.array_equal(P @ (Tq - Tx), S * e) and t.lp(Y, p) == rl
                        st["viol"] += not ok
                        lines.append("%s|%d|%d|%s|%d" % (t.key(), l, w, ",".join(map(str, bits(Y))), rl))
    return st, lines


def u16j(G):
    st = {"rules": 0, "oi": 0, "e5": 0, "eqp": 0, "viol": 0}
    lines = []
    trees = [Tree(par) for n in range(1, 7) for par in G[n]]
    pairs = [(t, Y) for t in trees for Y in t.carriers()]
    inst = leaf_instances(G, 6)
    for j in itertools.product(*[range(1, k + 1) for k in range(1, 6)]):
        st["rules"] += 1
        oi, eq = True, True
        for t, Y in pairs:
            compY, _, agree, _ = lattice(t, Y, ["jump"], jvec=j)
            m = bin(t.full & ~Y).count("1")
            if not agree["jump"]:
                oi = False
            if not np.array_equal(compY["jump"], (S ** m) * t.Pmat(Y)):
                eq = False
        eq = eq and oi
        wseq, e5 = {}, True
        for t, l in inst:
            c = col(t, "jump", t.full, l, j)
            for d, an in enumerate(t.proper_anc(l), start=1):
                wv = F(int(c[an]), S)
                if wseq.setdefault(d, wv) != wv:
                    e5 = False
        st["oi"] += oi; st["e5"] += e5; st["eqp"] += eq
        st["viol"] += not (e5 == eq == (j == (1, 1, 1, 1, 1)))
        lines.append("%s|%d|%d|%d" % (",".join(map(str, j)), e5, oi, eq))
    return st, lines


_GRID = {}


def grid_bruteforce():
    """B16b: every w in {-1,-1/2,0,1/2,1}^6 (scaled by 2), E5-shaped rule, E2 on every single pruning of U16."""
    if "res" in _GRID:
        return _GRID["res"]
    G = grow(7)
    inst = leaf_instances(G, 7)
    A = np.array(list(itertools.product(range(-2, 3), repeat=6)), dtype=np.int64)  # scaled weights
    ok = np.ones(len(A), dtype=bool)
    depths = set()
    for t, l in inst:
        anc = t.proper_anc(l)
        depths.add(len(anc))
        img = np.zeros((len(A), t.n), dtype=np.int64)
        for d, an in enumerate(anc):
            img[:, an] += A[:, d]
        ok &= img.sum(axis=1) == S  # total of T(e_l) equals 1 after normalization
    sols = [tuple(int(v) for v in A[i]) for i in np.flatnonzero(ok)]
    _GRID["res"] = (sols, sorted(depths))
    _GRID["size"] = len(A)
    return _GRID["res"]


def bounded():
    rng = np.random.default_rng(20261018)
    st = {"cases": 0, "seqs": 0, "viol": 0}
    for _ in range(400):
        n = int(rng.choice([8, 9, 10]))
        par = (None,) + tuple(int(rng.integers(0, i)) for i in range(1, n))
        t = Tree(par)
        Cs = t.carriers()
        Y = Cs[int(rng.integers(0, len(Cs)))]
        st["cases"] += 1
        m = bin(t.full & ~Y).count("1")
        P = t.Pmat(Y)
        seen = {r: None for r in LAT_RULES}
        for _s in range(30):
            W = t.full
            C = {r: np.eye(n, dtype=np.int64) for r in LAT_RULES}
            while W != Y:
                cand = [l for l in bits(W & ~Y) if t.leaf(W, l)]
                l = cand[int(rng.integers(0, len(cand)))]
                for r in LAT_RULES:
                    C[r] = mat(t, r, W, l) @ C[r]
                W &= ~(1 << l)
            st["seqs"] += 1
            if not np.array_equal(C["P1"], (S ** m) * P):
                st["viol"] += 1
            for r in LAT_RULES:
                if seen[r] is None:
                    seen[r] = C[r]
                elif not np.array_equal(seen[r], C[r]):
                    st["viol"] += 1
    return st


def digest(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    G = grow(7)
    V = instances()
    s16, l16 = u16(G)
    sl, ll = u16l(G)
    rres, lr, ninst, rviol = u16r(G)
    sp, lpl = u16p(G)
    sj, lj = u16j(G)
    sols, _ = grid_bruteforce()
    bs = bounded()
    U = {"trees": s16["trees"], "pairs": s16["pairs"], "sequences": s16["sequences"], "nontrivial": s16["nontrivial"],
         "multi_max": s16["multi_max"], "multi_fiber": s16["multi_fiber"], "multi_order": s16["multi_order"],
         "lemma_states": s16["lemma_states"], "u16_lines": len(l16), "u16_digest": digest(l16), "u16_viol": s16["viol"],
         "u16l_cases": sl["cases"], "u16l_pos": sl["pos"], "u16l_neg": sl["neg"], "u16l_digest": digest(ll), "u16l_viol": sl["viol"],
         "u16r_instances": ninst, "u16r_digest": digest(lr), "u16r_viol": rviol,
         "u16p_cases": sp["cases"], "u16p_ycases": sp["ycases"], "u16p_genesis_moved": sp["genesis_moved"],
         "u16p_lines": len(lpl), "u16p_digest": digest(lpl), "u16p_viol": sp["viol"],
         "u16j_rules": sj["rules"], "u16j_oi": sj["oi"], "u16j_e5": sj["e5"], "u16j_eqp": sj["eqp"],
         "u16j_digest": digest(lj), "u16j_viol": sj["viol"]}
    for r in LAT_RULES:
        U["oi_" + r], U["eq_" + r], U["neq_" + r] = s16["oi_" + r], s16["eq_" + r], s16["neq_" + r]
    cls = {ru: "".join("1" if rres[ru][k] else "0" for k in ("E1", "E2", "E3", "E4", "E5", "eqP1")) for ru in PANEL}
    B = {"B16a_cases": bs["cases"], "B16a_seqs": bs["seqs"], "B16a_viol": bs["viol"],
         "B16b_grid": _GRID["size"], "B16b_solutions": [[q(a, S) for a in s] for s in sols]}
    # ---------- rejecting controls (claims that must be refuted) ----------
    P = U["pairs"]

    def rej(c):
        return "REJECTED" if c else "ACCEPTED"
    conf = all(U["oi_" + r] == P and U["neq_" + r] > 0 for r in ("genesis", "grandparent", "halfsplit"))
    E14 = lambda ru: cls[ru][:4] == "1111"
    C = {"R1_confluence_selects_P1": rej(conf and all(E14(r) for r in ("genesis", "grandparent", "halfsplit"))),
         "R2_genesis_satisfies_E5": rej(cls["genesis"][4] == "0"),
         "R3_grandparent_satisfies_E5": rej(cls["grandparent"][4] == "0"),
         "R4_halfsplit_satisfies_E5": rej(cls["halfsplit"][4] == "0"),
         "R5_E1_to_E4_force_P1": rej(E14("genesis") and cls["genesis"][5] == "0"),
         "R6_without_E2_forces_P1": rej(all(cls[r][0] + cls[r][2:5] == "1111" and cls[r][1] == "0" and cls[r][5] == "0" for r in ("erase", "double"))),
         "R7_absolute_e2_conserves": rej(cls["fixed_e2"][1] == "0" and V["X11.fixed_e2"] == ["0"]),
         "R8_without_E3_forces_P1": rej(cls["leafshift"] == "110110"),
         "R9_without_E4_forces_P1": rej(cls["dipole"] == "111010"),
         "R10_without_E1_forces_P1": rej(cls["sign"] == "011110" and V["X8.T_minus"] != [("-" + s if s != "0" else "0") for s in V["X8.T_plus"]]),
         "R11_jump_confluence_selects_P1": rej(sj["oi"] > 1 and sj["eqp"] == 1),
         "R12_other_grid_vector_satisfies_E1_E5": rej(B["B16b_solutions"] == [["1", "0", "0", "0", "0", "0"]])}
    cert = {"meta": {"role": "checker", "result_sha256": rsha}, "values": V, "universe": U, "panel": cls,
            "bounded": B, "controls": C}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"universe": U, "panel": cls, "bounded": B, "controls": C}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
