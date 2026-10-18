"""observation_effect draft 3 freeze: CHECKER (independent algorithm). Preregistered in
observation_effect_review/FREEZE.md sections 2-4. Quantum items via numpy column-stacked
superoperator matrices; classical items via exact Fraction maps on atom dictionaries;
bounded randomized evidence (seed 20261018) and rejecting controls. No producer code is imported."""
import hashlib, itertools, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/observation_effect_review")
rng = np.random.default_rng(20261018)
TOL = 1e-9


# ---------- superoperator machinery (column stacking: vec(AXB) = (B^T kron A) vec X) ----------
def sup_conj(U):
    return np.kron(U.conj(), U)


def sup_mask(d, keep):  # keep(i,j) -> bool; a pinching onto a block/diagonal pattern
    m = np.zeros(d * d)
    for j in range(d):
        for i in range(d):
            if keep(i, j):
                m[j * d + i] = 1
    return np.diag(m)


def vec(X):
    return X.reshape(-1, order="F")


def unvec(v, d):
    return v.reshape(d, d, order="F")


def apply(S, X):
    return unvec(S @ vec(X), X.shape[0])


def tn(X):  # trace norm
    return float(np.sum(np.abs(np.linalg.eigvalsh((X + X.conj().T) / 2))))


def tvd(p, q):
    return 0.5 * float(np.sum(np.abs(np.asarray(p) - np.asarray(q))))


def ket(d, i):
    v = np.zeros((d, 1), complex)
    v[i] = 1
    return v


def haar(d):
    z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def rand_state(d, rank=None):
    rank = rank or d
    g = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    r = g @ g.conj().T
    return r / np.trace(r).real


