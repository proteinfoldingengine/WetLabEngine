"""receiver_identification d16 freeze ([D16] + section 22): CHECKER, algorithmically independent of the producer.
Trees grown by attaching a leaf to every vertex of every smaller tree, canonicalized as nested sorted tuples and relabelled
by breadth-first order; prefix subtrees as closures under leaf deletion; cones from ancestor paths. Every condition row has
the form u - v = 0 or u = 0, so dimensions are computed by equivalence classes (union-find; dim = classes with no member
forced to 0), cross-checked by a sparse mod-p rank (different prime and pivot order) and by explicit rational solution
families verified against every row. Green response by subtree sums (no linear solve), verified by neighbour sums."""
import hashlib, json, random, sys
from fractions import Fraction as F

RESULT_SHA = "e1eaf4592be4f234c18eff86fbc831a194a87fc3955402ce39724d35ce98715d"
PRIME = 1000000007


def tup(t, v): return tuple(sorted((tup(t, c) for c in t[v]), key=ser))
def ser(c): return '(' + ''.join(sorted(ser(x) for x in c)) + ')'


def relabel(t, root):
    """BFS relabelling with children sorted by canonical string; returns (labelled tree dict, map old->new)"""
    order = [root]; i = 0
    while i < len(order):
        order += sorted(t[order[i]], key=lambda c: ser(tup(t, c))); i += 1
    m = {v: j for j, v in enumerate(order)}
    return {m[v]: sorted(m[c] for c in t[v]) for v in order}, m


def grow(nmax):
    level = {'()': {0: []}}; out = {}
    for n in range(2, nmax + 1):
        nxt = {}
        for t in level.values():
            for v in list(t):
                u = {a: list(b) for a, b in t.items()}; new = len(u); u[v].append(new); u[new] = []
                s = ser(tup(u, 0))
                if s not in nxt:
                    nxt[s] = relabel(u, 0)[0]
        level = nxt; out.update(nxt)
    return out


def par_of(t): return {c: v for v in t for c in t[v]}


def path(t, v):
    p = par_of(t); out = [v]
    while out[-1] != 0:
        out.append(p[out[-1]])
    return out


def sub(t, S, root):
    s = {v: [c for c in t[v] if c in S] for v in S}
    lab, m = relabel(s, root)
    return ser(tup(s, root)), m


def closures(t):
    seen = set(); stack = [frozenset(t)]; out = []
    while stack:
        S = stack.pop()
        for v in S:
            if v != 0 and not [c for c in t[v] if c in S]:
                S2 = S - {v}
                if len(S2) >= 2 and S2 not in seen:
                    seen.add(S2); stack.append(S2); out.append(S2)
    return out


def automorphisms(t):
    """all rooted automorphisms by recursive matching of isomorphic children"""
    def iso(a, b):  # list of maps from subtree a onto subtree b (same tree)
        if ser(tup(t, a)) != ser(tup(t, b)):
            return []
        ca, cb = t[a], t[b]
        res = [{a: b}]
        def assign(i, used, cur):
            if i == len(ca):
                yield cur; return
            for j, y in enumerate(cb):
                if j in used: continue
                for m in iso(ca[i], y):
                    d = dict(cur); d.update(m); yield from assign(i + 1, used | {j}, d)
        return list(assign(0, frozenset(), {a: b}))
    return iso(0, 0)


class UF:
    def __init__(s): s.p = {}; s.zero = set()
    def f(s, a):
        s.p.setdefault(a, a)
        while s.p[a] != a:
            s.p[a] = s.p[s.p[a]]; a = s.p[a]
        return a
    def eq(s, a, b):
        ra, rb = s.f(a), s.f(b)
        if ra != rb:
            s.p[ra] = rb
            if ra in s.zero: s.zero.add(rb)
    def z(s, a): s.zero.add(s.f(a))


def dim_uf(vars_, rows):
    u = UF()
    for v in vars_: u.f(v)
    for r in rows:
        if len(r) == 1: u.z(r[0])
        else: u.eq(r[0], r[1])
    zero = {u.f(z) for z in u.zero}
    return len({u.f(v) for v in vars_} - zero)


def rank_modp(rows, order):
    piv = {}
    for r0 in rows:
        r = {order[r0[0]]: 1}
        if len(r0) == 2:
            k = order[r0[1]]; r[k] = (r.get(k, 0) - 1) % PRIME
            if r[k] == 0: del r[k]
        while r:
            k = max(r)
            if k in piv:
                c = r[k]
                for kk, vv in piv[k].items():
                    r[kk] = (r.get(kk, 0) - c * vv) % PRIME
                    if r[kk] == 0: del r[kk]
            else:
                inv = pow(r[k], PRIME - 2, PRIME); piv[k] = {kk: vv * inv % PRIME for kk, vv in r.items()}; break
    return len(piv)


