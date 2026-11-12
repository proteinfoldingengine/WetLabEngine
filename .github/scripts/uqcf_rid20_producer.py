"""receiver_identification d20 freeze (section 26, every vertex is a possible receiver): PRODUCER.
Pure-Python exact Fractions. Parent-array enumeration with AHU codes; condition rows in vertex coordinates on one unknown
read matrix per carrier class; dimensions by exact sparse Gauss-Jordan over Q; field by exact Gauss-Jordan solve of the
grounded weighted Laplacian; depth-matrix reads as S = N C in cone coordinates, vertex value s_v - sum of children."""
import hashlib, json, sys
from fractions import Fraction as Fr

RESULT_SHA = "2e10cfddb22129177e304e7a4456055d69769f42c36be811277c856cbd32883c"
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


def build(U):
    R = {k: [] for k in ("PN", "Z", "CR", "CC", "S", "SL", "CNF", "GP", "W2")}
    u = U.u
    for par in U.reps.values():
        n = len(par); lv = leaves(par); lvs = set(lv)
        for l in lv:
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
            for v in range(n):
                if v != l:
                    R["Z"].append(row((u(par, v, l), 1)))
            R["CR"].append(row((u(par, p, l), 1)))
            for v in ancs(par, l):
                R["CC"].append(row((u(par, v, l), 1)))
        for z in range(n):
            for v in range(n):
                if not le(par, v, z):
                    R["S"].append(row((u(par, v, z), 1)))
                    if z in lvs:
                        R["SL"].append(row((u(par, v, z), 1)))
        for a in range(1, n):
            X, mp = cone(par, a)
            for z in mp:
                for v in range(n):
                    r = row((u(par, v, z), 1), *([(u(X, mp[v], mp[z]), -1)] if v in mp else []))
                    if r:
                        R["CNF"].append(r)
        if n <= U.N - 1:
            Wp = [None, 0] + [par[v] + 1 for v in range(1, n)]
            for z in range(n):
                for vp in range(n + 1):
                    r = row((u(Wp, vp, z + 1), 1), *([(u(par, vp - 1, z), -1)] if vp >= 1 else []))
                    if r:
                        R["GP"].append(r)
        if U.N <= 7:
            for mask in range(1 << (n - 1)):
                S = {0} | {v for v in range(1, n) if mask >> (v - 1) & 1}
                if len(S) == n or any(par[v] not in S for v in S if v):
                    continue
                X, mp = sub(par, S)
                for z in S:
                    for v in range(n):
                        r = row((u(par, v, z), 1), *([(u(X, mp[v], mp[z]), -1)] if v in mp else []))
                        if r:
                            R["W2"].append(r)
    return R


def exact_rank(rows):
    piv = {}
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
    return len(piv)


SYSTEMS = {"PN": ["PN"], "PN+Z": ["PN", "Z"], "PN+CN_F": ["PN", "CNF"], "PN+G+": ["PN", "GP"], "PN+C_recv": ["PN", "CR"],
           "PN+C_climb": ["PN", "CC"], "PN+S": ["PN", "S"], "PN+S_leaf": ["PN", "SL"], "PN+S+C_climb": ["PN", "S", "CC"],
           "PN+S+C_recv": ["PN", "S", "CR"], "PN+S+G+": ["PN", "S", "GP"], "PN+W2_F": ["PN", "W2"],
           "PN+W2_F+C_recv": ["PN", "W2", "CR"]}


# ---------------- reads ----------------
def solve(A, b):
    n = len(A); M = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        p = next(r for r in range(i, n) if M[r][i] != 0); M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]; M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


A_T = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k), "alt": lambda k: Fr(1 if k % 2 else -2)}
M_T = {"one": lambda k: Fr(1), "inv": lambda k: 1 / Fr(k), "invalt": lambda k: 1 / Fr(1 if k % 2 else -2)}
FAMS = {"G1": ("unit", "one"), "G2": ("three", "one"), "G3": ("depth", "inv"), "G4": ("alt", "invalt"),
        "G5": ("depth", "one"), "G6": ("alt", "one")}
THETAS = [Fr(-1), Fr(-3), Fr(0), Fr(2)]