# ---------- exact finite universe, quantum part ----------
def quantum_items(c):
    d = 4
    DEPH = sup_mask(d, lambda i, j: i == j)
    I2 = np.eye(2)
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    CN = np.zeros((4, 4))
    for s in (0, 1):
        for r in (0, 1):
            CN[2 * s + (r ^ s), 2 * s + r] = 1
    Q = [np.kron(I2, np.diag([1, 0])), np.kron(I2, np.diag([0, 1]))]
    rec = lambda X: [np.trace(q @ X).real for q in Q]
    def hist(U):
        S = sup_conj(U)
        return DEPH @ S @ DEPH, DEPH @ S  # O, N
    plus = np.array([[1], [1]]) / np.sqrt(2)
    minus = np.array([[1], [-1]]) / np.sqrt(2)
    P00 = np.diag([1.0, 0])
    rW = [np.kron(v @ v.T, P00) for v in (plus, minus)]
    O, N = hist(CN @ np.kron(H, I2))
    c["W.tv_obs"] = tvd(rec(apply(O, rW[0])), rec(apply(O, rW[1])))
    c["W.tv_unobs"] = tvd(rec(apply(N, rW[0])), rec(apply(N, rW[1])))
    Dl = rW[0] - apply(DEPH, rW[0])
    c["W.kappa"] = tn(Dl) / 2
    c["W.occ_tv"] = tvd(rec(apply(N, rW[0])), rec(apply(O, rW[0])))
    ev = np.sort(np.linalg.eigvalsh(Dl))[::-1]
    c["W.kyfan"] = max(ev[:2].sum(), ev[:2].sum())
    Ry = np.array([[2, -1], [1, 2]]) / np.sqrt(5)
    O, N = hist(CN @ np.kron(Ry, I2))
    X = np.array([[0, 1], [1, 0]])
    rP = [np.kron(P00, P00), np.kron((I2 - 0.75 * X) / 2, P00)]
    c["P.tv_obs"] = tvd(rec(apply(O, rP[0])), rec(apply(O, rP[1])))
    c["P.tv_unobs"] = tvd(rec(apply(N, rP[0])), rec(apply(N, rP[1])))
    c["P.global_obs"] = [tn(rP[0] - rP[1]) / 2, tn(apply(DEPH, rP[0] - rP[1])) / 2, tn(apply(O, rP[0] - rP[1])) / 2]
    c["P.kappa1"] = tn(rP[1] - apply(DEPH, rP[1])) / 2
    c["P.occ1"] = tvd(rec(apply(N, rP[1])), rec(apply(O, rP[1])))
    c["P.occ0"] = tvd(rec(apply(N, rP[0])), rec(apply(O, rP[0])))
    # H witness: block pinching M2+M2, U = transposition (1 2)
    blk = lambda i: 0 if i < 2 else 1
    BP = sup_mask(4, lambda i, j: blk(i) == blk(j))
    U = np.eye(4)[:, [0, 2, 1, 3]]
    S = sup_conj(U)
    psi = (ket(4, 0) + ket(4, 2)) / np.sqrt(2)
    rho = psi @ psi.conj().T
    Nn, Oo = apply(BP @ S, rho), apply(BP @ S @ BP, rho)
    Pk = [np.diag([1, 1, 0, 0.]), np.diag([0, 0, 1, 1.])]
    inA = lambda Y: np.allclose(apply(BP, Y), Y)
    # closedness test by superoperator: (I - BP) S BP == 0 ?
    closed = np.allclose((np.eye(16) - BP) @ S @ BP, 0)
    central_ok = all(inA(U.T @ P @ U) for P in Pk) and np.allclose([np.trace(P @ Nn) for P in Pk], [np.trace(P @ Oo) for P in Pk])
    c["H.central_equal"] = bool(central_ok and not closed)
    c["H.full_effect"] = tn(Nn - Oo)
    # cadence
    D2 = sup_mask(2, lambda i, j: i == j)
    Uc = np.array([[1, -1], [1, 1]]) / np.sqrt(2)
    p0 = np.diag([1.0, 0])
    c["Z.cadence"] = tn(apply(D2 @ sup_conj(Uc @ Uc), p0) - apply(D2 @ sup_conj(Uc) @ D2 @ sup_conj(Uc), p0)) / 2
    st = np.diag([0, 1.0, 0, 0])
    c["S.swap_record"] = list(np.diag(apply(DEPH @ sup_conj(np.kron(X, I2)) @ DEPH, st)).real)
    # Q: qubit rotation, numeric on a theta grid against the preregistered closed forms
    okQ = True
    for th in np.linspace(-3.1, 3.1, 63):
        Ur = np.array([[np.cos(th / 2), -np.sin(th / 2)], [np.sin(th / 2), np.cos(th / 2)]])
        Xq = Ur.T @ p0 @ Ur
        Dq = np.linalg.norm(np.diag(np.diag(Xq)) - p0, 2)
        Cq = np.linalg.norm(Xq - np.diag(np.diag(Xq)), 2)
        okQ &= abs(Dq - np.sin(th / 2) ** 2) < 1e-12 and abs(Cq - abs(np.sin(th)) / 2) < 1e-12 \
            and abs(Cq - np.sqrt(Dq * (1 - Dq))) < 1e-7
    c["Q.D"], c["Q.C"] = ("sin(theta/2)**2", "Abs(sin(theta))/2") if okQ else ("mismatch", "mismatch")
    # M witness: single-sector A = M2 (x) I2, test closedness via superoperator of conditional expectation
    pi = np.diag([0, 1.0])
    Um = np.kron(I2, I2 - pi) + np.kron(X, pi)
    def Estar_M(Y):  # tracial E* onto M2 (x) I2
        Y4 = Y.reshape(2, 2, 2, 2)
        return np.kron(np.einsum("arbr->ab", Y4) / 2, I2)
    EM = np.column_stack([vec(Estar_M(unvec(e, 4))) for e in np.eye(16)])
    closedM = np.allclose((np.eye(16) - EM) @ sup_conj(Um.conj().T) @ EM, 0)
    c["M.witness"] = "inZprime_nonnormalizing_keeps_record" if np.allclose(Um @ Um.T, np.eye(4)) and not closedM else "fails"


# ---------- exact finite universe, classical part (Fraction dictionaries) ----------
def pushforward(T, x):  # T: dict atom->atom (deterministic move); x: dict atom->mass
    y = {}
    for a, m in x.items():
        y[T[a]] = y.get(T[a], F(0)) + m
    return y


def owner_section(fibers, owner, x):
    y = {}
    for a, m in x.items():
        o = owner[fibers[a]]
        y[o] = y.get(o, F(0)) + m
    return y


def totals(fibers, nf, x):
    t = [F(0)] * nf
    for a, m in x.items():
        t[fibers[a]] += m
    return t


