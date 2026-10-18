"""receiver_identification draft 8 (secs 14-15) freeze: CHECKER. Independent of the producer: bitmask views, numpy
integer-weight joint laws pushed forward by retraction matrices, rests recovered EMPIRICALLY from the joint law of
(old holder value, new holder value) with an exact independence test, numpy integer convolutions, outer-difference
support tests. Also bounded random evidence and the preregistered rejecting controls. Preregistration: FREEZE.md in
receiver_identification_d8_review/ (committed before this code)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d8_review")
L3W = [np.array([2, 0]), np.array([0, 2]), np.array([1, 1])]   # weights over {0,1}, denominator 2


def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def trim(a):
    a = np.asarray(a, dtype=np.int64)
    nz = np.nonzero(a)[0]
    return a[: nz[-1] + 1] if len(nz) else a[:1]


def pad(a, L):
    out = np.zeros(L, dtype=np.int64)
    out[: len(a)] = a
    return out


def eqv(a, b):
    a, b = trim(a), trim(b)
    return len(a) == len(b) and bool((a == b).all())


def eqn(a, b):
    """equality of the normalized laws of two integer weight vectors"""
    a, b = trim(a), trim(b)
    return eqv(a * int(b.sum()), b * int(a.sum()))


def tvw(a, b):
    """TV of two integer weight vectors on {0,1,...} (any total), returned as Fraction."""
    L = max(len(a), len(b))
    A, B = pad(a, L), pad(b, L)
    ta, tb = int(A.sum()), int(B.sum())
    return F(int(np.abs(A * tb - B * ta).sum()), 2 * ta * tb)


def shiftw(a, w, mod=None):
    if mod is None:
        return np.concatenate([np.zeros(w, dtype=np.int64), a])
    out = np.zeros(mod, dtype=np.int64)
    for i, x in enumerate(a):
        out[(i + w) % mod] += x
    return out


def convw(a, b, mod=None):
    c = np.convolve(np.asarray(a, dtype=np.int64), np.asarray(b, dtype=np.int64))
    if mod is None:
        return c
    out = np.zeros(mod, dtype=np.int64)
    np.add.at(out, np.arange(len(c)) % mod, c)
    return out


def supp(a):
    return np.nonzero(np.asarray(a))[0]


def dset(A, B, mod=None):
    d = np.subtract.outer(np.asarray(A), np.asarray(B)).ravel()
    return set((d % mod if mod else d).tolist())


def classify(p0w, w, rw, mod=None):
    """p0w, rw integer weights (index = group element). Returns quantities and violations."""
    L = (mod if mod else len(p0w) + w + len(rw))
    p0 = pad(p0w, L) if mod is None else pad(p0w, mod)
    p1 = pad(shiftw(np.asarray(p0w), w, mod), L)
    T0 = int(p0.sum())
    tv0 = tvw(p0, p1)
    q0, q1 = convw(p0, rw, mod), convw(p1, rw, mod)
    tv1 = tvw(q0, q1)
    f = p0 - p1
    fp, fm = np.where(f > 0, f, 0), np.where(f < 0, -f, 0)
    cp, cm = convw(fp, rw, mod), convw(fm, rw, mod)
    Lc = max(len(cp), len(cm))
    ov = F(int(np.minimum(pad(cp, Lc), pad(cm, Lc)).sum()), T0 * int(np.asarray(rw).sum()))
    T = supp(rw)
    D = dset(T, T, mod)
    S = np.union1d(supp(p0), supp(p1))
    eq = not (dset(supp(fp), supp(fm), mod) & D)
    crit_rec = dset(S, S, mod) & D == {0}
    sums = np.add.outer(S, T).ravel()
    if mod:
        sums = sums % mod
    direct_rec = len(np.unique(sums)) == len(sums)
    v = 0
    v += tv1 > tv0
    v += tv1 != tv0 - ov
    v += (tv1 == tv0) != eq
    v += direct_rec != crit_rec
    if not direct_rec:   # corrected D8 witness: (s, r), (s', r') with s - s' = r' - r
        found = False
        for s in S:
            for s2 in S:
                if s == s2:
                    continue
                for r in T:
                    r2 = r + s - s2
                    if mod:
                        r2 %= mod
                    if r2 in set(T.tolist()):
                        a1 = (s + r) % mod if mod else s + r
                        a2 = (s2 + r2) % mod if mod else s2 + r2
                        found |= a1 == a2
        v += not found
    if crit_rec:
        v += tv1 != tv0
    if crit_rec:
        reg = 1
    else:
        reg = 2 if eq else 3
    return {"tv0": tv0, "tv1": tv1, "q0": q0, "D": D, "rec": direct_rec, "reg": reg, "viol": v, "ov": ov}


# ---------------- trees by bitmask ----------------
def gen_trees(nmax):
    out, frontier = [], [(None,)]
    while frontier:
        out.extend(frontier)
        nxt = []
        for t in frontier:
            if len(t) < nmax:
                for p in range(len(t)):
                    nxt.append(t + (p,))
        frontier = nxt
    return out


def view_masks(par):
    n = len(par)
    pm = [0] + [1 << par[i] for i in range(1, n)]
    return [m for m in range(1 << n) if m & 1 and all((m >> i & 1) == 0 or (m & pm[i]) for i in range(1, n))]


def chain_masks(vm, lo, hi):
    res = []

    def go(ch):
        if lo <= len(ch) <= hi:
            res.append(list(ch))
        if len(ch) < hi:
            for m in vm:
                if m & ch[-1] == m and m != ch[-1]:
                    go(ch + [m])
    for m in vm:
        go([m])
    return res


def anc_map(lpar, mask):
    def up(v):
        while not mask >> v & 1:
            v = lpar[v]
        return v
    return [up(v) for v in range(len(lpar))]


def tree_case(par, l, w, lawsw, chain, stats, lines, tag):
    """lawsw: list of integer weight vectors (common total per node)."""
    n = len(par)
    e = n
    lpar = list(par) + [l]
    lifts = [m | ((1 << e) if m >> l & 1 else 0) for m in chain]
    grids = np.array(list(itertools.product(*[range(len(x)) for x in lawsw])), dtype=np.int64).reshape(-1, n)
    wts = np.ones(len(grids), dtype=object)
    for i in range(n):
        wts = wts * np.array([int(lawsw[i][g]) for g in grids[:, i]], dtype=object)
    keep = np.array([x != 0 for x in wts])
    grids, wts = grids[keep], np.array([int(x) for x in wts[keep]], dtype=np.int64)
    full = [np.hstack([grids, np.full((len(grids), 1), w * H, dtype=np.int64)]) for H in (0, 1)]
    Y, hold, addrs = [], [], []
    for m in lifts:
        am = anc_map(lpar, m)
        ad = [a for a in range(n + 1) if m >> a & 1]
        M = np.zeros((n + 1, len(ad)), dtype=np.int64)
        for v in range(n + 1):
            M[v, ad.index(am[v])] = 1
        Y.append([full[H] @ M for H in (0, 1)])
        hold.append(am[e])
        addrs.append(ad)
    total = int(wts.sum())

    def lawrows(rows, weights):
        u, inv = np.unique(rows, axis=0, return_inverse=True)
        return {tuple(r): int(c) for r, c in zip(u.tolist(), np.bincount(inv.ravel(), weights=weights).astype(np.int64).tolist()) if c}

    def tvd(a, b):
        ks = set(a) | set(b)
        return F(sum(abs(a.get(k, 0) - b.get(k, 0)) for k in ks), 2 * total)

    def vecw(col):
        return trim(np.bincount(col, weights=wts, minlength=1).astype(np.int64))

    out = []
    for k in range(len(chain) - 1):
        hk, hk1 = hold[k], hold[k + 1]
        ik, ik1 = addrs[k].index(hk), addrs[k + 1].index(hk1)
        old = [Y[k][H][:, ik] for H in (0, 1)]
        new = [Y[k + 1][H][:, ik1] for H in (0, 1)]
        v = 0
        # empirical rest and exact independence test in each history
        rws = []
        for H in (0, 1):
            r = new[H] - old[H]
            v += int((r < 0).sum())
            r = np.maximum(r, 0)
            jo = np.zeros((old[H].max() + 1, r.max() + 1), dtype=np.int64)
            np.add.at(jo, (old[H], r), wts)
            mo, mr = jo.sum(1), jo.sum(0)
            v += int((jo * total != np.outer(mo, mr)).any())
            rws.append(trim(mr))
        v += not eqn(rws[0], rws[1])
        rw = rws[0]
        p0w = vecw(old[0])
        st = classify(p0w, w, rw)
        v += st["viol"]
        v += tvw(vecw(old[0]), vecw(old[1])) != st["tv0"]
        v += tvw(vecw(new[0]), vecw(new[1])) != st["tv1"]
        v += not eqn(vecw(new[0]), st["q0"])
        J = [lawrows(Y[k + 1][H], wts) for H in (0, 1)]
        v += tvd(J[0], J[1]) != st["tv1"]
        for j in range(len(addrs[k + 1])):
            if j != ik1:
                v += tvw(vecw(Y[k + 1][0][:, j]), vecw(Y[k + 1][1][:, j])) != 0
        mp = {}
        rec = True
        for H in (0, 1):
            for s, y in set(zip(old[H].tolist(), new[H].tolist())):
                if mp.setdefault(y, s) != s:
                    rec = False
        v += rec != st["rec"]
        strict = hk1 != hk
        v += not lifts[k + 1] >> hk1 & 1
        if strict:
            v += bool(lifts[k + 1] >> hk & 1)
        fib = [u for u in range(n) if anc_map(lpar, lifts[k])[u] == hk]
        stats["viol"] += v
        stats["steps"] += 1
        stats["strict"] += strict
        stats["reg%d" % st["reg"]] += 1
        stats["gpt_case"] += strict and len(supp(rw)) > 1 and st["tv1"] == st["tv0"]
        stats["multi"] += st["tv0"] < 1 and sum(int((np.asarray(lawsw[u]) > 0).sum()) > 1 for u in fib) >= 2
        stats["tv_increase"] += st["tv1"] > st["tv0"]
        if lines is not None:
            lines.append("%s|%d|%d|%d|%s|%s|%d" % (tag, k + 1, hk, hk1, fs(st["tv0"]), fs(st["tv1"]), st["reg"]))
        out.append((hk, hk1, st, rw))
    return hold, out


def mstr(m, n):
    return ",".join(str(i) for i in range(n) if m >> i & 1)


def newstats():
    return {k: 0 for k in ("viol", "steps", "strict", "reg1", "reg2", "reg3", "gpt_case", "multi", "cases", "tv_increase")}


def u14():
    st, lines = newstats(), []
    ts = gen_trees(4)
    for par in ts:
        n = len(par)
        chs = chain_masks(view_masks(par), 2, 3)
        ps = ",".join("-" if p is None else str(p) for p in par)
        for l in range(n):
            for w in (1, 2):
                for asg in itertools.product(range(3), repeat=n):
                    lw = [L3W[i] for i in asg]
                    for ch in chs:
                        tag = "%s|%d|%d|%s|%s" % (ps, l, w, ";".join(mstr(m, n) for m in ch), "".join(map(str, asg)))
                        tree_case(par, l, w, lw, ch, st, lines, tag)
                        st["cases"] += 1
    return len(ts), st, lines


def lw(sup, typ):
    a = np.zeros(max(sup) + 1, dtype=np.int64)
    for j, s in enumerate(sorted(sup)):
        a[s] = 1 if typ == "u" else j + 1
    return a


def subs(base):
    return [list(c) for r in range(1, len(base) + 1) for c in itertools.combinations(base, r)]


def u15():
    st, lines = {"cases": 0, "viol": 0, "reg2": 0}, []
    for G, mod, ws in (("Z", None, range(1, 5)), ("Z5", 5, range(1, 5)), ("Z7", 7, range(1, 7))):
        for S0 in subs([0, 1, 2]):
            for t0 in "ul":
                for T in subs([0, 1, 2, 3]):
                    for t in "ul":
                        for w in ws:
                            p, r = lw(S0, t0), lw(T, t)
                            c = classify(p, w, r, mod)
                            v = c["viol"]
                            if len(S0) == 1:
                                rr = pad(r, (mod or 0) + len(r) + w + 1) if mod is None else pad(r, mod)
                                sh = shiftw(r, w, mod)
                                L = max(len(rr), len(sh))
                                pred = 1 - F(int(np.minimum(pad(rr, L), pad(sh, L)).sum()), int(r.sum()))
                                v += c["tv1"] != pred
                                v += (c["tv1"] == 1) != ((w % mod if mod else w) not in c["D"])
                            st["viol"] += v
                            st["cases"] += 1
                            st["reg2"] += c["reg"] == 2
                            lines.append("%s|%s|%s|%s|%s|%d|%s|%s|%d" % (G, ",".join(map(str, S0)), t0, ",".join(map(str, T)), t, w,
                                                                     fs(c["tv0"]), fs(c["tv1"]), c["reg"]))
    return st, lines


def twostep(p, w, r1, r2):
    a = classify(p, w, r1)
    b = classify(trim(a["q0"]), w, r2)
    c = classify(p, w, trim(convw(r1, r2)))
    return a, b, c


def u15m():
    st, lines = {"cases": 0, "viol": 0, "step_decrease": 0, "tv_increase": 0}, []
    for S0 in subs([0, 1]):
        p = lw(S0, "u")
        for w in (1, 2, 3):
            for T1 in subs([0, 1, 2]):
                for T2 in subs([0, 1, 2]):
                    r1, r2 = lw(T1, "u"), lw(T2, "u")
                    a, b, c = twostep(p, w, r1, r2)
                    v = a["viol"] + b["viol"] + c["viol"]
                    Dsum = {x + y for x in a["D"] for y in b["D"]}
                    v += c["D"] != Dsum
                    v += b["tv1"] != c["tv1"]
                    pp = pad(p, len(p) + w)
                    f = pp - shiftw(p, w)
                    v += (c["tv1"] == a["tv0"]) != (not (dset(supp(np.where(f > 0, f, 0)), supp(np.where(f < 0, -f, 0))) & Dsum))
                    cum, stp = [a["reg"], c["reg"]], [a["reg"], b["reg"]]
                    v += cum[1] < cum[0]
                    v += not (a["tv0"] >= a["tv1"] >= c["tv1"])
                    st["tv_increase"] += (a["tv1"] > a["tv0"]) + (c["tv1"] > a["tv1"])
                    st["viol"] += v
                    st["cases"] += 1
                    st["step_decrease"] += stp[1] < stp[0]
                    lines.append("%s|%d|%s|%s|%s|%s|%s" % (",".join(map(str, S0)), w, ",".join(map(str, T1)), ",".join(map(str, T2)),
                                 ",".join(fs(x) for x in (a["tv0"], a["tv1"], c["tv1"])), ",".join(map(str, cum)), ",".join(map(str, stp))))
    return st, lines


def instances():
    V, dummy = {}, newstats()
    hs, o = tree_case((None, 0, 1), 2, 2, [L3W[2], L3W[0], L3W[0]], [0b111, 0b011, 0b001], dummy, None, "")
    V["Y1.holders"] = hs
    V["Y1.tvs"] = [fs(o[0][2]["tv0"]), fs(o[0][2]["tv1"]), fs(o[1][2]["tv1"])]
    V["Y1.rest_nondegenerate_last"] = len(supp(o[1][3])) > 1
    V["Y1.recoverable_last"] = o[1][2]["rec"]
    V["Y1.regimes"] = [x[2]["reg"] for x in o]
    hs, o = tree_case((None, 0), 1, 1, [L3W[2], L3W[0]], [0b11, 0b01], dummy, None, "")
    s = o[0][2]
    V["Y2.holders"], V["Y2.tvs"] = hs, [fs(s["tv0"]), fs(s["tv1"])]
    V["Y2.loss"], V["Y2.overlap"], V["Y2.regime"] = fs(s["tv0"] - s["tv1"]), fs(s["ov"]), s["reg"]
    c = classify(lw([0, 1], "u"), 10, lw([0, 1], "u"))
    V["Y3.tv0"], V["Y3.tv1"], V["Y3.recoverable"], V["Y3.regime"] = fs(c["tv0"]), fs(c["tv1"]), c["rec"], c["reg"]
    V["Y4.tv1"] = fs(classify(np.array([1]), 1, lw([0, 1, 2, 3], "u"))["tv1"])
    c2, c1 = classify(np.array([1]), 2, lw([0, 1], "u"), 5), classify(np.array([1]), 1, lw([0, 1], "u"), 5)
    V["Y5.D"], V["Y5.tv_w2"], V["Y5.tv_w1"] = sorted(c2["D"]), fs(c2["tv1"]), fs(c1["tv1"])
    a, b, c = twostep(np.array([1]), 3, lw([0, 2], "u"), lw([0, 1], "u"))
    V["Y6.tvs"] = [fs(a["tv0"]), fs(a["tv1"]), fs(c["tv1"])]
    V["Y6.D_sum"] = sorted({x + y for x in a["D"] for y in b["D"]})
    V["Y6.D_union"] = sorted(a["D"] | b["D"])
    # Y7: joint over (y_h, y_b) as 3x2 weight tables
    J0 = np.array([[1, 0], [0, 1], [0, 0]]); J1 = np.array([[0, 0], [1, 0], [0, 1]])
    V["Y7.tv_joint"] = fs(F(int(np.abs(J0 - J1).sum()), 4))
    V["Y7.tv_holder"] = fs(tvw(J0.sum(1), J1.sum(1)))
    V["Y7.tv_ref"] = fs(tvw(J0.sum(0), J1.sum(0)))
    S, T = [0, 1], [0, 1]
    corr = [[s, r, s2, r2] for s in S for s2 in S for r in T for r2 in T if s == 1 and s2 == 0 and s - s2 == r2 - r]
    s, r, s2, r2 = corr[0]
    V["Y8.corrected_pair"], V["Y8.corrected_sums"] = [[s, r], [s2, r2]], [s + r, s2 + r2]
    V["Y8.draft7_pair"], V["Y8.draft7_sums"] = [[s, r2], [s2, r]], [s + r2, s2 + r]
    a, b, c = twostep(np.array([1]), 1, lw([0, 1], "u"), np.array([1]))
    V["Y9.per_step_regimes"], V["Y9.cumulative_regimes"] = [a["reg"], b["reg"]], [a["reg"], c["reg"]]
    return V, o


def bounded():
    rng = np.random.default_rng(20261018)
    st = newstats()
    cases = 0
    while cases < 1500:
        n = int(rng.integers(5, 7))
        par = (None,) + tuple(int(rng.integers(0, i)) for i in range(1, n))
        l = int(rng.integers(0, n))
        w = int(rng.integers(1, 4))
        laws = []
        for _ in range(n):
            cut = np.sort(rng.integers(0, 5, size=2))
            laws.append(trim(np.array([cut[0], cut[1] - cut[0], 4 - cut[1]], dtype=np.int64)))
        vm = view_masks(par)
        m = (1 << n) - 1 if rng.random() < 0.5 else int(rng.choice(vm))
        ch = [m]
        steps = int(rng.integers(2, 5))
        while len(ch) < steps:
            sub = [x for x in vm if x & ch[-1] == x and x != ch[-1]]
            if not sub:
                break
            ch.append(int(rng.choice(sub)))
        if len(ch) < 2:
            continue
        tree_case(par, l, w, laws, ch, st, None, "")
        cases += 1
    return cases, st


def controls(V):
    C = {}
    # R1: "TV preserved exactly when rho is a point mass": Y1 last step has nondegenerate rho and preserved TV
    C["R1_preserve_iff_point_mass"] = "REJECTED" if (V["Y1.rest_nondegenerate_last"] and V["Y1.tvs"][1] == V["Y1.tvs"][2]) else "ACCEPTED"
    C["R2_unrecoverable_if_nondegenerate"] = "REJECTED" if (V["Y1.rest_nondegenerate_last"] and V["Y1.recoverable_last"]) else "ACCEPTED"
    C["R3_draft7_witness_collides"] = "REJECTED" if V["Y8.draft7_sums"][0] != V["Y8.draft7_sums"][1] else "ACCEPTED"
    C["R4_preserved_implies_recoverable"] = "REJECTED" if (V["Y3.tv0"] == V["Y3.tv1"] and not V["Y3.recoverable"]) else "ACCEPTED"
    p = V["Y9.per_step_regimes"]
    C["R5_per_step_regime_monotone"] = "REJECTED" if p[1] < p[0] else "ACCEPTED"
    C["R6_holder_sufficient_correlated_after_climb"] = "REJECTED" if V["Y7.tv_joint"] != V["Y7.tv_holder"] else "ACCEPTED"
    union_predicts_no_loss = 3 not in V["Y6.D_union"]
    C["R7_union_instead_of_sumset"] = "REJECTED" if (union_predicts_no_loss and V["Y6.tvs"][2] != "1") else "ACCEPTED"
    return C


def digest(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    V, _ = instances()
    nt, s14, l14 = u14()
    s15, l15 = u15()
    s15m, l15m = u15m()
    bc, bs = bounded()
    C = controls(V)
    C["R8_tv_restored_by_later_step"] = "REJECTED" if (s14["tv_increase"] == 0 and s15m["tv_increase"] == 0 and bs["tv_increase"] == 0) else "ACCEPTED"
    U = {"trees_n4": nt, "u14_cases": s14["cases"], "u14_steps": s14["steps"], "u14_strict": s14["strict"],
         "u14_reg1": s14["reg1"], "u14_reg2": s14["reg2"], "u14_reg3": s14["reg3"], "u14_gpt_case": s14["gpt_case"],
         "u14_multi": s14["multi"], "u14_lines": len(l14), "u14_digest": digest(l14), "u14_viol": s14["viol"],
         "u15_cases": s15["cases"], "u15_reg2": s15["reg2"], "u15_lines": len(l15), "u15_digest": digest(l15), "u15_viol": s15["viol"],
         "u15m_cases": s15m["cases"], "u15m_step_decrease": s15m["step_decrease"], "u15m_lines": len(l15m),
         "u15m_digest": digest(l15m), "u15m_viol": s15m["viol"]}
    B = {"B14_cases": bc, "B14_viol": bs["viol"], "B14_steps": bs["steps"], "B14_strict": bs["strict"],
         "B14_reg2": bs["reg2"], "B14_reg3": bs["reg3"], "B14_gpt_case": bs["gpt_case"]}
    cert = {"meta": {"role": "checker", "result_sha256": rsha}, "values": V, "universe": U, "bounded": B, "controls": C}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"universe": U, "bounded": B, "controls": C}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
