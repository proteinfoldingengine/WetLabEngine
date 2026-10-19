"""receiver_identification d16 freeze ([D16] + section 22): PRODUCER. Pure-Python exact Fractions. Enumerates rooted
trees as parent arrays up to rooted isomorphism (AHU codes), prefix subtrees by vertex masks, cones by BFS, and eliminates
v16.22's comparison condition C and the root-shift square RS on unknown full edge-coordinate matrices exactly (sparse
Gauss-Jordan over Q). Green response by exact solve of the root-reduced Laplacian. Writes a JSON certificate."""
import hashlib, itertools, json, random, sys
from fractions import Fraction as F

RESULT_SHA = "e1eaf4592be4f234c18eff86fbc831a194a87fc3955402ce39724d35ce98715d"


def children(p, v): return [i for i in range(len(p)) if p[i] == v]
def code(p, v): return '(' + ''.join(sorted(code(p, c) for c in children(p, v))) + ')'


def depth(p, v):
    d = 0
    while p[v] is not None:
        v = p[v]; d += 1
    return d


def canonical(p):
    """relabel p in canonical preorder (children sorted by code); returns (code, canonical parent tuple, map old->new)"""
    order = []
    def walk(v):
        order.append(v)
        for c in sorted(children(p, v), key=lambda c: code(p, c)):
            walk(c)
    root = [v for v in range(len(p)) if p[v] is None][0]
    walk(root)
    new = {v: i for i, v in enumerate(order)}
    q = tuple(None if p[v] is None else new[p[v]] for v in order)
    return code(p, root), q, new


def sub(p, S, root):
    S = sorted(S); idx = {v: j for j, v in enumerate(S)}
    q = tuple(None if v == root else idx[p[v]] for v in S)
    c, qc, new = canonical(q)
    return c, {v: new[idx[v]] for v in S}


def universe(nmax):
    U = {}
    for n in range(2, nmax + 1):
        for par in itertools.product(*[range(i) for i in range(1, n)]):
            p = (None,) + par
            c, q, _ = canonical(p)
            if c not in U:
                U[c] = q
    return U


def cone(p, a):
    nodes = [a]; i = 0
    while i < len(nodes):
        nodes += children(p, nodes[i]); i += 1
    return nodes


def rank_Q(rows):
    piv = {}
    for r in rows:
        r = dict(r)
        while r:
            k = min(r)
            if k in piv:
                c = r[k]
                for kk, vv in piv[k].items():
                    x = r.get(kk, 0) - c * vv
                    if x:
                        r[kk] = x
                    else:
                        r.pop(kk, None)
            else:
                inv = 1 / F(r[k]); piv[k] = {kk: vv * inv for kk, vv in r.items()}; break
    return len(piv)


def build(nmax):
    U = universe(nmax); keys = sorted(U)
    vid = {}
    for c in keys:
        n = len(U[c])
        for e in range(1, n):
            for f in range(1, n):
                vid[(c, e, f)] = len(vid)
    rowsC, rowsR = [], []
    def eq(a, b=None):
        if b is None:
            return {a: F(1)}
        return None if a == b else {a: F(1), b: F(-1)}
    ncones = 0
    for c in keys:
        p = U[c]; n = len(p)
        for perm in itertools.permutations(range(1, n)):
            pm = (0,) + perm
            if pm != tuple(range(n)) and all(pm[p[v]] == p[pm[v]] for v in range(1, n)):
                for e in range(1, n):
                    for f in range(1, n):
                        r = eq(vid[(c, pm[e], pm[f])], vid[(c, e, f)])
                        if r: rowsC.append(r)
        for mask in range(1, 1 << n):
            S = {v for v in range(n) if mask >> v & 1}
            if 0 not in S or len(S) < 2 or len(S) == n or any(v and p[v] not in S for v in S):
                continue
            cy, m = sub(p, S, 0)
            for e in range(1, n):
                for f in range(1, n):
                    if e in S and f in S:
                        r = eq(vid[(c, e, f)], vid[(cy, m[e], m[f])])
                    elif (e in S) != (f in S):
                        r = eq(vid[(c, e, f)])
                    else:
                        continue
                    if r: rowsC.append(r)
        for a in range(1, n):
            S = set(cone(p, a))
            if len(S) < 2:
                continue
            ncones += 1
            ca, m = sub(p, S, a)
            for f in S - {a}:
                for e in range(1, n):
                    r = eq(vid[(c, e, f)], vid[(ca, m[e], m[f])]) if (e in S and e != a) else eq(vid[(c, e, f)])
                    if r: rowsR.append(r)
    return U, keys, vid, rowsC, rowsR, ncones