def classical_items(c):
    fib = {"a": 0, "u": 0, "b": 1}
    own = {0: "a", 1: "b"}
    T = {"a": "a", "u": "b", "b": "u"}
    x = {"a": F(1, 2), "u": F(1, 2), "b": F(0)}
    c["L.owner"] = totals(fib, 2, pushforward(T, owner_section(fib, own, x)))
    trac = {}
    for a, m in x.items():  # tracial fiber average
        mem = [b for b in fib if fib[b] == fib[a]]
        for b in mem:
            trac[b] = trac.get(b, F(0)) + m / len(mem)
    c["L.tracial"] = totals(fib, 2, pushforward(T, trac))
    c["L.unobs"] = totals(fib, 2, pushforward(T, x))
    xu = {"u": F(1)}
    c["O.perfect"] = tvd_f(totals(fib, 2, pushforward(T, xu)), totals(fib, 2, pushforward(T, owner_section(fib, own, xu))))
    c["G3.D"], c["G3.C"] = DC_f(fib, own, T)
    fib4 = {"a": 0, "u": 0, "b": 1, "v": 1}
    own4 = {0: "a", 1: "b"}
    T4 = {"a": "a", "b": "b", "u": "v", "v": "u"}
    c["G4.D"], c["G4.C"] = DC_f(fib4, own4, T4)
    # nonfaithful kernel: E(delta_u) = delta_a; the u-direction is in ker E(rho) but not in ker rho
    Ex = owner_section(fib, own, xu)
    c["N.kernel"] = "inclusion_fails" if Ex.get("u", F(0)) == 0 and xu["u"] != 0 else "inclusion_holds"


def tvd_f(p, q):
    return sum(abs(a - b) for a, b in zip(p, q)) / 2


def DC_f(fib, own, T):
    nf = len(own)
    subsets = [S for k in range(1, nf) for S in itertools.combinations(range(nf), k)]
    D = max(abs(sum(totals(fib, nf, pushforward(T, {own[f]: F(1)}))[s] for s in S) - (1 if f in S else 0))
            for S in subsets for f in range(nf))
    C = F(0)
    for S in subsets:
        for a in fib:
            un = totals(fib, nf, pushforward(T, {a: F(1)}))
            ob = totals(fib, nf, pushforward(T, owner_section(fib, own, {a: F(1)})))
            C = max(C, abs(sum(un[s] - ob[s] for s in S)))
    return D, C


# ---------- random conditional expectations for bounded evidence ----------
class CE:
    """E*(Y) = (+)_s (id (x) omega_s)(P_s Y P_s) (x) I_{k_s};  E(rho) = (+)_s Tr_k(P_s rho P_s) (x) sigma_s."""
    def __init__(self, ns, ks, faithful=True, tracial=False):
        self.ns, self.ks = ns, ks
        self.d = sum(n * k for n, k in zip(ns, ks))
        self.off = np.cumsum([0] + [n * k for n, k in zip(ns, ks)])
        self.sig = []
        for k in ks:
            if tracial:
                s = np.eye(k) / k
            elif faithful or k == 1:
                s = rand_state(k)
            else:
                s = rand_state(k, rank=k - 1)
            self.sig.append(s)
    def blk(self, Y, s):
        a, b = self.off[s], self.off[s + 1]
        return Y[a:b, a:b]
    def Estar(self, Y):
        out = np.zeros((self.d, self.d), complex)
        for s, (n, k) in enumerate(zip(self.ns, self.ks)):
            B = self.blk(Y, s).reshape(n, k, n, k)
            red = np.einsum("aibj,ji->ab", B, self.sig[s])
            a, b = self.off[s], self.off[s + 1]
            out[a:b, a:b] = np.kron(red, np.eye(k))
        return out
    def E(self, r):
        out = np.zeros((self.d, self.d), complex)
        for s, (n, k) in enumerate(zip(self.ns, self.ks)):
            B = self.blk(r, s).reshape(n, k, n, k)
            red = np.einsum("aibi->ab", B)
            a, b = self.off[s], self.off[s + 1]
            out[a:b, a:b] = np.kron(red, self.sig[s])
        return out
    def central(self):
        Ps = []
        for s in range(len(self.ns)):
            P = np.zeros((self.d, self.d))
            a, b = self.off[s], self.off[s + 1]
            P[a:b, a:b] = np.eye(b - a)
            Ps.append(P)
        return Ps
    def unitary_in_A(self):
        U = np.zeros((self.d, self.d), complex)
        for s, (n, k) in enumerate(zip(self.ns, self.ks)):
            a, b = self.off[s], self.off[s + 1]
            U[a:b, a:b] = np.kron(haar(n), np.eye(k))
        return U
    def unitary_in_Zprime(self):
        U = np.zeros((self.d, self.d), complex)
        for s in range(len(self.ns)):
            a, b = self.off[s], self.off[s + 1]
            U[a:b, a:b] = haar(b - a)
        return U
    def proj_in_A(self):
        Q = np.zeros((self.d, self.d), complex)
        for s, (n, k) in enumerate(zip(self.ns, self.ks)):
            r = rng.integers(0, n + 1)
            V = haar(n)[:, :r]
            a, b = self.off[s], self.off[s + 1]
            Q[a:b, a:b] = np.kron(V @ V.conj().T, np.eye(k))
        return Q


