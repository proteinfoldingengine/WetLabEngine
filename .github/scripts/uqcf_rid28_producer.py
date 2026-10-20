"""receiver_identification d28 freeze (section 33): PRODUCER. Recursive rooted-subtree enumeration, linear forms over Q,
exact Gaussian elimination for ranks and span equality, support scan, exact table evaluation. Standard library only."""
import hashlib, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review")
FROZEN_RESULT_SHA = "a747459613ab088fb363c583cc6cd5ed4333850b64758b88fbba14fcd50529e4"
TREES = {
    "TM": lambda v: (0, 1, 2) if len(v) == 0 else ((0, 1) if len(v) < 3 else ()),
    "MX": lambda v: {(): (0, 1), (0,): (0,), (0, 0): (0, 1), (1,): (0,)}.get(v, ()),
    "CH": lambda v: (0,) if len(v) < 3 else (),
    "S4": lambda v: {(): (0, 1), (0,): (0,)}.get(v, ()),
}
SYSTEMS = [("TM", 1, "a"), ("TM", 2, "a"), ("TM", 3, "a"), ("MX", 1, "a"), ("MX", 2, "a"), ("MX", 3, "a"),
           ("CH", 1, "a"), ("CH", 2, "a"), ("CH", 3, "a"), ("S4", 1, "alpha"), ("S4", 1, "beta")]
K = ((), ())


def s(v): return "r" + "".join("." + str(i) for i in v)
def key(var): return "A[%s|%s]" % (s(var[0]), s(var[1]))
def meet(x, y):
    n = 0
    while n < min(len(x), len(y)) and x[n] == y[n]: n += 1
    return x[:n]
def at_or_below(x, v): return x[:len(v)] == v


class Tree:
    def __init__(self, kids):
        self.kids = kids
        self.addrs = []
        def rec(v):
            self.addrs.append(v)
            for i in kids(v): rec(v + (i,))
        rec(())
        self.vars = [(v, v[:k]) for v in self.addrs for k in range(len(v) + 1)]
        def subtrees(v):  # rooted subtrees containing v (as lists)
            opts = [[]]
            for i in kids(v):
                u = v + (i,)
                ch = [[]] + subtrees(u)
                opts = [a + b for a in opts for b in ch]
            return [[v] + o for o in opts]
        self.carriers = [frozenset(W) for W in subtrees(())]
        cs = sorted(",".join(sorted(s(x) for x in W)) for W in self.carriers)
        self.digest = hashlib.sha256("\n".join(cs).encode()).hexdigest()

    def ch(self, W, v): return [v + (i,) for i in self.kids(v) if v + (i,) in W]

    def h(self, W, v, z):
        f = {}
        f[(v, meet(v, z))] = f.get((v, meet(v, z)), 0) + 1
        for u in self.ch(W, v):
            f[(u, meet(u, z))] = f.get((u, meet(u, z)), 0) - 1
        return {k: F(c) for k, c in f.items() if c}


def climb(tn, D, kind):
    if kind == "beta": return [(), (1,)]
    return [(0,) * d for d in range(D + 1)]


def norm(f): return tuple(sorted((k, c) for k, c in f.items() if c))


def et_rows(T, cl):
    rows, leafc = set(), []
    for d in range(1, len(cl)):
        a, n = cl[d], 0
        for W in T.carriers:
            if a in W and not T.ch(W, a):
                n += 1
                for v in W:
                    f = dict(T.h(W, v, a))
                    if v == a: f[K] = f.get(K, 0) - 1
                    r = norm(f)
                    if r: rows.add(r)
        leafc.append(n)
    return sorted(rows, key=lambda r: [(key(k), str(c)) for k, c in r]), leafc


def ds_rows(T, cl):
    aD = cl[-1]
    diag = [norm({(cl[d], cl[d]): F(1), K: F(-1)}) for d in range(1, len(cl))]
    side = {}
    for c in T.addrs:
        if at_or_below(aD, c) or at_or_below(c, aD): continue
        side[c] = norm({(c, meet(c, aD)): F(1)})
    return diag, side


def rank(rows):
    basis = []  # (pivot, row dict)
    for r in rows:
        f = dict(r)
        for p, b in basis:
            c = f.get(p)
            if c:
                for k, x in b.items():
                    f[k] = f.get(k, 0) - c * x
                    if not f[k]: del f[k]
        if f:
            p = min(f, key=key)
            c = f[p]
            basis.append((p, {k: x / c for k, x in f.items()}))
    return len(basis)


def ev(form, tab): return sum((c * tab.get(k, F(0)) for k, c in form), F(0))
def evd(fd, tab): return sum((c * tab.get(k, F(0)) for k, c in fd.items()), F(0))


def kid(T, kap=F(1)):
    return {(v, v): (kap if v == () else F(1)) for v in T.addrs}


def et_holds(T, cl, tab):
    kap = tab.get(K, F(0))
    for d in range(1, len(cl)):
        a = cl[d]
        for W in T.carriers:
            if a in W and not T.ch(W, a):
                for v in W:
                    if evd(T.h(W, v, a), tab) != (kap if v == a else 0): return False
    return True


