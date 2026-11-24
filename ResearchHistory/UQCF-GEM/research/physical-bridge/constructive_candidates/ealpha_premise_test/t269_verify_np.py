"""Independent dense-numpy checker for t269_ealpha.py (different construction: dense matrices, Choi matrices,
SVD ranks, float64 entropies with numpy default_rng(269)). Prints JSON of booleans and key numbers."""
import itertools, json
import numpy as np
tol = 1e-10
out = {}
X = ['o', 'p', 'u', 'v']
def C1(rho, P, U, idx):
    Q = np.eye(rho.shape[0]); Q[idx[U], idx[U]] = 0
    r = Q @ rho @ Q
    r[idx[P], idx[P]] += rho[idx[U], idx[U]]
    return r
def choi(ch, n):
    J = None
    for i in range(n):
        for j in range(n):
            E = np.zeros((n, n)); E[i, j] = 1
            t = np.kron(E, ch(E))
            J = t if J is None else J + t
    return J
def ptr(rho, dims, keep):
    n = len(dims); r = rho.reshape(dims + dims)
    tr = [i for i in range(n) if i not in keep]
    for c, i in enumerate(sorted(tr, reverse=True)):
        r = np.trace(r, axis1=i, axis2=i + r.ndim // 2)
    d = int(np.prod([dims[i] for i in keep]))
    return r.reshape(d, d)
def H(p):
    p = np.real(p); p = p[p > 1e-14]; return float(-(p * np.log2(p)).sum())
def S(rho):
    return H(np.linalg.eigvalsh((rho + rho.conj().T) / 2))
def D(a, b):
    return 0.5 * np.abs(np.linalg.eigvalsh(a - b)).sum()
# single-event frames, K = E(x)R, index 2e+r
k = lambda e, r: np.eye(4)[2 * e + r]
s2 = np.sqrt(2); th = np.pi / 8
ga = np.array([[.6, -.8], [.8, .6]]); gb = np.array([[.6, .8j], [.8j, .6]])
G = np.kron(ga, gb)
FR = {'W_R': (k(0, 0), k(0, 1)), 'W_R^g': (G @ k(0, 0), G @ k(0, 1)), 'W_E': (k(0, 0), k(1, 0)),
      'W_Bell': ((k(0, 0) + k(1, 1)) / s2, (k(0, 0) - k(1, 1)) / s2), 'W_W': (k(0, 0), (k(0, 1) + k(1, 0)) / s2),
      'W_ER': (k(0, 0), k(1, 1)), 'W_theta(pi/8)': (np.cos(th) * k(0, 0) + np.sin(th) * k(1, 1), np.cos(th) * k(0, 1) + np.sin(th) * k(1, 0))}
idx = {s: i for i, s in enumerate(X)}
def Wmat(e0, eu):
    W = np.zeros((16, 4), complex)
    for s in X:
        tgt = 'p' if s == 'u' else s
        W[:, idx[s]] = np.kron(np.eye(4)[idx[tgt]], eu if s == 'u' else e0)
    return W
zp = np.diag([1, 1, 2, 1]) / 5; zm = np.diag([1, 1, 1, 2]) / 5
adm = {}
for nm, (e0, eu) in FR.items():
    W = Wmat(e0, eu)
    chW = lambda r, W=W: ptr(W @ r @ W.conj().T, [4, 2, 2], [0])
    okC = np.allclose(choi(chW, 4), choi(lambda r: C1(r, 'p', 'u', idx), 4), atol=tol)
    oE = lambda z: ptr(W @ z @ W.conj().T, [4, 2, 2], [1]); oR = lambda z: ptr(W @ z @ W.conj().T, [4, 2, 2], [2])
    DE, DR = D(oE(zp), oE(zm)), D(oR(zp), oR(zm))
    adm[nm] = {'implements_C': bool(okC), 'D_E': round(DE, 12), 'D_R': round(DR, 12), 'admitted': bool(abs(DE) < tol and abs(DR - .2) < tol)}
out['admission'] = adm
# two-event carriers as dense maps on S(x)E(x)R
def carrier(c):
    if c == 'A':
        S_ = ['o', 'p1', 'u1', 'p2', 'u2', 'v']
        er = lambda kk, s: s == ('u1' if kk == 1 else 'u2'); Pk = lambda kk, s: ('p1' if kk == 1 else 'p2') if er(kk, s) else s
    else:
        S_ = [(a, b) for a in X for b in X]
        er = lambda kk, s: s[kk - 1] == 'u'
        Pk = lambda kk, s: tuple('p' if (i == kk - 1 and s[i] == 'u') else s[i] for i in range(2))
    return S_, er, Pk
def chan_ref(c):
    S_, er, Pk = carrier(c); n = len(S_); ii = {s: i for i, s in enumerate(S_)}
    def Ck(kk, rho):
        # Kraus form C_k(rho) = Q rho Q + L rho L^dag, L = sum_{erased s} |P_k s><s| (keeps coherences in the other factor)
        Q = np.diag([0. if er(kk, s) else 1. for s in S_])
        L = np.zeros((n, n))
        for s in S_:
            if er(kk, s):
                L[ii[Pk(kk, s)], ii[s]] = 1
        return Q @ rho @ Q + L @ rho @ L.T
    return S_, Ck
def build(c, ext):
    S_, er, Pk = carrier(c)
    if ext == 'X1': Ereg, Rreg = [0], [(0, 0), (1, 0), (0, 1), (1, 1)]
    elif ext == 'X3': Ereg, Rreg = [0], [(), (1,), (2,), (1, 2), (2, 1)]
    elif ext == 'OW': Ereg, Rreg = [0, 1, 2], [0, 1, 2]
    elif ext in ('OR', 'XOR'): Ereg, Rreg = [0], [0, 1]
    basis = [(s, e, r) for s in S_ for e in Ereg for r in Rreg]; ib = {b: i for i, b in enumerate(basis)}
    def wr(kk, e, r):
        if ext == 'X1':
            if r[kk - 1]: return None
            r = list(r); r[kk - 1] = 1; return e, tuple(r)
        if ext == 'X3':
            return (e, r + (kk,)) if kk not in r and len(r) < 2 else None
        if ext == 'OW': return (r, kk) if e == 0 else None
        if ext == 'OR': return e, 1
        if ext == 'XOR': return e, 1 - r
    V = {}
    for kk in (1, 2):
        M = np.zeros((len(basis), len(basis)))
        for (s, e, r) in basis:
            if er(kk, s):
                w = wr(kk, e, r)
                if w is None: continue
                M[ib[(Pk(kk, s),) + w], ib[(s, e, r)]] = 1
            else:
                M[ib[(s, e, r)], ib[(s, e, r)]] = 1
        V[kk] = M
    fresh = (0, (0, 0) if ext == 'X1' else (() if ext == 'X3' else 0))
    F = np.zeros((len(basis), len(S_)))
    for j, s in enumerate(S_): F[ib[(s,) + fresh], j] = 1
    return S_, basis, V, F, (len(S_), len(Ereg), len(Rreg)), Rreg
def analyze(c, ext, relabel=None):
    S_, basis, V, F, dims, Rreg = build(c, ext); _, Ck = chan_ref(c); n = len(S_)
    V12 = V[1] @ V[2] @ F; V21 = V[2] @ V[1] @ F
    iso = np.allclose(V12.T @ V12, np.eye(n)) and np.allclose(V21.T @ V21, np.eye(n))
    SE = lambda W: (lambda r: ptr(W @ r @ W.conj().T, list(dims), [0, 1]))
    Sm = lambda W: (lambda r: ptr(W @ r @ W.conj().T, list(dims), [0]))
    O = np.allclose(choi(SE(V12), n), choi(SE(V21), n), atol=tol)
    comp = np.allclose(choi(Sm(V12), n), choi(lambda r: Ck(1, Ck(2, r)), n), atol=tol)
    res = {'isometric_composites': bool(iso), 'O': bool(O), 'composite_C1C2': bool(comp)}
    if relabel is not None:
        P = np.zeros((len(Rreg), len(Rreg)))
        for i, r in enumerate(Rreg): P[Rreg.index(relabel(r)), i] = 1
        U = np.kron(np.eye(dims[0] * dims[1]), P)
        res['explicit_U'] = bool(np.allclose(V12, U @ V21))
    if ext in ('X1', 'X3'):
        if c == 'A':
            pr = {1: ([1, 1, 4, 1, 1, 2], [1, 1, 2, 1, 1, 4]), 2: ([1, 1, 1, 1, 4, 2], [1, 1, 1, 1, 2, 4])}
            pr = {kk: tuple(np.diag(np.array(z) / 10) for z in v) for kk, v in pr.items()}
        else:
            pr = {1: (np.kron(zp, zp), np.kron(zm, zp)), 2: (np.kron(zp, zp), np.kron(zp, zm))}
        for kk, (a, b) in pr.items():
            oa, ob = V12 @ a @ V12.T, V12 @ b @ V12.T
            res['event%d_DE_DR' % kk] = [round(D(ptr(oa, list(dims), [1]), ptr(ob, list(dims), [1])), 12), round(D(ptr(oa, list(dims), [2]), ptr(ob, list(dims), [2])), 12)]
    return res
pa = {}
swap = lambda r: {(1, 2): (2, 1), (2, 1): (1, 2)}.get(r, r)
for c in ('A', 'B'):
    pa[c] = {'X1': analyze(c, 'X1', relabel=lambda r: r), 'X3': analyze(c, 'X3', relabel=swap), 'X3_identityU': analyze(c, 'X3', relabel=lambda r: r)}
    for rule in ('OR', 'XOR'):
        pa[c][rule] = analyze(c, rule)
    # Choi rank of C1C2 via SVD
    S_, Ck = chan_ref(c); n = len(S_)
    pa[c]['choi_rank_C1C2'] = int(np.linalg.matrix_rank(choi(lambda r: Ck(1, Ck(2, r)), n), tol=1e-9))
pa['B']['overwrite'] = analyze('B', 'OW')
out['P_a'] = pa
# P-b float check, numpy default_rng(269), 2000 inputs
rng = np.random.default_rng(269)
pb = {}
ins = []
for t in range(2000):
    rk = 1 + t % 4; A = rng.normal(size=(4, rk)) + 1j * rng.normal(size=(4, rk)); r = A @ A.conj().T; ins.append(r / np.trace(r).real)
ins.append(np.diag([0, .5, .5, 0]))
for nm, (e0, eu) in FR.items():
    W = Wmat(e0, eu); mR = 9; mK = 9; mE = 0
    for r in ins:
        om = W @ r @ W.conj().T; dS = S(r) - S(C1(r, 'p', 'u', idx))
        mR = min(mR, S(ptr(om, [4, 2, 2], [2])) - dS); mK = min(mK, S(ptr(om, [4, 2, 2], [1, 2])) - dS); mE = max(mE, S(ptr(om, [4, 2, 2], [1])))
    pb[nm] = {'min_slack_R': round(mR, 9), 'min_slack_K': round(mK, 9), 'max_S_E': round(mE, 9)}
out['P_b'] = pb
print(json.dumps(out, indent=1, sort_keys=True))
