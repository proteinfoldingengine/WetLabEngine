"""receiver_identification d21 freeze (section 27, a leaf reads only what it holds, and one record climb fixes the reads up
to its depth): CHECKER. Algorithmically independent of the producer (no import). Trees grown by leaf attachment with
nested-tuple canonical forms and BFS relabelling; isomorphisms by canonical DFS orders; dimensions certified by a sparse
mod-p rank (upper bound on the nullity) and explicit rational solution families checked exactly against every row, with a
mod-p rank of the family (lower bound); depth-matrix reads by summing nu over common ancestors of reader and source."""
import hashlib, json, sys
from fractions import Fraction as Fr

RESULT_SHA = "7c0eb6f830e6ca167ec62839e760d092c88fb1084ce72c91877b7c314414b229"
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



def chain_t(d):
    return T([[v + 1] for v in range(d)] + [[]])


def cherry_t(d):
    ch = [[v + 1] for v in range(d)] + [[], []]
    ch[d - 1].append(d + 1)
    return T(ch)


def rank_ext(piv, rows):
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
    return piv


def rows(U):
    R = {"PN": [], "SL": [], "W21": [], "CR": []}
    c = U.c
    for t in U.trees:
        n = t.n
        for l in t.leaves():
            p = t.par[l]; Y, mp = prune(t, l)
            for z in range(n):
                zz = mp[p] if z == l else mp[z]
                for v in mp:
                    r = {c(Y, mp[v], zz): 1}; r[c(t, v, z)] = r.get(c(t, v, z), 0) - 1
                    if v == p:
                        r[c(t, l, z)] = r.get(c(t, l, z), 0) - 1
                    r = {k: x for k, x in r.items() if x}
                    if r:
                        R["PN"].append(r)
            for z in mp:
                R["SL"].append({c(t, l, z): 1})
                for v in range(n):
                    r = {c(t, v, z): 1}
                    if v != l:
                        r[c(Y, mp[v], mp[z])] = r.get(c(Y, mp[v], mp[z]), 0) - 1
                    r = {k: x for k, x in r.items() if x}
                    if r:
                        R["W21"].append(r)
            R["CR"].append({c(t, p, l): 1})
    for d in range(1, U.N):
        ct = chain_t(d)
        R["CL%d" % d] = [{c(ct, d - 1, d): 1}]
        R["BU%d" % d] = [{c(cherry_t(d), d - 1, d + 1): 1}] if d + 2 <= U.N else R["CL%d" % d]
    return R


def E(*terms):
    d = {}
    for (k, j), x in terms:
        d[(k, j)] = d.get((k, j), Fr(0)) + Fr(x)
    return d


def families(N):
    diag = [E(((k, k), 1)) for k in range(N)]
    F = {"PN": [E(((k, j), 1)) for k in range(N) for j in range(k + 1)], "PN+S_L": diag, "PN+W2_1": diag,
         "PN+S_L+C_recv": [E(*[((k, k), 1) for k in range(N)])]}
    for D in range(1, N):
        top = [E(*[((k, k), 1) for k in range(D + 1)])] + [E(((k, k), 1)) for k in range(D + 1, N)]
        F["PN+S_L+CL_%d" % D] = top; F["PN+S_L+BU_%d" % D] = top
        F["PN+CL_%d" % D] = [E(((k, j), 1), ((k, k), -1)) for k in range(1, N) for j in range(k)] + top
    return F


def systems(N):
    S = {"PN": ["PN"], "PN+S_L": ["PN", "SL"], "PN+W2_1": ["PN", "W21"], "PN+S_L+C_recv": ["PN", "SL", "CR"]}
    for D in range(1, N):
        S["PN+S_L+CL_%d" % D] = ["PN", "SL"] + ["CL%d" % d for d in range(1, D + 1)]
        S["PN+S_L+BU_%d" % D] = ["PN", "SL"] + ["BU%d" % d for d in range(1, D + 1)]
        S["PN+CL_%d" % D] = ["PN"] + ["CL%d" % d for d in range(1, D + 1)]
    return S


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
    return [sum((v.get(c, 0) * x for c, x in r.items()), Fr(0)) == 0 for r in rws]


def tables(N):
    off = E(*[((k, k), 1) for k in range(N)], ((2, 0), 1), ((2, 1), -1))
    gen = {(k, j): Fr((k + 1) * (-1) ** j, j + 2) + Fr(int(j == k)) for k in range(N) for j in range(k + 1)}
    return {"nu_off": off, "nu_gen": gen, "T1": {(k, k): Fr(k * k + 1) for k in range(N)},
            "T2": {(k, k): Fr(-1) ** k * Fr(k + 2, k + 1) for k in range(N)}}


def zext(t, l, y):
    _, mp = prune(t, l)
    return [Fr(0) if v == l else y[mp[v]] for v in range(t.n)]


