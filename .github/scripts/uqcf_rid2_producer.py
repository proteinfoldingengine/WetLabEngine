"""receiver_identification draft 2 freeze: PRODUCER (pure-Python exact Fractions; nearest-ancestor walk).
Computes the preregistered exact instances (FREEZE.md section 2) and the exhaustive universe (section 3)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d2_review")


def trees(n):
    # labelled rooted trees with parent[i] < i
    for ps in itertools.product(*[range(i) for i in range(1, n)]):
        yield (None,) + ps


def retained_sets(par):
    n = len(par)
    out = []
    def grow(cur, frontier):
        out.append(frozenset(cur))
        for i, c in enumerate(frontier):
            kids = [z for z in range(n) if par[z] == c]
            grow(cur | {c}, frontier[i + 1:] + kids)
    kids0 = [z for z in range(n) if par[z] == 0]
    grow({0}, kids0)
    return sorted(set(out), key=lambda s: (len(s), sorted(s)))


def owner(par, keep, z):
    while z not in keep:
        z = par[z]
    return z


def push(par, keep, x):
    y = {a: 0 for a in keep}
    for z, v in enumerate(x):
        if v is not None:
            y[owner(par, keep, z)] += v
    return y


def tv(p, q):
    ks = set(p) | set(q)
    return sum(abs(p.get(k, 0) - q.get(k, 0)) for k in ks) / 2


def conv(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i + j] = out.get(i + j, 0) + a * b
    return out


def s(v):
    return str(F(v))


def instances():
    V = {}
    par = (None, 0, 1); keep = {0, 1}
    a, b = push(par, keep, (1, 0, 1)), push(par, keep, (1, 0, 0))
    V["E1.mu_x"] = [str(a[k]) for k in sorted(keep)]; V["E1.mu_xp"] = [str(b[k]) for k in sorted(keep)]
    V["E1.owner"] = [k for k in sorted(keep) if a[k] != b[k]]
    par = (None, 0, 0); keep = {0}
    a, b = push(par, keep, (0, 1, 0)), push(par, keep, (0, 0, 1))
    V["E2.owner"] = [k for k in sorted(keep) if a[k] != b[k]]; V["E2.equal"] = a == b
    par = (None, 0, 1, 2); chain = [{0, 1, 2}, {0, 1}, {0}]
    x, xp = [0, 0, 0, 1], [0, 0, 0, 0]
    hold, diffs = [], []
    for keep in chain:
        a, b = push(par, keep, x), push(par, keep, xp)
        d = [k for k in sorted(keep) if a[k] != b[k]]
        assert len(d) == 1
        hold.append(d[0]); diffs.append(str(a[d[0]] - b[d[0]]))
    V["E3.holders"], V["E3.diffs"] = hold, diffs
    par = (None, 0, 0); d = [0, 1, -1]
    step = None
    for k, keep in enumerate([{0, 1}, {0}], 1):
        y = push(par, keep, d)
        if all(v == 0 for v in y.values()) and step is None:
            step = k
    V["E3.merge_step"] = step
    pu, qu, pa = {0: F(1)}, {1: F(1)}, {0: F(1, 2), 1: F(1, 2)}
    V["E4a.tv_src"] = s(tv(pu, qu)); V["E4a.tv_owner"] = s(tv(conv(pa, pu), conv(pa, qu)))
    V["E4a.tv_point"] = s(tv(conv({0: F(1)}, pu), conv({0: F(1)}, qu)))
    pu, qu = {0: F(1, 2), 1: F(1, 2)}, {0: F(1, 4), 1: F(3, 4)}
    V["E4b.tv_src"] = s(tv(pu, qu)); V["E4b.tv_owner"] = s(tv(conv(pa, pu), conv(pa, qu)))
    jp = {(0, 0): F(1, 2), (1, 1): F(1, 2)}; jq = {(0, 1): F(1, 2), (1, 0): F(1, 2)}
    def marg(j, i):
        m = {}
        for k, v in j.items():
            m[k[i]] = m.get(k[i], 0) + v
        return m
    def summ(j):
        m = {}
        for k, v in j.items():
            m[k[0] + k[1]] = m.get(k[0] + k[1], 0) + v
        return m
    V["E4c.tv_src_marg"] = s(tv(marg(jp, 1), marg(jq, 1)))
    V["E4c.tv_owner"] = s(tv(summ(jp), summ(jq))); V["E4c.tv_joint_before"] = s(tv(jp, jq))
    # Prop 5(c): permutation |u,a> -> |u, a+u mod 2> vs CNOT table
    cadd = {(u, a): (u, (a + u) % 2) for u in range(2) for a in range(2)}
    cnot = {(0, 0): (0, 0), (0, 1): (0, 1), (1, 0): (1, 1), (1, 1): (1, 0)}
    V["E5.cnot"] = cadd == cnot
    # control |+>, blank owner: output amplitudes 1/sqrt2 on |00>,|11>; owner reduced = diag of |amp|^2
    amps = {cadd[(u, 0)]: F(1, 2) for u in range(2)}  # squared amplitudes; off-diagonal owner terms vanish since u-values differ
    red = [[s(sum(v for (u, a), v in amps.items() if a == i)) if i == j else "0" for j in range(2)] for i in range(2)]
    V["E5.owner_reduced"] = red
    pts = list(itertools.product(range(2), range(3)))
    ok = all({p: int(p == q) for p in pts} == {p: int(p[0] == q[0]) * int(p[1] == q[1]) for p in pts} for q in pts)
    V["P1.factor"] = ok and len(set(pts)) == 6
    # draft 2 instances
    h = F(1, 2)
    par = (None, 0, 0); keep = {0}
    def owner_law(par, keep, laws, a):
        # full product joint, pushforward, owner marginal
        out = {}
        for x in itertools.product(*[sorted(l) for l in laws]):
            w = F(1)
            for l, v in zip(laws, x):
                w *= l[v]
            y = push(par, keep, x)
            out[y[a]] = out.get(y[a], 0) + w
        return out
    lp = [{0: F(1)}, {0: F(1)}, {0: h, 1: h}]; lq = [{0: F(1)}, {1: F(1)}, {0: h, 1: h}]
    V["E6.tv_src"] = s(tv(lp[1], lq[1])); V["E6.tv_owner"] = s(tv(owner_law(par, keep, lp, 0), owner_law(par, keep, lq, 0)))
    V["E6.tv_draft1_formula"] = s(tv(conv({0: F(1)}, lp[1]), conv({0: F(1)}, lq[1])))
    u6 = {i: F(1, 6) for i in range(6)}
    V["E7.tv"] = s(tv(conv(u6, {0: F(1)}), conv(u6, {1: F(1)})))
    n8 = {0: F(1, 4), 1: h, 2: F(1, 4)}
    V["E8.tv"] = s(tv(conv(n8, {0: F(1)}), conv(n8, {2: F(1)}))); V["E8.max_nu"] = s(max(n8.values()))
    V["E9.tv"] = s(tv(conv({0: h, 1: h}, {0: h, 2: h}), conv({0: h, 1: h}, {1: F(1)})))
    return V


D6 = [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]   # weights x2


def fmt(fr):
    fr = F(fr)
    return str(fr.numerator) if fr.denominator == 1 else "%d/%d" % (fr.numerator, fr.denominator)


def wconv(a, b):
    o = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            o[i + j] += x * y
    return o


def p4f():
    C = {"p4f_trees": 0, "p4f_cases": 0, "p4f_multi": 0, "p4f_draft1_wrong": 0, "p4f_point_nu": 0,
         "p4f_det_pairs": 0, "p4f_viol": 0}
    lines = []
    for n in range(1, 5):
        for par in trees(n):
            C["p4f_trees"] += 1
            pstr = ",".join("-" if v is None else str(v) for v in par)
            pts = list(itertools.product(range(3), repeat=n))
            for keep in retained_sets(par):
                ks = sorted(keep)
                ys = [push(par, keep, x) for x in pts]
                for u in [z for z in range(n) if z not in keep]:
                    a = owner(par, keep, u)
                    others = [z for z in range(n) if z != u]
                    fib = [z for z in others if owner(par, keep, z) == a]
                    for asg in itertools.product(range(6), repeat=len(others)):
                        law = dict(zip(others, asg))
                        nu = [1]
                        for z in fib:
                            nu = wconv(nu, D6[law[z]])
                        nuF = [F(v, 2 ** len(fib)) for v in nu]
                        point_nu = sum(1 for v in nu if v) == 1
                        base_w = []
                        for x in pts:
                            w = 1
                            for z in others:
                                w *= D6[law[z]][x[z]]
                            base_w.append(w)
                        for pi in range(6):
                            for qi in range(6):
                                C["p4f_cases"] += 1
                                C["p4f_multi"] += int(len(fib) >= 2)
                                jp, jq, op, oq = {}, {}, {}, {}
                                for x, y, w in zip(pts, ys, base_w):
                                    if not w:
                                        continue
                                    wp, wq = w * D6[pi][x[u]], w * D6[qi][x[u]]
                                    key = tuple(y[t] for t in ks)
                                    jp[key] = jp.get(key, 0) + wp; jq[key] = jq.get(key, 0) + wq
                                    op[y[a]] = op.get(y[a], 0) + wp; oq[y[a]] = oq.get(y[a], 0) + wq
                                Z = 2 ** n
                                otv = F(sum(abs(op.get(k, 0) - oq.get(k, 0)) for k in set(op) | set(oq)), 2 * Z)
                                jtv = F(sum(abs(jp.get(k, 0) - jq.get(k, 0)) for k in set(jp) | set(jq)), 2 * Z)
                                stv = F(sum(abs(D6[pi][i] - D6[qi][i]) for i in range(3)), 4)
                                bad = False
                                for lawu, o in ((D6[pi], op), (D6[qi], oq)):
                                    form = wconv(nu, lawu)
                                    bad |= any(F(o.get(k, 0), Z) != F(form[k] if k < len(form) else 0, 2 ** (len(fib) + 1))
                                               for k in set(o) | set(range(len(form))))
                                for t in ks:
                                    if t == a:
                                        continue
                                    mp, mq = {}, {}
                                    for k, v in jp.items():
                                        mp[k[ks.index(t)]] = mp.get(k[ks.index(t)], 0) + v
                                    for k, v in jq.items():
                                        mq[k[ks.index(t)]] = mq.get(k[ks.index(t)], 0) + v
                                    bad |= {k: v for k, v in mp.items() if v} != {k: v for k, v in mq.items() if v}
                                bad |= jtv != otv
                                bad |= otv > stv
                                if point_nu:
                                    C["p4f_point_nu"] += 1
                                    bad |= otv != stv
                                if pi != qi:
                                    bad |= otv == 0
                                if pi < 3 and qi < 3 and pi != qi:
                                    C["p4f_det_pairs"] += 1
                                    bad |= otv < max(nuF)
                                pa = D6[law[a]]
                                d1 = F(sum(abs(x - y) for x, y in zip(wconv(pa, D6[pi]), wconv(pa, D6[qi]))), 8)
                                C["p4f_draft1_wrong"] += int(d1 != otv)
                                C["p4f_viol"] += int(bad)
                                lines.append("%s|%s|%d|%s|%d|%d|%s" % (pstr, ",".join(map(str, ks)), u,
                                             ",".join(map(str, asg)), pi, qi, fmt(otv)))
    lines.sort()
    C["p4f_digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return C


def p42():
    C = {"p42_cases": 0, "p42_laws": 0, "p42_attained": 0, "p42_uniform_k1_attained": 0, "p42_viol": 0}
    lines = []
    def comps(total, parts):
        if parts == 1:
            yield (total,)
            return
        for i in range(total + 1):
            for rest in comps(total - i, parts - 1):
                yield (i,) + rest
    for c in comps(6, 6):
        C["p42_laws"] += 1
        nu = {j: F(v, 6) for j, v in enumerate(c) if v}
        for k in range(1, 7):
            C["p42_cases"] += 1
            t = tv(conv(nu, {0: F(1)}), conv(nu, {k: F(1)}))
            m = max(nu.values())
            C["p42_viol"] += int(not (m <= t <= 1))
            if t == m:
                C["p42_attained"] += 1
                if c == (1,) * 6 and k == 1:
                    C["p42_uniform_k1_attained"] += 1
            lines.append("%s|%d|%s" % (",".join(map(str, c)), k, fmt(t)))
    lines.sort()
    C["p42_digest"] = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return C


def exhaustive():
    C = {"t2_pairs": 0, "t2_W_checks": 0, "t2_single": 0, "t2_cancel": 0, "t2_viol": 0,
         "t3_cases": 0, "t3_viol": 0, "trees": 0, "retained_sets": 0}
    G = [0, 1, 2]
    for n in range(1, 6):
        for par in trees(n):
            C["trees"] += 1
            sets = retained_sets(par)
            C["retained_sets"] += len(sets)
            for keep in sets:
                ks = sorted(keep); rem = [z for z in range(n) if z not in keep]
                Ws = [set(c) for m in range(1, len(ks) + 1) for c in itertools.combinations(ks, m)]
                for x in itertools.product(G, repeat=n):
                    for xr in itertools.product(G, repeat=len(rem)):
                        xp = list(x)
                        for z, v in zip(rem, xr):
                            xp[z] = v
                        C["t2_pairs"] += 1
                        a, b = push(par, keep, x), push(par, keep, xp)
                        O = {t for t in ks if sum(x[u] - xp[u] for u in rem if owner(par, keep, u) == t) != 0}
                        if {t for t in ks if a[t] != b[t]} != O:
                            C["t2_viol"] += 1
                        for W in Ws:
                            C["t2_W_checks"] += 1
                            if any(a[t] != b[t] for t in W) != bool(W & O):
                                C["t2_viol"] += 1
                        dz = [u for u in range(n) if x[u] != xp[u]]
                        if len(dz) == 1:
                            C["t2_single"] += 1
                            if O != {owner(par, keep, dz[0])}:
                                C["t2_viol"] += 1
                        if dz and not O:
                            C["t2_cancel"] += 1
            full = frozenset(range(n))
            def chains(prev, depth):
                for s2 in sets:
                    if s2 < prev:
                        yield [s2]
                        if depth > 1:
                            for rest in chains(s2, depth - 1):
                                yield [s2] + rest
            for ch in chains(full, 3):
                ever = [u for u in range(n) if u not in ch[-1]]
                for u in ever:
                    for x in itertools.product(G, repeat=n):
                        for v in G:
                            if v == x[u]:
                                continue
                            xp = list(x); xp[u] = v
                            C["t3_cases"] += 1
                            for keep in ch:
                                a, b = push(par, keep, x), push(par, keep, xp)
                                d = [t for t in sorted(keep) if a[t] != b[t]]
                                if d != [owner(par, keep, u)] or a[d[0]] - b[d[0]] != x[u] - v:
                                    C["t3_viol"] += 1
                                    break
    C.update(p4f())
    C.update(p42())
    return C


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    cert = {"meta": {"role": "producer", "result_sha256": rsha, "method": "pure-Python Fractions, nearest-ancestor walk"},
            "values": instances(), "universe": exhaustive()}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps(cert["universe"], sort_keys=True))


if __name__ == "__main__":
    main()
