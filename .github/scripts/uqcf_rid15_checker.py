"""receiver_identification d15 freeze (section 21): CHECKER, algorithmically independent of the producer.
Trees grown by attaching a leaf to every vertex of every smaller tree, canonicalized as nested sorted tuples; prefix
subcarriers as the closure of W under deletion of leaves other than l; cones from ancestor paths. Conditions are
written as vector-level commuting squares on R^W with explicit zero-extension maps (numpy integer arrays). Affine
dimensions are certified exactly by two bounds: an upper bound NV - rank_p from Gaussian elimination modulo two
primes (rank_p <= rank_Q), and a lower bound from explicitly constructed rational solutions that are verified to satisfy
every row and to be affinely independent (rank over Q of their differences, fraction-free). Equality certifies dim_Q."""
import hashlib, json, sys
import numpy as np
from fractions import Fraction as F

RESULT_SHA = "b32481cf40d83691176972eef1c1deb8caadb7f25c4febd352aadba487a9f40c"
PRIMES = (2147483629, 1000000007)


def canon(t, mark):  # t: dict vertex -> list children, root 0; returns nested tuple (marked, sorted children)
    def go(v):
        return (1 if v == mark else 0, tuple(sorted(go(c) for c in t[v])))
    return go(0)


def ser(c):
    return '(' + ('*' if c[0] else '') + ''.join(sorted(ser(x) for x in c[1])) + ')'


def grow(nmax):
    level = {canon({0: []}, -1): {0: []}}
    trees = []
    for n in range(2, nmax + 1):
        nxt = {}
        for t in level.values():
            for v in list(t):
                u = {a: list(b) for a, b in t.items()}; new = len(u); u[v].append(new); u[new] = []
                nxt.setdefault(canon(u, -1), u)
        level = nxt; trees += list(nxt.values())
    return trees


def parents(t):
    return {c: v for v in t for c in t[v]}


def path_to_root(t, v):
    par = parents(t); out = [v]
    while out[-1] != 0:
        out.append(par[out[-1]])
    return out  # v, parent, ..., 0


def marked(nmax):
    U = {}
    for t in grow(nmax):
        for l in t:
            if l != 0 and not t[l]:
                U.setdefault(ser(canon(t, l)), (t, l))
    return U


def induced(t, S, root):
    keep = sorted(S); return {v: [c for c in t[v] if c in S] for v in keep}, root


def relabel(sub, root):
    order = [root]; i = 0
    while i < len(order):
        order += sub[order[i]]; i += 1
    m = {v: j for j, v in enumerate(order)}
    return {m[v]: [m[c] for c in sub[v]] for v in order}, m


def prefix_subs(t, l):
    full = frozenset(t); seen = set(); stack = [full]; out = []
    while stack:
        S = stack.pop()
        for v in S:
            kids = [c for c in t[v] if c in S]
            if v != 0 and v != l and not kids:
                S2 = S - {v}
                if S2 not in seen:
                    seen.add(S2); stack.append(S2); out.append(S2)
    return out


def rank_mod(rows, nv, p):
    if not rows:
        return 0
    A = np.array(rows, dtype=np.int64) % p
    r = 0
    for c in range(nv):
        piv = np.nonzero(A[r:, c])[0]
        if piv.size == 0:
            continue
        i = r + piv[0]; A[[r, i]] = A[[i, r]]
        inv = pow(int(A[r, c]), p - 2, p); A[r] = (A[r] * inv) % p
        nz = np.nonzero(A[:, c])[0]
        for j in nz:
            if j != r:
                A[j] = (A[j] - A[j, c] * A[r]) % p
        r += 1
        if r == A.shape[0]:
            break
    return r