def universe(N):
    U = Uni(N); codes = sorted(t.code for t in U.trees)
    out = {"carriers": len(U.trees), "leaves": sum(len(t.leaves()) for t in U.trees),
           "sum_n": sum(t.n for t in U.trees), "unknowns": len(U.col),
           "universe_digest": hashlib.sha256("\n".join(codes).encode()).hexdigest()}
    byc = {t.code: t for t in U.trees}
    out["digest"] = hashlib.sha256("\n".join(k + "|" + ",".join(map(str, sorted(byc[k].dep))) for k in codes).encode()).hexdigest()
    R = rows(U); out["row_counts"] = {k: len(v) for k, v in sorted(R.items()) if v and k[:2] not in ("CL", "BU")}
    nun = len(U.col); fams = families(N); S = systems(N); dims = {}
    base = {"PN": rank_ext({}, R["PN"])}
    base["PN+S_L"] = rank_ext(dict(base["PN"]), R["SL"])
    vecs_cache = {}
    for nm, parts in S.items():
        start = "PN+S_L" if parts[:2] == ["PN", "SL"] else "PN"
        extra = [r for s in parts[(2 if start == "PN+S_L" else 1):] for r in R[s]]
        upper = nun - len(rank_ext(dict(base[start]), extra))
        rw = [r for s in parts for r in R[s]]
        vecs = []
        for nu in fams[nm]:
            key = tuple(sorted(nu.items()))
            if key not in vecs_cache:
                vecs_cache[key] = vec_of(U, nu)
            vecs.append(vecs_cache[key])
        for v in vecs:
            need(all(holds(v, rw)), "family member fails a row: %d %s" % (N, nm))
        lower = len(rank_ext({}, [{c: modp(x) for c, x in v.items()} for v in vecs]))
        need(lower == len(vecs), "family not independent: %d %s" % (N, nm))
        need(upper == lower, "dimension not certified: %d %s upper %d lower %d" % (N, nm, upper, lower))
        dims[nm] = upper
    out["dims"] = dims
    TB = tables(N)
    hz = {"carriers": [], "vertices": [], "sharp": [], "ok": True}
    for D in range(1, N):
        H = {(k, k): Fr(-2) + 7 * max(0, k - D) for k in range(N)}
        c1 = c2 = c3 = 0
        for t in U.trees:
            cols = [nu_read(t, H, unit(t.n, z)) for z in range(t.n)]
            if max(t.dep) <= D:
                c1 += 1
                hz["ok"] &= all(cols[z][v] == (Fr(-2) if v == z else 0) for z in range(t.n) for v in range(t.n))
            for v in range(t.n):
                if t.dep[v] < D:
                    c2 += 1; hz["ok"] &= all(cols[z][v] == (Fr(-2) if v == z else 0) for z in range(t.n))
                elif t.dep[v] == D:
                    for ch in t.ch[v]:
                        c3 += 1; hz["ok"] &= cols[ch][v] == -7
        hz["carriers"].append(c1); hz["vertices"].append(c2); hz["sharp"].append(c3)
    out["horizon"] = hz
    acq = True
    for D in range(1, N):
        nu = {(k, k): Fr(int(k <= D)) for k in range(N)}
        for d in range(1, D + 1):
            ct = chain_t(d); Y, y = P(ct, d, unit(d + 1, d)); _, mp = prune(ct, d)
            acq &= nu_read(ct, nu, unit(d + 1, d))[d - 1] == 0 and nu_read(Y, nu, y)[mp[d - 1]] == 1
    out["family_acquisition"] = acq
    led = {"cases": 0, "ok": 0}; ker = {"cases": 0, "ok": 0, "T1_zero": 0, "nonzero_gen": 0, "nonzero_off": 0}
    for t in U.trees:
        for l in t.leaves():
            p = t.par[l]; Y, mp = prune(t, l)
            for z in range(t.n):
                f = nu_read(t, TB["nu_gen"], unit(t.n, z)); Yt, y = P(t, l, unit(t.n, z)); g = nu_read(Y, TB["nu_gen"], y)
                led["cases"] += 1
                led["ok"] += g[mp[p]] == f[p] + f[l] and all(g[mp[v]] == f[v] for v in mp if v != p) and sum(g) == sum(f)
            for j in range(Y.n):
                xI = zext(t, l, unit(Y.n, j))
                res = {}
                for nm in ("nu_gen", "nu_off", "T1"):
                    A = nu_read(t, TB[nm], xI); B = zext(t, l, nu_read(Y, TB[nm], unit(Y.n, j)))
                    res[nm] = (A, [a - b for a, b in zip(A, B)])
                A, Dv = res["nu_gen"]; ker["cases"] += 1
                ker["ok"] += all(Dv[v] == 0 for v in mp if v != p) and Dv[p] + Dv[l] == 0 and Dv[l] == A[l] \
                    and not any(P(t, l, Dv)[1])
                ker["nonzero_gen"] += any(x != 0 for x in Dv)
                ker["nonzero_off"] += any(x != 0 for x in res["nu_off"][1])
                ker["T1_zero"] += all(x == 0 for x in res["T1"][1])
    out["ledger"] = led; out["kernel"] = ker
    ba = {"cases": 0, "before_after": 0, "pair": 0}
    for nm in ("T1", "T2"):
        nu = TB[nm]
        for t in U.trees:
            for l in t.leaves():
                p = t.par[l]; d = t.dep[l]; Y, mp = prune(t, l); hi, lo = nu[(d - 1, d - 1)], nu[(d, d)]
                f = nu_read(t, nu, unit(t.n, l)); _, y = P(t, l, unit(t.n, l)); ba["cases"] += 1
                ba["before_after"] += f[p] == hi - lo and f[l] == lo and nu_read(Y, nu, y)[mp[p]] == hi
                r = (lo - hi) / hi; x = unit(t.n, l); x[p] = r; _, y = P(t, l, x)
                ba["pair"] += nu_read(t, nu, x)[p] == 0 and nu_read(Y, nu, y)[mp[p]] == lo
    out["before_after"] = ba
    voff = vec_of(U, TB["nu_off"])
    cl = [r for d in range(1, N) for r in R["CL%d" % d]]
    out["nu_off"] = {"pn_and_climbs_hold": all(holds(voff, R["PN"] + cl)), "SL_violations": holds(voff, R["SL"]).count(False)}
    out["R7_holds"] = all(holds(vec_of(U, E(*[((k, k), 1) for k in range(N)], ((1, 0), 1))), R["PN"] + R["SL"]))
    ev = {"cases": 0, "pn": 0, "conserved": 0, "blind": 0, "contrast": 0}
    for kap in (Fr(1), Fr(-3), Fr(1, 2)):
        rd = lambda tt, x, kap=kap: [kap * q for q in x]
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
    def rj(bad):
        return "ACCEPTED_WRONGLY" if bad else "REJECTED"
    big = {7: u["U7"], 8: u["U8"]}
    fail = False
    for x in big.values():
        fail |= x["ledger"]["ok"] != x["ledger"]["cases"] or x["kernel"]["ok"] != x["kernel"]["cases"]
        fail |= x["kernel"]["T1_zero"] != x["kernel"]["cases"]
        fail |= x["before_after"]["before_after"] != x["before_after"]["cases"] or x["before_after"]["pair"] != x["before_after"]["cases"]
        fail |= any(v != x["event"]["cases"] for v in x["event"].values())
        fail |= not (x["nu_off"]["pn_and_climbs_hold"] and x["family_acquisition"])
    return {"R1_nu_off_leaf_local": rj(any(x["nu_off"]["SL_violations"] == 0 for x in big.values())),
            "R2_climb_without_leaf_locality_forces_identity": rj(any(x["dims"]["PN+CL_%d" % (N - 1)] == 1 for N, x in big.items())),
            "R3_no_depth_horizon": rj(any(x["dims"]["PN+S_L+CL_%d" % D] == 1 for N, x in big.items() for D in range(1, N - 1))),
            "R4_identity_below_horizon": rj(not all(x["horizon"]["ok"] for x in big.values())),
            "R5_ledger_forces_zero_extension_square": rj(any(x["dims"]["PN+W2_1"] == x["dims"]["PN"] for x in big.values())),
            "R6_general_defect_vanishes": rj(any(x["kernel"]["nonzero_gen"] == 0 for x in big.values())),
            "R7_offdiagonal_passes_leaf_locality": rj(any(x["R7_holds"] for x in big.values())),
            "R8_case_failure": rj(fail)}


