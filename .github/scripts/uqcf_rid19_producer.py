"""receiver_identification d19 freeze (section 25, the Genesis datum is forced): PRODUCER.
Pure-Python exact Fractions. Parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the grounded
weighted Laplacian (no cone-total formula); reads as vertex-coordinate matrices on N[v]; cones re-rooted by relabelling;
eliminations as exact sparse Gauss-Jordan over Q with an augmented constant column."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d19_review")
TABLES = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k),
          "alt": lambda k: Fr(1) if k % 2 == 1 else Fr(-2)}
MT = {"one": lambda k: Fr(1), "inv": lambda k: Fr(1, k), "invalt": lambda k: Fr(1) if k % 2 == 1 else Fr(-1, 2)}
FAM = {"G1": ("unit", "one"), "G2": ("three", "one"), "G3": ("depth", "inv"), "G4": ("alt", "invalt"),
       "G5": ("depth", "one"), "G6": ("alt", "one")}
CONST = {"G1": Fr(1), "G2": Fr(3), "G3": Fr(1), "G4": Fr(1)}
THETAS = [Fr(-1), Fr(-3), Fr(0), Fr(2)]
GS = [Fr(1), Fr(-2), Fr(5, 3)]
VIOL = []


def canon_of(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n):
        ch[par[v]].append(v)
    memo = {}
    def s(v):
        if v not in memo:
            memo[v] = "(" + "".join(sorted(s(u) for u in ch[v])) + ")"
        return memo[v]
    return s, ch


def trees(nmax):
    out = {}; level = [[None]]
    out[canon_of([None])[0](0)] = [None]
    for _ in range(2, nmax + 1):
        new = []
        for par in level:
            for a in range(len(par)):
                q = par + [a]; c = canon_of(q)[0](0)
                if c not in out:
                    out[c] = q; new.append(q)
        level = new
    return out


def depth(par, v):
    d = 0
    while par[v] is not None:
        v = par[v]; d += 1
    return d


def solve(A, b):
    n = len(A); M = [row[:] + [bb] for row, bb in zip(A, b)]
    for i in range(n):
        piv = next(r for r in range(i, n) if M[r][i] != 0); M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]; M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


class Echelon:
    """incremental exact row echelon over Q."""
    def __init__(self, m):
        self.m = m; self.rows = {}
    def add(self, r):
        r = list(r)
        for c in range(self.m):
            if r[c] != 0 and c in self.rows:
                f = r[c]; r = [x - f * y for x, y in zip(r, self.rows[c])]
        c = next((c for c in range(self.m) if r[c] != 0), None)
        if c is None:
            return
        inv = 1 / r[c]; r = [x * inv for x in r]
        for c2, row in self.rows.items():
            if row[c] != 0:
                f = row[c]; self.rows[c2] = [x - f * y for x, y in zip(row, r)]
        self.rows[c] = r
    def nullity(self):
        return self.m - len(self.rows)
    def basis(self):
        piv = sorted(self.rows); out = []
        for fc in [c for c in range(self.m) if c not in self.rows]:
            v = [Fr(0)] * self.m; v[fc] = Fr(1)
            for pc in piv:
                v[pc] = -self.rows[pc][fc]
            out.append(v)
        return out


def field(par, x, a):
    n = len(par)
    if n == 1:
        return [Fr(0)]
    w = {v: 1 / a(depth(par, v)) for v in range(1, n)}
    L = [[Fr(0)] * n for _ in range(n)]
    for v in range(1, n):
        p = par[v]; L[v][v] += w[v]; L[p][p] += w[v]; L[v][p] -= w[v]; L[p][v] -= w[v]
    idx = list(range(1, n))
    return [Fr(0)] + solve([[L[i][j] for j in idx] for i in idx], [x[i] for i in idx])


def children(par):
    ch = [[] for _ in par]
    for v in range(1, len(par)):
        ch[par[v]].append(v)
    return ch


def rule_matrix(par, beta, gamma, gamma0):
    """vertex-coordinate read matrix: f = R phi."""
    n = len(par); ch = children(par); R = [[Fr(0)] * n for _ in range(n)]
    if ch[0]:
        g0 = gamma0(len(ch[0]))
        for u in ch[0]:
            R[0][u] += g0; R[0][0] -= g0
    for v in range(1, n):
        k = depth(par, v); b = beta(k, len(ch[v]))
        R[v][par[v]] += b; R[v][v] -= b
        if ch[v]:
            g = gamma(k, len(ch[v]))
            for u in ch[v]:
                R[v][u] += g; R[v][v] -= g
    return R


def depth_rule(par, m):
    return rule_matrix(par, lambda k, n: m(k), lambda k, n: m(k + 1), lambda n: m(1))


def apply(R, phi):
    return [sum((r * p for r, p in zip(row, phi)), Fr(0)) for row in R]


def unit(n, z):
    x = [Fr(0)] * n; x[z] = Fr(1); return x


def prune(par, l):
    mp = {}; j = 0
    for v in range(len(par)):
        if v != l:
            mp[v] = j; j += 1
    q = [None] * (len(par) - 1)
    for v in range(len(par)):
        if v != l and par[v] is not None:
            q[mp[v]] = mp[par[v]]
    return q, mp


def P(x, par, l, mp):
    y = [Fr(0)] * (len(x) - 1)
    for v in range(len(x)):
        if v != l:
            y[mp[v]] = x[v]
    y[mp[par[l]]] += x[l]
    return y


def balanced(x):
    return [x[0] - sum(x)] + list(x[1:])


def cone(par, z):
    ch = children(par); s = [z]; out = []
    while s:
        v = s.pop(); out.append(v); s.extend(ch[v])
    return out




class Affine:
    """exact sparse row echelon over Q for rows sum_c r[c] u_c = const."""
    def __init__(self):
        self.piv = {}; self.inconsistent = False
    def add(self, r, const=Fr(0)):
        r = {c: Fr(v) for c, v in r.items() if v != 0}; const = Fr(const)
        while r:
            c = min(r)
            if c not in self.piv:
                inv = 1 / r[c]; self.piv[c] = ({k: v * inv for k, v in r.items()}, const * inv)
                return
            f = r[c]; pr, pc = self.piv[c]
            for k, v in pr.items():
                nv = r.get(k, Fr(0)) - f * v
                if nv == 0:
                    r.pop(k, None)
                else:
                    r[k] = nv
            const -= f * pc
        if const != 0:
            self.inconsistent = True
    def rref(self):
        for c in sorted(self.piv, reverse=True):
            pr, pc = self.piv[c]
            for c2 in list(self.piv):
                r2, k2 = self.piv[c2]
                if c2 != c and c in r2:
                    f = r2[c]
                    for k, v in pr.items():
                        nv = r2.get(k, Fr(0)) - f * v
                        if nv == 0:
                            r2.pop(k, None)
                        else:
                            r2[k] = nv
                    self.piv[c2] = (r2, k2 - f * pc)
        return self.piv


def label_map(par):
    """canonical string of every vertex."""
    ch = children(par); memo = {}
    def s(v):
        if v not in memo:
            memo[v] = "(" + "".join(sorted(s(u) for u in ch[v])) + ")"
        return memo[v]
    for v in range(len(par)):
        s(v)
    return memo, ch


def iso(par, rep):
    """a rooted isomorphism from par onto rep (vertex map), matching children by canonical strings."""
    sa, cha = label_map(par); sb, chb = label_map(rep); mp = {0: 0}; stack = [(0, 0)]
    assert sa[0] == sb[0]
    while stack:
        u, w = stack.pop()
        A = sorted(cha[u], key=lambda v: sa[v]); B = sorted(chb[w], key=lambda v: sb[v])
        for x, y in zip(A, B):
            assert sa[x] == sb[y]; mp[x] = y; stack.append((x, y))
    return mp


def fhat(par, x, a, m, lam):
    f = apply(depth_rule(par, m), field(par, balanced(x), a))
    f[0] += lam(x)
    return f


def rerooted(par, aa):
    X = cone(par, aa); X.remove(aa); X = [aa] + sorted(X); loc = {v: i for i, v in enumerate(X)}
    return [None] + [loc[par[v]] for v in X[1:]], X, loc


def total(th):
    return lambda x: th * sum(x)


ZERO = lambda x: Fr(0)


def cnf_case(par, aa, q, a, m, lam):
    qpar, X, loc = rerooted(par, aa); n = len(par)
    lhs = fhat(par, unit(n, q), a, m, lam)
    fx = fhat(qpar, unit(len(X), loc[q]), a, m, lam)
    rhs = [fx[loc[v]] if v in loc else Fr(0) for v in range(n)]
    return lhs, rhs


def universe(nmax):
    T = trees(nmax); reps = T; D = nmax - 1
    cols = {}
    for cs, par in reps.items():
        for v in range(len(par)):
            cols[(cs, v)] = len(cols)
    top = [cs for cs, par in reps.items() if len(par) == nmax]
    U = {"carriers": len(reps), "positions": 0, "leaves": 0, "genesis_leaves": 0, "cases": 0, "unknowns": len(cols),
         "top_carriers": len(top), "max_depth": D, "sum_sq": 0}
    truth = {f: {str(th): 0 for th in THETAS} for f in FAM}; zero_fail = {f: 0 for f in CONST}
    arb = {f: Affine() for f in ("G1", "G3", "G5")}; rows_arb = {f: [] for f in arb}
    comp = Affine(); comp_rows = []; ncomp = D + 1  # columns 0..D-1 = mu_1..mu_D, column D = theta
    inv = Affine(); inv_rows = []
    lines = []
    one = TABLES["unit"]
    for cs, par in reps.items():
        n = len(par); ch = children(par); U["sum_sq"] += n * n
        dep = [depth(par, v) for v in range(n)]
        smap, _ = label_map(par); per = []
        for v in range(1, n):
            U["positions"] += 1; U["leaves"] += not ch[v]; U["genesis_leaves"] += (not ch[v]) and par[v] == 0
        for aa in range(1, n):
            qpar, X, loc = rerooted(par, aa); xs = smap[aa]; rep_x = reps[xs]; ix = iso(qpar, rep_x)
            hold = []
            for f, (an, mn) in FAM.items():
                for th in THETAS:
                    h = 0
                    for q in X:
                        lhs, rhs = cnf_case(par, aa, q, TABLES[an], MT[mn], total(th)); h += lhs == rhs
                    truth[f][str(th)] += h; hold.append(h)
            zf = []
            for f in CONST:
                an, mn = FAM[f]; lhs, rhs = cnf_case(par, aa, aa, TABLES[an], MT[mn], ZERO)
                zero_fail[f] += lhs != rhs; zf.append(int(lhs != rhs))
            for q in X:
                U["cases"] += 1
                for f in arb:
                    an, mn = FAM[f]; lhs, rhs = cnf_case(par, aa, q, TABLES[an], MT[mn], ZERO)
                    for v in range(n):
                        r = {}
                        if v == 0:
                            r[cols[(cs, q)]] = r.get(cols[(cs, q)], Fr(0)) + 1
                        if v == aa:
                            c = cols[(xs, ix[loc[q]])]; r[c] = r.get(c, Fr(0)) - 1
                        arb[f].add(r, rhs[v] - lhs[v]); rows_arb[f].append((r, rhs[v] - lhs[v]))
                # composite table: a = 1, m = e_k
                cl = {}
                for k in range(1, D + 1):
                    ek = (lambda kk: (lambda j: Fr(1) if j == kk else Fr(0)))(k)
                    cl[k] = cnf_case(par, aa, q, one, ek, ZERO)
                for v in range(n):
                    r = {k - 1: cl[k][0][v] - cl[k][1][v] for k in range(1, D + 1)}
                    r[D] = (Fr(1) if v == 0 else Fr(0)) - (Fr(1) if v == aa else Fr(0))
                    comp.add(r); comp_rows.append(r)
            per.append([dep[aa], xs, hold, zf])
        # P1 invariance
        for l in range(1, n):
            if ch[l]:
                continue
            qY, mp = prune(par, l); sY, _ = label_map(qY); iy = iso(qY, reps[sY[0]])
            for z in range(n):
                r = {cols[(cs, z)]: Fr(1)}
                tgt = cols[(sY[0], iy[mp[z if z != l else par[l]]])]
                r[tgt] = r.get(tgt, Fr(0)) - 1
                inv.add(r); inv_rows.append(r)
        lines.append(json.dumps([cs, sorted(per, key=str)], separators=(",", ":")))
    U["truth"] = truth; U["zero_apex_fail"] = zero_fail
    topcols = sorted(cols[(cs, 0)] for cs in top)
    arbrep = {}
    for f, E in arb.items():
        rec = {"consistent": not E.inconsistent}
        if f != "G5":
            piv = E.rref(); nul = len(cols) - len(piv)
            neg = all(sum((v * Fr(-1) for v in r.values()), Fr(0)) == c for r, c in rows_arb[f])
            forced = sum(1 for c, (r, k) in piv.items() if len(r) == 1 and k == -1)
            free = sorted(c for c in range(len(cols)) if c not in piv)
            rec.update({"dim": nul, "neg_total_solves": neg, "forced_to_minus_one": forced, "free_are_top_roots": free == topcols})
        arbrep[f] = rec
    U["arbitrary"] = arbrep
    sol = [Fr(1)] * D + [Fr(-1)]
    U["composite"] = {"dim": ncomp - len(comp.piv),
                      "contains_const": all(sum((v * sol[c] for c, v in r.items()), Fr(0)) == 0 for r in comp_rows)}
    U["p1_invariant"] = {"dim": len(cols) - len(inv.piv),
                         "contains_total": all(sum(r.values(), Fr(0)) == 0 for r in inv_rows)}
    U["event"] = events(reps)
    U["digest"] = hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(sorted(reps)).encode()).hexdigest()
    return U


def background(n, l):
    return [Fr((-1) ** v * (v + 2), 1 + v % 3) if v != l else Fr(0) for v in range(n)]


def events(reps):
    E = {f: {"pn_ok": 0, "cases": 0, "conserved": 0, "contrast_ok": 0, "pairs": 0, "neg_id": 0} for f in CONST}
    for par in reps.values():
        n = len(par); ch = children(par)
        for f, mu in CONST.items():
            an, mn = FAM[f]; a, m = TABLES[an], MT[mn]; lam = total(-mu); e = E[f]
            for z in range(n):
                fr = fhat(par, unit(n, z), a, m, lam)
                e["neg_id"] += sum(fr[v] == -mu * (1 if v == z else 0) for v in range(n))
            for l in range(1, n):
                if ch[l]:
                    continue
                p = par[l]; q, mp = prune(par, l)
                for g in GS:
                    outs = []
                    for mem in (0, 1):
                        x = background(n, l); x[l] = g * mem; xp = P(x, par, l, mp)
                        fw = fhat(par, x, a, m, lam); fy = fhat(q, xp, a, m, lam)
                        ok = all(fy[mp[v]] == fw[v] + (fw[l] if v == p else 0) for v in range(n) if v != l)
                        e["cases"] += 1; e["pn_ok"] += ok; e["conserved"] += sum(xp) == sum(x)
                        if not ok:
                            VIOL.append("pn " + f)
                        outs.append((fw, fy))
                    (fw0, fy0), (fw1, fy1) = outs
                    e["pairs"] += 1
                    e["contrast_ok"] += fw1[p] - fw0[p] == 0 and fy1[mp[p]] - fy0[mp[p]] == -mu * g
    return E


def instances():
    one, a1 = MT["one"], TABLES["unit"]; s = lambda v: [str(t) for t in v]
    Z = {}
    for th, key in ((Fr(-1), "Z1.theta_neg1"), (Fr(0), "Z1.theta0")):
        lhs, rhs = cnf_case([None, 0], 1, 1, a1, one, total(th)); Z[key] = [s(lhs), s(rhs)]
    Z["Z2.total"] = s(fhat([None, 0, 1], unit(3, 2), a1, one, total(Fr(-1))))
    Z["Z2.zero"] = s(fhat([None, 0, 1], unit(3, 2), a1, one, ZERO))
    lhs, rhs = cnf_case([None, 0, 1], 1, 2, TABLES["depth"], one, total(Fr(-1))); Z["Z3.G5"] = [s(lhs), s(rhs)]
    U3 = universe(3)
    Z["Z4.inv_dim"] = U3["p1_invariant"]["dim"]
    lam = total(Fr(-1))
    b = fhat([None, 0], [Fr(0), Fr(1)], a1, one, lam)[0] - fhat([None, 0], [Fr(0), Fr(0)], a1, one, lam)[0]
    af = fhat([None], [Fr(1)], a1, one, lam)[0] - fhat([None], [Fr(0)], a1, one, lam)[0]
    Z["Z5.genesis"] = [str(b), str(af)]
    Z["Z6.arb_dim"] = U3["arbitrary"]["G1"]["dim"]
    Z["Z7.comp_dim"] = U3["composite"]["dim"]
    return Z


def controls(us):
    def rej(bad):
        return "ACCEPTED_WRONGLY" if bad else "REJECTED"
    c = {}
    c["R1_zero_datum_satisfies_CN_F_at_apex"] = rej(any(v != u["positions"] for u in us.values() for v in u["zero_apex_fail"].values()))
    c["R2_nonconstant_mu_satisfies_CN_F_everywhere"] = rej(any(u["truth"][f][t] == u["cases"] for u in us.values() for f in ("G5", "G6") for t in u["truth"][f]))
    c["R3_wrong_theta_satisfies_CN_F_somewhere"] = rej(any(u["truth"][f][str(th)] > 0 for u in us.values() for f, mu in CONST.items() for th in THETAS if th != -mu))
    c["R4_arbitrary_datum_space_wrong"] = rej(any(u["arbitrary"][f]["dim"] != u["top_carriers"] or not u["arbitrary"][f]["neg_total_solves"] for u in us.values() for f in ("G1", "G3")))
    c["R5_G5_arbitrary_system_consistent"] = rej(any(u["arbitrary"]["G5"]["consistent"] for u in us.values()))
    c["R6_p1_invariant_space_wrong"] = rej(any(u["p1_invariant"]["dim"] != 1 or not u["p1_invariant"]["contains_total"] for u in us.values()))
    c["R7_composite_space_wrong"] = rej(any(u["composite"]["dim"] != 1 or not u["composite"]["contains_const"] for u in us.values()))
    c["R8_event_violation"] = rej(any(e["pn_ok"] != e["cases"] or e["conserved"] != e["cases"] or e["contrast_ok"] != e["pairs"] for u in us.values() for e in u["event"].values()))
    return c


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "producer", "result_sha256": hashlib.sha256(res).hexdigest(), "universes": {}}
    for name, nmax in (("U7", 7), ("U8", 8)):
        cert["universes"][name] = universe(nmax)
    cert["instances"] = instances()
    cert["violations"] = sorted(set(VIOL))
    cert["controls"] = controls(cert["universes"])
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    for u in cert["universes"].values():
        print(json.dumps({k: u[k] for k in u if k not in ("digest",)}, sort_keys=True))
    print(json.dumps(cert["instances"]), cert["controls"], cert["violations"])


if __name__ == "__main__":
    main()
