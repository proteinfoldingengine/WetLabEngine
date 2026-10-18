"""receiver_identification d14 freeze: independent CHECKER. Does not import the producer. Floating-point numpy
(complex128, tolerance 1e-9) with Stinespring isometries from QR of complex Gaussian matrices (seed 1018),
Schroedinger-side Gram read-off, explicit chain cone totals, restricted-growth-string partitions, orbit-based unit
invariance, integer-weight laws. Exact rational values only where a value string is certified."""
import hashlib, itertools, json, math, sys
from fractions import Fraction as Fr
import numpy as np

RESULT_SHA = "f6cc849663224a5a2c877cd32a6700ecad9df1ea2d4f723a040c66e55dbc38f9"
TOL = 1e-9
rng = np.random.default_rng(1018)
BAD = []


def need(c, m):
    if not c:
        BAD.append(m)


def s(x):
    x = Fr(x); return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def dg(o): return hashlib.sha256(json.dumps(o, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def close(A, B): return np.max(np.abs(np.asarray(A) - np.asarray(B))) < TOL if np.size(A) else True


SPEC = [((0, 1), (0, 1), (0,), (0, 1, 2)), ((0, 1, 2), (0, 1), (0,), (0, 1, 2, 3)), ((0, 1), (0, 1, 2), (0,), (0, 1, 2, 3)),
        ((0, 1, 2), (0, 1, 2), (0,), (0, 1, 2, 3, 4)), ((0, 2), (0,), (0,), (0, 1, 2)), ((0, 2), (0, 1), (0,), (0, 1, 2, 3)),
        ((0, 1), (0, 1), (0, 1), (0, 1, 2)), ((0, 1), (0,), (0, 1), (0, 1)), ((0, 1), (0, 1), (0,), (0, 1, 2, 3))]


class Region:
    def __init__(self, Ol, Op, Oz, reg, mapf=None):
        self.inp = list(itertools.product(Ol, Op, Oz))
        self.out = list(itertools.product(reg, Oz))
        mp = mapf or (lambda b: (b[0] + b[1], b[2]))
        self.f = [self.out.index(mp(b)) for b in self.inp]
        self.n, self.d = len(self.inp), len(self.out)
        self.R = sorted(set(self.f))
        self.fib = {y: [i for i in range(self.n) if self.f[i] == y] for y in self.R}

    def iso_from_coeff(self, C):
        # C[b] : coefficient vector over environment index; V|b> = sum_i C[b,i] |f(b)>|i>
        m = C.shape[1]; V = np.zeros((self.d * m, self.n), complex)
        for b in range(self.n):
            for i in range(m): V[self.f[b] * m + i, b] = C[b, i]
        return V, m

    def dephase(self): return self.iso_from_coeff(np.eye(self.n, dtype=complex))

    def pair(self, a, b):
        # Kraus K0 = |f(a)><a| + |f(b)><b|, others |f(c)><c|: environment index = (a merged with b)
        idx = {}; C = np.zeros((self.n, self.n - 1), complex); k = 0
        for c in range(self.n):
            if c == b: continue
            idx[c] = k; k += 1
        idx[b] = idx[a]
        for c in range(self.n): C[c, idx[c]] = 1
        return self.iso_from_coeff(C)

    def random(self, extra):
        m = max(len(v) for v in self.fib.values()) + extra; C = np.zeros((self.n, m), complex)
        for y in self.R:
            Z = rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m)); Qm, _ = np.linalg.qr(Z)
            for t, b in enumerate(self.fib[y]): C[b] = Qm[:, t]
        return self.iso_from_coeff(C)

    def family(self):
        prs = [(a, b) for a in range(self.n) for b in range(a + 1, self.n) if self.f[a] != self.f[b]]
        fam = [("dep",) + self.dephase()] + [("pair",) + self.pair(a, b) for a, b in prs]
        fam += [("rand",) + self.random(0 if k < 3 else 1) for k in range(6)]
        return fam, len(prs)


def heis(V, m, E): return V.conj().T @ np.kron(E, np.eye(m)) @ V


def schr(V, m, rho, d):
    W = V @ rho @ V.conj().T
    return np.einsum("aibi->ab", W.reshape(d, m, d, m))


def unit(d, u, v): E = np.zeros((d, d), complex); E[u, v] = 1; return E


