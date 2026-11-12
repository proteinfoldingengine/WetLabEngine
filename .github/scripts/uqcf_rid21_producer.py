"""receiver_identification d21 freeze (section 27, a leaf reads only what it holds, and one record climb fixes the reads up
to its depth): PRODUCER. Pure-Python exact Fractions. Parent-array enumeration with AHU codes; condition rows in vertex
coordinates on one unknown read matrix per carrier class; dimensions by exact sparse Gauss-Jordan over Q (PN echelon basis
computed once, extended per system); depth-matrix reads as S = N C in cone coordinates, vertex value s_v - sum of children."""
import hashlib, json, sys
from fractions import Fraction as Fr

RESULT_SHA = "7c0eb6f830e6ca167ec62839e760d092c88fb1084ce72c91877b7c314414b229"
VIOL = []


def need(c, msg):
    if not c:
        VIOL.append(msg)


# ---------------- trees ----------------
def kids(par):
    ch = [[] for _ in par]
    for v in range(1, len(par)):
        ch[par[v]].append(v)
    return ch


def ahu(par):
    ch = kids(par); memo = {}

    def s(v):
        if v not in memo:
            memo[v] = "(" + "".join(sorted(s(u) for u in ch[v])) + ")"
        return memo[v]
    return s


def enum(N):
    reps = {"()": [None]}; layer = [[None]]
    for _ in range(N - 1):
        nxt = []
        for par in layer:
            for a in range(len(par)):
                q = par + [a]; k = ahu(q)(0)
                if k not in reps:
                    reps[k] = q; nxt.append(q)
        layer = nxt
    return reps


def iso_to(par, rep):
    """rooted isomorphism v -> rep vertex"""
    sa, sb = ahu(par), ahu(rep); ca, cb = kids(par), kids(rep); mp = {0: 0}; st = [(0, 0)]
    while st:
        u, w = st.pop()
        for p_, q_ in zip(sorted(ca[u], key=sa), sorted(cb[w], key=sb)):
            mp[p_] = q_; st.append((p_, q_))
    return mp


def depths(par):
    d = [0] * len(par)
    for v in range(1, len(par)):
        x = v
        while par[x] is not None:
            x = par[x]; d[v] += 1
    return d


def ancs(par, z):
    out = []
    while par[z] is not None:
        z = par[z]; out.append(z)
    return out


def le(par, w, z):
    return w == z or w in ancs(par, z)


def leaves(par):
    ch = kids(par)
    return [v for v in range(1, len(par)) if not ch[v]]


def prune(par, l):
    mp = {}; j = 0
    for v in range(len(par)):
        if v != l:
            mp[v] = j; j += 1
    q = [None] * (len(par) - 1)
    for v in range(1, len(par)):
        if v != l:
            q[mp[v]] = mp[par[v]]
    return q, mp


def sub(par, S):
    S = sorted(S); mp = {v: i for i, v in enumerate(S)}
    return [None] + [mp[par[v]] for v in S[1:]], mp


def cone(par, a):
    S = [v for v in range(len(par)) if le(par, a, v)]
    S.sort(); mp = {v: i for i, v in enumerate(S)}
    return [None] + [mp[par[v]] for v in S[1:]], mp


# ---------------- unknown indexing ----------------
class Universe:
    def __init__(self, N):
        self.N = N; self.reps = enum(N); self.idx = {}
        for k, p in sorted(self.reps.items()):
            for i in range(len(p)):
                for j in range(len(p)):
                    self.idx[(k, i, j)] = len(self.idx)
        self.cache = {}

    def u(self, par, v, z):
        t = tuple(par)
        if t not in self.cache:
            k = ahu(par)(0); self.cache[t] = (k, iso_to(par, self.reps[k]))
        k, mp = self.cache[t]
        return self.idx[(k, mp[v], mp[z])]


def row(*terms):
    r = {}
    for c, x in terms:
        r[c] = r.get(c, 0) + x
    return {c: Fr(x) for c, x in r.items() if x}



def chain(n):
    return [None] + list(range(n - 1))


def build(U):
    N = U.N
    R = {k: [] for k in ("PN", "SL", "W21", "CR")}
    u = U.u
    for par in U.reps.values():
        n = len(par)
        for l in leaves(par):
            p = par[l]; Y, mp = prune(par, l)
            for z in range(n):
                zz = mp[p] if z == l else mp[z]
                for v in range(n):
                    if v == l:
                        continue
                    terms = [(u(Y, mp[v], zz), 1), (u(par, v, z), -1)]
                    if v == p:
                        terms.append((u(par, l, z), -1))
                    r = row(*terms)
                    if r:
                        R["PN"].append(r)
            for z in range(n):
                if z != l:
                    R["SL"].append(row((u(par, l, z), 1)))
                    for v in range(n):
                        r = row((u(par, v, z), 1), *([(u(Y, mp[v], mp[z]), -1)] if v != l else []))
                        if r:
                            R["W21"].append(r)
            R["CR"].append(row((u(par, p, l), 1)))
    for d in range(1, N):
        R["CL%d" % d] = [row((u(chain(d + 1), d - 1, d), 1))]
        R["BU%d" % d] = [row((u(chain(d + 1) + [d - 1], d - 1, d + 1), 1))] if d + 2 <= N else R["CL%d" % d]
    return R