def field_read(par, x, a, m, th):
    n = len(par); d = depths(par); ch = kids(par); tot = sum(x, Fr(0))
    xo = list(x); xo[0] -= tot
    L = [[Fr(0)] * n for _ in range(n)]
    for v in range(1, n):
        w = 1 / a(d[v]); p = par[v]
        L[v][v] += w; L[p][p] += w; L[v][p] -= w; L[p][v] -= w
    phi = [Fr(0)] + (solve([[L[i][j] for j in range(1, n)] for i in range(1, n)], xo[1:]) if n > 1 else [])
    y = {v: phi[v] - phi[par[v]] for v in range(1, n)}
    f = []
    for v in range(n):
        s = sum((y[c] for c in ch[v]), Fr(0))
        f.append(m(1) * s + th * tot if v == 0 else -m(d[v]) * y[v] + m(d[v] + 1) * s)
    return f


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


def pn_count(reps, rd):
    good = 0; tot = 0
    for par in reps.values():
        n = len(par)
        for l in leaves(par):
            for z in range(n):
                x = delta(n, z); Y, y = Pv(par, l, x); _, Pf = Pv(par, l, rd(par, x)); tot += 1
                good += rd(Y, y) == Pf
    return good, tot


def z_count(reps, rd):
    c = 0
    for par in reps.values():
        n = len(par)
        for a in leaves(par):
            f = rd(par, delta(n, a)); c += all(f[v] == 0 for v in range(n) if v != a)
    return c


def universe(N, elim):
    U = Universe(N); reps = U.reps
    keys = sorted(reps)
    out = {"carriers": len(reps), "leaves": sum(len(leaves(p)) for p in reps.values()),
           "genesis_leaves": sum(1 for p in reps.values() for l in leaves(p) if p[l] == 0),
           "sum_n": sum(len(p) for p in reps.values()), "unknowns": len(U.idx),
           "universe_digest": hashlib.sha256("\n".join(keys).encode()).hexdigest()}
    out["digest"] = hashlib.sha256("\n".join(k + "|" + ",".join(map(str, sorted(depths(reps[k])))) for k in keys).encode()).hexdigest()
    R = build(U)
    out["row_counts"] = {k: len(v) for k, v in sorted(R.items()) if v}
    dims = {}
    for nm in elim:
        dims[nm] = len(U.idx) - exact_rank([r for s in SYSTEMS[nm] for r in R[s]])
    out["dims"] = dims
    if "PN+Z" in elim:
        # every PN+Z solution is kappa id on carriers with <= N-1 vertices: these rows are implied
        k0 = U.u([None], 0, 0); extra = []
        for p in reps.values():
            if len(p) <= N - 1:
                for v in range(len(p)):
                    for z in range(len(p)):
                        extra.append(row((U.u(p, v, z), 1), *([(k0, -1)] if v == z else [])))
        out["kappa_id_small"] = len(U.idx) - exact_rank(R["PN"] + R["Z"] + extra) == dims["PN+Z"]
        # R6: I + E(1,0) against PN+Z rows
        nu = {(k, k): Fr(1) for k in range(N)}; nu[(1, 0)] = Fr(1); vec = {}
        for k, p in reps.items():
            for z in range(len(p)):
                f = nu_read(p, nu, delta(len(p), z))
                for v in range(len(p)):
                    vec[U.idx[(k, v, z)]] = f[v]
        out["R6_holds"] = all(sum(vec[c] * x for c, x in r.items()) == 0 for r in R["PN"] + R["Z"])
    if N == 3:
        return out
    # field identity, PN and Z truth table
    ident = {}; pn = {}; zt = {}
    for g, (an, mn) in FAMS.items():
        a, m = A_T[an], M_T[mn]
        for th in THETAS:
            key = g + ":" + str(th)
            nu = {(0, 0): th}
            for k in range(1, N + 1):
                nu[(k, k)] = -m(k) * a(k)
            rd = lambda p, x, a=a, m=m, th=th: field_read(p, x, a, m, th)
            ident[key] = sum(rd(p, delta(len(p), z)) == nu_read(p, nu, delta(len(p), z)) for p in reps.values() for z in range(len(p)))
            pn[key] = pn_count(reps, rd)[0]; zt[key] = z_count(reps, rd)
    out["field_identity"] = ident; out["field_pn"] = pn; out["field_z"] = zt
    out["pn_cases"] = pn_count(reps, lambda p, x: list(x))[1]
    # witnesses
    gd = lambda p, x: [sum(x, Fr(0))] + [Fr(0)] * (len(p) - 1)
    f0 = lambda p, x: field_read(p, x, A_T["unit"], M_T["one"], Fr(0))
    nuo = {(k, k): Fr(1) for k in range(N)}; nuo[(2, 0)] = Fr(1); nuo[(2, 1)] = Fr(-1)
    wo = lambda p, x: nu_read(p, nuo, x)
    wit = {}
    for nm, rd in (("genesis_dump", gd), ("field_zero", f0), ("nu_off", wo)):
        wit[nm] = {"pn": pn_count(reps, rd)[0], "z_holds": z_count(reps, rd)}
    climb = 0; nonanc = 0; s_all = True
    for p in reps.values():
        n = len(p)
        for a_ in leaves(p):
            f = wo(p, delta(n, a_)); A_ = set(ancs(p, a_))
            climb += all(f[v] == 0 for v in A_)
            nonanc += any(f[v] != 0 for v in range(n) if v != a_ and v not in A_)
        for z in range(n):
            f = wo(p, delta(n, z)); s_all &= all(f[v] == 0 for v in range(n) if not le(p, v, z))
    wit["nu_off"].update({"climb_blind": climb, "nonancestor_leaves": nonanc, "S_everywhere": s_all})
    out["witnesses"] = wit
    # events
    ev = {"cases": 0, "pn": 0, "conserved": 0, "blind": 0, "contrast": 0}
    for kap in (Fr(1), Fr(-3), Fr(1, 2)):
        rd = lambda p, x, kap=kap: [kap * t for t in x]
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
    nuo = {(k, k): Fr(1) for k in range(4)}; nuo[(2, 0)] = Fr(1); nuo[(2, 1)] = Fr(-1)
    I["Z1"] = [str(t) for t in nu_read([None, 0, 1, 0], nuo, delta(4, 3))]
    I["Z3.dump"] = [str(t) for t in [Fr(1), Fr(0)]]
    I["Z3.field0"] = [str(t) for t in field_read([None, 0], delta(2, 1), A_T["unit"], M_T["one"], Fr(0))]
    x = [Fr(0), Fr(0)]; x2 = [Fr(0), Fr(1)]
    Y, y = Pv([None, 0], 1, x); _, y2 = Pv([None, 0], 1, x2)
    I["Z4.before"] = [str(x[0]), str(x2[0])]; I["Z4.after"] = str(y2[0] - y[0])
    I["Z5"] = [str(t) for t in field_read([None, 0, 1], delta(3, 2), A_T["depth"], M_T["one"], Fr(-1))]
    return I


