"""receiver_identification draft 5 (secs 11-13) freeze: PRODUCER.
Pure-Python exact Fractions; nearest-ancestor walk; joint laws by brute-force product enumeration and dict pushforward.
Computes the preregistered exact instances (FREEZE.md section 2) and exhaustive universes U12, U114, U13 (section 3)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d5_review")
L3 = [{0: F(1)}, {1: F(1)}, {0: F(1, 2), 1: F(1, 2)}]


def trees(n):
    for ps in itertools.product(*[range(i) for i in range(1, n)]):
        yield (None,) + ps


def views(par):
    n = len(par)
    out = set()
    def grow(cur, frontier):
        out.add(frozenset(cur))
        for i, c in enumerate(frontier):
            kids = [z for z in range(n) if par[z] == c]
            grow(cur | {c}, frontier[i + 1:] + kids)
    grow({0}, [z for z in range(n) if par[z] == 0])
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def histories(par, maxlen):
    vs = views(par)
    out = []
    def ext(ch):
        if ch:
            out.append(list(ch))
        if len(ch) == maxlen:
            return
        for v in vs:
            if not ch or (v < ch[-1]):
                ext(ch + [v])
    ext([])
    return out


def nra(par, keep, z):
    while z not in keep:
        z = par[z]
    return z


def depth(par, z):
    d = 0
    while par[z] is not None:
        z = par[z]; d += 1
    return d


def lift(V, apps):
    L = set(V)
    for node, parent in apps:
        if parent in V:
            L.add(node)
    return frozenset(L)


def push(par, keep, x):
    y = {a: 0 for a in keep}
    for z, v in enumerate(x):
        y[nra(par, keep, z)] += v
    return y


def tv(p, q):
    return sum(abs(p.get(k, 0) - q.get(k, 0)) for k in set(p) | set(q)) / 2


def conv(p, q):
    o = {}
    for i, a in p.items():
        for j, b in q.items():
            o[i + j] = o.get(i + j, 0) + a * b
    return o


def joint(par, keep, laws, xe):
    ks = sorted(keep)
    out = {}
    for xs in itertools.product(*[sorted(l.items()) for l in laws]):
        x = [v for v, _ in xs] + [xe]
        p = F(1)
        for _, q in xs:
            p *= q
        y = push(par, keep, x)
        key = tuple(y[k] for k in ks)
        out[key] = out.get(key, 0) + p
    return out


def marg(law, idx):
    o = {}
    for k, v in law.items():
        kk = tuple(k[i] for i in idx)
        o[kk] = o.get(kk, 0) + v
    return o


def s(v):
    return str(F(v))


def fmtv(V):
    return ",".join(map(str, sorted(V)))


def instances():
    V = {}
    par = (None, 0, 1, 2)
    y1s, y0s, hs, ds, dp = [], [], [], [], []
    for X in [{0, 1, 2}, {0, 1}, {0}]:
        L = lift(X, [(3, 2)])
        a, b = push(par, L, [1, 0, 1, 1]), push(par, L, [1, 0, 1, 0])
        y1s.append([str(a[k]) for k in sorted(L)]); y0s.append([str(b[k]) for k in sorted(L)])
        d = [k for k in sorted(L) if a[k] != b[k]]
        hs.append(d[0]); ds.append(str(a[d[0]] - b[d[0]])); dp.append(depth(par, d[0]))
    V["X1.y1"], V["X1.y0"], V["X1.holders"], V["X1.diffs"], V["X1.depths"] = y1s, y0s, hs, ds, dp
    par = (None, 0, 0, 1, 3)
    HA = [nra(par, lift(X, [(4, 3)]), 4) for X in [{0, 1, 3}, {0, 1}]]
    HB = [nra(par, lift(X, [(4, 3)]), 4) for X in [{0, 1, 2}, {0, 1}]]
    V["X2.holders_A"], V["X2.holders_B"], V["X2.final_equal"] = HA, HB, HA[-1] == HB[-1]
    L = lift({0, 1, 2}, [(4, 3)])
    cor = []
    for a in sorted(L):
        z, ok = 4, False
        path = []
        while z is not None:
            if z == a:
                ok = all(p not in L for p in path); break
            path.append(z); z = par[z]
        if ok:
            cor.append(a)
    V["X2.cor125_B1"] = cor
    par = (None, 0, 0, 1, 2)
    pairs, merge = [], None
    tot = True
    for k, X in enumerate([{0, 1, 2}, {0, 1}, {0}], 1):
        L = lift(X, [(3, 1), (4, 2)])
        a, b = push(par, L, [0, 0, 0, 1, 0]), push(par, L, [0, 0, 0, 0, 1])
        tot = tot and sum(a.values()) == sum(b.values())
        plus = [z for z in sorted(L) if a[z] - b[z] == 1]; minus = [z for z in sorted(L) if a[z] - b[z] == -1]
        if plus:
            pairs.append([plus[0], minus[0]])
        else:
            pairs.append([])
            if merge is None:
                merge = k
    V["X3.pairs"], V["X3.merge_step"], V["X3.totals_equal"] = pairs, merge, tot
    par = (None, 0, 1)
    laws = [L3[0], L3[2]]
    L = lift({0}, [(2, 1)])
    l1, l0 = joint(par, L, laws, 1), joint(par, L, laws, 0)
    nu = conv(laws[0], laws[1])
    V["X4.holder"] = nra(par, L, 2); V["X4.tv"] = s(tv(l0, l1)); V["X4.max_nu"] = s(max(nu.values()))
    V["X4.helstrom_success"] = s(sum(max(l0.get(k, 0), l1.get(k, 0)) for k in set(l0) | set(l1)) / 2)
    tdist = V["X4.tv"]
    # explicit matrices on the retained configuration basis; pinching = sum_j P_j rho P_j, P_j = 1{y_h = j}
    basis = sorted(set(l0) | set(l1)); hi = sorted(L).index(V["X4.holder"])
    pinch = True
    for lw in (l0, l1):
        rho = [[lw.get(b, F(0)) if i == j else F(0) for j, b in enumerate(basis)] for i, b in enumerate(basis)]
        out = [[F(0)] * len(basis) for _ in basis]
        for g in sorted({b[hi] for b in basis}):
            P = [1 if b[hi] == g else 0 for b in basis]
            for i in range(len(basis)):
                for j in range(len(basis)):
                    out[i][j] += P[i] * rho[i][j] * P[j]
        pinch = pinch and out == rho
    L = lift({0, 1}, [(2, 1)])
    l1, l0 = joint(par, L, laws, 1), joint(par, L, laws, 0)
    ks = sorted(L)
    V["X5.holder"] = nra(par, L, 2); V["X5.tv"] = s(tv(l0, l1)); V["X5.tv_addr1"] = s(tv(marg(l0, [ks.index(1)]), marg(l1, [ks.index(1)])))
    j0 = {(0, 0): F(1, 2), (1, 1): F(1, 2)}; j1 = {(1, 0): F(1, 2), (2, 1): F(1, 2)}
    V["X6.tv_joint"] = s(tv(j0, j1)); V["X6.tv_holder"] = s(tv(marg(j0, [0]), marg(j1, [0]))); V["X6.tv_ref"] = s(tv(marg(j0, [1]), marg(j1, [1])))
    V["X7.pinch_fixed"] = pinch; V["X7.trace_distance"] = tdist
    return V


def u12():
    C = dict(u12_cases=0, u12_steps=0, u12_strict=0, u12_h_ne_e=0, u12_viol=0)
    lines = []
    for n in range(1, 6):
        for par0 in trees(n):
            hs_all = histories(par0, 3)
            for l in range(n):
                par = par0 + (l,); e = n
                for ch in hs_all:
                    line_h = None
                    for w in (1, 2):
                        for xP in itertools.product((0, 1), repeat=n):
                            C["u12_cases"] += 1
                            x1 = list(xP) + [w]; x0 = list(xP) + [0]
                            prevL, prevh, comp = None, None, e
                            hs = []
                            for k, X in enumerate(ch):
                                L = lift(X, [(e, l)])
                                C["u12_steps"] += 1
                                a, b = push(par, L, x1), push(par, L, x0)
                                d = [z for z in sorted(L) if a[z] != b[z]]
                                h = nra(par, L, e)
                                comp = nra(par, L, comp)
                                ok = d == [h] and a[h] - b[h] == w and comp == h
                                if prevh is not None:
                                    if prevh in L:
                                        ok = ok and h == prevh
                                    else:
                                        anc = []
                                        z = par[prevh]
                                        while z is not None:
                                            anc.append(z); z = par[z]
                                        ok = ok and h in anc and depth(par, h) < depth(par, prevh)
                                        C["u12_strict"] += 1
                                for aa in L:
                                    z, crit, path = e, False, []
                                    while z is not None:
                                        if z == aa:
                                            crit = all(p not in L for p in path); break
                                        path.append(z); z = par[z]
                                    ok = ok and (crit == (aa == h))
                                for v in range(n):
                                    ok = ok and nra(par, L, v) == nra(par0, X, v)
                                if h != e:
                                    C["u12_h_ne_e"] += 1
                                if not ok:
                                    C["u12_viol"] += 1
                                prevh = h; hs.append(h)
                            line_h = hs
                    pstr = ",".join("-" if p is None else str(p) for p in par0)
                    lines.append(pstr + "|" + str(l) + "|" + ";".join(fmtv(X) for X in ch) + "|" + ",".join(map(str, line_h)))
    lines.sort()
    C["u12_lines"] = len(lines)
    C["u12_digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return C


def u114():
    C = dict(u114_cases=0, u114_steps=0, u114_merged=0, u114_unmerged=0, u114_viol=0)
    lines = []
    for n in range(1, 6):
        for par0 in trees(n):
            hs_all = histories(par0, 3)
            for l in range(n):
                for lp in range(n):
                    if lp == l:
                        continue
                    par = par0 + (l, lp); e, ep = n, n + 1
                    for ch in hs_all:
                        rec = None
                        for base in (0, 1):
                            C["u114_cases"] += 1
                            xa = [base] * n + [1, 0]; xb = [base] * n + [0, 1]
                            merged, steps = False, []
                            for X in ch:
                                L = lift(X, [(e, l), (ep, lp)])
                                C["u114_steps"] += 1
                                a, b = push(par, L, xa), push(par, L, xb)
                                he, hep = nra(par, L, e), nra(par, L, ep)
                                d = {z: a[z] - b[z] for z in L if a[z] != b[z]}
                                ok = sum(a.values()) == sum(b.values())
                                if he == hep:
                                    ok = ok and d == {}
                                    merged = True; C["u114_merged"] += 1; steps.append("-")
                                else:
                                    ok = ok and d == {he: 1, hep: -1} and not merged
                                    C["u114_unmerged"] += 1; steps.append(str(he) + ":" + str(hep))
                                for z in L:
                                    ok = ok and ((z in d) == ((he == z) != (hep == z)))
                                if not ok:
                                    C["u114_viol"] += 1
                            rec = steps
                        pstr = ",".join("-" if p is None else str(p) for p in par0)
                        lines.append(pstr + "|" + str(l) + "|" + str(lp) + "|" + ";".join(fmtv(X) for X in ch) + "|" + ";".join(rec))
    lines.sort()
    C["u114_lines"] = len(lines)
    C["u114_digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return C


def u13():
    C = dict(u13_steps=0, u13_tv_lt1=0, u13_h_ne_e=0, u13_multi=0, u13_attained=0, u13_viol=0)
    lines = []
    for n in range(1, 5):
        for par0 in trees(n):
            hs_all = histories(par0, 2)
            for l in range(n):
                par = par0 + (l,); e = n
                for w in (1, 2):
                    for ch in hs_all:
                        for asg in itertools.product(range(3), repeat=n):
                            laws = [L3[i] for i in asg]
                            for k, X in enumerate(ch, 1):
                                L = lift(X, [(e, l)]); ks = sorted(L)
                                C["u13_steps"] += 1
                                l1, l0 = joint(par, L, laws, w), joint(par, L, laws, 0)
                                h = nra(par, L, e); hi = ks.index(h)
                                fib = [v for v in range(n) if nra(par, L, v) == h]
                                nu = {0: F(1)}
                                for v in fib:
                                    nu = conv(nu, laws[v])
                                nus = {i + w: p for i, p in nu.items()}
                                ok = True
                                for y in set(l0) | set(l1):
                                    ok = ok and l1.get(y, 0) * nu.get(y[hi], 0) == l0.get(y, 0) * nus.get(y[hi], 0)
                                T = tv(l0, l1)
                                ok = ok and T == tv(nu, nus) and T >= max(nu.values())
                                if len(nu) == 1:
                                    ok = ok and T == 1
                                for r in range(1, len(ks)):
                                    for S in itertools.combinations(range(len(ks)), r):
                                        t = tv(marg(l0, S), marg(l1, S))
                                        ok = ok and (t == T if hi in S else t == 0)
                                succ = sum((l1.get(y, 0) if nus.get(y[hi], 0) > nu.get(y[hi], 0) else l0.get(y, 0)) for y in set(l0) | set(l1)) / 2
                                ok = ok and succ == (1 + T) / 2
                                if T < 1:
                                    C["u13_tv_lt1"] += 1
                                if h != e:
                                    C["u13_h_ne_e"] += 1
                                if sum(1 for v in fib if asg[v] == 2) >= 2:
                                    C["u13_multi"] += 1
                                if T == max(nu.values()):
                                    C["u13_attained"] += 1
                                if not ok:
                                    C["u13_viol"] += 1
                                pstr = ",".join("-" if p is None else str(p) for p in par0)
                                lines.append("|".join([pstr, str(l), str(w), ";".join(fmtv(X) for X in ch), ",".join(map(str, asg)), str(k), str(h), s(T)]))
    lines.sort()
    C["u13_lines"] = len(lines)
    C["u13_digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return C


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    U = {}
    U.update(u12()); U.update(u114()); U.update(u13())
    U["trees_n5"] = sum(1 for n in range(1, 6) for _ in trees(n)); U["trees_n4"] = sum(1 for n in range(1, 5) for _ in trees(n))
    cert = {"meta": {"role": "producer", "result_sha256": rsha, "algorithm": "pure-Python Fractions, nearest-ancestor walk, brute-force product enumeration"},
            "values": instances(), "universe": U}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps(cert["universe"], indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
