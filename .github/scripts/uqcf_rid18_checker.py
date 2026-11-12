"""receiver_identification d18 freeze (section 24): CHECKER. Algorithmically independent of the producer (no import).
Trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; field by path sums of
a_depth * cone totals, verified against L phi = x by neighbour sums; reads in incident-edge coordinates; parameter and
Lemma 24.1 dimensions certified by a sparse mod-p rank (upper bound on the nullity) and explicit rational solution
families checked exactly against every row (lower bound)."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d18_review")
A = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k), "alt": lambda k: Fr(1 if k % 2 else -2)}
M = {"one": lambda k: Fr(1), "k": lambda k: Fr(k), "inv": lambda k: 1 / Fr(k), "alt": lambda k: Fr(1 if k % 2 else -2),
     "invalt": lambda k: 1 / Fr(1 if k % 2 else -2)}
FAMS = [("F1", "unit", "one"), ("F2", "three", "one"), ("F3", "depth", "inv"), ("F4", "alt", "invalt"),
        ("F5", "depth", "one"), ("F6", "unit", "k"), ("F7", "alt", "one")]
CONST = {"F1", "F2", "F3", "F4"}
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


def pkey(T, v):
    return ("b", T.dep[v], len(T.ch[v]))


def lin_reads(T, phi):
    """reads as sparse linear forms in the uniform parameters, edge coordinates."""
    y = edges(T, phi); F = [dict() for _ in range(T.n)]
    if T.ch[0]:
        F[0][("g0", len(T.ch[0]))] = sum((y[u] for u in T.ch[0]), Fr(0))
    for v in range(1, T.n):
        F[v][pkey(T, v)] = F[v].get(pkey(T, v), Fr(0)) - y[v]
        if T.ch[v]:
            key = ("g", T.dep[v], len(T.ch[v])); F[v][key] = F[v].get(key, Fr(0)) + sum((y[u] for u in T.ch[v]), Fr(0))
    return F


def sub(a, b, s=1):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, Fr(0)) - s * v
    return r


def ssum(fs):
    r = {}
    for f in fs:
        for k, v in f.items():
            r[k] = r.get(k, Fr(0)) + v
    return r


def level(key):
    return key[1] if key[0] == "b" else (key[1] + 1 if key[0] == "g" else 1)


def elimination(trees, a, D):
    ps = set(); R = {k: RankP() for k in ("PN", "SC", "K", "ALL")}; rows = []
    for T in trees:
        for v in range(1, T.n):
            ps.add(pkey(T, v))
            if T.ch[v]:
                ps.add(("g", T.dep[v], len(T.ch[v])))
        if T.ch[0]:
            ps.add(("g0", len(T.ch[0])))
    order = sorted(ps, key=str); col = {p: i for i, p in enumerate(order)}
    def put(name, row):
        rr = {col[k]: v for k, v in row.items() if v != 0}
        R[name].add(rr); R["ALL"].add(rr); rows.append(row)
    for T in trees:
        leaves = [v for v in range(1, T.n) if not T.ch[v]]
        for z in range(1, T.n):
            x = basis(T.n, z); FW = lin_reads(T, field(T, x, a)); kw = ssum(FW); put("K", kw)
            for l in leaves:
                Y, new = T.without(l); FY = lin_reads(Y, field(Y, Pmap(T, x, l, new), a)); p = T.par[l]
                put("SC", sub(ssum(FY), kw))
                for v in range(T.n):
                    if v == l:
                        continue
                    r = sub(FY[new[v]], FW[v])
                    if v == p:
                        r = sub(r, FW[l])
                    put("PN", r)
    lower = all(sum((c for k, c in row.items() if level(k) == j), Fr(0)) == 0 for j in range(1, D + 1) for row in rows)
    present = {j for j in range(1, D + 1) if any(level(p) == j for p in order)}
    return {k: len(order) - r.rank() for k, r in R.items()}, lower and present == set(range(1, D + 1)), len(order)


def lemma(T):
    n = T.n
    nb = {v: [v] + ([T.par[v]] if v else []) + T.ch[v] for v in range(n)}
    unk = [(v, q) for v in range(n) for q in nb[v]]; ix = {u: i for i, u in enumerate(unk)}
    rows = [{ix[(v, q)]: 1 for q in nb[v]} for v in range(n)]
    rows += [{ix[(v, q)]: 1 for v in range(n) if (v, q) in ix} for q in range(n)]
    Rk = RankP()
    for r in rows:
        Rk.add(r)
    upper = len(unk) - Rk.rank()
    ok = True
    for c in range(1, n):  # explicit edge-weight reads m = e_c: f_c = -y_c, f_par = +y_c
        p = T.par[c]; sol = {ix[(c, c)]: -1, ix[(c, p)]: 1, ix[(p, c)]: 1, ix[(p, p)]: -1}
        ok &= all(sum(r.get(i, 0) * s for i, s in sol.items()) == 0 for r in rows)
    # lower bound n-1 (each edge-weight read has its own (c, par c) entry); equality certifies span = edge-local reads
    return upper, ok and upper == n - 1


def family(T, an, mn):
    a, m = A[an], M[mn]; mu = lambda k: m(k) * a(k); n = T.n
    K = True; comp = 0; gen = True; R = {}
    for z in range(1, n):
        x = basis(n, z); f = reads(T, field(T, x, a), m); R[z] = f
        K &= sum(f) == 0
        c = {v: sum((x[w] for w in T.sub[v]), Fr(0)) for v in range(1, n)}
        for v in range(n):
            if v == 0:
                pred = mu(1) * sum((c[u] for u in T.ch[0]), Fr(0))
            else:
                k = T.dep[v]; pred = -mu(k) * c[v] + mu(k + 1) * sum((c[u] for u in T.ch[v]), Fr(0))
            comp += f[v] == pred
        gen &= f[0] == mu(1)
    blind = [False] + [all(R[z][p] == 0 for z in T.sub[p] - {p}) for p in range(1, n)]
    own = [False] + [all(R[z][p] == (-mu(T.dep[p]) if z == p else 0) for z in range(1, n)) for p in range(1, n)]
    return K, comp, gen, blind, own


def rsf(T, a_v, mn):
    m = M[mn]; X, new = T.cone(a_v); ok = True
    for q in X.sub[0]:
        psi = [Fr(0)] * X.n; psi[q] = Fr(1)
        h = [psi[new[v]] if v in new else psi[0] for v in range(T.n)]
        lhs = reads(T, h, m); fx = reads(X, psi, m)
        ok &= all(lhs[v] == (fx[new[v]] if v in new else 0) for v in range(T.n))
    return ok


def bg(n, l):
    return [Fr((-1) ** v * (v + 2), 1 + v % 3) if v != l else Fr(0) for v in range(n)]


def universe(nmax):
    trees = [Tree.from_tuple(t) for t in grow(nmax)]; D = nmax - 1
    U = {"carriers": len(trees), "positions": 0, "positions_with_children": 0, "leaves": 0, "genesis_leaves": 0, "cones": 0,
         "lemma_ok_carriers": 0, "R1_fail_prunings": 0, "R2_fail_carriers": 0,
         "families": {f: {"K_carriers": 0, "composite": 0, "genesis_read": 0, "blind": 0, "own_grade": 0} for f, _, _ in FAMS},
         "rs_f": {k: 0 for k in ("one", "k", "inv", "alt")},
         "event": {f: {"pn_cases": 0, "pn_ok": 0, "nonroot_contrast_ok": 0, "nonroot_blind_before": 0, "genesis_contrast_ok": 0}
                   for f, _, _ in FAMS}, "total": {}}
    for f, an, mn in FAMS:
        if f in CONST:
            mu1 = M[mn](1) * A[an](1)
            U["total"][f] = {str(t): {"contrast_ok": 0, "blind_before": 0, "pn_cases": 0, "pn_ok": 0} for t in (-mu1, Fr(0), Fr(2))}
            U["total"][f]["neg_id"] = 0
    lines = []
    for T in trees:
        n = T.n; leaves = [v for v in range(1, n) if not T.ch[v]]
        U["positions"] += n - 1; U["positions_with_children"] += n - 1 - len(leaves); U["leaves"] += len(leaves)
        U["genesis_leaves"] += sum(T.par[l] == 0 for l in leaves)
        ld, lok = lemma(T); U["lemma_ok_carriers"] += lok
        fr = {}
        for f, an, mn in FAMS:
            K, comp, gen, blind, own = family(T, an, mn); fr[f] = (blind, own); F = U["families"][f]
            F["K_carriers"] += K; F["composite"] += comp; F["genesis_read"] += gen and n >= 2
            F["blind"] += sum(blind); F["own_grade"] += sum(own)
        rsl = []
        for av in range(1, n):
            if T.ch[av]:
                flags = [int(rsf(T, av, mn)) for mn in ("one", "k", "inv", "alt")]; rsl.append([T.dep[av]] + flags)
                for mn, fl in zip(("one", "k", "inv", "alt"), flags):
                    U["rs_f"][mn] += fl
        U["cones"] += len(rsl)
        verts = sorted([T.dep[v], len(T.ch[v])] + [int(fr[f][0][v]) for f, _, _ in FAMS] + [int(fr[f][1][v]) for f, _, _ in FAMS]
                       for v in range(1, n))
        lines.append(json.dumps([T.cs[0], ld, verts, sorted(rsl)], separators=(",", ":")))
        # events
        for f, an, mn in FAMS:
            a, m = A[an], M[mn]; mu = lambda k: m(k) * a(k); E = U["event"][f]
            ths = [-mu(1), Fr(0), Fr(2)] if f in CONST else []
            for l in leaves:
                Y, new = T.without(l); p = T.par[l]; k = T.dep[p]
                for g in GS:
                    res = []
                    for mem in (0, 1):
                        x = bg(n, l); x[l] = g * mem; xp = Pmap(T, x, l, new)
                        fw = reads(T, field(T, x, a), m); fy = reads(Y, field(Y, xp, a), m)
                        ok = all(fy[new[v]] - fw[v] == (fw[l] if v == p else 0) for v in new)
                        E["pn_cases"] += 1; E["pn_ok"] += ok
                        if not ok:
                            VIOL.append("pn")
                        res.append((x, xp, fw, fy))
                    b = res[1][2][p] - res[0][2][p]; af = res[1][3][new[p]] - res[0][3][new[p]]
                    if p:
                        E["nonroot_contrast_ok"] += b == g * (mu(k + 1) - mu(k)) and af == -mu(k) * g
                        E["nonroot_blind_before"] += b == 0
                    else:
                        E["genesis_contrast_ok"] += b == mu(1) * g and af == 0
                        for th in ths:
                            t = U["total"][f][str(th)]
                            tot = [(r[2][0] + th * sum(r[0]), r[3][0] + th * sum(r[1])) for r in res]
                            tb = tot[1][0] - tot[0][0]; ta = tot[1][1] - tot[0][1]
                            t["contrast_ok"] += tb == (mu(1) + th) * g and ta == th * g
                            t["blind_before"] += tb == 0
                            for r, (bw, by) in zip(res, tot):
                                t["pn_cases"] += 1; t["pn_ok"] += by - bw == r[2][l]
            if f in CONST:
                th = -mu(1)
                for z in range(n):
                    x = basis(n, z); fz = reads(T, field(T, x, a), m); fz[0] += th * sum(x)
                    U["total"][f]["neg_id"] += sum(fz[v] == -mu(1) * x[v] for v in range(n))
        # controls: cone read (beta=1, gamma=0) and child-count rule, unit table
        one = A["unit"]
        for l in leaves:
            Y, new = T.without(l); p = T.par[l]; bad = False
            for z in range(1, n):
                x = basis(n, z); yw = edges(T, field(T, x, one)); yy = edges(Y, field(Y, Pmap(T, x, l, new), one))
                fw = [Fr(0)] + [-yw[v] for v in range(1, n)]; fy = [Fr(0)] + [-yy[v] for v in range(1, Y.n)]
                bad |= not all(fy[new[v]] - fw[v] == (fw[l] if v == p else 0) for v in new)
            U["R1_fail_prunings"] += bad
        def cc(x):
            y = edges(T, field(T, x, one))
            return sum((y[u] for u in T.ch[0]), Fr(0)) + sum((-(1 + len(T.ch[v])) * y[v] + sum((y[u] for u in T.ch[v]), Fr(0))
                                                               for v in range(1, n)), Fr(0))
        U["R2_fail_carriers"] += any(cc(basis(n, z)) != 0 for z in range(1, n))
    U["elimination"] = {}
    for an in ("unit", "depth", "alt"):
        dims, ok, npar = elimination(trees, A[an], D)
        U["elimination"][an] = {"dims": dims, "family_exact": ok}
    U["parameters"] = npar; U["max_depth"] = D
    U["digest"] = hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(sorted(T.cs[0] for T in trees)).encode()).hexdigest()
    return U


def instances():
    ch2 = Tree.from_tuple((((),),))
    def rd(T, x, an, mn):
        return [str(v) for v in reads(T, field(T, x, A[an]), M[mn])]
    Z = {"Z1.e2": rd(ch2, basis(3, 2), "unit", "one"), "Z1.e1": rd(ch2, basis(3, 1), "unit", "one"),
         "Z2.depth_one": rd(ch2, basis(3, 2), "depth", "one"), "Z2.depth_inv": rd(ch2, basis(3, 2), "depth", "inv"),
         "Z3.lemma_dim": lemma(Tree.from_tuple((((), ()),)))[0]}
    c4 = Tree.from_tuple(((((),),),))
    Z["Z4.rsf_alt"] = [rsf(c4, 1, "alt"), rsf(c4, 2, "alt")]
    c2 = Tree.from_tuple(((),)); Y, new = c2.without(1)
    for name, th in (("Z5.theta0", Fr(0)), ("Z5.theta_neg1", Fr(-1))):
        def g0(T, x):
            return reads(T, field(T, x, A["unit"]), M["one"])[0] + th * sum(x)
        b = g0(c2, [Fr(0), Fr(1)]) - g0(c2, [Fr(0), Fr(0)])
        af = g0(Y, Pmap(c2, [Fr(0), Fr(1)], 1, new)) - g0(Y, Pmap(c2, [Fr(0), Fr(0)], 1, new))
        Z[name] = [str(b), str(af)]
    y = edges(ch2, field(ch2, basis(3, 1), A["unit"]))
    Z["Z6.childcount_sum"] = str(y[1] + (-(1 + 1) * y[1] + y[2]) + (-(1 + 0) * y[2]))
    return Z


def controls(us):
    def rej(bad):
        return "ACCEPTED_WRONGLY" if bad else "REJECTED"
    return {"R1_cone_read_satisfies_PN": rej(any(u["R1_fail_prunings"] == 0 for u in us.values())),
            "R2_childcount_rule_satisfies_K": rej(any(u["R2_fail_carriers"] == 0 for u in us.values())),
            "R3_F5_blind_at_every_position_with_children": rej(any(u["families"]["F5"]["blind"] == u["positions"] for u in us.values())),
            "R4_inverse_depth_reads_satisfy_RS_F": rej(any(u["rs_f"]["inv"] == u["cones"] for u in us.values())),
            "R5_PN_space_larger_than_depth_tables": rej(any(e["dims"]["PN"] > u["max_depth"] for u in us.values()
                                                            for e in u["elimination"].values())),
            "R6_genesis_blind_with_theta_zero": rej(any(u["total"][f]["0"]["blind_before"] > 0 for u in us.values() for f in CONST)),
            "R7_named_family_violates_PN": rej(any(e["pn_ok"] != e["pn_cases"] for u in us.values() for e in u["event"].values())),
            "R8_lemma_dim_or_structure_fails": rej(any(u["lemma_ok_carriers"] != u["carriers"] for u in us.values()))}


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "checker", "result_sha256": hashlib.sha256(res).hexdigest(),
            "universes": {"U7": universe(7), "U8": universe(8)}}
    cert["instances"] = instances(); cert["violations"] = sorted(set(VIOL)); cert["controls"] = controls(cert["universes"])
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps(cert["instances"]), cert["controls"], cert["violations"])


if __name__ == "__main__":
    main()