def c19a():
    rec = []; cnt = {"extensions": 0, "pair": 0, "rand": 0, "dep": 0, "units": 0, "inv": 0, "noninv": 0, "kraus_ops": 0,
                     "coherent_inputs": 0}
    dims, units, prs_l, plocal = [], [], [], []
    for ri, sp in enumerate(SPEC):
        rg = Region(*sp); d, n = rg.d, rg.n; fam, npr = rg.family()
        Qo = np.diag([1.0 if rg.out[k][0] > 0 else 0.0 for k in range(d)])
        Pi = np.diag([1.0 if b[0] + b[1] > 0 else 0.0 for b in rg.inp])
        for kind, V, m in fam:
            cnt[kind] += 1; cnt["extensions"] += 1; cnt["kraus_ops"] += m
            need(close(V.conj().T @ V, np.eye(n)), "isometry r%d" % ri)
            for b in range(n):
                r = np.zeros((n, n)); r[b, b] = 1; need(close(schr(V, m, r, d), unit(d, rg.f[b], rg.f[b])), "classical r%d" % ri)
            for i in range(m):
                K = V.reshape(d, m, n)[:, i, :]; need(close(Qo @ K, K @ Pi), "QK r%d" % ri)
            need(close(heis(V, m, Qo), Pi), "Q pull r%d" % ri)
            need(close(heis(V, m, 0.25 * (np.eye(d) - Qo) + 0.75 * Qo), 0.25 * (np.eye(n) - Pi) + 0.75 * Pi), "Eab r%d" % ri)
            for y in range(d):
                need(close(heis(V, m, unit(d, y, y)), np.diag([1.0 if rg.f[b] == y else 0.0 for b in range(n)])), "19.4b")
            for t in range(3):
                v = rng.normal(size=n) + 1j * rng.normal(size=n); v /= np.linalg.norm(v); rho = np.outer(v, v.conj())
                o = schr(V, m, rho, d); cnt["coherent_inputs"] += 1
                law = np.array([sum(rho[b, b].real for b in range(n) if rg.f[b] == y) for y in range(d)])
                need(close(np.diag(o).real, law), "19.4c r%d" % ri)
        inv_list = []
        for u in range(d):
            for v in range(d):
                ims = [heis(V, m, unit(d, u, v)) for _, V, m in fam]
                inv = all(close(x, ims[0]) for x in ims[1:]); pred = (u == v) or (u not in rg.R) or (v not in rg.R)
                need(inv == pred, "19.4a r%d" % ri); cnt["units"] += 1; cnt["inv" if inv else "noninv"] += 1
                if inv: inv_list.append([u, v])
        dep = fam[0]; rows = []
        for kind, V, m in fam:
            if kind != "rand": continue
            rows.append(np.array([(heis(V, m, unit(d, u, v)) - heis(dep[1], dep[2], unit(d, u, v))).ravel()
                                  for u in range(d) for v in range(d)]).T)
        M = np.vstack(rows); kd = d * d - np.linalg.matrix_rank(M, tol=1e-8)
        pl = []
        if len(sp[2]) > 1:
            reg = sp[3]; nz = len(sp[2])
            for a in range(len(reg)):
                for c in range(len(reg)):
                    E = np.kron(unit(len(reg), a, c), np.eye(nz))  # output order is (y, z) lexicographic
                    ims = [heis(V, m, E) for _, V, m in fam]; inv = all(close(x, ims[0]) for x in ims[1:])
                    need(inv == (a == c), "19.4d r%d" % ri)
                    if inv: pl.append([a, c])
            plocal.append([len(reg) ** 2, len(pl)])
        dims.append(int(kd)); units.append(d * d); prs_l.append(npr); rec.append([inv_list, pl, npr, int(kd)])
    return {"digest": dg(rec), "det_dim": dims, "units": units, "pair_ext": prs_l, "plocal": plocal, "counts": cnt}


