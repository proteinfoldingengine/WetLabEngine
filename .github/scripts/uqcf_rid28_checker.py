"""receiver_identification d28 freeze (section 33): CHECKER. Independent of the producer (does not import it). BFS address
indexing, bitmask carriers built by parent-closed extension, its own holding function, the proof certificates of Theorem 33.1
in both directions verified identically over Q, independence by single-entry perturbation tables (Proposition 33.2(a)),
support by scan, and certificate tables for the span controls. Standard library only."""
import hashlib, json, sys
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review")
CHILDREN = {
    "TM": {(): 3, **{(a,): 2 for a in range(3)}, **{(a, b): 2 for a in range(3) for b in range(2)}},
    "MX": {(): 2, (0,): 1, (0, 0): 2, (1,): 1},
    "CH": {(): 1, (0,): 1, (0, 0): 1},
    "S4": {(): 2, (0,): 1},
}
GEN = ((), ())


def name_of(v): return "r" + "".join("." + str(i) for i in v)
def vkey(p): return "A[" + name_of(p[0]) + "|" + name_of(p[1]) + "]"
def lca(x, y):
    i = 0
    for a, b in zip(x, y):
        if a != b: break
        i += 1
    return x[:i]
def desc(x, v): return len(x) >= len(v) and x[:len(v)] == v


class Tr:
    def __init__(self, nm):
        cm = CHILDREN[nm]
        self.A = [()]
        q = [()]
        while q:
            v = q.pop(0)
            for i in range(cm.get(v, 0)):
                self.A.append(v + (i,)); q.append(v + (i,))
        self.ix = {v: i for i, v in enumerate(self.A)}
        self.kids = {v: [v + (i,) for i in range(cm.get(v, 0))] for v in self.A}
        masks = [1]
        for i, v in enumerate(self.A[1:], 1):
            pb = 1 << self.ix[v[:-1]]
            masks = masks + [m | (1 << i) for m in masks if m & pb]
        self.masks = sorted(masks)
        self.nvars = sum(len(v) + 1 for v in self.A)
        strs = sorted(",".join(sorted(name_of(v) for v in self.members(m))) for m in self.masks)
        self.digest = hashlib.sha256("\n".join(strs).encode()).hexdigest()

    def members(self, m): return [v for v in self.A if m >> self.ix[v] & 1]
    def inW(self, m, v): return bool(m >> self.ix[v] & 1)
    def cin(self, m, v): return [u for u in self.kids[v] if self.inW(m, u)]
    def mask(self, vs):
        m = 0
        for v in vs: m |= 1 << self.ix[v]
        return m

    def hold(self, m, v, z):
        f = {(v, lca(v, z)): Q(1)}
        for u in self.cin(m, v):
            k = (u, lca(u, z)); f[k] = f.get(k, Q(0)) - 1
        return {k: c for k, c in f.items() if c != 0}


def add(f, g, s=1):
    r = dict(f)
    for k, c in g.items():
        r[k] = r.get(k, Q(0)) + s * c
        if r[k] == 0: del r[k]
    return r


def canon(f): return tuple(sorted((vkey(k), str(c)) for k, c in f.items() if c != 0))
def val(f, t): return sum((c * t.get(k, Q(0)) for k, c in f.items()), Q(0))
def anc(v): return [v[:i] for i in range(len(v) + 1)]


def system(T, cl):
    aD = cl[-1]
    onclimb = set(cl)
    side = {c: {(c, lca(c, aD)): Q(1)} for c in T.A if c not in onclimb and not desc(c, aD)}
    diag = {d: {(cl[d], cl[d]): Q(1), GEN: Q(-1)} for d in range(1, len(cl))}
    return diag, side


def et_forms(T, cl):
    out, leaf = [], []
    for d in range(1, len(cl)):
        a, n = cl[d], 0
        for m in T.masks:
            if T.inW(m, a) and not T.cin(m, a):
                n += 1
                for v in T.members(m):
                    f = T.hold(m, v, a)
                    if v == a: f = add(f, {GEN: Q(1)}, -1)
                    out.append((d, m, v, f))
        leaf.append(n)
    return out, leaf