def diag_sol(U, keys, vid, a):
    v = {}
    for c in keys:
        p = U[c]
        for e in range(1, len(p)):
            for f in range(1, len(p)):
                v[vid[(c, e, f)]] = F(a(depth(p, e))) if e == f else F(0)
    return v


def sat(rows, v): return all(sum(cf * v[k] for k, cf in r.items()) == 0 for r in rows)


def green(p, k, weights=None):
    """root-zero potential phi with L phi = k for L = b d (positive Laplacian), by exact elimination of the reduced system;
    weights: optional depth table a_k applied as edge-coordinate diagonal (response d^-1 diag(a) b^-1)"""
    n = len(p)
    if weights is None:
        A = [[F(0)] * (n - 1) for _ in range(n - 1)]
        for v in range(1, n):
            u = p[v]
            for x, y in ((v, u), (u, v)):
                if x: A[x - 1][x - 1] += 1
                if x and y: A[x - 1][y - 1] -= 1
        b = [F(k[v]) for v in range(1, n)]
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        for i in range(n - 1):
            piv = next(r for r in range(i, n - 1) if M[r][i] != 0)
            M[i], M[piv] = M[piv], M[i]
            inv = 1 / M[i][i]; M[i] = [x * inv for x in M[i]]
            for r in range(n - 1):
                if r != i and M[r][i] != 0:
                    cf = M[r][i]; M[r] = [x - cf * y for x, y in zip(M[r], M[i])]
        return [F(0)] + [M[i][n - 1] for i in range(n - 1)]
    cv = [F(0)] * n
    for v in range(1, n):
        cv[v] = sum((F(k[u]) for u in cone(p, v)), F(0))
    phi = [F(0)] * n
    for v in sorted(range(1, n), key=lambda v: depth(p, v)):
        phi[v] = phi[p[v]] + weights(depth(p, v)) * cv[v]
    return phi


def lap(p, phi):
    k = [F(0)] * len(p)
    for v in range(1, len(p)):
        d = phi[v] - phi[p[v]]; k[v] += d; k[p[v]] -= d
    return k


def ctot(p, x, alive, v):
    return sum((x[u] for u in cone(p, v) if alive[u]), F(0))