def extend(piv, rows):
    for r0 in rows:
        r = dict(r0)
        while r:
            c = min(r)
            if c in piv:
                f = r[c]
                for cc, vv in piv[c].items():
                    x = r.get(cc, 0) - f * vv
                    if x:
                        r[cc] = x
                    else:
                        r.pop(cc, None)
            else:
                f = r[c]; piv[c] = {cc: vv / f for cc, vv in r.items()}
                break
    return piv


def nu_read(par, nu, x):
    n = len(par); d = depths(par); ch = kids(par)
    C = [sum((x[t] for t in range(n) if le(par, w, t)), Fr(0)) for w in range(n)]  # cone coordinates
    s = [sum((nu.get((d[v], d[w]), Fr(0)) * C[w] for w in range(n) if le(par, w, v)), Fr(0)) for v in range(n)]
    return [s[v] - sum((s[c] for c in ch[v]), Fr(0)) for v in range(n)]


def Pv(par, l, r):
    Y, mp = prune(par, l); out = [Fr(0)] * len(Y)
    for v in range(len(par)):
        out[mp[par[l]] if v == l else mp[v]] += r[v]
    return Y, out


def delta(n, i):
    x = [Fr(0)] * n; x[i] = Fr(1); return x


def Iext(par, l, y):
    """zero extension from X = W minus leaf l (pruned labels) to W"""
    _, mp = prune(par, l)
    return [Fr(0) if v == l else y[mp[v]] for v in range(len(par))]


def tables(N):
    T = {"nu_off": {(k, k): Fr(1) for k in range(N)}, "T1": {(k, k): Fr(k * k + 1) for k in range(N)},
         "T2": {(k, k): Fr((-1) ** k * (k + 2), k + 1) for k in range(N)}}
    T["nu_off"][(2, 0)] = Fr(1); T["nu_off"][(2, 1)] = Fr(-1)
    T["nu_gen"] = {(k, j): Fr((k + 1) * (-1) ** j, j + 2) + (1 if j == k else 0) for k in range(N) for j in range(k + 1)}
    return T


def sat(U, nu, rows):
    vec = {}
    for k, p in U.reps.items():
        for z in range(len(p)):
            f = nu_read(p, nu, delta(len(p), z))
            for v in range(len(p)):
                vec[U.idx[(k, v, z)]] = f[v]
    return [sum(vec[c] * x for c, x in r.items()) == 0 for r in rows]


