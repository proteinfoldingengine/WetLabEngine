"""receiver_identification draft 1 freeze: CHECKER (independent algorithm; does not import the producer).
Bitmask enumeration of ancestor-closed sets, owner = deepest member of the ancestor set, pushforward as a
0/1 numpy matrix, lineage as matrix products, vectorized over all grades. Also bounded evidence and
rejecting controls (FREEZE.md sections 3-5)."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_review")
RNG = np.random.default_rng(20261018)


def all_trees(n):
    if n == 1:
        return [[-1]]
    return [t + [p] for t in all_trees(n - 1) for p in range(n - 1)]


def ancestors(par):
    A = []
    for z in range(len(par)):
        s, c = {z}, z
        while par[c] >= 0:
            c = par[c]; s.add(c)
        A.append(s)
    return A


def closed_masks(par):
    n = len(par)
    return [m for m in range(1 << n) if m & 1 and all(par[z] < 0 or (m >> par[z]) & 1 for z in range(n) if (m >> z) & 1)]


def members(m, n):
    return [z for z in range(n) if (m >> z) & 1]


def pmatrix(par, keep_from, keep_to):
    # matrix from coordinates keep_from to keep_to; owner = deepest (largest label) ancestor inside keep_to
    A = ancestors(par)
    M = np.zeros((len(keep_to), len(keep_from)), dtype=np.int64)
    for j, z in enumerate(keep_from):
        M[keep_to.index(max(A[z] & set(keep_to))), j] = 1
    return M


def grid(n, g):
    if n == 0:
        return np.zeros((1, 0), dtype=np.int64)
    return np.array(list(itertools.product(range(g), repeat=n)), dtype=np.int64).reshape(-1, n)


def tvf(p, q):
    return sum(abs(p.get(k, F(0)) - q.get(k, F(0))) for k in set(p) | set(q)) / 2


def convf(p, q):
    o = {}
    for i in p:
        for j in q:
            o[i + j] = o.get(i + j, F(0)) + p[i] * q[j]
    return o


def instances():
    V = {}
    par = [-1, 0, 1]; M = pmatrix(par, [0, 1, 2], [0, 1])
    a, b = M @ np.array([1, 0, 1]), M @ np.array([1, 0, 0])
    V["E1.mu_x"] = [str(int(v)) for v in a]; V["E1.mu_xp"] = [str(int(v)) for v in b]
    V["E1.owner"] = [[0, 1][i] for i in np.nonzero(a - b)[0]]
    par = [-1, 0, 0]; M = pmatrix(par, [0, 1, 2], [0])
    d = M @ np.array([0, 1, 0]) - M @ np.array([0, 0, 1])
    V["E2.owner"] = [int(i) for i in np.nonzero(d)[0]]; V["E2.equal"] = bool(not d.any())
    par = [-1, 0, 1, 2]; chain = [[0, 1, 2, 3], [0, 1, 2], [0, 1], [0]]
    L = np.eye(4, dtype=np.int64); H, D = [], []
    for k in range(1, 4):
        L = pmatrix(par, chain[k - 1], chain[k]) @ L
        diff = L @ np.array([0, 0, 0, 1])
        nz = np.nonzero(diff)[0]; assert len(nz) == 1
        H.append(chain[k][nz[0]]); D.append(str(int(diff[nz[0]])))
    V["E3.holders"], V["E3.diffs"] = H, D
    par = [-1, 0, 0]; chain = [[0, 1, 2], [0, 1], [0]]; L = np.eye(3, dtype=np.int64); ms = None
    for k in range(1, 3):
        L = pmatrix(par, chain[k - 1], chain[k]) @ L
        if ms is None and not (L @ np.array([0, 1, -1])).any():
            ms = k
    V["E3.merge_step"] = ms
    pa = {0: F(1, 2), 1: F(1, 2)}
    pu, qu = {0: F(1)}, {1: F(1)}
    V["E4a.tv_src"] = str(tvf(pu, qu)); V["E4a.tv_owner"] = str(tvf(convf(pa, pu), convf(pa, qu)))
    V["E4a.tv_point"] = str(tvf(convf({0: F(1)}, pu), convf({0: F(1)}, qu)))
    pu, qu = {0: F(1, 2), 1: F(1, 2)}, {0: F(1, 4), 1: F(3, 4)}
    V["E4b.tv_src"] = str(tvf(pu, qu)); V["E4b.tv_owner"] = str(tvf(convf(pa, pu), convf(pa, qu)))
    # E4c as 2x2 joint arrays [x_a, x_u]
    P = np.array([[F(1, 2), F(0)], [F(0), F(1, 2)]], dtype=object); Q = np.array([[F(0), F(1, 2)], [F(1, 2), F(0)]], dtype=object)
    tva = lambda u, v: sum(abs(x - y) for x, y in zip(u, v)) / 2
    V["E4c.tv_src_marg"] = str(tva(P.sum(axis=0), Q.sum(axis=0)))
    sp = [sum(P[i, j] for i in range(2) for j in range(2) if i + j == s) for s in range(3)]
    sq = [sum(Q[i, j] for i in range(2) for j in range(2) if i + j == s) for s in range(3)]
    V["E4c.tv_owner"] = str(tva(sp, sq)); V["E4c.tv_joint_before"] = str(tva(P.ravel(), Q.ravel()))
    # Prop 5(c) as 4x4 matrices on |u a>, index 2u+a
    C = np.zeros((4, 4))
    for u in range(2):
        for a in range(2):
            C[2 * u + (a + u) % 2, 2 * u + a] = 1
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], float)
    V["E5.cnot"] = bool(np.array_equal(C, CNOT))
    psi = C @ np.kron(np.array([1, 1]) / np.sqrt(2), np.array([1, 0]))
    rho = np.outer(psi, psi.conj()).reshape(2, 2, 2, 2)
    red = np.einsum("uaub->ab", rho)
    V["E5.owner_reduced"] = [[str(F(float(red[i, j])).limit_denominator(64)) for j in range(2)] for i in range(2)]
    ind = [np.array([[1 if (p, q) == (i, j) else 0 for q in range(3)] for p in range(2)]) for i in range(2) for j in range(3)]
    prod = [np.outer(np.eye(2)[i], np.eye(3)[j]) for i in range(2) for j in range(3)]
    V["P1.factor"] = bool(all(np.array_equal(a, b) for a, b in zip(ind, prod)) and len({(i, j) for i in range(2) for j in range(3)}) == 6)
    return V


def exhaustive():
    C = {"t2_pairs": 0, "t2_W_checks": 0, "t2_single": 0, "t2_cancel": 0, "t2_viol": 0,
         "t3_cases": 0, "t3_viol": 0, "p4_triples": 0, "p4_viol": 0, "trees": 0, "retained_sets": 0}
    for n in range(1, 6):
        for par in all_trees(n):
            C["trees"] += 1
            masks = closed_masks(par); C["retained_sets"] += len(masks)
            full = list(range(n)); X = grid(n, 3)
            for m in masks:
                keep = members(m, n); rem = [z for z in full if z not in keep]
                M = pmatrix(par, full, keep)
                R = grid(len(rem), 3)
                # all pairs: x in X, x' = x with removed coords replaced by R rows
                Xp = np.repeat(X, len(R), axis=0); Xq = Xp.copy()
                if rem:
                    Xq[:, rem] = np.tile(R, (len(X), 1))
                C["t2_pairs"] += len(Xp)
                Dout = Xp @ M.T - Xq @ M.T
                Din = Xp - Xq
                # O from fiber sums of removed differences (owner index of each removed atom)
                O = np.zeros_like(Dout)
                for z in rem:
                    O[:, int(np.argmax(M[:, z]))] += Din[:, z]
                C["t2_viol"] += int(((Dout != 0) != (O != 0)).any(axis=1).sum())
                for w in range(1, 1 << len(keep)):
                    idx = [i for i in range(len(keep)) if (w >> i) & 1]
                    C["t2_W_checks"] += len(Xp)
                    C["t2_viol"] += int(((Dout[:, idx] != 0).any(axis=1) != (O[:, idx] != 0).any(axis=1)).sum())
                nd = (Din != 0).sum(axis=1)
                single = nd == 1
                C["t2_single"] += int(single.sum())
                for i in np.nonzero(single)[0]:
                    z = int(np.nonzero(Din[i])[0][0])
                    want = np.zeros(len(keep), bool); want[int(np.argmax(M[:, z]))] = True
                    C["t2_viol"] += int(not np.array_equal(O[i] != 0, want))
                C["t2_cancel"] += int(((nd > 0) & ~(O != 0).any(axis=1)).sum())
            # T3: chains of 1..3 strictly decreasing closed masks below full
            fm = (1 << n) - 1
            def chains(prev, depth):
                for m in masks:
                    if m != prev and (m & prev) == m:
                        yield [m]
                        if depth > 1:
                            for rest in chains(m, depth - 1):
                                yield [m] + rest
            for ch in chains(fm, 3):
                keeps = [full] + [members(m, n) for m in ch]
                Ls, L = [], np.eye(n, dtype=np.int64)
                for k in range(1, len(keeps)):
                    L = pmatrix(par, keeps[k - 1], keeps[k]) @ L; Ls.append(L)
                A = ancestors(par)
                for u in [z for z in full if z not in keeps[-1]]:
                    for v in range(3):
                        sel = X[:, u] != v
                        Xa = X[sel]; Xb = Xa.copy(); Xb[:, u] = v
                        C["t3_cases"] += len(Xa)
                        bad = np.zeros(len(Xa), bool)
                        for k, L in enumerate(Ls, 1):
                            Dk = Xa @ L.T - Xb @ L.T
                            holder = keeps[k].index(max(A[u] & set(keeps[k])))
                            exp = np.zeros_like(Dk); exp[:, holder] = Xa[:, u] - v
                            bad |= (Dk != exp).any(axis=1)
                        C["t3_viol"] += int(bad.sum())
    vals = [F(0), F(1, 3), F(2, 3), F(1)]
    dists = [p for p in itertools.product(vals, repeat=3) if sum(p) == 1]
    unif = [F(1, 3)] * 3
    def cv(p, q):
        o = [F(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                o[i + j] += a * b
        return o
    tvl = lambda p, q: sum(abs(a - b) for a, b in zip(p, q)) / 2
    for pu in dists:
        for qu in dists:
            for pa in dists:
                C["p4_triples"] += 1
                src, own = tvl(pu, qu), tvl(cv(pa, pu), cv(pa, qu))
                point = sum(1 for v in pa if v) == 1
                if own > src or (point and own != src):
                    C["p4_viol"] += 1
                jp = [a * b for a in cv(pa, pu) for b in unif]; jq = [a * b for a in cv(pa, qu) for b in unif]
                if tvl(jp, jq) != own:
                    C["p4_viol"] += 1
    return C


def rand_tree(n):
    return [-1] + [int(RNG.integers(0, i)) for i in range(1, n)]


def rand_closed(par, below=None):
    n = len(par); base = list(range(n)) if below is None else below
    keep = {0}
    for z in base:
        if z != 0 and par[z] in keep and RNG.random() < 0.6:
            keep.add(z)
    return sorted(keep)


def bounded():
    B = {"B2_cases": 0, "B2_viol": 0, "B3_cases": 0, "B3_viol": 0, "B4_cases": 0, "B4_viol": 0,
         "B5a_cases": 0, "B5a_viol": 0, "B5b_cases": 0, "B5b_viol": 0}
    for _ in range(3000):
        n = int(RNG.integers(6, 10)); par = rand_tree(n); keep = rand_closed(par)
        full = list(range(n)); rem = [z for z in full if z not in keep]; M = pmatrix(par, full, keep)
        x = RNG.integers(0, 5, n); xp = x.copy(); xp[rem] = RNG.integers(0, 5, len(rem))
        if RNG.random() < 0.5 and rem:
            xp = x.copy(); u = int(RNG.choice(rem)); xp[u] = (x[u] + 1 + RNG.integers(0, 4)) % 5
        d = M @ (x - xp); O = np.zeros(len(keep), np.int64)
        for z in rem:
            O[int(np.argmax(M[:, z]))] += x[z] - xp[z]
        bad = not np.array_equal(d != 0, O != 0)
        nz = np.nonzero(x - xp)[0]
        if len(nz) == 1:
            w = np.zeros(len(keep), bool); w[int(np.argmax(M[:, nz[0]]))] = True
            bad |= not np.array_equal(O != 0, w)
        B["B2_cases"] += 1; B["B2_viol"] += int(bad)
    for _ in range(2000):
        n = int(RNG.integers(6, 10)); par = rand_tree(n); keeps = [list(range(n))]
        for _k in range(int(RNG.integers(1, 5))):
            keeps.append(rand_closed(par, keeps[-1]))
        u = int(RNG.integers(0, n)); x = RNG.integers(0, 5, n); xp = x.copy(); xp[u] = (x[u] + 1) % 5
        L = np.eye(n, dtype=np.int64); A = ancestors(par); bad = False
        for k in range(1, len(keeps)):
            L = pmatrix(par, keeps[k - 1], keeps[k]) @ L
            dk = L @ (x - xp); h = keeps[k].index(max(A[u] & set(keeps[k])))
            e = np.zeros(len(keeps[k]), np.int64); e[h] = x[u] - xp[u]
            bad |= not np.array_equal(dk, e)
        B["B3_cases"] += 1; B["B3_viol"] += int(bad)
    def rdist(k):
        w = [int(v) for v in RNG.integers(0, 6, k)]
        if sum(w) == 0:
            w[0] = 1
        return [F(v, sum(w)) for v in w]
    def cv(p, q):
        o = [F(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                o[i + j] += a * b
        return o
    tvl = lambda p, q: sum(abs(a - b) for a, b in zip(p, q)) / 2
    for _ in range(2000):
        pu, qu, pa = rdist(4), rdist(4), rdist(4)
        own = tvl(cv(pa, pu), cv(pa, qu))
        joint_before = tvl([a * b for a in pa for b in pu], [a * b for a in pa for b in qu])
        B["B4_cases"] += 1; B["B4_viol"] += int(own > tvl(pu, qu) or own > joint_before)
    Cm = np.zeros((9, 9))
    for u in range(3):
        for a in range(3):
            Cm[3 * u + (a + u) % 3, 3 * u + a] = 1
    Cfull = np.kron(Cm, np.eye(3))
    for _ in range(200):
        Z = RNG.normal(size=(3, 3)) + 1j * RNG.normal(size=(3, 3)); Op = np.kron(np.eye(9), Z)
        B["B5a_cases"] += 1; B["B5a_viol"] += int(np.abs(Cfull @ Op - Op @ Cfull).max() > 1e-12)
    for _ in range(200):
        n = int(RNG.integers(3, 7)); par = rand_tree(n); keep = rand_closed(par); full = list(range(n))
        x = RNG.integers(0, 3, n); y = x.copy()
        M = pmatrix(par, full, keep)
        for z in full:
            if z not in keep:
                y[keep[int(np.argmax(M[:, z]))]] += y[z]   # controlled-add move into owner (unbounded = below capacity)
        B["B5b_cases"] += 1; B["B5b_viol"] += int(not np.array_equal(y[keep], M @ x))
    return B


def controls():
    R = {}
    par = [-1, 0, 1]; M = pmatrix(par, [0, 1, 2], [0, 1])
    d = M @ (np.array([1, 0, 1]) - np.array([1, 0, 0]))
    R["R1_wrong_owner_root"] = "REJECTED" if d[0] == 0 else "ACCEPTED"
    # copy rule: x_u written into both r(u) and the root (star-free path 0-1-2, u = 2, r(u) = 1)
    xa, xb = np.array([1, 0, 1]), np.array([1, 0, 0])
    cp = lambda x: np.array([x[0] + x[2], x[1] + x[2]])
    R["R2_copy_unique_holder"] = "REJECTED" if int((cp(xa) != cp(xb)).sum()) != 1 else "ACCEPTED"
    # swapped lineages: tree 0-1, 0-2-3; chain {0,1,2} then {0,1}; difference at u = 3 claimed at L(v), v = 1... use v whose lineage differs
    par = [-1, 0, 0, 2]; chain = [[0, 1, 2, 3], [0, 1, 2], [0, 1]]
    L = np.eye(4, dtype=np.int64)
    for k in range(1, 3):
        L = pmatrix(par, chain[k - 1], chain[k]) @ L
    dk = L @ np.array([0, 0, 0, 1]); hu = chain[2][int(np.argmax(dk))]
    hv = chain[2][int(np.argmax(L[:, 1]))]
    R["R3_swapped_lineage"] = "REJECTED" if hv != hu else "ACCEPTED"
    pa = {0: F(1, 2), 1: F(1, 2)}
    R["R4_equality_nonpoint_prior"] = "REJECTED" if tvf(convf(pa, {0: F(1)}), convf(pa, {1: F(1)})) != 1 else "ACCEPTED"
    # correlated boundary: owner TV 1 vs source marginal TV 0
    jp = {(0, 0): F(1, 2), (1, 1): F(1, 2)}; jq = {(0, 1): F(1, 2), (1, 0): F(1, 2)}
    mg = lambda j: {k: sum(v for (a, u), v in j.items() if u == k) for k in range(2)}
    sm = lambda j: {k: sum(v for (a, u), v in j.items() if a + u == k) for k in range(3)}
    R["R5_marginal_bound_correlated"] = "REJECTED" if tvf(sm(jp), sm(jq)) > tvf(mg(jp), mg(jq)) else "ACCEPTED"
    Cm = np.zeros((4, 4))
    for u in range(2):
        for a in range(2):
            Cm[2 * u + (a + u) % 2, 2 * u + a] = 1
    Z = RNG.normal(size=(2, 2)) + 1j * RNG.normal(size=(2, 2)); Op = np.kron(np.eye(2), Z)
    R["R6_commutes_on_owner"] = "REJECTED" if np.abs(Cm @ Op - Op @ Cm).max() > 1e-9 else "ACCEPTED"
    par = [-1, 0, 1]; keep = [0, 1]
    xa, xb = np.array([0, 1, 0]), np.array([0, 0, 0])
    R["R7_retained_diff_uninformed"] = "REJECTED" if (xa[keep] != xb[keep]).any() else "ACCEPTED"
    return R


def main():
    rsha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    cert = {"meta": {"role": "checker", "result_sha256": rsha, "method": "bitmask sets, numpy pushforward matrices, lineage products"},
            "values": instances(), "universe": exhaustive(), "bounded": bounded(), "controls": controls()}
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in ("universe", "bounded", "controls")}, sort_keys=True))


if __name__ == "__main__":
    main()