def w196():
    rg = Region((0, 1), (0, 1), (0,), (0, 1, 2)); d, n = 3, 4
    dep = rg.dephase()
    can = rg.iso_from_coeff(np.array([[1 if rg.inp[b][0] == i else 0 for i in range(2)] for b in range(n)], complex))
    alt = rg.iso_from_coeff(np.array([[1 if rg.inp[b][1] == i else 0 for i in range(2)] for b in range(n)], complex))

    def gram(V, m):
        Gm = np.zeros((n, n), complex)
        for a in range(n):
            for b in range(n):
                r = np.zeros((n, n)); r[a, b] = 1; Gm[a, b] = schr(V, m, r, d)[rg.f[a], rg.f[b]]
        return [[int(round(x.real)) for x in row] for row in Gm]
    sig, Nv, Qv = [], [], []
    for vec in ([1, 0, 1, 0], [1, 1, 0, 0]):
        v = np.array(vec, complex) / math.sqrt(2); rho = np.outer(v, v.conj()); row = []
        for V, m in (dep, can, alt):
            o = schr(V, m, rho, d)
            row.append(s(Fr(round(2 * (o[0, 1] + o[1, 0]).real), 2)))
            Nv.append(s(Fr(round(2 * sum(k * o[k, k].real for k in range(3))), 2)))
            Qv.append(s(Fr(round(2 * (o[1, 1] + o[2, 2]).real), 2)))
        sig.append(row)
    return {"X2.sigma": sig, "X2.N": Nv, "X2.Q": Qv, "X2.G_can": gram(*can), "X2.G_alt": gram(*alt)}


def sets(base): return [c for r in range(1, len(base) + 1) for c in itertools.combinations(base, r)]


def c19b():
    rec = []; k = 0
    for A in sets(range(4)):
        for B in sets(range(4)):
            dA = {a - b for a in A for b in A if a != b}; dB = {a - b for a in B for b in B if a != b}
            crit = not (dA & dB)
            coll = any(a + b == a2 + b2 for (a, b), (a2, b2) in itertools.combinations(itertools.product(A, B), 2))
            need(crit == (not coll), "19.1b"); rec.append([list(A), list(B), crit]); k += crit
    return {"digest": dg(rec), "pairs": len(rec), "injective": k, "noninjective": len(rec) - k}


SW = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1), Fr(3, 2)]


def cone_R(w):
    k = len(w); par = [None] + list(range(k))  # chain 0 - 1 - ... - k; leaf l = k, anc_d = k - d
    X = list(range(k + 1)); Y = X[:-1]
    Te = {v: Fr(0) for v in Y}
    for d_, wd in enumerate(w, 1): Te[k - d_] += wd

    def desc(a, S): return [v for v in S if v >= a]  # in a chain the cone of a is {a, a+1, ...}
    fails = [a for a in Y if sum(Te[v] for v in desc(a, Y)) != 1]  # C_a^X(e_l) = 1 for every a in Y
    return fails


def c19c():
    rec = []; rt, er, sg, nn, cntv = [], [], [], [], 0
    for k in range(1, 5):
        a = b = c = e = 0
        for w in itertools.product(SW, repeat=k):
            cntv += 1; fails = cone_R(w); R = not fails
            e1 = w[0] == 1 and all(x == 0 for x in w[1:]); need(R == e1, "19.8a")
            Rp = (k - 1) not in fails; E2 = 0 not in fails  # receiver p = k-1; Genesis = 0
            E2Rp = Rp and E2; nonneg = E2Rp and min(w) >= 0; need(nonneg == e1, "19.8c")
            a += R; b += E2Rp; c += E2Rp and not R; e += nonneg; rec.append([R, E2Rp])
        rt.append(a); er.append(b); sg.append(c); nn.append(e)
    return {"digest": dg(rec), "vectors": cntv, "R_true": rt, "E2Rp": er, "E2Rp_notR": sg, "E2Rp_nonneg": nn}


def rgs_partitions(S):
    S = list(S); n = len(S)

    def rec(i, a, mx):
        if i == n:
            blocks = [[] for _ in range(mx + 1)]
            for j, t in enumerate(a): blocks[t].append(S[j])
            yield blocks
            return
        for t in range(mx + 2):
            yield from rec(i + 1, a + [t], max(mx, t))
    if n == 0:
        yield []
        return
    yield from rec(1, [0], 0)


