"""receiver_identification draft 5 (secs 11-13) freeze: CHECKER (independent of the producer; does not import it).
Bitmask ancestor-closed views, deepest-retained-ancestor via ancestor bitmasks, numpy 0/1 retraction matrices composed by
matrix product, joint laws by sequential state-space dynamic programming over nodes, Helstrom via numpy eigen-decomposition.
Also bounded randomized evidence (seed 20261018) and the preregistered rejecting controls."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d5_review")
L3 = [((0, F(1)),), ((1, F(1)),), ((0, F(1, 2)), (1, F(1, 2)))]


def all_trees(n):
    if n == 1:
        yield (None,)
        return
    for t in all_trees(n - 1):
        for p in range(n - 1):
            yield t + (p,)


def anc_masks(par):
    n = len(par); m = [0] * n
    for i in range(n):
        z, mk = i, 0
        while z is not None:
            mk |= 1 << z; z = par[z]
        m[i] = mk  # ancestors-or-self
    return m


def closed_masks(par):
    n = len(par); am = anc_masks(par)
    return [m for m in range(1, 1 << n) if m & 1 and all((am[i] & m) == am[i] for i in range(n) if m >> i & 1)]


def chains(cm, maxlen):
    out = []
    def go(ch):
        if ch:
            out.append(tuple(ch))
        if len(ch) == maxlen:
            return
        for m in cm:
            if not ch or (m != ch[-1] and (m & ch[-1]) == m):
                go(ch + [m])
    go([])
    return out


def popl(m):
    return bin(m).count("1")


def deepest(am, m, z):
    cands = am[z] & m
    return max((i for i in range(len(am)) if cands >> i & 1), key=lambda i: popl(am[i]))


def liftm(m, apps):
    for node, parent in apps:
        if m >> parent & 1:
            m |= 1 << node
    return m


def members(m, n):
    return [i for i in range(n) if m >> i & 1]


def rmat(am, frm, to, n):
    """0/1 matrix (rows: members of `to`, cols: members of `frm`) of the retraction."""
    fr, tt = members(frm, n), members(to, n)
    M = np.zeros((len(tt), len(fr)), dtype=np.int64)
    for j, z in enumerate(fr):
        M[tt.index(deepest(am, to, z)), j] = 1
    return M


def tvf(p, q):
    return sum(abs(p.get(k, F(0)) - q.get(k, F(0))) for k in set(p) | set(q)) / 2


def dp_law(owners, laws, ret, extra):
    """owners[v] = index in ret; laws[v] = tuple of (value, prob); extra = (index, value) or None."""
    st = {tuple([0] * len(ret)): F(1)}
    for v, law in enumerate(laws):
        nst = {}
        for key, p in st.items():
            for val, q in law:
                kk = list(key); kk[owners[v]] += val; kk = tuple(kk)
                nst[kk] = nst.get(kk, F(0)) + p * q
        st = nst
    if extra is not None:
        st = {tuple(k[i] + (extra[1] if i == extra[0] else 0) for i in range(len(k))): p for k, p in st.items()}
    return st


def margf(law, S):
    o = {}
    for k, v in law.items():
        kk = tuple(k[i] for i in S); o[kk] = o.get(kk, F(0)) + v
    return o


def fr(v):
    return str(F(v))


def mstr(m, n):
    return ",".join(map(str, members(m, n)))


def instances():
    V = {}
    # X1
    par = (None, 0, 1, 2); n = 4; am = anc_masks(par)
    full = (1 << n) - 1
    y1s, y0s, hs, ds, dp = [], [], [], [], []
    for X in [0b0111, 0b0011, 0b0001]:
        Lm = liftm(X, [(3, 2)]); M = rmat(am, full, Lm, n)
        a, b = M @ np.array([1, 0, 1, 1]), M @ np.array([1, 0, 1, 0])
        y1s.append([str(int(v)) for v in a]); y0s.append([str(int(v)) for v in b])
        idx = [i for i in range(len(a)) if a[i] != b[i]]; h = members(Lm, n)[idx[0]]
        hs.append(h); ds.append(str(int(a[idx[0]] - b[idx[0]]))); dp.append(popl(am[h]) - 1)
    V["X1.y1"], V["X1.y0"], V["X1.holders"], V["X1.diffs"], V["X1.depths"] = y1s, y0s, hs, ds, dp
    # X2
    par = (None, 0, 0, 1, 3); n = 5; am = anc_masks(par)
    def hold(ch):
        return [deepest(am, liftm(X, [(4, 3)]), 4) for X in ch]
    HA, HB = hold([0b01011, 0b00011]), hold([0b00111, 0b00011])
    V["X2.holders_A"], V["X2.holders_B"], V["X2.final_equal"] = HA, HB, HA[-1] == HB[-1]
    Lm = liftm(0b00111, [(4, 3)])
    cor = [a for a in members(Lm, n) if (am[4] >> a & 1) and ((am[4] & ~am[a] & ~(1 << a)) | 0) & Lm == 0 and True]
    # path from e up to a excluding a = am[e] minus am[a]
    cor = [a for a in members(Lm, n) if (am[4] >> a & 1) and ((am[4] & ~am[a]) & Lm) == 0]
    V["X2.cor125_B1"] = cor
    # X3
    par = (None, 0, 0, 1, 2); n = 5; am = anc_masks(par); full = (1 << n) - 1
    pairs, merge, tot = [], None, True
    for k, X in enumerate([0b00111, 0b00011, 0b00001], 1):
        Lm = liftm(X, [(3, 1), (4, 2)]); M = rmat(am, full, Lm, n); mem = members(Lm, n)
        d = M @ (np.array([0, 0, 0, 1, 0]) - np.array([0, 0, 0, 0, 1]))
        tot = tot and int(d.sum()) == 0
        if np.any(d):
            pairs.append([mem[int(np.argmax(d))], mem[int(np.argmin(d))]])
        else:
            pairs.append([])
            merge = merge or k
    V["X3.pairs"], V["X3.merge_step"], V["X3.totals_equal"] = pairs, merge, tot
    # X4, X5, X7
    par = (None, 0, 1); n = 3; am = anc_masks(par)
    laws = [L3[0], L3[2]]
    for tag, X in (("X4", 0b001), ("X5", 0b011)):
        Lm = liftm(X, [(2, 1)]); mem = members(Lm, n)
        own = [mem.index(deepest(am, Lm, v)) for v in range(2)]
        h = deepest(am, Lm, 2); hi = mem.index(h)
        l0, l1 = dp_law(own, laws, mem, None), dp_law(own, laws, mem, (hi, 1))
        V[tag + ".holder"] = h; V[tag + ".tv"] = fr(tvf(l0, l1))
        if tag == "X4":
            nu = dp_law([0, 0], laws, [0], None)
            V["X4.max_nu"] = fr(max(nu.values()))
            basis = sorted(set(l0) | set(l1))
            r0 = np.diag([float(l0.get(b, 0)) for b in basis]); r1 = np.diag([float(l1.get(b, 0)) for b in basis])
            ev = np.linalg.eigvalsh(r1 - r0)
            td = F(float(np.abs(ev).sum() / 2)).limit_denominator(1000)
            V["X4.helstrom_success"] = fr((1 + td) / 2)
            V["X7.trace_distance"] = fr(td)
            ok = True
            for r in (r0, r1):
                out = np.zeros_like(r)
                for g in sorted({b[hi] for b in basis}):
                    P = np.diag([1.0 if b[hi] == g else 0.0 for b in basis])
                    out = out + P @ r @ P
                ok = ok and np.array_equal(out, r)
            V["X7.pinch_fixed"] = bool(ok)
        else:
            V["X5.tv_addr1"] = fr(tvf(margf(l0, [mem.index(1)]), margf(l1, [mem.index(1)])))
    j0 = {(0, 0): F(1, 2), (1, 1): F(1, 2)}; j1 = {(1, 0): F(1, 2), (2, 1): F(1, 2)}
    V["X6.tv_joint"] = fr(tvf(j0, j1)); V["X6.tv_holder"] = fr(tvf(margf(j0, [0]), margf(j1, [0]))); V["X6.tv_ref"] = fr(tvf(margf(j0, [1]), margf(j1, [1])))
    return V


def u12_case(par0, l, ch, grades_list, ws, C, n):
    par = par0 + (l,); e = n; N = n + 1; am = anc_masks(par); full = (1 << N) - 1
    holders = None
    for w in ws:
        for xP in grades_list:
            C["u12_cases"] += 1
            x1 = np.array(list(xP) + [w]); x0 = np.array(list(xP) + [0])
            prev_m, comp, prevh, hs = full, np.eye(N, dtype=np.int64), None, []
            for X in ch:
                Lm = liftm(X, [(e, l)]); mem = members(Lm, N)
                C["u12_steps"] += 1
                step = rmat(am, prev_m, Lm, N); comp = step @ comp
                one = rmat(am, full, Lm, N)
                d = one @ (x1 - x0)
                nz = [mem[i] for i in range(len(d)) if d[i] != 0]
                h = mem[int(np.argmax(one[:, e]))]
                ok = nz == [h] and int(d[mem.index(h)]) == w and np.array_equal(comp, one)
                if prevh is not None:
                    if Lm >> prevh & 1:
                        ok = ok and h == prevh
                    else:
                        ok = ok and (am[prevh] >> h & 1) and h != prevh and popl(am[h]) < popl(am[prevh])
                        C["u12_strict"] += 1
                for a in mem:
                    crit = bool(am[e] >> a & 1) and ((am[e] & ~am[a]) & Lm) == 0
                    ok = ok and crit == (a == h)
                Xm = X
                ok = ok and all(deepest(am, Lm, v) == deepest(anc_masks(par0), Xm, v) for v in range(n))
                if h != e:
                    C["u12_h_ne_e"] += 1
                if not ok:
                    C["u12_viol"] += 1
                prevh, prev_m = h, Lm; hs.append(h)
            holders = hs
    return holders


def exhaustive():
    U = dict(u12_cases=0, u12_steps=0, u12_strict=0, u12_h_ne_e=0, u12_viol=0,
             u114_cases=0, u114_steps=0, u114_merged=0, u114_unmerged=0, u114_viol=0,
             u13_steps=0, u13_tv_lt1=0, u13_h_ne_e=0, u13_multi=0, u13_attained=0, u13_viol=0)
    l12, l114, l13 = [], [], []
    for n in range(1, 6):
        for par0 in all_trees(n):
            cm = closed_masks(par0); chs = chains(cm, 3)
            pstr = ",".join("-" if p is None else str(p) for p in par0)
            grades = list(itertools.product((0, 1), repeat=n))
            for l in range(n):
                for ch in chs:
                    hs = u12_case(par0, l, ch, grades, (1, 2), U, n)
                    l12.append(pstr + "|" + str(l) + "|" + ";".join(mstr(X, n) for X in ch) + "|" + ",".join(map(str, hs)))
            for l in range(n):
                for lp in range(n):
                    if l == lp:
                        continue
                    par = par0 + (l, lp); e, ep, N = n, n + 1, n + 2; am = anc_masks(par); full = (1 << N) - 1
                    for ch in chs:
                        rec = None
                        for base in (0, 1):
                            U["u114_cases"] += 1
                            dvec = np.zeros(N, dtype=np.int64); dvec[e] = 1; dvec[ep] = -1
                            merged, steps = False, []
                            for X in ch:
                                Lm = liftm(X, [(e, l), (ep, lp)]); mem = members(Lm, N)
                                U["u114_steps"] += 1
                                M = rmat(am, full, Lm, N)
                                xa = np.array([base] * n + [1, 0]); xb = np.array([base] * n + [0, 1])
                                d = M @ xa - M @ xb
                                ok = int((M @ xa).sum()) == int((M @ xb).sum()) and np.array_equal(d, M @ dvec)
                                ie, iep = int(np.argmax(M[:, e])), int(np.argmax(M[:, ep]))
                                if ie == iep:
                                    ok = ok and not np.any(d); merged = True; U["u114_merged"] += 1; steps.append("-")
                                else:
                                    ok = ok and d[ie] == 1 and d[iep] == -1 and int(np.count_nonzero(d)) == 2 and not merged
                                    U["u114_unmerged"] += 1; steps.append(str(mem[ie]) + ":" + str(mem[iep]))
                                for i, z in enumerate(mem):
                                    ok = ok and ((d[i] != 0) == ((M[i, e] == 1) != (M[i, ep] == 1)))
                                if not ok:
                                    U["u114_viol"] += 1
                            rec = steps
                        l114.append(pstr + "|" + str(l) + "|" + str(lp) + "|" + ";".join(mstr(X, n) for X in ch) + "|" + ";".join(rec))
            if n <= 4:
                chs2 = chains(cm, 2)
                for l in range(n):
                    par = par0 + (l,); e, N = n, n + 1; am = anc_masks(par)
                    for w in (1, 2):
                        for ch in chs2:
                            for asg in itertools.product(range(3), repeat=n):
                                laws = [L3[i] for i in asg]
                                for k, X in enumerate(ch, 1):
                                    Lm = liftm(X, [(e, l)]); mem = members(Lm, N)
                                    U["u13_steps"] += 1
                                    own = [mem.index(deepest(am, Lm, v)) for v in range(n)]
                                    h = deepest(am, Lm, e); hi = mem.index(h)
                                    l0 = dp_law(own, laws, mem, None); l1 = dp_law(own, laws, mem, (hi, w))
                                    T = tvf(l0, l1)
                                    nuh = margf(l0, [hi]); nu = {kk[0]: v for kk, v in nuh.items()}
                                    nus = {kk + w: v for kk, v in nu.items()}
                                    ok = T == tvf(nu, nus) and T >= max(nu.values())
                                    for y in set(l0) | set(l1):
                                        ok = ok and l1.get(y, 0) * nu.get(y[hi], 0) == l0.get(y, 0) * nus.get(y[hi], 0)
                                    if len(nu) == 1:
                                        ok = ok and T == 1
                                    m = len(mem)
                                    for mask in range(1, (1 << m) - 1):
                                        S = [i for i in range(m) if mask >> i & 1]
                                        t = tvf(margf(l0, S), margf(l1, S))
                                        ok = ok and (t == T if (mask >> hi & 1) else t == 0)
                                    succ = F(0)
                                    for y in set(l0) | set(l1):
                                        succ += l1.get(y, F(0)) if nus.get(y[hi], 0) > nu.get(y[hi], 0) else l0.get(y, F(0))
                                    ok = ok and succ / 2 == (1 + T) / 2
                                    fib = [v for v in range(n) if own[v] == hi]
                                    U["u13_tv_lt1"] += T < 1; U["u13_h_ne_e"] += h != e
                                    U["u13_multi"] += sum(1 for v in fib if asg[v] == 2) >= 2
                                    U["u13_attained"] += T == max(nu.values())
                                    if not ok:
                                        U["u13_viol"] += 1
                                    l13.append("|".join([pstr, str(l), str(w), ";".join(mstr(X, n) for X in ch), ",".join(map(str, asg)), str(k), str(h), fr(T)]))
    for name, ls in (("u12", l12), ("u114", l114), ("u13", l13)):
        ls.sort(); U[name + "_lines"] = len(ls); U[name + "_digest"] = hashlib.sha256("\n".join(ls).encode()).hexdigest()
    U["trees_n5"] = sum(1 for n in range(1, 6) for _ in all_trees(n)); U["trees_n4"] = sum(1 for n in range(1, 5) for _ in all_trees(n))
    for k in ("u13_tv_lt1", "u13_h_ne_e", "u13_multi", "u13_attained"):
        U[k] = int(U[k])
    return U


def rand_tree(rng, n):
    return (None,) + tuple(int(rng.integers(0, i)) for i in range(1, n))


def rand_chain(rng, par, steps):
    cm = closed_masks(par)
    ch = [cm[int(rng.integers(0, len(cm)))]]
    for _ in range(steps - 1):
        sub = [m for m in cm if m != ch[-1] and (m & ch[-1]) == m]
        if not sub:
            break
        ch.append(sub[int(rng.integers(0, len(sub)))])
    return ch


def bounded():
    rng = np.random.default_rng(20261018)
    B = {}
    C = dict(u12_cases=0, u12_steps=0, u12_strict=0, u12_h_ne_e=0, u12_viol=0)
    for _ in range(3000):
        n = int(rng.integers(6, 10)); par0 = rand_tree(rng, n); l = int(rng.integers(0, n))
        ch = rand_chain(rng, par0, int(rng.integers(1, 6)))
        xs = [tuple(int(v) for v in rng.integers(0, 4, n))]
        u12_case(par0, l, ch, xs, (int(rng.integers(1, 4)),), C, n)
    B["B12_cases"], B["B12_viol"], B["B12_steps"] = 3000, C["u12_viol"], C["u12_steps"]
    viol = 0
    for _ in range(2000):
        n = int(rng.integers(6, 10)); par0 = rand_tree(rng, n)
        l, lp = [int(v) for v in rng.choice(n, 2, replace=False)]
        par = par0 + (l, lp); e, ep, N = n, n + 1, n + 2; am = anc_masks(par); full = (1 << N) - 1
        ch = rand_chain(rng, par0, int(rng.integers(1, 6))); merged = False
        xP = [int(v) for v in rng.integers(0, 4, n)]
        for X in ch:
            Lm = liftm(X, [(e, l), (ep, lp)]); M = rmat(am, full, Lm, N)
            a, b = M @ np.array(xP + [1, 0]), M @ np.array(xP + [0, 1]); d = a - b
            ie, iep = int(np.argmax(M[:, e])), int(np.argmax(M[:, ep]))
            ok = int(a.sum()) == int(b.sum())
            if ie == iep:
                ok = ok and not np.any(d); merged = True
            else:
                ok = ok and d[ie] == 1 and d[iep] == -1 and np.count_nonzero(d) == 2 and not merged
            viol += not ok
    B["B114_cases"], B["B114_viol"] = 2000, int(viol)
    viol = 0
    for _ in range(1000):
        n = int(rng.integers(5, 7)); par0 = rand_tree(rng, n); l = int(rng.integers(0, n)); w = int(rng.integers(1, 4))
        par = par0 + (l,); e, N = n, n + 1; am = anc_masks(par)
        laws = []
        for v in range(n):
            c = rng.multinomial(4, [1 / 3] * 3)
            laws.append(tuple((i, F(int(c[i]), 4)) for i in range(3) if c[i]))
        for X in rand_chain(rng, par0, int(rng.integers(1, 4))):
            Lm = liftm(X, [(e, l)]); mem = members(Lm, N)
            own = [mem.index(deepest(am, Lm, v)) for v in range(n)]; hi = mem.index(deepest(am, Lm, e))
            l0 = dp_law(own, laws, mem, None); l1 = dp_law(own, laws, mem, (hi, w)); T = tvf(l0, l1)
            nu = {kk[0]: v for kk, v in margf(l0, [hi]).items()}; nus = {k + w: v for k, v in nu.items()}
            ok = T == tvf(nu, nus) and T >= max(nu.values())
            comp = [i for i in range(len(mem)) if i != hi]
            if comp:
                ok = ok and tvf(margf(l0, comp), margf(l1, comp)) == 0
            for i in comp:
                ok = ok and tvf(margf(l0, [i]), margf(l1, [i])) == 0
            viol += not ok
    B["B13_cases"], B["B13_viol"] = 1000, int(viol)
    return B


def controls():
    R = {}
    def rej(claim_holds):
        return "ACCEPTED" if claim_holds else "REJECTED"
    par = (None, 0, 1, 2); am = anc_masks(par)
    hs = [deepest(am, liftm(X, [(3, 2)]), 3) for X in [0b0111, 0b0011, 0b0001]]
    R["R1_holder_is_parent"] = rej(all(h == 2 for h in hs))
    Lm = liftm(0b0111, [(3, 2)]); M = rmat(am, 0b1111, Lm, 4)
    d = M @ np.array([0, 0, 0, 1]); mem = members(Lm, 4)
    R["R2_copy_two_holders"] = rej(d[mem.index(3)] != 0 and d[mem.index(2)] != 0)
    h1 = deepest(am, liftm(0b0001, [(3, 2)]), 3); h2 = deepest(am, liftm(0b0111, [(3, 2)]), 3)
    R["R3_nonnested_depth_nonincreasing"] = rej(popl(am[h2]) <= popl(am[h1]))
    j0 = {(0, 0): F(1, 2), (1, 1): F(1, 2)}; j1 = {(1, 0): F(1, 2), (2, 1): F(1, 2)}
    R["R4_holder_sufficient_correlated"] = rej(tvf(j0, j1) == tvf(margf(j0, [0]), margf(j1, [0])))
    nu = {0: F(1, 2), 1: F(1, 2)}; nus = {1: F(1, 2), 2: F(1, 2)}
    R["R5_double_max_bound"] = rej(tvf(nu, nus) >= 2 * max(nu.values()))
    par = (None, 0, 0, 1, 2); am = anc_masks(par)
    Lm = liftm(0b00001, [(3, 1), (4, 2)]); M = rmat(am, 0b11111, Lm, 5)
    R["R6_survives_merge"] = rej(bool(np.any(M @ np.array([0, 0, 0, 1, -1]))))
    par = (None, 0, 0, 1, 3); am = anc_masks(par)
    hA = deepest(am, liftm(0b00011, [(4, 3)]), 4); hB = deepest(am, liftm(0b00011, [(4, 3)]), 4)
    R["R7_records_incomparable_order"] = rej(hA != hB)
    par = (None, 0, 1); am = anc_masks(par); Lm = liftm(0b011, [(2, 1)]); mem = members(Lm, 3)
    own = [mem.index(deepest(am, Lm, v)) for v in range(2)]
    l0 = dp_law(own, [L3[0], L3[2]], mem, None); l1 = dp_law(own, [L3[0], L3[2]], mem, (mem.index(2), 1))
    R["R8_zero_power_with_holder"] = rej(tvf(margf(l0, [mem.index(2)]), margf(l1, [mem.index(2)])) == 0)
    return R


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    cert = {"meta": {"role": "checker", "result_sha256": rsha, "numpy": np.__version__,
                     "algorithm": "bitmask views, numpy retraction matrices, DP joint laws, eigvalsh Helstrom"},
            "values": instances(), "universe": exhaustive(), "bounded": bounded(), "controls": controls()}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("universe", "bounded", "controls")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