def rank_Q(vecs):
    M = [[F(x) for x in v] for v in vecs]; r = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def main():
    cert = {"role": "checker", "result_sha256": RESULT_SHA, "universes": {}, "instances": {}, "controls": {}, "violations": []}
    viol = cert["violations"]
    for nmax in (7, 8):
        U = marked(nmax); keys = sorted(U)
        info = {}
        for k in keys:
            t, l = U[k]; path = path_to_root(t, l); K = len(path) - 1
            info[k] = (t, l, path, K)
        off = {}; nv = 0
        for k in keys:
            off[k] = nv; nv += info[k][3]

        def var(k, d): return off[k] + d - 1
        rowsE2, rhsE2 = [], []
        for k in keys:
            r = [0] * nv
            for d in range(1, info[k][3] + 1):
                r[var(k, d)] = 1
            rowsE2.append(r); rhsE2.append(1)
        # vector-level squares: T_W(e_l) - J(T_Y(e_l)) = 0 componentwise on vertices of W
        def square_rows(k, sk, emb, sub, ls):  # emb: map from sub-carrier vertex -> W vertex; sub is the relabelled subcarrier itself
            t, l, path, K = info[k]; paths = path_to_root(sub, ls); Ks = len(paths) - 1
            assert Ks == info[sk][3]
            comp = {}
            for d in range(1, K + 1):
                comp.setdefault(path[d], {})[var(k, d)] = comp.get(path[d], {}).get(var(k, d), 0) + 1
            for d in range(1, Ks + 1):
                v = emb[paths[d]]; comp.setdefault(v, {})[var(sk, d)] = comp.get(v, {}).get(var(sk, d), 0) - 1
            out = []
            for v, r in comp.items():
                row = [0] * nv
                for x, c in r.items():
                    row[x] += c
                if any(row):
                    out.append(row)
            return out
        NI, CNa, CNp = [], [], []
        for k in keys:
            t, l, path, K = info[k]
            for S in prefix_subs(t, l):
                sub, m = relabel({v: [c for c in t[v] if c in S] for v in S}, 0)
                sk = ser(canon(sub, m[l])); inv = {j: v for v, j in m.items()}
                NI += square_rows(k, sk, inv, sub, m[l])
            for d_a in range(1, K):  # a = path[d_a], proper non-root ancestor (d_a < K means a != 0 when d_a <= K-1)
                a = path[d_a]
                desc = set(); st = [a]
                while st:
                    x = st.pop(); desc.add(x); st += t[x]
                sub, m = relabel({v: list(t[v]) for v in desc}, a)
                sk = ser(canon(sub, m[l])); inv = {j: v for v, j in m.items()}
                rs = square_rows(k, sk, inv, sub, m[l])
                CNa += rs
                if d_a == 1:
                    CNp += rs
        D = [info[k][3] for k in keys]
        u = {"carriers": len(keys), "unknowns": nv, "by_depth": [D.count(x) for x in range(1, max(D) + 1)],
             "digest": hashlib.sha256("\n".join(sorted("%s:%d" % (k, info[k][3]) for k in keys)).encode()).hexdigest(),
             "dims": {}, "unique_P1": {}}
        maxK = max(D)

        def vec(rule):
            w = [F(0)] * nv
            for k in keys:
                vv = rule(k, info[k][3])
                for d in range(1, info[k][3] + 1):
                    w[var(k, d)] = F(vv[d - 1])
            return w

        def satisfies(w, rows, rhs=None):
            for i, r in enumerate(rows):
                s = sum(F(c) * w[j] for j, c in enumerate(r) if c)
                if s != (rhs[i] if rhs else 0):
                    return False
            return True
        P1 = vec(lambda k, K: [1] + [0] * (K - 1))
        # explicit solution families (lower bounds)
        cone_par = {}
        for k in keys:
            t, l, path, K = info[k]
            a = path[1]; desc = set(); st = [a]
            while st:
                x = st.pop(); desc.add(x); st += t[x]
            sub, m = relabel({v: list(t[v]) for v in desc}, a)
            cone_par[k] = ser(canon(sub, m[l]))
        depth1 = sorted({cone_par[k] for k in keys})
        fam = {
            "E2": [P1] + [vec(lambda k, K, k0=k0, d0=d0: [(1 if (k == k0 and d == d0) else 0) + (-1 if (k == k0 and d == 1) else 0) + (1 if d == 1 else 0) for d in range(1, K + 1)])
                          for k0 in keys for d0 in range(2, info[k0][3] + 1)],
            "E2+NI": [P1] + [vec(lambda k, K, K0=K0, d0=d0: [(1 if (K == K0 and d == d0) else 0) - (1 if (K == K0 and d == 1) else 0) + (1 if d == 1 else 0) for d in range(1, K + 1)])
                             for K0 in range(2, maxK + 1) for d0 in range(2, K0 + 1)],
            "CN": [[F(0)] * nv] + [vec(lambda k, K, X=X: [1 if (d == 1 and cone_par[k] == X) else 0 for d in range(1, K + 1)]) for X in depth1],
            "NI+CN": [[F(0)] * nv, P1]}
        fam["CNparent"] = fam["CN"]
        systems = {"E2": (rowsE2, rhsE2), "E2+NI": (rowsE2 + NI, rhsE2 + [0] * len(NI)), "E2+CN": (rowsE2 + CNa, rhsE2 + [0] * len(CNa)),
                   "E2+CNparent": (rowsE2 + CNp, rhsE2 + [0] * len(CNp)), "CN": (CNa, None), "CNparent": (CNp, None), "NI+CN": (NI + CNa, None),
                   "E2+NI+CNparent": (rowsE2 + NI + CNp, rhsE2 + [0] * (len(NI) + len(CNp)))}
        for name, (rows, rhs) in systems.items():
            rows_u = [list(r) for r in {tuple(r): None for r in rows}] if rhs is None else rows
            ub = min(nv - rank_mod(rows_u, nv, p) for p in PRIMES)
            sols = fam.get(name, [P1])
            for s in sols:
                if not satisfies(s, rows, rhs):
                    viol.append("explicit solution fails " + name)
            lb = rank_Q([[a - b for a, b in zip(s, sols[0])] for s in sols[1:]]) if len(sols) > 1 else 0
            if lb != ub:
                viol.append("dimension not certified %s: lb %d ub %d" % (name, lb, ub))
            u["dims"][name] = ub
            if ub == 0:
                u["unique_P1"][name] = satisfies(P1, rows, rhs)
        rules = {
            'P1': lambda k, K: [1] + [0] * (K - 1),
            'GenesisDump': lambda k, K: [0] * (K - 1) + [1],
            'Grandparent': lambda k, K: [1] if K == 1 else [0, 1] + [0] * (K - 2),
            'Split': lambda k, K: [1] if K == 1 else [F(1, 2), F(1, 2)] + [0] * (K - 2),
            'Annihilate': lambda k, K: [0] * K}
        u["rules"] = {nm: [satisfies(vec(rl), rowsE2, rhsE2), satisfies(vec(rl), NI), satisfies(vec(rl), CNa), satisfies(vec(rl), CNp)] for nm, rl in rules.items()}
        rng = np.random.default_rng(77 + nmax); cnt = {"tables": 300, "E2": 0, "NI": 0, "CNparent": 0, "P1": 0}
        for _ in range(300):
            tab = {}
            for K in range(1, maxK + 1):
                x = [int(v) for v in rng.integers(-3, 4, size=K)]
                x[-1] += 1 - sum(x)  # normalize on the deepest coordinate (different from producer)
                tab[K] = x
            w = vec(lambda k, K: tab[K])
            a, b, c = satisfies(w, rowsE2, rhsE2), satisfies(w, NI), satisfies(w, CNp)
            isP1 = all(tab[K] == [1] + [0] * (K - 1) for K in tab)
            cnt["E2"] += a; cnt["NI"] += b; cnt["CNparent"] += c; cnt["P1"] += isP1
            if c != isP1:
                viol.append("random table: CN-parent != P1")
        u["random_tables"] = cnt
        if nmax == 7:
            k0 = max(k for k in keys if info[k][3] == 3)  # a depth-3 carrier (different choice from the producer)
            w = vec(lambda k, K: [0, 1, 0] if k == k0 else [1] + [0] * (K - 1))
            cert["_r8"] = satisfies(w, CNp)
        cert["universes"]["U%d" % nmax] = u
    # hand-written instances as explicit matrices
    def T_matrix(n, col_l, target):  # E3: identity on non-l columns; column l given
        M = np.eye(n, dtype=object) * F(1); M[:, col_l] = [F(x) for x in target]; return M
    # Y1/Y2: chain 0-1-2, leaf 2; parent cone {1,2} re-rooted; J embeds cone vertex j -> 1+j
    J = np.zeros((3, 2), dtype=object); J[1, 0] = F(1); J[2, 1] = F(1)
    J = np.where(J == 0, F(0), J)
    for key, tW, tX in (("Y1.dump_residual", [1, 0, 0], [1, 0]), ("Y2.split_residual", [F(1, 2), F(1, 2), 0], [1, 0])):
        TW = T_matrix(3, 2, tW); TX = T_matrix(2, 1, tX)
        res = (TW.dot(J) - J.dot(TX))[:, 1]
        cert["instances"][key] = [str(res[1]), str(res[0])]  # [at parent, at Genesis]
    # Y3 cherry 0->1, 1->{2,3}; sibling rule column 2 -> e_3; cone of 1 = {1,2,3} -> {0,1,2}
    TW = T_matrix(4, 2, [0, 0, 0, 1]); TX = T_matrix(3, 1, [0, 0, 1])
    J = np.array([[F(0)] * 3, [F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]], dtype=object)
    sq = bool(np.all(TW.dot(J) == J.dot(TX))); e2 = sum(TW[:, 2]) == 1; e4 = all(TW[v, 2] == 0 for v in (2, 3))
    cert["instances"]["Y3.sibling"] = [sq, bool(e2), bool(e4)]
    TW = T_matrix(3, 2, [0, 0, 0]); TX = T_matrix(2, 1, [0, 0])
    J = np.array([[F(0), F(0)], [F(1), F(0)], [F(0), F(1)]], dtype=object)
    cert["instances"]["Y4.annihilate"] = [str(sum(TW[:, 2])), bool(np.all(TW.dot(J) == J.dot(TX))), True]
    t5 = {0: [1, 3], 1: [2], 2: [], 3: []}
    cert["instances"]["Y5.P1_counts"] = [len(prefix_subs(t5, 2)), len([a for a in path_to_root(t5, 2)[1:-1]])]
    u7 = cert["universes"]["U7"]; C = cert["controls"]
    def rj(cond): return "REJECTED" if not cond else "ACCEPTED_WRONGLY"
    C["R1_genesis_dump_satisfies_CNparent"] = rj(u7["rules"]["GenesisDump"][3])
    C["R2_grandparent_satisfies_CNparent"] = rj(u7["rules"]["Grandparent"][3])
    C["R3_split_satisfies_CNparent"] = rj(u7["rules"]["Split"][3])
    C["R4_annihilation_satisfies_E2"] = rj(u7["rules"]["Annihilate"][0])
    C["R5_sibling_rule_satisfies_E4"] = rj(cert["instances"]["Y3.sibling"][2])
    C["R6_NI_alone_forces_P1"] = rj(u7["dims"]["E2+NI"] == 0)
    C["R7_CN_without_E2_forces_P1"] = rj(u7["dims"]["CN"] == 0 or u7["dims"]["NI+CN"] == 0)
    C["R8_P1_with_one_substituted_carrier_satisfies_CNparent"] = rj(cert.pop("_r8"))
    for nm in ("U7", "U8"):
        if cert["universes"][nm]["rules"]["P1"] != [True] * 4:
            viol.append("P1 fails in " + nm)
    open(sys.argv[1], "w").write(json.dumps(cert, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