def c20a():
    rec = []; np_ = nf = 0
    for S in sets(range(5)):
        dims = []
        for pt in rgs_partitions(S):
            M = np.array([[1.0 if y in b else 0.0 for y in S] for b in pt]); r = np.linalg.matrix_rank(M)
            for a in M:
                for b in M:
                    x, res, *_ = np.linalg.lstsq(M.T, a * b, rcond=None); need(close(M.T @ x, a * b), "20.1 closure")
            need(r == len(pt), "20.1 dim"); dims.append(int(r)); np_ += 1
        gd = []
        for fv in itertools.product(range(3), repeat=len(S)):
            vals = sorted(set(fv)); Vd = np.array([[float(x) ** e for x in fv] for e in range(len(S))])
            r = np.linalg.matrix_rank(Vd); need(r == len(vals), "20.1 gen")
            for t in vals:  # Lagrange interpolation polynomial of the level set, evaluated on S
                L = [math.prod((x - u) / (t - u) for u in vals if u != t) for x in fv]
                need(close(L, [1.0 if x == t else 0.0 for x in fv]), "20.1 Lagrange")
            gd.append(int(r)); nf += 1
        rec.append([len(dims), sorted(dims), gd])
    return {"digest": dg(rec), "subsets": len(rec), "partitions": np_, "functions": nf}


