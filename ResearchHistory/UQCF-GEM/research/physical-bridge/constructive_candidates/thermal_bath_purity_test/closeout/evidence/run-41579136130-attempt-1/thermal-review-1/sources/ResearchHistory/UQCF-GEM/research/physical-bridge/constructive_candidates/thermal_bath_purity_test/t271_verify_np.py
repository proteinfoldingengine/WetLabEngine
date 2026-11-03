"""Independent numpy checker for T-271 (different construction: explicit Kraus-from-unitary channel, Choi comparison)."""
import json, numpy as np
o, p, u, v = 0, 1, 2, 3
def C_kraus():
    Q = np.diag([1., 1, 0, 1]); L = np.zeros((4, 4)); L[p, u] = 1; return [Q, L]
def choi_from_kraus(Ks, n=4):
    J = 0
    for K in Ks:
        vec = np.zeros((n * K.shape[0],), complex)
        for i in range(n):
            e = np.zeros(n); e[i] = 1; vec += np.kron(e, K @ e)
        J = J + np.outer(vec, vec.conj())
    return J
def kraus_of(U, sE, sR, dE, dR=2):
    """Kraus ops of rho -> Tr_ER U (rho (x) sE (x) sR) U^dag via spectral decomposition of env states."""
    env = np.kron(sE, sR); w, V = np.linalg.eigh(env); Ks = []
    for a in range(len(w)):
        if w[a] < 1e-15: continue
        for b in range(dE * dR):
            K = np.zeros((4, 4), complex)
            for i in range(4):
                for j in range(4):
                    for c in range(dE * dR):
                        K[i, j] += np.sqrt(w[a]) * U[i * dE * dR + b, j * dE * dR + c] * V[c, a]
            Ks.append(K)
    return Ks
def perm(f, dE, dR=2):
    n = 4 * dE * dR; U = np.zeros((n, n))
    for s in range(4):
        for e in range(dE):
            for r in range(dR):
                t = f(s, e, r); U[(t[0] * dE + t[1]) * dR + t[2], (s * dE + e) * dR + r] = 1
    return U
WR = perm(lambda s, e, r: (p, e, 1) if (s, r) == (u, 0) else ((u, e, 0) if (s, r) == (p, 1) else (s, e, r)), 2)
WE = perm(lambda s, e, r: (p, 1, r) if (s, e) == (u, 0) else ((u, 0, r) if (s, e) == (p, 1) else (s, e, r)), 2)
SW = np.zeros((16, 16))
for s in range(4):
    for e in range(2):
        for r in range(2):
            SW[(s * 2 + r) * 2 + e, (s * 2 + e) * 2 + r] = 1
WRS = SW @ WR
def iso_from_frames(fr):  # fr[k] = (e0, eu) for E-input k, R-input 0; R-input-1 columns via QR completion
    M = np.zeros((16, 16), complex); cols = []
    for k, (e0, eu) in enumerate(fr):
        for s in range(4):
            out = np.kron(np.eye(4)[p if s == u else s], eu if s == u else e0)
            M[:, (s * 2 + k) * 2] = out; cols.append((s * 2 + k) * 2)
    A = M[:, cols]; Qc, _ = np.linalg.qr(np.hstack([A, np.eye(16)]))
    comp = [c for c in range(16) if c not in cols]; extra = Qc[:, 8:16]
    for i, c in enumerate(comp): M[:, c] = extra[:, i]
    return M
k = lambda e, r: np.eye(4)[e * 2 + r]; h = 1 / np.sqrt(2)
FR = {'W_E^c': [(k(0, 0), k(1, 0)), (k(1, 1), k(0, 1))],
      'W_Bell^c': [((k(0, 0) + k(1, 1)) * h, (k(0, 0) - k(1, 1)) * h), (k(1, 0), k(0, 1))],
      'W_W^c': [(k(0, 0), (k(0, 1) + k(1, 0)) * h), ((k(1, 0) - k(0, 1)) * h, k(1, 1))]}
U_ = {'W_R(x)I_E': WR, 'W_E_fixed_mirror': WE, 'W_R;SWAP': WRS, **{n: iso_from_frames(f) for n, f in FR.items()}}
JC = choi_from_kraus(C_kraus()); blank = np.diag([1., 0]); out = {}
rs = np.diag([0, .5, .5, 0])
for tn, t in (('tau_q', np.diag([2 / 3, 1 / 3])), ('tau_half', np.diag([.5, .5]))):
    r = {}
    for n, U in U_.items():
        assert np.allclose(U.conj().T @ U, np.eye(16))
        Ks = kraus_of(U, t, blank, 2); J = choi_from_kraus(Ks)
        pv = sum((K @ rs @ K.conj().T)[p, p].real for K in Ks)
        r[n] = {'realizes_C': bool(np.allclose(J, JC, atol=1e-12)), 'p_value': round(float(pv), 12)}
    ev = sorted(np.kron(np.diag(rs), np.diag(t)), reverse=True); r['KF'] = round(float(sum(ev[:2])), 12)
    out[tn] = r
tq = np.diag([2 / 3, 1 / 3]); sw = {}
for n, U in (('W_E(x)I_R', WE), ('W_R(x)I_E', WR)):
    Ks = kraus_of(U, blank, tq, 2); sw[n] = bool(np.allclose(choi_from_kraus(Ks), JC, atol=1e-12))
out['swapped_world_realizes_C'] = sw
Ut = perm(lambda s, e, r: (p, e + 2, r) if (s == u and e < 2) else ((u, e - 2, r) if (s == p and e >= 2) else (s, e, r)), 4)
Ks = kraus_of(Ut, np.diag([.5, .5, 0, 0]), blank, 4); out['dE4_rank2_R_untouched_realizes_C'] = bool(np.allclose(choi_from_kraus(Ks), JC, atol=1e-12))
Ks = kraus_of(Ut, np.diag([1 / 3, 1 / 3, 1 / 3, 0]), blank, 4); out['dE4_rank3_p_value'] = round(float(sum((K @ rs @ K.conj().T)[p, p].real for K in Ks)), 12)
print(json.dumps(out, indent=1, sort_keys=True))