def main():
    rnd = random.Random(16022)
    cert = {"role": "producer", "result_sha256": RESULT_SHA, "universes": {}, "violations": []}
    viol = cert["violations"]
    ctl = {}
    for name, nmax in (("U7", 7), ("U8", 8)):
        U, keys, vid, rowsC, rowsR, ncones = build(nmax)
        K = nmax - 1
        nv = len(vid)
        dimC = nv - rank_Q(rowsC); dimCR = nv - rank_Q(rowsC + rowsR)
        sols = {"depth_indicators_solve_C": all(sat(rowsC, diag_sol(U, keys, vid, lambda d, k=k: 1 if d == k else 0)) for k in range(1, K + 1)),
                "unit_solves_C_RS": sat(rowsC + rowsR, diag_sol(U, keys, vid, lambda d: 1)),
                "depth_solves_C": sat(rowsC, diag_sol(U, keys, vid, lambda d: d)),
                "depth_violates_RS": not sat(rowsR, diag_sol(U, keys, vid, lambda d: d))}
        mism = 0; nonconst_acc = False
        tables = [{d: F(rnd.randint(-3, 3)) for d in range(1, K + 1)} for _ in range(100)] + [{d: F(1) for d in range(1, K + 1)}, {d: F(-2) for d in range(1, K + 1)}]
        for t in tables:
            r = sat(rowsR, diag_sol(U, keys, vid, lambda d: t[d])); const = len(set(t.values())) == 1
            mism += r != const; nonconst_acc |= (r and not const)
        # Green cone locality
        gv = 0; gcones = 0; lap_ok = True; depth_fails_somewhere = False
        for c in keys:
            p = U[c]; n = len(p)
            k = [F(rnd.randint(-4, 4)) for _ in range(n)]; k[0] -= sum(k)
            lap_ok &= lap(p, green(p, k)) == k
            for a in range(1, n):
                S = cone(p, a)
                if len(S) < 2:
                    continue
                gcones += 1
                cs, m = sub(p, set(S), a)
                q = U[cs]; inv = {m[v]: v for v in S}
                kc = [F(rnd.randint(-4, 4)) for _ in range(len(q))]; kc[0] -= sum(kc)
                kx = [F(0)] * n
                for i in range(len(q)): kx[inv[i]] = kc[i]
                phx, phc = green(p, kx), green(q, kc)
                dpx, dpc = green(p, kx, lambda d: d), green(q, kc, lambda d: d)
                for v in range(1, n):
                    want = phc[m[v]] - phc[q[m[v]]] if (v in m and v != a) else 0
                    gv += (phx[v] - phx[p[v]]) != want
                    wd = dpc[m[v]] - dpc[q[m[v]]] if (v in m and v != a) else 0
                    depth_fails_somewhere |= (dpx[v] - dpx[p[v]]) != wd
        # Proposition 22.4 on every (carrier, leaf) class
        classes = set(); pv = 0; dump_keeps_all = True
        for c in keys:
            p = U[c]; n = len(p)
            def mcode(v, l): return '(' + ('*' if v == l else '') + ''.join(sorted(mcode(u, l) for u in children(p, v))) + ')'
            for l in range(1, n):
                if children(p, l):
                    continue
                mc = mcode(0, l)
                if mc in classes:
                    continue
                classes.add(mc)
                x = [F(rnd.randint(-3, 3)) for _ in range(n)]; x[l] = F(rnd.choice([-2, -1, 1, 2]))
                alive = [True] * n; alive2 = alive[:]; alive2[l] = False
                y = x[:]; y[p[l]] += x[l]; y[l] = F(0)
                for v in range(1, n):
                    if v != l:
                        pv += ctot(p, x, alive, v) != ctot(p, y, alive2, v)
                pv += sum(x) != sum(y)
                pp = p[l]
                def cp(z, al, v): return ctot(p, z, al, v) if v else sum(z[u] for u in range(n) if al[u])
                pv += x[pp] != cp(x, alive, pp) - sum(cp(x, alive, u) for u in children(p, pp))
                pv += y[pp] != cp(y, alive2, pp) - sum(cp(y, alive2, u) for u in children(p, pp) if u != l)
                pv += y[pp] != x[pp] + x[l]
                g = F(rnd.choice([-3, -1, 2, 5]))
                x2 = x[:]; x2[l] += g; y2 = x2[:]; y2[pp] += x2[l]; y2[l] = F(0)
                anc = set(); u = l
                while p[u] is not None:
                    u = p[u]
                    if u: anc.add(u)
                bef = {v for v in range(1, n) if ctot(p, x, alive, v) != ctot(p, x2, alive, v)}
                aft = {v for v in range(1, n) if v != l and ctot(p, y, alive2, v) != ctot(p, y2, alive2, v)}
                pv += bef != anc | {l}; pv += aft != anc; pv += sum(x) == sum(x2)
                pv += (x2[pp] - x[pp]) != 0; pv += (y2[pp] - y[pp]) != g
                if depth(p, l) >= 2:
                    yd = x[:]; yd[0] += x[l]; yd[l] = F(0)
                    dump_keeps_all &= all(ctot(p, x, alive, v) == ctot(p, yd, alive2, v) for v in range(1, n) if v != l)
        if mism or not all(sols.values()) or gv or not lap_ok or pv:
            viol.append(name)
        digest = hashlib.sha256("\n".join(keys).encode()).hexdigest()
        cert["universes"][name] = {"carriers": len(keys), "unknowns": nv, "cones": ncones, "leaf_classes": len(classes),
                                   "dims": {"C": dimC, "C+RS": dimCR}, "solutions": sols,
                                   "random_tables": {"tables": len(tables), "mismatches": mism},
                                   "green": {"cones": gcones, "violations": gv, "laplacian_exact": lap_ok},
                                   "prop224": {"classes": len(classes), "violations": pv}, "digest": digest}
        ctl.setdefault("R1", []).append(not sols["depth_violates_RS"])
        ctl.setdefault("R2", []).append(nonconst_acc)
        ctl.setdefault("R3", []).append(dimC == 1)
        ctl.setdefault("R7", []).append(not depth_fails_somewhere)
        ctl.setdefault("R8", []).append(dump_keeps_all)
    # weight grid (chain 0..K, leaf K)
    vals = [F(x, 2) for x in range(-2, 4)]
    G = dict(vectors=0, E2=0, E5plus=0, E2_E5plus=0, R=0, CN=0, deletion=0, E2_E5plus_nonneg=0, E2_E5plus_notR=0,
             mismatch_R_deletion=0, mismatch_CN_R=0, mismatch_CN_implies_E5plus=0)
    dump_deletion = False; e2e5_forces = True
    for K in range(1, 5):
        for w in itertools.product(vals, repeat=K):
            G["vectors"] += 1
            def step(x): y = x[:K]; [y.__setitem__(K - d, y[K - d] + w[d - 1] * x[K]) for d in range(1, K + 1)]; return y
            e2 = sum(w) == 1; e5 = w[0] == 1
            Rr = True
            for d in range(1, K + 1):
                xe = [F(0)] * (K + 1); xe[K] = F(1); y = step(xe)
                Rr &= sum(y[K - d:]) == 1
            cn = list(w) == [1] + [0] * (K - 1)
            dele = True
            for _ in range(3):
                x = [F(rnd.randint(-3, 3)) for _ in range(K + 1)]; x[K] = F(rnd.choice([-2, -1, 1, 2]))
                y = step(x)
                dele &= [sum(y[v:]) for v in range(K)] == [sum(x[v:]) for v in range(K)]
            G["E2"] += e2; G["E5plus"] += e5; G["E2_E5plus"] += e2 and e5; G["R"] += Rr; G["CN"] += cn; G["deletion"] += dele
            G["E2_E5plus_nonneg"] += e2 and e5 and all(t >= 0 for t in w); G["E2_E5plus_notR"] += e2 and e5 and not Rr
            G["mismatch_R_deletion"] += Rr != dele; G["mismatch_CN_R"] += cn != Rr; G["mismatch_CN_implies_E5plus"] += cn and not e5
            if e2 and e5 and not cn: e2e5_forces = False
            if list(w) == [0] * (K - 1) + [1] and K >= 2 and dele: dump_deletion = True
    cert["grid"] = G
    # hand-written instances
    inst = {}
    ph = green((None, 0), [F(-1), F(1)]); pd = green((None, 0, 1), [F(0), F(-1), F(1)], lambda d: d)
    inst["Z1.depth_witness"] = [str(ph[1] - ph[0]), str(pd[2] - pd[1])]
    p2 = (None, 0, 1, 1, 0); k2 = [F(0), F(-2), F(1), F(1), F(0)]; g2 = green(p2, k2)
    q2 = (None, 0, 0); gq = green(q2, [F(-2), F(1), F(1)])
    inst["Z2.green_cone"] = [[str(g2[v] - g2[p2[v]]) for v in range(1, 5)], [str(gq[v] - gq[q2[v]]) for v in (1, 2)]]
    x = [F(0)] * 4; x[3] = F(1); y = [F(-1), F(1), F(1)]
    E2 = sum(y) == sum(x); E5 = y[2] == x[2] + x[3]; Rz = sum(y[1:]) == sum(x[1:]) and sum(y[2:]) == sum(x[2:]) and E2
    CNz = y == [0, 0, 1]; dz = [sum(y), sum(y[1:]), sum(y[2:])] == [sum(x), sum(x[1:]), sum(x[2:])]
    inst["Z3.signed_step"] = [[E2, E5, Rz, CNz, dz], str(sum(y[1:]))]
    p4 = (None, 0, 1, 1); al = [True] * 4; al2 = [True, True, True, False]
    xa = [F(0)] * 4; xb = [F(0), F(0), F(0), F(1)]
    def coords(z, a): return {"total": sum(z[u] for u in range(4) if a[u]), **{"c%d" % v: ctot(p4, z, a, v) for v in range(1, 4) if a[v]}}
    ya, yb = xa[:], xb[:]; yb[1] += xb[3]; yb[3] = F(0)
    ca, cb, da, db = coords(xa, al), coords(xb, al), coords(ya, al2), coords(yb, al2)
    inst["Z4.pair"] = [sorted(k for k in ca if ca[k] != cb[k]), sorted(k for k in da if da[k] != db[k]), str(xb[1] - xa[1]), str(yb[1] - ya[1])]
    p5 = (None, 0, 1); x5 = [F(0), F(0), F(1)]; y5 = [F(1), F(0), F(0)]
    inst["Z5.dump"] = str(ctot(p5, y5, [True, True, False], 1) - ctot(p5, x5, [True] * 3, 1))
    cert["instances"] = inst
    rj = lambda bad: "REJECTED" if not bad else "ACCEPTED_WRONGLY"
    cert["controls"] = {"R1_T_depth_satisfies_RS": rj(any(ctl["R1"])), "R2_nonconstant_table_satisfies_RS": rj(any(ctl["R2"])),
                        "R3_C_alone_forces_dim_1": rj(any(ctl["R3"])), "R4_genesis_dump_is_coordinate_deletion": rj(dump_deletion),
                        "R5_signed_step_satisfies_R": rj(Rz), "R6_signed_step_satisfies_CN": rj(CNz),
                        "R7_depth_response_passes_green_cone_locality": rj(any(ctl["R7"])),
                        "R8_genesis_dump_keeps_retained_cone_totals": rj(any(ctl["R8"])),
                        "R9_E2_E5plus_forces_P1_without_positivity": rj(e2e5_forces)}
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("instances", "controls", "violations", "grid")}, indent=1, sort_keys=True))
    print(json.dumps({u: {k: v for k, v in d.items() if k != "digest"} for u, d in cert["universes"].items()}, sort_keys=True))


if __name__ == "__main__":
    main()
