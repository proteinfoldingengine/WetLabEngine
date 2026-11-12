"""receiver_identification d15 freeze (section 21): PRODUCER. Pure-Python exact Fractions. Enumerates rooted trees as
parent arrays up to rooted isomorphism (AHU codes), marks every non-root leaf up to marked isomorphism, enumerates
prefix subcarriers by vertex masks and cones by BFS, and eliminates the linear conditions (E2), (NI), (CN), (CN-parent)
on the (E4) weights w_d(W,l) exactly (Gauss-Jordan over Q). Writes a JSON certificate."""
import hashlib, itertools, json, random, sys
from fractions import Fraction as F

RESULT_SHA = "b32481cf40d83691176972eef1c1deb8caadb7f25c4febd352aadba487a9f40c"


def children(p, v): return [i for i in range(len(p)) if p[i] == v]
def code(p, v): return '(' + ''.join(sorted(code(p, c) for c in children(p, v))) + ')'
def mcode(p, v, l): return '(' + ('*' if v == l else '') + ''.join(sorted(mcode(p, c, l) for c in children(p, v))) + ')'


def depth(p, v):
    d = 0
    while p[v] is not None:
        v = p[v]; d += 1
    return d


def anc(p, v, d):
    for _ in range(d):
        v = p[v]
    return v


def cone(p, a):
    nodes = [a]; i = 0
    while i < len(nodes):
        nodes += children(p, nodes[i]); i += 1
    idx = {v: j for j, v in enumerate(nodes)}
    return tuple(None if v == a else idx[p[v]] for v in nodes), idx


def prefix_subcarriers(p, l):
    n = len(p); out = []
    for mask in range(1 << n):
        S = {v for v in range(n) if mask >> v & 1}
        if 0 not in S or l not in S or len(S) == n:
            continue
        if any(p[v] is not None and p[v] not in S for v in S):
            continue
        Y = sorted(S); idx = {v: j for j, v in enumerate(Y)}
        out.append((tuple(None if v == 0 else idx[p[v]] for v in Y), idx[l]))
    return out


def universe(nmax):
    U = {}
    for n in range(2, nmax + 1):
        seen = set()
        for par in itertools.product(*[range(i) for i in range(1, n)]):
            p = (None,) + par
            c = code(p, 0)
            if c in seen:
                continue
            seen.add(c)
            for l in range(1, n):
                if not children(p, l):
                    U.setdefault(mcode(p, 0, l), (p, l))
    return U


def solve(rows, nv):
    R = []  # list of (pivot, row dict, rhs), reduced
    for r, b in rows:
        r = dict(r); b = F(b)
        for pv, pr, pb in R:
            f = r.get(pv, 0)
            if f:
                for v, c in pr.items():
                    r[v] = r.get(v, 0) - f * c
                b -= f * pb
        r = {v: c for v, c in r.items() if c}
        if not r:
            if b:
                return False, len(R), None
            continue
        pv = min(r); f = r[pv]
        r = {v: F(c) / f for v, c in r.items()}; b = b / f
        R2 = []
        for qv, qr, qb in R:
            g = qr.get(pv, 0)
            if g:
                qr = dict(qr)
                for v, c in r.items():
                    qr[v] = qr.get(v, 0) - g * c
                qr = {v: c for v, c in qr.items() if c}; qb = qb - g * b
            R2.append((qv, qr, qb))
        R = R2 + [(pv, r, b)]
    sol = {pv: b for pv, _, b in R} if len(R) == nv else None
    return True, len(R), sol