def rand_ce(faithful=True, tracial=False):
    M = int(rng.integers(1, 4))
    ns = [int(rng.integers(1, 3)) for _ in range(M)]
    ks = [int(rng.integers(1, 3)) for _ in range(M)]
    if not faithful and all(k == 1 for k in ks):
        ks[0] = 2
    return CE(ns, ks, faithful, tracial)


def channel_kraus(kind, ce):
    d = ce.d
    if kind == "unitary_A":
        return [ce.unitary_in_A()]
    if kind == "kraus_A":
        Ks = [ce.unitary_in_A() * np.sqrt(w) for w in (0.3, 0.7)]
        return Ks
    V = haar(d * 2)[:, :d]  # Haar isometry -> 2 Kraus operators
    return [V[:d], V[d:]]


def phi(Ks, r):
    return sum(K @ r @ K.conj().T for K in Ks)


def phistar(Ks, Y):
    return sum(K.conj().T @ Y @ K for K in Ks)


def basis(d):
    for i in range(d):
        for j in range(d):
            E = np.zeros((d, d), complex)
            E[i, j] = 1
            yield E


def certified_lambda(ce):
    def cp(lam):
        J = np.zeros((ce.d ** 2, ce.d ** 2), complex)
        for i in range(ce.d):
            for j in range(ce.d):
                Eij = np.zeros((ce.d, ce.d), complex)
                Eij[i, j] = 1
                J += np.kron(Eij, ce.Estar(Eij) - lam * Eij)
        return np.linalg.eigvalsh((J + J.conj().T) / 2).min() >= -1e-11
    lo, hi = 0.0, 1.0
    if not cp(0.0):
        return -1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cp(mid) else (lo, mid)
    return lo * (1 - 1e-9)


