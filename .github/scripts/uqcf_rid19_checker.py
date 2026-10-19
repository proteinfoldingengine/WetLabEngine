"""receiver_identification d19 freeze (section 25, the Genesis datum is forced): CHECKER. Algorithmically independent of
the producer (no import). Trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; field by
path sums of a_depth * cone totals, verified against L phi = x° by neighbour sums; reads in incident-edge coordinates;
isomorphisms by canonical DFS orders; dimensions certified by a sparse mod-p rank (upper bound on the nullity) and
explicit rational solutions checked exactly against every row (lower bound); consistency by an explicit solution or an
explicit contradictory row."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d19_review")
A = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k), "alt": lambda k: Fr(1 if k % 2 else -2)}
M = {"one": lambda k: Fr(1), "inv": lambda k: 1 / Fr(k), "invalt": lambda k: 1 / Fr(1 if k % 2 else -2)}
FAMS = [("G1", "unit", "one"), ("G2", "three", "one"), ("G3", "depth", "inv"), ("G4", "alt", "invalt"),
        ("G5", "depth", "one"), ("G6", "alt", "one")]
MU = {"G1": Fr(1), "G2": Fr(3), "G3": Fr(1), "G4": Fr(1)}
THETAS = [Fr(-1), Fr(-3), Fr(0), Fr(2)]
GS = [Fr(1), Fr(-2), Fr(5, 3)]
PRIME = 2147483629
VIOL = []


def cstr(t):
    return "(" + "".join(sorted(cstr(c) for c in t)) + ")"


def norm(t):
    return tuple(sorted(t, key=cstr))


def grow(nmax):
    def attach(t):
        res = {norm(t + ((),))}
        for i, c in enumerate(t):
            for c2 in attach(c):
                res.add(norm(t[:i] + (c2,) + t[i + 1:]))
        return res
    allt = {(): None}; layer = {()}
    for _ in range(nmax - 1):
        nxt = set()
        for t in layer:
            nxt |= attach(t)
        layer = {norm(t) for t in nxt}
        for t in layer:
            allt[t] = None
    return list(allt)


class Tree:
    def __init__(self, ch):
        self.ch = ch; self.n = len(ch); self.par = [None] * self.n
        for v in range(self.n):
            for u in ch[v]:
                self.par[u] = v
        self.dep = [0] * self.n; order = [0]
        for v in order:
            for u in ch[v]:
                self.dep[u] = self.dep[v] + 1; order.append(u)
        self.order = order
        self.sub = [None] * self.n
        for v in reversed(order):
            self.sub[v] = {v}.union(*[self.sub[u] for u in ch[v]])
        self.cs = [None] * self.n
        for v in reversed(order):
            self.cs[v] = "(" + "".join(sorted(self.cs[u] for u in ch[v])) + ")"

    @staticmethod
    def from_tuple(t):
        ch = [[]]; q = [(t, 0)]
        for node, v in q:
            for c in node:
                u = len(ch); ch.append([]); ch[v].append(u); q.append((c, u))
        return Tree(ch)

    def without(self, l):
        keep = [v for v in range(self.n) if v != l]; new = {v: i for i, v in enumerate(keep)}
        return Tree([[new[u] for u in self.ch[v] if u != l] for v in keep]), new

    def cone(self, a):
        keep = [a] + sorted(self.sub[a] - {a}); new = {v: i for i, v in enumerate(keep)}
        return Tree([[new[u] for u in self.ch[v]] for v in keep]), new


def field(T, x, a):
    c = {v: sum((x[z] for z in T.sub[v]), Fr(0)) for v in range(1, T.n)}
    phi = [Fr(0)] * T.n
    for v in T.order[1:]:
        phi[v] = phi[T.par[v]] + a(T.dep[v]) * c[v]
    xb = [x[0] - sum(x)] + list(x[1:])
    for v in range(1, T.n):
        lv = (phi[v] - phi[T.par[v]]) / a(T.dep[v]) - sum(((phi[u] - phi[v]) / a(T.dep[u]) for u in T.ch[v]), Fr(0))
        if lv != xb[v]:
            VIOL.append("laplacian")
    return phi


def edges(T, phi):
    return {v: phi[v] - phi[T.par[v]] for v in range(1, T.n)}


def reads(T, phi, m):
    y = edges(T, phi); f = [Fr(0)] * T.n
    f[0] = m(1) * sum((y[u] for u in T.ch[0]), Fr(0))
    for v in range(1, T.n):
        k = T.dep[v]; f[v] = -m(k) * y[v] + m(k + 1) * sum((y[u] for u in T.ch[v]), Fr(0))
    return f


def basis(n, z):
    x = [Fr(0)] * n; x[z] = Fr(1); return x


def Pmap(T, x, l, new):
    y = [Fr(0)] * (T.n - 1)
    for v in range(T.n):
        if v != l:
            y[new[v]] += x[v]
    y[new[T.par[l]]] += x[l]
    return y


def modp(q):
    q = Fr(q); return q.numerator % PRIME * pow(q.denominator % PRIME, PRIME - 2, PRIME) % PRIME


class RankP:
    def __init__(self):
        self.piv = {}
    def add(self, row):
        r = {c: modp(v) for c, v in row.items() if modp(v)}
        while r:
            c = min(r)
            if c not in self.piv:
                inv = pow(r[c], PRIME - 2, PRIME); self.piv[c] = {k: v * inv % PRIME for k, v in r.items()}
                return
            f = r[c]
            for k, v in self.piv[c].items():
                r[k] = (r.get(k, 0) - f * v) % PRIME
                if r[k] == 0:
                    del r[k]
    def rank(self):
        return len(self.piv)



def dfs_order(T):
    out = []; st = [0]
    while st:
        v = st.pop(); out.append(v)
        st.extend(sorted(T.ch[v], key=lambda u: T.cs[u], reverse=True))
    return out


def iso_to(T, R):
    assert T.cs[0] == R.cs[0]
    return dict(zip(dfs_order(T), dfs_order(R)))


def fhat(T, x, a, m, th):
    f = reads(T, field(T, x, a), m)
    if th is not None:
        f[0] += th * sum(x)
    return f


def jext(T, new, vals):
    inv = {i: v for v, i in new.items()}; out = [Fr(0)] * T.n
    for i, val in enumerate(vals):
        out[inv[i]] = val
    return out


def case(T, a_v, q, a, m, th):
    X, new = T.cone(a_v)
    lhs = fhat(T, basis(T.n, q), a, m, th)
    rhs = jext(T, new, fhat(X, basis(X.n, new[q]), a, m, th))
    return lhs, rhs, X, new


def dot(r, sol):
    return sum((v * sol(c) for c, v in r.items()), Fr(0))


def universe(nmax):
    trees = [Tree.from_tuple(t) for t in grow(nmax)]
    rep = {T.cs[0]: T for T in trees}; D = nmax - 1
    unknowns = [(T.cs[0], v) for T in trees for v in range(T.n)]
    tops = {(T.cs[0], 0) for T in trees if T.n == nmax}
    U = {"carriers": len(trees), "positions": sum(T.n - 1 for T in trees),
         "leaves": sum(1 for T in trees for v in range(1, T.n) if not T.ch[v]),
         "genesis_leaves": sum(1 for T in trees for v in T.ch[0] if not T.ch[v]),
         "cases": sum(len(T.sub[v]) for T in trees for v in range(1, T.n)), "unknowns": len(unknowns),
         "top_carriers": len(tops), "max_depth": max(max(T.dep) for T in trees), "sum_sq": sum(T.n * T.n for T in trees)}
    truth = {f: {str(t): 0 for t in THETAS} for f, _, _ in FAMS}; zero_fail = {f: 0 for f in MU}
    arb_rows = {f: [] for f in ("G1", "G3", "G5")}; comp_rows = []; inv_rows = []; lines = []
    for T in trees:
        cs = T.cs[0]; per = []
        for av in range(1, T.n):
            X, new = T.cone(av); R = rep[X.cs[0]]; ix = iso_to(X, R); hold = []
            for f, an, mn in FAMS:
                for th in THETAS:
                    h = 0
                    for q in T.sub[av]:
                        lhs, rhs, _, _ = case(T, av, q, A[an], M[mn], th); h += lhs == rhs
                    truth[f][str(th)] += h; hold.append(h)
            zf = []
            for f, an, mn in FAMS[:4]:
                lhs, rhs, _, _ = case(T, av, av, A[an], M[mn], None); zero_fail[f] += lhs != rhs; zf.append(int(lhs != rhs))
            for q in sorted(T.sub[av]):
                for f, an, mn in FAMS:
                    if f not in arb_rows:
                        continue
                    lhs, rhs, _, _ = case(T, av, q, A[an], M[mn], None)
                    for v in range(T.n):
                        r = {}
                        if v == 0:
                            r[(cs, q)] = Fr(1)
                        if v == av:
                            key = (X.cs[0], ix[new[q]]); r[key] = r.get(key, Fr(0)) - 1
                        arb_rows[f].append((r, rhs[v] - lhs[v]))
                per_k = {}
                for k in range(1, D + 1):
                    per_k[k] = case(T, av, q, A["unit"], (lambda kk: (lambda j: Fr(1 if j == kk else 0)))(k), None)
                for v in range(T.n):
                    r = {("mu", k): per_k[k][0][v] - per_k[k][1][v] for k in range(1, D + 1)}
                    r[("theta",)] = Fr(int(v == 0) - int(v == av))
                    comp_rows.append(r)
            per.append([T.dep[av], X.cs[0], hold, zf])
        for l in range(1, T.n):
            if T.ch[l]:
                continue
            Y, new = T.without(l); iy = iso_to(Y, rep[Y.cs[0]])
            for z in range(T.n):
                tgt = (Y.cs[0], iy[new[z] if z != l else new[T.par[l]]])
                r = {(cs, z): Fr(1)}; r[tgt] = r.get(tgt, Fr(0)) - 1
                inv_rows.append(r)
        lines.append(json.dumps([cs, sorted(per, key=str)], separators=(",", ":")))
    U["truth"] = truth; U["zero_apex_fail"] = zero_fail
    order = {u: i for i, u in enumerate(unknowns)}
    arb = {}
    for f, rows in arb_rows.items():
        rk = RankP()
        for r, c in rows:
            rk.add({order[k]: v for k, v in r.items() if v != 0})
        neg = all(dot(r, lambda c: Fr(-1)) == k for r, k in rows)
        contra = any(all(v == 0 for v in r.values()) and k != 0 for r, k in rows)
        if f == "G5":
            arb[f] = {"consistent": False if contra else (True if neg else None)}
            continue
        upper = len(unknowns) - rk.rank()
        lower_ok = all(r.get(t, Fr(0)) == 0 for r, _ in rows for t in tops)
        dim = upper if (lower_ok and upper == len(tops)) else None
        arb[f] = {"consistent": neg and not contra, "dim": dim, "neg_total_solves": neg,
                  "forced_to_minus_one": len(unknowns) - dim if (dim is not None and neg) else None,
                  "free_are_top_roots": dim is not None}
    U["arbitrary"] = arb
    rk = RankP(); cidx = {("mu", k): k - 1 for k in range(1, D + 1)}; cidx[("theta",)] = D
    for r in comp_rows:
        rk.add({cidx[k]: v for k, v in r.items() if v != 0})
    const = all(dot(r, lambda c: Fr(-1) if c == ("theta",) else Fr(1)) == 0 for r in comp_rows)
    U["composite"] = {"dim": (D + 1 - rk.rank()) if const else None, "contains_const": const}
    rk = RankP()
    for r in inv_rows:
        rk.add({order[k]: v for k, v in r.items() if v != 0})
    tot = all(dot(r, lambda c: Fr(1)) == 0 for r in inv_rows)
    U["p1_invariant"] = {"dim": (len(unknowns) - rk.rank()) if tot else None, "contains_total": tot}
    U["event"] = events(trees)
    U["digest"] = hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(sorted(rep)).encode()).hexdigest()
    return U


def bg(n, l):
    return [Fr((-1) ** v * (v + 2), 1 + v % 3) if v != l else Fr(0) for v in range(n)]


def events(trees):
    E = {f: {"pn_ok": 0, "cases": 0, "conserved": 0, "contrast_ok": 0, "pairs": 0, "neg_id": 0} for f in MU}
    for T in trees:
        for f, an, mn in FAMS[:4]:
            a, m, mu = A[an], M[mn], MU[f]; e = E[f]
            for z in range(T.n):
                fr = fhat(T, basis(T.n, z), a, m, -mu)
                e["neg_id"] += sum(1 for v in range(T.n) if fr[v] == (-mu if v == z else 0))
            for l in range(1, T.n):
                if T.ch[l]:
                    continue
                p = T.par[l]; Y, new = T.without(l); res = []
                for g in GS:
                    pair = []
                    for mem in (0, 1):
                        x = bg(T.n, l); x[l] = g * mem; xp = Pmap(T, x, l, new)
                        fw = fhat(T, x, a, m, -mu); fy = fhat(Y, xp, a, m, -mu)
                        ok = all(fy[new[v]] == fw[v] + (fw[l] if v == p else 0) for v in range(T.n) if v != l)
                        e["cases"] += 1; e["pn_ok"] += ok; e["conserved"] += sum(xp) == sum(x)
                        if not ok:
                            VIOL.append("pn " + f)
                        pair.append((fw, fy))
                    (fw0, fy0), (fw1, fy1) = pair
                    e["pairs"] += 1
                    e["contrast_ok"] += (fw1[p] - fw0[p] == 0) and (fy1[new[p]] - fy0[new[p]] == -mu * g)
    return E


def instances():
    s = lambda v: [str(t) for t in v]; Z = {}
    T2 = Tree.from_tuple(((),)); T3 = Tree.from_tuple((((),),))
    for th, key in ((Fr(-1), "Z1.theta_neg1"), (Fr(0), "Z1.theta0")):
        lhs, rhs, _, _ = case(T2, 1, 1, A["unit"], M["one"], th); Z[key] = [s(lhs), s(rhs)]
    Z["Z2.total"] = s(fhat(T3, basis(3, 2), A["unit"], M["one"], Fr(-1)))
    Z["Z2.zero"] = s(fhat(T3, basis(3, 2), A["unit"], M["one"], None))
    lhs, rhs, _, _ = case(T3, 1, 2, A["depth"], M["one"], Fr(-1)); Z["Z3.G5"] = [s(lhs), s(rhs)]
    U3 = universe(3)
    Z["Z4.inv_dim"] = U3["p1_invariant"]["dim"]
    T1 = Tree.from_tuple(())
    b = fhat(T2, [Fr(0), Fr(1)], A["unit"], M["one"], Fr(-1))[0] - fhat(T2, [Fr(0), Fr(0)], A["unit"], M["one"], Fr(-1))[0]
    af = fhat(T1, [Fr(1)], A["unit"], M["one"], Fr(-1))[0] - fhat(T1, [Fr(0)], A["unit"], M["one"], Fr(-1))[0]
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
    c["R3_wrong_theta_satisfies_CN_F_somewhere"] = rej(any(u["truth"][f][str(th)] > 0 for u in us.values() for f, mu in MU.items() for th in THETAS if th != -mu))
    c["R4_arbitrary_datum_space_wrong"] = rej(any(u["arbitrary"][f]["dim"] != u["top_carriers"] or not u["arbitrary"][f]["neg_total_solves"] for u in us.values() for f in ("G1", "G3")))
    c["R5_G5_arbitrary_system_consistent"] = rej(any(u["arbitrary"]["G5"]["consistent"] is not False for u in us.values()))
    c["R6_p1_invariant_space_wrong"] = rej(any(u["p1_invariant"]["dim"] != 1 or not u["p1_invariant"]["contains_total"] for u in us.values()))
    c["R7_composite_space_wrong"] = rej(any(u["composite"]["dim"] != 1 or not u["composite"]["contains_const"] for u in us.values()))
    c["R8_event_violation"] = rej(any(e["pn_ok"] != e["cases"] or e["conserved"] != e["cases"] or e["contrast_ok"] != e["pairs"] for u in us.values() for e in u["event"].values()))
    return c


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "checker", "result_sha256": hashlib.sha256(res).hexdigest(), "universes": {}}
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