def controls(u):
    out = {}
    U7, U8 = u["U7"], u["U8"]
    pred = {("G1", "-1"), ("G3", "-1"), ("G4", "-1"), ("G2", "-3")}
    flag = lambda b: "ACCEPTED_WRONGLY" if b else "REJECTED"
    out["R1_genesis_dump_leaf_blind"] = flag(max(U7["witnesses"]["genesis_dump"]["z_holds"], U8["witnesses"]["genesis_dump"]["z_holds"]) > 0)
    out["R2_zero_datum_field_leaf_blind"] = flag(max(U7["witnesses"]["field_zero"]["z_holds"], U8["witnesses"]["field_zero"]["z_holds"]) > 0)
    out["R3_nu_off_cone_local"] = flag(U7["witnesses"]["nu_off"]["S_everywhere"] or U8["witnesses"]["nu_off"]["S_everywhere"])
    out["R4_climb_alone_forces_identity"] = flag(1 in (U7["dims"]["PN+C_climb"], U8["dims"]["PN+C_climb"]))
    out["R5_apex_alone_forces_identity"] = flag(1 in (U7["dims"]["PN+G+"], U8["dims"]["PN+G+"]))
    out["R6_offdiagonal_passes_leaf_blindness"] = flag(any(x["R6_holds"] for x in u.values()))
    bad = False
    for X in (U7, U8):
        for key, val in X["field_z"].items():
            g, th = key.split(":")
            if (g, th) not in pred and val == X["leaves"]:
                bad = True
    out["R7_unpredicted_field_setting_leaf_blind"] = flag(bad)
    out["R8_event_violation"] = flag(any(X["event"][k] < X["event"]["cases"] for X in (U7, U8) for k in X["event"]))
    out["R9_PN_Z_not_identity_on_small"] = flag(not all(x["kappa_id_small"] for x in u.values()))
    return out


def main():
    ALL = list(SYSTEMS)
    unis = {"U3": universe(3, ["PN", "PN+Z", "PN+CN_F"]), "U7": universe(7, ALL), "U8": universe(8, ALL[:11])}
    inst = instances(); inst["Z2"] = unis["U3"]["dims"]
    cert = {"role": "producer", "result_sha256": RESULT_SHA, "universes": unis, "instances": inst, "controls": controls(unis), "violations": VIOL}
    Path_out = sys.argv[1]
    open(Path_out, "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({u: v["dims"] for u, v in unis.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