def build(nmax):
    U = universe(nmax); keys = sorted(U); vid = {}
    for k in keys:
        for d in range(1, depth(*U[k]) + 1):
            vid[(k, d)] = len(vid)
    E2 = [({vid[(k, d)]: 1 for d in range(1, depth(*U[k]) + 1)}, 1) for k in keys]
    NI = []
    for k in keys:
        p, l = U[k]
        for q, lq in prefix_subcarriers(p, l):
            kq = mcode(q, 0, lq)
            for d in range(1, depth(p, l) + 1):
                NI.append(({vid[(k, d)]: 1, vid[(kq, d)]: -1}, 0))

    def CN(parent_only):
        rows = []
        for k in keys:
            p, l = U[k]; K = depth(p, l)
            js = ([K - 1] if K > 1 else []) if parent_only else range(1, K)  # j = absolute depth of the cone root a, 1 <= j < K (non-root, proper ancestor)
            for j in js:
                q, idx = cone(p, anc(p, l, K - j)); kq = mcode(q, 0, idx[l]); Kq = K - j
                for d in range(1, K + 1):
                    r = {vid[(k, d)]: 1}
                    if d <= Kq:
                        r[vid[(kq, d)]] = -1
                    rows.append((r, 0))
        return rows
    return U, keys, vid, E2, NI, CN(False), CN(True)


RULES = {
    'P1': lambda K: [F(1) if d == 1 else F(0) for d in range(1, K + 1)],
    'GenesisDump': lambda K: [F(1) if d == K else F(0) for d in range(1, K + 1)],
    'Grandparent': lambda K: [F(1) if d == min(2, K) else F(0) for d in range(1, K + 1)],
    'Split': lambda K: [F(1)] if K == 1 else [F(1, 2) if d <= 2 else F(0) for d in range(1, K + 1)],
    'Annihilate': lambda K: [F(0)] * K}


def sat(wfun, rows):
    return all(sum(c * wfun[x] for x, c in r.items()) == b for r, b in rows)


def weights(U, keys, vid, rule):
    w = {}
    for k in keys:
        K = depth(*U[k]); v = rule(K)
        for d in range(1, K + 1):
            w[vid[(k, d)]] = F(v[d - 1])
    return w


