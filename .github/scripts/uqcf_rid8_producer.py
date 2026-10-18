"""receiver_identification draft 8 (secs 14-15) freeze: PRODUCER. Pure-Python exact Fractions. Joint retained laws by
brute-force enumeration of every base configuration and the nearest-retained-ancestor pushforward; rests by
convolution of node laws; group arithmetic by explicit modular addition. Preregistration: FREEZE.md in
receiver_identification_d8_review/ (committed before this code)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d8_review")
L3 = [{0: F(1)}, {1: F(1)}, {0: F(1, 2), 1: F(1, 2)}]


def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


# ---------- laws on a group (mod None = Z) ----------
def add(a, b, mod):
    return a + b if mod is None else (a + b) % mod


def conv(p, q, mod=None):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            k = add(a, b, mod)
            out[k] = out.get(k, 0) + x * y
    return {k: v for k, v in out.items() if v != 0}


def shift(p, w, mod=None):
    return {add(a, w, mod): x for a, x in p.items()}


def tv(p, q):
    return sum(abs(p.get(k, 0) - q.get(k, 0)) for k in set(p) | set(q)) / 2


def diffset(A, B, mod=None):
    return {(a - b) if mod is None else (a - b) % mod for a in A for b in B}


def jordan(p0, p1):
    f = {k: p0.get(k, 0) - p1.get(k, 0) for k in set(p0) | set(p1)}
    fp = {k: v for k, v in f.items() if v > 0}
    fm = {k: -v for k, v in f.items() if v < 0}
    return fp, fm


def overlap(fp, fm, rho, mod=None):
    a, b = conv(fp, rho, mod), conv(fm, rho, mod)
    return sum(min(a.get(k, 0), b.get(k, 0)) for k in set(a) | set(b))


def regime(S, Ap, Am, D, mod=None):
    if diffset(S, S, mod) & D == {0}:
        return 1
    return 2 if not (diffset(Ap, Am, mod) & D) else 3


def injective(S, T, mod=None):
    seen = {}
    for s in S:
        for r in T:
            y = add(s, r, mod)
            if y in seen and seen[y] != (s, r):
                return False, (seen[y], (s, r))
            seen[y] = (s, r)
    return True, None


def law_step(p0, w, rho, mod=None):
    """One step at law level. Returns dict of all quantities and violation count."""
    p1 = shift(p0, w, mod)
    tv0 = tv(p0, p1)
    q0, q1 = conv(p0, rho, mod), conv(p1, rho, mod)
    tv1 = tv(q0, q1)
    fp, fm = jordan(p0, p1)
    D = diffset(set(rho), set(rho), mod)
    S = set(p0) | set(p1)
    ov = overlap(fp, fm, rho, mod)
    crit_eq = not (diffset(set(fp), set(fm), mod) & D)
    crit_rec = diffset(S, S, mod) & D == {0}
    inj, wit = injective(S, set(rho), mod)
    v = 0
    v += tv1 > tv0
    v += tv1 != tv0 - ov
    v += (tv1 == tv0) != crit_eq
    v += inj != crit_rec
    if not inj:
        (s, r), (s2, r2) = wit
        v += not (s != s2 and add(s, r, mod) == add(s2, r2, mod))
    if crit_rec:
        v += tv1 != tv0
    return {"p1": p1, "tv0": tv0, "tv1": tv1, "q0": q0, "q1": q1, "ov": ov, "D": D, "S": S,
            "reg": regime(S, set(fp), set(fm), D, mod), "rec": inj, "eq": crit_eq, "viol": v}


# ---------- trees ----------
def trees(nmax):
    out = []
    for n in range(1, nmax + 1):
        for par in itertools.product(*[range(i) for i in range(1, n)]):
            out.append((None,) + par)
    return out


def views(par):
    n = len(par)
    res = []
    for mask in range(1 << n):
        X = {i for i in range(n) if mask >> i & 1}
        if 0 in X and all(par[i] in X for i in X if i):
            res.append(frozenset(X))
    return res


def chains(vs, lmin, lmax):
    vs = sorted(vs, key=lambda x: (-len(x), sorted(x)))
    res = []

    def go(ch):
        if lmin <= len(ch) <= lmax:
            res.append(tuple(ch))
        if len(ch) == lmax:
            return
        for v in vs:
            if v < ch[-1]:
                go(ch + [v])
    for v in vs:
        go([v])
    return res


def nra(par, X, v):
    while v not in X:
        v = par[v]
    return v


def tree_step_data(par, l, w, laws, chain):
    """Brute force: enumerate base configurations of P; push forward to each lifted view."""
    n = len(par)
    e = n
    lpar = tuple(par) + (l,)
    lifts = [frozenset(X | ({e} if l in X else set())) for X in chain]
    supp = [sorted(laws[i]) for i in range(n)]
    joint = [[{}, {}] for _ in chain]          # per step, per history: law of retained tuple
    pair = [[{}, {}] for _ in chain]            # per step k: law of (y_{h_k} at k, y_{h_{k+1}} at k+1)
    holders = [nra(lpar, Xl, e) for Xl in lifts]
    for cfg in itertools.product(*supp):
        pr = F(1)
        for i, g in enumerate(cfg):
            pr *= laws[i][g]
        for H in (0, 1):
            x = list(cfg) + [w if H else 0]
            ys = []
            for k, Xl in enumerate(lifts):
                y = {a: 0 for a in Xl}
                for v in range(n + 1):
                    y[nra(lpar, Xl, v)] += x[v]
                ys.append(y)
                t = tuple(y[a] for a in sorted(Xl))
                joint[k][H][t] = joint[k][H].get(t, 0) + pr
            for k in range(len(chain) - 1):
                t = (ys[k][holders[k]], ys[k + 1][holders[k + 1]])
                pair[k][H][t] = pair[k][H].get(t, 0) + pr
    return lifts, holders, joint, pair


def marg(law, idx):
    out = {}
    for t, p in law.items():
        k = tuple(t[i] for i in idx)
        out[k] = out.get(k, 0) + p
    return out


def m1(law, i):
    return {k[0]: v for k, v in marg(law, [i]).items()}


def fiber(par, X, a):
    return {v for v in range(len(par)) if nra(par, X, v) == a}


def tree_case(par, l, w, laws, chain, stats, lines, tag):
    n = len(par)
    e = n
    lifts, holders, joint, pair = tree_step_data(par, l, w, laws, chain)
    out = []
    for k in range(len(chain) - 1):
        hk, hk1 = holders[k], holders[k + 1]
        Xk, Xk1 = lifts[k], lifts[k + 1]
        ik = sorted(Xk).index(hk)
        ik1 = sorted(Xk1).index(hk1)
        nu_k = m1(joint[k][0], ik)
        Fk = fiber(par, chain[k], hk) if hk != e else set()
        Fk1 = fiber(par, chain[k + 1], hk1) if hk1 != e else set()
        rho = {0: F(1)}
        for v in sorted(Fk1 - Fk):
            rho = conv(rho, laws[v])
        st = law_step(nu_k, w, rho)
        v = st["viol"]
        nu_k1 = m1(joint[k + 1][0], ik1)
        v += nu_k1 != st["q0"]                                   # (a) Lemma 14.0
        v += m1(joint[k + 1][1], ik1) != st["q1"]
        jt = tv(joint[k + 1][0], joint[k + 1][1])
        v += jt != st["tv1"]                                     # (b) Theorem 14.1
        for j in range(len(Xk1)):
            if j != ik1:
                v += tv(m1(joint[k + 1][0], j), m1(joint[k + 1][1], j)) != 0
        v += tv(m1(joint[k][0], ik), m1(joint[k][1], ik)) != st["tv0"]
        # (f) direct recoverability from the joint (old, new) supports of both histories
        mp, rec = {}, True
        for H in (0, 1):
            for (s, y), p in pair[k][H].items():
                if p and mp.setdefault(y, s) != s:
                    rec = False
        v += rec != st["rec"]
        strict = hk1 != hk
        v += hk1 not in Xk1                                      # (h)
        if strict:
            v += hk in Xk1
        stats["viol"] += v
        stats["steps"] += 1
        stats["strict"] += strict
        stats["reg%d" % st["reg"]] += 1
        stats["gpt_case"] += strict and len(rho) > 1 and st["tv1"] == st["tv0"]
        stats["multi"] += st["tv0"] < 1 and sum(len(laws[u]) > 1 for u in Fk) >= 2
        if lines is not None:
            lines.append("%s|%d|%d|%d|%s|%s|%d" % (tag, k + 1, hk, hk1, fs(st["tv0"]), fs(st["tv1"]), st["reg"]))
        out.append(st)
    return holders, out


def chain_str(chain):
    return ";".join(",".join(str(i) for i in sorted(X)) for X in chain)


def par_str(par):
    return ",".join("-" if p is None else str(p) for p in par)


def u14():
    stats = {k: 0 for k in ("viol", "steps", "strict", "reg1", "reg2", "reg3", "gpt_case", "multi", "cases")}
    lines = []
    ts = trees(4)
    for par in ts:
        n = len(par)
        chs = chains(views(par), 2, 3)
        for l in range(n):
            for w in (1, 2):
                for asg in itertools.product(range(3), repeat=n):
                    laws = [L3[i] for i in asg]
                    for ch in chs:
                        tag = "%s|%d|%d|%s|%s" % (par_str(par), l, w, chain_str(ch), "".join(map(str, asg)))
                        tree_case(par, l, w, laws, ch, stats, lines, tag)
                        stats["cases"] += 1
    return len(ts), stats, lines


def lawpair(supp, typ):
    supp = sorted(supp)
    wts = [1] * len(supp) if typ == "u" else list(range(1, len(supp) + 1))
    s = sum(wts)
    return {a: F(x, s) for a, x in zip(supp, wts)}


def subsets(base):
    return [c for r in range(1, len(base) + 1) for c in itertools.combinations(base, r)]


def u15():
    stats = {"cases": 0, "viol": 0, "reg2": 0}
    lines = []
    for G, mod, ws in (("Z", None, range(1, 5)), ("Z5", 5, range(1, 5)), ("Z7", 7, range(1, 7))):
        for S0 in subsets([0, 1, 2]):
            for t0 in ("u", "l"):
                p0 = lawpair(S0, t0)
                for T in subsets([0, 1, 2, 3]):
                    for t in ("u", "l"):
                        rho = lawpair(T, t)
                        for w in ws:
                            st = law_step(p0, w, rho, mod)
                            v = st["viol"]
                            if len(S0) == 1:
                                pred = 1 - sum(min(rho.get(y, 0), rho.get(add(y, -w, mod), 0)) for y in
                                               set(rho) | {add(y, w, mod) for y in rho})
                                v += st["tv1"] != pred
                                v += (st["tv1"] == 1) != ((w if mod is None else w % mod) not in st["D"])
                            stats["viol"] += v
                            stats["cases"] += 1
                            stats["reg2"] += st["reg"] == 2
                            lines.append("%s|%s|%s|%s|%s|%d|%s|%s|%d" % (G, ",".join(map(str, S0)), t0, ",".join(map(str, T)),
                                                                     t, w, fs(st["tv0"]), fs(st["tv1"]), st["reg"]))
    return stats, lines


def two_step(p0, w, r1, r2):
    a = law_step(p0, w, r1)
    b = law_step(a["q0"], w, r2)            # per-step: step-1 laws against rho_2
    rt = conv(r1, r2)
    c = law_step(p0, w, rt)                # cumulative from base
    return a, b, c, rt


def u15m():
    stats = {"cases": 0, "viol": 0, "step_decrease": 0}
    lines = []
    for S0 in subsets([0, 1]):
        p0 = lawpair(S0, "u")
        for w in (1, 2, 3):
            for T1 in subsets([0, 1, 2]):
                for T2 in subsets([0, 1, 2]):
                    r1, r2 = lawpair(T1, "u"), lawpair(T2, "u")
                    a, b, c, rt = two_step(p0, w, r1, r2)
                    v = a["viol"] + b["viol"] + c["viol"]
                    D1, D2 = a["D"], b["D"]
                    v += c["D"] != {x + y for x in D1 for y in D2}
                    v += b["tv1"] != c["tv1"]
                    fp, fm = jordan(p0, a["p1"])
                    v += (c["tv1"] == a["tv0"]) != (not (diffset(set(fp), set(fm)) & {x + y for x in D1 for y in D2}))
                    cum = [a["reg"], c["reg"]]
                    stepr = [a["reg"], b["reg"]]
                    v += cum[1] < cum[0]
                    v += not (a["tv0"] >= a["tv1"] >= c["tv1"])
                    stats["viol"] += v
                    stats["cases"] += 1
                    stats["step_decrease"] += stepr[1] < stepr[0]
                    lines.append("%s|%d|%s|%s|%s|%s|%s" % (",".join(map(str, S0)), w, ",".join(map(str, T1)), ",".join(map(str, T2)),
                                 ",".join(fs(x) for x in (a["tv0"], a["tv1"], c["tv1"])),
                                 ",".join(map(str, cum)), ",".join(map(str, stepr))))
    return stats, lines


def digest(lines):
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def instances():
    V = {}
    dummy = {k: 0 for k in ("viol", "steps", "strict", "reg1", "reg2", "reg3", "gpt_case", "multi")}
    # Y1 GPT counterexample
    par = (None, 0, 1)
    laws = [L3[2], L3[0], L3[0]]
    ch = (frozenset({0, 1, 2}), frozenset({0, 1}), frozenset({0}))
    hs, st = tree_case(par, 2, 2, laws, ch, dummy, None, "")
    _, _, joint, _ = tree_step_data(par, 2, 2, laws, ch)
    V["Y1.holders"] = hs
    V["Y1.tvs"] = [fs(st[0]["tv0"]), fs(st[0]["tv1"]), fs(st[1]["tv1"])]
    lifts = [frozenset(X | ({3} if 2 in X else set())) for X in ch]
    Fk, Fk1 = fiber(par, ch[1], 1), fiber(par, ch[2], 0)
    rho = {0: F(1)}
    for v in sorted(Fk1 - Fk):
        rho = conv(rho, laws[v])
    V["Y1.rest_nondegenerate_last"] = len(rho) > 1
    V["Y1.recoverable_last"] = st[1]["rec"]
    V["Y1.regimes"] = [s["reg"] for s in st]
    # Y2 dilution
    hs, st = tree_case((None, 0), 1, 1, [L3[2], L3[0]], (frozenset({0, 1}), frozenset({0})), dummy, None, "")
    V["Y2.holders"] = hs
    V["Y2.tvs"] = [fs(st[0]["tv0"]), fs(st[0]["tv1"])]
    V["Y2.loss"] = fs(st[0]["tv0"] - st[0]["tv1"])
    V["Y2.overlap"] = fs(st[0]["ov"])
    V["Y2.regime"] = st[0]["reg"]
    # Y3
    s = law_step(lawpair([0, 1], "u"), 10, lawpair([0, 1], "u"))
    V["Y3.tv0"], V["Y3.tv1"], V["Y3.recoverable"], V["Y3.regime"] = fs(s["tv0"]), fs(s["tv1"]), s["rec"], s["reg"]
    V["Y4.tv1"] = fs(law_step({0: F(1)}, 1, lawpair([0, 1, 2, 3], "u"))["tv1"])
    s2 = law_step({0: F(1)}, 2, lawpair([0, 1], "u"), 5)
    s1 = law_step({0: F(1)}, 1, lawpair([0, 1], "u"), 5)
    V["Y5.D"], V["Y5.tv_w2"], V["Y5.tv_w1"] = sorted(s2["D"]), fs(s2["tv1"]), fs(s1["tv1"])
    a, b, c, rt = two_step({0: F(1)}, 3, lawpair([0, 2], "u"), lawpair([0, 1], "u"))
    V["Y6.tvs"] = [fs(a["tv0"]), fs(a["tv1"]), fs(c["tv1"])]
    V["Y6.D_sum"] = sorted({x + y for x in a["D"] for y in b["D"]})
    V["Y6.D_union"] = sorted(a["D"] | b["D"])
    # Y7 correlated control: (y_h, y_b) = (s + b + H, b), b uniform {0,1}, s = 0
    J = [{}, {}]
    for H in (0, 1):
        for bb in (0, 1):
            J[H][(bb + H, bb)] = F(1, 2)
    V["Y7.tv_joint"] = fs(tv(J[0], J[1]))
    V["Y7.tv_holder"] = fs(tv(m1(J[0], 0), m1(J[1], 0)))
    V["Y7.tv_ref"] = fs(tv(m1(J[0], 1), m1(J[1], 1)))
    s_, sp, r, rp = 1, 0, 0, 1
    V["Y8.corrected_pair"] = [[s_, r], [sp, rp]]
    V["Y8.corrected_sums"] = [s_ + r, sp + rp]
    V["Y8.draft7_pair"] = [[s_, rp], [sp, r]]
    V["Y8.draft7_sums"] = [s_ + rp, sp + r]
    a, b, c, rt = two_step({0: F(1)}, 1, lawpair([0, 1], "u"), {0: F(1)})
    V["Y9.per_step_regimes"] = [a["reg"], b["reg"]]
    V["Y9.cumulative_regimes"] = [a["reg"], c["reg"]]
    return V


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    V = instances()
    nt, s14, l14 = u14()
    s15, l15 = u15()
    s15m, l15m = u15m()
    U = {"trees_n4": nt, "u14_cases": s14["cases"], "u14_steps": s14["steps"], "u14_strict": s14["strict"],
         "u14_reg1": s14["reg1"], "u14_reg2": s14["reg2"], "u14_reg3": s14["reg3"], "u14_gpt_case": s14["gpt_case"],
         "u14_multi": s14["multi"], "u14_lines": len(l14), "u14_digest": digest(l14), "u14_viol": s14["viol"],
         "u15_cases": s15["cases"], "u15_reg2": s15["reg2"], "u15_lines": len(l15), "u15_digest": digest(l15), "u15_viol": s15["viol"],
         "u15m_cases": s15m["cases"], "u15m_step_decrease": s15m["step_decrease"], "u15m_lines": len(l15m),
         "u15m_digest": digest(l15m), "u15m_viol": s15m["viol"]}
    cert = {"meta": {"role": "producer", "result_sha256": rsha}, "values": V, "universe": U}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"values": V, "universe": U}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