def universe(N):
    U = Universe(N); reps = U.reps; keys = sorted(reps)
    out = {"carriers": len(reps), "leaves": sum(len(leaves(p)) for p in reps.values()),
           "sum_n": sum(len(p) for p in reps.values()), "unknowns": len(U.idx),
           "universe_digest": hashlib.sha256("\n".join(keys).encode()).hexdigest()}
    out["digest"] = hashlib.sha256("\n".join(k + "|" + ",".join(map(str, sorted(depths(reps[k])))) for k in keys).encode()).hexdigest()
    R = build(U); nun = len(U.idx)
    out["row_counts"] = {k: len(v) for k, v in sorted(R.items()) if v and not k[:2] in ("CL", "BU")}
    pn = extend({}, R["PN"]); sl = extend(dict(pn), R["SL"]); dims = {"PN": nun - len(pn), "PN+S_L": nun - len(sl)}
    dims["PN+W2_1"] = nun - len(extend(dict(pn), R["W21"]))
    dims["PN+S_L+C_recv"] = nun - len(extend(dict(sl), R["CR"]))
    for D in range(1, N):
        cl = [r for d in range(1, D + 1) for r in R["CL%d" % d]]; bu = [r for d in range(1, D + 1) for r in R["BU%d" % d]]
        dims["PN+S_L+CL_%d" % D] = nun - len(extend(dict(sl), cl))
        dims["PN+S_L+BU_%d" % D] = nun - len(extend(dict(sl), bu))
        dims["PN+CL_%d" % D] = nun - len(extend(dict(pn), cl))
    out["dims"] = dims
    T = tables(N)
    # horizon
    hz = {"carriers": [], "vertices": [], "sharp": [], "ok": True}
    for D in range(1, N):
        H = {(k, k): Fr(-2) if k <= D else Fr(-2 + 7 * (k - D)) for k in range(N)}
        c1 = c2 = c3 = 0
        for p in reps.values():
            n = len(p); dp = depths(p); ch = kids(p)
            F = [nu_read(p, H, delta(n, z)) for z in range(n)]   # F[z][v]
            if max(dp) <= D:
                c1 += 1; hz["ok"] &= all(F[z][v] == (-2 if v == z else 0) for z in range(n) for v in range(n))
            for v in range(n):
                if dp[v] < D:
                    c2 += 1; hz["ok"] &= all(F[z][v] == (-2 if v == z else 0) for z in range(n))
                if dp[v] == D:
                    for c in ch[v]:
                        c3 += 1; hz["ok"] &= F[c][v] == -7
        hz["carriers"].append(c1); hz["vertices"].append(c2); hz["sharp"].append(c3)
    out["horizon"] = hz
    # explicit-family acquisition: kappa = 1 member gains 1 after each chain step
    acq = True
    for D in range(1, N):
        nu = {(k, k): Fr(1 if k <= D else 0) for k in range(N)}
        for d in range(1, D + 1):
            W = chain(d + 1); Y, y = Pv(W, d, delta(d + 1, d))
            acq &= nu_read(W, nu, delta(d + 1, d))[d - 1] == 0 and nu_read(Y, nu, y)[d - 1] == 1
    out["family_acquisition"] = acq
    # ledger and kernel with nu_gen; T1 defect zero
    led = {"cases": 0, "ok": 0}; ker = {"cases": 0, "ok": 0, "T1_zero": 0, "nonzero_gen": 0, "nonzero_off": 0}
    for p in reps.values():
        n = len(p)
        for l in leaves(p):
            q = p[l]; Y, mp = prune(p, l)
            for z in range(n):
                x = delta(n, z); f = nu_read(p, T["nu_gen"], x); Yy, y = Pv(p, l, x); g = nu_read(Y, T["nu_gen"], y)
                good = g[mp[q]] == f[q] + f[l] and all(g[mp[v]] == f[v] for v in range(n) if v not in (l, q)) and sum(g) == sum(f)
                led["cases"] += 1; led["ok"] += good
            for zy in range(n - 1):
                y = delta(n - 1, zy); xI = Iext(p, l, y)
                for nm in ("nu_gen", "nu_off", "T1"):
                    A = nu_read(p, T[nm], xI); B = Iext(p, l, nu_read(Y, T[nm], y)); Dv = [a - b for a, b in zip(A, B)]
                    if nm == "nu_gen":
                        ker["cases"] += 1
                        ker["ok"] += all(Dv[v] == 0 for v in range(n) if v not in (l, q)) and Dv[q] == -Dv[l] and Dv[l] == A[l] \
                            and all(t == 0 for t in Pv(p, l, Dv)[1])
                        ker["nonzero_gen"] += any(Dv)
                    elif nm == "nu_off":
                        ker["nonzero_off"] += any(Dv)
                    else:
                        ker["T1_zero"] += not any(Dv)
    out["ledger"] = led; out["kernel"] = ker
    # before/after and correlated pairs
    ba = {"cases": 0, "before_after": 0, "pair": 0}
    for nm in ("T1", "T2"):
        nu = T[nm]
        for p in reps.values():
            n = len(p); dp = depths(p)
            for l in leaves(p):
                q = p[l]; d = dp[l]; Y, mp = prune(p, l); a, b = nu[(d - 1, d - 1)], nu[(d, d)]
                f = nu_read(p, nu, delta(n, l)); _, y = Pv(p, l, delta(n, l))
                ba["cases"] += 1
                ba["before_after"] += f[q] == a - b and f[l] == b and nu_read(Y, nu, y)[mp[q]] == a
                r = -(a - b) / a; x = delta(n, l); x[q] += r; _, y = Pv(p, l, x)
                ba["pair"] += nu_read(p, nu, x)[q] == 0 and nu_read(Y, nu, y)[mp[q]] == b
    out["before_after"] = ba
    # witness nu_off
    cl_all = [r for d in range(1, N) for r in R["CL%d" % d]]
    s = sat(U, T["nu_off"], R["PN"] + cl_all + R["SL"])
    npn = len(R["PN"]) + len(cl_all)
    out["nu_off"] = {"pn_and_climbs_hold": all(s[:npn]), "SL_violations": sum(1 for t in s[npn:] if not t)}
    nu7 = {(k, k): Fr(1) for k in range(N)}; nu7[(1, 0)] = Fr(1)
    out["R7_holds"] = all(sat(U, nu7, R["PN"] + R["SL"]))
    # kappa id events
    ev = {"cases": 0, "pn": 0, "conserved": 0, "blind": 0, "contrast": 0}
    for kap in (Fr(1), Fr(-3), Fr(1, 2)):
        rd = lambda pp, x, kap=kap: [kap * t for t in x]
        for p in reps.values():
            n = len(p)
            for l in leaves(p):
                for g in (Fr(1), Fr(-2), Fr(5, 3)):
                    x = [Fr(0) if v == l else Fr((-1) ** v * (v + 2), 1 + v % 3) for v in range(n)]
                    x2 = list(x); x2[l] += g; ev["cases"] += 1; q = p[l]
                    Y, y = Pv(p, l, x); _, y2 = Pv(p, l, x2); _, mp = prune(p, l)
                    ev["pn"] += (rd(Y, y) == Pv(p, l, rd(p, x))[1]) and (rd(Y, y2) == Pv(p, l, rd(p, x2))[1])
                    ev["conserved"] += sum(y, Fr(0)) == sum(x, Fr(0)) and sum(y2, Fr(0)) == sum(x2, Fr(0))
                    ev["blind"] += rd(p, x)[q] == rd(p, x2)[q]
                    ev["contrast"] += rd(Y, y2)[mp[q]] - rd(Y, y)[mp[q]] == kap * g
    out["event"] = ev
    return out


