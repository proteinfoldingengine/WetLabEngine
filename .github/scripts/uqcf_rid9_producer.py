"""receiver_identification draft 9 (sec 16) freeze: PRODUCER. Pure-Python exact Fractions on parent-pointer trees:
carriers as frozensets, grade vectors as dicts, longest prefix by walking up parent pointers, explicit depth-first
enumeration of every single-pruning sequence with the composite carried as basis images, and the Theorem 16.1
triangular system solved by forward substitution. Preregistration: FREEZE.md in receiver_identification_d9_review/
(committed before this code)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d9_review")
PANEL = ["P1", "genesis", "grandparent", "halfsplit", "erase", "double", "fixed_e2", "leafshift", "dipole", "sign"]
DFS_RULES = ["P1", "genesis", "grandparent", "halfsplit"]


def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def trees(n):
    for p in itertools.product(*[range(i) for i in range(1, n)]):
        yield (None,) + p


def pstr(par):
    return "%d:%s" % (len(par), ",".join(str(p) for p in par[1:]))


def ancestors(par, v):
    out = []
    while par[v] is not None:
        v = par[v]
        out.append(v)
    return out  # nearest first


def depth(par, v):
    return len(ancestors(par, v))


def is_carrier(par, W):
    return len(W) > 0 and all(v == 0 or par[v] in W for v in W) and 0 in W


def children_in(par, W, v):
    return [c for c in W if par[c] == v]


def carriers(par):
    n = len(par)
    out = []
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            W = frozenset(S)
            if is_carrier(par, W):
                out.append(W)
    return out


def lp(par, Y, v):
    while v not in Y:
        v = par[v]
    return v


def push(par, Y, x):
    out = {y: F(0) for y in Y}
    for v, c in x.items():
        out[lp(par, Y, v)] += c
    return out


def vec(W, x):
    return [fs(x.get(v, 0)) for v in sorted(W)]


def clean(x):
    return {k: v for k, v in x.items() if v != 0}


def unit(v, c=1):
    return {v: F(c)}


# ---------- rules: image of the pruned unit, and full application ----------
def img(rule, par, W, l, j=None):
    a = ancestors(par, l)
    k = len(a)
    if rule == "P1":
        return {a[0]: F(1)}
    if rule == "genesis":
        return {0: F(1)}
    if rule == "grandparent":
        return {a[1]: F(1)} if k >= 2 else {0: F(1)}
    if rule == "halfsplit":
        return {0: F(1)} if k == 1 else clean({a[0]: F(1, 2), a[1]: F(1, 2)} if a[0] != a[1] else {a[0]: F(1)})
    if rule == "erase":
        return {}
    if rule == "double":
        return {a[0]: F(2)}
    if rule == "fixed_e2":
        return {a[1]: F(1)} if k >= 2 else {}
    if rule == "dipole":
        na = sorted(v for v in W if v != l and v not in a)
        if len(na) >= 2:
            d = {a[0]: F(1)}
            d[na[0]] = d.get(na[0], 0) + 1
            d[na[1]] = d.get(na[1], 0) - 1
            return clean(d)
        return {a[0]: F(1)}
    if rule == "jump":
        return {a[j[k - 1] - 1]: F(1)}
    raise ValueError(rule)


def apply(rule, par, W, l, x):
    """Full T_{W,l}(x) as a dict on W \\ {l}."""
    out = {v: F(0) for v in W if v != l}
    xl = F(x.get(l, 0))
    if rule == "leafshift":
        leaves = [v for v in W if v != 0 and not children_in(par, W, v)]
        for v, c in x.items():
            if v in leaves:
                out[par[v]] += c
            else:
                out[v] += c
        return out
    if rule == "sign":
        for v, c in x.items():
            if v != l:
                out[v] += c
        out[par[l] if xl >= 0 else 0] += xl
        return out
    for v, c in x.items():
        if v != l:
            out[v] += c
    for v, c in img(rule, par, W, l).items():
        out[v] += xl * c
    return out


def eqv(a, b):
    return clean(a) == clean(b)


def lin(*terms):
    out = {}
    for c, x in terms:
        for k, v in x.items():
            out[k] = out.get(k, 0) + c * v
    return clean(out)


# ---------- section 2: exact instances ----------
def instances():
    V = {}
    c = (None, 0, 1)
    x = {0: F(3), 1: F(5), 2: F(7)}
    Y = frozenset({0, 1})
    W = frozenset({0, 1, 2})
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        V["X1." + r] = vec(Y, apply(r, c, W, 2, x))
    for r in ("P1", "genesis", "grandparent"):
        V["X1.receiver_" + r] = [k for k, v in clean(apply(r, c, W, 2, unit(2))).items()][0]
    t = (None, 0, 1, 0)
    W = frozenset(range(4))
    Y = frozenset({0, 1, 3})
    xp, xm = unit(2), unit(3)
    Tp, Tm = apply("P1", t, W, 2, xp), apply("P1", t, W, 2, xm)
    V["X2.p_before"] = [fs(xp.get(1, 0)), fs(xm.get(1, 0))]
    V["X2.T_plus"], V["X2.T_minus"] = vec(Y, Tp), vec(Y, Tm)
    V["X2.p_after"] = [fs(Tp[1]), fs(Tm[1])]
    V["X2.totals"] = [fs(sum(z.values())) for z in (xp, Tp, xm, Tm)]
    for r in ("genesis", "grandparent", "halfsplit"):
        V["X2.p_after_" + r] = [fs(apply(r, t, W, 2, xp)[1]), fs(apply(r, t, W, 2, xm)[1])]
    x = {0: F(1), 1: F(-2), 2: F(3), 3: F(4)}
    xq = dict(x); xq[2] += -5
    Tx, Txq = apply("P1", t, W, 2, x), apply("P1", t, W, 2, xq)
    V["X3.Tx"], V["X3.Txp"] = vec(Y, Tx), vec(Y, Txq)
    V["X3.diff"] = vec(Y, lin((1, Txq), (-1, Tx)))
    V["X3.changed_before"] = sorted(v for v in W if x.get(v, 0) != xq.get(v, 0))
    V["X3.changed_after"] = sorted(v for v in Y if Tx[v] != Txq[v])
    V["X3.totals"] = [fs(sum(z.values())) for z in (x, Tx, xq, Txq)]
    w, depths = solve_triangular()
    V["X4.w"], V["X4.depths"] = [fs(a) for a in w], depths
    ch = {1: (None, 0), 2: (None, 0, 1), 3: (None, 0, 1, 2)}
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        rows = []
        for k in (1, 2, 3):
            p = ch[k]
            im = img(r, p, frozenset(range(k + 1)), k)
            a = ancestors(p, k)
            rows.append([fs(im.get(a[d], 0)) for d in range(k)])
        V["X5." + r] = rows
    t6 = (None, 0, 1, 1, 0, 4)
    Y6 = frozenset({0, 1})
    x6 = {v: F(v + 1) for v in range(6)}
    seqs = []
    enum_sequences(t6, frozenset(range(6)), Y6, [], seqs)
    V["X6.orders"] = len(seqs)
    V["X6.maximal"] = sorted(m for m in range(6) if m not in Y6 and not any(par_desc(t6, c, m) for c in range(6) if c not in Y6 and c != m))
    V["X6.r"] = [lp(t6, Y6, v) for v in range(6)]
    for r in ("P1", "genesis", "grandparent", "halfsplit"):
        outs = set()
        for s in seqs:
            z, Wc = dict(x6), frozenset(range(6))
            for l in s:
                z = apply(r, t6, Wc, l, z)
                Wc = Wc - {l}
            outs.add(tuple(vec(Y6, z)))
        assert len(outs) == 1
        V["X6." + r] = list(outs.pop())
    W6 = frozenset(range(6))
    rem = sorted(l for l in W6 if is_carrier(t6, W6 - {l}))
    V["X7.removable"], V["X7.genesis_removable"] = rem, 0 in rem
    c3, W3, Y3 = (None, 0, 1), frozenset({0, 1, 2}), frozenset({0, 1})
    tp, tm = apply("sign", c3, W3, 2, unit(2)), apply("sign", c3, W3, 2, unit(2, -1))
    V["X8.T_plus"], V["X8.T_minus"] = vec(Y3, tp), vec(Y3, tm)
    V["X8.neg_T_plus"] = vec(Y3, lin((-1, tp)))
    V["X9.T_e3"] = vec(Y, apply("leafshift", t, W, 2, unit(3)))
    V["X9.T_e1"] = vec(Y, apply("leafshift", t, W, 2, unit(1)))
    st, Ws, Ys = (None, 0, 0, 0), frozenset(range(4)), frozenset({0, 1, 2})
    V["X10.dipole"] = vec(Ys, apply("dipole", st, Ws, 3, unit(3)))
    V["X10.P1"] = vec(Ys, apply("P1", st, Ws, 3, unit(3)))
    c2, W2, Y2 = (None, 0), frozenset({0, 1}), frozenset({0})
    for r in ("erase", "double", "fixed_e2"):
        V["X11." + r] = vec(Y2, apply(r, c2, W2, 1, unit(1)))
    return V


def par_desc(par, c, m):
    """c is a proper descendant of m."""
    return m in ancestors(par, c)


def enum_sequences(par, W, Y, pre, out):
    if W == Y:
        out.append(list(pre))
        return
    for l in sorted(W - Y):
        if is_carrier(par, W - {l}):
            pre.append(l)
            enum_sequences(par, W - {l}, Y, pre, out)
            pre.pop()


def solve_triangular():
    depths = set()
    for n in range(1, 8):
        for par in trees(n):
            W = frozenset(range(n))
            for l in range(1, n):
                if not children_in(par, W, l):
                    depths.add(depth(par, l))
    K = max(depths)
    assert sorted(depths) == list(range(1, K + 1))
    # equations: for each k, sum_{d<=k} w_d = 1 ; forward substitution
    w = []
    for k in range(1, K + 1):
        w.append(F(1) - sum(w))
    return w, sorted(depths)


# ---------- U16: every pair, every sequence ----------
def u16():
    st = {"trees": 0, "pairs": 0, "sequences": 0, "nontrivial": 0, "multi_max": 0, "multi_fiber": 0, "multi_order": 0,
          "lemma_states": 0, "viol": 0}
    for r in DFS_RULES:
        st["oi_" + r] = 0; st["eq_" + r] = 0; st["neq_" + r] = 0
    lines = []
    for n in range(1, 8):
        for par in trees(n):
            st["trees"] += 1
            X = frozenset(range(n))
            for Y in carriers(par):
                st["pairs"] += 1
                r = [lp(par, Y, v) for v in range(n)]
                D = X - Y
                maximal = sorted(m for m in D if not any(m in ancestors(par, c) for c in D))
                leavesD = sorted(m for m in D if not children_in(par, X, m))
                remov = sorted(m for m in D if is_carrier(par, X - {m}) and Y <= X - {m})
                if not (maximal == leavesD == remov):
                    st["viol"] += 1
                finals = {ru: set() for ru in DFS_RULES}
                cnt = [0]

                def dfs(W, imgs):
                    if W == Y:
                        cnt[0] += 1
                        for ru in DFS_RULES:
                            finals[ru].add(tuple(tuple(sorted(imgs[ru][v].items())) for v in range(n)))
                        return
                    nxt = []
                    for l in sorted(W - Y):
                        st["lemma_states"] += 1
                        pc = is_carrier(par, W - {l})
                        lf = l != 0 and not children_in(par, W, l)
                        if pc != lf:
                            st["viol"] += 1
                        if pc:
                            nxt.append(l)
                    if not nxt:
                        st["viol"] += 1
                        return
                    for l in nxt:
                        new = {}
                        for ru in DFS_RULES:
                            t = img(ru, par, W, l)
                            row = []
                            for v in range(n):
                                im = imgs[ru][v]
                                if l in im:
                                    c = im[l]
                                    d = {a: b for a, b in im.items() if a != l}
                                    for a, b in t.items():
                                        d[a] = d.get(a, 0) + c * b
                                    row.append(clean(d))
                                else:
                                    row.append(im)
                            new[ru] = row
                        dfs(W - {l}, new)

                dfs(X, {ru: [{v: F(1)} for v in range(n)] for ru in DFS_RULES})
                st["sequences"] += cnt[0]
                target = tuple(((r[v], F(1)),) for v in range(n))
                oi, eq = [], []
                for ru in DFS_RULES:
                    o = len(finals[ru]) == 1
                    e = o and next(iter(finals[ru])) == target
                    oi.append(o); eq.append(e)
                    st["oi_" + ru] += o; st["eq_" + ru] += e
                    st["neq_" + ru] += (not e)
                if Y != X:
                    st["nontrivial"] += 1
                if len(maximal) >= 2:
                    st["multi_max"] += 1
                if any(r.count(y) >= 3 for y in Y):
                    st["multi_fiber"] += 1
                if cnt[0] >= 2:
                    st["multi_order"] += 1
                lines.append("%s|%s|%d|%s|%s|%s|%s" % (pstr(par), ",".join(map(str, sorted(Y))), cnt[0],
                             ",".join(map(str, maximal)), ",".join(map(str, r)),
                             "".join("1" if b else "0" for b in oi), "".join("1" if b else "0" for b in eq)))
    return st, lines


def u16l():
    st = {"cases": 0, "pos": 0, "neg": 0, "viol": 0}
    lines = []
    for n in range(1, 8):
        for par in trees(n):
            W = frozenset(range(n))
            for l in range(n):
                pc = is_carrier(par, W - {l})
                lf = l != 0 and not children_in(par, W, l)
                st["cases"] += 1
                st["pos" if pc else "neg"] += 1
                st["viol"] += pc != lf
                lines.append("%s|%d|%d|%d" % (pstr(par), l, pc, lf))
    return st, lines


def testset(W, l):
    T = []
    for v in sorted(W):
        T += [unit(v), unit(v, -1), unit(v, 2), lin((1, unit(l)), (1, unit(v))), lin((1, unit(l)), (-1, unit(v)))]
    return T


def u16r():
    res = {}
    lines = []
    inst = []
    for n in range(1, 8):
        for par in trees(n):
            W = frozenset(range(n))
            for l in range(1, n):
                if not children_in(par, W, l):
                    inst.append((par, W, l))
    for ru in PANEL:
        E = {"E1": True, "E2": True, "E3": True, "E4": True, "E5": True, "eqP1": True}
        wseq = {}
        for par, W, l in inst:
            ts = testset(W, l)
            ys = [unit(l), unit(l, -1)]
            Tts = [apply(ru, par, W, l, z) for z in ts]
            Tys = [apply(ru, par, W, l, z) for z in ys]
            if E["E1"]:
                for i, xx in enumerate(ts):
                    for jy, yy in enumerate(ys):
                        for a in (1, -1, 2):
                            for b in (1, -1, 2):
                                lhs = apply(ru, par, W, l, lin((a, xx), (b, yy)))
                                if not eqv(lhs, lin((a, Tts[i]), (b, Tys[jy]))):
                                    E["E1"] = False
                for z, Tz in zip(ts, Tts):
                    if sum(Tz.values()) != sum(z.values()):
                        E["E2"] = False
                    if not eqv(Tz, push(par, W - {l}, z)):
                        E["eqP1"] = False
            else:
                for z, Tz in zip(ts, Tts):
                    if sum(Tz.values()) != sum(z.values()):
                        E["E2"] = False
                    if not eqv(Tz, push(par, W - {l}, z)):
                        E["eqP1"] = False
            for v in W:
                if v != l and not eqv(apply(ru, par, W, l, unit(v)), unit(v)):
                    E["E3"] = False
            Tl = clean(apply(ru, par, W, l, unit(l)))
            a = ancestors(par, l)
            if any(v not in a for v in Tl):
                E["E4"] = False
            for d, an in enumerate(a, start=1):
                c = Tl.get(an, F(0))
                if wseq.setdefault(d, c) != c:
                    E["E5"] = False
        res[ru] = E
        lines.append("%s|%s|%d" % (ru, "".join("1" if E[k] else "0" for k in ("E1", "E2", "E3", "E4", "E5")), E["eqP1"]))
    viol = sum((all(res[ru][k] for k in ("E1", "E2", "E3", "E4", "E5"))) != res[ru]["eqP1"] for ru in PANEL)
    return res, lines, len(inst), viol


def u16p():
    st = {"cases": 0, "ycases": 0, "genesis_moved": 0, "viol": 0}
    lines = []
    for n in range(2, 8):
        for par in trees(n):
            X = frozenset(range(n))
            Ys = carriers(par)
            for l in range(1, n):
                if children_in(par, X, l):
                    continue
                p = par[l]
                for w in (-2, 1, 3):
                    st["cases"] += 1
                    x = {v: F((7 * v + 3) % 11 - 5) for v in range(n)}
                    xq = dict(x); xq[l] += w
                    if sorted(v for v in X if x[v] != xq[v]) != [l]:
                        st["viol"] += 1
                    Tx, Tq = apply("P1", par, X, l, x), apply("P1", par, X, l, xq)
                    if sorted(v for v in X - {l} if Tx[v] != Tq[v]) != [p]:
                        st["viol"] += 1
                    if not eqv(lin((1, Tq), (-1, Tx)), unit(p, w)):
                        st["viol"] += 1
                    if Tx[p] != x[p] + x[l] or Tq[p] != xq[p] + xq[l]:
                        st["viol"] += 1
                    if sum(Tx.values()) != sum(x.values()) or sum(Tq.values()) != sum(xq.values()):
                        st["viol"] += 1
                    G = lin((1, apply("genesis", par, X, l, xq)), (-1, apply("genesis", par, X, l, x)))
                    if sorted(G) != [p]:
                        st["genesis_moved"] += 1
                    for Y in Ys:
                        if l in Y:
                            continue
                        st["ycases"] += 1
                        rl = lp(par, Y, l)
                        d1 = lin((1, push(par, Y, xq)), (-1, push(par, Y, x)))
                        d2 = lin((1, push(par, Y, Tq)), (-1, push(par, Y, Tx)))
                        if not (eqv(d1, unit(rl, w)) and eqv(d2, unit(rl, w)) and lp(par, Y, p) == rl):
                            st["viol"] += 1
                        lines.append("%s|%d|%d|%s|%d" % (pstr(par), l, w, ",".join(map(str, sorted(Y))), rl))
    return st, lines


def u16j():
    st = {"rules": 0, "oi": 0, "e5": 0, "eqp": 0, "viol": 0}
    lines = []
    pairs = []
    for n in range(1, 7):
        for par in trees(n):
            for Y in carriers(par):
                pairs.append((par, Y))
    for j in itertools.product(*[range(1, k + 1) for k in range(1, 6)]):
        st["rules"] += 1
        oi_all, eq_all = True, True
        for par, Y in pairs:
            n = len(par)
            X = frozenset(range(n))
            finals = set()

            def dfs(W, loc):
                if W == Y:
                    finals.add(loc)
                    return
                for l in sorted(W - Y):
                    if l != 0 and not children_in(par, W, l):
                        t = next(iter(img("jump", par, W, l, j)))
                        dfs(W - {l}, tuple(t if a == l else a for a in loc))

            dfs(X, tuple(range(n)))
            if len(finals) != 1:
                oi_all = False
            elif next(iter(finals)) != tuple(lp(par, Y, v) for v in range(n)):
                eq_all = False
        if not oi_all:
            eq_all = False
        # E5 weak on every single pruning of the n<=6 trees
        wseq, e5 = {}, True
        for n in range(2, 7):
            for par in trees(n):
                W = frozenset(range(n))
                for l in range(1, n):
                    if children_in(par, W, l):
                        continue
                    t = img("jump", par, W, l, j)
                    for d, an in enumerate(ancestors(par, l), start=1):
                        c = t.get(an, F(0))
                        if wseq.setdefault(d, c) != c:
                            e5 = False
        st["oi"] += oi_all; st["e5"] += e5; st["eqp"] += eq_all
        if not (e5 == eq_all == (j == (1, 1, 1, 1, 1))):
            st["viol"] += 1
        lines.append("%s|%d|%d|%d" % (",".join(map(str, j)), e5, oi_all, eq_all))
    return st, lines


def digest(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    V = instances()
    s16, l16 = u16()
    sl, ll = u16l()
    rres, lr, ninst, rviol = u16r()
    sp, lpl = u16p()
    sj, lj = u16j()
    U = {"trees": s16["trees"], "pairs": s16["pairs"], "sequences": s16["sequences"], "nontrivial": s16["nontrivial"],
         "multi_max": s16["multi_max"], "multi_fiber": s16["multi_fiber"], "multi_order": s16["multi_order"],
         "lemma_states": s16["lemma_states"], "u16_lines": len(l16), "u16_digest": digest(l16), "u16_viol": s16["viol"],
         "u16l_cases": sl["cases"], "u16l_pos": sl["pos"], "u16l_neg": sl["neg"], "u16l_digest": digest(ll), "u16l_viol": sl["viol"],
         "u16r_instances": ninst, "u16r_digest": digest(lr), "u16r_viol": rviol,
         "u16p_cases": sp["cases"], "u16p_ycases": sp["ycases"], "u16p_genesis_moved": sp["genesis_moved"],
         "u16p_lines": len(lpl), "u16p_digest": digest(lpl), "u16p_viol": sp["viol"],
         "u16j_rules": sj["rules"], "u16j_oi": sj["oi"], "u16j_e5": sj["e5"], "u16j_eqp": sj["eqp"],
         "u16j_digest": digest(lj), "u16j_viol": sj["viol"]}
    for r in DFS_RULES:
        U["oi_" + r], U["eq_" + r], U["neq_" + r] = s16["oi_" + r], s16["eq_" + r], s16["neq_" + r]
    cls = {ru: "".join("1" if rres[ru][k] else "0" for k in ("E1", "E2", "E3", "E4", "E5", "eqP1")) for ru in PANEL}
    cert = {"meta": {"role": "producer", "result_sha256": rsha}, "values": V, "universe": U, "panel": cls}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"universe": U, "panel": cls}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