def depth(t, v): return len(path(t, v)) - 1
def cone(t, a): return [v for v in t if a in path(t, v)]


def green(t, k, a=lambda d: 1):
    phi = {0: F(0)}
    for v in sorted(t, key=lambda v: depth(t, v)):
        for c in t[v]:
            phi[c] = phi[v] + a(depth(t, c)) * sum((F(k[u]) for u in cone(t, c)), F(0))
    return phi


def lap(t, phi):
    p = par_of(t); k = {v: F(0) for v in t}
    for v in t:
        nb = list(t[v]) + ([p[v]] if v else [])
        k[v] = sum((phi[v] - phi[u] for u in nb), F(0))
    return k


def main():
    rnd = random.Random(777)
    cert = {"role": "checker", "result_sha256": RESULT_SHA, "universes": {}, "violations": []}
    ctl = {}
    for name, nmax in (("U7", 7), ("U8", 8)):
        U = grow(nmax); keys = sorted(U); K = nmax - 1
        vars_ = [(s, e, f) for s in keys for e in U[s] if e for f in U[s] if f]
        order = {v: i for i, v in enumerate(vars_)}
        rC, rR = [], []
        def add(rows, a, b=None):
            if b is None: rows.append((a,))
            elif a != b: rows.append((a, b))
        ncones = 0
        for s in keys:
            t = U[s]; E = [v for v in t if v]
            for m in automorphisms(t):
                if any(m[v] != v for v in t):
                    for e in E:
                        for f in E: add(rC, (s, m[e], m[f]), (s, e, f))
            for S in closures(t):
                sy, m = sub(t, S, 0)
                for e in E:
                    for f in E:
                        if e in S and f in S: add(rC, (s, e, f), (sy, m[e], m[f]))
                        elif (e in S) != (f in S): add(rC, (s, e, f))
            for a in E:
                S = set(cone(t, a))
                if len(S) < 2: continue
                ncones += 1
                sa, m = sub(t, S, a)
                for f in S - {a}:
                    for e in E:
                        if e in S and e != a: add(rR, (s, e, f), (sa, m[e], m[f]))
                        else: add(rR, (s, e, f))
        dC, dCR = dim_uf(vars_, rC), dim_uf(vars_, rC + rR)
        mpC, mpCR = len(vars_) - rank_modp(rC, order), len(vars_) - rank_modp(rC + rR, order)
        def sol(a): return {(s, e, f): (F(a(depth(U[s], e))) if e == f else F(0)) for (s, e, f) in vars_}
        def ok(rows, v): return all((v[r[0]] == 0) if len(r) == 1 else (v[r[0]] == v[r[1]]) for r in rows)
        ind = [sol(lambda d, k=k: 1 if d == k else 0) for k in range(1, K + 1)]
        sols = {"depth_indicators_solve_C": all(ok(rC, v) for v in ind), "unit_solves_C_RS": ok(rC + rR, sol(lambda d: 1)),
                "depth_solves_C": ok(rC, sol(lambda d: d)), "depth_violates_RS": not ok(rR, sol(lambda d: d))}
        lower_C = K if sols["depth_indicators_solve_C"] else 0  # indicators have disjoint supports: independent
        viol = dC != mpC or dCR != mpCR or lower_C != dC or not (sols["unit_solves_C_RS"] and dCR >= 1)
        tables = [{d: F(rnd.choice(range(-3, 4))) for d in range(1, K + 1)} for _ in range(100)]
        tables += [{d: F(1) for d in range(1, K + 1)}, {d: F(-2) for d in range(1, K + 1)}]
        mism = 0; nonconst_acc = False
        for tb in tables:
            r = ok(rR, sol(lambda d: tb[d])); const = len(set(tb.values())) == 1
            mism += r != const; nonconst_acc |= r and not const
        gv = 0; gc = 0; lapok = True; depth_fail = False
        for s in keys:
            t = U[s]
            k = {v: F(rnd.choice(range(-5, 6))) for v in t}; k[0] -= sum(k.values())
            lapok &= lap(t, green(t, k)) == k
            for a in t:
                if a == 0: continue
                S = cone(t, a)
                if len(S) < 2: continue
                gc += 1
                sc = {v: [c for c in t[v] if c in S] for v in S}
                ks = {v: F(rnd.choice(range(-5, 6))) for v in S}; tot = sum(ks.values()); ks[a] -= tot
                kx = {v: ks.get(v, F(0)) for v in t}
                px = green(t, kx); pc = green(relabel(sc, a)[0], {relabel(sc, a)[1][v]: ks[v] for v in S})
                m = relabel(sc, a)[1]; tc = relabel(sc, a)[0]; pt = par_of(tc); P = par_of(t)
                dx = green(t, kx, lambda d: d); dc = green(tc, {m[v]: ks[v] for v in S}, lambda d: d)
                for v in t:
                    if v == 0: continue
                    inc = v in S and v != a
                    want = (pc[m[v]] - pc[pt[m[v]]]) if inc else 0
                    gv += (px[v] - px[P[v]]) != want
                    wd = (dc[m[v]] - dc[pt[m[v]]]) if inc else 0
                    depth_fail |= (dx[v] - dx[P[v]]) != wd
        # Proposition 22.4
        seen = set(); pv = 0; dump_keeps = True
        for s in keys:
            t = U[s]; P = par_of(t)
            for l in t:
                if l == 0 or t[l]: continue
                # marked class key: canonical string of the tree with l marked
                def mk(v): return '(' + ('*' if v == l else '') + ''.join(sorted(mk(c) for c in t[v])) + ')'
                key = mk(0)
                if key in seen: continue
                seen.add(key)
                def C(x, alive):
                    c = {v: F(0) for v in t if alive(v)}
                    for u in t:
                        if alive(u):
                            for v in path(t, u): c[v] += x[u]
                    return c  # c[0] is the total
                al = lambda v: True; al2 = lambda v: v != l
                x = {v: F(rnd.choice([-2, -1, 0, 1, 3])) for v in t}; x[l] = F(rnd.choice([-3, 1, 4]))
                y = dict(x); y[P[l]] += x[l]; y[l] = F(0)
                cx, cy = C(x, al), C(y, al2)
                pv += any(cx[v] != cy[v] for v in cy)
                p = P[l]
                pv += x[p] != cx[p] - sum(cx[c] for c in t[p])
                pv += y[p] != cy[p] - sum(cy[c] for c in t[p] if c != l)
                pv += y[p] - x[p] != x[l]
                g = F(rnd.choice([-1, 2, 7]))
                x2 = dict(x); x2[l] += g; y2 = dict(x2); y2[p] += x2[l]; y2[l] = F(0)
                c2, d2 = C(x2, al), C(y2, al2)
                anc = set(path(t, l)[1:])
                pv += {v for v in cx if cx[v] != c2[v]} != (anc | {l})
                pv += {v for v in cy if cy[v] != d2[v]} != anc
                pv += x2[p] != x[p]; pv += y2[p] - y[p] != g
                if depth(t, l) >= 2:
                    yd = dict(x); yd[0] += x[l]; yd[l] = F(0); cd = C(yd, al2)
                    dump_keeps &= all(cd[v] == cx[v] for v in cd if v)
        if viol or mism or gv or not lapok or pv or not all(sols.values()):
            cert["violations"].append(name)
        cert["universes"][name] = {"carriers": len(keys), "unknowns": len(vars_), "cones": ncones, "leaf_classes": len(seen),
                                   "dims": {"C": dC, "C+RS": dCR}, "solutions": sols,
                                   "random_tables": {"tables": len(tables), "mismatches": mism},
                                   "green": {"cones": gc, "violations": gv, "laplacian_exact": lapok},
                                   "prop224": {"classes": len(seen), "violations": pv},
                                   "digest": hashlib.sha256("\n".join(keys).encode()).hexdigest()}
        for c_, v_ in (("R1", not sols["depth_violates_RS"]), ("R2", nonconst_acc), ("R3", dC == 1), ("R7", not depth_fail), ("R8", dump_keeps)):
            ctl.setdefault(c_, []).append(v_)
    # weight grid on chains, written on vertex lists
    vals = [F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(3, 2)]
    G = dict(vectors=0, E2=0, E5plus=0, E2_E5plus=0, R=0, CN=0, deletion=0, E2_E5plus_nonneg=0, E2_E5plus_notR=0,
             mismatch_R_deletion=0, mismatch_CN_R=0, mismatch_CN_implies_E5plus=0)
    dump_del = False; forces = True
    def vecs(K, pre=()):
        if len(pre) == K: yield pre; return
        for v in vals: yield from vecs(K, pre + (v,))
    for K in range(1, 5):
        t = {i: [i + 1] for i in range(K)}; t[K] = []; l = K
        anc = path(t, l)[1:]  # p, ..., 0 at distances 1..K
        for w in vecs(K):
            G["vectors"] += 1
            def T(x):
                y = {v: x[v] for v in t if v != l}
                for d, a in enumerate(anc, 1): y[a] += w[d - 1] * x[l]
                return y
            el = {v: F(1 if v == l else 0) for v in t}; y = T(el)
            e2 = sum(y.values()) == 1; e5 = y[anc[0]] == 1
            Rr = all(sum(y[u] for u in cone(t, a) if u != l) == 1 for a in anc)
            cn = all(y[v] == (1 if v == anc[0] else 0) for v in y)
            dele = True
            for _ in range(3):
                x = {v: F(rnd.choice(range(-4, 5))) for v in t}; x[l] = F(rnd.choice([-1, 3]))
                yx = T(x)
                dele &= all(sum(yx[u] for u in cone(t, a) if u != l) == sum(x[u] for u in cone(t, a)) for a in anc)
            G["E2"] += e2; G["E5plus"] += e5; G["E2_E5plus"] += e2 and e5; G["R"] += Rr; G["CN"] += cn; G["deletion"] += dele
            G["E2_E5plus_nonneg"] += e2 and e5 and min(w) >= 0; G["E2_E5plus_notR"] += e2 and e5 and not Rr
            G["mismatch_R_deletion"] += Rr != dele; G["mismatch_CN_R"] += cn != Rr; G["mismatch_CN_implies_E5plus"] += cn and not e5
            forces &= not (e2 and e5) or cn
            if K >= 2 and w[-1] == 1 and not any(w[:-1]) and dele: dump_del = True
    cert["grid"] = G
    inst = {}
    pa = green({0: [1], 1: []}, {0: F(-1), 1: F(1)}); pb = green({0: [1], 1: [2], 2: []}, {0: F(0), 1: F(-1), 2: F(1)}, lambda d: d)
    inst["Z1.depth_witness"] = [str(pa[1] - pa[0]), str(pb[2] - pb[1])]
    t2 = {0: [1, 4], 1: [2, 3], 2: [], 3: [], 4: []}; P2 = par_of(t2)
    g2 = green(t2, {0: F(0), 1: F(-2), 2: F(1), 3: F(1), 4: F(0)})
    tc = {0: [1, 2], 1: [], 2: []}; gq = green(tc, {0: F(-2), 1: F(1), 2: F(1)})
    inst["Z2.green_cone"] = [[str(g2[v] - g2[P2[v]]) for v in (1, 2, 3, 4)], [str(gq[1] - gq[0]), str(gq[2] - gq[0])]]
    t3 = {0: [1], 1: [2], 2: [3], 3: []}
    y3 = {0: F(-1), 1: F(1), 2: F(1)}
    E2 = sum(y3.values()) == 1; E5 = y3[2] == 1
    Rz = all(sum(y3[u] for u in cone(t3, a) if u != 3) == 1 for a in (2, 1, 0))
    CNz = y3 == {0: 0, 1: 0, 2: 1}
    inst["Z3.signed_step"] = [[E2, E5, Rz, CNz, Rz], str(y3[1] + y3[2])]
    t4 = {0: [1], 1: [2, 3], 2: [], 3: []}
    def coords(x, drop):
        out = {"total": sum(x[v] for v in t4 if v != drop)}
        for a in (1, 2, 3):
            if a != drop: out["c%d" % a] = sum(x[v] for v in cone(t4, a) if v != drop)
        return out
    xa = {v: F(0) for v in t4}; xb = dict(xa); xb[3] = F(1)
    ya, yb = dict(xa), dict(xb); yb[1] += 1; yb[3] = F(0)
    A, B, Ca, Cb = coords(xa, None), coords(xb, None), coords(ya, 3), coords(yb, 3)
    inst["Z4.pair"] = [sorted(k for k in A if A[k] != B[k]), sorted(k for k in Ca if Ca[k] != Cb[k]), str(xb[1] - xa[1]), str(yb[1] - ya[1])]
    t5 = {0: [1], 1: [2], 2: []}; x5 = {0: F(0), 1: F(0), 2: F(1)}; y5 = {0: x5[0] + x5[2], 1: x5[1]}
    inst["Z5.dump"] = str(sum(y5[v] for v in cone(t5, 1) if v != 2) - sum(x5[v] for v in cone(t5, 1)))
    cert["instances"] = inst
    rj = lambda bad: "REJECTED" if not bad else "ACCEPTED_WRONGLY"
    cert["controls"] = {"R1_T_depth_satisfies_RS": rj(any(ctl["R1"])), "R2_nonconstant_table_satisfies_RS": rj(any(ctl["R2"])),
                        "R3_C_alone_forces_dim_1": rj(any(ctl["R3"])), "R4_genesis_dump_is_coordinate_deletion": rj(dump_del),
                        "R5_signed_step_satisfies_R": rj(Rz), "R6_signed_step_satisfies_CN": rj(CNz),
                        "R7_depth_response_passes_green_cone_locality": rj(any(ctl["R7"])),
                        "R8_genesis_dump_keeps_retained_cone_totals": rj(any(ctl["R8"])),
                        "R9_E2_E5plus_forces_P1_without_positivity": rj(forces)}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({u: {k: v for k, v in d.items() if k != "digest"} for u, d in cert["universes"].items()}, sort_keys=True))
    print(json.dumps(cert["instances"]), cert["violations"], json.dumps(cert["grid"], sort_keys=True))


if __name__ == "__main__":
    main()