def certify_iii_to_i(T, cl, diag, side, d, m, v, f):
    """The combination written in the proof of Theorem 33.1, (iii) => (i)."""
    D0 = lambda i: diag[i] if i >= 1 else {}
    if v == cl[d]: g = dict(diag[d])
    elif v in cl[:d]:
        i = cl.index(v)
        g = add(D0(i), D0(i + 1), -1)
        for u in T.cin(m, v):
            if u != cl[i + 1]: g = add(g, side[u], -1)
    else:
        g = dict(side[v])
        for u in T.cin(m, v): g = add(g, side[u], -1)
    return canon(g) == canon(f)


def et_ok(T, cl, t):
    k = t.get(GEN, Q(0))
    for d in range(1, len(cl)):
        a = cl[d]
        for m in T.masks:
            if T.inW(m, a) and not T.cin(m, a):
                for v in T.members(m):
                    if val(T.hold(m, v, a), t) != (k if v == a else 0): return False
    return True


def after_ok(T, cl, t):
    k = t.get(GEN, Q(0))
    for d in range(1, len(cl)):
        a, p = cl[d], cl[d - 1]
        for m in T.masks:
            if T.inW(m, a) and not T.cin(m, a):
                y = m & ~(1 << T.ix[a])
                for v in T.members(y):
                    if val(T.hold(y, v, p), t) != (k if v == p else 0): return False
    return True


def pos_ok(T, t):
    for m in T.masks:
        mem = T.members(m)
        for z in mem:
            for v in mem:
                if val(T.hold(m, v, z), t) < 0: return False
    return True


def ident(T, kap=Q(1)):
    t = {(v, v): Q(1) for v in T.A}; t[GEN] = kap
    return t