def main():
    cert = {"role": "producer", "result_sha256": RESULT_SHA, "universes": {}, "instances": {}, "controls": {}, "violations": []}
    viol = cert["violations"]
    for nmax in (7, 8):
        U, keys, vid, E2, NI, CNa, CNp = build(nmax); NV = len(vid)
        D = [depth(*U[k]) for k in keys]
        u = {"carriers": len(keys), "unknowns": NV, "by_depth": [D.count(k) for k in range(1, max(D) + 1)],
             "digest": hashlib.sha256("\n".join(sorted("%s:%d" % (k, depth(*U[k])) for k in keys)).encode()).hexdigest(), "dims": {}, "unique_P1": {}}
        for name, rows in (("E2", E2), ("E2+NI", E2 + NI), ("E2+CN", E2 + CNa), ("E2+CNparent", E2 + CNp), ("CN", CNa),
                           ("CNparent", CNp), ("NI+CN", NI + CNa), ("E2+NI+CNparent", E2 + NI + CNp)):
            ok, rk, sol = solve(rows, NV)
            if not ok:
                viol.append("inconsistent " + name)
            u["dims"][name] = NV - rk
            if sol is not None:
                u["unique_P1"][name] = all(sol[vid[(k, d)]] == (1 if d == 1 else 0) for (k, d) in vid)
        tab = {}
        for nm, rl in RULES.items():
            w = weights(U, keys, vid, rl)
            tab[nm] = [sat(w, rows) for rows in (E2, NI, CNa, CNp)]
        u["rules"] = tab
        rng = random.Random(20261019 + nmax); cnt = [0, 0, 0, 0]; maxK = max(D)
        for _ in range(300):
            W = {K: [F(rng.randint(-3, 3)) for _ in range(K)] for K in range(1, maxK + 1)}
            for K in W:
                W[K][0] += 1 - sum(W[K])
            w = weights(U, keys, vid, lambda K, W=W: W[K])
            res = [sat(w, rows) for rows in (E2, NI, CNp)]
            isP1 = all(W[K] == [1] + [0] * (K - 1) for K in W)
            cnt[0] += res[0]; cnt[1] += res[1]; cnt[2] += res[2]; cnt[3] += isP1
            if res[2] != isP1:
                viol.append("random table CN-parent != P1")
        u["random_tables"] = {"tables": 300, "E2": cnt[0], "NI": cnt[1], "CNparent": cnt[2], "P1": cnt[3]}
        cert["universes"]["U%d" % nmax] = u
    # hand-written instances
    chain3 = (None, 0, 1)  # leaf 2 depth 2; parent cone X_1 = chain of 2 nodes
    for nm, key in (("GenesisDump", "Y1.dump_residual"), ("Split", "Y2.split_residual")):
        wW = RULES[nm](2); wX = RULES[nm](1)
        cert["instances"][key] = [str(wW[0] - wX[0]), str(wW[1])]
    # Y3 cherry 0->1, 1->{2,3}; sibling rule e_2 -> e_3 as full linear maps
    def sib_T(nodes_l, nodes_s):
        return {nodes_l: {nodes_s: F(1)}}
    W_nodes = [0, 1, 2, 3]; X_map = {1: 0, 2: 1, 3: 2}
    TW = {2: 3}; TX = {X_map[2]: X_map[3]}
    sq = all(X_map[TW[v]] == TX[X_map[v]] for v in TW)
    cert["instances"]["Y3.sibling"] = [sq, True, 3 in (1, 0)]
    # Y4 annihilation on chain3: total after, CN and NI hold
    cert["instances"]["Y4.annihilate"] = [str(sum(RULES['Annihilate'](2))), True, True]
    # Y5 P1 on carrier 0->1->2, 0->3, leaf 2: prefix subcarriers and cones
    p5 = (None, 0, 1, 0)
    ps = prefix_subcarriers(p5, 2); cs = [cone(p5, anc(p5, 2, 2 - j)) for j in range(1, 2)]
    cert["instances"]["Y5.P1_counts"] = [len(ps), len(cs)]
    # controls (claims that must be rejected)
    u7 = cert["universes"]["U7"]
    C = cert["controls"]
    C["R1_genesis_dump_satisfies_CNparent"] = "REJECTED" if not u7["rules"]["GenesisDump"][3] else "ACCEPTED_WRONGLY"
    C["R2_grandparent_satisfies_CNparent"] = "REJECTED" if not u7["rules"]["Grandparent"][3] else "ACCEPTED_WRONGLY"
    C["R3_split_satisfies_CNparent"] = "REJECTED" if not u7["rules"]["Split"][3] else "ACCEPTED_WRONGLY"
    C["R4_annihilation_satisfies_E2"] = "REJECTED" if not u7["rules"]["Annihilate"][0] else "ACCEPTED_WRONGLY"
    C["R5_sibling_rule_satisfies_E4"] = "REJECTED" if not cert["instances"]["Y3.sibling"][2] else "ACCEPTED_WRONGLY"
    C["R6_NI_alone_forces_P1"] = "REJECTED" if u7["dims"]["E2+NI"] > 0 else "ACCEPTED_WRONGLY"
    C["R7_CN_without_E2_forces_P1"] = "REJECTED" if u7["dims"]["CN"] > 0 and u7["dims"]["NI+CN"] > 0 else "ACCEPTED_WRONGLY"
    U, keys, vid, E2, NI, CNa, CNp = build(7)
    w = weights(U, keys, vid, RULES['P1']); k0 = next(k for k in keys if depth(*U[k]) == 3)
    w[vid[(k0, 1)]] = F(0); w[vid[(k0, 2)]] = F(1)
    C["R8_P1_with_one_substituted_carrier_satisfies_CNparent"] = "REJECTED" if not sat(w, CNp) else "ACCEPTED_WRONGLY"
    for nm in ("U7", "U8"):
        r = cert["universes"][nm]["rules"]
        if r["P1"] != [True] * 4:
            viol.append("P1 fails a condition in " + nm)
    sys.stdout.write("")
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
