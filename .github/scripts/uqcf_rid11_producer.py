"""receiver_identification draft 11 (sec 17) freeze: PRODUCER. Pure Python, exact Fractions, carriers as frozensets
built by recursion over children, holdings in ROW form omega_v = a(v) x_v + sum_{w child of v} b(w) C_w, exact sparse
Gaussian elimination with W2 imposed on covers. Writes a JSON certificate (FREEZE.md sections 2 and 3)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d11_review")
S = lambda q: str(F(q))


def depth(par, v):
    d = 0
    while v != 0:
        v = par[v]; d += 1
    return d


def anc_or_eq(par, a, v):          # a <= v in prefix order
    while True:
        if v == a:
            return True
        if v == 0:
            return False
        v = par[v]


def children(par, X, v):
    return [w for w in sorted(X) if w != 0 and par[w] == v]


def carriers(par):
    n = len(par)
    kids = {v: [w for w in range(1, n) if par[w] == v] for v in range(n)}

    def sub(v):                      # all prefix-closed subsets of the subtree of v that contain v
        opts = [[frozenset()] + sub(c) for c in kids[v]]
        return [frozenset([v]).union(*combo) for combo in itertools.product(*opts)]
    return sorted(sub(0), key=lambda X: (len(X), sorted(X)))


def leaves(par, X):
    return [l for l in sorted(X) if l != 0 and not children(par, X, l)]


def chain(par, u):
    out = {u}
    while u != 0:
        u = par[u]; out.add(u)
    return frozenset(out)


# ---------- assignments (row form) ----------
def b_panel(name, par):
    n = len(par)
    out = {}
    for w in range(1, n):
        d = depth(par, w)
        out[w] = {"own": F(0), "gtax": F(1, 2) if d == 1 else F(0), "half": F(1, 4), "deep": F(1, 3) if d == 2 else F(0),
                  "sat": F(1) if w == 1 else F(0), "mixed": F((3 * w + 1) % 5, 20),
                  "negative": F(1) if d <= 2 else F(0)}[name]
    return out


def a_of(par, b, u):
    s = F(1)
    while u != 0:
        s -= b[u]; u = par[u]
    return s


def matrix_family(par, b, X):
    M = {}
    for v in X:
        kids = children(par, X, v)
        for u in X:
            val = a_of(par, b, v) if u == v else F(0)
            for w in kids:
                if anc_or_eq(par, w, u):
                    val += b[w]
            M[(v, u)] = val
    return M


def matrix_named(name, par, X):
    if name == "cone":
        return {(v, u): F(1 if anc_or_eq(par, v, u) else 0) for v in X for u in X}
    if name == "parent":
        return {(v, u): F(1 if (u != 0 and par[u] == v) or (u == v == 0) else 0) for v in X for u in X}
    return matrix_family(par, b_panel(name, par), X)


def omega(M, X, v, x):
    return sum((M[(v, u)] * x[u] for u in X), F(0))


def P1(par, X, l, x):
    y = {u: x[u] for u in X if u != l}
    y[par[l]] += x[l]
    return y


def composite_row(par, MY, Y, l, v):     # coefficients of omega_v^Y(P x) in x
    row = {u: MY[(v, u)] for u in Y}
    row[l] = MY[(v, par[l])]
    return row


AFFINE = ["own", "gtax", "half", "deep", "sat", "mixed", "negative"]
FAMILY = AFFINE[:6]
PANEL = AFFINE + ["cone", "parent"]


def panel_universe(par, uname, lines, nv):
    Cs = carriers(par)
    n = len(par)
    Mall = {}
    flags = {}
    viol = 0
    covers = [(X, X | {w}) for X in Cs for w in range(1, n) if w not in X and par[w] in X]
    prun = [(X, l) for X in Cs for l in leaves(par, X)]
    for name in PANEL:
        Ms = {X: matrix_named(name, par, X) for X in Cs}
        f = {}
        f["W1eq"] = all(sum(Ms[X][(v, u)] for v in X) == 1 for X in Cs for u in X)
        f["W1pos"] = all(val >= 0 for X in Cs for val in Ms[X].values())
        f["W2"] = all(Ms[X2][(v, u)] == (Ms[X][(v, u)] if v in X else 0) for X, X2 in covers for v in X2 for u in X)
        w4 = True
        for X, l in prun:
            Y = X - {l}; p = par[l]
            for v in Y:
                if v != p and composite_row(par, Ms[Y], Y, l, v) != {u: Ms[X][(v, u)] for u in X}:
                    w4 = False
        f["W4"] = w4
        bt = {u: Ms[chain(par, u)][(par[u], u)] for u in range(1, n)}
        aff = all(matrix_family(par, bt, X) == Ms[X] for X in Cs)
        f["family"] = aff and all(bt[u] >= 0 and a_of(par, bt, u) >= 0 for u in range(1, n))
        f["affine"] = aff
        f["L170"] = all(Ms[X][(v, u)] == (Ms[chain(par, u)][(v, u)] if anc_or_eq(par, v, u) else 0)
                        for X in Cs for v in X for u in X)
        f["i"] = all(Ms[X][(v, u)] == (1 if v == u else 0) for X in Cs for v in X for u in X)
        f["ii"] = all(Ms[X][(par[l], l)] == 0 and Ms[X - {l}][(par[l], par[l])] != 0 for X, l in prun)
        f["iii"] = all(Ms[X][(par[l], l)] == 0 for X, l in prun)
        iv = True
        for X, l in prun:
            Y = X - {l}; p = par[l]
            cr = composite_row(par, Ms[Y], Y, l, p)
            if any(cr[u] - Ms[X][(p, u)] != (1 if u == l else 0) for u in X):
                iv = False
        f["iv"] = iv
        f["D"] = all(Ms[X][(v, u)] == 0 for X in Cs for v in X for u in X if u != v and anc_or_eq(par, v, u))
        flags[name] = "".join("1" if f[k] else "0" for k in
                              ("W1eq", "W1pos", "W2", "W4", "family", "affine", "L170", "i", "ii", "iii", "iv", "D"))
        # derived both-direction theorem checks
        if (f["W1eq"] and f["W1pos"] and f["W2"] and f["W4"]) != f["family"]:
            viol += 1
        if f["W1eq"] and f["W1pos"] and f["W2"] and f["W4"] and not (f["i"] == f["ii"] == f["iii"] == f["iv"]):
            viol += 1
        if (f["W1eq"] and f["W1pos"] and f["W2"] and f["D"]) != f["i"]:
            viol += 1
        if name in AFFINE:
            b = b_panel(name, par)
            for X, l in prun:
                Y = X - {l}; p = par[l]
                al, bl, ap = a_of(par, b, l), b[l], a_of(par, b, p)
                cr = composite_row(par, Ms[Y], Y, l, p)
                inc = {u: cr[u] - Ms[X][(p, u)] for u in X}
                if inc != {u: (al if u == l else F(0)) for u in X}:
                    viol += 1
                for v in Y:
                    if v != p and composite_row(par, Ms[Y], Y, l, v) != {u: Ms[X][(v, u)] for u in X}:
                        viol += 1
                if Ms[X][(p, l)] != bl:
                    viol += 1
                for w in (1, -2, 3):
                    e = {u: F(w if u == l else 0) for u in X}
                    if omega(Ms[X], X, p, e) != w * bl or omega(Ms[Y], Y, p, P1(par, X, l, e)) != w * ap:
                        viol += 1
                before, after = Ms[X][(p, l)], Ms[Y][(p, p)]
                acq = before == 0 and after != 0
                corr = "-"
                if name in FAMILY:
                    crit = bl == 0 and ap > 0
                    if acq != crit:
                        viol += 1
                    nv["acq" if acq else "nonacq"] += 1
                    if not acq and bl == 0 and ap == 0:
                        nv["b0_a0"] += 1
                    if p != 0:
                        if al > 0:
                            r = bl / ap
                            vs = [u for u in sorted(X) if u != 0 and not anc_or_eq(par, p, u)]
                            vstar = vs[0] if vs else 0
                            xp = {u: F(1) + (1 if u == l else 0) for u in X}
                            xm = {u: F(1) + (r if u == p else 0) + ((1 - r) if u == vstar else 0) for u in X}
                            ok = all(t >= 0 for t in list(xp.values()) + list(xm.values()))
                            ok &= sum(xp.values()) == sum(xm.values())
                            ok &= omega(Ms[X], X, p, xp) == omega(Ms[X], X, p, xm)
                            sep = omega(Ms[Y], Y, p, P1(par, X, l, xp)) - omega(Ms[Y], Y, p, P1(par, X, l, xm))
                            ok &= sep == al
                            if not ok:
                                viol += 1
                            corr = S(sep)
                            if bl > 0:
                                nv["corr_bpos"] += 1
                        else:
                            if any(t != 0 for t in inc.values()):
                                viol += 1
                            corr = "0"
                            nv["D0"] += 1
                lines.append("%s|%s|%d|%d|%s|%s|%s|%s|%s|%d|%s" % (
                    name, ",".join(map(str, sorted(X))), l, p, S(al), S(bl), S(ap), S(before), S(after), int(acq), corr))
    for X in Cs:
        deg = max(len(children(par, X, v)) for v in X)
        nv["deg2"] += deg >= 2
        if uname == "U17B":
            nv["deg3"] += deg >= 3
    return {"carriers": len(Cs), "covers": len(covers), "prunings": len(prun),
            "prunings_pno": sum(1 for X, l in prun if par[l] != 0)}, flags, viol


# ---------- exact elimination (Theorem 17.1) ----------
def systems(par):
    Cs = carriers(par)
    n = len(par)
    idx = {}
    for X in Cs:
        for v in sorted(X):
            for u in sorted(X):
                idx[(X, v, u)] = len(idx)
    w1, w2, w4 = [], [], []
    for X in Cs:
        for u in X:
            w1.append(({idx[(X, v, u)]: F(1) for v in X}, F(1)))
        for w in range(1, n):
            if w not in X and par[w] in X:
                X2 = X | {w}
                for u in X:
                    for v in X2:
                        r = {idx[(X2, v, u)]: F(1)}
                        if v in X:
                            r[idx[(X, v, u)]] = F(-1)
                        w2.append((r, F(0)))
        for l in leaves(par, X):
            Y = X - {l}; p = par[l]
            for v in Y:
                if v == p:
                    continue
                for u in X:
                    r = {}
                    t = idx[(Y, v, u if u in Y else p)]
                    r[t] = r.get(t, F(0)) + 1
                    s = idx[(X, v, u)]
                    r[s] = r.get(s, F(0)) - 1
                    r = {k: c for k, c in r.items() if c != 0}
                    if r:
                        w4.append((r, F(0)))
    return Cs, idx, w1, w2, w4


def elim_dim(nvars, rows):
    piv = {}
    consistent = True
    for coefs, rhs in rows:
        r, rr = dict(coefs), rhs
        while r:
            k = min(r)
            if k in piv:
                pr, prh = piv[k]
                f = r[k]
                for kk, vv in pr.items():
                    nvv = r.get(kk, F(0)) - f * vv
                    if nvv == 0:
                        r.pop(kk, None)
                    else:
                        r[kk] = nvv
                rr -= f * prh
            else:
                f = r[k]
                piv[k] = ({kk: vv / f for kk, vv in r.items()}, rr / f)
                break
        else:
            if rr != 0:
                consistent = False
    return nvars - len(piv), consistent


def ue_tree(par):
    n = len(par)
    Cs, idx, w1, w2, w4 = systems(par)
    dim, cons = elim_dim(len(idx), w1 + w2 + w4)
    dim4, cons4 = elim_dim(len(idx), w1 + w2)
    dim2, cons2 = elim_dim(len(idx), w1 + w4)
    fam_ok = True
    for bvec in [{u: F(0) for u in range(1, n)}] + [{u: F(int(u == w)) for u in range(1, n)} for w in range(1, n)]:
        val = {}
        for X in Cs:
            M = matrix_family(par, bvec, X)
            for (v, u), m in M.items():
                val[idx[(X, v, u)]] = m
        for coefs, rhs in w1 + w2 + w4:
            if sum((c * val[k] for k, c in coefs.items()), F(0)) != rhs:
                fam_ok = False
    sd = sum(depth(par, u) for u in range(1, n))
    viol = int(not (cons and cons4 and cons2)) + int(dim != n - 1) + int(dim4 != sd) + int(not fam_ok)
    return {"carriers": len(Cs), "unknowns": len(idx), "dim": dim, "dim_noW4": dim4, "dim_noW2": dim2,
            "family_ok": fam_ok}, viol


def tree_list():
    out = []
    for n in range(1, 7):
        for t in itertools.product(*[range(i) for i in range(1, n)]):
            out.append([-1] + list(t))
    return out + [[-1, 0, 0, 1, 1, 2, 2], [-1, 0, 0, 1, 1, 1, 2]]


def explicit():
    V = {}
    T4, ch3 = [-1, 0, 1, 0], [-1, 0, 1]
    X = frozenset(range(4)); Y = X - {2}
    gt = b_panel("gtax", T4)
    M = matrix_family(T4, gt, X)
    V["X1.gtax_M"] = [[S(M[(v, u)]) for u in range(4)] for v in range(4)]
    V["X1.gtax_a"] = [S(a_of(T4, gt, u)) for u in range(4)]
    V["X1.colsums"] = [S(sum(M[(v, u)] for v in range(4))) for u in range(4)]
    x = {0: F(3), 1: F(5), 2: F(7), 3: F(2)}
    MY = matrix_family(T4, gt, Y); y = P1(T4, X, 2, x)
    V["X2.gtax_before"] = [S(omega(M, X, v, x)) for v in range(4)]
    V["X2.gtax_after"] = [S(omega(MY, Y, v, y)) for v in sorted(Y)]
    V["X2.gtax_increment"] = S(omega(MY, Y, 1, y) - omega(M, X, 1, x))
    V["X2.gtax_totals"] = [S(sum(omega(M, X, v, x) for v in X)), S(sum(omega(MY, Y, v, y) for v in Y))]
    ob = {u: F(0) for u in range(1, 4)}
    Mo, MoY = matrix_family(T4, ob, X), matrix_family(T4, ob, Y)
    V["X2.own_before"] = [S(omega(Mo, X, v, x)) for v in range(4)]
    V["X2.own_after"] = [S(omega(MoY, Y, v, y)) for v in sorted(Y)]
    gptb = {1: F(1, 4), 2: F(1, 4), 3: F(0)}
    sat = {1: F(1), 2: F(0), 3: F(0)}
    acqs = []
    for key, b in (("gptb", gptb), ("gtax", gt), ("own", ob), ("sat", sat)):
        MX, MY2 = matrix_family(T4, b, X), matrix_family(T4, b, Y)
        xp = {u: F(int(u == 2)) for u in X}; xm = {u: F(int(u == 3)) for u in X}
        bef = [omega(MX, X, 1, xp), omega(MX, X, 1, xm)]
        aft = [omega(MY2, Y, 1, P1(T4, X, 2, xp)), omega(MY2, Y, 1, P1(T4, X, 2, xm))]
        V["X3.%s_p" % key] = [[S(t) for t in bef], [S(t) for t in aft]]
        acqs.append(bef[0] == bef[1] and aft[0] != aft[1])
    V["X3.acq"] = acqs
    A, B, Dd = a_of(T4, gptb, 1), gptb[2], a_of(T4, gptb, 2)
    r = B / A
    V["X3.gptb_ABDr"] = [S(A), S(B), S(Dd), S(r)]
    MX, MY2 = matrix_family(T4, gptb, X), matrix_family(T4, gptb, Y)
    xp = {u: F(1) + (1 if u == 2 else 0) for u in X}
    xm = {u: F(1) + (r if u == 1 else 0) + ((1 - r) if u == 3 else 0) for u in X}
    V["X4.x_plus"] = [S(xp[u]) for u in range(4)]; V["X4.x_minus"] = [S(xm[u]) for u in range(4)]
    V["X4.totals"] = [S(sum(xp.values())), S(sum(xm.values()))]
    V["X4.before_plus"] = [S(omega(MX, X, v, xp)) for v in range(4)]
    V["X4.before_minus"] = [S(omega(MX, X, v, xm)) for v in range(4)]
    yp, ym = P1(T4, X, 2, xp), P1(T4, X, 2, xm)
    V["X4.Px_plus"] = [S(yp[u]) for u in sorted(Y)]; V["X4.Px_minus"] = [S(ym[u]) for u in sorted(Y)]
    V["X4.after_plus"] = [S(omega(MY2, Y, v, yp)) for v in sorted(Y)]
    V["X4.after_minus"] = [S(omega(MY2, Y, v, ym)) for v in sorted(Y)]
    V["X4.p_before"] = [S(omega(MX, X, 1, xp)), S(omega(MX, X, 1, xm))]
    V["X4.p_after"] = [S(omega(MY2, Y, 1, yp)), S(omega(MY2, Y, 1, ym))]
    V["X4.separation"] = S(omega(MY2, Y, 1, yp) - omega(MY2, Y, 1, ym))
    V["X4.leaf_holding"] = [S(omega(MX, X, 2, xp)), S(omega(MX, X, 2, xm))]
    V["X4.oneloc_before"] = S(omega(MX, X, 1, {u: F(int(u == 2)) for u in X}))
    Y3 = X - {3}
    MgY3 = matrix_family(T4, gt, Y3)
    e3 = {u: F(int(u == 3)) for u in X}
    bef, aft = omega(M, X, 0, e3), omega(MgY3, Y3, 0, P1(T4, X, 3, e3))
    V["X5.before"], V["X5.after"], V["X5.acq"] = S(bef), S(aft), bef == 0 and aft != 0
    Xc = frozenset(range(3)); xc = {0: F(3), 1: F(5), 2: F(7)}
    Mc = matrix_named("cone", ch3, Xc)
    V["X6.C"] = [S(omega(Mc, Xc, v, xc)) for v in range(3)]
    V["X6.sumC"] = S(sum(omega(Mc, Xc, v, xc) for v in Xc)); V["X6.total"] = S(sum(xc.values()))
    V["X6.W1eq"] = all(sum(Mc[(v, u)] for v in Xc) == 1 for u in Xc)
    Yc = Xc - {2}
    Mp, MpY = matrix_named("parent", ch3, Xc), matrix_named("parent", ch3, Yc)
    yc = P1(ch3, Xc, 2, xc)
    V["X7.before"] = [S(omega(Mp, Xc, v, xc)) for v in range(3)]
    V["X7.after"] = [S(omega(MpY, Yc, v, yc)) for v in sorted(Yc)]
    V["X7.changed_nonreceivers"] = [v for v in sorted(Yc) if v != 1 and omega(MpY, Yc, v, yc) != omega(Mp, Xc, v, xc)]
    for key, par in (("chain2", [-1, 0]), ("chain5", [-1, 0, 1, 2, 3]), ("T4", T4), ("star3", [-1, 0, 0, 0]),
                     ("bin2", [-1, 0, 0, 1, 1, 2, 2]), ("mixed7", [-1, 0, 0, 1, 1, 1, 2])):
        rec, _ = ue_tree(par)
        V["X8." + key] = [rec["carriers"], rec["unknowns"], rec["dim"], rec["dim_noW4"]]
        if key == "chain2":
            V["X8.chain2_noW2"] = rec["dim_noW2"]
    Mg = matrix_family(T4, gptb, X)
    V["X9.M12"] = S(Mg[(1, 2)]); V["X9.M12_chain"] = S(matrix_family(T4, gptb, chain(T4, 2))[(1, 2)])
    V["X9.M32"] = S(Mg[(3, 2)]); V["X9.M21"] = S(Mg[(2, 1)])
    return V


def main():
    sha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    uni = {}
    lines, viol, n_ge2_pos, gt_w2 = [], 0, 0, 0
    trees = tree_list()
    for par in trees:
        rec, v = ue_tree(par)
        viol += v
        n = len(par)
        n_ge2_pos += n >= 2 and rec["dim"] >= 1
        gt_w2 += rec["dim_noW2"] > n - 1
        lines.append("%d:%s|%d|%d|%d|%d|%d|%d" % (n, ",".join(map(str, par[1:])), rec["carriers"], rec["unknowns"],
                                                 rec["dim"], rec["dim_noW4"], rec["dim_noW2"], int(rec["family_ok"])))
    uni.update({"ue_trees": len(trees), "ue_lines": len(lines),
                "ue_digest": hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest(), "ue_viol": viol,
                "ue_n_ge2_dim_pos": n_ge2_pos, "ue_noW2_gt": gt_w2})
    nv = {k: 0 for k in ("acq", "nonacq", "b0_a0", "corr_bpos", "D0", "deg2", "deg3")}
    panel, flag_lines = {}, []
    for uname, par in (("U17A", [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]), ("U17B", [-1, 0, 0, 0, 1, 1, 1, 2, 2, 4, 7])):
        ul = []
        counts, flags, v = panel_universe(par, uname, ul, nv)
        panel[uname] = flags
        key = uname.lower()
        for k, c in counts.items():
            uni["%s_%s" % (key, k)] = c
        uni[key + "_lines"] = len(ul)
        uni[key + "_digest"] = hashlib.sha256("\n".join(sorted(ul)).encode()).hexdigest()
        uni[key + "_viol"] = v
        flag_lines += ["%s|%s|%s" % (uname, a, f) for a, f in flags.items()]
    uni["flags_digest"] = hashlib.sha256("\n".join(sorted(flag_lines)).encode()).hexdigest()
    for k, c in nv.items():
        uni["nv_" + k] = c
    cert = {"meta": {"role": "producer", "result_sha256": sha}, "values": explicit(), "universe": uni, "panel": panel}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps(uni, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