def main(outp):
    trees = {n: Tr(n) for n in CHILDREN}
    rep = {"role": "checker", "frozen_result_sha256": hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest(),
           "structural": {n: {"carriers": len(T.masks), "variables": T.nvars, "carrier_digest": T.digest} for n, T in trees.items()},
           "systems": {}, "tables": {}, "instances": {}, "controls": {}}
    bad = 0
    S = {}
    specs = [("TM", d, "") for d in (1, 2, 3)] + [("MX", d, "") for d in (1, 2, 3)] + [("CH", d, "") for d in (1, 2, 3)] + \
            [("S4", 1, "α"), ("S4", 1, "β")]
    for tn, D, tag in specs:
        T = trees[tn]
        cl = [(), (1,)] if tag == "β" else [(0,) * i for i in range(D + 1)]
        nm = tn + tag + "|" + str(D)
        diag, side = system(T, cl)
        forms, leaf = et_forms(T, cl)
        distinct = {canon(f) for _, _, _, f in forms if f}
        # (iii) => (i): every ET form is the proof's combination of Diag and Side rows
        c1 = sum(0 if certify_iii_to_i(T, cl, diag, side, d, m, v, f) else 1 for d, m, v, f in forms)
        # (i) => (iii): Diag_d = -sum_j ET(h_{a_{j-1}}(e_{a_j}) on [0, a_j]); Side_c = ET(h_c(e_{a_{i+1}}) on [0,a_{i+1}] u [0,c])
        etset = {(d, m, v): f for d, m, v, f in forms}
        c2 = 0
        for d in diag:
            g = {}
            for j in range(1, d + 1):
                mj = T.mask(anc(cl[j]))
                if (j, mj, cl[j - 1]) not in etset: c2 += 1; continue
                g = add(g, etset[(j, mj, cl[j - 1])], -1)
            c2 += 0 if canon(g) == canon(diag[d]) else 1
        for c in side:
            i = len(lca(c, cl[-1]))
            mc = T.mask(set(anc(cl[i + 1])) | set(anc(c)))
            f = etset.get((i + 1, mc, c))
            c2 += 0 if (f is not None and canon(f) == canon(side[c])) else 1
        # independence: each row violated alone (Proposition 33.2(a) tables)
        c3 = 0
        rows = [("d", d, r) for d, r in diag.items()] + [("s", c, r) for c, r in side.items()]
        for typ, e, r in rows:
            t = ident(T)
            k = next(iter(x for x in r if x != GEN))
            t[k] = t.get(k, Q(0)) + Q(1, 2)
            if val(r, t) == 0 or any(val(r2, t) != 0 for typ2, e2, r2 in rows if (typ2, e2) != (typ, e)): c3 += 1
        bad += c1 + c2 + c3
        ok = c1 == c2 == c3 == 0
        n = len(rows)
        supp = sorted({vkey(k) for _, _, _, f in forms for k in f})
        dss = sorted({vkey(k) for _, _, r in rows for k in r})
        rep["systems"][nm] = {"side": len(side), "rank_et": n if ok else -1, "rank_ds": n if c3 == 0 else -1,
                              "rank_union": n if ok else -1, "span_equal": ok, "support": len(supp),
                              "support_equals_ds_support": supp == dss, "leaf_carriers": leaf, "et_rows": len(distinct),
                              "side_addresses": sorted(name_of(c) for c in side)}
        S[nm] = (T, cl, diag, side, forms)
    # X1
    x1 = 0
    for T in trees.values():
        for m in T.masks:
            mem = T.members(m)
            for z in mem:
                g = {GEN: Q(-1)}
                for v in mem: g = add(g, T.hold(m, v, z))
                x1 += 1 if g else 0
    rep["tables"]["X1"] = {"violations": x1}
    inst = {}
    # X2
    x2 = 0
    for nm in ("TM|3", "MX|3", "CH|3", "S4β|1"):
        T, cl, diag, side, forms = S[nm]
        for typ, e in [("d", d) for d in diag] + [("s", c) for c in side]:
            for eps in (Q(1, 2), Q(-1)):
                t = ident(T)
                if typ == "d":
                    t[(cl[e], cl[e])] = 1 + eps
                    m = T.mask(anc(cl[e])); w = val(T.hold(m, cl[e - 1], cl[e]), t); good = w == -eps
                else:
                    i = len(lca(e, cl[-1])); t[(e, cl[i])] = eps
                    m = T.mask(set(anc(cl[i + 1])) | set(anc(e))); w = val(T.hold(m, e, cl[i + 1]), t); good = w == eps
                others = [r for d2, r in diag.items() if not (typ == "d" and d2 == e)] + \
                         [r for c2, r in side.items() if not (typ == "s" and c2 == e)]
                good &= all(val(r, t) == 0 for r in others) and not et_ok(T, cl, t)
                if nm == "TM|3" and typ == "s" and e == (0, 0, 1) and eps == Q(1, 2): inst["Y2"] = str(w)
                if nm == "TM|3" and typ == "d" and e == 2 and eps == -1: inst["Y3"] = str(w)
                x2 += 0 if good else 1
    rep["tables"]["X2"] = {"violations": x2}
    # X3
    T, cl, diag, side, forms = S["TM|3"]; x3 = 0
    for mm in range(3):
        u = cl[mm] + (1,)
        for t_ in (Q(-2), Q(-1, 2), Q(1, 2), Q(1), Q(3)):
            t = ident(T); t[(cl[mm + 1], cl[mm])] = t_
            good = et_ok(T, cl, t) and after_ok(T, cl, t) and not pos_ok(T, t)
            if t_ > 0:
                w = val(T.hold(T.mask(anc(cl[mm + 1]) + [u]), cl[mm], u), t); good &= w == -t_
                if mm == 1 and t_ == Q(1, 2): inst["Y4"] = str(w)
            else:
                good &= val(T.hold(T.mask(anc(cl[mm + 1])), cl[mm + 1], cl[mm]), t) == t_
            m = T.mask(anc(cl[mm + 1]))
            good &= val(T.hold(m, cl[mm + 1], cl[mm]), t) != 0
            x3 += 0 if good else 1
    rep["tables"]["X3"] = {"violations": x3}
    # X4
    T, cl, diag, side, forms = S["MX|3"]; x4 = 0
    for t_ in (Q(1, 2), Q(1), Q(-1, 2), Q(3, 2)):
        t = ident(T); t[((0, 0), (0,))] = t_
        good = pos_ok(T, t) == (Q(0) <= t_ <= Q(1)) and et_ok(T, cl, t)
        m = T.mask(anc((0, 0)))
        good &= val(T.hold(m, (0, 0), (0,)), t) != 0
        if t_ == 1: inst["Y5"] = [str(val(T.hold(m, v, (0,)), t)) for v in [(), (0,), (0, 0)]]
        x4 += 0 if good else 1
    rep["tables"]["X4"] = {"violations": x4}
    # X5
    x5 = 0
    for nm in ("TM|1", "TM|2", "TM|3", "MX|3", "CH|3", "S4α|1"):
        T, cl, diag, side, forms = S[nm]
        fixed = {(a, a) for a in cl[1:]} | {(c, lca(c, cl[-1])) for c in side}
        for kap in (Q(1), Q(2), Q(-1), Q(0)):
            t = {}
            for v in T.A:
                for w in anc(v):
                    p = (v, w)
                    if p == GEN: t[p] = kap
                    elif p in fixed: t[p] = kap if v == w else Q(0)
                    else: t[p] = Q(int(hashlib.sha256(vkey(p).encode()).hexdigest()[:8], 16) % 7 - 3)
            x5 += 0 if (et_ok(T, cl, t) and after_ok(T, cl, t)) else 1
    rep["tables"]["X5"] = {"violations": x5}
    # X6
    T = trees["S4"]
    t6 = {((), ()): Q(1), ((0,), (0,)): Q(1), ((0, 0), ()): Q(1), ((0, 0), (0, 0)): Q(1), ((1,), (1,)): Q(1)}
    s_fails = any(t6.get((v, w), 0) != 0 for v in T.A for w in anc(v)[:-1])
    _, cla, diaga, sidea, _ = S["S4α|1"]; _, clb, diagb, sideb, _ = S["S4β|1"]
    leafa = sorted(sorted(name_of(v) for v in T.members(m)) for m in T.masks if T.inW(m, (0,)) and not T.cin(m, (0,)))
    okA = all(val(r, t6) == 0 for r in list(diaga.values()) + list(sidea.values())) and et_ok(T, cla, t6) and \
        leafa == [["r", "r.0"], ["r", "r.0", "r.1"]]
    okB = any(val(r, t6) != 0 for r in sideb.values()) and not et_ok(T, clb, t6)
    full = T.mask(T.A)
    inst["Y1"] = [str(val(T.hold(full, v, (1,)), t6)) for v in [(), (0,), (0, 0), (1,)]]
    rep["tables"]["X6"] = {"violations": 0 if (s_fails and okA and okB) else 1}
    rep["instances"] = dict(sorted(inst.items()))
    R = lambda b: "REJECTED" if b else "ACCEPTED"
    T, cl, diag, side, forms = S["TM|2"]
    t = ident(T); t[(min(side), lca(min(side), cl[-1]))] = Q(1)  # satisfies Diag, violates ET
    rep["controls"]["R1"] = R(all(val(r, t) == 0 for r in diag.values()) and not et_ok(T, cl, t))
    t = {(cl[1], cl[1]): Q(1)}  # satisfies Side and kappa = 0, violates ET
    rep["controls"]["R2"] = R(all(val(r, t) == 0 for r in side.values()) and t.get(GEN, 0) == 0 and not et_ok(T, cl, t))
    T, cl, diag, side, forms = S["TM|3"]
    rep["controls"]["R3"] = R(all(((0,), ()) not in f for _, _, _, f in forms))
    rep["controls"]["R4"] = R(s_fails)
    rep["controls"]["R5"] = R(not et_ok(trees["S4"], clb, t6))
    T, cl, diag, side, forms = S["MX|3"]
    t = ident(T); t[((0, 0, 1), (0, 0))] = Q(1)
    rep["controls"]["R6"] = R(all(val(r, t) == 0 for r in list(diag.values()) + [r for c, r in side.items() if c != (0, 0, 1)])
                              and not et_ok(T, cl, t))
    T, cl, diag, side, forms = S["TM|3"]
    t = ident(T); t[((0,), ())] = Q(1, 2)
    rep["controls"]["R7"] = R(not pos_ok(T, t))
    t = ident(T); t[((0, 0, 1), (0, 0))] = Q(1, 2)
    rep["controls"]["R8"] = R(not et_ok(T, cl, t))
    T = trees["MX"]; t = ident(T); t[((0, 0), (0,))] = Q(3, 2)
    rep["controls"]["R9"] = R(not pos_ok(T, t))
    rep["violations"] = bad + x1 + x2 + x3 + x4 + x5 + rep["tables"]["X6"]["violations"]
    Path(outp).write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print("checker violations", rep["violations"])


if __name__ == "__main__":
    main(sys.argv[1])
