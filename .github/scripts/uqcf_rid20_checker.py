"""receiver_identification d20 freeze (section 26, every vertex is a possible receiver): CHECKER. Algorithmically
independent of the producer (no import). Trees grown by leaf attachment with nested-tuple canonical forms and BFS
relabelling; isomorphisms by canonical DFS orders; dimensions certified by a sparse mod-p rank (upper bound on the nullity)
and explicit rational solution families checked exactly against every row, with a mod-p rank of the family (lower bound);
depth-matrix reads by summing nu over common ancestors; field by path sums of a_depth * cone totals, verified against
L phi = x° by neighbour sums; reads in incident-edge coordinates."""
import hashlib, json, sys
from fractions import Fraction as Fr

RESULT_SHA = "2e10cfddb22129177e304e7a4456055d69769f42c36be811277c856cbd32883c"
PRIME = 2147483629
VIOL = []


def need(c, msg):
    if not c:
        VIOL.append(msg)


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
    allt = [()]; layer = {()}
    for _ in range(nmax - 1):
        nxt = set()
        for t in layer:
            nxt |= attach(t)
        layer = {norm(t) for t in nxt}; allt += sorted(layer, key=cstr)
    return allt


class T:
    """labelled tree from a children list; BFS-labelled when built from a tuple"""
    def __init__(self, ch):
        self.ch = [list(c) for c in ch]; self.n = len(ch); self.par = [None] * self.n
        for v in range(self.n):
            for u in self.ch[v]:
                self.par[u] = v
        self.dep = [0] * self.n; order = [0]
        for v in order:
            for u in self.ch[v]:
                self.dep[u] = self.dep[v] + 1; order.append(u)
        self.anc = []
        for v in range(self.n):
            a = set([v]); x = v
            while self.par[x] is not None:
                x = self.par[x]; a.add(x)
            self.anc.append(a)          # ancestors-or-self
        memo = {}

        def s(v):
            if v not in memo:
                memo[v] = "(" + "".join(sorted(s(u) for u in self.ch[v])) + ")"
            return memo[v]
        self.code = s(0); self.s = s
        pos = {}; st = [0]
        while st:                         # canonical DFS order
            v = st.pop(); pos[v] = len(pos)
            st += sorted(self.ch[v], key=s, reverse=True)
        self.pos = pos

    @staticmethod
    def from_tuple(t):
        ch = [[]]; q = [(t, 0)]
        for node, v in q:
            for c in node:
                ch.append([]); w = len(ch) - 1; ch[v].append(w); q.append((c, w))
        return T(ch)

    def leaves(self):
        return [v for v in range(1, self.n) if not self.ch[v]]

    def induced(self, S):
        S = sorted(S, key=lambda v: (self.dep[v], v)); mp = {v: i for i, v in enumerate(S)}
        return T([[mp[u] for u in self.ch[v] if u in mp] for v in S]), mp


def rank_p(rows):
    piv = {}
    for r0 in rows:
        r = {c: x % PRIME for c, x in r0.items() if x % PRIME}
        while r:
            c = min(r)
            if c in piv:
                f = r[c]
                for cc, vv in piv[c].items():
                    x = (r.get(cc, 0) - f * vv) % PRIME
                    if x:
                        r[cc] = x
                    else:
                        r.pop(cc, None)
            else:
                inv = pow(r[c], PRIME - 2, PRIME); piv[c] = {cc: vv * inv % PRIME for cc, vv in r.items()}
                break
    return len(piv)


def modp(x):
    return x.numerator * pow(x.denominator, PRIME - 2, PRIME) % PRIME


def nu_read(t, nu, x):
    s = [sum((nu.get((t.dep[v], t.dep[w]), Fr(0)) * x[z] for z in range(t.n) if x[z] for w in (t.anc[v] & t.anc[z])), Fr(0))
         for v in range(t.n)]
    return [s[v] - sum((s[c] for c in t.ch[v]), Fr(0)) for v in range(t.n)]


A_T = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k), "alt": lambda k: Fr(1 if k % 2 else -2)}
M_T = {"one": lambda k: Fr(1), "inv": lambda k: 1 / Fr(k), "invalt": lambda k: 1 / Fr(1 if k % 2 else -2)}
FAMS = [("G1", "unit", "one"), ("G2", "three", "one"), ("G3", "depth", "inv"), ("G4", "alt", "invalt"),
        ("G5", "depth", "one"), ("G6", "alt", "one")]
