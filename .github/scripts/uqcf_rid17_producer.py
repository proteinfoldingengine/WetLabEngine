"""receiver_identification d17 freeze (section 23, field-to-state association): PRODUCER.
Pure-Python exact Fractions. Parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the grounded
weighted Laplacian (no cone-total formula); descendant-blind local reads as the exact nullspace over Q, in vertex
coordinates on N[p], of the constant row and the field responses of every strict descendant."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d17_review")
TABLES = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k),
          "alt": lambda k: Fr(1) if k % 2 == 1 else Fr(-2)}
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


def anc(par, z):
    s = []
    while par[z] is not None:
        z = par[z]; s.append(z)
    return s


def solve(A, b):
    n = len(A); M = [row[:] + [bb] for row, bb in zip(A, b)]
    for i in range(n):
        piv = next(r for r in range(i, n) if M[r][i] != 0); M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]; M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def nullspace(rows, m):
    R = [r[:] for r in rows]; piv = []; ri = 0
    for c in range(m):
        p = next((r for r in range(ri, len(R)) if R[r][c] != 0), None)
        if p is None:
            continue
        R[ri], R[p] = R[p], R[ri]; R[ri] = [x / R[ri][c] for x in R[ri]]
        for r in range(len(R)):
            if r != ri and R[r][c] != 0:
                f = R[r][c]; R[r] = [x - f * y for x, y in zip(R[r], R[ri])]
        piv.append(c); ri += 1
    basis = []
    for fc in [c for c in range(m) if c not in piv]:
        v = [Fr(0)] * m; v[fc] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][fc]
        basis.append(v)
    return basis


def field(par, x, a):
    """grounded potential: weighted Laplacian, conductance 1/a_depth, on the Genesis-balanced part of x."""
    n = len(par)
    if n == 1:
        return [Fr(0)]
    w = {v: 1 / a(depth(par, v)) for v in range(1, n)}
    L = [[Fr(0)] * n for _ in range(n)]
    for v in range(1, n):
        p = par[v]; L[v][v] += w[v]; L[p][p] += w[v]; L[v][p] -= w[v]; L[p][v] -= w[v]
    idx = list(range(1, n))
    return [Fr(0)] + solve([[L[i][j] for j in idx] for i in idx], [x[i] for i in idx])


def unit(n, z):
    return [Fr(int(i == z)) for i in range(n)]


def blind(par, p, G):
    n = len(par); ch = [v for v in range(n) if par[v] == p]
    N = ([par[p]] if p != 0 else []) + [p] + ch
    desc = [z for z in range(n) if z != p and p in anc(par, z)]
    rows = [[Fr(1)] * len(N)] + [[G[z][q] for q in N] for z in desc]
    return N, ch, nullspace([[Fr(1)] * len(N)], len(N)), nullspace(rows, len(N))


def analyse(par, a):
    n = len(par); s, _ = canon_of(par)
    G = [field(par, unit(n, z) if z != 0 else [Fr(0)] * n, a) for z in range(n)]
    out = {"local_ok": 0, "blind1": 0, "gen0": 0, "own": 0, "coef": 0, "summ": [], "R1": True, "R2": True, "R8": False,
           "R4": False}
    for p in range(n):
        N, ch, loc, B = blind(par, p, G)
        deg = len(N) - 1
        out["local_ok"] += len(loc) == deg
        if p == 0:
            out["gen0"] += len(B) == 0; out["R4"] |= len(B) > 0
            continue
        out["R8"] |= len(B) != 1
        if len(B) != 1:
            VIOL.append("blind dim"); continue
        out["blind1"] += 1
        k = B[0]; f = lambda z: sum(k[i] * G[z][q] for i, q in enumerate(N))
        sc = f(p); k = [c / sc for c in k]
        if all(f(z) == 0 for z in range(n) if z != p):
            out["own"] += 1
        d = depth(par, p); ak, ak1 = a(d), a(d + 1)
        exp = [-1 / ak, 1 / ak + len(ch) / ak1] + [-1 / ak1] * len(ch)
        out["coef"] += k == exp
        out["summ"].append("%s@%d:%s" % (s(p), d, k[1]))
        desc = [z for z in range(n) if z != p and p in anc(par, z)]
        if desc:
            out["R1"] &= all(G[z][p] == 0 for z in desc)
            if ch:
                out["R2"] &= all(G[z][p] - G[z][par[p]] == 0 for z in desc)
    out["summ"].sort()
    return out


def prune(par, l):
    keep = [v for v in range(len(par)) if v != l]; ren = {v: i for i, v in enumerate(keep)}
    return [None if par[v] is None else ren[par[v]] for v in keep], keep, ren


def balanced(x):
    return [x[0] - sum(x)] + x[1:]


def read(par, p, phi, a):
    ch = [v for v in range(len(par)) if par[v] == p]; k = depth(par, p)
    return (phi[p] - phi[par[p]]) / a(k) - sum((phi[u] - phi[p]) / a(k + 1) for u in ch)


def events(par, ev):
    n = len(par)
    for l in range(1, n):
        if any(par[v] == l for v in range(n)):
            continue
        p = par[l]; par2, keep, ren = prune(par, l)
        for a in TABLES.values():
            for g in GS:
                base = [Fr((-1) ** v * (v + 2), 1 + v % 3) for v in range(n)]; base[l] = Fr(0)
                pre, post = [], []
                for xl in (Fr(0), g):
                    x = base[:]; x[l] = xl
                    ph = field(par, balanced(x), a)
                    x2 = [x[v] for v in keep]; x2[ren[p]] += x[l]
                    ph2 = field(par2, balanced(x2), a)
                    ev["cases"] += 1
                    if all(ph2[ren[v]] == ph[v] for v in keep):
                        ev["field_identity"] += 1
                    else:
                        ev["R5"] = True
                    pre.append((ph, x)); post.append((ph2, x2))
                if p != 0:
                    rb = [read(par, p, ph, a) for ph, _ in pre]
                    ra = [read(par2, ren[p], ph, a) for ph, _ in post]
                    ev["R6"] |= rb[0] != rb[1]
                    if rb[0] == rb[1] and ra[1] - ra[0] == g and all(rb[i] == pre[i][1][p] for i in range(2)) \
                            and all(ra[i] == post[i][1][ren[p]] for i in range(2)):
                        ev["contrast_ok"] += 1
                else:
                    same = post[0][0] == post[1][0]
                    ev["R7"] |= not same
                    ev["genesis_coincide"] += same and pre[0][0] != pre[1][0]


def dense(par):
    """M = 2I + J on nonroot edges; grounded potential by path sums of (Mc)_e."""
    n = len(par)
    cone = lambda x, v: sum(x[z] for z in range(n) if z == v or v in anc(par, z))
    G = []
    for z in range(n):
        x = unit(n, z) if z != 0 else [Fr(0)] * n
        c = {e: cone(x, e) for e in range(1, n)}; S = sum(c.values())
        Mc = {e: 2 * c[e] + S for e in range(1, n)}
        G.append([Fr(0)] + [sum(Mc[e] for e in [v] + [u for u in anc(par, v) if u != 0]) for v in range(1, n)])
    res = []
    for p in range(1, n):
        N, ch, _, B = blind(par, p, G)
        if not ch:
            continue
        rows = [[Fr(1)] * len(N)] + [[G[z][q] for q in N] for z in range(n) if z != p]
        own = any(sum(k[i] * G[p][q] for i, q in enumerate(N)) != 0 for k in nullspace(rows, len(N)))
        res.append((len(B), own))
    return res


def instances():
    Z = {}
    for nm, par, p, a in (("Z1.unit", [None, 0, 1], 1, "unit"), ("Z1.depth", [None, 0, 1], 1, "depth"),
                          ("Z2.star", [None, 0, 1, 1], 1, "unit")):
        n = len(par); A = TABLES[a]
        G = [field(par, unit(n, z) if z != 0 else [Fr(0)] * n, A) for z in range(n)]
        N, ch, _, B = blind(par, p, G)
        k = B[0]; sc = sum(k[i] * G[p][q] for i, q in enumerate(N)); k = [c / sc for c in k]
        order = sorted(range(len(N)), key=lambda i: N[i])
        Z[nm] = [str(k[i]) for i in order]
    G = [field([None, 0], unit(2, z) if z else [Fr(0)] * 2, TABLES["unit"]) for z in range(2)]
    N, ch, loc, B = blind([None, 0], 0, G)
    Z["Z3.genesis"] = [len(loc), len(B)]
    def ev(par, l, g):
        n = len(par); par2, keep, ren = prune(par, l); pre, post = [], []
        for xl in (Fr(0), g):
            x = [Fr(0)] * n; x[l] = xl
            pre.append(field(par, balanced(x), TABLES["unit"]))
            x2 = [x[v] for v in keep]; x2[ren[par[l]]] += x[l]
            post.append(field(par2, balanced(x2), TABLES["unit"]))
        return par2, ren, pre, post
    par2, ren, pre, post = ev([None, 0, 1], 2, Fr(1))
    rb = [read([None, 0, 1], 1, ph, TABLES["unit"]) for ph in pre]
    ra = [read(par2, ren[1], ph, TABLES["unit"]) for ph in post]
    Z["Z4.event"] = [[str(v) for v in pre[0]], [str(v) for v in pre[1]], [str(v) for v in post[0]], [str(v) for v in post[1]],
                     str(rb[1] - rb[0]), str(ra[1] - ra[0])]
    par2, ren, pre, post = ev([None, 0], 1, Fr(1))
    Z["Z5.genesis_event"] = [[str(v) for v in pre[0]], [str(v) for v in pre[1]], [str(v) for v in post[0]], [str(v) for v in post[1]]]
    par = [None, 0, 1, 1, 0]
    d = dense(par)  # positions with children in order p = 1..; only p = 1 has children
    Z["Z6.dense"] = [d[0][0], d[0][1]]
    return Z


def universe(nmax):
    T = trees(nmax)
    U = {"carriers": len(T), "positions": 0, "positions_with_children": 0, "leaves": 0, "genesis_leaves": 0,
         "tables": {}, "event": {}, "dense": {}}
    ctl = {"R1": True, "R2": True, "R3": True, "R4": False, "R8": False}
    tabs = {t: {"local_dim_deg": 0, "blind_dim1": 0, "genesis_dim0": 0, "own_grade_read": 0, "coefficients_match": 0}
            for t in TABLES}
    ev = {"cases": 0, "field_identity": 0, "contrast_ok": 0, "genesis_coincide": 0, "R5": False, "R6": False, "R7": False}
    dcounts = {}; lines = []
    for cs in sorted(T):
        par = T[cs]; n = len(par)
        U["positions"] += n - 1
        for v in range(1, n):
            if any(par[w] == v for w in range(n)):
                U["positions_with_children"] += 1
            else:
                U["leaves"] += 1; U["genesis_leaves"] += par[v] == 0
        parts = [cs]
        for t, a in TABLES.items():
            o = analyse(par, a)
            for k1, k2 in (("local_dim_deg", "local_ok"), ("blind_dim1", "blind1"), ("genesis_dim0", "gen0"),
                           ("own_grade_read", "own"), ("coefficients_match", "coef")):
                tabs[t][k1] += o[k2]
            ctl["R1"] &= o["R1"]; ctl["R2"] &= o["R2"]; ctl["R4"] |= o["R4"]; ctl["R8"] |= o["R8"]
            parts.append(t + "=" + ",".join(o["summ"]))
        events(par, ev)
        if n >= 4:
            dd = dense(par)
            for dm, own in dd:
                key = "%d,%s" % (dm, "own" if own else "not_own"); dcounts[key] = dcounts.get(key, 0) + 1
                ctl["R3"] &= own
            parts.append("J=" + ",".join(sorted("%d%s" % (dm, int(own)) for dm, own in dd)))
        lines.append("|".join(parts))
    U["tables"] = tabs
    U["event"] = {k: ev[k] for k in ("cases", "field_identity", "contrast_ok", "genesis_coincide")}
    U["dense"] = {"positions": sum(dcounts.values()), "counts": dict(sorted(dcounts.items()))}
    U["digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(sorted(T)).encode()).hexdigest()
    ctl.update({"R5": ev["R5"], "R6": ev["R6"], "R7": ev["R7"]})
    return U, ctl


CTL_NAMES = {"R1": ("R1_grounded_value_is_descendant_blind", True), "R2": ("R2_parent_edge_read_is_descendant_blind", True),
             "R3": ("R3_dense_J_gives_own_grade_everywhere", True), "R4": ("R4_nonzero_blind_read_at_genesis", True),
             "R5": ("R5_event_changes_retained_field", True), "R6": ("R6_blind_read_preinformed", True),
             "R7": ("R7_genesis_pair_fields_differ_after_event", True), "R8": ("R8_nonroot_blind_dim_not_1", True)}


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "producer", "result_sha256": hashlib.sha256(res).hexdigest(), "universes": {}, "controls": {}}
    claims = {k: False for k in CTL_NAMES}
    for name, nmax in (("U7", 7), ("U8", 8)):
        U, ctl = universe(nmax)
        cert["universes"][name] = U
        for k, v in ctl.items():
            claims[k] |= v
    cert["controls"] = {CTL_NAMES[k][0]: ("ACCEPTED_WRONGLY" if claims[k] else "REJECTED") for k in CTL_NAMES}
    cert["instances"] = instances()
    cert["violations"] = VIOL
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("controls", "instances", "violations")}, indent=1, sort_keys=True))
    for u in cert["universes"].values():
        print(json.dumps({k: u[k] for k in u if k != "digest"}, sort_keys=True))


if __name__ == "__main__":
    main()