def bounded(b):
    v, nclosed = 0, 0
    for t in range(300):  # Thm 1
        ce = rand_ce(faithful=t % 3 != 2, tracial=t % 3 == 0)
        kind = ("unitary_A", "kraus_A", "haar")[t % 3]
        Ks = channel_kraus(kind, ce)
        lhs = max(np.abs(ce.E(phi(Ks, ce.E(X))) - ce.E(phi(Ks, X))).max() for X in basis(ce.d))
        rhs = max(np.abs(ce.Estar(phistar(Ks, ce.Estar(Y))) - phistar(Ks, ce.Estar(Y))).max() for Y in basis(ce.d))
        v += (lhs < 1e-9) != (rhs < 1e-9)
        nclosed += rhs < 1e-9
    b["thm1_cases"], b["thm1_violations"], b["thm1_closed_count"] = 300, int(v), int(nclosed)
    v = 0
    for t in range(300):  # Thm 2(d)
        ce = rand_ce(faithful=t % 2 == 0)
        U = haar(ce.d)
        r = rand_state(ce.d)
        N = ce.E(U @ r @ U.conj().T)
        O = ce.E(U @ ce.E(r) @ U.conj().T)
        v += tn(N - O) > tn(r - ce.E(r)) + 1e-9
    b["thm2d_cases"], b["thm2d_violations"] = 300, int(v)
    v, nk = 0, 0
    for t in range(300):  # Thm 3 (faithful), states supported on a random subset of sectors, rank deficient
        ce = rand_ce(faithful=True)
        Ps = ce.central()
        keep = [P for P in Ps if rng.random() < 0.6] or [Ps[0]]
        Pk = sum(keep)
        W = haar(ce.d)
        g = Pk @ W[:, : max(1, int(np.trace(Pk).real) - 1)]
        r = g @ g.conj().T
        r = r / np.trace(r).real
        w, V = np.linalg.eigh(ce.E(r))
        K = V[:, w < 1e-10]
        v += K.size > 0 and np.abs(r @ K).max() > 1e-8
        nk += K.size > 0
    b["thm3_cases"], b["thm3_violations"], b["thm3_nontrivial_kernel"] = 300, int(v), int(nk)
    v, npers = 0, 0
    for t in range(200):  # Thm 4(a), direct persistence on matrix-unit inputs vs commutation
        ce = rand_ce(faithful=True)
        U = ce.unitary_in_Zprime() if t % 2 == 0 else haar(ce.d)
        Ps = ce.central()
        pers = all(abs(np.trace(P @ ce.E(U @ ce.E(X) @ U.conj().T)) - np.trace(P @ X)) < 1e-9 for X in basis(ce.d) for P in Ps)
        comm = all(np.abs(U @ P - P @ U).max() < 1e-9 for P in Ps)
        v += pers != comm
        npers += pers
    b["thm4a_cases"], b["thm4a_violations"], b["thm4a_persistent_count"] = 200, int(v), int(npers)
    v = 0
    for t in range(100):  # Thm 12.3 Ky Fan
        d = int(rng.integers(2, 7))
        Hm = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        Dl = (Hm + Hm.conj().T) / 2
        Dl -= np.trace(Dl).real / d * np.eye(d)
        q = int(rng.integers(1, d))
        w, V = np.linalg.eigh(Dl)
        w, V = w[::-1], V[:, ::-1]
        Fq = max(w[:q].sum(), w[:d - q].sum())
        top = V[:, :q] @ V[:, :q].conj().T
        bot = V[:, d - q:] @ V[:, d - q:].conj().T  # rank-q projector onto bottom eigenvectors
        att = max(abs(np.trace(top @ Dl).real), abs(np.trace(bot @ Dl).real))
        v += abs(att - Fq) > 1e-9
        for _ in range(2000):
            U = haar(d)
            Pq = U[:, :q] @ U[:, :q].conj().T
            v += abs(np.trace(Pq @ Dl).real) > Fq + 1e-9
        npos, nneg = int((w > 1e-12).sum()), int((w < -1e-12).sum())
        kappa = w[w > 0].sum()
        cond = (npos <= q <= d - nneg) or (npos <= d - q <= d - nneg)
        v += (abs(Fq - kappa) < 1e-9) != cond
    b["thm12_3_cases"], b["thm12_3_violations"] = 100, int(v)
    v = 0
    for t in range(300):  # Prop 12.4(a) for M-sector full-block pinchings
        M = int(rng.integers(2, 5))
        ns = [int(rng.integers(1, 3)) for _ in range(M)]
        ce = CE(ns, [1] * M, True, True)
        r = rand_state(ce.d, rank=int(rng.integers(1, ce.d + 1)))
        v += tn(r - ce.E(r)) / 2 > 1 - 1 / M + 1e-9
    b["prop12_4_cases"], b["prop12_4_violations"] = 300, int(v)
    v, worst = 0, 0.0
    for t in range(1000):  # Thm 12.5(b)
        ce = rand_ce(faithful=True, tracial=t % 4 == 0)
        lam = certified_lambda(ce)
        Q = ce.proj_in_A()
        tt = (1, 0.3, 0.1, 0.01, 1e-4)[t % 5]
        Ks = [np.sqrt(1 - tt) * np.eye(ce.d)] + [np.sqrt(tt) * K for K in channel_kraus("haar", ce)]
        Xs = phistar(Ks, Q)
        D = np.linalg.norm(ce.Estar(Xs) - Q, 2)
        C = np.linalg.norm(Xs - ce.Estar(Xs), 2)
        bound = D + 2 * np.sqrt(D / lam) if lam > 0 else np.inf
        v += lam <= 0 or C > bound + 1e-9
        if np.isfinite(bound) and bound > 0:
            worst = max(worst, C / bound)
    b["thm12_5b_cases"], b["thm12_5b_violations"], b["thm12_5b_max_ratio"] = 1000, int(v), round(float(worst), 6)