THETAS = [Fr(-1), Fr(-3), Fr(0), Fr(2)]


def field_read(t, x, a, m, th):
    tot = sum(x, Fr(0)); c = [sum((x[z] for z in range(t.n) if v in t.anc[z]), Fr(0)) for v in range(t.n)]
    y = {v: a(t.dep[v]) * c[v] for v in range(1, t.n)}
    phi = [sum((y[w] for w in t.anc[v] if w), Fr(0)) for v in range(t.n)]
    xo = list(x); xo[0] -= tot
    for v in range(t.n):                     # L phi = x° by neighbour sums
        lap = sum(((phi[v] - phi[u]) / a(t.dep[u]) for u in t.ch[v]), Fr(0))
        if v:
            lap += (phi[v] - phi[t.par[v]]) / a(t.dep[v])
        need(lap == xo[v], "Laplacian check")
    out = []
    for v in range(t.n):
        inc = sum((y[u] for u in t.ch[v]), Fr(0))
        out.append(m(1) * inc + th * tot if v == 0 else -m(t.dep[v]) * y[v] + m(t.dep[v] + 1) * inc)
    return out


def unit(n, i):
    x = [Fr(0)] * n; x[i] = Fr(1); return x


def prune(t, l):
    return t.induced([v for v in range(t.n) if v != l])


def P(t, l, r):
    Y, mp = prune(t, l); out = [Fr(0)] * Y.n
    for v in range(t.n):
        out[mp[t.par[l]] if v == l else mp[v]] += r[v]
    return Y, out


class Uni:
    def __init__(self, N):
        self.N = N; self.trees = [T.from_tuple(x) for x in grow(N)]; self.col = {}
        for t in sorted(self.trees, key=lambda t: t.code):
            for i in range(t.n):
                for j in range(t.n):
                    self.col[(t.code, i, j)] = len(self.col)

    def c(self, t, v, z):
        return self.col[(t.code, t.pos[v], t.pos[z])]


def rows(U):
    R = {k: [] for k in ("PN", "Z", "CR", "CC", "S", "SL", "CNF", "GP", "W2")}
    c = U.c
    for t in U.trees:
        n = t.n; lv = t.leaves()
        for l in lv:
            p = t.par[l]; Y, mp = prune(t, l)
            for z in range(n):
                zz = mp[p] if z == l else mp[z]
                for v in mp:
                    r = {c(Y, mp[v], zz): 1}; r[c(t, v, z)] = r.get(c(t, v, z), 0) - 1
                    if v == p:
                        r[c(t, l, z)] = r.get(c(t, l, z), 0) - 1
                    R["PN"].append({k: x for k, x in r.items() if x})
            R["Z"] += [{c(t, v, l): 1} for v in range(n) if v != l]
            R["CR"].append({c(t, p, l): 1})
            R["CC"] += [{c(t, v, l): 1} for v in t.anc[l] if v != l]
        for z in range(n):
            for v in range(n):
                if v not in t.anc[z]:
                    R["S"].append({c(t, v, z): 1})
                    if z in lv:
                        R["SL"].append({c(t, v, z): 1})
        for a in range(1, n):
            X, mp = t.induced([v for v in range(n) if a in t.anc[v]])
            for z in mp:
                for v in range(n):
                    r = {c(t, v, z): 1}
                    if v in mp:
                        r[c(X, mp[v], mp[z])] = -1
                    R["CNF"].append(r)
        if n <= U.N - 1:
            Wp = T([[1]] + [[u + 1 for u in t.ch[v]] for v in range(n)])
            for z in range(n):
                for vp in range(n + 1):
                    r = {c(Wp, vp, z + 1): 1}
                    if vp:
                        r[c(t, vp - 1, z)] = -1
                    R["GP"].append(r)
        if U.N <= 7:
            nonroot = list(range(1, n))
            for mask in range(1 << (n - 1)):
                S = {0} | {nonroot[i] for i in range(n - 1) if mask >> i & 1}
                if len(S) == n or any(t.par[v] not in S for v in S if v):
                    continue
                X, mp = t.induced(S)
                for z in S:
                    for v in range(n):
                        r = {c(t, v, z): 1}
                        if v in mp:
                            r[c(X, mp[v], mp[z])] = -1
                        R["W2"].append(r)
    return R