def instances():
    I = {}
    TB = tables(3); t = chain_t(2)
    A = nu_read(t, TB["nu_off"], unit(3, 0)); B = nu_read(T([[]]), TB["nu_off"], unit(1, 0)) + [Fr(0), Fr(0)]
    I["Y1.read"] = [str(q) for q in A]; I["Y1.defect"] = [str(a - b) for a, b in zip(A, B)]
    I["Y3"] = [str(q) for q in nu_read(t, {(0, 0): Fr(1), (1, 1): Fr(1), (2, 2): Fr(8)}, unit(3, 2))]
    nu = TB["T1"]; r = (nu[(2, 2)] - nu[(1, 1)]) / nu[(1, 1)]; x = [Fr(0), r, Fr(1)]; Y, y = P(t, 2, x); _, mp = prune(t, 2)
    I["Y4"] = {"r": str(r), "before": str(nu_read(t, nu, x)[1]), "after": str(nu_read(Y, nu, y)[mp[1]])}
    t5 = T([[1], [2, 3], [], []]); Y, y = P(t5, 3, unit(4, 3)); _, mp = prune(t5, 3)
    I["Y5"] = {"before": str(nu_read(t5, nu, unit(4, 3))[1]), "after": str(nu_read(Y, nu, y)[mp[1]])}
    return I


def main():
    unis = {"U3": universe(3), "U7": universe(7), "U8": universe(8)}
    inst = instances(); inst["Y2"] = unis["U3"]["dims"]
    cert = {"role": "checker", "result_sha256": RESULT_SHA, "universes": unis, "instances": inst,
            "controls": controls(unis), "violations": VIOL[:50]}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({u: v["dims"] for u, v in unis.items()}, sort_keys=True), "violations", len(VIOL))


if __name__ == "__main__":
    main()