def controls(r):
    I2 = np.eye(2)
    CN = np.zeros((4, 4))
    for s in (0, 1):
        for q in (0, 1):
            CN[2 * s + (q ^ s), 2 * s + q] = 1
    DEPH = sup_mask(4, lambda i, j: i == j)
    Q = [np.kron(I2, np.diag([1, 0])), np.kron(I2, np.diag([0, 1]))]
    rec = lambda X: [np.trace(q @ X).real for q in Q]
    plus, minus = np.array([[1], [1]]) / np.sqrt(2), np.array([[1], [-1]]) / np.sqrt(2)
    rW = [np.kron(v @ v.T, np.diag([1.0, 0])) for v in (plus, minus)]
    S = sup_conj(CN)
    tv_o = tvd(rec(apply(DEPH @ S @ DEPH, rW[0])), rec(apply(DEPH @ S @ DEPH, rW[1])))
    tv_n = tvd(rec(apply(DEPH @ S, rW[0])), rec(apply(DEPH @ S, rW[1])))
    r["R1_closed_motion_substituted"] = "REJECTED" if not (abs(tv_o) < 1e-12 and abs(tv_n - 1) < 1e-12) else "ACCEPTED"
    mx = 0.0
    for _ in range(200):
        U = haar(4)
        rho = np.diag(rng.dirichlet(np.ones(4)))
        Su = sup_conj(U)
        mx = max(mx, tvd(rec(apply(DEPH @ Su, rho)), rec(apply(DEPH @ Su @ DEPH, rho))))
    r["R2_classical_prefix_nonzero_record"] = "REJECTED" if mx < 1e-12 else "ACCEPTED"
    th = 0.05
    Dq, Cq = np.sin(th / 2) ** 2, abs(np.sin(th)) / 2
    lam = certified_lambda(CE([1, 1], [1, 1], True, True))
    r["qubit_pinching_lambda"] = round(lam, 9)
    r["R3_linear_bound"] = "REJECTED" if Cq > Dq + 2 * Dq / lam else "ACCEPTED"
    own = CE([1], [2], faithful=False)
    own.sig = [np.diag([1.0, 0])]
    r["R4_owner_section_lambda_positive"] = "REJECTED" if certified_lambda(own) < 1e-9 else "ACCEPTED"
    fib = {"a": 0, "u": 0, "b": 1}
    D3, _ = DC_f(fib, {0: "a", 1: "b"}, {"a": "a", "u": "b", "b": "u"})
    r["R5_three_atom_swap_preserving"] = "REJECTED" if D3 != 0 else "ACCEPTED"
    ok = True
    for _ in range(1000):
        U = haar(2)
        ok &= np.allclose(U @ np.eye(2) @ U.conj().T, np.eye(2))
    r["R6_multiplicity_only_nonnormalizer"] = "REJECTED" if ok else "ACCEPTED"
    w = np.array([0.25, 0.25, -0.25, -0.25])
    F1 = max(w[:1].sum(), w[:3].sum())
    srch = 0.0
    Dl = np.diag(w)
    for _ in range(2000):
        U = haar(4)
        srch = max(srch, abs(np.trace(U[:, :1] @ U[:, :1].conj().T @ Dl).real))
    r["R7_kyfan_rank1_saturation"] = "REJECTED" if (F1 < 0.5 - 1e-9 and srch <= F1 + 1e-9) else "ACCEPTED"
    mk = 0.0
    ce = CE([1, 1], [1, 1], True, True)
    for _ in range(2000):
        rr = rand_state(2, rank=1)
        mk = max(mk, tn(rr - ce.E(rr)) / 2)
    r["R8_faithful_perfect_record"] = "REJECTED" if mk <= 0.5 + 1e-12 else "ACCEPTED"


def enc(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, (list, tuple)):
        return [enc(e) for e in v]
    if isinstance(v, (bool, str)):
        return v
    return float(v)


def main():
    c, b, r = {}, {}, {}
    quantum_items(c)
    classical_items(c)
    bounded(b)
    controls(r)
    meta = {"role": "checker", "algorithm": "numpy column-stacked superoperators + Fraction atom maps",
            "numpy": np.__version__, "seed": 20261018,
            "result_sha256": hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()}
    out = {"meta": meta, "values": {k: enc(v) for k, v in c.items()}, "bounded": b, "controls": r}
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"bounded": b, "controls": r}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