def after_holds(T, cl, tab):
    kap = tab.get(K, F(0))
    for d in range(1, len(cl)):
        a, p = cl[d], cl[d - 1]
        for W in T.carriers:
            if a in W and not T.ch(W, a):
                Y = W - {a}
                for v in Y:
                    if evd(T.h(Y, v, p), tab) != (kap if v == p else 0): return False
    return True


def pos_holds(T, tab):
    for W in sorted(T.carriers, key=len):
        for v in W:
            for z in W:
                if evd(T.h(W, v, z), tab) < 0: return False
    return True


def col(T, W, z, tab, order): return [evd(T.h(W, v, z), tab) for v in order]


def chain(v): return [v[:k] for k in range(len(v) + 1)]


def hashval(var): return F(int(hashlib.sha256(key(var).encode()).hexdigest()[:8], 16) % 7 - 3)


def main(outp):
    trees = {n: Tree(k) for n, k in TREES.items()}
    out = {"role": "producer", "frozen_result_sha256": hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest(),
           "structural": {n: {"carriers": len(T.carriers), "variables": len(T.vars), "carrier_digest": T.digest}
                          for n, T in trees.items()}, "systems": {}, "tables": {}, "instances": {}, "controls": {}}
    viol = 0
    sysdata = {}
    for tn, D, kind in SYSTEMS:
        T = trees[tn]; cl = climb(tn, D, kind)
        name = "%s%s|%d" % (tn, {"a": "", "alpha": "α", "beta": "β"}[kind], D)
        et, leafc = et_rows(T, cl)
        diag, side = ds_rows(T, cl)
        ds = diag + list(side.values())
        rE, rD, rU = rank(et), rank(ds), rank(et + ds)
        supp = sorted({key(k) for r in et for k, _ in r})
        dssupp = sorted({key(k) for r in ds for k, _ in r})
        out["systems"][name] = {"side": len(side), "rank_et": rE, "rank_ds": rD, "rank_union": rU,
                                "span_equal": rE == rD == rU, "support": len(supp), "support_equals_ds_support": supp == dssupp,
                                "leaf_carriers": leafc, "et_rows": len(et), "side_addresses": sorted(s(c) for c in side)}
        sysdata[name] = (T, cl, et, diag, side)
    # X1 Lemma 33.0
    x1 = 0
    for tn, T in trees.items():
        for W in T.carriers:
            for z in W:
                f = {}
                for v in W:
                    for k, c in T.h(W, v, z).items(): f[k] = f.get(k, 0) + c
                f[K] = f.get(K, 0) - 1
                if norm(f): x1 += 1
    out["tables"]["X1"] = {"violations": x1}
    # X2 independence by single perturbations
    x2, inst = 0, {}
    for name in ("TM|3", "MX|3", "CH|3", "S4β|1"):
        T, cl, et, diag, side = sysdata[name]
        ents = [("diag", d) for d in range(1, len(cl))] + [("side", c) for c in sorted(side)]
        for typ, e in ents:
            for eps in (F(1, 2), F(-1)):
                tab = kid(T)
                if typ == "diag":
                    var = (cl[e], cl[e]); tab[var] = F(1) + eps
                else:
                    var = (e, meet(e, cl[-1])); tab[var] = eps
                others = [r for r in diag + list(side.values()) if r != norm({var: F(1), K: F(-1)}) and r != norm({var: F(1)})]
                ok = all(ev(r, tab) == 0 for r in others) and not all(ev(r, tab) == 0 for r in et)
                if typ == "side":
                    i = len(meet(e, cl[-1])) if name != "S4β|1" else 0
                    W = frozenset(chain(cl[i + 1]) + chain(e))
                    w = evd(T.h(W, e, cl[i + 1]), tab); ok &= w == eps
                else:
                    W = frozenset(chain(cl[e])); w = evd(T.h(W, cl[e - 1], cl[e]), tab); ok &= w == -eps
                if name == "TM|3" and typ == "side" and e == (0, 0, 1) and eps == F(1, 2): inst["Y2"] = str(w)
                if name == "TM|3" and typ == "diag" and e == 2 and eps == F(-1): inst["Y3"] = str(w)
                x2 += 0 if ok else 1
    out["tables"]["X2"] = {"violations": x2}
    # X3 leak on TM|3
    T, cl, et, diag, side = sysdata["TM|3"]; x3 = 0
    for m in range(3):
        u = cl[m] + (1,)
        for t in (F(-2), F(-1, 2), F(1, 2), F(1), F(3)):
            tab = kid(T); tab[(cl[m + 1], cl[m])] = t
            ok = et_holds(T, cl, tab) and after_holds(T, cl, tab) and not pos_holds(T, tab)
            if t > 0:
                w = evd(T.h(frozenset(chain(cl[m + 1]) + [u]), cl[m], u), tab); ok &= w == -t
                if m == 1 and t == F(1, 2): inst["Y4"] = str(w)
            else:
                ok &= evd(T.h(frozenset(chain(cl[m + 1])), cl[m + 1], cl[m]), tab) == t
            W = frozenset(chain(cl[m + 1]))
            ok &= any(evd(T.h(W, v, cl[m]), tab) != (1 if v == cl[m] else 0) for v in W)
            x3 += 0 if ok else 1
    out["tables"]["X3"] = {"violations": x3}
    # X4 MX scope
    T, cl, et, diag, side = sysdata["MX|3"]; x4 = 0
    for t in (F(1, 2), F(1), F(-1, 2), F(3, 2)):
        tab = kid(T); tab[((0, 0), (0,))] = t
        p = pos_holds(T, tab)
        ok = (p == (0 <= t <= 1)) and et_holds(T, cl, tab)
        W = frozenset(chain((0, 0)))
        ok &= any(evd(T.h(W, v, (0,)), tab) != (1 if v == (0,) else 0) for v in W)
        if t == 1: inst["Y5"] = [str(x) for x in col(T, W, (0,), tab, [(), (0,), (0, 0)])]
        x4 += 0 if ok else 1
    out["tables"]["X4"] = {"violations": x4}
    # X5 general tables
    x5 = 0
    for name in ("TM|1", "TM|2", "TM|3", "MX|3", "CH|3", "S4α|1"):
        T, cl, et, diag, side = sysdata[name]
        dsv = {(cl[d], cl[d]) for d in range(1, len(cl))} | {(c, meet(c, cl[-1])) for c in side}
        for kap in (F(1), F(2), F(-1), F(0)):
            tab = {}
            for var in T.vars:
                if var == K: tab[var] = kap
                elif var in dsv: tab[var] = kap if var[0] == var[1] else F(0)
                else: tab[var] = hashval(var)
            x5 += 0 if (et_holds(T, cl, tab) and after_holds(T, cl, tab)) else 1
    out["tables"]["X5"] = {"violations": x5}
    # X6 S4 table
    T = trees["S4"]
    tab6 = {((), ()): F(1), ((0,), ()): F(0), ((0,), (0,)): F(1), ((0, 0), ()): F(1), ((0, 0), (0,)): F(0),
            ((0, 0), (0, 0)): F(1), ((1,), ()): F(0), ((1,), (1,)): F(1)}
    S_fails = any(tab6[(v, w)] != 0 for (v, w) in T.vars if w != v)
    _, cla, eta, diaga, sidea = sysdata["S4α|1"]
    _, clb, etb, diagb, sideb = sysdata["S4β|1"]
    leafa = sorted(sorted(s(x) for x in W) for W in T.carriers if (0,) in W and not T.ch(W, (0,)))
    okA = all(ev(r, tab6) == 0 for r in diaga + list(sidea.values())) and et_holds(T, cla, tab6) and \
        leafa == [["r", "r.0"], ["r", "r.0", "r.1"]]
    okB = (not all(ev(r, tab6) == 0 for r in sideb.values())) and not et_holds(T, clb, tab6)
    full = frozenset(T.addrs)
    inst["Y1"] = [str(x) for x in col(T, full, (1,), tab6, [(), (0,), (0, 0), (1,)])]
    out["tables"]["X6"] = {"violations": 0 if (S_fails and okA and okB) else 1}
    out["instances"] = dict(sorted(inst.items()))
    # controls
    def rej(b): return "REJECTED" if b else "ACCEPTED"
    T, cl, et, diag, side = sysdata["TM|2"]
    out["controls"]["R1"] = rej(rank(diag + et) > rank(diag))
    sk = list(side.values()) + [norm({K: F(1)})]
    out["controls"]["R2"] = rej(rank(sk + et) > rank(sk))
    T, cl, et, diag, side = sysdata["TM|3"]
    out["controls"]["R3"] = rej(key(((0,), ())) not in {key(k) for r in et for k, _ in r})
    out["controls"]["R4"] = rej(S_fails)
    out["controls"]["R5"] = rej(not et_holds(trees["S4"], clb, tab6))
    T, cl, et, diag, side = sysdata["MX|3"]
    sm = diag + [r for c, r in side.items() if c != (0, 0, 1)]
    out["controls"]["R6"] = rej(rank(sm + et) > rank(sm))
    T, cl, et, diag, side = sysdata["TM|3"]
    tab = kid(T); tab[((0,), ())] = F(1, 2)
    out["controls"]["R7"] = rej(not pos_holds(T, tab))
    tab = kid(T); tab[((0, 0, 1), (0, 0))] = F(1, 2)
    out["controls"]["R8"] = rej(not et_holds(T, cl, tab))
    T = trees["MX"]; tab = kid(T); tab[((0, 0), (0,))] = F(3, 2)
    out["controls"]["R9"] = rej(not pos_holds(T, tab))
    out["violations"] = x1 + x2 + x3 + x4 + x5 + out["tables"]["X6"]["violations"]
    Path(outp).write_text(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print("producer violations", out["violations"])


if __name__ == "__main__":
    main(sys.argv[1])