def instances():
    I = {}
    T = tables(3); W = [None, 0, 1]
    # X = {0}: zero-extend delta_0 from the one-vertex carrier to the chain 0-1-2
    A = nu_read(W, T["nu_off"], [Fr(1), Fr(0), Fr(0)]); B = nu_read([None], T["nu_off"], [Fr(1)]) + [Fr(0), Fr(0)]
    I["Y1.read"] = [str(t) for t in A]; I["Y1.defect"] = [str(a - b) for a, b in zip(A, B)]
    H = {(0, 0): Fr(1), (1, 1): Fr(1), (2, 2): Fr(8)}
    I["Y3"] = [str(t) for t in nu_read(W, H, delta(3, 2))]
    nu = T["T1"]; a, b = nu[(1, 1)], nu[(2, 2)]; r = -(a - b) / a; x = [Fr(0), r, Fr(1)]; Y, y = Pv(W, 2, x)
    I["Y4"] = {"r": str(r), "before": str(nu_read(W, nu, x)[1]), "after": str(nu_read(Y, nu, y)[1])}
    W5 = [None, 0, 1, 1]; Y, y = Pv(W5, 3, delta(4, 3)); _, mp = prune(W5, 3)
    I["Y5"] = {"before": str(nu_read(W5, nu, delta(4, 3))[1]), "after": str(nu_read(Y, nu, y)[mp[1]])}
    return I


def controls(u):
    flag = lambda b: "ACCEPTED_WRONGLY" if b else "REJECTED"
    big = [u["U7"], u["U8"]]
    return {"R1_nu_off_leaf_local": flag(any(x["nu_off"]["SL_violations"] == 0 for x in big)),
            "R2_climb_without_leaf_locality_forces_identity": flag(any(x["dims"]["PN+CL_%d" % (N - 1)] == 1 for N, x in ((7, big[0]), (8, big[1])))),
            "R3_no_depth_horizon": flag(any(x["dims"]["PN+S_L+CL_%d" % D] == 1 for N, x in ((7, big[0]), (8, big[1])) for D in range(1, N - 1))),
            "R4_identity_below_horizon": flag(not all(x["horizon"]["ok"] for x in big)),
            "R5_ledger_forces_zero_extension_square": flag(any(x["dims"]["PN+W2_1"] == x["dims"]["PN"] for x in big)),
            "R6_general_defect_vanishes": flag(any(x["kernel"]["nonzero_gen"] == 0 for x in big)),
            "R7_offdiagonal_passes_leaf_locality": flag(any(x["R7_holds"] for x in big)),
            "R8_case_failure": flag(any(x[k]["ok"] != x[k]["cases"] for x in big for k in ("ledger", "kernel"))
                                    or any(x["kernel"]["T1_zero"] != x["kernel"]["cases"] for x in big)
                                    or any(x["before_after"][k] != x["before_after"]["cases"] for x in big for k in ("before_after", "pair"))
                                    or any(x["event"][k] != x["event"]["cases"] for x in big for k in x["event"])
                                    or not all(x["nu_off"]["pn_and_climbs_hold"] and x["family_acquisition"] for x in big))}


def main():
    unis = {"U3": universe(3), "U7": universe(7), "U8": universe(8)}
    inst = instances(); inst["Y2"] = unis["U3"]["dims"]
    cert = {"role": "producer", "result_sha256": RESULT_SHA, "universes": unis, "instances": inst, "controls": controls(unis), "violations": VIOL}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({u: v["dims"] for u, v in unis.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
