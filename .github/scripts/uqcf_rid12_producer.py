"""receiver_identification draft 12 (sec 18) freeze: PRODUCER. Pure-Python exact Fractions; carriers as frozensets;
laws as dicts {value-tuple: Fraction}; source records as (origin, grade) tuples; ownership as row functionals.
Computes the preregistered exact instances (FREEZE.md sec 2) and the exhaustive universes U18A-U18D (sec 3)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d12_review")


def fs(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def law_str(d):
    return [[fs(k), fs(v)] for k, v in sorted(d.items()) if v != 0]


def dig(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


# ---------------- trees, carriers ----------------
def trees(nmax):
    out = []

    def rec(par):
        out.append(tuple(par))
        if len(par) < nmax:
            for q in range(len(par)):
                rec(par + [q])
    rec([None])
    return out


def carriers(par):
    n = len(par)
    res = []
    for k in range(1, n + 1):
        for sub in itertools.combinations(range(1, n), k - 1):
            S = frozenset((0,) + sub)
            if all(par[i] in S for i in sub):
                res.append(S)
    return res


def leaves(par, X):
    return sorted(i for i in X if i != 0 and not any(par[j] == i for j in X if j != 0))


def ancestors(par, u):  # chain [0, u] as list from 0 to u
    ch = [u]
    while ch[-1] != 0:
        ch.append(par[ch[-1]])
    return ch[::-1]


def rep(par, k, Y):  # longest prefix of k in Y
    while k not in Y:
        k = par[k]
    return k


def field(S, X):
    J = {a: F(0) for a in X}
    for k, g in S:
        J[k] += g
    return J


def push(par, S, Y):
    J = {a: F(0) for a in Y}
    for k, g in S:
        J[rep(par, k, Y)] += g
    return J


def T(par, J, l):
    p = par[l]
    out = {a: v for a, v in J.items() if a != l}
    out[p] = out[p] + J[l]
    return out


def vstr(J):
    return ",".join(fs(J[a]) for a in sorted(J))


def u18a():
    lines, viol, n_tree, n_car, n_leaf, n_pair, n_ord = [], 0, 0, 0, 0, 0, 0
    for par in trees(6):
        n_tree += 1
        C = carriers(par)
        n_car += len(C)
        pstr = "".join("-" if q is None else str(q) for q in par)
        for X in C:
            S = [(k, F(k + 1)) for k in sorted(X)] + [(k, F(1, k + 2)) for k in sorted(X)]
            J = field(S, X)
            for l in leaves(par, X):
                n_leaf += 1
                Y = X - {l}
                a, b = push(par, S, Y), T(par, J, l)
                moved = [(k, g) for k, g in S if rep(par, k, Y) != k]
                viol += (a != b) + (len(moved) != 2) + any(k != l or rep(par, k, Y) != par[l] for k, _ in moved)
                lines.append("%s|%s|%d|%s" % (pstr, ",".join(map(str, sorted(X))), l, vstr(a)))
            for Y in C:
                if Y < X:
                    n_pair += 1
                    target = push(par, S, Y)
                    cnt = [0]

                    def walk(Z, Jz):
                        if Z == Y:
                            cnt[0] += 1
                            return Jz == target
                        ok = True
                        for l in leaves(par, Z):
                            if l not in Y:
                                ok &= walk(Z - {l}, T(par, Jz, l))
                        return ok
                    viol += not walk(X, J)
                    n_ord += cnt[0]
                    lines.append("%s|%s|%s|%s|%d" % (pstr, ",".join(map(str, sorted(X))), ",".join(map(str, sorted(Y))),
                                                     vstr(target), cnt[0]))
    return {"u18a_trees": n_tree, "u18a_carriers": n_car, "u18a_leaf": n_leaf, "u18a_pairs": n_pair,
            "u18a_orders": n_ord, "u18a_digest": dig(lines), "u18a_viol": viol}


# ---------------- laws ----------------
def tv(a, b):
    keys = set(a) | set(b)
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in keys) / 2


def marg(law, fn):
    out = {}
    for k, w in law.items():
        y = fn(k)
        out[y] = out.get(y, 0) + w
    return out


def family_law_product(recs, qs):
    law = {}
    for pres in itertools.product((0, 1), repeat=len(recs)):
        w = F(1)
        for b, q in zip(pres, qs):
            w *= q if b else 1 - q
        if w:
            fam = tuple(r for r, b in zip(recs, pres) if b)
            law[fam] = law.get(fam, 0) + w
    return law


def field_law(fam_law, D, X, par, Y=None):
    """law of the field vector (tuple over sorted X) before, or over sorted Y after (pushforward)."""
    out = {}
    for fam, w in fam_law.items():
        S = list(fam) + list(D)
        J = field(S, X) if Y is None else push(par, S, Y)
        key = tuple(J[a] for a in sorted(J))
        out[key] = out.get(key, 0) + w
    return out


def shift(law, d):
    return {k + d: v for k, v in law.items()}


def is_product(law, dim):
    margs = [marg(law, lambda k, i=i: k[i]) for i in range(dim)]
    for k in itertools.product(*[sorted(m) for m in margs]):
        w = F(1)
        for i, m in enumerate(margs):
            w *= m[k[i]]
        if law.get(tuple(k), 0) != w:
            return False
    return True


T5 = (None, 0, 1, 1, 0)
RECS = [(1, F(1)), (2, F(2)), (3, F(1, 2)), (4, F(1)), (0, F(1))]


def u18b_laws():
    laws = []
    for qs in itertools.product((F(0), F(1, 3), F(1, 2)), repeat=5):
        laws.append(("prod", "".join({F(0): "0", F(1, 3): "t", F(1, 2): "h"}[q] for q in qs),
                     family_law_product(RECS, qs)))
    atoms = [(), (RECS[0], RECS[1]), (RECS[1],), (RECS[3],), (RECS[0], RECS[2], RECS[4])]
    for w in itertools.product((0, 1, 2), repeat=5):
        if not any(w) or all(x in (0, 2) for x in w):
            continue
        s = sum(w)
        law = {}
        for a, x in zip(atoms, w):
            if x:
                law[a] = law.get(a, 0) + F(x, s)
        laws.append(("corr", "".join(map(str, w)), law))
    return laws


CATALOG = [()] + [((a, F(g)),) for g in (1, 2) for a in range(5)]


def cat_str(D):
    return "-" if not D else "%s@%d" % (fs(D[0][1]), D[0][0])


def u18b():
    X = frozenset(range(5))
    lines, viol = [], 0
    conf = {"blind": [0, 0, 0, 0], "sep": [0, 0, 0, 0]}  # [comp&der, comp&!der, !comp&der, !comp&!der]
    cnt = {"cases": 0, "transfer": 0, "oneloc": 0, "nv_multi": 0, "nv_corr_adv": 0, "nv_bound_eq": 0,
           "nv_bound_gt": 0, "prodclass_fiberprod": 0, "prodclass_total": 0}
    laws = u18b_laws()
    for l in (2, 3, 4):
        p = T5[l]
        Y = X - {l}
        ys = sorted(Y)
        ip = ys.index(p)
        for cls, lid, fam_law in laws:
            mu = marg(fam_law, lambda f: sum((g for k, g in f if k == p), F(0)))
            nu = marg(fam_law, lambda f: sum((g for k, g in f if k in (p, l)), F(0)))
            bg_after = field_law(fam_law, (), X, T5, Y)
            fprod = is_product(bg_after, len(ys))
            if cls == "prod":
                cnt["prodclass_total"] += 1
                cnt["prodclass_fiberprod"] += fprod
            multi = any(w > 0 and sum(1 for k, _ in f if k in (p, l)) >= 2 for f, w in fam_law.items())
            maxnu = max(nu.values())
            for Dp in CATALOG:
                for Dm in CATALOG:
                    if Dp == Dm:
                        continue
                    cnt["cases"] += 1
                    Dv = lambda D, A: sum((g for k, g in D if k in A), F(0))
                    fb = {s: field_law(fam_law, D, X, T5) for s, D in (("+", Dp), ("-", Dm))}
                    fa = {s: field_law(fam_law, D, X, T5, Y) for s, D in (("+", Dp), ("-", Dm))}
                    rb = {s: marg(fb[s], lambda k: k[p]) for s in fb}
                    ra = {s: marg(fa[s], lambda k: k[ip]) for s in fa}
                    # 18.2(a)
                    for s, D in (("+", Dp), ("-", Dm)):
                        viol += rb[s] != shift(mu, Dv(D, {p}))
                        viol += ra[s] != shift(nu, Dv(D, {p, l}))
                    blind = rb["+"] == rb["-"]
                    sep = ra["+"] != ra["-"]
                    dblind = Dv(Dp, {p}) == Dv(Dm, {p})
                    dsep = Dv(Dp, {p, l}) != Dv(Dm, {p, l})
                    for key, c, d in (("blind", blind, dblind), ("sep", sep, dsep)):
                        conf[key][(0 if c else 2) + (0 if d else 1)] += 1
                    cnt["transfer"] += blind and sep
                    t = tv(ra["+"], ra["-"])
                    tj = tv(fa["+"], fa["-"])
                    tf = tv(fb["+"], fb["-"])
                    qa = {s: marg(ra[s], lambda y: int(y > 0)) for s in ra}
                    tq = tv(qa["+"], qa["-"])
                    if sep:
                        viol += not (t >= maxnu > 0)
                        cnt["nv_bound_eq"] += t == maxnu
                        cnt["nv_bound_gt"] += t > maxnu
                    viol += not (t <= tj <= tf)
                    viol += not (tq <= t)
                    if Dm == () and Dp != () and Dp[0][0] == l:
                        cnt["oneloc"] += 1
                        viol += tq != nu.get(F(0), 0)
                        if fprod:
                            viol += tj != t
                        cnt["nv_multi"] += multi
                        cnt["nv_corr_adv"] += cls == "corr" and tj > t
                    lines.append("|".join([str(l), cls, lid, cat_str(Dp), cat_str(Dm), str(int(blind)), str(int(sep)),
                                           fs(t), fs(tj), fs(tf), fs(maxnu), fs(tq)]))
    u = {"u18b_" + k: v for k, v in cnt.items()}
    u.update({"u18b_laws": len(laws), "u18b_digest": dig(lines), "u18b_viol": viol,
              "u18b_conf_blind": conf["blind"], "u18b_conf_sep": conf["sep"]})
    return u


# ---------------- ownership (rows) ----------------
U17A = (None, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6)
U17B = (None, 0, 0, 0, 1, 1, 1, 2, 2, 4, 7)


def depth(par, u):
    return len(ancestors(par, u)) - 1


def column(par, asg, u):
    """distribution over the chain [0,u]: dict v -> share"""
    ch = ancestors(par, u)
    if u == 0:
        return {0: F(1)}
    if asg in ("own", "field"):
        return {u: F(1)}
    if asg in ("gtax", "mixed", "root"):
        def b(w):
            if asg == "gtax":
                return F(1, 2) if depth(par, w) == 1 else F(0)
            if asg == "root":
                return F(1) if depth(par, w) == 1 else F(0)
            return F((3 * w + 1) % 5, 20)
        col = {u: 1 - sum((b(w) for w in ch[1:]), F(0))}
        for i, v in enumerate(ch[:-1]):
            col[v] = col.get(v, 0) + b(ch[i + 1])
        return col
    if asg == "parent":
        return {par[u]: F(1)}
    if asg == "uniform":
        return {v: F(1, len(ch)) for v in ch}
    if asg == "pert":
        return {7: F(1, 2), 0: F(1, 2)} if u == 7 else {u: F(1)}
    if asg == "rand":
        ws = {v: 1 + (5 * u + 3 * v) % 4 for v in ch}
        s = sum(ws.values())
        return {v: F(w, s) for v, w in ws.items()}
    raise KeyError(asg)


PANEL = ["own", "gtax", "mixed", "root", "field", "parent", "uniform", "pert", "rand"]


def rows(par, asg, X):
    """omega^X as {v: {u: coeff}}"""
    om = {v: {} for v in X}
    for u in X:
        for v, c in column(par, asg, u).items():
            if c:
                om[v][u] = c
    return om


def apply_rows(om, x):
    return {v: sum((c * x[u] for u, c in r.items()), F(0)) for v, r in om.items()}


def basis(X, u):
    return {a: F(int(a == u)) for a in X}


def P(par, x, l):
    return T(par, x, l)


def field_holdings(S, X):  # (H-J): holdings = field value
    return field(S, X)


def u18c():
    out, lines, viol = {}, [], 0
    acq = {}
    for uname, par in (("U17A", U17A), ("U17B", U17B)):
        C = carriers(par)
        n = len(par)
        tc = {}
        for asg in PANEL:
            ok12 = True
            for X in C:
                om = rows(par, asg, X)
                for u in X:  # W1
                    cs = [om[v].get(u, 0) for v in X]
                    ok12 &= sum(cs) == 1 and min(cs) >= 0
                for w in range(1, n):  # W2 on covers
                    if w not in X and par[w] in X:
                        om2 = rows(par, asg, X | {w})
                        ok12 &= all(om2[v].get(u, 0) == om[v].get(u, 0) for v in X for u in X)
                        ok12 &= all(om2[w].get(u, 0) == 0 for u in X)
            viol += not ok12
            t, univ_acq, w4_all = 0, True, True
            for X in C:
                omX = rows(par, asg, X)
                for l in leaves(par, X):
                    p = par[l]
                    Y = X - {l}
                    omY = rows(par, asg, Y)
                    xs = sorted(X)
                    # grade-level facts
                    for u in Y:
                        e = basis(Y, u)
                        Ie = {a: e.get(a, F(0)) for a in X}
                        viol += P(par, Ie, l) != e
                    if asg == "field":  # (H-J): holdings before = J_S on X, after = r_* J_S on Y
                        S = [(k, F(k + 1)) for k in xs] + [(l, F(1, 3))]
                        Jx, Jy = field_holdings(S, X), push(par, S, Y)
                        viol += Jy != T(par, Jx, l)
                        viol += any(Jy[a] != Jx[a] for a in Y if a != p)
                    hX = {u: apply_rows(omX, basis(X, u)) for u in X}
                    hY = {u: apply_rows(omY, P(par, basis(X, u), l)) for u in X}
                    # (i) W4 as functionals: compare on basis
                    i_ok = all(hY[u][v] == hX[u][v] for u in X for v in Y if v != p)
                    # (ii) naturality omega^Y P = P omega^X
                    ii_ok = all(hY[u] == P(par, hX[u], l) for u in X)
                    # (iii) descent
                    dvec = {a: basis(X, l)[a] - basis(X, p)[a] for a in X}
                    img = apply_rows(omX, dvec)
                    lam = img[l]
                    iii_ok = all(img[a] == (lam if a == l else (-lam if a == p else 0)) for a in X)
                    # (iv)
                    iv_ok = all(omX[v].get(l, 0) == omX[v].get(p, 0) for v in ancestors(par, p)[:-1])
                    viol += len({i_ok, ii_ok, iii_ok, iv_ok}) != 1
                    t += i_ok
                    w4_all &= i_ok
                    # one-location acquisition: before omega_p(e_l), after omega_p^Y(P e_l)
                    before = omX[p].get(l, 0)
                    after = hY[l][p]
                    univ_acq &= before == 0 and after != 0
                    lines.append("%s|%s|%s|%d|%d|%d|%d|%d" % (uname, asg, ",".join(map(str, xs)), l, i_ok, ii_ok, iii_ok,
                                                             iv_ok))
            tc[asg] = t
            if w4_all:
                acq[uname + "." + asg] = univ_acq
        out[uname] = tc
    return {"u18c_true": out, "u18c_acq": acq, "u18c_digest": dig(lines), "u18c_lines": len(lines), "u18c_viol": viol}


# ---------------- Kraus (Cayley) ----------------
def matmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0)) for j in range(len(B[0]))] for i in range(len(A))]


def inv(A):
    n = len(A)
    M = [list(r) + [F(int(i == j)) for j in range(n)] for i, r in enumerate(A)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [r[n:] for r in M]


def cayley(r, seed):
    A = [[F(0)] * r for _ in range(r)]
    for i in range(r):
        for j in range(i + 1, r):
            v = F(((7 * seed + 3 * i + 5 * j) % 5) - 2, 1 + (i + j + seed) % 3)
            A[i][j], A[j][i] = v, -v
    I = [[F(int(i == j)) for j in range(r)] for i in range(r)]
    return matmul([[I[i][j] - A[i][j] for j in range(r)] for i in range(r)],
                  inv([[I[i][j] + A[i][j] for j in range(r)] for i in range(r)]))


def rank(rowsM):
    M = [list(r) for r in rowsM]
    rk, c, ncol = 0, 0, len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk


def kraus_family(dl, dp, r, seed):
    """K[i] as dict {(out, (j,x)): coeff}."""
    K = [dict() for _ in range(r)]
    for n in range(dl + dp - 1):
        fib = [(j, n - j) for j in range(dl) if 0 <= n - j < dp]
        Qm = cayley(r, seed + 10 * n)
        for col, b in enumerate(fib):
            for i in range(r):
                if Qm[i][col]:
                    K[i][(n, b)] = Qm[i][col]
    return K


def apply_kraus(K, psi):  # psi dict b->amp ; returns output density dict (a,b)->val
    rho = {}
    for Ki in K:
        out = {}
        for (o, b), c in Ki.items():
            if psi.get(b):
                out[o] = out.get(o, 0) + c * psi[b]
        for a, va in out.items():
            for b2, vb in out.items():
                rho[(a, b2)] = rho.get((a, b2), 0) + va * vb
    return rho


def u18d():
    lines, viol, fam, ops, ncl, nco = [], 0, 0, 0, 0, 0
    for dl, dp in ((2, 2), (2, 3), (3, 2), (3, 3)):
        m = min(dl, dp)
        B = [(j, x) for j in range(dl) for x in range(dp)]
        for r in (m, m + 1):
            for seed in range(3):
                fam += 1
                K = kraus_family(dl, dp, r, seed)
                ops += len(K)
                tp = all(sum((Ki.get((o, b), 0) * Ki.get((o, b2), 0) for Ki in K for o in range(dl + dp - 1)), F(0))
                         == int(b == b2) for b in B for b2 in B)
                inter = all(all(o == b[0] + b[1] for (o, b), c in Ki.items() if c) for Ki in K)
                cl = True
                for b in B:
                    ncl += 1
                    rho = apply_kraus(K, {b: F(1)})
                    cl &= {k: v for k, v in rho.items() if v} == {(b[0] + b[1], b[0] + b[1]): F(1)}
                rk = rank([[Ki.get((o, b), F(0)) for o in range(dl + dp - 1) for b in B] for Ki in K])
                viol += not (tp and inter and cl and rk >= m)
                lines.append("%d|%d|%d|%d|%d|%d|%d|%d" % (dl, dp, r, seed, tp, inter, cl, rk >= m))
                for n in range(dl + dp - 1):
                    fib = [b for b in B if b[0] + b[1] == n]
                    if len(fib) < 2:
                        continue
                    for sgn in (0, 1):
                        nco += 1
                        psi = {b: F((-1) ** (i * sgn)) for i, b in enumerate(fib)}
                        norm = sum(v * v for v in psi.values())
                        rho = {k: v / norm for k, v in apply_kraus(K, psi).items() if v}
                        pure = rho == {(n, n): F(1)}
                        trq = sum((v for (a, b2), v in rho.items() if a == b2 and a > 0), F(0))
                        viol += not (pure and trq == int(n > 0))
                        lines.append("%d|%d|%d|%d|%d|%d|%d|%s" % (dl, dp, r, seed, n, len(fib), pure, fs(trq)))
    return {"u18d_families": fam, "u18d_ops": ops, "u18d_classical": ncl, "u18d_coherent": nco,
            "u18d_digest": dig(lines), "u18d_viol": viol}


# ---------------- exact instances ----------------
def inst():
    V = {}
    X = frozenset({0, 1, 2, 3})
    par = (None, 0, 1, 0)
    Y = X - {2}
    p, l, v = 1, 2, 3
    ys = sorted(Y)

    def scenario(fam_law, Dp, Dm):
        fb = {s: field_law(fam_law, D, X, par) for s, D in (("+", Dp), ("-", Dm))}
        fa = {s: field_law(fam_law, D, X, par, Y) for s, D in (("+", Dp), ("-", Dm))}
        rb = {s: marg(fb[s], lambda k: k[p]) for s in fb}
        ra = {s: marg(fa[s], lambda k: k[ys.index(p)]) for s in fa}
        nu = marg(fam_law, lambda f: sum((g for k, g in f if k in (p, l)), F(0)))
        qa = {s: marg(ra[s], lambda y: int(y > 0)) for s in ra}
        bg = field_law(fam_law, (), X, par, Y)
        return dict(rb=rb, ra=ra, nu=nu, tv=tv(ra["+"], ra["-"]), tj=tv(fa["+"], fa["-"]), tf=tv(fb["+"], fb["-"]),
                    tq=tv(qa["+"], qa["-"]), blind=rb["+"] == rb["-"], sep=ra["+"] != ra["-"],
                    fprod=is_product(bg, len(ys)), maxnu=max(nu.values()))

    def eqclass(nu, g):
        supp = sorted(k for k, w in nu.items() if w)
        if any((k / g).denominator != 1 for k in supp):
            return False
        top = int(max(supp) / g)
        ws = [nu.get(j * g, 0) for j in range(top + 2)]
        return all(ws[j] >= ws[j + 1] for j in range(len(ws) - 1))
    bgA = family_law_product([(1, F(1)), (2, F(2))], (F(1, 2), F(1, 3)))
    a = scenario(bgA, ((2, F(1)),), ())
    V["Y1.mu_plus"], V["Y1.mu_minus"] = law_str(a["rb"]["+"]), law_str(a["rb"]["-"])
    V["Y1.nu"], V["Y1.after_plus"] = law_str(a["nu"]), law_str(a["ra"]["+"])
    V["Y1.blind"], V["Y1.sep"] = a["blind"], a["sep"]
    V["Y1.tv"], V["Y1.maxnu"], V["Y1.tvq"] = fs(a["tv"]), fs(a["maxnu"]), fs(a["tq"])
    V["Y1.tv_joint"], V["Y1.tv_full"], V["Y1.eqclass"] = fs(a["tj"]), fs(a["tf"]), eqclass(a["nu"], F(1))
    b = scenario(bgA, ((2, F(2)),), ())
    V["Y2.tv"], V["Y2.tvq"], V["Y2.tv_joint"], V["Y2.tv_full"] = fs(b["tv"]), fs(b["tq"]), fs(b["tj"]), fs(b["tf"])
    V["Y2.eqclass"] = eqclass(b["nu"], F(2))
    bgC = {((2, F(1)),): F(1, 2), ((3, F(1)),): F(1, 2)}
    c = scenario(bgC, ((2, F(1)),), ())
    V["Y3.after_plus"], V["Y3.after_minus"] = law_str(c["ra"]["+"]), law_str(c["ra"]["-"])
    V["Y3.blind"], V["Y3.tv"], V["Y3.maxnu"] = c["blind"], fs(c["tv"]), fs(c["maxnu"])
    V["Y3.tv_joint"], V["Y3.tv_full"], V["Y3.tvq"], V["Y3.fiber_product"] = fs(c["tj"]), fs(c["tf"]), fs(c["tq"]), c["fprod"]
    Dp, Dm = [(2, F(1))], [(3, F(1))]
    V["Y4.p_before"] = [fs(field(Dp, X)[p]), fs(field(Dm, X)[p])]
    V["Y4.v_before"] = [fs(field(Dp, X)[v]), fs(field(Dm, X)[v])]
    V["Y4.p_after"] = [fs(push(par, Dp, Y)[p]), fs(push(par, Dm, Y)[p])]
    d = scenario({(): F(1)}, tuple(Dp), tuple(Dm))
    V["Y4.tv"], V["Y4.tvq"], V["Y4.tv_full"], V["Y4.blind"] = fs(d["tv"]), fs(d["tq"]), fs(d["tf"]), d["blind"]
    e = scenario(family_law_product([(1, F(1))], (F(3, 4),)), ((2, F(1)),), ())
    V["Y5.nu"], V["Y5.tv"], V["Y5.tvq"], V["Y5.maxnu"] = law_str(e["nu"]), fs(e["tv"]), fs(e["tq"]), fs(e["maxnu"])
    V["Y5.eqclass"] = eqclass(e["nu"], F(1))
    # Y6 Kraus witness
    Bs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    K = [{(0, (0, 0)): F(1), (1, (0, 1)): F(1)}, {(1, (1, 0)): F(1), (2, (1, 1)): F(1)}]
    V["Y6.K0"], V["Y6.K1"] = [[[fs(Ki.get((o, b), 0)) for b in Bs] for o in range(3)] for Ki in K]
    V["Y6.tp"] = all(sum((Ki.get((o, b), 0) * Ki.get((o, b2), 0) for Ki in K for o in range(3)), F(0)) == int(b == b2)
                     for b in Bs for b2 in Bs)
    V["Y6.intertwine"] = [all(o == b[0] + b[1] for (o, b), c in Ki.items() if c) for Ki in K]
    psi = {(0, 1): F(1), (1, 0): F(1)}  # unnormalized, norm^2 = 2
    rho = apply_kraus(K, psi)
    V["Y6.out_psi"] = [fs(rho.get((o, o), 0) / 2) for o in range(3)]
    assert all(v == 0 for (a1, b1), v in rho.items() if a1 != b1)
    V["Y6.branch"] = [fs(sum((c * psi.get(bb, 0)) ** 2 for (o, bb), c in Ki.items()) / 2) for Ki in K]
    V["Y6.rank"] = rank([[Ki.get((o, b), F(0)) for o in range(3) for b in Bs] for Ki in K])
    V["Y6.maxfiber"] = max(sum(1 for b in Bs if b[0] + b[1] == n) for n in range(3))
    fams = [[(2, F(1)), (1, F(2))], [(2, F(2)), (1, F(1))], [(2, F(3))]]
    V["Y7.values"] = [fs(push(par, S, Y)[p]) for S in fams]
    V["Y7.components"] = len({tuple(sorted((k, g) for k, g in S if rep(par, k, Y) == p)) for S in fams})
    x = {0: F(3), 1: F(5), 2: F(7), 3: F(2)}
    for asg in ("own", "gtax", "parent"):
        omX, omY = rows(par, asg, X), rows(par, asg, Y)
        hx = apply_rows(omX, x)
        hy = apply_rows(omY, T(par, x, 2))
        pw = T(par, hx, 2)
        nat = all(apply_rows(omY, T(par, basis(X, u), 2)) == T(par, apply_rows(omX, basis(X, u)), 2) for u in X)
        dv = apply_rows(omX, {a: basis(X, 2)[a] - basis(X, 1)[a] for a in X})
        V["Y8." + asg] = [[fs(hx[a]) for a in sorted(X)], [fs(hy[a]) for a in ys], [fs(pw[a]) for a in ys], nat,
                          [fs(dv[a]) for a in sorted(X)]]
    omP = rows(par, "parent", X)
    V["Y8.parent_iv"] = [fs(omP[0].get(2, 0)), fs(omP[0].get(1, 0))]
    forced = T(par, x, 2)
    dump = {a: x[a] for a in ys}
    dump[0] += x[2]
    V["Y9.forced"], V["Y9.dump"] = [fs(forced[a]) for a in ys], [fs(dump[a]) for a in ys]
    V["Y9.totals"] = [fs(sum(x.values())), fs(sum(forced.values())), fs(sum(dump.values()))]
    V["Y9.changed"] = [[a for a in ys if forced[a] != x[a]][0], [a for a in ys if dump[a] != x[a]][0]]
    reg = []
    for xo, xl, xp in ((0, 1, 0), (0, 0, 1)):
        reg.append([int(xp + xl > 0), int(xp > 0)])
    V["Y9.region"] = reg
    G = [F(0), F(1, 2), F(1), F(2)]
    inv_n = form_n = 0
    for vals in itertools.product((0, 1, 2), repeat=4):
        f = dict(zip(G, vals))
        if all(f[c * y] == f[y] for c in (F(2), F(1, 2)) for y in G if c * y in f):
            inv_n += 1
            form_n += len({f[y] for y in G if y > 0}) == 1
    V["Y10.invariant"] = [inv_n, form_n]
    return V


def main():
    result_sha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    uni = {}
    for fn in (u18a, u18b, u18c, u18d):
        uni.update(fn())
    cert = {"meta": {"role": "producer", "result_sha256": result_sha}, "values": inst(), "universe": uni}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps(cert["universe"], indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