SYSTEMS = {"PN": ["PN"], "PN+Z": ["PN", "Z"], "PN+CN_F": ["PN", "CNF"], "PN+G+": ["PN", "GP"], "PN+C_recv": ["PN", "CR"],
           "PN+C_climb": ["PN", "CC"], "PN+S": ["PN", "S"], "PN+S_leaf": ["PN", "SL"], "PN+S+C_climb": ["PN", "S", "CC"],
           "PN+S+C_recv": ["PN", "S", "CR"], "PN+S+G+": ["PN", "S", "GP"], "PN+W2_F": ["PN", "W2"],
           "PN+W2_F+C_recv": ["PN", "W2", "CR"]}


def E(*terms):
    d = {}
    for (k, j), x in terms:
        d[(k, j)] = d.get((k, j), Fr(0)) + Fr(x)
    return d


def small_null(N):
    """basis of the C_recv / C_climb nu-system: A(d-1,d-1)=A(d,d) (d=1..N-1), A(d,d-1)=0 (d<=N-2)"""
    idx = [(k, j) for k in range(N) for j in range(k + 1)]
    M = []
    for d in range(1, N):
        M.append([Fr(int(k == d - 1)) - Fr(int(k == d)) for (k, j) in idx])
        if d <= N - 2:
            M.append([Fr(int(k == d and j <= d - 1)) for (k, j) in idx])
    piv = []; r = 0
    for col in range(len(idx)):
        p = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]; M[r] = [x / M[r][col] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(col); r += 1
    out = []
    for fc in [c for c in range(len(idx)) if c not in piv]:
        v = {idx[fc]: Fr(1)}
        for i, pc in enumerate(piv):
            if M[i][fc]:
                v[idx[pc]] = -M[i][fc]
        out.append(v)
    return out


def families(N):
    I = E(*[((k, k), 1) for k in range(N)])
    gp = []
    for free in [None] + list(range(1, N)):
        nu = {}; r1 = {r: Fr(1 if free == r else 0) for r in range(1, N)}
        for k in range(N):
            for j in range(1, k + 1):
                nu[(k, j)] = r1[k - j + 1]
        nu[(0, 0)] = Fr(1 if free is None else 0)
        for k in range(1, N):
            nu[(k, 0)] = nu[(k - 1, 0)] - nu[(k, 1)]
        gp.append(nu)
    diag = [E(((k, k), 1)) for k in range(N)]
    return {"PN": [E(((k, j), 1)) for k in range(N) for j in range(k + 1)],
            "PN+Z": [I] + [E(((N - 1, w), 1), ((N - 1, N - 1), -1)) for w in range(N - 1)],
            "PN+CN_F": [I, E(((N - 1, 0), 1), ((N - 1, 1), -1))], "PN+G+": gp,
            "PN+C_recv": small_null(N), "PN+C_climb": small_null(N), "PN+S": diag, "PN+W2_F": diag,
            "PN+S_leaf": diag + [E(((N - 1, j), 1)) for j in range(N - 1)],
            "PN+S+C_climb": [I], "PN+S+C_recv": [I], "PN+S+G+": [I], "PN+W2_F+C_recv": [I]}


def vec_of(U, nu):
    v = {}
    for t in U.trees:
        for z in range(t.n):
            f = nu_read(t, nu, unit(t.n, z))
            for w in range(t.n):
                if f[w]:
                    v[U.c(t, w, z)] = f[w]
    return v


def holds(v, rws):
    return all(sum((v.get(c, 0) * x for c, x in r.items()), Fr(0)) == 0 for r in rws)


def pn_count(U, rd):
    g = 0; tot = 0
    for t in U.trees:
        for l in t.leaves():
            for z in range(t.n):
                x = unit(t.n, z); Y, y = P(t, l, x); tot += 1
                g += rd(Y, y) == P(t, l, rd(t, x))[1]
    return g, tot


def z_count(U, rd):
    return sum(all(f[v] == 0 for v in range(t.n) if v != a) for t in U.trees for a in t.leaves()
               for f in [rd(t, unit(t.n, a))])


def universe(N, elim):
    U = Uni(N); codes = sorted(t.code for t in U.trees)
    out = {"carriers": len(U.trees), "leaves": sum(len(t.leaves()) for t in U.trees),
           "genesis_leaves": sum(1 for t in U.trees for l in t.leaves() if t.par[l] == 0),
           "sum_n": sum(t.n for t in U.trees), "unknowns": len(U.col),
           "universe_digest": hashlib.sha256("\n".join(codes).encode()).hexdigest()}
    byc = {t.code: t for t in U.trees}
    out["digest"] = hashlib.sha256("\n".join(k + "|" + ",".join(map(str, sorted(byc[k].dep))) for k in codes).encode()).hexdigest()
    R = rows(U); out["row_counts"] = {k: len(v) for k, v in sorted(R.items()) if v}
    fams = families(N); dims = {}
    for nm in elim:
        rw = [r for s in SYSTEMS[nm] for r in R[s]]
        upper = len(U.col) - rank_p(rw)
        vecs = [vec_of(U, nu) for nu in fams[nm]]
        for v in vecs:
            need(holds(v, rw), "family member fails a row: %d %s" % (N, nm))
        lower = rank_p([{c: modp(x) for c, x in v.items()} for v in vecs])
        need(lower == len(vecs), "family not independent: %d %s" % (N, nm))
        need(upper == lower, "dimension not certified: %d %s upper %d lower %d" % (N, nm, upper, lower))
        dims[nm] = upper
    out["dims"] = dims
    if "PN+Z" in elim:
        ok = True
        for nu in fams["PN+Z"]:
            kap = nu.get((0, 0), Fr(0))
            for t in U.trees:
                if t.n <= N - 1:
                    for z in range(t.n):
                        f = nu_read(t, nu, unit(t.n, z)); ok &= all(f[v] == (kap if v == z else 0) for v in range(t.n))
        out["kappa_id_small"] = ok
        nu = E(*[((k, k), 1) for k in range(N)], ((1, 0), 1))
        out["R6_holds"] = holds(vec_of(U, nu), R["PN"] + R["Z"])
    if N == 3:
        return out
    ident = {}; pn = {}; zt = {}
    for g, an, mn in FAMS:
        a, m = A_T[an], M_T[mn]
        for th in THETAS:
            key = g + ":" + str(th)
            nu = {(0, 0): th}; nu.update({(k, k): -m(k) * a(k) for k in range(1, N + 1)})
            rd = lambda t, x, a=a, m=m, th=th: field_read(t, x, a, m, th)
            ident[key] = sum(rd(t, unit(t.n, z)) == nu_read(t, nu, unit(t.n, z)) for t in U.trees for z in range(t.n))
            pn[key] = pn_count(U, rd)[0]; zt[key] = z_count(U, rd)
    out.update({"field_identity": ident, "field_pn": pn, "field_z": zt, "pn_cases": pn_count(U, lambda t, x: x)[1]})
    gd = lambda t, x: [sum(x, Fr(0))] + [Fr(0)] * (t.n - 1)
    f0 = lambda t, x: field_read(t, x, A_T["unit"], M_T["one"], Fr(0))
    nuo = E(*[((k, k), 1) for k in range(N)], ((2, 0), 1), ((2, 1), -1))
    wo = lambda t, x: nu_read(t, nuo, x)
    wit = {nm: {"pn": pn_count(U, rd)[0], "z_holds": z_count(U, rd)} for nm, rd in
           (("genesis_dump", gd), ("field_zero", f0), ("nu_off", wo))}
    climb = nonanc = 0; s_all = True
    for t in U.trees:
        for a_ in t.leaves():
            f = wo(t, unit(t.n, a_))
            climb += all(f[v] == 0 for v in t.anc[a_] if v != a_)
            nonanc += any(f[v] != 0 for v in range(t.n) if v not in t.anc[a_])
        for z in range(t.n):
            f = wo(t, unit(t.n, z)); s_all &= all(f[v] == 0 for v in range(t.n) if v not in t.anc[z])
    wit["nu_off"].update({"climb_blind": climb, "nonancestor_leaves": nonanc, "S_everywhere": s_all})
    out["witnesses"] = wit
    ev = {"cases": 0, "pn": 0, "conserved": 0, "blind": 0, "contrast": 0}
    for kap in (Fr(1), Fr(-3), Fr(1, 2)):
        rd = lambda t, x, kap=kap: [kap * q for q in x]
        for t in U.trees:
            for l in t.leaves():
                p = t.par[l]; Y, mp = prune(t, l)
                for g in (Fr(1), Fr(-2), Fr(5, 3)):
                    x = [Fr(0) if v == l else Fr(-1) ** v * Fr(v + 2, 1 + v % 3) for v in range(t.n)]
                    x2 = list(x); x2[l] = g; ev["cases"] += 1
                    _, y = P(t, l, x); _, y2 = P(t, l, x2)
                    ev["pn"] += rd(Y, y) == P(t, l, rd(t, x))[1] and rd(Y, y2) == P(t, l, rd(t, x2))[1]
                    ev["conserved"] += sum(y) == sum(x) and sum(y2) == sum(x2)
                    ev["blind"] += rd(t, x)[p] == rd(t, x2)[p]
                    ev["contrast"] += rd(Y, y2)[mp[p]] - rd(Y, y)[mp[p]] == kap * g
    out["event"] = ev
    return out


def controls(u):
    PRED = {"G1:-1", "G3:-1", "G4:-1", "G2:-3"}
    def rj(bad):
        return "ACCEPTED_WRONGLY" if bad else "REJECTED"
    big = [u["U7"], u["U8"]]
    return {"R1_genesis_dump_leaf_blind": rj(any(x["witnesses"]["genesis_dump"]["z_holds"] > 0 for x in big)),
            "R2_zero_datum_field_leaf_blind": rj(any(x["witnesses"]["field_zero"]["z_holds"] > 0 for x in big)),
            "R3_nu_off_cone_local": rj(any(x["witnesses"]["nu_off"]["S_everywhere"] for x in big)),
            "R4_climb_alone_forces_identity": rj(any(x["dims"]["PN+C_climb"] == 1 for x in big)),
            "R5_apex_alone_forces_identity": rj(any(x["dims"]["PN+G+"] == 1 for x in big)),
            "R6_offdiagonal_passes_leaf_blindness": rj(any(u[k]["R6_holds"] for k in u)),
            "R7_unpredicted_field_setting_leaf_blind": rj(any(v == x["leaves"] for x in big for k, v in x["field_z"].items()
                                                              if k not in PRED)),
            "R8_event_violation": rj(any(x["event"][k] != x["event"]["cases"] for x in big for k in x["event"])),
            "R9_PN_Z_not_identity_on_small": rj(any(not u[k]["kappa_id_small"] for k in u))}


def instances():
    I = {}
    t = T([[1, 3], [2], [], []])          # 0 -> {1 -> 2, 3}
    nuo = E(*[((k, k), 1) for k in range(4)], ((2, 0), 1), ((2, 1), -1))
    I["Z1"] = [str(q) for q in nu_read(t, nuo, unit(4, 3))]
    t2 = T([[1], []])
    I["Z3.dump"] = [str(sum(unit(2, 1))), "0"]
    I["Z3.field0"] = [str(q) for q in field_read(t2, unit(2, 1), A_T["unit"], M_T["one"], Fr(0))]
    x = [Fr(0), Fr(0)]; x2 = [Fr(0), Fr(1)]
    _, y = P(t2, 1, x); _, y2 = P(t2, 1, x2)
    I["Z4.before"] = [str(x[0]), str(x2[0])]; I["Z4.after"] = str(y2[0] - y[0])
    I["Z5"] = [str(q) for q in field_read(T([[1], [2], []]), unit(3, 2), A_T["depth"], M_T["one"], Fr(-1))]
    return I


def main():
    ALL = list(SYSTEMS)
    unis = {"U3": universe(3, ["PN", "PN+Z", "PN+CN_F"]), "U7": universe(7, ALL), "U8": universe(8, ALL[:11])}
    inst = instances(); inst["Z2"] = unis["U3"]["dims"]
    cert = {"role": "checker", "result_sha256": RESULT_SHA, "universes": unis, "instances": inst,
            "controls": controls(unis), "violations": VIOL[:50]}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({u: v["dims"] for u, v in unis.items()}, sort_keys=True), "violations", len(VIOL))


if __name__ == "__main__":
    main()