def int_laws(n):
    seen = {}
    for w in itertools.product(range(3), repeat=n):
        if not any(w): continue
        gc = math.gcd(*w); red = tuple(x // gc for x in w); seen[red] = None
    out = []
    for red in seen:
        tot = sum(red); out.append((tuple(Fr(x, tot) for x in red), red))
    out.sort(key=lambda t: t[0])
    return [{i: p for i, p in enumerate(t[0]) if p} for t in out]


def tvd(a, b): return sum(abs(a.get(y, 0) - b.get(y, 0)) for y in set(a) | set(b)) / 2


def blk_tv(a, b, pt):
    return sum(abs(sum(a.get(y, 0) for y in bl) - sum(b.get(y, 0) for y in bl)) for bl in pt) / 2


def c20b():
    rec = []; tot = cv = st = ps_ = 0
    for nu in int_laws(3):
        for g in (1, 2):
            pl = {y + g: p for y, p in nu.items()}; reach = sorted(set(pl) | set(nu)); full = tvd(pl, nu)
            parts = list(rgs_partitions(reach)); npos = nst = ncv = 0
            for pt in parts:
                c = blk_tv(pl, nu, pt); need(c <= full, "20.2b"); npos += c > 0
                need((c > 0) == any(sum(nu.get(y - g, 0) for y in bl) != sum(nu.get(y, 0) for y in bl) for bl in pt), "20.2c")
                for i in range(len(pt)):
                    for j in range(i + 1, len(pt)):
                        mg = [pt[k] for k in range(len(pt)) if k not in (i, j)] + [pt[i] + pt[j]]
                        cm = blk_tv(pl, nu, mg); need(cm <= c, "20.2 mono"); ncv += 1; nst += cm < c
            need(blk_tv(pl, nu, [[y] for y in reach]) == full and blk_tv(pl, nu, [reach]) == 0, "20.2 ends")
            tot += len(parts); cv += ncv; st += nst; ps_ += npos; rec.append([len(parts), npos, ncv, nst, s(full)])
    return {"digest": dg(rec), "cases": len(rec), "partitions": tot, "covering": cv, "strict_decrease": st, "positive": ps_}


T = [Fr(0), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(3)]


def invariant_orbit(S, pt):
    orbits = [o for o in ([y for y in S if y == 0], [y for y in S if y > 0]) if o]
    blk = {y: k for k, b in enumerate(pt) for y in b}
    return all(len({blk[y] for y in o}) == 1 for o in orbits)


def c20c():
    rec = []; npt = ninv = adm = 0
    for S in sets(T):
        parts = list(rgs_partitions(S)); inv = [p for p in parts if invariant_orbit(S, p)]
        nt = [p for p in inv if len(p) == 2]
        need(all(len(p) <= 2 for p in inv), "20.3 at most two"); need(len(nt) == (1 if (0 in S and max(S) > 0) else 0), "20.3a")
        npt += len(parts); ninv += len(inv); adm += bool(nt); rec.append([len(parts), len(inv), bool(nt)])
    return {"digest": dg(rec), "subsets": len(rec), "partitions": npt, "invariant": ninv, "admit_nontrivial": adm}


GS = [Fr(1, 2), Fr(1), Fr(2), Fr(3)]
AB = [Fr(k, 4) for k in range(5)]


def C_nu(nu, g):
    ts = sorted(set(nu) | {y + g for y in nu})
    best = Fr(0)
    for t in ts + [(a + b) / 2 for a, b in zip(ts, ts[1:])]:
        best = max(best, sum(p for y, p in nu.items() if y <= t < y + g))
    return best


def c20d():
    rec = []; tr = 0
    for nu in int_laws(4):
        for g in GS:
            pl = {y + g: p for y, p in nu.items()}
            q = abs(nu.get(0, Fr(0)) - pl.get(0, Fr(0))); full = tvd(pl, nu); c = C_nu(nu, g)
            need(q == nu.get(0, 0), "20.4b"); need(q <= full and full >= c and c > 0, "20.4d/18.2c")
            reach = sorted(set(pl) | set(nu))
            uf = max(blk_tv(pl, nu, p) for p in rgs_partitions(reach) if invariant_orbit(reach, p)); need(uf == q, "uf")
            tr += q > 0; rec.append([s(q), s(full), s(c), q > 0])
    return {"digest": dg(rec), "cases": len(rec), "transfers": tr, "nontransfers": len(rec) - tr}


def c20e():
    rec = []; tr = 0
    for a in AB:
        for b in AB:
            for nu in int_laws(4):
                for g in GS:
                    pl = {y + g: p for y, p in nu.items()}
                    bern = lambda law: {1: sum(p for y, p in law.items() if y > 0) * b + law.get(0, 0) * a}
                    pp, pm = bern(pl)[1], bern(nu)[1]
                    t = tvd({1: pp, 0: 1 - pp}, {1: pm, 0: 1 - pm})
                    need(t == abs(b - a) * nu.get(0, 0), "FU3"); need((t > 0) == (a != b and 0 in nu), "FU4")
                    tr += t > 0; rec.append(t > 0)
    return {"digest": dg(rec), "cases": len(rec), "transfers": tr, "nontransfers": len(rec) - tr}


def dump_region():
    return Region((0,), (0, 1), (0, 1), None, mapf=None)


def inst_and_controls(wit):
    I = {}
    coll = [[list(a), list(b)] for a, b in itertools.combinations(itertools.product((0, 1), (0, 1)), 2) if sum(a) == sum(b)]
    I["X1.inj_01_01"] = not coll; I["X1.collision"] = coll[0]
    I.update(wit)
    d1 = {1: Fr(1)}; p1 = {2: Fr(1)}
    I["X4.a"] = [s(tvd(p1, d1)), s(max(blk_tv(p1, d1, p) for p in rgs_partitions([1, 2]) if invariant_orbit([1, 2], p)))]
    nu = {0: Fr(1, 2), 2: Fr(1, 2)}; pl = {1: Fr(1, 2), 3: Fr(1, 2)}
    I["X4.b"] = [s(tvd(pl, nu))] + [s(blk_tv(pl, nu, p)) for p in ([[0], [1, 2, 3]], [[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 1, 2, 3]])]
    un = {0: Fr(1, 3), 1: Fr(1, 3), 2: Fr(1, 3)}; up = {1: Fr(1, 3), 2: Fr(1, 3), 3: Fr(1, 3)}
    I["X4.c"] = [s(tvd(up, un)), s(blk_tv(up, un, [[0], [1, 2, 3]]))]
    a, b = Fr(1, 4), Fr(3, 4)
    pm = nu[0] * a + (1 - nu[0]) * b; pp = b
    I["X5.illus"] = [s(pm), s(pp), s(abs(pp - pm))]
    I["X5.controls"] = [s(abs(Fr(1, 2) - Fr(1, 2))), s(abs(b - b))]  # a = b; z = 0 gives both responses b
    # u + (v-u)a = 0, u + (v-u)b = 1  =>  (v-u)(b-a) = 1
    I["X5.vminusu"] = s(Fr(1) / (b - a))
    vs = [(1, 1, -1), (0, 0, 1), (0, 1, 0), (Fr(1, 2), Fr(1, 2), 0)]
    I["X6.prefix"] = [[s(sum(Fr(x) for x in w[:j])) for j in range(1, 4)] for w in vs]
    I["X6.rfail"] = [sorted(3 - a_ for a_ in cone_R([Fr(x) for x in w]) if a_ != 3) for w in vs]
    # Genesis dump (o, l, p): (x_o, j, x_p) -> (x_o + j, x_p); input order (x_o, j, x_p), output (o', p')
    rg = Region.__new__(Region)
    rg.inp = [(0, j, x) for j in (0, 1) for x in (0, 1)]; rg.out = [(o, p) for o in (0, 1) for p in (0, 1)]
    rg.f = [rg.out.index((b[0] + b[1], b[2])) for b in rg.inp]; rg.n, rg.d = 4, 4; rg.R = sorted(set(rg.f))
    rg.fib = {y: [i for i in range(4) if rg.f[i] == y] for y in rg.R}
    fam, _ = rg.family(); pinv = 0
    for y in (0, 1):
        for y2 in (0, 1):
            E = np.kron(np.eye(2), unit(2, y, y2)); ims = [heis(V, m, E) for _, V, m in fam]
            inv = all(close(x, ims[0]) for x in ims[1:]); pinv += inv
    worst = Fr(0)
    for nul in int_laws(4):  # one-location pair at l (grade 1 vs absent); receiver p's background law nul
        lawp = {}
        for prep in (1, 0):
            out = {}
            for y, p in nul.items():
                xo, j, xp = 0, prep, y; o2, p2 = xo + j, xp  # dump sends l's grade to Genesis, p unchanged
                out[p2] = out.get(p2, 0) + p
            lawp[prep] = out
        worst = max(worst, abs(lawp[1].get(0, 0) - lawp[0].get(0, 0)))
    I["X7.dump"] = [4, pinv, s(worst)]
    C = {}
    C["R1_trivial_availability_transfers"] = any(blk_tv({y + g: p for y, p in n.items()}, n, [sorted(set(n) | {y + g for y in n})]) != 0
                                                for n in int_laws(4) for g in GS)
    C["R2_genesis_dump_receiver_gains"] = worst != 0
    g1 = Region(*SPEC[0]); fam1, _ = g1.family(); sg = unit(3, 0, 1) + unit(3, 1, 0)
    ims = [heis(V, m, sg) for _, V, m in fam1]; C["R3_sigma_event_determined"] = all(close(x, ims[0]) for x in ims[1:])
    C["R4_canonical_extension_unique"] = wit["X2.sigma"][0][1] == wit["X2.sigma"][0][2] and wit["X2.sigma"][1][1] == wit["X2.sigma"][1][2]
    C["R5_addition_injective_01"] = I["X1.inj_01_01"]
    C["R6_threshold_unit_invariant"] = invariant_orbit([0, 1, 2, 3], [[0, 1], [2, 3]])
    C["R7_E2_Rp_imply_R_signed"] = not cone_R([Fr(1), Fr(1), Fr(-1)])
    C["R8_relabel_sharpens_E"] = any(abs(u + (v - u) / 4) < TOL and abs(u + 3 * (v - u) / 4 - 1) < TOL
                                     for u in np.linspace(0, 1, 9) for v in np.linspace(0, 1, 9))
    C["R9_unit_free_transfers_without_empty"] = I["X4.a"][1] != "0"
    ims = [heis(V, m, np.eye(3)) for _, V, m in fam1]; idinv = all(close(x, ims[0]) for x in ims[1:])
    C["R10_A1_A2_force_full_access"] = not (idinv and 1 != 3)  # C.1 is local and determined; dim 1 vs dim D_p = 3 in G1
    return I, {k: ("ACCEPTED_WRONGLY" if v else "REJECTED") for k, v in C.items()}


def main():
    wit = w196(); I, C = inst_and_controls(wit)
    U = {"U19A": c19a(), "U19B": c19b(), "U19C": c19c(), "U20A": c20a(), "U20B": c20b(), "U20C": c20c(),
         "U20D": c20d(), "U20E": c20e()}
    I["X3.units"] = U["U19A"]["units"]; I["X3.det_dim"] = U["U19A"]["det_dim"]
    I["X3.pair_ext"] = U["U19A"]["pair_ext"]; I["X3.plocal"] = U["U19A"]["plocal"]
    cert = {"role": "checker", "result_sha256": RESULT_SHA, "instances": I, "universes": U, "controls": C, "violations": BAD}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print("checker violations", len(BAD))


if __name__ == "__main__":
    main()
