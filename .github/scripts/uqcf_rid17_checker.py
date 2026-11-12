"""receiver_identification d17 freeze (section 23): CHECKER. Algorithmically independent of the producer (no import).
Trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; field by path sums of
a_depth * cone totals (subtree sums), verified against L phi = x by neighbour sums; blind reads in incident-edge
coordinates, dimension certified by a mod-p rank of the descendant rows (upper bound on the nullity) and the explicit
own-grade read checked against every row (lower bound); Genesis by full mod-p rank; dense control by exact
fraction-free (Bareiss) integer ranks."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d17_review")
TABLE_ORDER = ["unit", "three", "depth", "alt"]
TAB = {"unit": lambda k: 1, "three": lambda k: 3, "depth": lambda k: k, "alt": lambda k: 1 if k % 2 else -2}
GS = [Fr(1), Fr(-2), Fr(5, 3)]
PRIME = 2147483629
VIOL = []


def norm(t):
    return tuple(sorted(t, key=cstr))


def cstr(t):
    return "(" + "".join(sorted(cstr(c) for c in t)) + ")"


def grow(nmax):
    """all rooted trees with 1..nmax vertices as nested tuples, by leaf attachment."""
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
        self.sub = [None] * self.n
        for v in reversed(order):
            self.sub[v] = {v}.union(*[self.sub[u] for u in ch[v]]) if ch[v] else {v}
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


def cone_totals(T, x):
    return {v: sum((x[z] for z in T.sub[v]), Fr(0)) for v in range(1, T.n)}


def field(T, x, a):
    """grounded phi by path sums phi_v = sum over path edges of a_depth c_e of the Genesis-balanced part."""
    c = cone_totals(T, x); phi = [Fr(0)] * T.n; order = [0]
    for v in order:
        for u in T.ch[v]:
            phi[u] = phi[v] + a(T.dep[u]) * c[u]; order.append(u)
    xb = [x[0] - sum(x)] + list(x[1:])
    for v in range(1, T.n):  # neighbour-sum check of L phi = x on nonroot vertices
        lv = (phi[v] - phi[T.par[v]]) / a(T.dep[v]) - sum((phi[u] - phi[v]) / a(T.dep[u]) for u in T.ch[v])
        if lv != xb[v]:
            VIOL.append("laplacian")
    return phi


def rank_mod(rows):
    R = [[int(v) % PRIME for v in r] for r in rows]; rk = 0; m = len(R[0]) if R else 0
    for c in reversed(range(m)):
        p = next((i for i in range(rk, len(R)) if R[i][c]), None)
        if p is None:
            continue
        R[rk], R[p] = R[p], R[rk]; inv = pow(R[rk][c], PRIME - 2, PRIME)
        R[rk] = [v * inv % PRIME for v in R[rk]]
        for i in range(len(R)):
            if i != rk and R[i][c]:
                f = R[i][c]; R[i] = [(v - f * w) % PRIME for v, w in zip(R[i], R[rk])]
        rk += 1
    return rk


def rank_bareiss(rows):
    M = [list(map(int, r)) for r in rows if any(r)]
    if not M:
        return 0
    m = len(M[0]); rk = 0; prev = 1
    for c in range(m):
        p = next((i for i in range(rk, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(rk + 1, len(M)):
            M[i] = [(M[rk][c] * M[i][j] - M[i][c] * M[rk][j]) // prev for j in range(m)]
        prev = M[rk][c]; rk += 1
        if rk == len(M):
            break
    return rk


def incident(T, p):
    return ([p] if p != 0 else []) + list(T.ch[p])  # edges named by their child vertex


def edge_row(T, p, z, a):
    """incident edge values a_depth(e) c_e of the field of the unit grade at z (z != 0)."""
    return [a(T.dep[e]) * (1 if z in T.sub[e] else 0) for e in incident(T, p)]


def explicit(T, p, a):
    """own-grade read f = c_p - sum c_u in incident-edge coordinates."""
    return [Fr(1, a(T.dep[p]))] + [Fr(-1, a(T.dep[u])) for u in T.ch[p]]


def analyse(T, a):
    o = {"local": 0, "b1": 0, "g0": 0, "own": 0, "coef": 0, "summ": [], "R1": True, "R2": True, "R4": False, "R8": False}
    for p in range(T.n):
        deg = len(incident(T, p)); o["local"] += 1  # local reads <-> incident edge values (d_W is an isomorphism)
        desc = [z for z in T.sub[p] if z != p]
        rows = [edge_row(T, p, z, a) for z in desc]
        rk = rank_mod(rows) if rows else 0
        if p == 0:
            ok = rk == deg; o["g0"] += ok; o["R4"] |= not ok
            continue
        lam = explicit(T, p, a)
        sat = all(sum(l * r for l, r in zip(lam, row)) == 0 for row in rows)
        f = lambda z: sum(l * r for l, r in zip(lam, edge_row(T, p, z, a))) if z != 0 else 0
        dim1 = deg - rk == 1 and sat
        o["R8"] |= not dim1
        if not dim1:
            VIOL.append("dim"); continue
        o["b1"] += 1
        o["own"] += f(p) == 1 and all(f(z) == 0 for z in range(T.n) if z != p)
        k = T.dep[p]; coef_p = lam[0] - sum(lam[1:])
        o["coef"] += coef_p == Fr(1, a(k)) + Fr(len(T.ch[p]), a(k + 1))
        o["summ"].append("%s@%d:%s" % (T.cs[p], k, coef_p))
        if desc:
            o["R1"] &= all(pathval(T, z, p, a) == 0 for z in desc)
            if T.ch[p]:
                o["R2"] &= all(edge_row(T, p, z, a)[0] == 0 for z in desc)
    o["summ"].sort()
    return o


def pathval(T, z, p, a):
    """grounded phi_p of the unit grade at z: sum over the path edges e of a_depth [z in X_e]."""
    v = p; s = 0
    while v != 0:
        s += a(T.dep[v]) * (1 if z in T.sub[v] else 0); v = T.par[v]
    return s


def pruned(T, l):
    keep = [v for v in range(T.n) if v != l]; ren = {v: i for i, v in enumerate(keep)}
    ch = [[ren[u] for u in T.ch[v] if u != l] for v in keep]
    return Tree(ch), keep, ren


def edge_read(T, p, phi, a):
    lam = explicit(T, p, a)
    vals = [(phi[p] - phi[T.par[p]])] + [(phi[u] - phi[p]) for u in T.ch[p]]
    return sum(l * v for l, v in zip(lam, vals)) / 1


def events(T, ev):
    for l in range(1, T.n):
        if T.ch[l]:
            continue
        p = T.par[l]; T2, keep, ren = pruned(T, l)
        for t in TABLE_ORDER:
            a = TAB[t]
            for g in GS:
                base = [Fr((-1) ** v * (v + 2), 1 + v % 3) for v in range(T.n)]
                pre, post = [], []
                for xl in (Fr(0), g):
                    x = base[:]; x[l] = xl
                    ph = field(T, x, a)
                    x2 = [x[v] for v in keep]; x2[ren[p]] += x[l]
                    ph2 = field(T2, x2, a)
                    ev["cases"] += 1
                    same = all(ph2[ren[v]] == ph[v] for v in keep)
                    ev["field_identity"] += same; ev["R5"] |= not same
                    pre.append((ph, x)); post.append((ph2, x2))
                if p != 0:
                    rb = [edge_read(T, p, ph, a) for ph, _ in pre]
                    ra = [edge_read(T2, ren[p], ph, a) for ph, _ in post]
                    ev["R6"] |= rb[0] != rb[1]
                    ev["contrast_ok"] += (rb[0] == rb[1] and ra[1] - ra[0] == g and rb[0] == pre[0][1][p]
                                          and ra[0] == post[0][1][ren[p]] and ra[1] == post[1][1][ren[p]])
                else:
                    same = post[0][0] == post[1][0]; ev["R7"] |= not same
                    ev["genesis_coincide"] += same and pre[0][0] != pre[1][0]


def dense(T):
    S = lambda z: T.dep[z]  # sum of nonroot cone totals of the unit grade at z
    def row(p, z):
        if z == 0:
            return [0] * len(incident(T, p))
        return [2 * (1 if z in T.sub[e] else 0) + S(z) for e in incident(T, p)]
    out = []
    for p in range(1, T.n):
        if not T.ch[p]:
            continue
        deg = len(incident(T, p))
        desc = [row(p, z) for z in T.sub[p] if z != p]
        others = [row(p, z) for z in range(T.n) if z != p]
        dim = deg - rank_bareiss(desc)
        own = rank_bareiss(others + [row(p, p)]) > rank_bareiss(others)
        out.append((dim, own))
    return out


def universe(nmax):
    trees = sorted((Tree.from_tuple(t) for t in grow(nmax)), key=lambda T: T.cs[0])
    U = {"carriers": len(trees), "positions": 0, "positions_with_children": 0, "leaves": 0, "genesis_leaves": 0}
    tabs = {t: {"local_dim_deg": 0, "blind_dim1": 0, "genesis_dim0": 0, "own_grade_read": 0, "coefficients_match": 0}
            for t in TABLE_ORDER}
    ctl = {"R1": True, "R2": True, "R3": True, "R4": False, "R8": False}
    ev = {"cases": 0, "field_identity": 0, "contrast_ok": 0, "genesis_coincide": 0, "R5": False, "R6": False, "R7": False}
    dc = {}; lines = []
    for T in trees:
        U["positions"] += T.n - 1
        for v in range(1, T.n):
            if T.ch[v]:
                U["positions_with_children"] += 1
            else:
                U["leaves"] += 1; U["genesis_leaves"] += T.par[v] == 0
        parts = [T.cs[0]]
        for t in TABLE_ORDER:
            o = analyse(T, TAB[t])
            for k1, k2 in (("local_dim_deg", "local"), ("blind_dim1", "b1"), ("genesis_dim0", "g0"),
                           ("own_grade_read", "own"), ("coefficients_match", "coef")):
                tabs[t][k1] += o[k2]
            ctl["R1"] &= o["R1"]; ctl["R2"] &= o["R2"]; ctl["R4"] |= o["R4"]; ctl["R8"] |= o["R8"]
            parts.append(t + "=" + ",".join(o["summ"]))
        events(T, ev)
        if T.n >= 4:
            dd = dense(T)
            for dm, own in dd:
                key = "%d,%s" % (dm, "own" if own else "not_own"); dc[key] = dc.get(key, 0) + 1
                ctl["R3"] &= own
            parts.append("J=" + ",".join(sorted("%d%d" % (dm, int(own)) for dm, own in dd)))
        lines.append("|".join(parts))
    U["tables"] = tabs
    U["event"] = {k: ev[k] for k in ("cases", "field_identity", "contrast_ok", "genesis_coincide")}
    U["dense"] = {"positions": sum(dc.values()), "counts": dict(sorted(dc.items()))}
    U["digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(T.cs[0] for T in trees).encode()).hexdigest()
    ctl.update({k: ev[k] for k in ("R5", "R6", "R7")})
    return U, ctl


NAMES = {"R1": "R1_grounded_value_is_descendant_blind", "R2": "R2_parent_edge_read_is_descendant_blind",
         "R3": "R3_dense_J_gives_own_grade_everywhere", "R4": "R4_nonzero_blind_read_at_genesis",
         "R5": "R5_event_changes_retained_field", "R6": "R6_blind_read_preinformed",
         "R7": "R7_genesis_pair_fields_differ_after_event", "R8": "R8_nonroot_blind_dim_not_1"}


def vertex_coeffs(T, p, a):
    """explicit read converted to vertex coefficients, listed in increasing vertex label."""
    lam = explicit(T, p, a); co = {T.par[p]: -lam[0], p: lam[0] - sum(lam[1:])}
    for l, u in zip(lam[1:], T.ch[p]):
        co[u] = l
    return [str(co[v]) for v in sorted(co)]


def instances():
    Z = {}
    chain3 = Tree([[1], [2], []]); star = Tree([[1], [2, 3], [], []])
    Z["Z1.unit"] = vertex_coeffs(chain3, 1, TAB["unit"]); Z["Z1.depth"] = vertex_coeffs(chain3, 1, TAB["depth"])
    Z["Z2.star"] = vertex_coeffs(star, 1, TAB["unit"])
    for T, p in ((chain3, 1), (star, 1)):  # the explicit read must be the blind one: verify against rows
        for t in ("unit", "depth"):
            lam = explicit(T, p, TAB[t])
            if any(sum(l * r for l, r in zip(lam, edge_row(T, p, z, TAB[t]))) for z in T.sub[p] if z != p):
                VIOL.append("instance read not blind")
    c2 = Tree([[1], []])
    Z["Z3.genesis"] = [len(incident(c2, 0)), len(incident(c2, 0)) - rank_mod([edge_row(c2, 0, 1, TAB["unit"])])]
    def ev(T, l, g):
        T2, keep, ren = pruned(T, l); pre, post = [], []
        for xl in (Fr(0), g):
            x = [Fr(0)] * T.n; x[l] = xl
            pre.append(field(T, x, TAB["unit"]))
            x2 = [x[v] for v in keep]; x2[ren[T.par[l]]] += x[l]
            post.append(field(T2, x2, TAB["unit"]))
        return T2, ren, pre, post
    T2, ren, pre, post = ev(chain3, 2, Fr(1))
    rb = [edge_read(chain3, 1, ph, TAB["unit"]) for ph in pre]; ra = [edge_read(T2, ren[1], ph, TAB["unit"]) for ph in post]
    Z["Z4.event"] = [[str(v) for v in pre[0]], [str(v) for v in pre[1]], [str(v) for v in post[0]], [str(v) for v in post[1]],
                     str(rb[1] - rb[0]), str(ra[1] - ra[0])]
    T2, ren, pre, post = ev(c2, 1, Fr(1))
    Z["Z5.genesis_event"] = [[str(v) for v in pre[0]], [str(v) for v in pre[1]], [str(v) for v in post[0]], [str(v) for v in post[1]]]
    d = dense(Tree([[1, 4], [2, 3], [], [], []]))
    Z["Z6.dense"] = [d[0][0], d[0][1]]
    return Z


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "checker", "result_sha256": hashlib.sha256(res).hexdigest(), "universes": {}}
    claims = {k: False for k in NAMES}
    for name, nmax in (("U7", 7), ("U8", 8)):
        U, ctl = universe(nmax)
        cert["universes"][name] = U
        for k, v in ctl.items():
            claims[k] |= v
    cert["controls"] = {NAMES[k]: ("ACCEPTED_WRONGLY" if claims[k] else "REJECTED") for k in NAMES}
    cert["instances"] = instances()
    cert["violations"] = VIOL
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("controls", "instances", "violations")}, sort_keys=True))
    for u in cert["universes"].values():
        print(json.dumps({k: u[k] for k in u if k != "digest"}, sort_keys=True))


if __name__ == "__main__":
    main()
